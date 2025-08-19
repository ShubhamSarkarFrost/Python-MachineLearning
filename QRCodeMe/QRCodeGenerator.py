import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyqrcode
from PIL import Image, ImageTk
import io
import os


class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        self.qr_image = None
        self.qr_code = None

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="QR Code Generator",
                                font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input section
        ttk.Label(main_frame, text="Enter text or URL:").grid(row=1, column=0,
                                                              sticky=tk.W, pady=(0, 5))

        # Text input with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                        pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.text_input = tk.Text(text_frame, height=4, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_input.yview)
        self.text_input.configure(yscrollcommand=scrollbar.set)

        self.text_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E),
                           pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)

        # Error correction level
        ttk.Label(options_frame, text="Error Correction:").grid(row=0, column=0,
                                                                sticky=tk.W, padx=(0, 5))
        self.error_correction = ttk.Combobox(options_frame, values=['L', 'M', 'Q', 'H'],
                                             state="readonly", width=10)
        self.error_correction.set('M')  # Default to Medium
        self.error_correction.grid(row=0, column=1, sticky=tk.W, pady=2)

        # Scale factor
        ttk.Label(options_frame, text="Scale:").grid(row=1, column=0, sticky=tk.W,
                                                     padx=(0, 5))
        self.scale_var = tk.IntVar(value=8)
        scale_frame = ttk.Frame(options_frame)
        scale_frame.grid(row=1, column=1, sticky=tk.W, pady=2)

        self.scale_scale = ttk.Scale(scale_frame, from_=4, to=12, orient=tk.HORIZONTAL,
                                     variable=self.scale_var, length=150)
        self.scale_scale.grid(row=0, column=0)

        self.scale_label = ttk.Label(scale_frame, text="8")
        self.scale_label.grid(row=0, column=1, padx=(5, 0))

        self.scale_scale.configure(command=self.update_scale_label)

        # Generate button
        generate_btn = ttk.Button(main_frame, text="Generate QR Code",
                                  command=self.generate_qr_code)
        generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # QR Code display frame
        display_frame = ttk.LabelFrame(main_frame, text="Generated QR Code", padding="5")
        display_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                           pady=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)

        # Canvas for QR code display
        self.canvas = tk.Canvas(display_frame, bg="white", width=300, height=300)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Save button
        self.save_btn = ttk.Button(buttons_frame, text="Save as PNG",
                                   command=self.save_qr_code, state="disabled")
        self.save_btn.grid(row=0, column=0, padx=(0, 5))

        # Clear button
        clear_btn = ttk.Button(buttons_frame, text="Clear", command=self.clear_all)
        clear_btn.grid(row=0, column=1, padx=5)

        # Configure main_frame grid weights
        main_frame.rowconfigure(5, weight=1)

    def update_scale_label(self, value):
        """Update the scale label when slider moves"""
        self.scale_label.config(text=str(int(float(value))))

    def generate_qr_code(self):
        """Generate QR code from input text"""
        text = self.text_input.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter some text to generate QR code")
            return

        try:
            # Generate QR code
            error_level = self.error_correction.get()
            scale = self.scale_var.get()

            # Create QR code
            self.qr_code = pyqrcode.create(text, error=error_level)

            # Convert to PNG in memory
            buffer = io.BytesIO()
            self.qr_code.png(buffer, scale=scale)
            buffer.seek(0)

            # Open with PIL and display
            pil_image = Image.open(buffer)
            self.qr_image = pil_image.copy()  # Keep original for saving

            # Resize for display if needed
            display_size = 300
            if pil_image.width > display_size or pil_image.height > display_size:
                pil_image.thumbnail((display_size, display_size), Image.Resampling.LANCZOS)

            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(pil_image)

            # Clear canvas and display image
            self.canvas.delete("all")
            self.canvas.configure(width=pil_image.width, height=pil_image.height)
            self.canvas.create_image(pil_image.width // 2, pil_image.height // 2,
                                     image=photo, anchor=tk.CENTER)

            # Keep a reference to prevent garbage collection
            self.canvas.image = photo

            # Enable save button
            self.save_btn.config(state="normal")

            messagebox.showinfo("Success", "QR code generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def save_qr_code(self):
        """Save the generated QR code as PNG file"""
        if self.qr_image is None:
            messagebox.showwarning("Warning", "No QR code to save. Generate one first.")
            return

        try:
            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                title="Save QR Code"
            )

            if filename:
                self.qr_image.save(filename)
                messagebox.showinfo("Success", f"QR code saved as {os.path.basename(filename)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")

    def clear_all(self):
        """Clear all inputs and displays"""
        self.text_input.delete("1.0", tk.END)
        self.canvas.delete("all")
        self.canvas.configure(bg="white")
        self.save_btn.config(state="disabled")
        self.qr_image = None
        self.qr_code = None


def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()