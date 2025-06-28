import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

# Import the separated logic functions
# These functions handle the core file compression and decompression operations.
from compress_logic import compress_file_data
from decompress_logic import decompress_file_data

class CompressionToolApp:
    def __init__(self, master):
        """
        Initializes the Tkinter File Compression/Decompression application.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("File Compression Tool")
        master.geometry("500x350")
        master.resizable(False, False)
        master.configure(bg="#f0f0f0") # Light grey background

        # --- UI Elements ---

        # Header Label
        tk.Label(master, text="File Compression & Decompression",
                 font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333") \
            .pack(pady=15)

        # --- Compression Section ---
        compress_frame = tk.LabelFrame(master, text="Compress File", padx=15, pady=15, bg="#ffffff", bd=2, relief=tk.GROOVE)
        compress_frame.pack(padx=20, pady=10, fill=tk.X)

        self.compress_file_path = tk.StringVar()
        tk.Label(compress_frame, text="Source File:", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(compress_frame, textvariable=self.compress_file_path, width=40, state="readonly").grid(row=0, column=1, pady=5, padx=5)
        tk.Button(compress_frame, text="Browse", command=self.browse_file_to_compress).grid(row=0, column=2, pady=5)

        tk.Button(compress_frame, text="Compress", command=self.compress_file,
                  font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", activebackground="#45a049") \
            .grid(row=1, column=0, columnspan=3, pady=10)

        # --- Decompression Section ---
        decompress_frame = tk.LabelFrame(master, text="Decompress File", padx=15, pady=15, bg="#ffffff", bd=2, relief=tk.GROOVE)
        decompress_frame.pack(padx=20, pady=10, fill=tk.X)

        self.decompress_file_path = tk.StringVar()
        tk.Label(decompress_frame, text="Compressed File:", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(decompress_frame, textvariable=self.decompress_file_path, width=40, state="readonly").grid(row=0, column=1, pady=5, padx=5)
        tk.Button(decompress_frame, text="Browse", command=self.browse_file_to_decompress).grid(row=0, column=2, pady=5)

        tk.Button(decompress_frame, text="Decompress", command=self.decompress_file,
                  font=("Arial", 10, "bold"), bg="#2196F3", fg="white", activebackground="#1976D2") \
            .grid(row=1, column=0, columnspan=3, pady=10)

        # --- Status Bar ---
        self.status_label = tk.Label(master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        print("CompressionToolApp initialized.")

    def browse_file_to_compress(self):
        """Opens a file dialog to select the file to be compressed."""
        filepath = filedialog.askopenfilename()
        if filepath:
            self.compress_file_path.set(filepath)
            self.update_status(f"Selected file for compression: {os.path.basename(filepath)}")

    def browse_file_to_decompress(self):
        """Opens a file dialog to select the compressed file for decompression."""
        filepath = filedialog.askopenfilename(filetypes=[("Compressed files", "*.zlib"), ("All files", "*.*")])
        if filepath:
            self.decompress_file_path.set(filepath)
            self.update_status(f"Selected file for decompression: {os.path.basename(filepath)}")

    def compress_file(self):
        """
        Calls the external compression logic and handles the GUI feedback.
        """
        source_path = self.compress_file_path.get()
        if not source_path:
            messagebox.showwarning("No File Selected", "Please select a file to compress.")
            return

        initial_filename = os.path.basename(source_path) + ".zlib"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".zlib",
            initialfile=initial_filename,
            filetypes=[("Compressed ZLIB files", "*.zlib"), ("All files", "*.*")]
        )

        if save_path:
            self.update_status(f"Compressing '{os.path.basename(source_path)}'...")
            success, message = compress_file_data(source_path, save_path)
            if success:
                messagebox.showinfo("Success", f"File compressed successfully!\nSaved as: {os.path.basename(save_path)}")
                self.update_status(f"Compressed '{os.path.basename(source_path)}' to '{os.path.basename(save_path)}'")
                self.compress_file_path.set("") # Clear input path on success
            else:
                messagebox.showerror("Error", f"Compression failed: {message}")
                self.update_status(f"Compression failed: {message}")
        else:
            self.update_status("Compression cancelled.")

    def decompress_file(self):
        """
        Calls the external decompression logic and handles the GUI feedback.
        """
        source_path = self.decompress_file_path.get()
        if not source_path:
            messagebox.showwarning("No File Selected", "Please select a compressed file to decompress.")
            return

        original_filename = os.path.basename(source_path)
        if original_filename.endswith(".zlib"):
            initial_filename = original_filename[:-5] # Remove .zlib
        else:
            initial_filename = "decompressed_" + original_filename

        save_path = filedialog.asksaveasfilename(
            initialfile=initial_filename,
            filetypes=[("All files", "*.*")]
        )

        if save_path:
            self.update_status(f"Decompressing '{os.path.basename(source_path)}'...")
            success, message = decompress_file_data(source_path, save_path)
            if success:
                messagebox.showinfo("Success", f"File decompressed successfully!\nSaved as: {os.path.basename(save_path)}")
                self.update_status(f"Decompressed '{os.path.basename(source_path)}' to '{os.path.basename(save_path)}'")
                self.decompress_file_path.set("") # Clear input path on success
            else:
                messagebox.showerror("Error", f"Decompression failed: {message}")
                self.update_status(f"Decompression failed: {message}")
        else:
            self.update_status("Decompression cancelled.")

    def update_status(self, message):
        """
        Updates the text in the status bar at the bottom of the application window.

        Args:
            message (str): The message string to display in the status bar.
        """
        self.status_label.config(text=message)
        self.master.update_idletasks() # Force update the GUI


if __name__ == "__main__":
    root = tk.Tk()
    app = CompressionToolApp(root)
    root.mainloop()
