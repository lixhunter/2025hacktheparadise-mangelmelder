import cv2
import ssl
from ultralytics import YOLO

ssl._create_default_https_context = ssl._create_unverified_context

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


if __name__ == "__main__":
    image_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/personen/20250614_144511.jpg.jpeg"
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/personen/output.jpeg"
    weights_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/yolov8n-face.pt"

    # YOLOv8 Modell laden (auch wenn Dateiname "yolov5s-face.pt" heißt, bitte sicherstellen, dass es ein YOLOv8-kompatibles Modell ist)
    model = YOLO(weights_path)

    image = cv2.imread(image_path)
    if image is None:
        print("Bild konnte nicht geladen werden.")
        exit(1)

    image = pixelate_faces(image, model)
    cv2.imwrite(output_path, image)
    print(f"Bild mit verpixelten Gesichtern gespeichert: {output_path}")
