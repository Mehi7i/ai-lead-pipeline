"""
Simple CRM Writer
-----------------
Saves qualified leads into a local SQLite database.
"""

import os
import json
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "leads.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT,
            budget TEXT,
            source TEXT,
            score TEXT,
            reason TEXT,
            priority INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_lead(lead: dict, qualification: dict) -> int:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads (name, email, phone, message, budget, source, score, reason, priority, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lead.get("name"),
        lead.get("email"),
        lead.get("phone"),
        lead.get("message"),
        lead.get("budget"),
        lead.get("source", "website"),
        qualification.get("score"),
        qualification.get("reason"),
        qualification.get("priority", 3),
        datetime.utcnow().isoformat(),
    ))

    lead_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lead_id


if __name__ == "__main__":
    try:
        input_data = json.loads(sys.stdin.read())
        lead = input_data.get("lead", input_data)
        qualification = input_data.get("qualification", {})
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    lead_id = save_lead(lead, qualification)
    print(json.dumps({"success": True, "lead_id": lead_id}))