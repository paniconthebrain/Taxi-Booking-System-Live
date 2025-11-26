# UI/Dashboard_Driver.py
"""
Driver Dashboard - Main interface for drivers
"""

import tkinter as tk
from tkinter import messagebox
from Controllers.DriverController import DriverController
from Controllers.BookingController import BookingController
from Controllers.VehicleController import VehicleController
from config import *


class DriverDashboard:
    """
    Driver Dashboard - Trip and availability management
    """
    
    def __init__(self, root, user, login_root):
        """
        Initialize Driver Dashboard
        
        Args:
            root: Dashboard window
            user: Logged in user object
            login_root: Login window reference
        """
        self.root = root
        self.user = user
        self.login_root = login_root
        
        # Initialize controllers
        self.driver_ctrl = DriverController()
        self.booking_ctrl = BookingController()
        self.vehicle_ctrl = VehicleController()
        
        # Get driver details
        self.driver = self.driver_ctrl.get_driver_by_user_id(user.user_id)
        
        self.setup_window()
        self.create_layout()
        self.show_dashboard_home()
    
    def setup_window(self):
        """Configure the dashboard window"""
        self.root.title("Taxi Booking System - Driver Dashboard")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - DASHBOARD_WIDTH) // 2
        y = (screen_height - DASHBOARD_HEIGHT) // 2
        
        self.root.geometry(f"{DASHBOARD_WIDTH}x{DASHBOARD_HEIGHT}+{x}+{y}")
        self.root.configure(bg=BG_COLOR)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_layout(self):
        """Create main dashboard layout"""
        
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Header
        header_frame = tk.Frame(self.sidebar, bg=SUCCESS_COLOR)
        header_frame.pack(fill='x', pady=(0, PADDING_LARGE))
        
        tk.Label(
            header_frame,
            text="🚗",
            font=("Segoe UI", 32),
            bg=SUCCESS_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(20, 5))
        
        tk.Label(
            header_frame,
            text="DRIVER",
            font=FONT_LARGE,
            bg=SUCCESS_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 10))
        
        welcome_text = self.driver.name if self.driver else self.user.username
        tk.Label(
            header_frame,
            text=f"Welcome, {welcome_text}",
            font=FONT_MEDIUM,
            bg=SUCCESS_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 20))
        
        # Menu buttons
        self.create_menu_button("📊 Dashboard", self.show_dashboard_home)
        self.create_menu_button("📋 My Trips", self.show_my_trips)
        self.create_menu_button("🚙 My Vehicle", self.show_my_vehicle)
        self.create_menu_button("⚡ Availability", self.show_availability)
        self.create_menu_button("👤 My Profile", self.show_profile)
        
        # Logout button
        logout_btn = tk.Button(
            self.sidebar,
            text="🚪 Logout",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=self.logout
        )
        logout_btn.pack(side='bottom', fill='x', padx=10, pady=20)
        
        # Content area
        self.content_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.content_frame.pack(side='right', fill='both', expand=True)
    
    def create_menu_button(self, text, command):
        """Create a sidebar menu button"""
        btn = tk.Button(
            self.sidebar,
            text=text,
            font=FONT_MEDIUM,
            bg=SIDEBAR_BG,
            fg=TEXT_LIGHT,
            activebackground=SUCCESS_COLOR,
            activeforeground=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=20,
            command=command
        )
        btn.pack(fill='x', pady=2)
        
        btn.bind('<Enter>', lambda e: btn.config(bg=SUCCESS_COLOR))
        btn.bind('<Leave>', lambda e: btn.config(bg=SIDEBAR_BG))
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard_home(self):
        """Show dashboard home"""
        self.clear_content()
        
        tk.Label(
            self.content_frame,
            text="Driver Dashboard",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor='w')
        
        # Statistics
        if self.driver:
            stats_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
            stats_frame.pack(fill='both', expand=True, padx=PADDING_LARGE)
            
            # Get statistics
            bookings = self.booking_ctrl.get_bookings_by_driver(self.driver.driver_id)
            completed = [b for b in bookings if b.is_completed()]
            total_earnings = sum([b.fare for b in completed if b.fare])
            
            # Availability status color
            status_color = self.driver.get_status_color()
            
            self.create_stat_card(stats_frame, "📋 Total Trips", len(bookings), "#3498DB")
            self.create_stat_card(stats_frame, "✅ Completed", len(completed), "#27AE60")
            self.create_stat_card(stats_frame, "💰 Total Earnings", f"₹ {total_earnings:.2f}", "#E74C3C")
            
            # Availability status
            status_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
            status_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
            
            tk.Label(
                status_frame,
                text=f"Current Status: {self.driver.availability}",
                font=FONT_LARGE,
                bg=status_color,
                fg=TEXT_LIGHT,
                relief='raised',
                borderwidth=2
            ).pack(fill='x', ipady=20)
    
    def create_stat_card(self, parent, label, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief='raised', borderwidth=2)
        card.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            bg=color,
            fg=TEXT_LIGHT
        ).pack(pady=(30, 5))
        
        tk.Label(
            card,
            text=label,
            font=FONT_MEDIUM,
            bg=color,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 30))
    
    def show_my_trips(self):
        """Show driver's trips"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 My Trips - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_my_vehicle(self):
        """Show vehicle information"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 My Vehicle - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_availability(self):
        """Show availability management"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Availability Management - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_profile(self):
        """Show driver profile"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 My Profile - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def logout(self):
        """Logout and return to login"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.login_root.deiconify()
    
    def on_closing(self):
        """Handle window close event"""
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.login_root.destroy()