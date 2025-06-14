import cv2
import subprocess
from PIL import Image, ImageDraw
import numpy as np

# Funktion: Gesichter verpixeln
def pixelate_face(image_path, output_path):
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.resize(face, (10, 10), interpolation=cv2.INTER_LINEAR)
        face = cv2.resize(face, (w, h), interpolation=cv2.INTER_NEAREST)
        image[y:y+h, x:x+w] = face

    cv2.imwrite(output_path, image)

# Funktion: Metadaten entfernen
def remove_metadata(image_path, output_path):
    subprocess.run(["exiftool", "-all=", image_path, "-o", output_path])

# Funktion: Gesichter verwischen
def blur_faces(image_path, output_path):
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.GaussianBlur(face, (99, 99), 30)
        image[y:y+h, x:x+w] = face

    cv2.imwrite(output_path, image)

# Funktion: Text oder Logos entfernen
def remove_text(image_path, output_path, coordinates):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    for (x, y, w, h) in coordinates:
        draw.rectangle([x, y, x+w, y+h], fill="black")
    image.save(output_path)

# Funktion: Hintergrund ändern (vereinfachtes Beispiel)
def change_background(image_path, output_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([0, 0, 0])
    upper_bound = np.array([180, 255, 30])
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    image[mask > 0] = [255, 255, 255]  # ersetze dunklen Hintergrund mit Weiß

    cv2.imwrite(output_path, image)

# Hauptprogramm
if __name__ == "__main__":
    print("Wähle eine Option:")
    print("1: Gesichter verpixeln")
    print("2: Metadaten entfernen")
    print("3: Gesichter verwischen")
    print("4: Text oder Logos entfernen")
    print("5: Hintergrund ändern")

    choice = input("Option eingeben (1-5): ")
    input_path = input("Pfad zum Eingabebild: ")
    output_path = input("Pfad zum Ausgabebild: ")

    if choice == "1":
        pixelate_face(input_path, output_path)
        print("Gesichter wurden verpixelt.")
    elif choice == "2":
        remove_metadata(input_path, output_path)
        print("Metadaten wurden entfernt.")
    elif choice == "3":
        blur_faces(input_path, output_path)
        print("Gesichter wurden verwischt.")
    elif choice == "4":
        coordinates = eval(input("Gib die Koordinaten als Liste von Tupeln ein (z.B. [(50, 50, 100, 50)]): "))
        remove_text(input_path, output_path, coordinates)
        print("Text oder Logos wurden entfernt.")
    elif choice == "5":
        change_background(input_path, output_path)
        print("Hintergrund wurde geändert.")
    else:
        print("Ungültige Option.")
