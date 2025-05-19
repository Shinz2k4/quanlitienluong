import tkinter as tk
from tkinter import ttk, messagebox
from util.database import Database
import util.manage_degree as manage_degree
import util.manage_faculty as manage_faculty
import util.manage_teacher as manage_teacher
import util.statistics as statistics

def main():
    # Khởi tạo database
    db = Database()

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("Quản Lý Giáo Viên")
    root.geometry("1000x600")

    # ===== Khung chức năng bên trái =====
    frame_left = tk.Frame(root, bg="#eeeeee", width=200)
    frame_left.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(frame_left, text="CHỨC NĂNG", font=("Arial", 12, "bold"), bg="#eeeeee").pack(pady=10)

    # Tạo các nút chức năng chính
    tk.Button(frame_left, text="Quản lý bằng cấp", font=("Arial", 10)).pack(pady=5, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Quản lý khoa", font=("Arial", 10)).pack(pady=5, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Quản lý giáo viên", font=("Arial", 10)).pack(pady=5, padx=10, fill=tk.X)
    tk.Button(frame_left, text="Thống kê giáo viên", font=("Arial", 10)).pack(pady=5, padx=10, fill=tk.X)

    # ===== Khung quản lý bên phải =====
    frame_right = tk.Frame(root)
    frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Dictionary để lưu trữ các frame cho từng chức năng
    frames = {}

    # Tạo các frame
    frames["degree"] = manage_degree.create_degree_frame()
    frames["teacher"] = manage_teacher.create_teacher_frame()
    frames["faculty"] = manage_faculty.create_faculty_frame()
    frames["statistics"] = statistics.create_statistics_frame()

    # Hàm chuyển đổi giữa các frame
    def show_frame(frame_name):
        # Ẩn tất cả các frame
        for frame in frames.values():
            frame.pack_forget()
        # Hiển thị frame được chọn
        frames[frame_name].pack(fill=tk.BOTH, expand=True)

    # Gán các hàm cho các nút
    for button in frame_left.winfo_children():
        if button.cget("text") == "Quản lý bằng cấp":
            button.config(command=lambda: show_frame("degree"))
        elif button.cget("text") == "Quản lý khoa":
            button.config(command=lambda: show_frame("faculty"))
        elif button.cget("text") == "Quản lý giáo viên":
            button.config(command=lambda: show_frame("teacher"))
        elif button.cget("text") == "Thống kê giáo viên":
            button.config(command=lambda: show_frame("statistics"))

    # Hiển thị frame giáo viên mặc định
    show_frame("teacher")

    root.mainloop()
