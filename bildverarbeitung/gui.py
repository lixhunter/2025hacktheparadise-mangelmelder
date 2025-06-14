import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import complete  # dein Modul, z. B. complete.py mit pixelate und blackout

def show_image_on_label(cv_image, label, max_width=700, max_height=500):
    if cv_image is None:
        return
    rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    orig_width, orig_height = pil_image.size
    scale = min(max_width / orig_width, max_height / orig_height)

    new_width = int(orig_width * scale)
    new_height = int(orig_height * scale)

    pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    tk_image = ImageTk.PhotoImage(pil_image)
    label.config(image=tk_image)
    label.image = tk_image 

def open_file():
    file_path = filedialog.askopenfilename(
        title="Bild auswählen",
        filetypes=(("Bilddateien", "*.jpeg *.jpg *.png"), ("Alle Dateien", "*.*"))
    )
    if file_path:
        original = cv2.imread(file_path)
        show_image_on_label(original, label_original)

        result_image = complete.complete(file_path)
        show_image_on_label(result_image, label_processed)

root = tk.Tk()
root.title("Nummernschilder & Gesichter anonymisieren")
root.geometry("1500x700")  # Größeres Fenster

button = tk.Button(root, text="Bild auswählen", command=open_file)
button.grid(row=0, column=0, columnspan=2, pady=10)

label_original_text = tk.Label(root, text="Originalbild")
label_original_text.grid(row=1, column=0)

label_processed_text = tk.Label(root, text="Bearbeitetes Bild")
label_processed_text.grid(row=1, column=1)

label_original = tk.Label(root)
label_original.grid(row=2, column=0, padx=10)

label_processed = tk.Label(root)
label_processed.grid(row=2, column=1, padx=10)

root.mainloop()
