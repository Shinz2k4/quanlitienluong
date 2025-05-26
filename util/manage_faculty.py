import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database
import sqlite3

def create_faculty_frame():
    frame = tk.Frame()
    
    tk.Label(frame, text="QUẢN LÝ KHOA", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Nhập thông tin khoa")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Các trường nhập liệu
    ttk.Label(input_frame, text="Mã khoa:").grid(row=0, column=0, padx=5, pady=5)
    faculty_id_entry = ttk.Entry(input_frame)
    faculty_id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Tên khoa:").grid(row=1, column=0, padx=5, pady=5)
    faculty_name_entry = ttk.Entry(input_frame)
    faculty_name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Viết tắt:").grid(row=2, column=0, padx=5, pady=5)
    abbreviation_entry = ttk.Entry(input_frame)
    abbreviation_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Mô tả:").grid(row=3, column=0, padx=5, pady=5)
    description_entry = ttk.Entry(input_frame)
    description_entry.grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Trưởng khoa:").grid(row=4, column=0, padx=5, pady=5)
    head_entry = ttk.Entry(input_frame)
    head_entry.grid(row=4, column=1, padx=5, pady=5)
    
    # Frame chứa các nút chức năng
    button_frame = ttk.Frame(input_frame)
    button_frame.grid(row=5, column=0, columnspan=2, pady=10)
    
    def add_faculty():
        faculty_id = faculty_id_entry.get()
        faculty_name = faculty_name_entry.get()
        abbreviation = abbreviation_entry.get()
        description = description_entry.get()
        head = head_entry.get()
        
        if not faculty_id or not faculty_name or not abbreviation:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin bắt buộc!")
            return
            
        db = Database()
        try:
            db.add_faculty(faculty_id, faculty_name, abbreviation, description, head)
            messagebox.showinfo("Thành công", "Thêm khoa thành công!")
            refresh_tree()
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã khoa đã tồn tại!")
    
    def clear_entries():
        faculty_id_entry.delete(0, tk.END)
        faculty_name_entry.delete(0, tk.END)
        abbreviation_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        head_entry.delete(0, tk.END)
    
    def refresh_tree():
        for item in tree.get_children():
            tree.delete(item)
        db = Database()
        faculties = db.get_all_faculties()
        for faculty in faculties:
            tree.insert("", tk.END, values=faculty)
    
    ttk.Button(button_frame, text="Thêm", command=add_faculty).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Xóa", command=lambda: clear_entries()).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Làm mới", command=refresh_tree).pack(side=tk.LEFT, padx=5)
    
    # Treeview hiển thị danh sách khoa
    tree = ttk.Treeview(frame, columns=("Mã khoa", "Tên khoa", "Viết tắt", "Mô tả", "Trưởng khoa"), show="headings")
    tree.heading("Mã khoa", text="Mã khoa")
    tree.heading("Tên khoa", text="Tên khoa")
    tree.heading("Viết tắt", text="Viết tắt")
    tree.heading("Mô tả", text="Mô tả")
    tree.heading("Trưởng khoa", text="Trưởng khoa")
    
    tree.column("Mã khoa", width=100)
    tree.column("Tên khoa", width=200)
    tree.column("Viết tắt", width=100)
    tree.column("Mô tả", width=200)
    tree.column("Trưởng khoa", width=150)
    
    tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Load dữ liệu ban đầu
    refresh_tree()
    
    return frame
