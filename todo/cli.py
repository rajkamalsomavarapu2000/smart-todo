import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .db import init_db, get_conn
from .utils import now_iso, join_tags

app = typer.Typer(add_completion=False)
console = Console()

@app.callback()
def startup():
    init_db()

@app.command()
def add(
    title: str = typer.Argument(...),
    notes: str = typer.Option("", "--notes"),
    tag: List[str] = typer.Option([], "--tag"),
    due: Optional[str] = typer.Option(None, "--due", help="ISO date e.g. 2026-02-10"),
):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO tasks (title, notes, tags, created_at, due_at, done)
            VALUES (?, ?, ?, ?, ?, 0)
            """,
            (title, notes, join_tags(tag), now_iso(), due),
        )
        conn.commit()

    console.print(Panel.fit(
        f"[bold green]Task Added[/bold green]\n{title}",
        border_style="green"
    ))

@app.command()
def list(
    all: bool = typer.Option(False, "--all", help="Include completed tasks")
):
    query = "SELECT * FROM tasks"
    if not all:
        query += " WHERE done = 0"
    query += " ORDER BY id DESC"

    with get_conn() as conn:
        rows = conn.execute(query).fetchall()

    table = Table(title="📝 Tasks", show_lines=True)
    table.add_column("ID", justify="right")
    table.add_column("Title", overflow="fold")
    table.add_column("Tags")
    table.add_column("Due")
    table.add_column("Done", justify="center")

    for r in rows:
        table.add_row(
            str(r["id"]),
            r["title"],
            r["tags"] or "-",
            r["due_at"] or "-",
            "✅" if r["done"] else "",
        )

    console.print(table)

@app.command()
def done(task_id: int):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE tasks SET done = 1, done_at = ? WHERE id = ?",
            (now_iso(), task_id),
        )
        conn.commit()

    if cur.rowcount == 0:
        console.print("[red]No task found[/red]")
    else:
        console.print(f"[cyan]Completed[/cyan] task {task_id}")

@app.command()
def delete(task_id: int):
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

    if cur.rowcount == 0:
        console.print("[red]No task found[/red]")
    else:
        console.print(f"[yellow]Deleted[/yellow] task {task_id}")
