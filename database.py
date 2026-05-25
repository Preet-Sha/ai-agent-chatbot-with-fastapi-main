import sqlite3
import hashlib


conn = sqlite3.connect(
    "chat_history.db",
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

email TEXT UNIQUE,

password_hash TEXT,

support_type TEXT

)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history(

id INTEGER PRIMARY KEY AUTOINCREMENT,

user_id INTEGER,

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
            INSERT INTO users(

            name,
            email,
            password_hash,
            support_type

            )

            VALUES(?,?,?,?)
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



def save_message(
    user_id,
    role,
    message
):

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



def get_history(user_id):

    cursor.execute(
        """
        SELECT role,message

        FROM chat_history

        WHERE user_id=?

        ORDER BY id
        """,

        (
            user_id,
        )
    )

    return cursor.fetchall()