import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database

def create_course_frame():
    frame = tk.Frame()
    
    # Tiêu đề
    tk.Label(frame, text="QUẢN LÝ HỌC PHẦN", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Thông tin học phần")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Tạo các trường nhập liệu
    ttk.Label(input_frame, text="Mã học phần:").grid(row=0, column=0, padx=5, pady=5)
    course_id_entry = ttk.Entry(input_frame)
    course_id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Tên học phần:").grid(row=1, column=0, padx=5, pady=5)
    course_name_entry = ttk.Entry(input_frame)
    course_name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Số tín chỉ:").grid(row=2, column=0, padx=5, pady=5)
    credits_entry = ttk.Entry(input_frame)
    credits_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Khoa phụ trách:").grid(row=3, column=0, padx=5, pady=5)
    faculty_combo = ttk.Combobox(input_frame)
    faculty_combo.grid(row=3, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách học phần")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("course_id", "course_name", "credits", "faculty")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("course_id", text="Mã học phần")
    tree.heading("course_name", text="Tên học phần")
    tree.heading("credits", text="Số tín chỉ")
    tree.heading("faculty", text="Khoa phụ trách")
    
    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Đặt vị trí các thành phần
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Frame chứa các nút chức năng
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", padx=5, pady=5)
    
    # Các nút chức năng
    ttk.Button(button_frame, text="Thêm").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cập nhật").pack(side="left", padx=5)
    
    return frame
