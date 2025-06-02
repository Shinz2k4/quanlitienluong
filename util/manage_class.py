import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_course import Database

def create_class_frame():
    frame = tk.Frame()
    db = Database()
    
    # Tiêu đề
    tk.Label(frame, text="QUẢN LÝ LỚP HỌC PHẦN", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa form nhập liệu
    input_frame = ttk.LabelFrame(frame, text="Thông tin lớp học phần")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Tạo các trường nhập liệu
    ttk.Label(input_frame, text="Kì học:").grid(row=0, column=0, padx=5, pady=5)
    semester_combo = ttk.Combobox(input_frame)
    semester_combo.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Học phần:").grid(row=1, column=0, padx=5, pady=5)
    course_combo = ttk.Combobox(input_frame)
    course_combo.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Mã lớp:").grid(row=2, column=0, padx=5, pady=5)
    class_id_entry = ttk.Entry(input_frame)
    class_id_entry.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Tên lớp:").grid(row=3, column=0, padx=5, pady=5)
    class_name_entry = ttk.Entry(input_frame)
    class_name_entry.grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(input_frame, text="Số sinh viên:").grid(row=4, column=0, padx=5, pady=5)
    student_count_entry = ttk.Entry(input_frame)
    student_count_entry.grid(row=4, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách lớp học phần")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("semester_id", "course_id", "course_name", "class_id", "class_name", "student_count")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("semester_id", text="Kì học")
    tree.heading("course_id", text="Mã học phần")
    tree.heading("course_name", text="Tên học phần")
    tree.heading("class_id", text="Mã lớp")
    tree.heading("class_name", text="Tên lớp")
    tree.heading("student_count", text="Số sinh viên")
    
    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Đặt vị trí các thành phần
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_classes():
        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)
        # Lấy và hiển thị dữ liệu mới
        classes = db.get_all_classes()
        for class_item in classes:
            tree.insert("", "end", values=class_item)
    
    def load_comboboxes():
        # Load dữ liệu cho combobox kì học
        semesters = db.get_all_semesters()
        semester_combo['values'] = [sem[1] for sem in semesters]  # Lấy tên kì học
        
        # Load dữ liệu cho combobox học phần
        courses = db.get_all_courses()
        course_combo['values'] = [f"{course[0]} - {course[1]} ({course[2]} tín chỉ)" for course in courses]  # Mã - Tên học phần - Số tín chỉ
    
    def clear_entries():
        semester_combo.set("")
        course_combo.set("")
        class_id_entry.delete(0, tk.END)
        class_name_entry.delete(0, tk.END)
        student_count_entry.delete(0, tk.END)
    
    def add_class():
        try:
            semester = semester_combo.get().strip()
            course_id = course_combo.get().split(" - ")[0].strip()  # Lấy mã học phần từ combobox
            class_id = class_id_entry.get().strip()
            class_name = class_name_entry.get().strip()
            student_count = int(student_count_entry.get())
            
            if not all([semester, course_id, class_id, class_name]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            db.add_class(semester, course_id, class_id, class_name, student_count)
            messagebox.showinfo("Thành công", "Thêm lớp học phần thành công!")
            load_classes()
            clear_entries()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def update_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp học phần cần cập nhật!")
            return
            
        try:
            semester = semester_combo.get().strip()
            course_id = course_combo.get().split(" - ")[0].strip()  # Lấy mã học phần từ combobox
            class_id = class_id_entry.get().strip()
            class_name = class_name_entry.get().strip()
            student_count = int(student_count_entry.get())
            
            if not all([semester, course_id, class_id, class_name]):
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            db.update_class(semester, course_id, class_id, class_name, student_count)
            messagebox.showinfo("Thành công", "Cập nhật lớp học phần thành công!")
            load_classes()
            clear_entries()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng số!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def delete_class():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lớp học phần cần xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa lớp học phần này?"):
            try:
                class_id = tree.item(selected[0])["values"][3]  # Lấy mã lớp từ dòng được chọn
                db.delete_class(class_id)
                messagebox.showinfo("Thành công", "Xóa lớp học phần thành công!")
                load_classes()
                clear_entries()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    # Frame chứa các nút chức năng
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", padx=5, pady=5)
    
    # Các nút chức năng
    ttk.Button(button_frame, text="Thêm", command=add_class).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa", command=delete_class).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cập nhật", command=update_class).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Làm mới", command=lambda: [load_comboboxes(), load_classes()]).pack(side="left", padx=5)
    
    # Thêm sự kiện chọn item trong treeview
    def on_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0])["values"]
            semester_combo.set(values[0])  # Kì học
    # Load dữ liệu ban đầu
    load_classes()
    load_comboboxes()
    
    return frame
