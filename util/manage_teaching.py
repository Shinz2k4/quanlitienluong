import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database as TeacherDB
from util.db_manage_course import Database as CourseDB

def create_teaching_frame():
    frame = tk.Frame()
    teacher_db = TeacherDB()  # Database cho giáo viên
    course_db = CourseDB()    # Database cho khóa học
    
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
    
    # Frame chứa thông tin chi tiết lớp học
    detail_frame = ttk.LabelFrame(frame, text="Thông tin chi tiết lớp học")
    detail_frame.pack(fill="x", padx=5, pady=5)
    
    # Các label hiển thị thông tin
    ttk.Label(detail_frame, text="Mã học phần:").grid(row=0, column=0, padx=5, pady=5)
    course_id_label = ttk.Label(detail_frame, text="")
    course_id_label.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(detail_frame, text="Tên học phần:").grid(row=1, column=0, padx=5, pady=5)
    course_name_label = ttk.Label(detail_frame, text="")
    course_name_label.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(detail_frame, text="Kì học:").grid(row=2, column=0, padx=5, pady=5)
    semester_label = ttk.Label(detail_frame, text="")
    semester_label.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(detail_frame, text="Số sinh viên:").grid(row=3, column=0, padx=5, pady=5)
    student_count_label = ttk.Label(detail_frame, text="")
    student_count_label.grid(row=3, column=1, padx=5, pady=5)
    
    # Frame chứa bảng dữ liệu
    table_frame = ttk.LabelFrame(frame, text="Danh sách phân công")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo Treeview
    columns = ("teacher_id", "teacher_name", "class_id", "class_name", "course_name", "semester", "student_count")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    
    # Định nghĩa các cột
    tree.heading("teacher_id", text="Mã GV")
    tree.heading("teacher_name", text="Tên giáo viên")
    tree.heading("class_id", text="Mã lớp")
    tree.heading("class_name", text="Tên lớp")
    tree.heading("course_name", text="Tên học phần")
    tree.heading("semester", text="Kì học")
    tree.heading("student_count", text="Số SV")
    
    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Đặt vị trí các thành phần
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def load_data():
        try:
            # Load teachers từ teacher_management.db
            teachers = teacher_db.get_all_teachers()
            if teachers:
                teacher_combo['values'] = [f"{t[0]} - {t[1]}" for t in teachers]
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy dữ liệu giáo viên!")
            
            # Load classes từ course_management.db
            classes = course_db.get_all_classes()
            if classes:
                class_combo['values'] = [f"{c[0]} - {c[1]}" for c in classes]
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy dữ liệu lớp học!")
            
            # Load assignments từ course_management.db
            for item in tree.get_children():
                tree.delete(item)
            assignments = course_db.get_all_teaching_assignments()
            if assignments:
                for assignment in assignments:
                    tree.insert("", "end", values=assignment)
            else:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy dữ liệu phân công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {str(e)}")
    
    def update_class_details(event):
        selected = class_combo.get()
        if selected:
            try:
                class_id = selected.split(" - ")[0]
                class_details = course_db.get_class_details(class_id)
                if class_details:
                    course_id_label.config(text=class_details[0])
                    course_name_label.config(text=class_details[1])
                    semester_label.config(text=class_details[2])
                    student_count_label.config(text=class_details[3])
                else:
                    messagebox.showwarning("Cảnh báo", "Không tìm thấy thông tin lớp học!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thông tin lớp: {str(e)}")
    
    def clear_entries():
        teacher_combo.set("")
        class_combo.set("")
        course_id_label.config(text="")
        course_name_label.config(text="")
        semester_label.config(text="")
        student_count_label.config(text="")
    
    def add_assignment():
        teacher = teacher_combo.get()
        class_selected = class_combo.get()
        
        if not teacher or not class_selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn đầy đủ thông tin!")
            return
            
        try:
            teacher_id = teacher.split(" - ")[0]
            class_id = class_selected.split(" - ")[0]
            
            # Kiểm tra xem phân công đã tồn tại chưa
            existing = course_db.check_teaching_assignment(teacher_id, class_id)
            if existing:
                messagebox.showwarning("Cảnh báo", "Phân công này đã tồn tại!")
                return
                
            course_db.add_teaching_assignment(teacher_id, class_id)
            messagebox.showinfo("Thành công", "Thêm phân công thành công!")
            load_data()
            clear_entries()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def delete_assignment():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phân công cần xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phân công này?"):
            try:
                item = tree.item(selected[0])
                teacher_id = item['values'][0]
                class_id = item['values'][2]
                
                course_db.delete_teaching_assignment(teacher_id, class_id)
                messagebox.showinfo("Thành công", "Xóa phân công thành công!")
                load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    def update_assignment():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phân công cần cập nhật!")
            return
            
        teacher = teacher_combo.get()
        class_selected = class_combo.get()
        
        if not teacher or not class_selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn đầy đủ thông tin!")
            return
            
        try:
            old_item = tree.item(selected[0])
            old_teacher_id = old_item['values'][0]
            old_class_id = old_item['values'][2]
            
            new_teacher_id = teacher.split(" - ")[0]
            new_class_id = class_selected.split(" - ")[0]
            
            course_db.update_teaching_assignment(old_teacher_id, old_class_id, new_teacher_id, new_class_id)
            messagebox.showinfo("Thành công", "Cập nhật phân công thành công!")
            load_data()
            clear_entries()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
    
    # Bind events
    class_combo.bind('<<ComboboxSelected>>', update_class_details)
    
    # Frame chứa các nút chức năng
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill="x", padx=5, pady=5)
    
    # Các nút chức năng
    ttk.Button(button_frame, text="Thêm", command=add_assignment).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa", command=delete_assignment).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Thêm").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Xóa").pack(side="left", padx=5)
    ttk.Button(button_frame, text="Cập nhật").pack(side="left", padx=5)
    
    return frame
