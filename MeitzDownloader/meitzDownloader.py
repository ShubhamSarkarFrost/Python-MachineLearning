import tkinter as tk
from tkinter import messagebox, filedialog
import yt_dlp
import os

def download_video():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a video link!")
        return

    try:
        save_path = filedialog.askdirectory()
        if not save_path:
            return

        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'mp4[ext=mp4][vcodec!=none][acodec!=none]/best',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # this returns metadata
            filename = ydl.prepare_filename(info)

        messagebox.showinfo("Success", f"Downloaded:\n{filename}")

    except Exception as e:
        messagebox.showerror("Download Failed", str(e))

# Tkinter UI
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("600x200")
root.config(bg="white")

heading = tk.Label(root, text="YouTube Video Downloader", font=("Arial", 16, "bold"), bg="white")
heading.pack(pady=10)

url_entry = tk.Entry(root, width=60, font=("Arial", 12), bd=2, relief="solid")
url_entry.pack(pady=10, padx=10)

download_btn = tk.Button(root, text="Download", font=("Arial", 12, "bold"),
                         bg="limegreen", fg="white", padx=20, pady=5,
                         command=download_video)
download_btn.pack(pady=10)

footer = tk.Label(root, text="Paste your video link above and click Download",
                  font=("Arial", 10), fg="gray", bg="white")
footer.pack(pady=5)

root.mainloop()
