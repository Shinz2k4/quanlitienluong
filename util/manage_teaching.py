import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database

def create_teaching_frame():
    frame = tk.Frame()
    
    # Tiêu đề
    tk.Label(frame, text="PHÂN CÔNG GIẢNG DẠY", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Thông tin phân công")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Tạo các trường nhập liệu
    ttk.Label(input_frame, text="Giáo viên:").grid(row=0, column=0, padx=5, pady=5)
    teacher_combo = ttk.Combobox(input_frame)
    teacher_combo.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Lớp học phần:").grid(row=1, column=0, padx=5, pady=5)
    class_combo = ttk.Combobox(input_frame)
    class_combo.grid(row=1, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách phân công")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("teacher_id", "teacher_name", "class_id", "class_name")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("teacher_id", text="Mã GV")
    tree.heading("teacher_name", text="Tên giáo viên")
    tree.heading("class_id", text="Mã lớp")
    tree.heading("class_name", text="Tên lớp")
    
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
