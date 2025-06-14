import cv2
import easyocr
import ssl
import numpy as np

# SSL-Kontext anpassen, falls nötig (z. B. macOS mit HTTPS-Problemen)
ssl._create_default_https_context = ssl._create_unverified_context

def blur_license_plate(image_path, output_path):
    # Lade das Bild
    image = cv2.imread(image_path)
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        return

    # Initialisiere EasyOCR mit deutscher Sprache und Textrichtungserkennung
    reader = easyocr.Reader(['de'], gpu=False)

    # Führe Texterkennung durch, aktiviere Erkennung der Textausrichtung
    results = reader.readtext(image, detail=1, paragraph=False)

    # Debug: Alle erkannten Texte ausgeben
    for (bbox, text, prob) in results:
        print(f"Erkannt: {text}, Wahrscheinlichkeit: {prob:.2f}, Box: {bbox}")

    # Iteriere über die erkannten Texte
    for (bbox, text, prob) in results:
        # Lockere Filterbedingungen (z. B. für Kennzeichen)
        if prob > 0.3 and 3 <= len(text) <= 12:
            # Eckpunkte der Bounding Box extrahieren (Polygon)
            pts = np.array(bbox).astype(int)

            # Fülle die Region als Polygon mit schwarzer Farbe
            cv2.fillPoly(image, [pts], color=(0, 0, 0))

    # Speichere das bearbeitete Bild
    cv2.imwrite(output_path, image)
    print(f"Das bearbeitete Bild wurde gespeichert unter: {output_path}")

if __name__ == "__main__":
    # Eingabe- und Ausgabe-Pfade
    input_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/22c0d9a3-605e-41c8-a7ba-2c6712e368e3_blur.jpeg"
    output_path = "/Users/aschulte-kroll/Downloads/HackTheParadise/2025hacktheparadise-mangelmelder/bildverarbeitung/fahrzeuge/output_blur.jpeg"
    
    blur_license_plate(input_path, output_path)
