# UI/RegistrationPage.py
"""
Registration Page - New user registration interface
"""

import tkinter as tk
from tkinter import messagebox
from Controllers.UserController import UserController
from Controllers.PassengerController import PassengerController
from Controllers.DriverController import DriverController
from config import (
    LOGIN_WINDOW_WIDTH,
    LOGIN_WINDOW_HEIGHT,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    BG_COLOR,
    TEXT_PRIMARY,
    TEXT_LIGHT,
    FONT_LARGE_HEADING,
    FONT_LARGE,
    FONT_MEDIUM,
    FONT_NORMAL_REGULAR,
    BTN_PRIMARY,
    BTN_PRIMARY_HOVER,
    BTN_SECONDARY,
    INPUT_BG,
    PADDING_LARGE,
    PADDING_MEDIUM,
    USER_TYPE_PASSENGER,
    USER_TYPE_DRIVER,
    validate_email,
    validate_phone,
    validate_license,
    ERROR_REQUIRED_FIELD,
    ERROR_WEAK_PASSWORD,
    ERROR_PASSWORD_MISMATCH
)


class RegistrationPage:
    """
    Registration interface for new users (Passengers and Drivers)
    """
    
    def __init__(self, root, login_window):
        """
        Initialize Registration Page
        
        Args:
            root: Registration window
            login_window: Reference to login window
        """
        self.root = root
        self.login_window = login_window
        
        # Controllers
        self.user_ctrl = UserController()
        self.passenger_ctrl = PassengerController()
        self.driver_ctrl = DriverController()
        
        # Variables
        self.user_type_var = tk.StringVar(value=USER_TYPE_PASSENGER)
        
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the registration window"""
        self.root.title("Taxi Booking System - Register")
        
        # Center the window (slightly larger than login)
        window_width = 500
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
    
    def create_widgets(self):
        """Create and layout all UI components"""
        
        # Main container with scrollbar
        main_canvas = tk.Canvas(self.root, bg=BG_COLOR, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
        header_frame.pack(pady=(20, PADDING_LARGE), padx=40)
        
        tk.Label(
            header_frame,
            text="🚕",
            font=("Segoe UI", 36),
            bg=BG_COLOR
        ).pack()
        
        tk.Label(
            header_frame,
            text="Create New Account",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        ).pack(pady=(10, 5))
        
        tk.Label(
            header_frame,
            text="Register as Passenger or Driver",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack()
        
        # Form container
        form_frame = tk.Frame(scrollable_frame, bg=BG_COLOR)
        form_frame.pack(padx=40, pady=PADDING_MEDIUM, fill='x')
        
        # User Type Selection
        tk.Label(
            form_frame,
            text="Register As:",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(anchor='w', pady=(0, 5))
        
        type_frame = tk.Frame(form_frame, bg=BG_COLOR)
        type_frame.pack(fill='x', pady=(0, PADDING_MEDIUM))
        
        tk.Radiobutton(
            type_frame,
            text="🙋 Passenger",
            variable=self.user_type_var,
            value=USER_TYPE_PASSENGER,
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            selectcolor=BG_COLOR,
            activebackground=BG_COLOR,
            command=self.on_user_type_change
        ).pack(side='left', padx=(0, 20))
        
        tk.Radiobutton(
            type_frame,
            text="🚗 Driver",
            variable=self.user_type_var,
            value=USER_TYPE_DRIVER,
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            selectcolor=BG_COLOR,
            activebackground=BG_COLOR,
            command=self.on_user_type_change
        ).pack(side='left')
        
        # Common fields
        self.create_field(form_frame, "Full Name:", "name_entry")
        self.create_field(form_frame, "Email:", "email_entry")
        self.create_field(form_frame, "Phone (10 digits):", "phone_entry")
        
        # Address field (larger)
        tk.Label(
            form_frame,
            text="Address:",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(anchor='w', pady=(PADDING_MEDIUM, 5))
        
        self.address_text = tk.Text(
            form_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1,
            height=3
        )
        self.address_text.pack(fill='x')
        
        # Driver-specific fields (initially hidden)
        self.driver_frame = tk.Frame(form_frame, bg=BG_COLOR)
        
        tk.Label(
            self.driver_frame,
            text="License Number (8-15 chars):",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(anchor='w', pady=(PADDING_MEDIUM, 5))
        
        self.license_entry = tk.Entry(
            self.driver_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        self.license_entry.pack(fill='x', ipady=8)
        
        # Login credentials
        tk.Label(
            form_frame,
            text="Username:",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(anchor='w', pady=(PADDING_MEDIUM, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        self.username_entry.pack(fill='x', ipady=8)
        
        self.create_field(form_frame, "Password (min 6 chars):", "password_entry", show="●")
        self.create_field(form_frame, "Confirm Password:", "confirm_password_entry", show="●")
        
        # Register button
        self.register_button = tk.Button(
            form_frame,
            text="REGISTER",
            font=FONT_LARGE,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            activebackground=BTN_PRIMARY_HOVER,
            activeforeground=TEXT_LIGHT,
            cursor='hand2',
            relief='flat',
            command=self.handle_registration
        )
        self.register_button.pack(fill='x', ipady=12, pady=(PADDING_LARGE, PADDING_MEDIUM))
        
        # Hover effects
        self.register_button.bind('<Enter>', lambda e: self.register_button.config(bg=BTN_PRIMARY_HOVER))
        self.register_button.bind('<Leave>', lambda e: self.register_button.config(bg=BTN_PRIMARY))
        
        # Back to login button
        back_button = tk.Button(
            form_frame,
            text="← Back to Login",
            font=FONT_MEDIUM,
            bg=BTN_SECONDARY,
            fg=TEXT_PRIMARY,
            cursor='hand2',
            relief='flat',
            command=self.back_to_login
        )
        back_button.pack(fill='x', ipady=8)
        
        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        main_canvas.bind_all("<MouseWheel>", lambda e: main_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def create_field(self, parent, label_text, entry_name, show=None):
        """Helper to create labeled entry fields"""
        tk.Label(
            parent,
            text=label_text,
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(anchor='w', pady=(PADDING_MEDIUM, 5))
        
        entry = tk.Entry(
            parent,
            font=FONT_MEDIUM,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1,
            show=show
        )
        entry.pack(fill='x', ipady=8)
        setattr(self, entry_name, entry)
    
    def on_user_type_change(self):
        """Show/hide driver-specific fields based on user type"""
        if self.user_type_var.get() == USER_TYPE_DRIVER:
            self.driver_frame.pack(fill='x', pady=(0, PADDING_MEDIUM))
        else:
            self.driver_frame.pack_forget()
    
    def handle_registration(self):
        """Handle registration form submission"""
        
        # Get all values
        user_type = self.user_type_var.get()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Validation
        if not all([name, email, phone, address, username, password, confirm_password]):
            messagebox.showerror("Error", ERROR_REQUIRED_FIELD)
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return
        
        if not validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number! Must be 10 digits.")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", ERROR_WEAK_PASSWORD)
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", ERROR_PASSWORD_MISMATCH)
            return
        
        # Driver-specific validation
        if user_type == USER_TYPE_DRIVER:
            license_number = self.license_entry.get().strip()
            if not license_number:
                messagebox.showerror("Error", "License number is required for drivers!")
                return
            if not validate_license(license_number):
                messagebox.showerror("Error", "Invalid license number format! (8-15 alphanumeric characters)")
                return
        
        # Create user account
        success, message, user_id = self.user_ctrl.create_user(username, password, user_type)
        
        if not success:
            messagebox.showerror("Registration Failed", message)
            return
        
        # Create passenger or driver profile
        if user_type == USER_TYPE_PASSENGER:
            success, message, profile_id = self.passenger_ctrl.create_passenger(
                name, email, phone, address, user_id
            )
        else:  # Driver
            success, message, profile_id = self.driver_ctrl.create_driver(
                name, license_number, phone, email, user_id
            )
        
        if success:
            messagebox.showinfo(
                "Success",
                f"Registration successful!\n\nUsername: {username}\nYou can now login."
            )
            self.back_to_login()
        else:
            # Rollback: delete user if profile creation failed
            self.user_ctrl.delete_user(user_id)
            messagebox.showerror("Registration Failed", f"Profile creation failed: {message}")
    
    def back_to_login(self):
        """Close registration and show login window"""
        self.root.destroy()
        self.login_window.deiconify()


# Test the registration page
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    reg_window = tk.Toplevel()
    app = RegistrationPage(reg_window, root)
    reg_window.mainloop()