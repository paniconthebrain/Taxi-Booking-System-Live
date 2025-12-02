import tkinter as tk
from tkinter import ttk, messagebox
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
            self.create_stat_card(stats_frame, "💰 Total Earnings", f"{CURRENCY_SYMBOL} {total_earnings:.2f}", "#E74C3C")
            
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
        """Show driver's trips in a simple grid with basic actions"""
        self.clear_content()

        if not self.driver:
            tk.Label(
                self.content_frame,
                text="Driver profile not found. Please contact admin.",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY,
            ).pack(pady=PADDING_LARGE)
            return

        # Header
        tk.Label(
            self.content_frame,
            text="My Trips",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor="w")

        # Filter frame
        filter_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        filter_frame.pack(fill="x", padx=PADDING_LARGE, pady=(0, PADDING_MEDIUM))

        tk.Label(
            filter_frame,
            text="Status:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(side="left")

        status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=status_var,
            values=["All"] + BOOKING_STATUSES,
            state="readonly",
            width=18,
        )
        status_combo.pack(side="left", padx=(10, 0))

        # Table frame
        table_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        table_frame.pack(
            fill="both", expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE)
        )

        v_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        v_scroll.pack(side="right", fill="y")

        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Pickup", "Destination", "Status", "Fare", "Date"),
            show="headings",
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
        )
        v_scroll.config(command=tree.yview)
        h_scroll.config(command=tree.xview)

        tree.heading("ID", text="ID")
        tree.heading("Pickup", text="Pickup")
        tree.heading("Destination", text="Destination")
        tree.heading("Status", text="Status")
        tree.heading("Fare", text="Fare")
        tree.heading("Date", text="Date")

        tree.column("ID", width=50, anchor="center")
        tree.column("Pickup", width=160, anchor="w")
        tree.column("Destination", width=160, anchor="w")
        tree.column("Status", width=100, anchor="center")
        tree.column("Fare", width=90, anchor="center")
        tree.column("Date", width=140, anchor="center")

        tree.pack(side="left", fill="both", expand=True)

        def load_trips():
            """Refresh trip list based on status filter"""
            status_filter = status_var.get()
            bookings = self.booking_ctrl.get_bookings_by_driver(self.driver.driver_id)

            if status_filter != "All":
                bookings = [b for b in bookings if b.status == status_filter]

            for item in tree.get_children():
                tree.delete(item)

            from datetime import datetime

            for b in bookings:
                date_text = ""
                if b.booking_date:
                    if isinstance(b.booking_date, datetime):
                        date_text = b.booking_date.strftime("%d-%m-%Y %H:%M")
                    else:
                        date_text = str(b.booking_date)[:16]

                fare_text = b.get_formatted_fare() if hasattr(b, "get_formatted_fare") else (
                    f"{CURRENCY_SYMBOL} {b.fare:.2f}" if b.fare else "N/A"
                )

                tree.insert(
                    "",
                    "end",
                    values=(
                        b.booking_id,
                        b.pickup_location or "N/A",
                        b.destination or "N/A",
                        b.status or "N/A",
                        fare_text,
                        date_text,
                    ),
                )

        status_combo.bind("<<ComboboxSelected>>", lambda e: load_trips())

        # Action buttons
        action_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        action_frame.pack(fill="x", padx=PADDING_LARGE, pady=(0, PADDING_LARGE))

        def get_selected_booking_id():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Trip", "Please select a trip first.")
                return None
            item = tree.item(selected[0])
            return item["values"][0]

        def view_trip():
            booking_id = get_selected_booking_id()
            if not booking_id:
                return
            booking = self.booking_ctrl.get_booking_by_id(booking_id)
            if not booking:
                messagebox.showerror("Error", "Booking not found")
                return

            from datetime import datetime

            booking_date = (
                booking.booking_date.strftime("%d-%m-%Y %I:%M %p")
                if hasattr(booking.booking_date, "strftime")
                else str(booking.booking_date)
            )

            details = (
                f"Booking ID: {booking.booking_id}\n"
                f"Pickup: {booking.pickup_location}\n"
                f"Destination: {booking.destination}\n"
                f"Status: {booking.status}\n"
                f"Fare: {booking.get_formatted_fare() if hasattr(booking,'get_formatted_fare') else booking.fare}\n"
                f"Date: {booking_date}"
            )
            messagebox.showinfo("Trip Details", details)

        def update_status(new_status):
            booking_id = get_selected_booking_id()
            if not booking_id:
                return
            success, msg = self.booking_ctrl.update_booking_status(booking_id, new_status)
            if success:
                messagebox.showinfo("Success", msg)
                load_trips()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            action_frame,
            text="View Details",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=view_trip,
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Mark In Progress",
            font=FONT_MEDIUM,
            bg=BTN_WARNING,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: update_status(BOOKING_STATUS_IN_PROGRESS),
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Mark Completed",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: update_status(BOOKING_STATUS_COMPLETED),
        ).pack(side="left", padx=5)

        # Initial load
        load_trips()
    
    def show_my_vehicle(self):
        """Show vehicle information"""
        self.clear_content()

        if not self.driver:
            tk.Label(
                self.content_frame,
                text="Driver profile not found. Please contact admin.",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY,
            ).pack(pady=PADDING_LARGE)
            return

        tk.Label(
            self.content_frame,
            text="My Vehicle",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor="w")

        vehicle = self.vehicle_ctrl.get_vehicle_by_driver(self.driver.driver_id)
        if not vehicle:
            tk.Label(
                self.content_frame,
                text="No vehicle assigned to you yet.",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY,
            ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor="w")
            return

        frame = tk.Frame(self.content_frame, bg=BG_LIGHT, relief="solid", borderwidth=1)
        frame.pack(fill="x", padx=PADDING_LARGE, pady=PADDING_LARGE)

        def row(label, value):
            r = tk.Frame(frame, bg=BG_LIGHT)
            r.pack(fill="x", pady=5, padx=10)
            tk.Label(r, text=label, font=FONT_MEDIUM, bg=BG_LIGHT, fg=TEXT_PRIMARY).pack(
                side="left"
            )
            tk.Label(
                r,
                text=value or "N/A",
                font=FONT_MEDIUM,
                bg=BG_LIGHT,
                fg=TEXT_PRIMARY,
            ).pack(side="left", padx=10)

        row("Model:", vehicle.model)
        row("License Plate:", vehicle.license_plate)
        row("Type:", vehicle.vehicle_type)
        row("Color:", vehicle.color)
        row("Year:", str(vehicle.year) if vehicle.year else "N/A")
    
    def show_availability(self):
        """Show availability management"""
        self.clear_content()

        if not self.driver:
            tk.Label(
                self.content_frame,
                text="Driver profile not found. Please contact admin.",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY,
            ).pack(pady=PADDING_LARGE)
            return

        tk.Label(
            self.content_frame,
            text="Availability",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor="w")

        info = tk.Label(
            self.content_frame,
            text=f"Current status: {self.driver.availability}",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        )
        info.pack(pady=(0, PADDING_LARGE), padx=PADDING_LARGE, anchor="w")

        status_var = tk.StringVar(value=self.driver.availability)

        def set_status(new_status):
            if self.driver_ctrl.update_driver_availability(self.driver.driver_id, new_status):
                self.driver.availability = new_status
                status_var.set(new_status)
                info.config(text=f"Current status: {new_status}")
                messagebox.showinfo("Success", f"Status updated to {new_status}")
            else:
                messagebox.showerror("Error", "Failed to update availability")

        btn_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        btn_frame.pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor="w")

        tk.Button(
            btn_frame,
            text="Available",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: set_status(DRIVER_AVAILABLE),
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Busy",
            font=FONT_MEDIUM,
            bg=BTN_WARNING,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: set_status(DRIVER_BUSY),
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Offline",
            font=FONT_MEDIUM,
            bg=BTN_DANGER,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=lambda: set_status(DRIVER_OFFLINE),
        ).pack(side="left", padx=5)
    
    def show_profile(self):
        """Show driver profile"""
        self.clear_content()

        if not self.driver:
            tk.Label(
                self.content_frame,
                text="Driver profile not found. Please contact admin.",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY,
            ).pack(pady=PADDING_LARGE)
            return

        tk.Label(
            self.content_frame,
            text="My Profile",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor="w")

        form = tk.Frame(self.content_frame, bg=BG_LIGHT, relief="solid", borderwidth=1)
        form.pack(fill="x", padx=PADDING_LARGE, pady=PADDING_LARGE)

        def add_field(row, label, value, editable=True):
            tk.Label(
                form,
                text=label,
                font=FONT_MEDIUM,
                bg=BG_LIGHT,
                fg=TEXT_PRIMARY,
            ).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            if editable:
                entry = tk.Entry(form, font=FONT_MEDIUM, bg=INPUT_BG)
                entry.insert(0, value or "")
                entry.grid(row=row, column=1, sticky="ew", padx=10, pady=5, ipady=4)
                return entry
            else:
                tk.Label(
                    form,
                    text=value or "N/A",
                    font=FONT_MEDIUM,
                    bg=BG_LIGHT,
                    fg=TEXT_PRIMARY,
                ).grid(row=row, column=1, sticky="w", padx=10, pady=5)
                return None

        form.columnconfigure(1, weight=1)

        name_entry = add_field(0, "Name:", self.driver.name)
        email_entry = add_field(1, "Email:", self.driver.email)
        phone_entry = add_field(2, "Phone:", self.driver.phone)
        add_field(3, "License Number:", self.driver.license_number, editable=False)

        def save_profile():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()

            if not all([name, email, phone]):
                messagebox.showerror("Error", "Name, Email and Phone are required.")
                return

            success, msg = self.driver_ctrl.update_driver(
                self.driver.driver_id,
                name=name,
                email=email,
                phone=phone,
            )
            if success:
                messagebox.showinfo("Success", "Profile updated successfully.")
                # Refresh local driver data
                self.driver = self.driver_ctrl.get_driver_by_id(self.driver.driver_id)
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            self.content_frame,
            text="Save Profile",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            relief="flat",
            cursor="hand2",
            command=save_profile,
        ).pack(pady=(0, PADDING_LARGE), padx=PADDING_LARGE, anchor="e")
    
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