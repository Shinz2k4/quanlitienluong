import tkinter as tk
from tkinter import ttk
from util.database import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_statistics_frame():
    frame = tk.Frame()
    
    tk.Label(frame, text="THỐNG KÊ GIÁO VIÊN", font=("Arial", 14, "bold")).pack(anchor="w")
    
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
        faculty_stats = db.get_teacher_count_by_faculty()
        
        # Tạo figure mới
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Vẽ biểu đồ cột
        faculties = [stat[0] for stat in faculty_stats]
        counts = [stat[1] for stat in faculty_stats]
        
        ax.bar(faculties, counts)
        ax.set_title("Số lượng giáo viên theo khoa")
        ax.set_xlabel("Khoa")
        ax.set_ylabel("Số lượng")
        
        # Xoay nhãn trục x để dễ đọc
        plt.xticks(rotation=45, ha='right')
        
        # Tạo canvas để hiển thị biểu đồ trong tkinter
        canvas = FigureCanvasTkAgg(fig, master=left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Hàm vẽ biểu đồ theo bằng cấp
    def plot_degree_stats():
        db = Database()
        degree_stats = db.get_teacher_count_by_degree()
        
        # Tạo figure mới
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Vẽ biểu đồ cột
        degrees = [stat[0] for stat in degree_stats]
        counts = [stat[1] for stat in degree_stats]
        
        ax.bar(degrees, counts)
        ax.set_title("Số lượng giáo viên theo bằng cấp")
        ax.set_xlabel("Bằng cấp")
        ax.set_ylabel("Số lượng")
        
        # Xoay nhãn trục x để dễ đọc
        plt.xticks(rotation=45, ha='right')
        
        # Tạo canvas để hiển thị biểu đồ trong tkinter
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    # Vẽ các biểu đồ
    plot_faculty_stats()
    plot_degree_stats()
    
    return frame
