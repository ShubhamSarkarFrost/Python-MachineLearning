import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageViewerApp:
    def __init__(self, master):
        """
        Initializes the Tkinter Image Viewer application.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        master.title("Simple Image Viewer")
        master.geometry("800x600") # Set initial window size
        master.configure(bg="#f0f0f0") # Light grey background

        self.current_image_index = 0
        self.image_files = []
        self.photo_image = None # To hold the Tkinter PhotoImage object

        # --- UI Elements ---

        # Frame for controls (buttons)
        self.control_frame = tk.Frame(master, bg="#e0e0e0", bd=2, relief=tk.RAISED)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Open Directory Button
        self.open_button = tk.Button(
            self.control_frame,
            text="Open Folder",
            command=self.open_directory,
            font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white",
            activebackground="#45a049",
            bd=0, relief=tk.FLAT, padx=10, pady=5,
            cursor="hand2"
        )
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Navigation Buttons
        self.prev_button = tk.Button(
            self.control_frame,
            text="< Prev",
            command=self.show_previous_image,
            font=("Arial", 12),
            bg="#2196F3", fg="white",
            activebackground="#1976D2",
            bd=0, relief=tk.FLAT, padx=10, pady=5,
            cursor="hand2",
            state=tk.DISABLED # Disabled initially
        )
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(
            self.control_frame,
            text="Next >",
            command=self.show_next_image,
            font=("Arial", 12),
            bg="#2196F3", fg="white",
            activebackground="#1976D2",
            bd=0, relief=tk.FLAT, padx=10, pady=5,
            cursor="hand2",
            state=tk.DISABLED # Disabled initially
        )
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Image Label (where the image will be displayed)
        self.image_label = tk.Label(master, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Status Label
        self.status_label = tk.Label(master, text="No folder selected.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Bind resize event to update image display
        master.bind("<Configure>", self.on_resize)

    def open_directory(self):
        """
        Opens a file dialog to select a directory and loads image files from it.
        """
        directory = filedialog.askdirectory()
        if directory:
            self.image_files = []
            # Supported image extensions
            supported_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
            for filename in os.listdir(directory):
                if filename.lower().endswith(supported_extensions):
                    self.image_files.append(os.path.join(directory, filename))

            self.image_files.sort() # Sort files for consistent order

            if not self.image_files:
                messagebox.showinfo("No Images Found", "No supported image files found in the selected directory.")
                self.status_label.config(text=f"No images found in: {directory}")
                self.clear_image_display()
                self.update_navigation_buttons()
                return

            self.current_image_index = 0
            self.show_current_image()
            self.update_navigation_buttons()
            self.status_label.config(text=f"Loaded {len(self.image_files)} images from: {directory}")
        else:
            self.status_label.config(text="Folder selection cancelled.")

    def show_current_image(self):
        """
        Displays the image at the current_image_index in the image_label.
        Handles resizing the image to fit the label.
        """
        if not self.image_files:
            self.clear_image_display()
            return

        image_path = self.image_files[self.current_image_index]
        try:
            # Open the image using Pillow
            original_image = Image.open(image_path)

            # Get label dimensions
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()

            # Only resize if label has actual dimensions (after it's rendered)
            if label_width == 1 or label_height == 1: # Default Tkinter size before packing/rendering
                # If label dimensions are not yet available, use a fallback or wait
                # For initial load, we might need a slight delay or rely on on_resize
                # For now, we'll assume it gets dimensions soon after packing.
                # A more robust solution might involve .update_idletasks()
                pass

            # Calculate aspect ratio to fit image within label without distortion
            img_width, img_height = original_image.size
            aspect_ratio = img_width / img_height

            if label_width > 1 and label_height > 1:
                # Calculate new dimensions based on label size
                if (label_width / label_height) > aspect_ratio:
                    # Label is wider, fit by height
                    new_height = label_height
                    new_width = int(new_height * aspect_ratio)
                else:
                    # Label is taller or same aspect, fit by width
                    new_width = label_width
                    new_height = int(new_width / aspect_ratio)

                # Ensure dimensions are at least 1x1 to avoid errors
                new_width = max(1, new_width)
                new_height = max(1, new_height)

                resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
            else:
                # If label size is not yet available, display original or a default size
                # For simplicity, we'll display a smaller version if label not ready
                resized_image = original_image.copy() # Use a copy to avoid modifying original
                max_dim = 500 # Max dimension for initial display if label not ready
                if img_width > max_dim or img_height > max_dim:
                    if (img_width / img_height) > 1:
                        resized_image = original_image.resize((max_dim, int(max_dim / aspect_ratio)), Image.LANCZOS)
                    else:
                        resized_image = original_image.resize((int(max_dim * aspect_ratio), max_dim), Image.LANCZOS)


            self.photo_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.photo_image)
            self.status_label.config(text=f"Displaying: {os.path.basename(image_path)} ({self.current_image_index + 1}/{len(self.image_files)})")

        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load image '{os.path.basename(image_path)}': {e}")
            self.clear_image_display()
            self.status_label.config(text=f"Error loading image: {os.path.basename(image_path)}")

    def clear_image_display(self):
        """Clears the image displayed in the label."""
        self.image_label.config(image='')
        self.photo_image = None # Release reference to PhotoImage

    def show_next_image(self):
        """Displays the next image in the list."""
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.show_current_image()
            self.update_navigation_buttons()

    def show_previous_image(self):
        """Displays the previous image in the list."""
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1 + len(self.image_files)) % len(self.image_files)
            self.show_current_image()
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        """Enables/disables navigation buttons based on the number of images."""
        if len(self.image_files) > 1:
            self.prev_button.config(state=tk.NORMAL)
            self.next_button.config(state=tk.NORMAL)
        else:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)

    def on_resize(self, event):
        """
        Callback function for window resize event.
        Redraws the current image to fit the new window size.
        """
        # Only redraw if the image label has content and its size has changed significantly
        if self.photo_image and self.image_files and (event.widget == self.master or event.widget == self.image_label):
            # Check if the label's actual width/height changed from previous state
            # This prevents excessive redraws during rapid resizing
            if self.image_label.winfo_width() > 1 and self.image_label.winfo_height() > 1:
                self.show_current_image()


if __name__ == "__main__":
    # Ensure Pillow is installed: pip install Pillow
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Error", "Pillow library not found.\nPlease install it using: pip install Pillow")
        exit()

    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
