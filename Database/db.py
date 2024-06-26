import sqlite3

def create_connection():
    return sqlite3.connect('Database/db.db')

async def AddUser(user_id, username, user_firstname, amount):
    conn = create_connection()
    cursor = conn.cursor()

    if username is None:
        username = user_firstname
    else:
        username = f"@{username}"

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        cursor.execute("INSERT INTO users (user_id, username, amount) VALUES (?, ?, ?)", (user_id, username, amount))
        conn.commit()

    conn.close()


async def delete_user_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()

    # Get user_id using username
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()

    if user_id:
        user_id = user_id[0]

        # Delete user from users table
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))

        # Delete records from other tables where the user_id appears
        cursor.execute("DELETE FROM referrers WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM invited_referrals WHERE referral_id = ?", (user_id,))
        cursor.execute("UPDATE invited_referrals SET referral_id = NULL WHERE referral_id = ?", (username,))
    
        conn.commit()
        conn.close()
    else:
        print("User not found")


async def increase_amount(username):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET amount = amount + 1 WHERE username = ?", (username,))
    conn.commit()

    conn.close()

async def user_in_invited_referrals(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM invited_referrals WHERE referral_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    conn.close()
    if existing_user == None:
        return False
    else:
        return True 


async def GetAmount(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT amount FROM users WHERE user_id = ?", (user_id,))
    amount = cursor.fetchone()[0]

    conn.close()
    return amount

async def insert_referrer(user_id, referral_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO referrers (user_id, referral_id) VALUES (?, ?)", (user_id, referral_id))
    conn.commit()

async def insert_invited_referral(referral_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO invited_referrals (referral_id) VALUES (?)", (referral_id,))
    conn.commit()

async def reset_database():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM invited_referrals")
    cursor.execute("DELETE FROM referrers")
    cursor.execute("UPDATE users SET amount = 0")

    conn.commit()
    conn.close()


async def get_username_by_user_id(user_id: int) -> str:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

async def delete_user_from_invited_referrals(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM invited_referrals WHERE referral_id = ?", (user_id,))
    conn.commit()

    conn.close()

async def set_amount(username: int, amount: int):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET amount = ? WHERE username = ?", (amount, username))
    conn.commit()

    conn.close()
