import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk  # Import Image and ImageTk for image handling
import os  # Import os for path manipulation

from tts_logic import TextToSpeechEngine


class TextToSpeechApp:
    def __init__(self, master):
        self.master = master
        master.title("Text To Speech Converter")
        master.geometry("450x450")
        master.resizable(False, False)
        master.configure(bg="#f0f0f0")

        self.tts_engine = TextToSpeechEngine()
        if not self.tts_engine.is_ready():
            messagebox.showerror("Engine Error",
                                 "Text-to-Speech engine could not be initialized.\n"
                                 "Please ensure necessary speech components are installed on your OS and pyttsx3 is correctly set up.")
            self.engine_ready = False
        else:
            self.engine_ready = True

        # --- UI Elements ---

        # 1. Application Icon at the top
        self.app_icon_path = os.path.join(os.path.dirname(__file__), "resources", "speech.png")
        self.app_photo_image = None

        try:
            original_image = Image.open(self.app_icon_path)
            resized_iamge = original_image.resize((80, 80), Image.LANCZOS)
            self.app_photo_image = ImageTk.PhotoImage(resized_iamge)
            # Create a Label to display the image
            self.icon_label = tk.Label(master, image=self.app_photo_image, bg="#f0f0f0")
            self.icon_label.pack(pady=10)
        except FileNotFoundError:
            messagebox.showwarning("Icon Not Found",
                                   f"Application icon not found at: {self.app_icon_path}\n"
                                   "Please ensure 'tts_icon.png' is in a 'resources' folder next to the script.")
            # Create a placeholder label if image not found
            tk.Label(master, text="(Icon Missing)", font=("Arial", 10), fg="red", bg="#f0f0f0").pack(pady=10)
        except Exception as e:
            messagebox.showerror("Icon Error", f"Could not load application icon: {e}")
            tk.Label(master, text="(Icon Error)", font=("Arial", 10), fg="red", bg="#f0f0f0").pack(pady=10)

            # Text input area label
        tk.Label(master, text="Enter text or load from file:",
                 font=("Arial", 12), bg="#f0f0f0", fg="#333333") \
            .pack(pady=(10, 5))

        self.text_input = tk.Text(master, height=7, width=50, wrap="word",
                                  font=("Arial", 10), bd=2, relief=tk.SUNKEN)
        self.text_input.pack(pady=5, padx=10)

        # Frame for buttons
        button_frame = tk.Frame(master, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Speak Button
        self.speak_button = tk.Button(
            button_frame,
            text="Speak",
            command=self.speak_text,
            font=("Arial", 12, "bold"),
            bg="#4CAF50", fg="white",
            activebackground="#45a049",
            bd=0, relief=tk.RAISED, padx=15, pady=8,
            cursor="hand2",
            state=tk.NORMAL if self.engine_ready else tk.DISABLED  # Disable if engine not ready
        )
        self.speak_button.pack(side=tk.LEFT, padx=5)

        # Browse File Button
        self.browse_button = tk.Button(
            button_frame,
            text="Load from File",
            command=self.load_text_from_file,
            font=("Arial", 12),
            bg="#2196F3", fg="white",
            activebackground="#1976D2",
            bd=0, relief=tk.RAISED, padx=15, pady=8,
            cursor="hand2"
        )
        self.browse_button.pack(side=tk.LEFT, padx=5)

        # Clear Button
        self.clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_text,
            font=("Arial", 12),
            bg="#FF6347", fg="white",
            activebackground="#E55337",
            bd=0, relief=tk.RAISED, padx=15, pady=8,
            cursor="hand2"
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)  # Changed to LEFT for better layout with new button

        # Status Label
        self.status_label = tk.Label(master, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e0e0e0")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        if not self.engine_ready:
            self.update_status("Error: TTS engine not initialized. Functionality limited.")

    def speak_text(self):
        """
        Retrieves text from the input area and speaks it using the TTS engine.
        """
        if not self.engine_ready:
            messagebox.showerror("Error", "Text-to-Speech engine is not initialized. Cannot speak.")
            return

        text = self.text_input.get("1.0", tk.END).strip()  # Get all text from the Text widget
        if not text:
            messagebox.showwarning("No Text", "Please enter some text or load from a file to speak.")
            self.update_status("No text entered.")
            return

        try:
            self.update_status("Speaking...")
            self.tts_engine.speak(text)
            self.update_status("Finished speaking.")
        except RuntimeError as e:
            messagebox.showerror("Speech Error", f"Engine not ready: {e}")
            self.update_status(f"Speech error: {e}")
        except Exception as e:
            messagebox.showerror("Speech Error", f"An unexpected error occurred during speech synthesis: {e}")
            self.update_status(f"Speech error: {e}")

    def load_text_from_file(self):
        """
        Opens a file dialog, reads text from the selected .txt file,
        and inserts it into the text input area.
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.text_input.delete("1.0", tk.END)  # Clear existing text
                self.text_input.insert("1.0", content)  # Insert new text
                self.update_status(f"Loaded text from: {os.path.basename(filepath)}")
            except FileNotFoundError:
                messagebox.showerror("File Error", f"File not found: {os.path.basename(filepath)}")
                self.update_status("File loading failed: Not found.")
            except Exception as e:
                messagebox.showerror("File Error", f"An error occurred while reading the file: {e}")
                self.update_status("File loading failed.")
        else:
            self.update_status("File loading cancelled.")

    def clear_text(self):
        """
        Clears the text from the input area.
        """
        self.text_input.delete("1.0", tk.END)
        self.update_status("Text cleared.")

    def update_status(self, message):
        """
        Updates the text in the status bar at the bottom of the application window.

        Args:
            message (str): The message string to display in the status bar.
        """
        self.status_label.config(text=message)
        self.master.update_idletasks()  # Force update the GUI


if __name__ == "__main__":
    # Ensure pyttsx3 is installed: pip install pyttsx3
    try:
        import pyttsx3
    except ImportError:
        messagebox.showerror("Error", "pyttsx3 library not found.\nPlease install it using: pip install pyttsx3")
        exit()

    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
