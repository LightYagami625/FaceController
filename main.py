import tkinter as tk
import os

def open_file():
    # Replace 'opcv.py' with the path to the Python file you want to open
    os.system("python opcv.py")

# Create the main window
root = tk.Tk()
root.title("OpenCV GUI")
#root.geometry("300x200")
canvas=tk.Canvas(root,width=400,height=200)
canvas.pack()
canvas.create_oval(50,50,350,150, fill='white')

# Add a button to open the Python file
open_button = tk.Button(root, text="Open opcv.py", command=open_file, font=("Arial", 12), bg="grey", fg="white")
open_button.pack(pady=50)

# Run the GUI event loop
root.mainloop()