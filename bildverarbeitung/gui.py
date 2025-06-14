import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import complete  # dein Modul, z. B. complete.py mit pixelate und blackout

# Funktion zum Anzeigen eines OpenCV-Bildes in einem Tkinter-Label
def show_image_on_label(cv_image, label, max_width=400, max_height=300):
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

# Callback für Button
def open_file():
    file_path = filedialog.askopenfilename(
        title="Bild auswählen",
        filetypes=(("Bilddateien", "*.jpeg *.jpg *.png"), ("Alle Dateien", "*.*"))
    )
    if file_path:
        # Originalbild anzeigen
        original = cv2.imread(file_path)
        show_image_on_label(original, label_original)

        # Ausgabepfad
        output_path = file_path.replace(".", "_processed.", 1)

        # Bild verarbeiten und anzeigen
        result_image = complete.complete(file_path)
        show_image_on_label(result_image, label_processed)

# Fenster
root = tk.Tk()
root.title("Nummernschilder & Gesichter anonymisieren")
root.geometry("850x700")

# Button
button = tk.Button(root, text="Bild auswählen", command=open_file)
button.pack(pady=10)

# Labels für Vorher/Nachher
label_original_text = tk.Label(root, text="Originalbild")
label_original_text.pack()
label_original = tk.Label(root)
label_original.pack()

label_processed_text = tk.Label(root, text="Bearbeitetes Bild")
label_processed_text.pack()
label_processed = tk.Label(root)
label_processed.pack()

# Starte GUI
root.mainloop()
