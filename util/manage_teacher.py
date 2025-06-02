import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database
import sqlite3
import random

def create_teacher_frame():
        frame = tk.Frame()
        
        tk.Label(frame, text="QUẢN LÝ GIÁO VIÊN", font=("Arial", 14, "bold")).pack(anchor="w")
        
        # Frame chứa form nhập liệu
        input_frame = ttk.LabelFrame(frame, text="Nhập thông tin giáo viên")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Các trường nhập liệu
        ttk.Label(input_frame, text="Mã GV:").grid(row=0, column=0, padx=5, pady=5)
        teacher_id_entry = ttk.Entry(input_frame, state="readonly")
        teacher_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Họ tên:").grid(row=1, column=0, padx=5, pady=5)
        full_name_entry = ttk.Entry(input_frame)
        full_name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Ngày sinh:").grid(row=2, column=0, padx=5, pady=5)
        birth_date_entry = ttk.Entry(input_frame)
        birth_date_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Số điện thoại:").grid(row=3, column=0, padx=5, pady=5)
        phone_entry = ttk.Entry(input_frame)
        phone_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Email:").grid(row=4, column=0, padx=5, pady=5)
        email_entry = ttk.Entry(input_frame)
        email_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Khoa:").grid(row=5, column=0, padx=5, pady=5)
        faculty_combobox = ttk.Combobox(input_frame, state="readonly")
        faculty_combobox.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Bằng cấp:").grid(row=6, column=0, padx=5, pady=5)
        degree_combobox = ttk.Combobox(input_frame, state="readonly")
        degree_combobox.grid(row=6, column=1, padx=5, pady=5)
        
        # Load dữ liệu cho combobox
        def load_combobox_data():
            db = Database()
            faculties = db.get_all_faculties()
            degrees = db.get_all_degrees()
            
            faculty_combobox['values'] = [f"{f[0]} - {f[1]}" for f in faculties]
            degree_combobox['values'] = [f"{d[0]} - {d[1]}" for d in degrees]
        
        # Frame chứa các nút chức năng
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        def generate_teacher_id():
            return str(random.randint(100000, 999999))
        
        def add_teacher():
            teacher_id = generate_teacher_id()
            full_name = full_name_entry.get()
            birth_date = birth_date_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            
            # Lấy ID từ combobox (format: "ID - Name")
            faculty_id = faculty_combobox.get().split(" - ")[0] if faculty_combobox.get() else None
            degree_id = degree_combobox.get().split(" - ")[0] if degree_combobox.get() else None
            
            if not full_name:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            db = Database()
            try:
                db.add_teacher(teacher_id, full_name, birth_date, phone, email, faculty_id, degree_id)
                messagebox.showinfo("Thành công", "Thêm giáo viên thành công!")
                refresh_tree()
                clear_entries()
            except sqlite3.IntegrityError:
                messagebox.showerror("Lỗi", "Mã giáo viên đã tồn tại!")

        def edit_teacher():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Lỗi", "Vui lòng chọn giáo viên cần sửa!")
                return
                
            teacher_id = tree.item(selected_item[0])['values'][0]
            full_name = full_name_entry.get()
            birth_date = birth_date_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            faculty_id = faculty_combobox.get().split(" - ")[0] if faculty_combobox.get() else None
            degree_id = degree_combobox.get().split(" - ")[0] if degree_combobox.get() else None
            
            if not full_name:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            db = Database()
            try:
                db.update_teacher(teacher_id, full_name, birth_date, phone, email, faculty_id, degree_id)
                messagebox.showinfo("Thành công", "Cập nhật thông tin giáo viên thành công!")
                refresh_tree()
                clear_entries()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Cập nhật thất bại: {str(e)}")

        def delete_teacher():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Lỗi", "Vui lòng chọn giáo viên cần xóa!")
                return
                
            teacher_id = tree.item(selected_item[0])['values'][0]
            
            if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giáo viên này?"):
                db = Database()
                try:
                    db.delete_teacher(teacher_id)
                    messagebox.showinfo("Thành công", "Xóa giáo viên thành công!")
                    refresh_tree()
                    clear_entries()
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Xóa thất bại: {str(e)}")
        
        def clear_entries():
            teacher_id_entry.delete(0, tk.END)
            full_name_entry.delete(0, tk.END)
            birth_date_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            faculty_combobox.set('')
            degree_combobox.set('')
        
        def refresh_tree():
            for item in tree.get_children():
                tree.delete(item)
            db = Database()
            teachers = db.get_all_teachers()
            for teacher in teachers:
                tree.insert("", tk.END, values=teacher)
        
        def on_select(event):
            selected_item = tree.selection()
            if selected_item:
                values = tree.item(selected_item[0])['values']
                teacher_id_entry.delete(0, tk.END)
                teacher_id_entry.insert(0, values[0])
                full_name_entry.delete(0, tk.END)
                full_name_entry.insert(0, values[1])
                birth_date_entry.delete(0, tk.END)
                birth_date_entry.insert(0, values[2])
                phone_entry.delete(0, tk.END)
                phone_entry.insert(0, values[3])
                email_entry.delete(0, tk.END)
                email_entry.insert(0, values[4])
                
                # Set combobox values
                faculty_text = f"{values[5]} - {values[6]}" if values[5] else ""
                degree_text = f"{values[7]} - {values[8]}" if values[7] else ""
                faculty_combobox.set(faculty_text)
                degree_combobox.set(degree_text)
        
        ttk.Button(button_frame, text="Thêm", command=add_teacher).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sửa", command=edit_teacher).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Xóa", command=delete_teacher).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Làm mới", command=lambda: [load_combobox_data(), refresh_tree()]).pack(side=tk.LEFT, padx=5)
        
        # Treeview hiển thị danh sách giáo viên
        tree = ttk.Treeview(frame, columns=("Mã GV", "Họ tên", "Ngày sinh", "Số điện thoại", "Email", "Khoa", "Bằng cấp"), show="headings")
        tree.heading("Mã GV", text="Mã GV")
        tree.heading("Họ tên", text="Họ tên")
        tree.heading("Ngày sinh", text="Ngày sinh")
        tree.heading("Số điện thoại", text="Số điện thoại")
        tree.heading("Email", text="Email")
        tree.heading("Khoa", text="Khoa")
        tree.heading("Bằng cấp", text="Bằng cấp")
        
        tree.column("Mã GV", width=100)
        tree.column("Họ tên", width=200)
        tree.column("Ngày sinh", width=100)
        tree.column("Email", width=200)
        tree.column("Khoa", width=150)
        tree.column("Bằng cấp", width=150)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Load dữ liệu ban đầu
        load_combobox_data()
        refresh_tree()
        
        return frame