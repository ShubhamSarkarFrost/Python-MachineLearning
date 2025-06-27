import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk      # pip install pillow
import os

UNITS = ("Celsius", "Fahrenheit", "Kelvin")

def to_celsius(v, unit):
    return {"Celsius": v,
            "Fahrenheit": (v - 32) * 5 / 9,
            "Kelvin": v - 273.15}[unit]

def from_celsius(v, unit):
    return {"Celsius": v,
            "Fahrenheit": v * 9 / 5 + 32,
            "Kelvin": v + 273.15}[unit]

class TempApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Temp Converter")
        self.geometry("280x320")
        self.configure(bg="#f0f0f0")

        self._add_icon()
        self._build_ui()

    # ―― optional icon ――
    def _add_icon(self):
        path = os.path.join(os.path.dirname(__file__),
                            "resources", "temperature.png")
        if os.path.exists(path):
            img = Image.open(path).resize((80, 80), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            tk.Label(self, image=self.photo, bg="#f0f0f0").pack(pady=10)

    # ―― main widgets ――
    def _build_ui(self):
        self.entry = tk.Entry(self, justify="center")
        self.entry.insert(0, "0")
        self.entry.pack(pady=5)

        self.from_unit = tk.StringVar(value=UNITS[0])
        self.to_unit   = tk.StringVar(value=UNITS[1])

        for label, var in (("From", self.from_unit), ("To", self.to_unit)):
            tk.Label(self, text=label, bg="#f0f0f0").pack()
            ttk.Combobox(self, textvariable=var,
                         values=UNITS, state="readonly").pack(pady=2)

        tk.Button(self, text="Convert", command=self.convert).pack(pady=10)
        self.result = tk.Label(self, text="Result: ",
                               font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.result.pack()

    # ―― conversion ――
    def convert(self):
        try:
            value = float(self.entry.get())
            if self.from_unit.get() == self.to_unit.get():
                result = value
            else:
                result = from_celsius(
                    to_celsius(value, self.from_unit.get()), self.to_unit.get()
                )
            self.result.config(text=f"Result: {result:.2f} {self.to_unit.get()}")
        except ValueError:
            messagebox.showerror("Input Error", "Enter a numeric value.")

if __name__ == "__main__":
    TempApp().mainloop()
