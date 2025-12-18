# UI/LoginPage.py
"""
Login Page - User authentication interface
"""
import tkinter as tk
from tkinter import messagebox
from Controllers.UserController import UserController
from config import (LOGIN_WINDOW_WIDTH,LOGIN_WINDOW_HEIGHT,PRIMARY_COLOR,SECONDARY_COLOR,BG_COLOR,TEXT_PRIMARY,TEXT_LIGHT,FONT_LARGE_HEADING
                    ,FONT_LARGE,FONT_MEDIUM,FONT_NORMAL_REGULAR,BTN_PRIMARY,BTN_PRIMARY_HOVER,INPUT_BG,INPUT_BORDER,PADDING_LARGE,PADDING_MEDIUM
                    ,ERROR_INVALID_CREDENTIALS,USER_TYPE_ADMIN,USER_TYPE_PASSENGER,USER_TYPE_DRIVER
)

class LoginPage:
    """
    Login interface for user authentication
    """
    def __init__(self, root):
        """
        Initialize Login Page
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.user_controller = UserController()
        self.current_user = None
        
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the login window"""
        self.root.title("Taxi Booking System - Login")
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - LOGIN_WINDOW_WIDTH) // 2
        y = (screen_height - LOGIN_WINDOW_HEIGHT) // 2
        
        self.root.geometry(f"{LOGIN_WINDOW_WIDTH}x{LOGIN_WINDOW_HEIGHT}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)
    
    def create_widgets(self):
        """Create and layout all UI components"""
        
        # Main container
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Header section with icon
        header_frame = tk.Frame(main_frame, bg=BG_COLOR)
        header_frame.pack(pady=(0, PADDING_LARGE))
        
        # Taxi icon (using emoji)
        icon_label = tk.Label(
            header_frame,
            text="🚕",
            font=("Segoe UI", 48),
            bg=BG_COLOR
        )
        icon_label.pack()
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Taxi Booking System",
            font=FONT_LARGE_HEADING,
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Please login to continue",
            font=FONT_MEDIUM,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        subtitle_label.pack()
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg=BG_COLOR)
        form_frame.pack(pady=PADDING_LARGE, fill='x')
        
        # Username field
        username_label = tk.Label(
            form_frame,
            text="Username",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        username_label.pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=FONT_LARGE,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            relief='solid',
            borderwidth=1
        )
        self.username_entry.pack(fill='x', ipady=10)
        
        # Password field
        password_label = tk.Label(
            form_frame,
            text="Password",
            font=FONT_LARGE,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        )
        password_label.pack(anchor='w', pady=(PADDING_MEDIUM, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=FONT_LARGE,
            bg=INPUT_BG,
            fg=TEXT_PRIMARY,
            show="●",
            relief='solid',
            borderwidth=1
        )
        self.password_entry.pack(fill='x', ipady=10)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
        
        # Show/Hide password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_check = tk.Checkbutton(
            form_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=FONT_NORMAL_REGULAR,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            selectcolor=BG_COLOR,
            activebackground=BG_COLOR
        )
        show_password_check.pack(anchor='w', pady=(5, 0))
        
        # Login button
        self.login_button = tk.Button(
            form_frame,
            text="LOGIN",
            font=FONT_LARGE,
            bg=BTN_PRIMARY,
            fg=TEXT_LIGHT,
            activebackground=BTN_PRIMARY_HOVER,
            activeforeground=TEXT_LIGHT,
            cursor='hand2',
            relief='flat',
            command=self.handle_login
        )
        self.login_button.pack(fill='x', ipady=12, pady=(PADDING_LARGE, 0))
        
        # Hover effects for login button
        self.login_button.bind('<Enter>', lambda e: self.login_button.config(bg=BTN_PRIMARY_HOVER))
        self.login_button.bind('<Leave>', lambda e: self.login_button.config(bg=BTN_PRIMARY))
        
        # Footer
        footer_frame = tk.Frame(main_frame, bg=BG_COLOR)
        footer_frame.pack(side='bottom', pady=(PADDING_LARGE, 0))
        
        footer_text_frame = tk.Frame(footer_frame, bg=BG_COLOR)
        footer_text_frame.pack()
        
        tk.Label(
            footer_text_frame,
            text="Don't have an account? ",
            font=FONT_NORMAL_REGULAR,
            bg=BG_COLOR,
            fg=TEXT_PRIMARY
        ).pack(side='left')
        
        register_label = tk.Label(
            footer_text_frame,
            text="Register here",
            font=FONT_NORMAL_REGULAR,
            bg=BG_COLOR,
            fg=SECONDARY_COLOR,
            cursor='hand2'
        )
        register_label.pack(side='left')
        register_label.bind('<Button-1>', lambda e: self.open_registration())
        
        # Underline on hover
        register_label.bind('<Enter>', lambda e: register_label.config(font=("Segoe UI", 10, "underline")))
        register_label.bind('<Leave>', lambda e: register_label.config(font=FONT_NORMAL_REGULAR))
        
        # Default credentials hint
        hint_frame = tk.Frame(main_frame, bg=BG_COLOR)
        hint_frame.pack(side='bottom')
        
        hint_label = tk.Label(
            hint_frame,
            text="Default Admin: username='admin', password='admin123'",
            font=("Segoe UI", 9, "italic"),
            bg=BG_COLOR,
            fg="#7F8C8D"
        )
        hint_label.pack()
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='●')
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Authenticate
        user = self.user_controller.authenticate_user(username, password)
        
        if user:
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.redirect_to_dashboard()
        else:
            messagebox.showerror("Login Failed", ERROR_INVALID_CREDENTIALS)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def redirect_to_dashboard(self):
        """Redirect user to appropriate dashboard based on user type"""
        
        # Close login window
        self.root.withdraw()
        
        # Import dashboards here to avoid circular imports
        if self.current_user.user_type == USER_TYPE_ADMIN:
            from UI.Dashboard_Admin import AdminDashboard
            dashboard_window = tk.Toplevel(self.root)
            AdminDashboard(dashboard_window, self.current_user, self.root)
            
        elif self.current_user.user_type == USER_TYPE_PASSENGER:
            from UI.Dashboard_Passenger import PassengerDashboard
            dashboard_window = tk.Toplevel(self.root)
            PassengerDashboard(dashboard_window, self.current_user, self.root)
            
        elif self.current_user.user_type == USER_TYPE_DRIVER:
            from UI.Dashboard_Driver import DriverDashboard
            dashboard_window = tk.Toplevel(self.root)
            DriverDashboard(dashboard_window, self.current_user, self.root)
    
    def open_registration(self):
        """Open registration window"""
        self.root.withdraw()
        
        from UI.RegistrationPage import RegistrationPage
        registration_window = tk.Toplevel(self.root)
        RegistrationPage(registration_window, self.root)
    
    def run(self):
        """Start the login page"""
        self.username_entry.focus()
        self.root.mainloop()


