import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ExcelComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Comparator")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f8f9fa")

        self.file1 = None
        self.file2 = None
        self.df1 = None
        self.df2 = None

        # ===== Title =====
        title = tk.Label(
            root,
            text="Compare Excel files and other spreadsheets",
            font=("Arial", 16, "bold"),
            bg="#d4edda",
            fg="#155724",
            padx=10,
            pady=10
        )
        title.pack(fill="x")

        subtitle = tk.Label(
            root,
            text="Upload two Excel files to compare. Supported formats: xlsx, xls, csv, tsv",
            font=("Arial", 11),
            bg="#f8f9fa",
            fg="#6c757d"
        )
        subtitle.pack(pady=5)

        # ===== Main Frame =====
        main_frame = tk.Frame(root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left Panel
        left_frame = tk.Frame(main_frame, bd=2, relief="groove", bg="white", width=400, height=300)
        left_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        tk.Label(left_frame, text="Drop Excel File 1 Here", font=("Arial", 13), bg="white").pack(pady=40)
        tk.Button(left_frame, text="Browse File 1", command=self.load_file1).pack(pady=10)

        # Right Panel
        right_frame = tk.Frame(main_frame, bd=2, relief="groove", bg="white", width=400, height=300)
        right_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        tk.Label(right_frame, text="Drop Excel File 2 Here", font=("Arial", 13), bg="white").pack(pady=40)
        tk.Button(right_frame, text="Browse File 2", command=self.load_file2).pack(pady=10)

        # Compare Button
        compare_btn = tk.Button(root, text="Compare Files", font=("Arial", 12, "bold"), bg="#007bff", fg="white",
                                command=self.compare_files)
        compare_btn.pack(pady=15)

        # Graph Frame
        self.graph_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def load_file1(self):
        self.file1 = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls *.csv *.tsv")])
        if self.file1:
            try:
                if self.file1.endswith(".csv") or self.file1.endswith(".tsv"):
                    self.df1 = pd.read_csv(self.file1)
                else:
                    self.df1 = pd.read_excel(self.file1)
                self.clean_data(self.df1)
                messagebox.showinfo("File 1 Loaded", f"File 1 loaded successfully:\n{self.file1}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load File 1\n{e}")

    def load_file2(self):
        self.file2 = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls *.csv *.tsv")])
        if self.file2:
            try:
                if self.file2.endswith(".csv") or self.file2.endswith(".tsv"):
                    self.df2 = pd.read_csv(self.file2)
                else:
                    self.df2 = pd.read_excel(self.file2)
                self.clean_data(self.df2)
                messagebox.showinfo("File 2 Loaded", f"File 2 loaded successfully:\n{self.file2}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load File 2\n{e}")

    def clean_data(self, df):
        """Basic cleaning: drop NaN, remove duplicates"""
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

    def compare_files(self):
        if self.df1 is None or self.df2 is None:
            messagebox.showwarning("Missing Files", "Please upload both files first.")
            return

        # Find common columns for comparison
        common_cols = list(set(self.df1.columns).intersection(set(self.df2.columns)))
        numeric_cols = [col for col in common_cols if pd.api.types.is_numeric_dtype(self.df1[col])]

        if not numeric_cols:
            messagebox.showwarning("No Numeric Data", "No common numeric columns to compare.")
            return

        col_to_compare = numeric_cols[0]  # Compare first numeric column

        # Align lengths (truncate longer one)
        min_len = min(len(self.df1[col_to_compare]), len(self.df2[col_to_compare]))
        data1 = self.df1[col_to_compare].head(min_len).reset_index(drop=True)
        data2 = self.df2[col_to_compare].head(min_len).reset_index(drop=True)

        # Plot overlay graph
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(data1, label="File 1", color="#007bff", marker="o")
        ax.plot(data2, label="File 2", color="#28a745", marker="x")
        ax.set_title(f"Comparison of '{col_to_compare}' Column")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.legend()

        # Clear old graph and display new one
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelComparatorApp(root)
    root.mainloop()
