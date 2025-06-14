import cv2
import torch
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def blur_license_plates_yolov5(image_path, output_path, model_path):
    # Lade vortrainiertes YOLOv5-Modell
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    
    # Bild laden
    image = cv2.imread(image_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        return
    
    # Modell auf Bild anwenden (Erkennung)
    results = model(image)

    # Ergebnisse als DataFrame bekommen (xmin, ymin, xmax, ymax, confidence, class, name)
    detections = results.pandas().xyxy[0]

    for idx, row in detections.iterrows():
        # Nur Nummernschilder (Klasse 0 oder Name 'license plate' prüfen)
        if row['name'] == 'license plate' or row['class'] == 0:
            x_min, y_min, x_max, y_max = map(int, [row['xmin'], row['ymin'], row['xmax'], row['ymax']])
            # Rechteck schwärzen
            image[y_min:y_max, x_min:x_max] = 0

    # Bild speichern
    cv2.imwrite(output_path, image)
    print(f"Bearbeitetes Bild gespeichert unter: {output_path}")

if __name__ == "__main__":
    input_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/IMG_5240.jpeg"
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/output_blur.jpeg"
    model_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/Automatic-Number-Plate-Recognition-using-YOLOv5/Weights/best.pt"  # Pfad zum heruntergeladenen oder trainierten Modell

    blur_license_plates_yolov5(input_path, output_path, model_path)
