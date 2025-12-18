# UI/Dashboard_Admin.py
"""
Admin Dashboard - Main interface for administrators
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
    TEXT_SECONDARY,
    SIDEBAR_BG,
    FONT_LARGE_HEADING,
    FONT_LARGE,
    FONT_MEDIUM,
    PADDING_LARGE,
    PADDING_MEDIUM,
    BTN_PRIMARY,
    BTN_SUCCESS,
    BTN_DANGER,
    BTN_WARNING,
    INPUT_BG,
    CURRENCY_SYMBOL,
    validate_email,
    validate_phone,
    validate_license,
    DRIVER_AVAILABLE,
    DRIVER_BUSY,
    DRIVER_OFFLINE,
    DRIVER_STATUSES,
    BOOKING_STATUS_PENDING,
    BOOKING_STATUS_CONFIRMED,
    BOOKING_STATUS_IN_PROGRESS,
    BOOKING_STATUS_COMPLETED,
    BOOKING_STATUS_CANCELLED,
    BOOKING_STATUSES
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
        self.create_menu_button("📑 Reports", self.show_reports)
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
            ("💰 Total Revenue", f"{CURRENCY_SYMBOL} {total_revenue:.2f}", "#E74C3C")
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
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Label(
            header_frame,
            text="👥 Manage Passengers",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left')
        
        # Search and Add button frame
        search_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        search_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_MEDIUM))
        
        # Search
        tk.Label(
            search_frame,
            text="Search:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left', padx=(0, PADDING_MEDIUM))
        
        search_entry = tk.Entry(
            search_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            width=30
        )
        search_entry.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        def refresh_passengers():
            """Refresh passenger list"""
            search_term = search_entry.get().strip()
            if search_term:
                passengers = self.passenger_ctrl.search_passengers(search_term)
            else:
                passengers = self.passenger_ctrl.get_all_passengers()
            
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Populate tree
            for passenger in passengers:
                from datetime import datetime
                created_date = ""
                if passenger.created_at:
                    if isinstance(passenger.created_at, datetime):
                        created_date = passenger.created_at.strftime("%d-%m-%Y")
                    else:
                        created_date = str(passenger.created_at)[:10]
                
                tree.insert('', 'end', values=(
                    passenger.passenger_id,
                    passenger.name or "",
                    passenger.email or "",
                    passenger.phone or "",
                    passenger.address or "N/A",
                    created_date
                ))
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=refresh_passengers,
            padx=15,
            pady=5
        )
        search_btn.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        refresh_btn = tk.Button(
            search_frame,
            text="🔄 Refresh",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=refresh_passengers,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        # add_btn = tk.Button(
        #     search_frame,
        #     text="➕ Add Passenger",
        #     font=FONT_MEDIUM,
        #     bg=BTN_SUCCESS,
        #     fg=TEXT_LIGHT,
        #     relief='flat',
        #     cursor='hand2',
        #     command=self.add_passenger_dialog,
        #     padx=15,
        #     pady=5
        # )
        # add_btn.pack(side='right')
        
        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: refresh_passengers())
        
        # Table frame with scrollbars
        table_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        table_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview
        tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'Email', 'Phone', 'Address', 'Created'),
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)
        
        # Column headings
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('Email', text='Email')
        tree.heading('Phone', text='Phone')
        tree.heading('Address', text='Address')
        tree.heading('Created', text='Created Date')
        
        # Column widths
        tree.column('ID', width=50, anchor='center')
        tree.column('Name', width=150, anchor='w')
        tree.column('Email', width=200, anchor='w')
        tree.column('Phone', width=120, anchor='w')
        tree.column('Address', width=200, anchor='w')
        tree.column('Created', width=100, anchor='center')
        
        tree.pack(side='left', fill='both', expand=True)
        
        # Action buttons frame
        action_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        action_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        def view_passenger():
            """View passenger details"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a passenger to view")
                return
            
            item = tree.item(selected[0])
            passenger_id = item['values'][0]
            passenger = self.passenger_ctrl.get_passenger_by_id(passenger_id)
            
            if passenger:
                from datetime import datetime
                created_date = ""
                if passenger.created_at:
                    if isinstance(passenger.created_at, datetime):
                        created_date = passenger.created_at.strftime("%d-%m-%Y %I:%M %p")
                    else:
                        created_date = str(passenger.created_at)
                
                details = (
                    f"Passenger Details\n\n"
                    f"ID: {passenger.passenger_id}\n"
                    f"Name: {passenger.name or 'N/A'}\n"
                    f"Email: {passenger.email or 'N/A'}\n"
                    f"Phone: {passenger.phone or 'N/A'}\n"
                    f"Address: {passenger.address or 'N/A'}\n"
                    f"User ID: {passenger.user_id or 'N/A'}\n"
                    f"Created: {created_date}"
                )
                messagebox.showinfo("Passenger Details", details)
        
        def edit_passenger():
            """Edit passenger"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a passenger to edit")
                return
            
            item = tree.item(selected[0])
            passenger_id = item['values'][0]
            self.edit_passenger_dialog(passenger_id)
        
        def delete_passenger():
            """Delete passenger"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a passenger to delete")
                return
            
            item = tree.item(selected[0])
            passenger_id = item['values'][0]
            passenger_name = item['values'][1]
            
            if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete passenger:\n{passenger_name} (ID: {passenger_id})?\n\nThis action cannot be undone!"
            ):
                success, message = self.passenger_ctrl.delete_passenger(passenger_id)
                if success:
                    messagebox.showinfo("Success", message)
                    refresh_passengers()
                else:
                    messagebox.showerror("Error", f"Failed to delete: {message}")
        
        # Action buttons
        view_btn = tk.Button(
            action_frame,
            text="👁️ View Details",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=view_passenger,
            padx=15,
            pady=8
        )
        view_btn.pack(side='left', padx=5)
        
        edit_btn = tk.Button(
            action_frame,
            text="✏️ Edit",
            font=FONT_MEDIUM,
            bg=BTN_WARNING,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=edit_passenger,
            padx=15,
            pady=8
        )
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="🗑️ Delete",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=delete_passenger,
            padx=15,
            pady=8
        )
        delete_btn.pack(side='left', padx=5)
        
        # Initial load
        refresh_passengers()
    
    def add_passenger_dialog(self):
        """Open dialog to add new passenger"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Passenger")
        dialog.geometry("500x450")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"500x450+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Add New Passenger",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE)
        
        form_frame = tk.Frame(dialog, bg=BG_COLOR)
        form_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Name
        tk.Label(form_frame, text="Name:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        name_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        
        # Email
        tk.Label(form_frame, text="Email:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=1, column=0, sticky='w', pady=5)
        email_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        email_entry.grid(row=1, column=1, pady=5, padx=10, sticky='ew')
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=2, column=0, sticky='w', pady=5)
        phone_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        phone_entry.grid(row=2, column=1, pady=5, padx=10, sticky='ew')
        
        # Address
        tk.Label(form_frame, text="Address:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=3, column=0, sticky='nw', pady=5)
        address_text = tk.Text(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30, height=3, wrap='word')
        address_text.grid(row=3, column=1, pady=5, padx=10, sticky='ew')
        
        form_frame.columnconfigure(1, weight=1)
        
        def save_passenger():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_text.get('1.0', 'end-1c').strip()
            
            if not name or not email or not phone:
                messagebox.showerror("Error", "Name, Email, and Phone are required!")
                return
            
            if not validate_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            
            if not validate_phone(phone):
                messagebox.showerror("Error", "Invalid phone number! Must be 10 digits.")
                return
            
            # Note: user_id is None for now - in real app, you'd create a user account first
            success, message, passenger_id = self.passenger_ctrl.create_passenger(
                name, email, phone, address, None
            )
            
            if success:
                messagebox.showinfo("Success", f"Passenger added successfully!\nID: {passenger_id}")
                dialog.destroy()
                # Refresh the passenger list
                self.show_passengers()
            else:
                messagebox.showerror("Error", f"Failed to add passenger: {message}")
        
        button_frame = tk.Frame(dialog, bg=BG_COLOR)
        button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Button(
            button_frame,
            text="Save",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=save_passenger,
            padx=20,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=dialog.destroy,
            padx=20,
            pady=8
        ).pack(side='right', padx=5)
    
    def edit_passenger_dialog(self, passenger_id):
        """Open dialog to edit passenger"""
        passenger = self.passenger_ctrl.get_passenger_by_id(passenger_id)
        if not passenger:
            messagebox.showerror("Error", "Passenger not found!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Passenger - {passenger.name}")
        dialog.geometry("500x450")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"500x450+{x}+{y}")
        
        tk.Label(
            dialog,
            text=f"Edit Passenger (ID: {passenger_id})",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE)
        
        form_frame = tk.Frame(dialog, bg=BG_COLOR)
        form_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Name
        tk.Label(form_frame, text="Name:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        name_entry.insert(0, passenger.name or "")
        name_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        
        # Email
        tk.Label(form_frame, text="Email:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=1, column=0, sticky='w', pady=5)
        email_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        email_entry.insert(0, passenger.email or "")
        email_entry.grid(row=1, column=1, pady=5, padx=10, sticky='ew')
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=2, column=0, sticky='w', pady=5)
        phone_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        phone_entry.insert(0, passenger.phone or "")
        phone_entry.grid(row=2, column=1, pady=5, padx=10, sticky='ew')
        
        # Address
        tk.Label(form_frame, text="Address:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=3, column=0, sticky='nw', pady=5)
        address_text = tk.Text(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30, height=3, wrap='word')
        address_text.insert('1.0', passenger.address or "")
        address_text.grid(row=3, column=1, pady=5, padx=10, sticky='ew')
        
        form_frame.columnconfigure(1, weight=1)
        
        def update_passenger():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_text.get('1.0', 'end-1c').strip()
            
            if not name or not email or not phone:
                messagebox.showerror("Error", "Name, Email, and Phone are required!")
                return
            
            if not validate_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            
            if not validate_phone(phone):
                messagebox.showerror("Error", "Invalid phone number! Must be 10 digits.")
                return
            
            success, message = self.passenger_ctrl.update_passenger(
                passenger_id, name, email, phone, address
            )
            
            if success:
                messagebox.showinfo("Success", "Passenger updated successfully!")
                dialog.destroy()
                # Refresh the passenger list
                self.show_passengers()
            else:
                messagebox.showerror("Error", f"Failed to update passenger: {message}")
        
        button_frame = tk.Frame(dialog, bg=BG_COLOR)
        button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Button(
            button_frame,
            text="Update",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=update_passenger,
            padx=20,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=dialog.destroy,
            padx=20,
            pady=8
        ).pack(side='right', padx=5)
    
    def show_drivers(self):
        """Show driver management interface"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Label(
            header_frame,
            text="🚗 Manage Drivers",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left')
        
        # Search and Add button frame
        search_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        search_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_MEDIUM))
        
        # Search
        tk.Label(
            search_frame,
            text="Search:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left', padx=(0, PADDING_MEDIUM))
        
        search_entry = tk.Entry(
            search_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            width=30
        )
        search_entry.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        # Table frame with scrollbars
        table_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        table_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview
        tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'License', 'Phone', 'Email', 'Status', 'Created'),
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)
        
        # Column headings
        tree.heading('ID', text='ID')
        tree.heading('Name', text='Name')
        tree.heading('License', text='License Number')
        tree.heading('Phone', text='Phone')
        tree.heading('Email', text='Email')
        tree.heading('Status', text='Status')
        tree.heading('Created', text='Created Date')
        
        # Column widths
        tree.column('ID', width=50, anchor='center')
        tree.column('Name', width=150, anchor='w')
        tree.column('License', width=120, anchor='w')
        tree.column('Phone', width=120, anchor='w')
        tree.column('Email', width=180, anchor='w')
        tree.column('Status', width=100, anchor='center')
        tree.column('Created', width=100, anchor='center')
        
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_drivers():
            """Refresh driver list"""
            search_term = search_entry.get().strip()
            if search_term:
                drivers = self.driver_ctrl.search_drivers(search_term)
            else:
                drivers = self.driver_ctrl.get_all_drivers()
            
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Populate tree
            for driver in drivers:
                from datetime import datetime
                created_date = ""
                if driver.created_at:
                    if isinstance(driver.created_at, datetime):
                        created_date = driver.created_at.strftime("%d-%m-%Y")
                    else:
                        created_date = str(driver.created_at)[:10]
                
                tree.insert('', 'end', values=(
                    driver.driver_id,
                    driver.name or "",
                    driver.license_number or "",
                    driver.phone or "",
                    driver.email or "N/A",
                    driver.availability or "N/A",
                    created_date
                ))
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=refresh_drivers,
            padx=15,
            pady=5
        )
        search_btn.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        refresh_btn = tk.Button(
            search_frame,
            text="🔄 Refresh",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=refresh_drivers,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        # add_btn = tk.Button(
        #     search_frame,
        #     text="➕ Add Driver",
        #     font=FONT_MEDIUM,
        #     bg=BTN_SUCCESS,
        #     fg=TEXT_LIGHT,
        #     relief='flat',
        #     cursor='hand2',
        #     command=self.add_driver_dialog,
        #     padx=15,
        #     pady=5
        # )
        # add_btn.pack(side='right')
        
        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: refresh_drivers())
        
        # Action buttons frame
        action_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        action_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        def view_driver():
            """View driver details"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a driver to view")
                return
            
            item = tree.item(selected[0])
            driver_id = item['values'][0]
            driver = self.driver_ctrl.get_driver_by_id(driver_id)
            
            if driver:
                from datetime import datetime
                created_date = ""
                if driver.created_at:
                    if isinstance(driver.created_at, datetime):
                        created_date = driver.created_at.strftime("%d-%m-%Y %I:%M %p")
                    else:
                        created_date = str(driver.created_at)
                
                details = (
                    f"Driver Details\n\n"
                    f"ID: {driver.driver_id}\n"
                    f"Name: {driver.name or 'N/A'}\n"
                    f"License Number: {driver.license_number or 'N/A'}\n"
                    f"Phone: {driver.phone or 'N/A'}\n"
                    f"Email: {driver.email or 'N/A'}\n"
                    f"Status: {driver.availability or 'N/A'}\n"
                    f"User ID: {driver.user_id or 'N/A'}\n"
                    f"Created: {created_date}"
                )
                messagebox.showinfo("Driver Details", details)
        
        def edit_driver():
            """Edit driver"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a driver to edit")
                return
            
            item = tree.item(selected[0])
            driver_id = item['values'][0]
            self.edit_driver_dialog(driver_id)
        
        def delete_driver():
            """Delete driver"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a driver to delete")
                return
            
            item = tree.item(selected[0])
            driver_id = item['values'][0]
            driver_name = item['values'][1]
            
            if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete driver:\n{driver_name} (ID: {driver_id})?\n\nThis action cannot be undone!"
            ):
                success, message = self.driver_ctrl.delete_driver(driver_id)
                if success:
                    messagebox.showinfo("Success", message)
                    refresh_drivers()
                else:
                    messagebox.showerror("Error", f"Failed to delete: {message}")
        
        # Action buttons
        view_btn = tk.Button(
            action_frame,
            text="👁️ View Details",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=view_driver,
            padx=15,
            pady=8
        )
        view_btn.pack(side='left', padx=5)
        
        edit_btn = tk.Button(
            action_frame,
            text="✏️ Edit",
            font=FONT_MEDIUM,
            bg=BTN_WARNING,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=edit_driver,
            padx=15,
            pady=8
        )
        edit_btn.pack(side='left', padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="🗑️ Delete",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=delete_driver,
            padx=15,
            pady=8
        )
        delete_btn.pack(side='left', padx=5)
        
        # Initial load
        refresh_drivers()
    
    def add_driver_dialog(self):
        """Open dialog to add new driver"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Driver")
        dialog.geometry("500x500")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"500x500+{x}+{y}")
        
        tk.Label(
            dialog,
            text="Add New Driver",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE)
        
        form_frame = tk.Frame(dialog, bg=BG_COLOR)
        form_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Name
        tk.Label(form_frame, text="Name:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        name_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        
        # License Number
        tk.Label(form_frame, text="License Number:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=1, column=0, sticky='w', pady=5)
        license_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        license_entry.grid(row=1, column=1, pady=5, padx=10, sticky='ew')
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=2, column=0, sticky='w', pady=5)
        phone_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        phone_entry.grid(row=2, column=1, pady=5, padx=10, sticky='ew')
        
        # Email
        tk.Label(form_frame, text="Email:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=3, column=0, sticky='w', pady=5)
        email_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        email_entry.grid(row=3, column=1, pady=5, padx=10, sticky='ew')
        
        # Availability Status
        tk.Label(form_frame, text="Status:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=4, column=0, sticky='w', pady=5)
        status_var = tk.StringVar(value=DRIVER_AVAILABLE)
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=DRIVER_STATUSES, state='readonly', width=27)
        status_combo.grid(row=4, column=1, pady=5, padx=10, sticky='ew')
        
        form_frame.columnconfigure(1, weight=1)
        
        def save_driver():
            name = name_entry.get().strip()
            license_number = license_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            availability = status_var.get()
            
            if not name or not license_number or not phone:
                messagebox.showerror("Error", "Name, License Number, and Phone are required!")
                return
            
            if not validate_license(license_number):
                messagebox.showerror("Error", "Invalid license number format!")
                return
            
            if not validate_phone(phone):
                messagebox.showerror("Error", "Invalid phone number! Must be 10 digits.")
                return
            
            if email and not validate_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            
            # Note: user_id is None for now - in real app, you'd create a user account first
            success, message, driver_id = self.driver_ctrl.create_driver(
                name, license_number, phone, email, None, availability
            )
            
            if success:
                messagebox.showinfo("Success", f"Driver added successfully!\nID: {driver_id}")
                dialog.destroy()
                # Refresh the driver list
                self.show_drivers()
            else:
                messagebox.showerror("Error", f"Failed to add driver: {message}")
        
        button_frame = tk.Frame(dialog, bg=BG_COLOR)
        button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Button(
            button_frame,
            text="Save",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=save_driver,
            padx=20,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=dialog.destroy,
            padx=20,
            pady=8
        ).pack(side='right', padx=5)
    
    def edit_driver_dialog(self, driver_id):
        """Open dialog to edit driver"""
        driver = self.driver_ctrl.get_driver_by_id(driver_id)
        if not driver:
            messagebox.showerror("Error", "Driver not found!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Driver - {driver.name}")
        dialog.geometry("500x500")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"500x500+{x}+{y}")
        
        tk.Label(
            dialog,
            text=f"Edit Driver (ID: {driver_id})",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE)
        
        form_frame = tk.Frame(dialog, bg=BG_COLOR)
        form_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)
        
        # Name
        tk.Label(form_frame, text="Name:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        name_entry.insert(0, driver.name or "")
        name_entry.grid(row=0, column=1, pady=5, padx=10, sticky='ew')
        
        # License Number
        tk.Label(form_frame, text="License Number:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=1, column=0, sticky='w', pady=5)
        license_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        license_entry.insert(0, driver.license_number or "")
        license_entry.grid(row=1, column=1, pady=5, padx=10, sticky='ew')
        
        # Phone
        tk.Label(form_frame, text="Phone:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=2, column=0, sticky='w', pady=5)
        phone_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        phone_entry.insert(0, driver.phone or "")
        phone_entry.grid(row=2, column=1, pady=5, padx=10, sticky='ew')
        
        # Email
        tk.Label(form_frame, text="Email:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=3, column=0, sticky='w', pady=5)
        email_entry = tk.Entry(form_frame, font=FONT_MEDIUM, bg=INPUT_BG, width=30)
        email_entry.insert(0, driver.email or "")
        email_entry.grid(row=3, column=1, pady=5, padx=10, sticky='ew')
        
        # Availability Status
        tk.Label(form_frame, text="Status:", font=FONT_MEDIUM, bg=BG_COLOR, fg=TEXT_PRIMARY).grid(row=4, column=0, sticky='w', pady=5)
        status_var = tk.StringVar(value=driver.availability or DRIVER_AVAILABLE)
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=DRIVER_STATUSES, state='readonly', width=27)
        status_combo.grid(row=4, column=1, pady=5, padx=10, sticky='ew')
        
        form_frame.columnconfigure(1, weight=1)
        
        def update_driver():
            name = name_entry.get().strip()
            license_number = license_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            availability = status_var.get()
            
            if not name or not license_number or not phone:
                messagebox.showerror("Error", "Name, License Number, and Phone are required!")
                return
            
            if not validate_license(license_number):
                messagebox.showerror("Error", "Invalid license number format!")
                return
            
            if not validate_phone(phone):
                messagebox.showerror("Error", "Invalid phone number! Must be 10 digits.")
                return
            
            if email and not validate_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            
            success, message = self.driver_ctrl.update_driver(
                driver_id, name, license_number, phone, email, availability
            )
            
            if success:
                messagebox.showinfo("Success", "Driver updated successfully!")
                dialog.destroy()
                # Refresh the driver list
                self.show_drivers()
            else:
                messagebox.showerror("Error", f"Failed to update driver: {message}")
        
        button_frame = tk.Frame(dialog, bg=BG_COLOR)
        button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Button(
            button_frame,
            text="Update",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=update_driver,
            padx=20,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=dialog.destroy,
            padx=20,
            pady=8
        ).pack(side='right', padx=5)
    
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
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Label(
            header_frame,
            text="📋 View Bookings",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left')
        
        # Filter and Refresh frame
        filter_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        filter_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_MEDIUM))
        
        # Status filter
        tk.Label(
            filter_frame,
            text="Filter by Status:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left', padx=(0, PADDING_MEDIUM))
        
        status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=status_var,
            values=["All"] + BOOKING_STATUSES,
            state='readonly',
            width=15
        )
        status_combo.pack(side='left', padx=(0, PADDING_MEDIUM))
        
        # Table frame with scrollbars
        table_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        table_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical')
        v_scrollbar.pack(side='right', fill='y')
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview
        tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Passenger', 'Driver', 'Pickup', 'Destination', 'Status', 'Fare', 'Date'),
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        
        # Configure scrollbars
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)
        
        # Column headings
        tree.heading('ID', text='ID')
        tree.heading('Passenger', text='Passenger')
        tree.heading('Driver', text='Driver')
        tree.heading('Pickup', text='Pickup Location')
        tree.heading('Destination', text='Destination')
        tree.heading('Status', text='Status')
        tree.heading('Fare', text='Fare')
        tree.heading('Date', text='Booking Date')
        
        # Column widths
        tree.column('ID', width=50, anchor='center')
        tree.column('Passenger', width=120, anchor='w')
        tree.column('Driver', width=120, anchor='w')
        tree.column('Pickup', width=180, anchor='w')
        tree.column('Destination', width=180, anchor='w')
        tree.column('Status', width=100, anchor='center')
        tree.column('Fare', width=100, anchor='center')
        tree.column('Date', width=120, anchor='center')
        
        tree.pack(side='left', fill='both', expand=True)
        
        def refresh_bookings():
            """Refresh booking list"""
            status_filter = status_var.get()
            
            if status_filter == "All":
                bookings = self.booking_ctrl.get_all_bookings()
            else:
                bookings = self.booking_ctrl.get_bookings_by_status(status_filter)
            
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Populate tree
            for booking in bookings:
                from datetime import datetime
                
                # Get passenger name
                passenger_name = "N/A"
                if booking.passenger_id:
                    passenger = self.passenger_ctrl.get_passenger_by_id(booking.passenger_id)
                    if passenger:
                        passenger_name = passenger.name or "N/A"
                
                # Get driver name
                driver_name = "Not Assigned"
                if booking.driver_id:
                    driver = self.driver_ctrl.get_driver_by_id(booking.driver_id)
                    if driver:
                        driver_name = driver.name or "N/A"
                
                # Format date
                booking_date = ""
                if booking.booking_date:
                    if isinstance(booking.booking_date, datetime):
                        booking_date = booking.booking_date.strftime("%d-%m-%Y %H:%M")
                    else:
                        booking_date = str(booking.booking_date)[:16]
                
                # Format fare
                fare_str = "N/A"
                if booking.fare:
                    fare_str = f"{CURRENCY_SYMBOL} {booking.fare:.2f}"
                
                tree.insert('', 'end', values=(
                    booking.booking_id,
                    passenger_name,
                    driver_name,
                    booking.pickup_location or "N/A",
                    booking.destination or "N/A",
                    booking.status or "N/A",
                    fare_str,
                    booking_date
                ))
        
        refresh_btn = tk.Button(
            filter_frame,
            text="🔄 Refresh",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=refresh_bookings,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side='right')
        
        # Bind status change to refresh
        status_combo.bind('<<ComboboxSelected>>', lambda e: refresh_bookings())
        
        # Action buttons frame
        action_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        action_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        def view_booking():
            """View booking details"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a booking to view")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            booking = self.booking_ctrl.get_booking_by_id(booking_id)
            
            if booking:
                from datetime import datetime
                
                # Get passenger name
                passenger_name = "N/A"
                if booking.passenger_id:
                    passenger = self.passenger_ctrl.get_passenger_by_id(booking.passenger_id)
                    if passenger:
                        passenger_name = passenger.name or "N/A"
                
                # Get driver name
                driver_name = "Not Assigned"
                if booking.driver_id:
                    driver = self.driver_ctrl.get_driver_by_id(booking.driver_id)
                    if driver:
                        driver_name = driver.name or "N/A"
                
                booking_date = ""
                if booking.booking_date:
                    if isinstance(booking.booking_date, datetime):
                        booking_date = booking.booking_date.strftime("%d-%m-%Y %I:%M %p")
                    else:
                        booking_date = str(booking.booking_date)
                
                completion_date = ""
                if booking.completion_date:
                    if isinstance(booking.completion_date, datetime):
                        completion_date = booking.completion_date.strftime("%d-%m-%Y %I:%M %p")
                    else:
                        completion_date = str(booking.completion_date)
                
                fare_str = "N/A"
                if booking.fare:
                    fare_str = f"{CURRENCY_SYMBOL} {booking.fare:.2f}"
                
                distance_str = "N/A"
                if booking.distance_km:
                    distance_str = f"{booking.distance_km:.2f} km"
                
                details = (
                    f"Booking Details\n\n"
                    f"Booking ID: {booking.booking_id}\n"
                    f"Passenger: {passenger_name}\n"
                    f"Driver: {driver_name}\n"
                    f"Pickup Location: {booking.pickup_location or 'N/A'}\n"
                    f"Destination: {booking.destination or 'N/A'}\n"
                    f"Status: {booking.status or 'N/A'}\n"
                    f"Distance: {distance_str}\n"
                    f"Fare: {fare_str}\n"
                    f"Booking Date: {booking_date}\n"
                    f"Completion Date: {completion_date or 'N/A'}"
                )
                messagebox.showinfo("Booking Details", details)
        
        def assign_driver():
            """Assign driver to booking"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a booking to assign driver")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            booking = self.booking_ctrl.get_booking_by_id(booking_id)
            
            if not booking:
                messagebox.showerror("Error", "Booking not found!")
                return
            
            # Check if already has driver
            if booking.driver_id:
                if not messagebox.askyesno(
                    "Driver Already Assigned",
                    f"This booking already has a driver assigned.\nDo you want to change the driver?"
                ):
                    return
            
            # Get available drivers
            available_drivers = self.driver_ctrl.get_available_drivers()
            if not available_drivers:
                messagebox.showwarning("Warning", "No available drivers found!")
                return
            
            # Create dialog for driver selection
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Assign Driver - Booking #{booking_id}")
            dialog.geometry("400x300")
            dialog.configure(bg=BG_COLOR)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (dialog.winfo_screenheight() // 2) - (300 // 2)
            dialog.geometry(f"400x300+{x}+{y}")
            
            tk.Label(
                dialog,
                text=f"Assign Driver to Booking #{booking_id}",
                font=FONT_LARGE_HEADING,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY
            ).pack(pady=PADDING_LARGE)
            
            info_frame = tk.Frame(dialog, bg=BG_COLOR)
            info_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_MEDIUM)
            
            tk.Label(
                info_frame,
                text=f"Route: {booking.pickup_location} → {booking.destination}",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY,
                wraplength=350
            ).pack(pady=5)
            
            tk.Label(
                info_frame,
                text="Select Driver:",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY
            ).pack(pady=(10, 5))
            
            # Driver selection
            driver_var = tk.StringVar()
            driver_combo = ttk.Combobox(
                info_frame,
                textvariable=driver_var,
                state='readonly',
                width=30
            )
            
            # Create driver list with ID and name
            driver_list = [f"{d.driver_id} - {d.name} ({d.license_number})" for d in available_drivers]
            driver_combo['values'] = driver_list
            if driver_list:
                driver_combo.current(0)
            
            driver_combo.pack(pady=5)
            
            def save_assignment():
                if not driver_var.get():
                    messagebox.showerror("Error", "Please select a driver!")
                    return
                
                # Extract driver ID from selection
                driver_id = int(driver_var.get().split(' - ')[0])
                
                success, message = self.booking_ctrl.assign_driver(booking_id, driver_id)
                
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    refresh_bookings()
                else:
                    messagebox.showerror("Error", f"Failed to assign driver: {message}")
            
            button_frame = tk.Frame(dialog, bg=BG_COLOR)
            button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
            
            tk.Button(
                button_frame,
                text="Assign",
                font=FONT_MEDIUM,
                bg=BTN_SUCCESS,
                fg=TEXT_LIGHT,
                relief='flat',
                cursor='hand2',
                command=save_assignment,
                padx=20,
                pady=8
            ).pack(side='left', padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=FONT_MEDIUM,
                bg=BTN_DANGER,
                fg=TEXT_LIGHT,
                relief='flat',
                cursor='hand2',
                command=dialog.destroy,
                padx=20,
                pady=8
            ).pack(side='right', padx=5)
        
        def update_status():
            """Update booking status"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a booking to update status")
                return
            
            item = tree.item(selected[0])
            booking_id = item['values'][0]
            booking = self.booking_ctrl.get_booking_by_id(booking_id)
            
            if not booking:
                messagebox.showerror("Error", "Booking not found!")
                return
            
            # Create dialog for status update
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Update Status - Booking #{booking_id}")
            dialog.geometry("350x200")
            dialog.configure(bg=BG_COLOR)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
            y = (dialog.winfo_screenheight() // 2) - (200 // 2)
            dialog.geometry(f"350x200+{x}+{y}")
            
            tk.Label(
                dialog,
                text=f"Update Booking Status",
                font=FONT_LARGE,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY
            ).pack(pady=PADDING_LARGE)
            
            tk.Label(
                dialog,
                text=f"Current Status: {booking.status}",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_SECONDARY
            ).pack(pady=5)
            
            tk.Label(
                dialog,
                text="New Status:",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY
            ).pack(pady=(10, 5))
            
            status_var_dialog = tk.StringVar(value=booking.status)
            status_combo_dialog = ttk.Combobox(
                dialog,
                textvariable=status_var_dialog,
                values=BOOKING_STATUSES,
                state='readonly',
                width=20
            )
            status_combo_dialog.pack(pady=5)
            
            def save_status():
                new_status = status_var_dialog.get()
                success, message = self.booking_ctrl.update_booking_status(booking_id, new_status)
                
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    refresh_bookings()
                else:
                    messagebox.showerror("Error", f"Failed to update status: {message}")
            
            button_frame = tk.Frame(dialog, bg=BG_COLOR)
            button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
            
            tk.Button(
                button_frame,
                text="Update",
                font=FONT_MEDIUM,
                bg=BTN_SUCCESS,
                fg=TEXT_LIGHT,
                relief='flat',
                cursor='hand2',
                command=save_status,
                padx=20,
                pady=8
            ).pack(side='left', padx=5)
            
            tk.Button(
                button_frame,
                text="Cancel",
                font=FONT_MEDIUM,
                bg=BTN_DANGER,
                fg=TEXT_LIGHT,
                relief='flat',
                cursor='hand2',
                command=dialog.destroy,
                padx=20,
                pady=8
            ).pack(side='right', padx=5)
        
        # Action buttons
        view_btn = tk.Button(
            action_frame,
            text="👁️ View Details",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=view_booking,
            padx=15,
            pady=8
        )
        view_btn.pack(side='left', padx=5)
        
        assign_btn = tk.Button(
            action_frame,
            text="🚗 Assign Driver",
            font=FONT_MEDIUM,
            bg=BTN_WARNING,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=assign_driver,
            padx=15,
            pady=8
        )
        assign_btn.pack(side='left', padx=5)
        
        status_btn = tk.Button(
            action_frame,
            text="📝 Update Status",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=update_status,
            padx=15,
            pady=8
        )
        status_btn.pack(side='left', padx=5)
        
        # Initial load
        refresh_bookings()
    
    def show_payments(self):
        """Show payments list made by customers."""
        self.clear_content()

        # Header
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)

        tk.Label(
            header_frame,
            text="💰 Payments",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left')

        # Filter frame
        filter_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        filter_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_MEDIUM))

        tk.Label(
            filter_frame,
            text="Filter by Status:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left', padx=(0, PADDING_MEDIUM))

        status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=status_var,
            values=["All", "Pending", "Completed", "Failed"],
            state='readonly',
            width=15
        )
        status_combo.pack(side='left')

        # Table frame
        table_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        table_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))

        v_scroll = ttk.Scrollbar(table_frame, orient='vertical')
        v_scroll.pack(side='right', fill='y')

        h_scroll = ttk.Scrollbar(table_frame, orient='horizontal')
        h_scroll.pack(side='bottom', fill='x')

        tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Booking', 'Passenger', 'Amount', 'Method', 'Status', 'Date'),
            show='headings',
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )

        v_scroll.config(command=tree.yview)
        h_scroll.config(command=tree.xview)

        tree.heading('ID', text='Payment ID')
        tree.heading('Booking', text='Booking ID')
        tree.heading('Passenger', text='Passenger')
        tree.heading('Amount', text='Amount')
        tree.heading('Method', text='Method')
        tree.heading('Status', text='Status')
        tree.heading('Date', text='Payment Date')

        tree.column('ID', width=80, anchor='center')
        tree.column('Booking', width=80, anchor='center')
        tree.column('Passenger', width=180, anchor='w')
        tree.column('Amount', width=100, anchor='e')
        tree.column('Method', width=120, anchor='center')
        tree.column('Status', width=100, anchor='center')
        tree.column('Date', width=140, anchor='center')

        tree.pack(side='left', fill='both', expand=True)

        def refresh_payments():
            """Load and display payments based on selected status."""
            for item in tree.get_children():
                tree.delete(item)

            selected_status = status_var.get()

            # Load all payments, then filter in memory to avoid changing controller API
            payments = self.payment_ctrl.get_all_payments()

            from datetime import datetime

            for payment in payments:
                # Filter by status if needed
                if selected_status != "All" and payment.payment_status != selected_status:
                    continue

                booking = self.booking_ctrl.get_booking_by_id(payment.booking_id)
                passenger_name = "N/A"

                if booking and booking.passenger_id:
                    passenger = self.passenger_ctrl.get_passenger_by_id(booking.passenger_id)
                    if passenger and passenger.name:
                        passenger_name = passenger.name

                date_text = ""
                if payment.payment_date:
                    if isinstance(payment.payment_date, datetime):
                        date_text = payment.payment_date.strftime("%d-%m-%Y %H:%M")
                    else:
                        date_text = str(payment.payment_date)[:16]

                amount_text = payment.get_formatted_amount() if hasattr(payment, "get_formatted_amount") else f"{CURRENCY_SYMBOL} {payment.amount:.2f}"

                tree.insert(
                    '',
                    'end',
                    values=(
                        payment.payment_id,
                        payment.booking_id,
                        passenger_name,
                        amount_text,
                        payment.payment_method,
                        payment.payment_status,
                        date_text,
                    ),
                )

        # Controls on filter frame
        refresh_btn = tk.Button(
            filter_frame,
            text="🔄 Refresh",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=refresh_payments,
            padx=15,
            pady=5
        )
        refresh_btn.pack(side='right')

        status_combo.bind('<<ComboboxSelected>>', lambda e: refresh_payments())

        # Initial load
        refresh_payments()
    
    def show_settings(self):
        """Show settings interface"""
        self.clear_content()
        tk.Label(
            self.content_frame,
            text="🚧 Settings - Coming Soon",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR
        ).pack(expand=True)
    
    def show_reports(self):
        """Show reports (progress and detailed) with export option."""
        self.clear_content()

        # Header
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)

        tk.Label(
            header_frame,
            text="📑 Reports",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(side='left')

        # Controls
        controls_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        controls_frame.pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_MEDIUM))

        tk.Label(
            controls_frame,
            text="Report type:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(side='left')

        self.report_type_var = tk.StringVar(value="Progress")
        report_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.report_type_var,
            values=["Progress", "Detailed Bookings", "Detailed Payments"],
            state='readonly',
            width=20,
        )
        report_combo.pack(side='left', padx=(10, PADDING_MEDIUM))

        export_btn = tk.Button(
            controls_frame,
            text="⬇ Export CSV",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=self.export_current_report_to_csv,
        )
        export_btn.pack(side='right')

        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=self.load_current_report,
        )
        refresh_btn.pack(side='right', padx=(0, PADDING_MEDIUM))

        # Table area
        table_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        table_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_LARGE)

        v_scroll = ttk.Scrollbar(table_frame, orient='vertical')
        v_scroll.pack(side='right', fill='y')

        h_scroll = ttk.Scrollbar(table_frame, orient='horizontal')
        h_scroll.pack(side='bottom', fill='x')

        self.report_tree = ttk.Treeview(
            table_frame,
            show='headings',
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
        )
        self.report_tree.pack(side='left', fill='both', expand=True)

        v_scroll.config(command=self.report_tree.yview)
        h_scroll.config(command=self.report_tree.xview)

        # Initial load
        self.load_current_report()
        report_combo.bind('<<ComboboxSelected>>', lambda e: self.load_current_report())

    # -------------------- REPORT HELPERS -------------------- #

    def load_current_report(self):
        """Load data into the report table based on selected report type."""
        if not hasattr(self, "report_type_var"):
            return
        report_type = self.report_type_var.get()

        # Clear existing
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
        self.report_tree["columns"] = ()

        if report_type == "Progress":
            self._load_progress_report()
        elif report_type == "Detailed Bookings":
            self._load_detailed_bookings_report()
        else:
            self._load_detailed_payments_report()

    def _setup_report_columns(self, columns):
        """Configure Treeview columns."""
        self.report_tree["columns"] = [c[0] for c in columns]
        for key, title, width, anchor in columns:
            self.report_tree.heading(key, text=title)
            self.report_tree.column(key, width=width, anchor=anchor)

    def _load_progress_report(self):
        """Show high‑level KPIs."""
        columns = [
            ("metric", "Metric", 260, "w"),
            ("value", "Value", 160, "w"),
        ]
        self._setup_report_columns(columns)

        total_passengers = self.passenger_ctrl.get_total_passengers_count()
        total_drivers = self.driver_ctrl.get_total_drivers_count()
        available_drivers = self.driver_ctrl.get_available_drivers_count()
        total_vehicles = self.vehicle_ctrl.get_total_vehicles_count()
        total_bookings = self.booking_ctrl.get_total_bookings_count()
        completed_bookings = len(self.booking_ctrl.get_completed_bookings())
        pending_bookings = len(self.booking_ctrl.get_pending_bookings())
        active_bookings = len(self.booking_ctrl.get_active_bookings())
        booking_revenue = self.booking_ctrl.get_total_revenue()
        payment_count = self.payment_ctrl.get_total_payments_count()
        payment_revenue = self.payment_ctrl.get_total_revenue()

        rows = [
            ("Total Passengers", total_passengers),
            ("Total Drivers", total_drivers),
            ("Available Drivers", available_drivers),
            ("Total Vehicles", total_vehicles),
            ("Total Bookings", total_bookings),
            ("Completed Bookings", completed_bookings),
            ("Pending Bookings", pending_bookings),
            ("Active Bookings (Confirmed + In Progress)", active_bookings),
            (f"Booking Revenue ({CURRENCY_SYMBOL})", f"{booking_revenue:.2f}"),
            ("Total Payments", payment_count),
            (f"Payment Revenue ({CURRENCY_SYMBOL})", f"{payment_revenue:.2f}"),
        ]

        for metric, value in rows:
            self.report_tree.insert("", "end", values=(metric, value))

    def _load_detailed_bookings_report(self):
        """Show detailed bookings report."""
        columns = [
            ("id", "Booking ID", 80, "center"),
            ("passenger", "Passenger", 160, "w"),
            ("driver", "Driver", 160, "w"),
            ("pickup", "Pickup", 180, "w"),
            ("destination", "Destination", 180, "w"),
            ("status", "Status", 100, "center"),
            ("fare", "Fare", 90, "e"),
            ("date", "Booking Date", 140, "center"),
        ]
        self._setup_report_columns(columns)

        bookings = self.booking_ctrl.get_all_bookings()
        from datetime import datetime

        for b in bookings:
            passenger_name = "N/A"
            if b.passenger_id:
                p = self.passenger_ctrl.get_passenger_by_id(b.passenger_id)
                if p and p.name:
                    passenger_name = p.name

            driver_name = "Not Assigned"
            if b.driver_id:
                d = self.driver_ctrl.get_driver_by_id(b.driver_id)
                if d and d.name:
                    driver_name = d.name

            if b.booking_date and isinstance(b.booking_date, datetime):
                date_text = b.booking_date.strftime("%d-%m-%Y %H:%M")
            else:
                date_text = str(b.booking_date)[:16] if b.booking_date else ""

            fare_text = "N/A"
            if b.fare:
                fare_text = f"{CURRENCY_SYMBOL} {b.fare:.2f}"

            self.report_tree.insert(
                "",
                "end",
                values=(
                    b.booking_id,
                    passenger_name,
                    driver_name,
                    b.pickup_location or "",
                    b.destination or "",
                    b.status or "",
                    fare_text,
                    date_text,
                ),
            )

    def _load_detailed_payments_report(self):
        """Show detailed payments report."""
        columns = [
            ("id", "Payment ID", 80, "center"),
            ("booking", "Booking ID", 80, "center"),
            ("passenger", "Passenger", 160, "w"),
            ("amount", "Amount", 100, "e"),
            ("method", "Method", 120, "center"),
            ("status", "Status", 100, "center"),
            ("date", "Payment Date", 140, "center"),
        ]
        self._setup_report_columns(columns)

        payments = self.payment_ctrl.get_all_payments()
        from datetime import datetime

        for p in payments:
            booking = self.booking_ctrl.get_booking_by_id(p.booking_id)
            passenger_name = "N/A"
            if booking and booking.passenger_id:
                passenger = self.passenger_ctrl.get_passenger_by_id(booking.passenger_id)
                if passenger and passenger.name:
                    passenger_name = passenger.name

            if p.payment_date and isinstance(p.payment_date, datetime):
                date_text = p.payment_date.strftime("%d-%m-%Y %H:%M")
            else:
                date_text = str(p.payment_date)[:16] if p.payment_date else ""

            amount_text = (
                p.get_formatted_amount()
                if hasattr(p, "get_formatted_amount")
                else f"{CURRENCY_SYMBOL} {p.amount:.2f}"
            )

            self.report_tree.insert(
                "",
                "end",
                values=(
                    p.payment_id,
                    p.booking_id,
                    passenger_name,
                    amount_text,
                    p.payment_method,
                    p.payment_status,
                    date_text,
                ),
            )

    def export_current_report_to_csv(self):
        """Export the current report to CSV."""
        if not hasattr(self, "report_tree"):
            return

        rows = [self.report_tree.item(item, "values") for item in self.report_tree.get_children()]
        if not rows:
            messagebox.showinfo("Export CSV", "No data to export.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Export report as CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"report_{self.report_type_var.get().lower().replace(' ', '_')}.csv",
        )
        if not file_path:
            return

        import csv

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.report_tree["columns"])
                for row in rows:
                    writer.writerow(row)
            messagebox.showinfo("Export CSV", f"Report exported:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export CSV", f"Failed to export report:\n{e}")
    
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


