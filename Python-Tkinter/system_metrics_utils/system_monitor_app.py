import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk # For image handling
import os # For path manipulation

# Import the separated system metrics logic
import system_metrics

class SystemMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("System Monitor")
        master.geometry("450x480") # Increased height for the image
        master.resizable(False, False)
        master.configure(bg="#f0f0f0") # Light grey background

        # --- Check for psutil installation (handled here as it's the entry point) ---
        try:
            import psutil
        except ImportError:
            messagebox.showerror("Error", "psutil library not found.\n"
                                   "Please install it using: pip install psutil")
            master.destroy() # Close the window if psutil is not found
            return

        # --- UI Elements ---

        # 1. Application Icon at the top
        # Assumes 'monitor_icon.png' is in a 'resources' folder next to the script
        self.app_icon_path = os.path.join(os.path.dirname(__file__), "resources", "monitor.png")
        self.app_photo_image = None # To hold the PhotoImage reference

        try:
            # Load the image using Pillow
            original_image = Image.open(self.app_icon_path)
            # Resize image to a suitable size (e.g., 100x100 pixels)
            resized_image = original_image.resize((100, 100), Image.LANCZOS)
            self.app_photo_image = ImageTk.PhotoImage(resized_image)

            # Create a Label to display the image
            self.icon_label = tk.Label(master, image=self.app_photo_image, bg="#f0f0f0")
            self.icon_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showwarning("Icon Not Found",
                                   f"Application icon not found at: {self.app_icon_path}\n"
                                   "Please ensure 'monitor_icon.png' is in a 'resources' folder next to the script.")
            # Create a placeholder label if image not found
            tk.Label(master, text="(Icon Missing)", font=("Arial", 10), fg="red", bg="#f0f0f0").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Icon Error", f"Could not load application icon: {e}")
            tk.Label(master, text="(Icon Error)", font=("Arial", 10), fg="red", bg="#f0f0f0").pack(pady=10)


        # Header Label
        tk.Label(master, text="Real-time System Monitor",
                 font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333333") \
            .pack(pady=5) # Reduced pady as icon is already there

        # Frame for displaying metrics
        metrics_frame = tk.LabelFrame(master, text="System Metrics", padx=20, pady=15, bg="#ffffff", bd=2, relief=tk.GROOVE)
        metrics_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # CPU Usage
        tk.Label(metrics_frame, text="CPU Usage:", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        self.cpu_label = tk.Label(metrics_frame, text="N/A", font=("Arial", 12), bg="#ffffff", fg="#007bff")
        self.cpu_label.grid(row=0, column=1, sticky="w", pady=5)

        # Memory Usage
        tk.Label(metrics_frame, text="Memory Usage:", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
        self.memory_label = tk.Label(metrics_frame, text="N/A", font=("Arial", 12), bg="#ffffff", fg="#007bff")
        self.memory_label.grid(row=1, column=1, sticky="w", pady=5)

        # Disk Usage
        # Determine the default disk path based on OS
        disk_path_label = "Disk Usage (C:):" if os.name == 'nt' else "Disk Usage (/):"
        self.disk_path = 'C:\\' if os.name == 'nt' else '/' # Store the actual path
        tk.Label(metrics_frame, text=disk_path_label, font=("Arial", 12, "bold"), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
        self.disk_label = tk.Label(metrics_frame, text="N/A", font=("Arial", 12), bg="#ffffff", fg="#007bff")
        self.disk_label.grid(row=2, column=1, sticky="w", pady=5)

        # Network Activity (Bytes Sent/Received)
        tk.Label(metrics_frame, text="Net Sent:", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5)
        self.net_sent_label = tk.Label(metrics_frame, text="N/A", font=("Arial", 12), bg="#ffffff", fg="#007bff")
        self.net_sent_label.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(metrics_frame, text="Net Received:", font=("Arial", 12, "bold"), bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5)
        self.net_recv_label = tk.Label(metrics_frame, text="N/A", font=("Arial", 12), bg="#ffffff", fg="#007bff")
        self.net_recv_label.grid(row=4, column=1, sticky="w", pady=5)

        # Status Label
        self.status_label = tk.Label(master, text="Updating...", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Start updating metrics
        self.update_metrics()

    def update_metrics(self):
        """
        Fetches and updates system metrics in the GUI by calling functions from system_metrics.
        """
        try:
            # CPU Usage
            cpu_percent = system_metrics.get_cpu_usage()
            self.cpu_label.config(text=f"{cpu_percent}%")

            # Memory Usage
            memory_info = system_metrics.get_memory_usage()
            self.memory_label.config(text=f"{memory_info['percent']}% ({memory_info['used_gb']:.2f} GB / {memory_info['total_gb']:.2f} GB)")

            # Disk Usage
            disk_usage = system_metrics.get_disk_usage(self.disk_path)
            self.disk_label.config(text=f"{disk_usage['percent']}% ({disk_usage['used_gb']:.2f} GB / {disk_usage['total_gb']:.2f} GB)")

            # Network Activity
            net_activity = system_metrics.get_network_activity()
            self.net_sent_label.config(text=f"{net_activity['bytes_sent_gb']:.2f} GB")
            self.net_recv_label.config(text=f"{net_activity['bytes_recv_gb']:.2f} GB")

            # Update status label with current time for last update
            import datetime
            self.status_label.config(text=f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            self.status_label.config(text=f"Error updating metrics: {e}")
            print(f"Error updating metrics: {e}") # Log error to console

        # Schedule the next update after 1000 milliseconds (1 second)
        self.master.after(1000, self.update_metrics)


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()