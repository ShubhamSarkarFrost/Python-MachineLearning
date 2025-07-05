import tkinter as tk
from tkinter import messagebox, ttk
import bcrypt


DEMO_PASSWORD = b"thisismypassword"
HASHED_DEMO_PASSWORD = bcrypt.hashpw(DEMO_PASSWORD, bcrypt.gensalt())
print(f"Pre-hashed password for demonstration: {HASHED_DEMO_PASSWORD.decode('utf-8')}")


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bcrypt Login Validator")
        self.root.geometry("400x250")
        self.root.resizable(False, False)  # Fixed window size

        # Set background color
        self.root.configure(bg="#FFEDF3")  # Light pinkish background

        self._create_widgets()

    def _create_widgets(self):
        # Frame for better organization and padding
        main_frame = tk.Frame(self.root, bg="#FFEDF3", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = tk.Label(
            main_frame,
            text="Login to System",
            font=("Arial", 16, "bold"),
            bg="#FFEDF3",
            fg="#333333"
        )
        title_label.pack(pady=15)

        # Password Label and Entry
        password_label = tk.Label(
            main_frame,
            text="Enter Password:",
            font=("Arial", 10),
            bg="#FFEDF3",
            fg="#555555"
        )
        password_label.pack(anchor="w", pady=(10, 2))

        self.password_entry = ttk.Entry(main_frame, show="*", width=40)
        self.password_entry.pack(pady=5)
        self.password_entry.focus_set()  # Set focus to the password entry

        # Login Button
        # Using a custom style for the button to apply specific background color
        style = ttk.Style()
        style.configure(
            "Login.TButton",
            background="#ADEED9",  # Light green/teal color
            foreground="#333333",
            font=("Arial", 10, "bold"),
            padding=8
        )
        # Map hover state for a subtle visual feedback
        style.map(
            "Login.TButton",
            background=[('active', '#8CD9B9')],  # Slightly darker on hover
            foreground=[('active', '#333333')]
        )

        login_button = ttk.Button(
            main_frame,
            text="Login",
            command=self._check_login,
            style="Login.TButton"  # Apply the custom style
        )
        login_button.pack(pady=20)

        # Bind Enter key to login function
        self.root.bind('<Return>', lambda event=None: self._check_login())

    def _check_login(self):
        entered_password = self.password_entry.get()
        if not entered_password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return

        password_bytes = entered_password.encode('utf-8')

        # Verify the entered password against the pre-hashed password
        if bcrypt.checkpw(password_bytes, HASHED_DEMO_PASSWORD):
            messagebox.showinfo("Login Status", "Login Successful!")
        else:
            messagebox.showerror("Login Status", f"Invalid Login Password: '{entered_password}'")

        self.password_entry.delete(0, tk.END)  # Clear the password field


if __name__ == "__main__":
    # Ensure bcrypt is installed: pip install bcrypt
    try:
        import bcrypt
    except ImportError:
        messagebox.showerror("Error",
                             "The 'bcrypt' library is not installed.\nPlease run 'pip install bcrypt' in your terminal.")
        exit()

    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

