-- Projects-Hours: project management + time tracking
-- Run this in the Supabase SQL editor against the gbkhkbfbarsnpbdkxzii project.
-- Idempotent: safe to re-run.

-- ============================================================
-- TEAM MEMBERS
-- ============================================================
create table if not exists ph_team_members (
    id              bigserial primary key,
    name            text not null,
    email           text unique,
    role            text,                       -- e.g. "Developer", "Designer", "PM"
    hourly_rate     numeric(10,2),              -- optional, for cost reporting
    avatar_color    text default '#6c757d',     -- hex color for UI
    active          boolean not null default true,
    created_at      timestamptz not null default now()
);

-- ============================================================
-- PROJECTS
-- ============================================================
create table if not exists ph_projects (
    id              bigserial primary key,
    name            text not null,
    code            text unique,                -- short code like "AMZ-INTEL"
    purpose         text,                       -- the "why"
    description     text,                       -- the "what"
    status          text not null default 'planning'
                    check (status in ('planning','active','on_hold','completed','cancelled')),
    priority        text default 'medium'
                    check (priority in ('low','medium','high','urgent')),
    start_date      date,
    target_end_date date,
    actual_end_date date,
    owner_id        bigint references ph_team_members(id) on delete set null,
    color           text default '#0d6efd',     -- hex color for timeline bars
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

create index if not exists idx_ph_projects_status on ph_projects(status);
create index if not exists idx_ph_projects_dates  on ph_projects(start_date, target_end_date);

-- ============================================================
-- PROJECT MEMBERSHIPS (many-to-many: who works on which project)
-- ============================================================
create table if not exists ph_project_members (
    project_id      bigint not null references ph_projects(id) on delete cascade,
    member_id       bigint not null references ph_team_members(id) on delete cascade,
    role_on_project text,                       -- e.g. "Lead", "Contributor"
    added_at        timestamptz not null default now(),
    primary key (project_id, member_id)
);

-- ============================================================
-- TASKS
-- ============================================================
create table if not exists ph_tasks (
    id              bigserial primary key,
    project_id      bigint not null references ph_projects(id) on delete cascade,
    parent_task_id  bigint references ph_tasks(id) on delete set null,
    title           text not null,
    description     text,
    status          text not null default 'todo'
                    check (status in ('todo','in_progress','blocked','review','done','cancelled')),
    priority        text default 'medium'
                    check (priority in ('low','medium','high','urgent')),
    assigned_to     bigint references ph_team_members(id) on delete set null,
    estimated_hours numeric(6,2),
    due_date        date,
    completed_at    timestamptz,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

create index if not exists idx_ph_tasks_project on ph_tasks(project_id);
create index if not exists idx_ph_tasks_assignee on ph_tasks(assigned_to);
create index if not exists idx_ph_tasks_status on ph_tasks(status);

-- ============================================================
-- MILESTONES (timeline anchors per project)
-- ============================================================
create table if not exists ph_milestones (
    id              bigserial primary key,
    project_id      bigint not null references ph_projects(id) on delete cascade,
    title           text not null,
    description     text,
    target_date     date not null,
    completed       boolean not null default false,
    completed_at    timestamptz,
    created_at      timestamptz not null default now()
);

create index if not exists idx_ph_milestones_project on ph_milestones(project_id);

-- ============================================================
-- TIME ENTRIES (clock in / clock out)
-- ============================================================
-- A row with clock_out IS NULL means "currently clocked in".
-- duration_minutes is auto-computed when clock_out is set.
create table if not exists ph_time_entries (
    id              bigserial primary key,
    member_id       bigint not null references ph_team_members(id) on delete cascade,
    project_id      bigint references ph_projects(id) on delete set null,
    task_id         bigint references ph_tasks(id) on delete set null,
    clock_in        timestamptz not null default now(),
    clock_out       timestamptz,
    duration_minutes integer
                    generated always as (
                        case when clock_out is null then null
                        else greatest(0, extract(epoch from (clock_out - clock_in))::integer / 60)
                        end
                    ) stored,
    notes           text,
    created_at      timestamptz not null default now()
);

create index if not exists idx_ph_time_member  on ph_time_entries(member_id);
create index if not exists idx_ph_time_project on ph_time_entries(project_id);
create index if not exists idx_ph_time_task    on ph_time_entries(task_id);
create index if not exists idx_ph_time_open    on ph_time_entries(member_id) where clock_out is null;

-- Only one open clock per member at a time.
create unique index if not exists uq_ph_time_one_open_per_member
    on ph_time_entries(member_id)
    where clock_out is null;

-- ============================================================
-- PROJECT UPDATES / TEAM COMMUNICATION
-- ============================================================
-- Free-form messages on a project so teams can communicate (status updates,
-- blockers, decisions). Linkable to a task.
create table if not exists ph_project_updates (
    id              bigserial primary key,
    project_id      bigint not null references ph_projects(id) on delete cascade,
    task_id         bigint references ph_tasks(id) on delete set null,
    author_id       bigint references ph_team_members(id) on delete set null,
    kind            text not null default 'note'
                    check (kind in ('note','status','blocker','decision','question')),
    body            text not null,
    created_at      timestamptz not null default now()
);

create index if not exists idx_ph_updates_project on ph_project_updates(project_id, created_at desc);

-- ============================================================
-- VIEW: hours rolled up per project / member
-- ============================================================
create or replace view ph_hours_summary as
select
    te.member_id,
    m.name as member_name,
    te.project_id,
    p.name as project_name,
    count(*) as session_count,
    coalesce(sum(te.duration_minutes), 0) as total_minutes,
    round(coalesce(sum(te.duration_minutes), 0) / 60.0, 2) as total_hours
from ph_time_entries te
left join ph_team_members m on m.id = te.member_id
left join ph_projects     p on p.id = te.project_id
where te.clock_out is not null
group by te.member_id, m.name, te.project_id, p.name;

-- ============================================================
-- TRIGGER: keep updated_at fresh
-- ============================================================
create or replace function ph_touch_updated_at() returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_ph_projects_updated on ph_projects;
create trigger trg_ph_projects_updated
    before update on ph_projects
    for each row execute function ph_touch_updated_at();

drop trigger if exists trg_ph_tasks_updated on ph_tasks;
create trigger trg_ph_tasks_updated
    before update on ph_tasks
    for each row execute function ph_touch_updated_at();
