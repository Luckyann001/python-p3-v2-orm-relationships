from lib.db import CURSOR, CONN
from lib.department import Department

class Employee:

    def __init__(self, name, job_title, department_id, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}, {self.job_title}>"

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                job_title TEXT,
                department_id INTEGER,
                FOREIGN KEY (department_id) REFERENCES departments(id)
            );
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS employees;")
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute("""
                INSERT INTO employees (name, job_title, department_id)
                VALUES (?, ?, ?)
            """, (self.name, self.job_title, self.department_id))
            self.id = CURSOR.lastrowid
        else:
            self.update()
        CONN.commit()
        return self

    @classmethod
    def create(cls, name, job_title, department_id):
        emp = cls(name, job_title, department_id)
        emp.save()
        return emp

    def update(self):
        CURSOR.execute("""
            UPDATE employees
            SET name = ?, job_title = ?, department_id = ?
            WHERE id = ?
        """, (self.name, self.job_title, self.department_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM employees WHERE id = ?", (self.id,))
        CONN.commit()
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        return cls(row[1], row[2], row[3], row[0])

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM employees").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute(
            "SELECT * FROM employees WHERE id = ?", (id,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute(
            "SELECT * FROM employees WHERE name = ?", (name,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None
