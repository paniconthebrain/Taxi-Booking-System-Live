# UI/RegistrationPage.py
import tkinter as tk
from tkinter import messagebox

from Controllers.UserController import UserController
from Controllers.PassengerController import PassengerController
from Controllers.DriverController import DriverController

from config import (
    BG_COLOR, PRIMARY_COLOR, TEXT_PRIMARY, TEXT_LIGHT,
    FONT_LARGE_HEADING, FONT_LARGE, FONT_MEDIUM,
    INPUT_BG, BTN_PRIMARY, BTN_PRIMARY_HOVER, BTN_SECONDARY,
    USER_TYPE_PASSENGER, USER_TYPE_DRIVER,
    validate_email, validate_phone, validate_license,
    ERROR_REQUIRED_FIELD, ERROR_WEAK_PASSWORD, ERROR_PASSWORD_MISMATCH
)


class RegistrationPage:

    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window

        # controllers
        self.user_ctrl = UserController()
        self.passenger_ctrl = PassengerController()
        self.driver_ctrl = DriverController()

        # variable
        self.user_type_var = tk.StringVar(value=USER_TYPE_PASSENGER)

        self._setup_window()
        self._build_ui()

    # ------------------------------------------------------------------
    # WINDOW SETUP
    # ------------------------------------------------------------------
    def _setup_window(self):
        self.root.title("Register - Taxi Booking System")
        width, height = 500, 750
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

    # ------------------------------------------------------------------
    # UI BUILD
    # ------------------------------------------------------------------
    def _build_ui(self):
        # Canvas + scrollbar to make the page scrollable
        canvas = tk.Canvas(self.root, bg=BG_COLOR, highlightthickness=0)
        v_scroll = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        main = tk.Frame(canvas, bg=BG_COLOR)
        canvas.create_window((0, 0), window=main, anchor="nw")

        # Update scroll region when content size changes
        main.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Mouse wheel scrolling
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        # Heading
        tk.Label(main, text="Create New Account",
                 font=FONT_LARGE_HEADING, fg=PRIMARY_COLOR, bg=BG_COLOR).pack(pady=(10, 5))

        tk.Label(main, text="Register as Passenger or Driver",
                 font=FONT_MEDIUM, fg=TEXT_PRIMARY, bg=BG_COLOR).pack(pady=(0, 15))

        # Form Frame
        form = tk.Frame(main, bg=BG_COLOR)
        form.pack(fill='x', padx=20)

        # User type
        tk.Label(form, text="Register As:", font=FONT_LARGE,
                 bg=BG_COLOR, fg=TEXT_PRIMARY).pack(anchor="w")

        type_frame = tk.Frame(form, bg=BG_COLOR)
        type_frame.pack(anchor="w", pady=5)

        tk.Radiobutton(type_frame, text="Passenger", variable=self.user_type_var,
                       value=USER_TYPE_PASSENGER, font=FONT_MEDIUM,
                       bg=BG_COLOR, fg=TEXT_PRIMARY, activebackground=BG_COLOR,
                       command=self._toggle_driver_fields).pack(side="left", padx=10)

        tk.Radiobutton(type_frame, text="Driver", variable=self.user_type_var,
                       value=USER_TYPE_DRIVER, font=FONT_MEDIUM,
                       bg=BG_COLOR, fg=TEXT_PRIMARY, activebackground=BG_COLOR,
                       command=self._toggle_driver_fields).pack(side="left", padx=10)

        # Common Input Fields
        self.name_entry = self._field(form, "Full Name")
        self.email_entry = self._field(form, "Email")
        self.phone_entry = self._field(form, "Phone Number (10 digits)")

        # Driver-only fields
        self.driver_frame = tk.Frame(form, bg=BG_COLOR)
        self.license_entry = self._field(self.driver_frame, "Driver License (8-15 chars)")

        # Address
        tk.Label(form, text="Address:", font=FONT_LARGE,
                 bg=BG_COLOR, fg=TEXT_PRIMARY).pack(anchor='w')
        self.address_text = tk.Text(form, height=2, bg=INPUT_BG, font=FONT_MEDIUM, width=50)
        self.address_text.pack(fill='x', pady=5)

        # Account credentials
        self.username_entry = self._field(form, "Username")
        self.password_entry = self._field(form, "Password (min 6 chars)", show="*")
        self.conf_password_entry = self._field(form, "Confirm Password", show="*")

        # Button: Register
        self.register_btn = tk.Button(form, text="REGISTER", font=FONT_LARGE,
                                      bg=BTN_PRIMARY, fg=TEXT_LIGHT, command=self._register)
        self.register_btn.pack(fill='x', pady=20, ipady=8)

        self.register_btn.bind("<Enter>", lambda e: self.register_btn.config(bg=BTN_PRIMARY_HOVER))
        self.register_btn.bind("<Leave>", lambda e: self.register_btn.config(bg=BTN_PRIMARY))

        # Back to login
        tk.Button(form, text="Back to Login", bg=BTN_SECONDARY, fg=TEXT_PRIMARY,
                  font=FONT_MEDIUM, command=self._back).pack(fill='x', ipady=6)

        self._toggle_driver_fields()

    # ------------------------------------------------------------------
    # FIELD CREATION
    # ------------------------------------------------------------------
    def _field(self, parent, label, show=None):
        tk.Label(parent, text=label, font=FONT_LARGE,
                 bg=BG_COLOR, fg=TEXT_PRIMARY).pack(anchor='w', pady=(10, 3))
        entry = tk.Entry(parent, font=FONT_MEDIUM, bg=INPUT_BG, show=show, width=50)
        entry.pack(fill='x', ipady=4)
        return entry

    # ------------------------------------------------------------------
    # TOGGLE DRIVER FIELDS
    # ------------------------------------------------------------------
    def _toggle_driver_fields(self):
        if self.user_type_var.get() == USER_TYPE_DRIVER:
            # Show driver fields just below the address field
            self.driver_frame.pack(fill='x', after=self.address_text)
        else:
            self.driver_frame.pack_forget()

    # ------------------------------------------------------------------
    # REGISTRATION LOGIC
    # ------------------------------------------------------------------
    def _register(self):
        user_type = self.user_type_var.get()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_text.get("1.0", "end").strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        conf_pass = self.conf_password_entry.get().strip()

        # Required checks
        if not all([name, email, phone, address, username, password, conf_pass]):
            messagebox.showerror("Error", ERROR_REQUIRED_FIELD)
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return

        if not validate_phone(phone):
            messagebox.showerror("Error", "Phone must be 10 digits")
            return

        if len(password) < 6:
            messagebox.showerror("Error", ERROR_WEAK_PASSWORD)
            return

        if password != conf_pass:
            messagebox.showerror("Error", ERROR_PASSWORD_MISMATCH)
            return

        # Driver checks
        license_num = None
        if user_type == USER_TYPE_DRIVER:
            license_num = self.license_entry.get().strip()
            if not validate_license(license_num):
                messagebox.showerror("Error", "Invalid license number format")
                return

        # Create user
        success, msg, user_id = self.user_ctrl.create_user(username, password, user_type)
        if not success:
            messagebox.showerror("Error", msg)
            return

        # Create profile
        if user_type == USER_TYPE_PASSENGER:
            ok, msg, pid = self.passenger_ctrl.create_passenger(name, email, phone, address, user_id)
        else:
            ok, msg, did = self.driver_ctrl.create_driver(name, license_num, phone, email, user_id)

        if not ok:
            self.user_ctrl.delete_user(user_id)
            messagebox.showerror("Error", msg)
            return

        messagebox.showinfo("Success", "Registration completed. You can now login.")
        self._back()

    # ------------------------------------------------------------------
    # BACK TO LOGIN
    # ------------------------------------------------------------------
    def _back(self):
        self.root.destroy()
        self.login_window.deiconify()