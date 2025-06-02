import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from util.db_manage_course import Database

def create_course_statistics_frame():
    frame = tk.Frame()
    
    tk.Label(frame, text="THỐNG KÊ HỌC PHẦN", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Frame chứa các biểu đồ
    charts_frame = ttk.LabelFrame(frame, text="Biểu đồ thống kê")
    charts_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Tạo 2 frame con để chứa biểu đồ
    left_frame = ttk.Frame(charts_frame)
    left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
    
    right_frame = ttk.Frame(charts_frame)
    right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)
    
    # Hàm vẽ biểu đồ theo khoa
    def plot_faculty_stats():
        db = Database()
        faculty_stats = db.get_course_count_by_faculty()
        
        # Tạo figure mới
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Vẽ biểu đồ cột
        faculties = [stat[0] for stat in faculty_stats]
        counts = [stat[1] for stat in faculty_stats]
        
        ax.bar(faculties, counts)
        ax.set_title("Số lượng học phần theo khoa")
        ax.set_xlabel("Khoa")
        ax.set_ylabel("Số lượng")
        
        # Xoay nhãn trục x để dễ đọc
        plt.xticks(rotation=45, ha='right')
        
        # Tạo canvas để hiển thị biểu đồ trong tkinter
        canvas = FigureCanvasTkAgg(fig, master=left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Hàm vẽ biểu đồ theo số tín chỉ
    def plot_credits_stats():
        db = Database()
        credits_stats = db.get_course_count_by_credits()
        
        # Tạo figure mới
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Vẽ biểu đồ cột
        credits = [stat[0] for stat in credits_stats]
        counts = [stat[1] for stat in credits_stats]
        
        ax.bar(credits, counts)
        ax.set_title("Số lượng học phần theo số tín chỉ")
        ax.set_xlabel("Số tín chỉ")
        ax.set_ylabel("Số lượng")
        
        # Tạo canvas để hiển thị biểu đồ trong tkinter
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Vẽ các biểu đồ
    plot_faculty_stats()
    plot_credits_stats()
    
    return frame
