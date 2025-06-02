import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database

def create_course_frame():
    frame = tk.Frame()
    db = Database()
    
    # Tiêu đề
    tk.Label(frame, text="QUẢN LÝ HỌC PHẦN", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Thông tin học phần")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Tạo các trường nhập liệu
    ttk.Label(input_frame, text="Mã số:").grid(row=0, column=0, padx=5, pady=5)
    course_id_entry = ttk.Entry(input_frame)
    course_id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Tên:").grid(row=1, column=0, padx=5, pady=5)
    course_name_entry = ttk.Entry(input_frame)
    course_name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Số tín chỉ:").grid(row=2, column=0, padx=5, pady=5)
    credits_entry = ttk.Entry(input_frame)
    credits_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Hệ số học phần:").grid(row=3, column=0, padx=5, pady=5)
    coefficient_entry = ttk.Entry(input_frame)
    coefficient_entry.grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Số tiết học:").grid(row=4, column=0, padx=5, pady=5)
    total_hours_entry = ttk.Entry(input_frame)
    total_hours_entry.grid(row=4, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách học phần")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("course_id", "course_name", "credits", "coefficient", "total_hours")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("course_id", text="Mã số")
    tree.heading("course_name", text="Tên")
    tree.heading("credits", text="Số tín chỉ")
    tree.heading("coefficient", text="Hệ số học phần")
    tree.heading("total_hours", text="Số tiết học")
    
    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Đặt vị trí các thành phần
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_courses():
        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)
        # Lấy và hiển thị dữ liệu mới
        courses = db.get_all_courses()
        for course in courses:
            tree.insert("", "end", values=course)
    
    def add_course():
        try:
            course_id = course_id_entry.get().strip()
            course_name = course_name_entry.get().strip()
            credits = int(credits_entry.get())
            coefficient = float(coefficient_entry.get())
            total_hours = int(total_hours_entry.get())
            
            if not all([course_id, course_name]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            db.add_course(course_id, course_name, credits, coefficient, total_hours)
            messagebox.showinfo("Thành công", "Thêm học phần thành công!")
            load_courses()
            clear_entries()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def update_course():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn học phần cần cập nhật!")
            return
            
        try:
            course_id = course_id_entry.get().strip()
            course_name = course_name_entry.get().strip()
            credits = int(credits_entry.get())
            coefficient = float(coefficient_entry.get())
            total_hours = int(total_hours_entry.get())
            
            if not all([course_id, course_name]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            db.update_course(course_id, course_name, credits, coefficient, total_hours)
            messagebox.showinfo("Thành công", "Cập nhật học phần thành công!")
            load_courses()
            clear_entries()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def delete_course():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn học phần cần xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa học phần này?"):
            try:
                course_id = tree.item(selected[0])["values"][0]
                db.delete_course(course_id)
                messagebox.showinfo("Thành công", "Xóa học phần thành công!")
                load_courses()
                clear_entries()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def clear_entries():
        course_id_entry.delete(0, tk.END)
        course_name_entry.delete(0, tk.END)
        credits_entry.delete(0, tk.END)
        coefficient_entry.delete(0, tk.END)
        total_hours_entry.delete(0, tk.END)
    
    def on_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0])["values"]
            course_id_entry.delete(0, tk.END)
            course_id_entry.insert(0, values[0])
            course_name_entry.delete(0, tk.END)
            course_name_entry.insert(0, values[1])
            credits_entry.delete(0, tk.END)
            credits_entry.insert(0, values[2])
            coefficient_entry.delete(0, tk.END)
            coefficient_entry.insert(0, values[3])
            total_hours_entry.delete(0, tk.END)
            total_hours_entry.insert(0, values[4])
    
    # Bind sự kiện chọn item trong tree
    tree.bind("<<TreeviewSelect>>", on_select)
    
    # Frame chứa các nút chức năng
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", padx=5, pady=5)
    
    # Các nút chức năng
    ttk.Button(button_frame, text="Thêm", command=add_course).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa", command=delete_course).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cập nhật", command=update_course).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Làm mới", command=clear_entries).pack(side="left", padx=5)
    
    # Load dữ liệu ban đầu
    load_courses()
    
    return frame
