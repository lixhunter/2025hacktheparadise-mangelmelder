import cv2
import easyocr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def blur_license_plate(image_path, output_path):
    # Lade das Bild
    image = cv2.imread(image_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        return

    # Initialisiere EasyOCR
    reader = easyocr.Reader(['de'], gpu=False)

    # Führe Texterkennung durch
    results = reader.readtext(image)

    # Debug: Alle erkannten Texte ausgeben
    for (bbox, text, prob) in results:
        print(f"Erkannt: {text}, Wahrscheinlichkeit: {prob}, Box: {bbox}")

    # Iteriere über die erkannten Texte
    for (bbox, text, prob) in results:
        # Lockere Filterbedingungen
        if prob > 0.3 and 3 <= len(text) <= 12:
            # Eckpunkte der Bounding Box extrahieren
            pts = [tuple(map(int, point)) for point in bbox]
            x_coords = [pt[0] for pt in pts]
            y_coords = [pt[1] for pt in pts]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            # Bereich ausschneiden und blurren
            roi = image[y_min:y_max, x_min:x_max]
            if roi.size == 0:
                continue
            blurred_roi = cv2.GaussianBlur(roi, (31, 31), 0)
            image[y_min:y_max, x_min:x_max] = blurred_roi

    # Speichere das bearbeitete Bild
    cv2.imwrite(output_path, image)
    print(f"Das bearbeitete Bild wurde gespeichert unter: {output_path}")

if __name__ == "__main__":
    # Relative Pfade
    input_path = "2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/22c0d9a3-605e-41c8-a7ba-2c6712e368e3.jpeg"
    output_path = "2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/22c0d9a3-605e-41c8-a7ba-2c6712e368e3_blur.jpeg"