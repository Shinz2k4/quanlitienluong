import sqlite3
import os

class Database:
    def __init__(self, db_name="db/teacher_management.db"):
        # Create db directory if it doesn't exist
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tạo bảng bằng cấp
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS degrees (
            degree_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            abbreviation TEXT NOT NULL
        )
        ''')
        
        # Tạo bảng khoa
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculties (
            faculty_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            abbreviation TEXT NOT NULL,
            description TEXT,
            head_of_faculty TEXT
        )
        ''')
        
        # Tạo bảng giáo viên
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            birth_date DATE,
            phone TEXT,
            email TEXT,
            faculty_id TEXT,
            degree_id TEXT,
            FOREIGN KEY (faculty_id) REFERENCES faculties (faculty_id) ON DELETE SET NULL,
            FOREIGN KEY (degree_id) REFERENCES degrees (degree_id) ON DELETE SET NULL
        )
        ''')
        
        # Tạo bảng học phần
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            coefficient REAL NOT NULL,
            total_hours INTEGER NOT NULL
        )
        ''')
        
        # Tạo bảng phân công giảng dạy
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teaching_assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            semester TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
        conn.close()
    
    # === CRUD operations for Degrees ===
    def add_degree(self, degree_id, full_name, abbreviation):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO degrees (degree_id, full_name, abbreviation)
            VALUES (?, ?, ?)
            ''', (degree_id, full_name, abbreviation))
            conn.commit()
        finally:
            conn.close()
    
    def get_all_degrees(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM degrees')
            return cursor.fetchall()
        finally:
            conn.close()
    
    def update_degree(self, degree_id, full_name, abbreviation):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE degrees 
            SET full_name = ?, abbreviation = ?
            WHERE degree_id = ?
            ''', (full_name, abbreviation, degree_id))
            conn.commit()
        finally:
            conn.close()
    
    def delete_degree(self, degree_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM degrees WHERE degree_id = ?', (degree_id,))
            conn.commit()
        finally:
            conn.close()
    
    # === CRUD operations for Faculties ===
    def add_faculty(self, faculty_id, full_name, abbreviation, description, head_of_faculty):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO faculties (faculty_id, full_name, abbreviation, description, head_of_faculty)
            VALUES (?, ?, ?, ?, ?)
            ''', (faculty_id, full_name, abbreviation, description, head_of_faculty))
            conn.commit()
        finally:
            conn.close()
    
    def get_all_faculties(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM faculties')
            return cursor.fetchall()
        finally:
            conn.close()
    
    def update_faculty(self, faculty_id, full_name, abbreviation, description, head_of_faculty):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE faculties 
            SET full_name = ?, abbreviation = ?, description = ?, head_of_faculty = ?
            WHERE faculty_id = ?
            ''', (full_name, abbreviation, description, head_of_faculty, faculty_id))
            conn.commit()
        finally:
            conn.close()
    
    def delete_faculty(self, faculty_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM faculties WHERE faculty_id = ?', (faculty_id,))
            conn.commit()
        finally:
            conn.close()
    
    # === CRUD operations for Teachers ===
    def add_teacher(self, teacher_id, full_name, birth_date, phone, email, faculty_id, degree_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO teachers (teacher_id, full_name, birth_date, phone, email, faculty_id, degree_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (teacher_id, full_name, birth_date, phone, email, faculty_id, degree_id))
            conn.commit()
        finally:
            conn.close()
    
    def get_all_teachers(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT t.teacher_id, t.full_name, t.birth_date, t.phone, t.email, 
                   f.full_name as faculty_name, d.full_name as degree_name 
            FROM teachers t
            LEFT JOIN faculties f ON t.faculty_id = f.faculty_id
            LEFT JOIN degrees d ON t.degree_id = d.degree_id
            ''')
            return cursor.fetchall()
        finally:
            conn.close()
    
    def update_teacher(self, teacher_id, full_name, birth_date, phone, email, faculty_id, degree_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE teachers 
            SET full_name = ?, birth_date = ?, phone = ?, email = ?, faculty_id = ?, degree_id = ?
            WHERE teacher_id = ?
            ''', (full_name, birth_date, phone, email, faculty_id, degree_id, teacher_id))
            conn.commit()
        finally:
            conn.close()
    
    def delete_teacher(self, teacher_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
            conn.commit()
        finally:
            conn.close()

    # === CRUD operations for Courses ===
    def add_course(self, course_id, course_name, credits, coefficient, total_hours):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO courses (course_id, course_name, credits, coefficient, total_hours)
            VALUES (?, ?, ?, ?, ?)
            ''', (course_id, course_name, credits, coefficient, total_hours))
            conn.commit()
        finally:
            conn.close()
    
    def get_all_courses(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM courses')
            return cursor.fetchall()
        finally:
            conn.close()
    
    def update_course(self, course_id, course_name, credits, coefficient, total_hours):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE courses 
            SET course_name = ?, credits = ?, coefficient = ?, total_hours = ?
            WHERE course_id = ?
            ''', (course_name, credits, coefficient, total_hours, course_id))
            conn.commit()
        finally:
            conn.close()
    
    def delete_course(self, course_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM courses WHERE course_id = ?', (course_id,))
            conn.commit()
        finally:
            conn.close()

    # === CRUD operations for Teaching Assignments ===
    def add_teaching_assignment(self, teacher_id, course_id, semester, academic_year):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO teaching_assignments (teacher_id, course_id, semester, academic_year)
            VALUES (?, ?, ?, ?)
            ''', (teacher_id, course_id, semester, academic_year))
            conn.commit()
        finally:
            conn.close()
    def get_all_teaching_assignments(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT ta.*, t.full_name as teacher_name, c.course_name
            FROM teaching_assignments ta
            JOIN teachers t ON ta.teacher_id = t.teacher_id
            JOIN courses c ON ta.course_id = c.course_id
            ''')
            return cursor.fetchall()
        finally:
            conn.close()
