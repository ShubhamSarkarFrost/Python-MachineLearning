import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import python_core_hashing # Import the core logic module

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Hash Password Manager")
        self.root.geometry("800x600")
        # Set background color
        self.root.configure(bg="#FFEDF3")  # Light pinkish background
        self.root.resizable(False, False) # Fixed window size

        self.encryptor = None # Will be set after successful master password login

        # Check master password status using core logic
        if python_core_hashing.check_master_password_exists():
            self.show_login_screen()
        else:
            self.show_set_master_password_screen()

    def clear_frame(self):
        """Clears all widgets from the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- Master Password Screens ---
    def show_set_master_password_screen(self):
        self.clear_frame()
        self.root.title("Set Master Password")

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Set Your Master Password", font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Label(frame, text="New Master Password:").pack(anchor="w", pady=5)
        self.new_master_pwd_entry = ttk.Entry(frame, show="*", width=40)
        self.new_master_pwd_entry.pack(pady=5)

        ttk.Label(frame, text="Confirm Master Password:").pack(anchor="w", pady=5)
        self.confirm_master_pwd_entry = ttk.Entry(frame, show="*", width=40)
        self.confirm_master_pwd_entry.pack(pady=5)

        ttk.Button(frame, text="Set Master Password", command=self._set_master_password_action).pack(pady=20)

    def _set_master_password_action(self):
        new_pwd = self.new_master_pwd_entry.get()
        confirm_pwd = self.confirm_master_pwd_entry.get()

        if not new_pwd or not confirm_pwd:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        if new_pwd != confirm_pwd:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        python_core_hashing.set_new_master_password(new_pwd) # Use core logic
        messagebox.showinfo("Success", "Master password set successfully!")
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_frame()
        self.root.title("Login to Password Manager")

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Enter Master Password to Login", font=("Arial", 16, "bold")).pack(pady=20)

        ttk.Label(frame, text="Master Password:").pack(anchor="w", pady=5)
        self.login_master_pwd_entry = ttk.Entry(frame, show="*", width=40)
        self.login_master_pwd_entry.pack(pady=5)

        ttk.Button(frame, text="Login", command=self._login_action).pack(pady=20)

    def _login_action(self):
        entered_pwd = self.login_master_pwd_entry.get()
        if not entered_pwd:
            messagebox.showerror("Error", "Please enter your master password.")
            return

        if python_core_hashing.verify_master_password(entered_pwd): # Use core logic
            self.encryptor = python_core_hashing.PasswordEncryptor(entered_pwd) # Initialize encryptor
            messagebox.showinfo("Success", "Login successful!")
            self.show_main_manager_screen()
        else:
            messagebox.showerror("Login Failed", "Incorrect master password.")

    # --- Main Manager Screen ---
    def show_main_manager_screen(self):
        self.clear_frame()
        self.root.title("Password Manager")

        # Top section for adding entries
        add_frame = ttk.LabelFrame(self.root, text="Add New Entry", padding="10")
        add_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(add_frame, text="Website:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.website_entry = ttk.Entry(add_frame, width=30)
        self.website_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Username:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = ttk.Entry(add_frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Password:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(add_frame, width=30)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Generate", command=self._generate_and_set_password_action).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(add_frame, text="Add Entry", command=self._add_entry_action).grid(row=3, column=1, pady=10)

        # Middle section for displaying entries
        display_frame = ttk.LabelFrame(self.root, text="Stored Passwords", padding="10")
        display_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(display_frame, columns=("Website", "Username"), show="headings")
        self.tree.heading("Website", text="Website")
        self.tree.heading("Username", text="Username")
        self.tree.column("Website", width=200, anchor="center")
        self.tree.column("Username", width=200, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Scrollbar for the Treeview
        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Double-1>", self._on_tree_double_click) # Double click to show/copy

        # Bottom section for actions
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(pady=10, padx=20, fill="x")

        ttk.Button(action_frame, text="Refresh List", command=self._load_entries_action).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Selected", command=self._delete_selected_entry_action).pack(side="right", padx=5)

        self._load_entries_action() # Load entries on startup

    def _add_entry_action(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        python_core_hashing.add_password_entry(self.encryptor, website, username, password) # Use core logic

        messagebox.showinfo("Success", "Entry added successfully!")
        self.website_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self._load_entries_action()

    def _load_entries_action(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        entries = python_core_hashing.get_all_password_entries() # Use core logic

        for entry in entries:
            self.tree.insert("", "end", iid=entry['id'], values=(entry['website'], entry['username']))

    def _on_tree_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_id = self.tree.item(selected_item[0])['iid']
        self._show_decrypted_password_action(item_id)

    def _show_decrypted_password_action(self, entry_id):
        encrypted_pwd = python_core_hashing.get_encrypted_password_by_id(entry_id) # Use core logic

        if encrypted_pwd:
            decrypted_pwd = self.encryptor.decrypt(encrypted_pwd)
            if decrypted_pwd:
                result = simpledialog.askstring("Decrypted Password",
                                                f"Password:\n\n{decrypted_pwd}\n\nClick OK to copy to clipboard.",
                                                parent=self.root)
                if result is not None: # User clicked OK
                    self.root.clipboard_clear()
                    self.root.clipboard_append(decrypted_pwd)
                    messagebox.showinfo("Copied", "Password copied to clipboard!")
            else:
                # Decryption failed, error message already shown by PasswordEncryptor
                pass
        else:
            messagebox.showerror("Error", "Entry not found.")

    def _delete_selected_entry_action(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an entry to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?")
        if confirm:
            item_id = selected_item[0]
            python_core_hashing.delete_password_entry_by_id(item_id) # Use core logic
            messagebox.showinfo("Deleted", "Entry deleted successfully.")
            self._load_entries_action()

    def _generate_and_set_password_action(self):
        generated_pwd = python_core_hashing.generate_password(length=16, use_digits=True, use_symbols=True, use_uppercase=True, use_lowercase=True) # Use core logic
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, generated_pwd)
        messagebox.showinfo("Password Generated", "A strong password has been generated and placed in the password field.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
