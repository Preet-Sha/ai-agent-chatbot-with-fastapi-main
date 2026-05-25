import sqlite3

conn = sqlite3.connect(
    "/tmp/chat_history.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS chat_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        session_id TEXT,

        role TEXT,

        message TEXT

    )
    """
)

conn.commit()


def save_message(

    user_id,

    session_id,

    role,

    message

):

    cursor.execute(

        """
        INSERT INTO chat_history(

            user_id,

            session_id,

            role,

            message

        )

        VALUES(?,?,?,?)

        """,

        (

            user_id,

            session_id,

            role,

            message

        )

    )

    conn.commit()


def get_history(

    session_id

):

    cursor.execute(

        """
        SELECT message

        FROM chat_history

        WHERE session_id=?

        ORDER BY id

        """,

        (

            session_id,

        )

    )

    rows = cursor.fetchall()

    return [

        row[0]

        for row in rows

    ]