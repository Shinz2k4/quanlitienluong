import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database

def create_semester_frame():
    frame = tk.Frame()
    
    # Tiêu đề
    tk.Label(frame, text="QUẢN LÝ KÌ HỌC", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Thông tin kì học")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Tạo các trường nhập liệu
    ttk.Label(input_frame, text="Mã kì học:").grid(row=0, column=0, padx=5, pady=5)
    semester_id_entry = ttk.Entry(input_frame)
    semester_id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Tên kì học:").grid(row=1, column=0, padx=5, pady=5)
    semester_name_entry = ttk.Entry(input_frame)
    semester_name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Năm học:").grid(row=2, column=0, padx=5, pady=5)
    academic_year_entry = ttk.Entry(input_frame)
    academic_year_entry.grid(row=2, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách kì học")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("semester_id", "semester_name", "academic_year")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("semester_id", text="Mã kì học")
    tree.heading("semester_name", text="Tên kì học")
    tree.heading("academic_year", text="Năm học")
    
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
