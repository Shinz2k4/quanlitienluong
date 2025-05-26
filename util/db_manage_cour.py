import sqlite3
import os
from typing import List, Tuple

class Database:
    def __init__(self):
        # Tạo thư mục db nếu chưa tồn tại
        if not os.path.exists('db'):
            os.makedirs('db')
            
        self.conn = sqlite3.connect('db/course_management.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        """Tạo các bảng cần thiết nếu chưa tồn tại"""
        try:
            # Tạo bảng khoa
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS faculties (
                faculty_id TEXT PRIMARY KEY,
                faculty_name TEXT NOT NULL,
                description TEXT
            )
            ''')
            
            # Tạo bảng học phần
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id TEXT PRIMARY KEY,
                course_name TEXT NOT NULL,
                credits INTEGER NOT NULL,
                faculty_id TEXT,
                FOREIGN KEY (faculty_id) REFERENCES faculties (faculty_id) ON DELETE SET NULL
            )
            ''')
            
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
        
    def get_course_count_by_faculty(self) -> List[Tuple[str, int]]:
        """Lấy số lượng học phần theo khoa"""
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
        """Lấy số lượng học phần theo số tín chỉ"""
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
        """Lấy tất cả học phần"""
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
        """Thêm học phần mới"""
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
        """Cập nhật thông tin học phần"""
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
        """Xóa học phần"""
        try:
            query = "DELETE FROM courses WHERE course_id = ?"
            self.cursor.execute(query, (course_id,))
            self.conn.commit()
            return True
        except sqlite3.OperationalError as e:
            print(f"SQL error: {e}")
            return False
    
    def get_course_by_id(self, course_id: str) -> Tuple:
        """Lấy thông tin học phần theo mã"""
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
    
    def __del__(self):
        """Đóng kết nối database khi đối tượng bị hủy"""
        if hasattr(self, 'conn'):
            self.conn.close()
