from lib.db import CURSOR, CONN

class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name} ({self.location})>"

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            );
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments;")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO departments (name, location)
                VALUES (?, ?)
            """, (self.name, self.location))
            self.id = CURSOR.lastrowid
        else:
            self.update()
        CONN.commit()
        return self

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    def update(self):
        CURSOR.execute("""
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM departments WHERE id = ?", (self.id,))
        CONN.commit()
        self.id = None

    def employees(self):
        from lib.employee import Employee

        rows = CURSOR.execute(
            "SELECT * FROM employees WHERE department_id = ?",
            (self.id,)
        ).fetchall()

        return [Employee.instance_from_db(row) for row in rows]

    @classmethod
    def instance_from_db(cls, row):
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM departments").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE id = ?", (id,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE name = ?", (name,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None
