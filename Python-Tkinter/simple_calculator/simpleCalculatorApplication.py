from PIL import Image, ImageTk
from tkinter import *
import ast
import os

root = Tk()
root.title("Tkinter Calculator")
root.geometry("300x400")
root.resizable(False, False)

i = 0

# ---- Add an image at the top (should be in the same folder) ----
try:
    image_path = os.path.join(os.path.dirname(__file__), "calculator.png")  # Your image path
    original_img = Image.open(image_path)
    resized_img = original_img.resize((100, 100), Image.LANCZOS)  # Resize to 100x100
    calculator_img = ImageTk.PhotoImage(resized_img)

    image_label = Label(root, image=calculator_img)
    image_label.grid(row=0, column=0, columnspan=6, pady=10)
except Exception:
    Label(root, text="Calculator", font=("Arial", 16)).grid(row=0, column=0, columnspan=6, pady=10)

# --- Functions ---
def get_number(num):
    global i
    display.insert(i, num)
    i += 1

def get_operation(operator):
    global i
    length = len(operator)
    display.insert(i, operator)
    i += length

def clear_all():
    global i
    display.delete(0, END)
    i = 0

def calculate():
    global i
    entire_string = display.get()
    try:
        node = ast.parse(entire_string, mode="eval")
        result = eval(compile(node, '<string>', 'eval'))
        clear_all()
        display.insert(0, result)
        i = len(str(result))
    except Exception:
        clear_all()
        display.insert(0, "Error")
        i = 0

def undo():
    global i
    entire_string = display.get()
    if len(entire_string):
        new_string = entire_string[:-1]
        clear_all()
        display.insert(0, new_string)
        i = len(new_string)
    else:
        clear_all()
        display.insert(0, "")
        i = 0

# --- Entry Widget ---
display = Entry(root, font=("Arial", 14))
display.grid(row=1, columnspan=6, sticky=W + E, padx=10, pady=5)

# --- Number Buttons (1 to 9) ---
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
counter = 0
for x in range(3):
    for y in range(3):
        num = numbers[counter]
        Button(root, text=str(num), width=6, height=2, command=lambda n=num: get_number(n)) \
            .grid(row=x + 2, column=y, padx=2, pady=2)
        counter += 1

# --- Zero Button ---
Button(root, text="0", width=6, height=2, command=lambda: get_number(0)).grid(row=5, column=1, padx=2, pady=2)

# --- AC, =, < Buttons ---
Button(root, text="AC", width=6, height=2, command=clear_all).grid(row=5, column=0, padx=2, pady=2)
Button(root, text="=", width=6, height=2, command=calculate).grid(row=5, column=2, padx=2, pady=2)
Button(root, text="<-", width=6, height=2, command=undo).grid(row=5, column=4, padx=2, pady=2)

# --- Operator Buttons ---
operations = ['+', '-', '*', '/', '*3.14', "%", "(", "**", ")", "**2"]
count = 0
for x in range(4):
    for y in range(3):
        if count < len(operations):
            op = operations[count]
            Button(root, text=op, width=6, height=2, command=lambda o=op: get_operation(o)) \
                .grid(row=x + 2, column=y + 3, padx=2, pady=2)
            count += 1

root.mainloop()
