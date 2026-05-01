# Projects-Hours

A FastAPI project management + time tracking app for cross-team collaboration.
Backed by the same Supabase project as `../amin`.

## Features

- **Projects** — name, code, purpose, description, status, priority, dates, color, owner
- **Tasks** — per-project, with status, priority, assignee, estimated hours, due date
- **Milestones** — date-anchored project goals, mark complete
- **Timeline** — Gantt-style view of all projects with a "today" marker
- **Team members** — name, role, email, hourly rate, avatar color
- **Time tracking** — clock in / clock out per member, per project, per task. One open clock per member at a time.
- **Updates** — team communication (notes, status, blockers, decisions, questions) per project
- **Hours report** — totals by member, by project, plus recent sessions

## Setup

### 1. Run database migrations

Open the Supabase SQL editor for the `gbkhkbfbarsnpbdkxzii` project and run the entire contents of `migrations.sql`.

All tables are prefixed with `ph_` so they don't collide with the `amin` app.

### 2. Install dependencies

```bash
cd C:/windows32/projects-hours
python -m venv .venv
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Run

```bash
uvicorn app:app --reload --port 8001
```

Then open http://localhost:8001

> Note: the `amin` app runs on the default port (8000), so use `--port 8001` here.

## Data model

```
ph_team_members ──┬─< ph_project_members >── ph_projects
                  │                              │
                  │                              ├─< ph_tasks
                  │                              │     │
                  └────< ph_time_entries >───────┴─────┘
                                ▲
                                └ one open clock per member (DB constraint)
```

- `ph_projects` — projects with timeline (`start_date`, `target_end_date`)
- `ph_tasks` — work units within a project (with `parent_task_id` for sub-tasks)
- `ph_milestones` — date markers on the timeline
- `ph_time_entries` — clock-in/out sessions; `duration_minutes` auto-computed
- `ph_project_updates` — chat-style team communication on a project
- `ph_hours_summary` — view aggregating hours per member/project

## How time tracking works

1. Add team members on `/team`
2. Open a project, go to the **Clock In/Out** tab
3. Pick a member (and optionally a task), add notes, click **Start clock**
4. Later, on the same tab (or any project page), pick the member and click **Stop clock**
5. Hours roll up automatically into `/hours` and the project's **Hours** tab

The DB enforces only one open clock per member — if they try to clock in twice, the API returns 400.

## Routes

- `/` — dashboard with project cards + active clocks
- `/projects/new` — new project form
- `/projects/{id}` — project detail (tasks, milestones, updates, clock, hours)
- `/team` — team member CRUD
- `/timeline` — cross-project Gantt view
- `/hours` — hours report
- `/api/projects`, `/api/projects/{id}/tasks`, `/api/hours/summary` — JSON
- `/healthz` — liveness check
