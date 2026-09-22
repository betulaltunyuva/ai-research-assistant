import json
import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join(
    "outputs",
    "memory.db"
)


def get_connection():
    os.makedirs(
        "outputs",
        exist_ok=True
    )

    connection = sqlite3.connect(
        DB_PATH
    )

    connection.row_factory = (
        sqlite3.Row
    )

    return connection


def init_memory():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            query TEXT NOT NULL,
            final_answer TEXT,
            sources_json TEXT,
            document_path TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_message(
    role: str,
    content: str,
    session_id: str = "default"
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            session_id,
            role,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            session_id,
            role,
            content,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_recent_messages(
    session_id: str = "default",
    limit: int = 6
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            session_id,
            limit
        )
    )

    rows = cursor.fetchall()
    connection.close()

    rows = list(reversed(rows))

    return [
        {
            "role": row["role"],
            "content": row["content"]
        }
        for row in rows
    ]


def save_research(
    query: str,
    final_answer: str,
    sources: list,
    document_path: str = "",
    session_id: str = "default"
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO research_history (
            session_id,
            query,
            final_answer,
            sources_json,
            document_path,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            query,
            final_answer,
            json.dumps(
                sources,
                ensure_ascii=False
            ),
            document_path,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_last_research(
    session_id: str = "default"
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM research_history
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (session_id,)
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return {
        "query": row["query"],
        "final_answer": row["final_answer"],
        "sources": json.loads(
            row["sources_json"] or "[]"
        ),
        "document_path":
            row["document_path"] or ""
    }

def get_sessions():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            session_id,
            COUNT(*) AS research_count,
            MAX(created_at) AS last_activity
        FROM research_history
        GROUP BY session_id
        ORDER BY last_activity DESC
        """
    )

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "session_id": row["session_id"],
            "research_count": row["research_count"],
            "last_activity": row["last_activity"]
        }
        for row in rows
    ]