import tkinter as tk
import complete 
from tkinter import filedialog

# Function to open the file dialog
def open_file():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if file_path:  # Check if a file was selected
        complete.complete(file_path)


# Create the main application window
root = tk.Tk()
root.title("File Open Dialog Example")
root.geometry("400x200")

# Create a label to display the selected file path
label = tk.Label(root, text="No file selected", font=("Arial", 12))
label.pack(pady=20)

# Create a button to trigger the file open dialog
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()