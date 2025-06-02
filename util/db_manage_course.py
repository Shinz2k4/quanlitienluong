import sqlite3
import os
from typing import List, Tuple

class Database:
    def __init__(self):
        if not os.path.exists('db'):
            os.makedirs('db')
            
        self.conn = sqlite3.connect('db/course_management.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS faculties (
                faculty_id TEXT PRIMARY KEY,
                faculty_name TEXT NOT NULL,
                description TEXT
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                faculty_id TEXT,
                FOREIGN KEY (faculty_id) REFERENCES faculties (faculty_id) ON DELETE SET NULL
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS semesters (
                semester_id TEXT PRIMARY KEY,
                semester_name TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT
            )
            ''')
            
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                class_id TEXT PRIMARY KEY,
                course_id TEXT NOT NULL,
                semester_id TEXT NOT NULL,
                class_name TEXT NOT NULL,
                max_students INTEGER NOT NULL,
                current_students INTEGER DEFAULT 0,
                FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE,
                FOREIGN KEY (semester_id) REFERENCES semesters (semester_id) ON DELETE CASCADE
            )
            ''')
            
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
        
    def get_course_count_by_faculty(self) -> List[Tuple[str, int]]:
        query = """
        SELECT f.faculty_name, COUNT(*) as count
        FROM courses c
        JOIN faculties f ON c.faculty_id = f.faculty_id
        GROUP BY f.faculty_name
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []
    
    def get_course_count_by_credits(self) -> List[Tuple[int, int]]:
        query = """
        SELECT credits, COUNT(*) as count
        FROM courses
        GROUP BY credits
        ORDER BY credits
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []
    
    def get_all_courses(self) -> List[Tuple]:
        query = """
        SELECT c.course_id, c.course_name, c.credits, f.faculty_name
        FROM courses c
        JOIN faculties f ON c.faculty_id = f.faculty_id
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []
    
    def add_course(self, course_id: str, course_name: str, credits: int, faculty_id: str) -> bool:
        try:
            query = """
            INSERT INTO courses (course_id, course_name, credits, faculty_id)
            VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(query, (course_id, course_name, credits, faculty_id))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return False
    
    def update_course(self, course_id: str, course_name: str, credits: int, faculty_id: str) -> bool:
        try:
            query = """
            UPDATE courses
            SET course_name = ?, credits = ?, faculty_id = ?
            WHERE course_id = ?
            """
            self.cursor.execute(query, (course_name, credits, faculty_id, course_id))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return False
    
    def delete_course(self, course_id: str) -> bool:
        try:
            query = "DELETE FROM courses WHERE course_id = ?"
            self.cursor.execute(query, (course_id,))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return False
    
    def get_course_by_id(self, course_id: str) -> Tuple:
        query = """
        SELECT c.course_id, c.course_name, c.credits, f.faculty_id, f.faculty_name
        FROM courses c
        JOIN faculties f ON c.faculty_id = f.faculty_id
        WHERE c.course_id = ?
        """
        try:
            self.cursor.execute(query, (course_id,))
            return self.cursor.fetchone()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return None
            
    def get_all_semesters(self) -> List[Tuple]:
        query = """
        SELECT semester_id, semester_name, start_date, end_date 
        FROM semesters
        ORDER BY start_date DESC
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []
        
    def get_all_classes(self) -> List[Tuple]:
        query = """
        SELECT c.class_id, c.class_name, c.max_students, c.current_students,
               co.course_name, s.semester_name
        FROM classes c
        JOIN courses co ON c.course_id = co.course_id
        JOIN semesters s ON c.semester_id = s.semester_id
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []
    def get_teacher_count_by_faculty(self):
        query = """
        SELECT f.faculty_name, COUNT(*) as count
        FROM teachers t
        JOIN faculties f ON t.faculty_id = f.faculty_id
        GROUP BY f.faculty_name
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []
    def add_semester(self, semester_id: str, semester_name: str, start_date: str, end_date: str):
        query = """
        INSERT INTO semesters (semester_id, semester_name, start_date, end_date)
        VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (semester_id, semester_name, start_date, end_date))
        self.conn.commit()
    def get_course_count_by_faculty(self) -> List[Tuple[str, int]]:
        query = """
        SELECT f.faculty_name, COUNT(*) as count
        FROM courses c
        JOIN faculties f ON c.faculty_id = f.faculty_id
        GROUP BY f.faculty_name
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []

    def get_all_courses(self) -> List[Tuple]:
        query = """
        SELECT c.course_id, c.course_name, c.credits, f.faculty_name
        FROM courses c
        LEFT JOIN faculties f ON c.faculty_id = f.faculty_id
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []

    def get_all_faculties(self) -> List[Tuple]:
        query = """
        SELECT faculty_id, faculty_name, description
        FROM faculties
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return []

    def add_course(self, course_id: str, course_name: str, credits: int, faculty_id: str = None):
        query = """
        INSERT INTO courses (course_id, course_name, credits, faculty_id)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.cursor.execute(query, (course_id, course_name, credits, faculty_id))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Mã học phần đã tồn tại!")

    def add_faculty(self, faculty_id: str, faculty_name: str, description: str = None):
        query = """
        INSERT INTO faculties (faculty_id, faculty_name, description)
        VALUES (?, ?, ?)
        """
        try:
            self.cursor.execute(query, (faculty_id, faculty_name, description))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Mã khoa đã tồn tại!")

    def update_course(self, course_id: str, course_name: str, credits: int, faculty_id: str = None):
        query = """
        UPDATE courses
        SET course_name = ?, credits = ?, faculty_id = ?
        WHERE course_id = ?
        """
        try:
            self.cursor.execute(query, (course_name, credits, faculty_id, course_id))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception(f"Cập nhật thất bại: {str(e)}")

    def update_faculty(self, faculty_id: str, faculty_name: str, description: str = None):
        query = """
        UPDATE faculties
        SET faculty_name = ?, description = ?
        WHERE faculty_id = ?
        """
        try:
            self.cursor.execute(query, (faculty_name, description, faculty_id))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception(f"Cập nhật thất bại: {str(e)}")

    def delete_course(self, course_id: str):
        query = """
        DELETE FROM courses
        WHERE course_id = ?
        """
        try:
            self.cursor.execute(query, (course_id,))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception(f"Xóa thất bại: {str(e)}")

    def delete_faculty(self, faculty_id: str):
        query = """
        DELETE FROM faculties
        WHERE faculty_id = ?
        """
        try:
            self.cursor.execute(query, (faculty_id,))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception(f"Xóa thất bại: {str(e)}")

    def add_class(self, semester_id: str, course_id: str, class_id: str, class_name: str, max_students: int):
        query = """
        INSERT INTO classes (semester_id, course_id, class_id, class_name, max_students)
        VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(query, (semester_id, course_id, class_id, class_name, max_students))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("Mã lớp đã tồn tại!")

    def update_class(self, class_id: str, semester_id: str, course_id: str, class_name: str, max_students: int):
        query = """
        UPDATE classes
        SET semester_id = ?, course_id = ?, class_name = ?, max_students = ?
        WHERE class_id = ?
        """
        try:
            self.cursor.execute(query, (semester_id, course_id, class_name, max_students, class_id))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception(f"Cập nhật thất bại: {str(e)}")

    def delete_class(self, class_id: str):
        query = """
        DELETE FROM classes
        WHERE class_id = ?
        """
        try:
            self.cursor.execute(query, (class_id,))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            raise Exception(f"Xóa thất bại: {str(e)}")
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
