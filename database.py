import sqlite3
from datetime import datetime

from config import get_database_path
from security import hash_password, verify_password


class Database:
    def __init__(self):
        self.database_path = get_database_path()

        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row

        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = NORMAL")

        self.create_tables()

    def create_tables(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,

                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
            """
        )

        self.connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_notes_user
            ON notes(user_id)
            """
        )

        self.connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_notes_updated
            ON notes(updated_at)
            """
        )

        self.connection.commit()

    def register_user(self, username, password):
        username = username.strip()

        if not username:
            return False, "Username is required."

        if len(username) > 50:
            return False, "Username is too long."

        if len(password) < 6:
            return False, "Password must contain at least 6 characters."

        existing = self.connection.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(username) = LOWER(?)
            """,
            (username,)
        ).fetchone()

        if existing:
            return False, "Username already exists."

        salt, password_hash = hash_password(password)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.connection.execute(
                """
                INSERT INTO users
                (
                    username,
                    password_salt,
                    password_hash,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    salt,
                    password_hash,
                    now
                )
            )

            self.connection.commit()

            return True, "Account created successfully."

        except sqlite3.Error as error:
            self.connection.rollback()
            return False, "Unable to create account: {}".format(error)

    def login_user(self, username, password):
        username = username.strip()

        user = self.connection.execute(
            """
            SELECT *
            FROM users
            WHERE LOWER(username) = LOWER(?)
            """,
            (username,)
        ).fetchone()

        if not user:
            return None

        if not verify_password(
            password,
            user["password_salt"],
            user["password_hash"]
        ):
            return None

        return {
            "id": user["id"],
            "username": user["username"],
            "created_at": user["created_at"]
        }

    def user_count(self):
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM users
            """
        ).fetchone()

        return row["total"]

    def create_note(self, user_id, title, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.connection.execute(
                """
                INSERT INTO notes
                (
                    user_id,
                    title,
                    content,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    title,
                    content,
                    now,
                    now
                )
            )

            self.connection.commit()

            return cursor.lastrowid

        except sqlite3.Error:
            self.connection.rollback()
            raise

    def update_note(self, note_id, user_id, title, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.connection.execute(
                """
                UPDATE notes
                SET
                    title = ?,
                    content = ?,
                    updated_at = ?
                WHERE
                    id = ?
                    AND user_id = ?
                """,
                (
                    title,
                    content,
                    now,
                    note_id,
                    user_id
                )
            )

            self.connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            self.connection.rollback()
            raise

    def delete_note(self, note_id, user_id):
        try:
            cursor = self.connection.execute(
                """
                DELETE FROM notes
                WHERE
                    id = ?
                    AND user_id = ?
                """,
                (
                    note_id,
                    user_id
                )
            )

            self.connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            self.connection.rollback()
            raise

    def get_notes(self, user_id, search_text=""):
        search_text = search_text.strip()

        if search_text:
            wildcard = "%" + search_text + "%"

            rows = self.connection.execute(
                """
                SELECT *
                FROM notes
                WHERE
                    user_id = ?
                    AND
                    (
                        title LIKE ?
                        OR content LIKE ?
                    )
                ORDER BY updated_at DESC
                """,
                (
                    user_id,
                    wildcard,
                    wildcard
                )
            ).fetchall()

        else:
            rows = self.connection.execute(
                """
                SELECT *
                FROM notes
                WHERE user_id = ?
                ORDER BY updated_at DESC
                """,
                (user_id,)
            ).fetchall()

        return rows

    def get_note(self, note_id, user_id):
        return self.connection.execute(
            """
            SELECT *
            FROM notes
            WHERE
                id = ?
                AND user_id = ?
            """,
            (
                note_id,
                user_id
            )
        ).fetchone()

    def note_count(self, user_id):
        row = self.connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM notes
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        return row["total"]

    def export_notes(self, user_id, file_path):
        notes = self.get_notes(user_id)

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            for index, note in enumerate(notes, 1):
                file.write("=" * 70)
                file.write("\n")
                file.write("NOTE {}\n".format(index))
                file.write("=" * 70)
                file.write("\n\n")

                file.write(
                    "Title: {}\n".format(
                        note["title"]
                    )
                )

                file.write(
                    "Created: {}\n".format(
                        note["created_at"]
                    )
                )

                file.write(
                    "Updated: {}\n\n".format(
                        note["updated_at"]
                    )
                )

                file.write(note["content"])
                file.write("\n\n")

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            finally:
                self.connection = None
