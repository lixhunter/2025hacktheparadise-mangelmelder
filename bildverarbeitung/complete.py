import cv2
import torch
import numpy as np
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def blur_license_plates_yolov5(image, model):
    # Modell auf Bild anwenden (Erkennung)
    results = model(image)

    # Ergebnisse als DataFrame bekommen (xmin, ymin, xmax, ymax, confidence, class, name)
    detections = results.pandas().xyxy[0]

    for idx, row in detections.iterrows():
        # Nur Nummernschilder (Klasse 0 oder Name 'license plate' prüfen)
        if row['name'] == 'license plate' or row['class'] == 0:
            x_min, y_min, x_max, y_max = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
            # Rechteck verpixeln (verkleinern und vergrößern)
            roi = image[y_min:y_max, x_min:x_max]
            roi = cv2.resize(roi, (10, 10), interpolation=cv2.INTER_LINEAR)
            roi = cv2.resize(roi, (x_max - x_min, y_max - y_min), interpolation=cv2.INTER_NEAREST)
            image[y_min:y_max, x_min:x_max] = roi
    return image

def pixelate_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.resize(face, (10, 10), interpolation=cv2.INTER_LINEAR)
        face = cv2.resize(face, (w, h), interpolation=cv2.INTER_NEAREST)
        image[y:y+h, x:x+w] = face
    return image

if __name__ == "__main__":
    input_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/personen/3e834d56-1644-4345-9091-7a29967bb775.jpeg"
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/output_pixelated.jpeg"
    model_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/Automatic-Number-Plate-Recognition-using-YOLOv5/Weights/best.pt"

    # Modell laden (nur einmal)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    # Bild laden
    image = cv2.imread(input_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        exit(1)

    # Nummernschilder verpixeln
    image = blur_license_plates_yolov5(image, model)

    # Gesichter verpixeln
    image = pixelate_faces(image)

    # Ergebnis speichern
    cv2.imwrite(output_path, image)
    print(f"Bild mit verpixelten Nummernschildern und Gesichtern gespeichert unter: {output_path}")
