"""
Projects-Hours — FastAPI project management + time tracking app.
Backed by Supabase (same project as ../amin).

Run locally:
    pip install -r requirements.txt
    uvicorn app:app --reload --port 8001
"""

import os
import logging
from datetime import datetime, date, timezone
from typing import Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Projects-Hours", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def _empty_to_none(v: Optional[str]) -> Optional[str]:
    if v is None:
        return None
    v = v.strip()
    return v or None


def _parse_date(v: Optional[str]) -> Optional[str]:
    v = _empty_to_none(v)
    if not v:
        return None
    # HTML date input is already YYYY-MM-DD
    return v


def _parse_int(v: Optional[str]) -> Optional[int]:
    v = _empty_to_none(v)
    if v is None:
        return None
    try:
        return int(v)
    except ValueError:
        return None


def _parse_float(v: Optional[str]) -> Optional[float]:
    v = _empty_to_none(v)
    if v is None:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _open_clock_for(member_id: int):
    res = (sb.table("ph_time_entries")
           .select("*")
           .eq("member_id", member_id)
           .is_("clock_out", "null")
           .limit(1)
           .execute())
    return (res.data or [None])[0]


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    projects = (sb.table("ph_projects")
                .select("*")
                .order("created_at", desc=True)
                .execute()).data or []

    # Tally task counts and open clocks per project
    task_counts = {}
    if projects:
        ids = [p["id"] for p in projects]
        tasks = (sb.table("ph_tasks")
                 .select("project_id,status")
                 .in_("project_id", ids)
                 .execute()).data or []
        for t in tasks:
            d = task_counts.setdefault(t["project_id"], {"total": 0, "done": 0, "in_progress": 0})
            d["total"] += 1
            if t["status"] == "done":
                d["done"] += 1
            elif t["status"] == "in_progress":
                d["in_progress"] += 1

    open_clocks = (sb.table("ph_time_entries")
                   .select("*, ph_team_members(name), ph_projects(name)")
                   .is_("clock_out", "null")
                   .execute()).data or []

    return templates.TemplateResponse(request, "dashboard.html", {
        "projects": projects,
        "task_counts": task_counts,
        "open_clocks": open_clocks,
    })


# ─────────────────────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────────────────────
@app.get("/projects/new", response_class=HTMLResponse)
async def new_project_form(request: Request):
    members = (sb.table("ph_team_members")
               .select("*")
               .eq("active", True)
               .order("name")
               .execute()).data or []
    return templates.TemplateResponse(request, "project_form.html", {
        "members": members,
        "project": None,
    })


@app.post("/projects")
async def create_project(
    name: str = Form(...),
    code: Optional[str] = Form(None),
    purpose: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    status: str = Form("planning"),
    priority: str = Form("medium"),
    start_date: Optional[str] = Form(None),
    target_end_date: Optional[str] = Form(None),
    owner_id: Optional[str] = Form(None),
    color: Optional[str] = Form("#0d6efd"),
):
    payload = {
        "name": name.strip(),
        "code": _empty_to_none(code),
        "purpose": _empty_to_none(purpose),
        "description": _empty_to_none(description),
        "status": status,
        "priority": priority,
        "start_date": _parse_date(start_date),
        "target_end_date": _parse_date(target_end_date),
        "owner_id": _parse_int(owner_id),
        "color": _empty_to_none(color) or "#0d6efd",
    }
    res = sb.table("ph_projects").insert(payload).execute()
    pid = res.data[0]["id"]
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.get("/projects/{pid}", response_class=HTMLResponse)
async def project_detail(request: Request, pid: int):
    proj = (sb.table("ph_projects").select("*").eq("id", pid).single().execute()).data
    if not proj:
        raise HTTPException(404, "Project not found")

    tasks = (sb.table("ph_tasks")
             .select("*, assignee:ph_team_members!ph_tasks_assigned_to_fkey(name,avatar_color)")
             .eq("project_id", pid)
             .order("created_at", desc=True)
             .execute()).data or []

    milestones = (sb.table("ph_milestones")
                  .select("*")
                  .eq("project_id", pid)
                  .order("target_date")
                  .execute()).data or []

    updates = (sb.table("ph_project_updates")
               .select("*, author:ph_team_members(name,avatar_color)")
               .eq("project_id", pid)
               .order("created_at", desc=True)
               .limit(50)
               .execute()).data or []

    members = (sb.table("ph_team_members")
               .select("*")
               .eq("active", True)
               .order("name")
               .execute()).data or []

    # Hours per member on this project
    hours = (sb.table("ph_hours_summary")
             .select("*")
             .eq("project_id", pid)
             .execute()).data or []

    return templates.TemplateResponse(request, "project_detail.html", {
        "project": proj,
        "tasks": tasks,
        "milestones": milestones,
        "updates": updates,
        "members": members,
        "hours": hours,
    })


@app.post("/projects/{pid}/status")
async def update_project_status(pid: int, status: str = Form(...)):
    sb.table("ph_projects").update({"status": status}).eq("id", pid).execute()
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.post("/projects/{pid}/delete")
async def delete_project(pid: int):
    sb.table("ph_projects").delete().eq("id", pid).execute()
    return RedirectResponse("/", status_code=303)


# ─────────────────────────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────────────────────────
@app.post("/projects/{pid}/tasks")
async def create_task(
    pid: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    status: str = Form("todo"),
    priority: str = Form("medium"),
    assigned_to: Optional[str] = Form(None),
    estimated_hours: Optional[str] = Form(None),
    due_date: Optional[str] = Form(None),
):
    payload = {
        "project_id": pid,
        "title": title.strip(),
        "description": _empty_to_none(description),
        "status": status,
        "priority": priority,
        "assigned_to": _parse_int(assigned_to),
        "estimated_hours": _parse_float(estimated_hours),
        "due_date": _parse_date(due_date),
    }
    sb.table("ph_tasks").insert(payload).execute()
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.post("/tasks/{tid}/status")
async def update_task_status(tid: int, status: str = Form(...)):
    update = {"status": status}
    if status == "done":
        update["completed_at"] = datetime.now(timezone.utc).isoformat()
    else:
        update["completed_at"] = None
    res = sb.table("ph_tasks").update(update).eq("id", tid).execute()
    pid = res.data[0]["project_id"] if res.data else None
    return RedirectResponse(f"/projects/{pid}" if pid else "/", status_code=303)


@app.post("/tasks/{tid}/delete")
async def delete_task(tid: int):
    row = sb.table("ph_tasks").select("project_id").eq("id", tid).single().execute().data
    sb.table("ph_tasks").delete().eq("id", tid).execute()
    pid = row["project_id"] if row else None
    return RedirectResponse(f"/projects/{pid}" if pid else "/", status_code=303)


# ─────────────────────────────────────────────────────────────
# MILESTONES
# ─────────────────────────────────────────────────────────────
@app.post("/projects/{pid}/milestones")
async def create_milestone(
    pid: int,
    title: str = Form(...),
    target_date: str = Form(...),
    description: Optional[str] = Form(None),
):
    sb.table("ph_milestones").insert({
        "project_id": pid,
        "title": title.strip(),
        "target_date": target_date,
        "description": _empty_to_none(description),
    }).execute()
    return RedirectResponse(f"/projects/{pid}", status_code=303)


@app.post("/milestones/{mid}/toggle")
async def toggle_milestone(mid: int):
    row = sb.table("ph_milestones").select("*").eq("id", mid).single().execute().data
    if not row:
        raise HTTPException(404)
    update = {
        "completed": not row["completed"],
        "completed_at": datetime.now(timezone.utc).isoformat() if not row["completed"] else None,
    }
    sb.table("ph_milestones").update(update).eq("id", mid).execute()
    return RedirectResponse(f"/projects/{row['project_id']}", status_code=303)


# ─────────────────────────────────────────────────────────────
# UPDATES (team communication)
# ─────────────────────────────────────────────────────────────
@app.post("/projects/{pid}/updates")
async def post_update(
    pid: int,
    body: str = Form(...),
    kind: str = Form("note"),
    author_id: Optional[str] = Form(None),
    task_id: Optional[str] = Form(None),
):
    sb.table("ph_project_updates").insert({
        "project_id": pid,
        "task_id": _parse_int(task_id),
        "author_id": _parse_int(author_id),
        "kind": kind,
        "body": body.strip(),
    }).execute()
    return RedirectResponse(f"/projects/{pid}#updates", status_code=303)


# ─────────────────────────────────────────────────────────────
# TEAM MEMBERS
# ─────────────────────────────────────────────────────────────
@app.get("/team", response_class=HTMLResponse)
async def team_page(request: Request):
    members = (sb.table("ph_team_members")
               .select("*")
               .order("active", desc=True)
               .order("name")
               .execute()).data or []

    # Add open-clock + total hours info per member
    open_clocks = (sb.table("ph_time_entries")
                   .select("member_id,clock_in,project_id,task_id, ph_projects(name)")
                   .is_("clock_out", "null")
                   .execute()).data or []
    open_by_member = {oc["member_id"]: oc for oc in open_clocks}

    hours_rows = (sb.table("ph_hours_summary").select("*").execute()).data or []
    hours_by_member = {}
    for h in hours_rows:
        hours_by_member[h["member_id"]] = hours_by_member.get(h["member_id"], 0) + (h["total_hours"] or 0)

    for m in members:
        m["open_clock"] = open_by_member.get(m["id"])
        m["total_hours"] = round(hours_by_member.get(m["id"], 0), 2)

    # Active projects for the clock-in dropdown
    projects = (sb.table("ph_projects")
                .select("id,name,code,color")
                .neq("status", "completed")
                .neq("status", "cancelled")
                .order("name")
                .execute()).data or []

    return templates.TemplateResponse(request, "team.html", {
        "members": members,
        "projects": projects,
    })


@app.post("/team")
async def create_member(
    name: str = Form(...),
    email: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    hourly_rate: Optional[str] = Form(None),
    avatar_color: Optional[str] = Form("#6c757d"),
):
    sb.table("ph_team_members").insert({
        "name": name.strip(),
        "email": _empty_to_none(email),
        "role": _empty_to_none(role),
        "hourly_rate": _parse_float(hourly_rate),
        "avatar_color": _empty_to_none(avatar_color) or "#6c757d",
    }).execute()
    return RedirectResponse("/team", status_code=303)


@app.post("/team/{mid}/toggle")
async def toggle_member(mid: int):
    row = sb.table("ph_team_members").select("active").eq("id", mid).single().execute().data
    if not row:
        raise HTTPException(404)
    sb.table("ph_team_members").update({"active": not row["active"]}).eq("id", mid).execute()
    return RedirectResponse("/team", status_code=303)


# ─────────────────────────────────────────────────────────────
# CLOCK IN / OUT (time tracking)
# ─────────────────────────────────────────────────────────────
@app.post("/clock-in")
async def clock_in(
    member_id: int = Form(...),
    project_id: Optional[str] = Form(None),
    task_id: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
):
    if _open_clock_for(member_id):
        raise HTTPException(400, "Member already clocked in. Clock out first.")
    sb.table("ph_time_entries").insert({
        "member_id": member_id,
        "project_id": _parse_int(project_id),
        "task_id": _parse_int(task_id),
        "notes": _empty_to_none(notes),
    }).execute()
    referer = "/"
    if project_id:
        referer = f"/projects/{project_id}"
    return RedirectResponse(referer, status_code=303)


@app.post("/clock-out")
async def clock_out(
    member_id: int = Form(...),
    notes: Optional[str] = Form(None),
):
    open_entry = _open_clock_for(member_id)
    if not open_entry:
        raise HTTPException(400, "No open clock entry for this member.")
    update = {"clock_out": datetime.now(timezone.utc).isoformat()}
    if _empty_to_none(notes):
        # append, don't overwrite
        existing = open_entry.get("notes") or ""
        update["notes"] = (existing + "\n" + notes.strip()).strip() if existing else notes.strip()
    sb.table("ph_time_entries").update(update).eq("id", open_entry["id"]).execute()
    pid = open_entry.get("project_id")
    return RedirectResponse(f"/projects/{pid}" if pid else "/", status_code=303)


# ─────────────────────────────────────────────────────────────
# HOURS REPORT
# ─────────────────────────────────────────────────────────────
@app.get("/hours", response_class=HTMLResponse)
async def hours_report(request: Request):
    summary = (sb.table("ph_hours_summary").select("*").execute()).data or []

    recent = (sb.table("ph_time_entries")
              .select("*, ph_team_members(name,avatar_color), ph_projects(name,color), ph_tasks(title)")
              .order("clock_in", desc=True)
              .limit(100)
              .execute()).data or []

    # Totals
    total_hours = sum(s.get("total_hours") or 0 for s in summary)
    by_member = {}
    by_project = {}
    for s in summary:
        by_member[s["member_name"]] = by_member.get(s["member_name"], 0) + (s["total_hours"] or 0)
        if s.get("project_name"):
            by_project[s["project_name"]] = by_project.get(s["project_name"], 0) + (s["total_hours"] or 0)

    return templates.TemplateResponse(request, "hours.html", {
        "summary": summary,
        "recent": recent,
        "total_hours": round(total_hours, 2),
        "by_member": sorted(by_member.items(), key=lambda x: -x[1]),
        "by_project": sorted(by_project.items(), key=lambda x: -x[1]),
    })


# ─────────────────────────────────────────────────────────────
# TIMELINE (cross-project Gantt)
# ─────────────────────────────────────────────────────────────
@app.get("/timeline", response_class=HTMLResponse)
async def timeline(request: Request):
    projects = (sb.table("ph_projects")
                .select("*")
                .neq("status", "cancelled")
                .order("start_date")
                .execute()).data or []

    milestones = (sb.table("ph_milestones")
                  .select("*, ph_projects(name,color)")
                  .order("target_date")
                  .execute()).data or []

    # Compute timeline bounds
    today = date.today()
    all_dates = []
    for p in projects:
        if p.get("start_date"):
            all_dates.append(date.fromisoformat(p["start_date"]))
        if p.get("target_end_date"):
            all_dates.append(date.fromisoformat(p["target_end_date"]))
    if not all_dates:
        all_dates = [today]

    range_start = min(all_dates + [today])
    range_end = max(all_dates + [today])
    span_days = max(1, (range_end - range_start).days + 1)

    # Build bars
    bars = []
    for p in projects:
        s = p.get("start_date")
        e = p.get("target_end_date") or p.get("actual_end_date")
        if not s:
            continue
        s_d = date.fromisoformat(s)
        e_d = date.fromisoformat(e) if e else today
        offset = (s_d - range_start).days
        length = max(1, (e_d - s_d).days + 1)
        bars.append({
            "project": p,
            "left_pct": (offset / span_days) * 100,
            "width_pct": (length / span_days) * 100,
            "start": s_d.isoformat(),
            "end": e_d.isoformat(),
        })

    return templates.TemplateResponse(request, "timeline.html", {
        "projects": projects,
        "bars": bars,
        "milestones": milestones,
        "range_start": range_start.isoformat(),
        "range_end": range_end.isoformat(),
        "span_days": span_days,
        "today_offset_pct": max(0, min(100, ((today - range_start).days / span_days) * 100)),
    })


# ─────────────────────────────────────────────────────────────
# JSON API (for any future frontend integrations)
# ─────────────────────────────────────────────────────────────
@app.get("/api/projects")
async def api_projects():
    return JSONResponse((sb.table("ph_projects").select("*").execute()).data or [])


@app.get("/api/projects/{pid}/tasks")
async def api_tasks(pid: int):
    return JSONResponse((sb.table("ph_tasks").select("*").eq("project_id", pid).execute()).data or [])


@app.get("/api/hours/summary")
async def api_hours_summary():
    return JSONResponse((sb.table("ph_hours_summary").select("*").execute()).data or [])


@app.get("/healthz")
async def healthz():
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}
