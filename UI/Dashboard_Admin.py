# UI/Dashboard_Admin.py
"""
Admin Dashboard - Main interface for administrators
"""

import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.UserController import UserController
from Controllers.PassengerController import PassengerController
from Controllers.DriverController import DriverController
from Controllers.VehicleController import VehicleController
from Controllers.BookingController import BookingController
from Controllers.PaymentController import PaymentController
from config import (
    DASHBOARD_WIDTH,
    DASHBOARD_HEIGHT,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    BG_COLOR,
    BG_DARK,
    TEXT_LIGHT,
    TEXT_PRIMARY,
    SIDEBAR_BG,
    FONT_LARGE_HEADING,
    FONT_LARGE,
    FONT_MEDIUM,
    PADDING_LARGE,
    BTN_PRIMARY,
    BTN_DANGER
)


class AdminDashboard:
    """
    Admin Dashboard - Complete management interface
    """
    
    def __init__(self, root, user, login_root):
        """
        Initialize Admin Dashboard
        
        Args:
            root: Dashboard window
            user: Logged in user object
            login_root: Login window reference
        """
        self.root = root
        self.user = user
        self.login_root = login_root
        
        # Initialize controllers
        self.user_ctrl = UserController()
        self.passenger_ctrl = PassengerController()
        self.driver_ctrl = DriverController()
        self.vehicle_ctrl = VehicleController()
        self.booking_ctrl = BookingController()
        self.payment_ctrl = PaymentController()
        
        self.setup_window()
        self.create_layout()
        self.show_dashboard_home()
    
    def setup_window(self):
        """Configure the dashboard window"""
        self.root.title("Taxi Booking System - Admin Dashboard")
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - DASHBOARD_WIDTH) // 2
        y = (screen_height - DASHBOARD_HEIGHT) // 2
        
        self.root.geometry(f"{DASHBOARD_WIDTH}x{DASHBOARD_HEIGHT}+{x}+{y}")
        self.root.configure(bg=BG_COLOR)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_layout(self):
        """Create main dashboard layout"""
        
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR_BG, width=250)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Header in sidebar
        header_frame = tk.Frame(self.sidebar, bg=PRIMARY_COLOR)
        header_frame.pack(fill='x', pady=(0, PADDING_LARGE))
        
        tk.Label(
            header_frame,
            text="🚕",
            font=("Segoe UI", 32),
            bg=PRIMARY_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(20, 5))
        
        tk.Label(
            header_frame,
            text="ADMIN PANEL",
            font=FONT_LARGE,
            bg=PRIMARY_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 10))
        
        tk.Label(
            header_frame,
            text=f"Welcome, {self.user.username}",
            font=FONT_MEDIUM,
            bg=PRIMARY_COLOR,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 20))
        
        # Menu buttons
        self.create_menu_button("📊 Dashboard", self.show_dashboard_home)
        self.create_menu_button("👥 Manage Passengers", self.show_passengers)
        self.create_menu_button("🚗 Manage Drivers", self.show_drivers)
        self.create_menu_button("🚙 Manage Vehicles", self.show_vehicles)
        self.create_menu_button("📋 View Bookings", self.show_bookings)
        self.create_menu_button("💰 View Payments", self.show_payments)
        self.create_menu_button("⚙️ Settings", self.show_settings)
        
        # Logout button at bottom
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
        
        # Main content area
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
            activebackground=PRIMARY_COLOR,
            activeforeground=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=20,
            command=command
        )
        btn.pack(fill='x', pady=2)
        
        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=PRIMARY_COLOR))
        btn.bind('<Leave>', lambda e: btn.config(bg=SIDEBAR_BG))
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard_home(self):
        """Show dashboard home with statistics"""
        self.clear_content()
        
        # Header
        header = tk.Label(
            self.content_frame,
            text="Dashboard Overview",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        header.pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor='w')
        
        # Statistics frame
        stats_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        stats_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        # Get statistics
        total_passengers = self.passenger_ctrl.get_total_passengers_count()
        total_drivers = self.driver_ctrl.get_total_drivers_count()
        available_drivers = self.driver_ctrl.get_available_drivers_count()
        total_vehicles = self.vehicle_ctrl.get_total_vehicles_count()
        total_bookings = self.booking_ctrl.get_total_bookings_count()
        total_revenue = self.booking_ctrl.get_total_revenue()
        
        # Create stat cards
        stats = [
            ("👥 Total Passengers", total_passengers, "#3498DB"),
            ("🚗 Total Drivers", total_drivers, "#2ECC71"),
            ("✅ Available Drivers", available_drivers, "#27AE60"),
            ("🚙 Total Vehicles", total_vehicles, "#9B59B6"),
            ("📋 Total Bookings", total_bookings, "#E67E22"),
            ("💰 Total Revenue", f"₹ {total_revenue:.2f}", "#E74C3C")
        ]
        
        row_frame = None
        for i, (label, value, color) in enumerate(stats):
            if i % 3 == 0:
                row_frame = tk.Frame(stats_frame, bg=BG_COLOR)
                row_frame.pack(fill='x', pady=10)
            
            self.create_stat_card(row_frame, label, value, color)
    
    def create_stat_card(self, parent, label, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief='raised', borderwidth=2)
        card.pack(side='left', fill='both', expand=True, padx=10)
        
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
    
    def show_passengers(self):
        """Show passenger management interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Passenger Management - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_drivers(self):
        """Show driver management interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Driver Management - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_vehicles(self):
        """Show vehicle management interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Vehicle Management - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_bookings(self):
        """Show bookings interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Bookings View - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_payments(self):
        """Show payments interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Payments View - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_settings(self):
        """Show settings interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Settings - Coming Soon",
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


# Test the dashboard
if __name__ == "__main__":
    # This is for testing only
    from Models.UserModel import UserModel
    
    root = tk.Tk()
    root.withdraw()
    
    # Create dummy user
    dummy_user = UserModel(user_id=1, username="admin", user_type="Admin")
    
    dashboard_window = tk.Toplevel()
    app = AdminDashboard(dashboard_window, dummy_user, root)
    dashboard_window.mainloop()