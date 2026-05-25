import sqlite3
import hashlib
import uuid

conn = sqlite3.connect(
    "chat_history.db",
    check_same_thread=False
)

cursor = conn.cursor()


# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

email TEXT UNIQUE,

password_hash TEXT,

support_type TEXT
)
""")


# CHAT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

session_id TEXT,

role TEXT,

message TEXT
)
""")

conn.commit()


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_user(
    name,
    email,
    password,
    support_type
):

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash,
                support_type
            )

            VALUES (?,?,?,?)
            """,

            (
                name,
                email,
                hash_password(password),
                support_type
            )
        )

        conn.commit()

        return True

    except:

        return False


def login_user(
    email,
    password
):

    cursor.execute(
        """
        SELECT id,
        name,
        support_type

        FROM users

        WHERE email=?

        AND password_hash=?
        """,

        (
            email,
            hash_password(password)
        )
    )

    return cursor.fetchone()

# ==========================
# SAVE CHAT
# ==========================
def save_message(

    user_id,

    role,

    message
):

    try:

        cursor.execute(

            """
            INSERT INTO chat_history(

            user_id,

            role,

            message

            )

            VALUES(?,?,?)
            """,

            (

                user_id,

                role,

                message

            )
        )

        conn.commit()

    except Exception as e:

        print(
            "SAVE ERROR:",
            e
        )

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