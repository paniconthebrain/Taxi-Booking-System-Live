# UI/Dashboard_Passenger.py
"""
Passenger Dashboard - Main interface for passengers
"""

import tkinter as tk
from tkinter import messagebox
from Controllers.PassengerController import PassengerController
from Controllers.BookingController import BookingController
from Controllers.PaymentController import PaymentController
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
        self.payment_ctrl = PaymentController()
        
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
        card.pack(side='left', fill='x', expand=True, padx=8, pady=8)
        
        tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            bg=color,
            fg=TEXT_LIGHT
        ).pack(pady=(20, 5))
        
        tk.Label(
            card,
            text=label,
            font=FONT_MEDIUM,
            bg=color,
            fg=TEXT_LIGHT
        ).pack(pady=(0, 20))
    
    def show_book_ride(self):
        """Show booking interface"""
        self.clear_content()
        
        # Header
        tk.Label(
            self.content_frame,
            text="🚖 Book a Ride",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor='w')
        
        # Form container
        form_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        form_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        # Inner padding frame
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Pickup Location
        tk.Label(
            inner_frame,
            text="Pickup Location:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        pickup_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        pickup_entry.grid(row=1, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Drop-off Location
        tk.Label(
            inner_frame,
            text="Drop-off Location:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        dropoff_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        dropoff_entry.grid(row=3, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Date
        tk.Label(
            inner_frame,
            text="Pickup Date (YYYY-MM-DD):",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        date_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        date_entry.grid(row=5, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Set today's date as placeholder
        from datetime import datetime
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Time
        tk.Label(
            inner_frame,
            text="Pickup Time (HH:MM):",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=6, column=0, sticky='w', pady=(0, 5))
        
        time_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        time_entry.grid(row=7, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Set current time as placeholder
        time_entry.insert(0, datetime.now().strftime("%H:%M"))
        
        # Distance (Optional)
        tk.Label(
            inner_frame,
            text="Distance (km) - Optional:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=8, column=0, sticky='w', pady=(0, 5))
        
        distance_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        distance_entry.grid(row=9, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Fare label
        fare_label = tk.Label(
            inner_frame,
            text="",
            font=FONT_MEDIUM,
            bg='white',
            fg=SUCCESS_COLOR
        )
        fare_label.grid(row=10, column=0, sticky='w', pady=(0, 15))
    
        # Calculate fare on distance change
        def calculate_fare_estimate(*args):
            distance_text = distance_entry.get().strip()
            if distance_text:
                try:
                    distance = float(distance_text)
                    if distance > 0:
                        estimated_fare = calculate_fare(distance)
                        fare_label.config(text=f"💰 Estimated Fare: {CURRENCY_SYMBOL} {estimated_fare:.2f}")
                    else:
                        fare_label.config(text="")
                except ValueError:
                    fare_label.config(text="")
            else:
                fare_label.config(text="")
        
        distance_entry.bind('<KeyRelease>', calculate_fare_estimate)
    
    # Configure grid
        inner_frame.columnconfigure(0, weight=1)
    
    # Button frame
        button_frame = tk.Frame(form_frame, bg='white')
        button_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        def submit_booking():
            """Handle booking submission"""
            pickup = pickup_entry.get().strip()
            dropoff = dropoff_entry.get().strip()
            date_text = date_entry.get().strip()
            time_text = time_entry.get().strip()
            distance_text = distance_entry.get().strip()
            
            # Validation
            if not pickup or not dropoff:
                messagebox.showerror("Error", "Please enter pickup and drop-off locations!")
                return
            
            if not date_text or not time_text:
                messagebox.showerror("Error", "Please enter date and time!")
                return
            
            # Validate distance if provided
            distance_km = None
            if distance_text:
                try:
                    distance_km = float(distance_text)
                    if distance_km <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", "Distance must be a positive number!")
                    return
            
            # Create booking
            success, message, booking_id = self.booking_ctrl.create_booking(
                passenger_id=self.passenger.passenger_id,
                pickup_location=pickup,
                destination=dropoff,
                distance_km=distance_km
            )
            
            if success:
                fare_info = ""
                if distance_km:
                    fare = calculate_fare(distance_km)
                    fare_info = f"\nEstimated Fare: {CURRENCY_SYMBOL} {fare:.2f}"
                
                messagebox.showinfo(
                    "Success",
                    f"Booking created successfully!\n\n"
                    f"Booking ID: #{booking_id}\n"
                    f"From: {pickup}\n"
                    f"To: {dropoff}\n"
                    f"Date: {date_text}\n"
                    f"Time: {time_text}\n"
                    f"Status: Pending{fare_info}"
                )
                
                # Clear form
                pickup_entry.delete(0, tk.END)
                dropoff_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
                time_entry.delete(0, tk.END)
                time_entry.insert(0, datetime.now().strftime("%H:%M"))
                distance_entry.delete(0, tk.END)
                fare_label.config(text="")
            else:
                messagebox.showerror("Error", f"Failed to create booking: {message}")
        
        # Buttons
        tk.Button(
            button_frame,
            text="🚖 Book Ride",
            font=FONT_LARGE,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            cursor='hand2',
            relief='flat',
            command=submit_booking,
            padx=30,
            pady=10
        ).pack(side='left', padx=10)
        
        def clear_form():
            """Clear all form fields"""
            pickup_entry.delete(0, tk.END)
            dropoff_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            time_entry.delete(0, tk.END)
            time_entry.insert(0, datetime.now().strftime("%H:%M"))
            distance_entry.delete(0, tk.END)
            fare_label.config(text="")
        
        tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=FONT_LARGE,
            bg=BTN_SECONDARY,
            fg=TEXT_LIGHT,
            cursor='hand2',
            relief='flat',
            command=clear_form,
            padx=30,
            pady=10
        ).pack(side='left', padx=10)

    
    def show_my_bookings(self):
        """Show user's bookings"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        header_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        tk.Label(
            header_frame,
            text="My Bookings",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left')
        
        # Refresh button
        tk.Button(
            header_frame,
            text="🔄 Refresh",
            font=FONT_MEDIUM,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            cursor='hand2',
            relief='flat',
            command=self.show_my_bookings
        ).pack(side='right')
        
        # Check passenger
        if not self.passenger:
            tk.Label(
                self.content_frame,
                    text="⚠️ No passenger profile found",
                    font=FONT_LARGE,
                    bg=BG_COLOR,
                    fg=TEXT_PRIMARY
                ).pack(expand=True)
            return
        
        # Get bookings
        bookings = self.booking_ctrl.get_bookings_by_passenger(self.passenger.passenger_id)
        
        if not bookings:
            # Empty state
            empty_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
            empty_frame.pack(expand=True)
            
            tk.Label(
                empty_frame,
                text="📋",
                font=("Segoe UI", 72),
                bg=BG_COLOR
            ).pack()
            
            tk.Label(
                empty_frame,
                text="No Bookings Yet",
            font=FONT_LARGE_HEADING,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY
            ).pack(pady=10)
            
            tk.Label(
                empty_frame,
                text="Book your first ride to get started!",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_PRIMARY
            ).pack()
            
            return
        
        # Bookings list
        list_frame = tk.Frame(self.content_frame, bg=BG_COLOR)
        list_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        # Canvas for scrolling
        canvas = tk.Canvas(list_frame, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display bookings
        for booking in bookings:
            self.create_booking_card(scrollable_frame, booking)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))


    def create_booking_card(self, parent, booking):
        """Create a booking card"""
        # Card
        card = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        card.pack(fill='x', pady=10, padx=5)
        
        # Status bar
        status_color = booking.get_status_color()
        tk.Frame(card, bg=status_color, height=5).pack(fill='x')
        
        # Content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header
        header = tk.Frame(content, bg='white')
        header.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            header,
            text=f"Booking #{booking.booking_id}",
            font=("Segoe UI", 12, "bold"),
            bg='white',
            fg=TEXT_PRIMARY
        ).pack(side='left')
        
        tk.Label(
            header,
            text=booking.status,
            font=("Segoe UI", 11, "bold"),
            bg=status_color,
            fg=TEXT_LIGHT,
            padx=15,
            pady=5
        ).pack(side='right')
        
        # Route
        route_frame = tk.Frame(content, bg='white')
        route_frame.pack(fill='x', pady=5)
        
        tk.Label(
            route_frame,
            text="📍 From:",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg=TEXT_PRIMARY
        ).pack(anchor='w')
        
        tk.Label(
            route_frame,
            text=booking.pickup_location,
            font=FONT_MEDIUM,
            bg='white',
            fg=TEXT_PRIMARY,
            wraplength=500
        ).pack(anchor='w', padx=20)
        
        tk.Label(
            route_frame,
            text="📍 To:",
            font=("Segoe UI", 11, "bold"),
            bg='white',
            fg=TEXT_PRIMARY
        ).pack(anchor='w', pady=(5, 0))
        
        tk.Label(
            route_frame,
            text=booking.destination,
            font=FONT_MEDIUM,
            bg='white',
            fg=TEXT_PRIMARY,
            wraplength=500
        ).pack(anchor='w', padx=20)
        
        # Details
        details = tk.Frame(content, bg='white')
        details.pack(fill='x', pady=(10, 0))
        
        if booking.booking_date:
            tk.Label(
                details,
                text=f"🕐 {booking.booking_date.strftime('%d %b %Y, %I:%M %p')}",
                font=FONT_MEDIUM,
                bg='white',
                fg=TEXT_PRIMARY
            ).pack(side='left')
        
        if booking.distance_km:
            tk.Label(
                details,
                text=f"📏 {booking.get_formatted_distance()}",
                font=FONT_MEDIUM,
                bg='white',
                fg=TEXT_PRIMARY
            ).pack(side='left', padx=20)
        
        if booking.fare:
            tk.Label(
                details,
                text=f"💰 {booking.get_formatted_fare()}",
                font=("Segoe UI", 11, "bold"),
                bg='white',
                fg=SUCCESS_COLOR
            ).pack(side='left')
        
        if booking.driver_id:
            tk.Label(
                content,
                text="🚗 Driver Assigned",
                font=FONT_MEDIUM,
                bg='white',
                fg=SUCCESS_COLOR
            ).pack(anchor='w', pady=(10, 0))
        
        # Actions frame (payment / cancel)
        actions_frame = tk.Frame(content, bg='white')
        actions_frame.pack(fill='x', pady=(15, 0))

        # Payment button: available when fare exists and booking is confirmed/completed
        payment = self.payment_ctrl.get_payment_by_booking(booking.booking_id)
        can_pay = booking.fare is not None and (booking.is_confirmed() or booking.is_completed())

        if payment and payment.is_completed():
            tk.Label(
                actions_frame,
                text=f"Payment: {payment.get_formatted_amount()} (Completed)",
                font=FONT_MEDIUM,
                bg='white',
                fg=SUCCESS_COLOR
            ).pack(side='left')
        elif can_pay:
            tk.Button(
                actions_frame,
                text="💳 Make Payment",
                font=FONT_MEDIUM,
                bg=BTN_SUCCESS,
                fg=TEXT_LIGHT,
                cursor='hand2',
                relief='flat',
                command=lambda b=booking: self.make_payment(b)
            ).pack(side='left')

        # Cancel button – only while booking is still pending (before confirmation/driver assignment)
        if booking.is_pending():
            tk.Button(
                actions_frame,
                text="❌ Cancel Booking",
                font=FONT_MEDIUM,
                bg=BTN_DANGER,
                fg=TEXT_LIGHT,
                cursor='hand2',
                relief='flat',
                command=lambda b=booking: self.cancel_booking(b)
            ).pack(side='right')


    def cancel_booking(self, booking):
        """Cancel a booking"""
        if messagebox.askyesno("Confirm", f"Cancel Booking #{booking.booking_id}?"):
            success, message = self.booking_ctrl.cancel_booking(booking.booking_id)
            
            if success:
                messagebox.showinfo("Success", "Booking cancelled!")
                self.show_my_bookings()
            else:
                messagebox.showerror("Error", f"Failed to cancel: {message}")

    def make_payment(self, booking):
        """Create a payment for a confirmed/completed booking"""
        from config import PAYMENT_METHODS, PAYMENT_COMPLETED

        if not booking.fare:
            messagebox.showerror("Payment", "Fare not available for this booking.")
            return

        existing = self.payment_ctrl.get_payment_by_booking(booking.booking_id)
        if existing and existing.is_completed():
            messagebox.showinfo("Payment", "Payment already completed for this booking.")
            return

        # Simple dialog for payment method selection
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Make Payment - Booking #{booking.booking_id}")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text=f"Amount to Pay: {booking.get_formatted_fare()}",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(padx=20, pady=(20, 10), fill='x')

        tk.Label(
            dialog,
            text="Select Payment Method:",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(padx=20, anchor='w')

        method_var = tk.StringVar(value=PAYMENT_METHODS[0])
        method_menu = tk.OptionMenu(dialog, method_var, *PAYMENT_METHODS)
        method_menu.configure(font=FONT_MEDIUM, bg=BG_LIGHT)
        method_menu.pack(padx=20, pady=10, fill='x')

        btn_frame = tk.Frame(dialog, bg=BG_COLOR)
        btn_frame.pack(padx=20, pady=(10, 20), fill='x')

        def confirm_payment():
            method = method_var.get()
            success, msg, payment_id = self.payment_ctrl.create_payment(
                booking.booking_id,
                booking.fare,
                method,
                payment_status=PAYMENT_COMPLETED
            )
            if success:
                messagebox.showinfo(
                    "Payment Successful",
                    f"Payment completed.\nPayment ID: {payment_id}\nAmount: {booking.get_formatted_fare()}\nMethod: {method}"
                )
                dialog.destroy()
                self.show_my_bookings()
            else:
                messagebox.showerror("Payment Failed", msg or "Unable to process payment.")

        tk.Button(
            btn_frame,
            text="Pay Now",
            font=FONT_MEDIUM,
            bg=BTN_SUCCESS,
            fg=TEXT_LIGHT,
            relief='flat',
            cursor='hand2',
            command=confirm_payment
        ).pack(side='left', padx=5)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=FONT_MEDIUM,
            bg=BTN_SECONDARY,
            fg=TEXT_PRIMARY,
            relief='flat',
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
    
    def show_profile(self):
        """Show user profile"""
        self.clear_content()
        
        # Header
        tk.Label(
            self.content_frame,
            text="👤 My Profile",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(pady=PADDING_LARGE, padx=PADDING_LARGE, anchor='w')
        
        if not self.passenger:
            tk.Label(
                self.content_frame,
                text="Profile not found. Please contact support.",
                font=FONT_MEDIUM,
                bg=BG_COLOR,
                fg=TEXT_SECONDARY
            ).pack(pady=PADDING_LARGE)
            return
        
        # Profile container
        profile_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        profile_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_LARGE))
        
        # Inner padding frame
        inner_frame = tk.Frame(profile_frame, bg='white')
        inner_frame.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Username (from user object - read-only)
        tk.Label(
            inner_frame,
            text="Username:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        username_label = tk.Label(
            inner_frame,
            text=self.user.username,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1,
            anchor='w'
        )
        username_label.grid(row=1, column=0, sticky='ew', pady=(0, 15), ipady=8, ipadx=10)
        
        # Name
        tk.Label(
            inner_frame,
            text="Full Name:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        name_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        name_entry.insert(0, self.passenger.name or "")
        name_entry.grid(row=3, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Email
        tk.Label(
            inner_frame,
            text="Email:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        email_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        email_entry.insert(0, self.passenger.email or "")
        email_entry.grid(row=5, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Phone
        tk.Label(
            inner_frame,
            text="Phone:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=6, column=0, sticky='w', pady=(0, 5))
        
        phone_entry = tk.Entry(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        phone_entry.insert(0, self.passenger.phone or "")
        phone_entry.grid(row=7, column=0, sticky='ew', pady=(0, 15), ipady=8)
        
        # Address
        tk.Label(
            inner_frame,
            text="Address:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=8, column=0, sticky='w', pady=(0, 5))
        
        address_text = tk.Text(
            inner_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1,
            height=3,
            wrap='word'
        )
        address_text.insert('1.0', self.passenger.address or "")
        address_text.grid(row=9, column=0, sticky='ew', pady=(0, 15))
        
        # Created At (read-only)
        from datetime import datetime
        created_date = ""
        if self.passenger.created_at:
            if isinstance(self.passenger.created_at, datetime):
                created_date = self.passenger.created_at.strftime("%d-%m-%Y %I:%M %p")
            else:
                created_date = str(self.passenger.created_at)
        
        tk.Label(
            inner_frame,
            text="Member Since:",
            font=FONT_LARGE,
            bg='white',
            fg=TEXT_PRIMARY
        ).grid(row=10, column=0, sticky='w', pady=(0, 5))
        
        created_label = tk.Label(
            inner_frame,
            text=created_date or "N/A",
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1,
            anchor='w'
        )
        created_label.grid(row=11, column=0, sticky='ew', pady=(0, 15), ipady=8, ipadx=10)
        
        # Configure grid
        inner_frame.columnconfigure(0, weight=1)
        
        # Button frame
        button_frame = tk.Frame(profile_frame, bg='white')
        button_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        def update_profile():
            """Handle profile update"""
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_text.get('1.0', 'end-1c').strip()
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Name is required!")
                return
            
            if not email:
                messagebox.showerror("Error", "Email is required!")
                return
            
            if not phone:
                messagebox.showerror("Error", "Phone is required!")
                return
            
            # Update profile
            success, message = self.passenger_ctrl.update_passenger(
                passenger_id=self.passenger.passenger_id,
                name=name,
                email=email,
                phone=phone,
                address=address
            )
            
            if success:
                messagebox.showinfo("Success", "Profile updated successfully!")
                # Refresh passenger data
                self.passenger = self.passenger_ctrl.get_passenger_by_user_id(self.user.user_id)
                # Update welcome text in sidebar if needed
                # You might want to refresh the sidebar here
            else:
                messagebox.showerror("Error", f"Failed to update profile: {message}")
        
        # Update button
        tk.Button(
            button_frame,
            text="💾 Update Profile",
            font=FONT_LARGE,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            cursor='hand2',
            relief='flat',
            command=update_profile,
            padx=30,
            pady=10
        ).pack(side='left', padx=10)
    
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