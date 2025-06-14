import cv2
import torch
import ssl
from ultralytics import YOLO

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

def pixelate_faces(image, model):
    # YOLOv8 gibt standardmäßig Ergebnisse in results.boxes
    # Bei YOLOv8: results.boxes.xyxy, results.boxes.conf, results.boxes.cls
    results = model(image)  # Bild übergeben

    # Annahme: 1. Bild im Batch (meist nur ein Bild)
    detections = results[0].boxes  # boxes Objekt mit xyxy, conf, cls

    for box in detections:
        x_min, y_min, x_max, y_max = map(int, box.xyxy[0].tolist())
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        # Gesichter mit Konfidenz > 0.5 pixeln
        if conf > 0.5:
            face = image[y_min:y_max, x_min:x_max]

            if face.size == 0:
                continue

            # Pixelate: Runterskalieren und wieder hochskalieren
            face = cv2.resize(face, (5, 5), interpolation=cv2.INTER_LINEAR)
            face = cv2.resize(face, (x_max - x_min, y_max - y_min), interpolation=cv2.INTER_NEAREST)
            image[y_min:y_max, x_min:x_max] = face

    return image

def complete(input_path):
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/output_blackout_pixelate.jpeg"
    model_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/Automatic-Number-Plate-Recognition-using-YOLOv5/Weights/best.pt"

    # YOLOv5 Modell laden (nur einmal)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    # Bild laden
    image = cv2.imread(input_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        exit(1)


    image_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/personen/20250614_144511.jpg.jpeg"
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/personen/output.jpeg"
    weights_path_face = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/yolov8n-face.pt"

    # YOLOv8 Modell laden (auch wenn Dateiname "yolov5s-face.pt" heißt, bitte sicherstellen, dass es ein YOLOv8-kompatibles Modell ist)
    model_face = YOLO(weights_path_face)

    

    image = pixelate_faces(image, model_face)
    cv2.imwrite(output_path, image)
    print(f"Bild mit verpixelten Gesichtern gespeichert: {output_path}")    

    # Nummernschilder schwärzen
    image = blackout_license_plates_yolov5(image, model)

    

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
    weights_path_face = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/yolov8n-face.pt"

    # YOLOv8 Modell laden (auch wenn Dateiname "yolov5s-face.pt" heißt, bitte sicherstellen, dass es ein YOLOv8-kompatibles Modell ist)
    model_face = YOLO(weights_path_face)
    image = pixelate_faces(image, model_face)

    # Ergebnis speichern
    cv2.imwrite(output_path, image)
    print(f"Bild mit geschwärzten Nummernschildern und verpixelten Gesichtern gespeichert unter: {output_path}")
