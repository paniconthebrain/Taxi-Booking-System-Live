# UI/Dashboard_Passenger.py
"""
Passenger Dashboard - Main interface for passengers
"""

import tkinter as tk
from tkinter import messagebox
from Controllers.PassengerController import PassengerController
from Controllers.BookingController import BookingController
from config import *


class PassengerDashboard:
    """
    Passenger Dashboard - Booking and trip management
    """
    
    def __init__(self, root, user, login_root):
        """
        Initialize Passenger Dashboard
        
        Args:
            root: Dashboard window
            user: Logged in user object
            login_root: Login window reference
        """
        self.root = root
        self.user = user
        self.login_root = login_root
        
        # Initialize controllers
        self.passenger_ctrl = PassengerController()
        self.booking_ctrl = BookingController()
        
        # Get passenger details
        self.passenger = self.passenger_ctrl.get_passenger_by_user_id(user.user_id)
        
        self.setup_window()
        self.create_layout()
        self.show_dashboard_home()
    
    def setup_window(self):
        """Configure the dashboard window"""
        self.root.title("Taxi Booking System - Passenger Dashboard")
        
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
        header_frame = tk.Frame(self.sidebar, bg=SECONDARY_COLOR)
        header_frame.pack(fill='x', pady=(0, PADDING_LARGE))
        
        tk.Label(
            header_frame,
            text="🚕",
            font=("Segoe UI", 32),
            bg=SECONDARY_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(20, 5))
        
        tk.Label(
            header_frame,
            text="PASSENGER",
            font=FONT_LARGE,
            bg=SECONDARY_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 10))
        
        welcome_text = self.passenger.name if self.passenger else self.user.username
        tk.Label(
            header_frame,
            text=f"Welcome, {welcome_text}",
            font=FONT_MEDIUM,
            bg=SECONDARY_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 20))
        
        # Menu buttons
        self.create_menu_button("📊 Dashboard", self.show_dashboard_home)
        self.create_menu_button("🚖 Book a Ride", self.show_book_ride)
        self.create_menu_button("📋 My Bookings", self.show_my_bookings)
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
            activebackground=SECONDARY_COLOR,
            activeforeground=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=20,
            command=command
        )
        btn.pack(fill='x', pady=2)
        
        btn.bind('<Enter>', lambda e: btn.config(bg=SECONDARY_COLOR))
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
            text="Passenger Dashboard",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor='w')
        
        # Statistics
        if self.passenger:
            stats_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
            stats_frame.pack(fill='both', expand=True, padx=PADDING_LARGE)
            
            bookings = self.booking_ctrl.get_bookings_by_passenger(self.passenger.passenger_id)
            pending = [b for b in bookings if b.is_pending()]
            completed = [b for b in bookings if b.is_completed()]
            
            self.create_stat_card(stats_frame, "📋 Total Bookings", len(bookings), "#3498DB")
            self.create_stat_card(stats_frame, "⏳ Pending", len(pending), "#F39C12")
            self.create_stat_card(stats_frame, "✅ Completed", len(completed), "#27AE60")
    
    def create_stat_card(self, parent, label, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief='raised', borderwidth=2)
        card.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 36, "bold"),
            bg=color,
            fg=TEXT_LIGHT
        ).pack(pady=(30, 5))
        
        tk.Label(
            card,
            text=label,
            font=FONT_LARGE,
            bg=color,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 30))
    
    def show_book_ride(self):
        """Show booking interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Book a Ride - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_my_bookings(self):
        """Show user's bookings"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 My Bookings - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_profile(self):
        """Show user profile"""
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