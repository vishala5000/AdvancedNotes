def create_note(
    self,
    user_id,
    title,
    content
):

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

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

    except Exception:

        self.connection.rollback()

        raise


def update_note(
    self,
    note_id,
    user_id,
    title,
    content
):

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

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

    except Exception:

        self.connection.rollback()

        raise


def delete_note(
    self,
    note_id,
    user_id
):

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

    except Exception:

        self.connection.rollback()

        raise
