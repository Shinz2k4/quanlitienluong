import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_course import Database
from tkcalendar import DateEntry
import sqlite3

def create_semester_frame():
    frame = tk.Frame()
    db = Database()
    
    # Tiêu đề
    tk.Label(frame, text="QUẢN LÝ KÌ HỌC", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Thông tin kì học")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Tạo các trường nhập liệu
    ttk.Label(input_frame, text="Tên kì học:").grid(row=0, column=0, padx=5, pady=5)
    semester_name_entry = ttk.Entry(input_frame)
    semester_name_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Năm học:").grid(row=1, column=0, padx=5, pady=5)
    academic_year_entry = ttk.Entry(input_frame)
    academic_year_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Ngày bắt đầu:").grid(row=2, column=0, padx=5, pady=5)
    start_date_entry = DateEntry(input_frame, width=12, background='darkblue',
                               foreground='white', borderwidth=2)
    start_date_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Ngày kết thúc:").grid(row=3, column=0, padx=5, pady=5)
    end_date_entry = DateEntry(input_frame, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
    end_date_entry.grid(row=3, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách kì học")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("semester_name", "academic_year", "start_date", "end_date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("semester_name", text="Tên kì học")
    tree.heading("academic_year", text="Năm học")
    tree.heading("start_date", text="Ngày bắt đầu")
    tree.heading("end_date", text="Ngày kết thúc")
    
    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Đặt vị trí các thành phần
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def refresh_tree():
        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)
        # Lấy và hiển thị dữ liệu mới
        semesters = db.get_all_semesters()
        for semester in semesters:
            tree.insert("", "end", values=semester)

    def clear_entries():
        semester_name_entry.delete(0, tk.END)
        academic_year_entry.delete(0, tk.END)
        start_date_entry.set_date(None)
        end_date_entry.set_date(None)

    def add_semester():
        semester_name = semester_name_entry.get().strip()
        academic_year = academic_year_entry.get().strip()
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()

        if not all([semester_name, academic_year, start_date, end_date]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            db.add_semester(semester_name, academic_year, start_date, end_date)
            messagebox.showinfo("Thành công", "Thêm kì học thành công!")
            refresh_tree()
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Kì học đã tồn tại!")

    def edit_semester():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn kì học cần sửa!")
            return

        semester_name = semester_name_entry.get().strip()
        academic_year = academic_year_entry.get().strip()
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()

        if not all([semester_name, academic_year, start_date, end_date]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            old_semester = tree.item(selected_item[0])['values'][0]
            db.update_semester(old_semester, semester_name, academic_year, start_date, end_date)
            messagebox.showinfo("Thành công", "Cập nhật kì học thành công!")
            refresh_tree()
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Kì học đã tồn tại!")

    def delete_semester():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn kì học cần xóa!")
            return

        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa kì học này?"):
            semester_name = tree.item(selected_item[0])['values'][0]
            try:
                db.delete_semester(semester_name)
                messagebox.showinfo("Thành công", "Xóa kì học thành công!")
                refresh_tree()
                clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror("Lỗi", "Không thể xóa kì học này vì đang được sử dụng!")

    # Frame chứa các nút chức năng
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", padx=5, pady=5)
    
    # Các nút chức năng
    ttk.Button(button_frame, text="Thêm", command=add_semester).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa", command=delete_semester).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cập nhật", command=edit_semester).pack(side="left", padx=5)

    # Load dữ liệu ban đầu
    refresh_tree()
    
    return frame
