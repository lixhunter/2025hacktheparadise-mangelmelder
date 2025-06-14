import cv2
import torch
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def blackout_license_plates_yolov5(image, model):
    # Modell auf Bild anwenden (Erkennung)
    results = model(image)

    # Ergebnisse als DataFrame bekommen (xmin, ymin, xmax, ymax, confidence, class, name)
    detections = results.pandas().xyxy[0]

    for idx, row in detections.iterrows():
        # Nur Nummernschilder (Klasse 0 oder Name 'license plate' prüfen)
        if row['name'] == 'license plate' or row['class'] == 0:
            x_min, y_min, x_max, y_max = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
            # Rechteck komplett schwarz machen
            image[y_min:y_max, x_min:x_max] = 0
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

def complete(input_path):
    output_path = inputFile + "_blurred.jpg",
    model_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/Automatic-Number-Plate-Recognition-using-YOLOv5/Weights/best.pt"

    # YOLOv5 Modell laden (nur einmal)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    # Bild laden
    image = cv2.imread(input_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        exit(1)

    # Nummernschilder schwärzen
    image = blackout_license_plates_yolov5(image, model)

    # Gesichter verpixeln
    image = pixelate_faces(image)

    # Ergebnis speichern
    cv2.imwrite(output_path, image)
    print(f"Bild mit geschwärzten Nummernschildern und verpixelten Gesichtern gespeichert unter: {output_path}")



if __name__ == "__main__":
    input_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/personen/20250614_144511.jpg.jpeg"
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/output_blackout_pixelate.jpeg"
    model_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/Automatic-Number-Plate-Recognition-using-YOLOv5/Weights/best.pt"

    # YOLOv5 Modell laden (nur einmal)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    # Bild laden
    image = cv2.imread(input_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        exit(1)

    # Nummernschilder schwärzen
    image = blackout_license_plates_yolov5(image, model)

    # Gesichter verpixeln
    image = pixelate_faces(image)

    # Ergebnis speichern
    cv2.imwrite(output_path, image)
    print(f"Bild mit geschwärzten Nummernschildern und verpixelten Gesichtern gespeichert unter: {output_path}")
