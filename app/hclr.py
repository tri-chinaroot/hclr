#!/usr/bin/env python3
"""HCLR CLI 原型：记录任务事件、介入、双重确认并生成报告。

用法示例见 app/README.md。数据默认保存在 ~/.hclr/hclr.db（本地，不联网）。
"""
import argparse
import json
import os
import sqlite3
import sys
import uuid
from datetime import datetime, date

DB_DIR = os.path.expanduser("~/.hclr")
DB_PATH = os.path.join(DB_DIR, "hclr.db")

P_LABELS = {1: "P1 局部改变", 2: "P2 模块改变", 3: "P3 结论改变", 4: "P4 方案改变", 5: "P5 框架改变"}


def db() -> sqlite3.Connection:
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(args=None):
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                title TEXT,
                domain TEXT NOT NULL,
                model TEXT NOT NULL,
                audience TEXT NOT NULL,
                O0 TEXT NOT NULL DEFAULT '',
                O1 TEXT NOT NULL DEFAULT '',
                I REAL NOT NULL DEFAULT 0,
                I_metric TEXT NOT NULL DEFAULT 'judgments',
                P INTEGER,
                P_note TEXT,
                C1 INTEGER,
                C2 INTEGER,
                C2_note TEXT,
                created_at TEXT NOT NULL,
                confirmed_at TEXT,
                c2_at TEXT,
                c2_deadline TEXT
            );
            CREATE TABLE IF NOT EXISTS interventions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                seq INTEGER NOT NULL,
                text TEXT NOT NULL,
                kind TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks(task_id)
            );
            """
        )
    print(f"数据库已初始化: {DB_PATH}")


def new_task(args):
    task_id = args.task_id or f"hclr-{datetime.now():%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:4]}"
    with db() as conn:
        conn.execute(
            "INSERT INTO tasks (task_id, title, domain, model, audience, created_at) VALUES (?,?,?,?,?,?)",
            (task_id, args.title, args.domain, args.model, args.audience, datetime.now().isoformat(timespec="seconds")),
        )
    print(f"任务已创建: {task_id}")


def _require_task(conn, task_id) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
    if not row:
        raise SystemExit(f"任务不存在: {task_id}")
    return row


def freeze(args):
    """冻结 AI 初稿 O0（仅当 O0 为空时允许）。"""
    with db() as conn:
        row = _require_task(conn, args.task_id)
        if row["O0"]:
            raise SystemExit("O0 已冻结，不允许覆盖。若确需修改请新建任务。")
        if args.file:
            content = open(args.file, encoding="utf-8").read()
        elif args.text:
            content = args.text
        else:
            content = sys.stdin.read()
        conn.execute("UPDATE tasks SET O0=? WHERE task_id=?", (content, args.task_id))
    print(f"O0 已冻结: {args.task_id}")


def intervene(args):
    """记录一次人类介入，并更新介入量。"""
    with db() as conn:
        _require_task(conn, args.task_id)
        seq = conn.execute(
            "SELECT COALESCE(MAX(seq),0)+1 FROM interventions WHERE task_id=?", (args.task_id,)
        ).fetchone()[0]
        conn.execute(
            "INSERT INTO interventions (task_id, seq, text, kind, timestamp) VALUES (?,?,?,?,?)",
            (args.task_id, seq, args.text, args.kind, datetime.now().isoformat(timespec="seconds")),
        )
        # 更新介入量：默认按判断数（每条介入 = 1 次判断），可 --metric chars/turns 覆盖
        if args.metric == "chars":
            delta = len(args.text)
        elif args.metric == "turns":
            delta = 1
        else:
            delta = 1
        conn.execute(
            "UPDATE tasks SET I=I+?, I_metric=? WHERE task_id=?",
            (delta, args.metric, args.task_id),
        )
    print(f"介入已记录 (seq={seq}, {args.metric}=+{delta}): {args.task_id}")


def confirm1(args):
    """第一轮确认：adopt(1) / reject(0)。"""
    c1 = 1 if args.choice == "adopt" else 0
    with db() as conn:
        _require_task(conn, args.task_id)
        conn.execute(
            "UPDATE tasks SET C1=?, confirmed_at=?, P=COALESCE(P,?) WHERE task_id=?",
            (c1, datetime.now().isoformat(timespec="seconds"), args.p, args.task_id),
        )
        if args.p:
            conn.execute("UPDATE tasks SET P=?, P_note=COALESCE(P_note,?) WHERE task_id=?",
                         (args.p, args.note, args.task_id))
    print(f"C1={c1} 已记录: {args.task_id}")


def set_p(args):
    with db() as conn:
        _require_task(conn, args.task_id)
        conn.execute("UPDATE tasks SET P=?, P_note=? WHERE task_id=?", (args.p, args.note, args.task_id))
    print(f"P={args.p} ({P_LABELS.get(args.p)}) 已记录: {args.task_id}")


def confirm2(args):
    """第二轮确认：approved(1) / rejected(0) / pending(待确认)。"""
    mapping = {"approved": 1, "rejected": 0, "pending": None}
    c2 = mapping[args.choice]
    with db() as conn:
        _require_task(conn, args.task_id)
        conn.execute(
            "UPDATE tasks SET C2=?, C2_note=?, c2_at=? WHERE task_id=?",
            (c2, args.note, datetime.now().isoformat(timespec="seconds"), args.task_id),
        )
    print(f"C2={'待确认' if c2 is None else c2} 已记录: {args.task_id}")


def _status(row) -> str:
    if row["C1"] == 0:
        return "S0"
    if row["C1"] == 1:
        if row["C2"] is None:
            return "S1"
        return "S3" if row["C2"] == 1 else "S2"
    return "S0"


def report(args):
    with db() as conn:
        if args.task_id:
            row = _require_task(conn, args.task_id)
            rows = [row]
        else:
            rows = conn.execute("SELECT * FROM tasks ORDER BY created_at").fetchall()
        if not rows:
            print("暂无记录。先创建任务: app/hclr.py task add ...")
            return
        ints = {r["task_id"]: conn.execute(
            "SELECT seq, text, kind FROM interventions WHERE task_id=? ORDER BY seq", (r["task_id"],)
        ).fetchall() for r in rows}

    print("=" * 60)
    print("HCLR 个人记录报告")
    print("=" * 60)
    n = len(rows)
    adopted = [r for r in rows if r["C1"] == 1]
    with_c2 = [r for r in adopted if r["C2"] is not None]
    approved = [r for r in with_c2 if r["C2"] == 1]
    p_dist = {}
    for r in rows:
        if r["P"]:
            p_dist[r["P"]] = p_dist.get(r["P"], 0) + 1
    status_dist = {}
    for r in rows:
        s = _status(r)
        status_dist[s] = status_dist.get(s, 0) + 1

    print(f"任务数: {n}")
    print(f"直接采用率(无介入基线): --")  # CLI 暂不自动判断无介入任务，见 SCORING.md
    print(f"介入后采用率(C1=1): {len(adopted)}/{n} = {len(adopted)/n:.0%}" if n else "0")
    print(f"第二轮完成率: {len(with_c2)}/{len(adopted)} = {len(with_c2)/len(adopted):.0%}" if adopted else "0")
    print(f"已确认认可率: {len(approved)}/{len(with_c2)} = {len(approved)/len(with_c2):.0%}" if with_c2 else "0")
    print(f"P分布: { {P_LABELS.get(k): v for k, v in sorted(p_dist.items())} }")
    print(f"状态分布: {status_dist}")
    print("-" * 60)
    for r in rows:
        st = _status(r)
        marker = {"S0": "✗", "S1": "…", "S2": "!", "S3": "✓"}[st]
        print(f"[{marker} {st}] {r['task_id']} | {r['domain']} | {r['model']} | P={r['P'] or '-'} | I={r['I']}{r['I_metric'][0]} | {r['title'] or ''}")
        for iv in ints[r["task_id"]]:
            print(f"    #{iv['seq']} [{iv['kind'] or 'other'}] {iv['text'][:60]}")
    print("=" * 60)
    print("注: 当前为参考报告，不输出合成总分；P 为顺序等级，参考值口径见 SCORING.md")


def export_json(args):
    with db() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY created_at").fetchall()
        ints = {r["task_id"]: conn.execute(
            "SELECT seq, text, kind, timestamp FROM interventions WHERE task_id=? ORDER BY seq", (r["task_id"],)
        ).fetchall() for r in rows}
    out = []
    for r in rows:
        d = dict(r)
        d["interventions"] = [dict(i) for i in ints[r["task_id"]]]
        d["status"] = _status(r)
        out.append(d)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"已导出: {args.output} ({len(out)} 条)")


def main():
    parser = argparse.ArgumentParser(prog="hclr", description="HCLR 记录与计算工具（本地）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="初始化数据库").set_defaults(func=init_db)

    p = sub.add_parser("task", help="创建任务")
    p.add_argument("add", nargs="?", const="add")
    p.add_argument("--task-id")
    p.add_argument("--title")
    p.add_argument("--domain", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--audience", required=True)
    p.set_defaults(func=new_task)

    p = sub.add_parser("draft", help="冻结 AI 初稿 O0")
    p.add_argument("freeze")
    p.add_argument("task_id")
    p.add_argument("--file", help="从文件读取初稿")
    p.add_argument("--text", help="直接传入初稿文本")
    p.set_defaults(func=freeze)

    p = sub.add_parser("intervene", help="记录人类介入")
    p.add_argument("task_id")
    p.add_argument("text")
    p.add_argument("--kind", choices=["fact_correction", "goal_adjustment", "constraint", "conclusion_revision", "framework_change", "style_adaptation", "other"], default="other")
    p.add_argument("--metric", choices=["judgments", "chars", "turns"], default="judgments")
    p.set_defaults(func=intervene)

    p = sub.add_parser("p", help="设置改变范围 P1-P5")
    p.add_argument("task_id")
    p.add_argument("p", type=int, choices=[1, 2, 3, 4, 5])
    p.add_argument("--note")
    p.set_defaults(func=set_p)

    p = sub.add_parser("confirm1", help="第一轮确认")
    p.add_argument("task_id")
    p.add_argument("choice", choices=["adopt", "reject"])
    p.add_argument("--p", type=int, choices=[1, 2, 3, 4, 5])
    p.add_argument("--note")
    p.set_defaults(func=confirm1)

    p = sub.add_parser("confirm2", help="第二轮确认")
    p.add_argument("task_id")
    p.add_argument("choice", choices=["approved", "rejected", "pending"])
    p.add_argument("--note")
    p.set_defaults(func=confirm2)

    p = sub.add_parser("report", help="生成报告")
    p.add_argument("task_id", nargs="?")
    p.set_defaults(func=report)

    p = sub.add_parser("export", help="导出 JSON")
    p.add_argument("--output", default=os.path.join(DB_DIR, "hclr-export.json"))
    p.set_defaults(func=export_json)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
