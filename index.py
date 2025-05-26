import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database
import util.manage_degree as manage_degree
import util.manage_faculty as manage_faculty
import util.manage_teacher as manage_teacher
import util.teacher_statistics as teacher_statistics
import util.manage_course as manage_course
import util.manage_semester as manage_semester
import util.manage_class as manage_class
import util.manage_teaching as manage_teaching
import util.course_statistics as course_statistics

def main():
    # Khởi tạo database
    db = Database()

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Quản Lý Giáo Viên và Lớp Học")
    root.geometry("1200x700")

    # ===== Khung chức năng bên trái =====
    frame_left = tk.Frame(root, bg="#eeeeee", width=200)
    frame_left.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(frame_left, text="CHỨC NĂNG", font=("Arial", 12, "bold"), bg="#eeeeee").pack(pady=10)

    # Tạo các nút chức năng chính
    tk.Label(frame_left, text="Quản lý giáo viên", font=("Arial", 10, "bold"), bg="#eeeeee").pack(pady=5)
    tk.Button(frame_left, text="Quản lý bằng cấp", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Quản lý khoa", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Quản lý giáo viên", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Thống kê giáo viên", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)

    # Thêm separator
    ttk.Separator(frame_left, orient='horizontal').pack(fill='x', padx=5, pady=10)

    # Thêm các nút quản lý lớp học
    tk.Label(frame_left, text="Quản lý lớp học", font=("Arial", 10, "bold"), bg="#eeeeee").pack(pady=5)
    tk.Button(frame_left, text="Quản lý học phần", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Quản lý kì học", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Quản lý lớp học phần", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Phân công giảng dạy", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Thống kê lớp học", font=("Arial", 10)).pack(pady=2, padx=10, fill=tk.X)

    # ===== Khung quản lý bên phải =====
    frame_right = tk.Frame(root)
    frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Dictionary để lưu trữ các frame cho từng chức năng
    frames = {}

    # Tạo các frame
    frames["degree"] = manage_degree.create_degree_frame()
    frames["teacher"] = manage_teacher.create_teacher_frame()
    frames["faculty"] = manage_faculty.create_faculty_frame()
    frames["statistics"] = teacher_statistics.create_statistics_frame()
    frames["course"] = manage_course.create_course_frame()
    frames["semester"] = manage_semester.create_semester_frame()
    frames["class"] = manage_class.create_class_frame()
    frames["teaching"] = manage_teaching.create_teaching_frame()
    frames["course_stats"] = course_statistics.create_course_statistics_frame()

    # Hàm chuyển đổi giữa các frame
    def show_frame(frame_name):
        # Ẩn tất cả các frame
        for frame in frames.values():
            frame.pack_forget()
        # Hiển thị frame được chọn
        frames[frame_name].pack(fill=tk.BOTH, expand=True)

    # Gán các hàm cho các nút
    for button in frame_left.winfo_children():
        if isinstance(button, tk.Button):
            text = button.cget("text")
            if text == "Quản lý bằng cấp":
                button.config(command=lambda: show_frame("degree"))
            elif text == "Quản lý khoa":
                button.config(command=lambda: show_frame("faculty"))
            elif text == "Quản lý giáo viên":
                button.config(command=lambda: show_frame("teacher"))
            elif text == "Thống kê giáo viên":
                button.config(command=lambda: show_frame("statistics"))
            elif text == "Quản lý học phần":
                button.config(command=lambda: show_frame("course"))
            elif text == "Quản lý kì học":
                button.config(command=lambda: show_frame("semester"))
            elif text == "Quản lý lớp học phần":
                button.config(command=lambda: show_frame("class"))
            elif text == "Phân công giảng dạy":
                button.config(command=lambda: show_frame("teaching"))
            elif text == "Thống kê lớp học":
                button.config(command=lambda: show_frame("course_stats"))
        
    # Hiển thị frame giáo viên mặc định
    show_frame("teacher")

    root.mainloop()
