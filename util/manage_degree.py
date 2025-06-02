import tkinter as tk
from tkinter import ttk, messagebox
from util.db_manage_teacher import Database
import sqlite3

def create_degree_frame():
    frame = tk.Frame()
    
    # Title
    title_label = tk.Label(frame, text="QUẢN LÝ BẰNG CẤP", font=("Arial", 14, "bold"))
    title_label.pack(anchor="w")
    
    # Input form frame
    input_frame = ttk.LabelFrame(frame, text="Nhập thông tin bằng cấp")
    input_frame.pack(fill="x", padx=5, pady=5)
    
    # Input fields
    fields = [
        ("Mã bằng cấp:", "degree_id"),
        ("Tên đầy đủ:", "full_name"),
        ("Viết tắt:", "abbreviation")
    ]
    
    entries = {}
    for i, (label_text, field_name) in enumerate(fields):
        ttk.Label(input_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5)
        entry = ttk.Entry(input_frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[field_name] = entry
    
    # Button frame
    button_frame = ttk.Frame(input_frame)
    button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    def add_degree():
        values = {name: entry.get() for name, entry in entries.items()}
        
        if not all(values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        db = Database()
        try:
            db.add_degree(values["degree_id"], values["full_name"], values["abbreviation"])
            messagebox.showinfo("Thành công", "Thêm bằng cấp thành công!")
            refresh_tree()
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã bằng cấp đã tồn tại!")

    def edit_degree():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn bằng cấp cần sửa!")
            return
            
        values = {name: entry.get() for name, entry in entries.items()}
        if not all(values.values()):
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        old_id = tree.item(selected_item[0])['values'][0]
        db = Database()
        try:
            # Fixed: Removed old_id from parameters since it's not needed
            db.update_degree(values["degree_id"], values["full_name"], values["abbreviation"])
            messagebox.showinfo("Thành công", "Sửa bằng cấp thành công!")
            refresh_tree()
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã bằng cấp đã tồn tại!")
    
    def delete_degree():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn bằng cấp cần xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bằng cấp này?"):
            degree_id = tree.item(selected_item[0])['values'][0]
            db = Database()
            try:
                db.delete_degree(degree_id)
                messagebox.showinfo("Thành công", "Xóa bằng cấp thành công!")
                refresh_tree()
                clear_entries()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Xóa thất bại: {str(e)}")
    
    def clear_entries():
        for entry in entries.values():
            entry.delete(0, tk.END)
    
    def refresh_tree():
        for item in tree.get_children():
            tree.delete(item)
        db = Database()
        degrees = db.get_all_degrees()
        for degree in degrees:
            tree.insert("", tk.END, values=degree)

    def on_select(event):
        selected_item = tree.selection()
        if selected_item:
            values = tree.item(selected_item[0])['values']
            for i, (_, field_name) in enumerate(fields):
                entries[field_name].delete(0, tk.END)
                entries[field_name].insert(0, values[i])
    
    # Buttons
    ttk.Button(button_frame, text="Thêm", command=add_degree).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Sửa", command=edit_degree).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Xóa", command=delete_degree).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Làm mới", command=refresh_tree).pack(side=tk.LEFT, padx=5)
    
    # Treeview
    columns = ("Mã bằng cấp", "Tên đầy đủ", "Viết tắt")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col != "Tên đầy đủ" else 200)
    
    tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    tree.bind('<<TreeviewSelect>>', on_select)
    
    # Initial data load
    refresh_tree()
    
    return frame
