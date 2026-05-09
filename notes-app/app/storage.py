import sqlite3

DB_FILE="my.db"

def get_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
def create_table():
    conn = get_db()
    if conn:
        table_sql = """CREATE TABLE IF NOT EXISTS notes(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        createdAt DATETIME NOT NULL,
        updatedAt DATETIME
        )"""

        try:
            cursor = conn.cursor()
            cursor.execute(table_sql)
            conn.commit()
            print("Table created successfully!")
        except sqlite3.Error as e:
            print(f"Failed to create tables: {e}")
        finally:
            conn.close()

def insert_note(note):
    conn = get_db()
    if conn:
        create_table()
        insert_sql = """INSERT INTO notes(title, content, createdAt)
        VALUES (?,?,?)"""

        try:
            cursor = conn.cursor()
            cursor.execute(insert_sql, note)
            conn.commit()
            print("Data inserted!")
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting: {e}")
        finally:
            conn.close()

def get_note_by_id(note_id):
    conn = get_db()
    if conn:
        sql = """SELECT * FROM notes WHERE id = ?"""

        try:
            cursor = conn.cursor()
            cursor.execute(sql, (note_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except sqlite3.Error as e:
            print(f"Error fetching: {e}")
        finally:
            conn.close()

def update_note(note_tuple):
    # note_tuple: (title, content, updatedAt, id) 
    conn = get_db()
    if conn:
        sql = """UPDATE notes
        SET title = ?, content = ?, updatedAt = ?
        WHERE id = ?"""

        try:
            cursor = conn.cursor()
            cursor.execute(sql, note_tuple)
            conn.commit()
            print("Data updated!")
        except sqlite3.Error as e:
            print(f"Error while updating: {e}")
        finally:
            conn.close()

def delete_note(note_id):
    conn = get_db()
    if conn:
        sql = """DELETE FROM notes WHERE ID = ?"""

        try:
            deleted_note = get_note_by_id(note_id)
            if deleted_note:
                cursor = conn.cursor()
                cursor.execute(sql, (note_id,))
                conn.commit()
                return deleted_note
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error deleting: {e}")
        finally:
            conn.close()


def get_all_notes(search:str|None=None, sort:str|None=None, limit=10, skip=0):
    conn = get_db()
    if conn:
        sql = "SELECT * FROM notes"
        params = []
        if search:
            sql += " WHERE title LIKE ?"
            params.append(search)
        if sort:
            sql += f" ORDER BY {sort} DESC"
        sql += f" LIMIT ? OFFSET ?"
        params.append(limit)
        params.append(skip)

        try:
            cursor = conn.cursor()
            cursor.execute(sql,params)
            rows = cursor.fetchall()
            # [] is still a valid result. not a missing resource unlike in 
            # get_note_by_id (cus that simply doesnt exist)
            # but here table might be empty but it still exists - not a missing resource
            # no need of if rows, just directly returning the list of dicts
            return [dict(row) for row in rows] 
        except sqlite3.Error as e:
            print(f"Error fetching rows: {e}")
        finally:
            conn.close()

            
        