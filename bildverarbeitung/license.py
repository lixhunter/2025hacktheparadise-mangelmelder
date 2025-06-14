import cv2
import easyocr

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

    # Iteriere über die erkannten Texte
    for (bbox, text, prob) in results:
        # Überprüfe, ob der erkannte Text wie ein deutsches Kennzeichen aussieht
        if prob > 0.5 and 5 <= len(text) <= 10:
            # Extrahiere die Bounding Box
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            # Zeichne ein schwarzes Rechteck über das Kennzeichen
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), -1)

    # Speichere das bearbeitete Bild
    cv2.imwrite(output_path, image)
    print(f"Das bearbeitete Bild wurde gespeichert unter: {output_path}")

# Beispielaufruf
if __name__ == "__main__":
    input_path = input("Pfad zum Eingabebild: ")
    output_path = input("Pfad zum Ausgabebild: ")
    blur_license_plate(input_path, output_path)
