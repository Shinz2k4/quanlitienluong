import tkinter as tk
from tkinter import ttk
from util.db_manage_course import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_statistics_frame():
    frame = tk.Frame()
    db = Database()
    
    # Title
    tk.Label(frame, text="THỐNG KÊ GIẢNG VIÊN", font=("Arial", 14, "bold")).pack(anchor="w")
    
    # Faculty statistics
    faculty_stats = db.get_teacher_count_by_faculty()
    faculty_stats_frame = ttk.LabelFrame(frame, text="Thống kê giảng viên theo khoa")
    faculty_stats_frame.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = [stat[0] for stat in faculty_stats]
    sizes = [stat[1] for stat in faculty_stats]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.set_title('Phân bố giảng viên theo khoa')
    
    # Add chart to frame
    canvas = FigureCanvasTkAgg(fig, master=faculty_stats_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    return frame