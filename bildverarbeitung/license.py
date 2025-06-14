import cv2  # Importiert die OpenCV-Bibliothek für Bildverarbeitung
import easyocr  # Importiert EasyOCR für Texterkennung in Bildern
import ssl  # Importiert das ssl-Modul zur Anpassung von SSL-Kontexten

# Setzt den SSL-Kontext auf "unverified", um mögliche SSL-Fehler zu umgehen
ssl._create_default_https_context = ssl._create_unverified_context

def blur_license_plate(image_path, output_path):
    # Lade das Bild vom angegebenen Pfad
    image = cv2.imread(image_path)
    # Überprüft, ob das Bild erfolgreich geladen wurde
    if image is None:
        print("Fehler: Bild konnte nicht geladen werden.")
        return

    # Initialisiert den EasyOCR-Reader für deutsche Sprache, ohne GPU
    reader = easyocr.Reader(['de'], gpu=False)

    # Führt Texterkennung auf dem Bild durch
    results = reader.readtext(image)

    # Iteriert über alle erkannten Textbereiche
    for (bbox, text, prob) in results:
        # Prüft, ob der erkannte Text wie ein deutsches Kennzeichen aussieht
        if prob > 0.5 and 5 <= len(text) <= 10:
            # Extrahiert die Eckpunkte der Bounding Box
            (top_left, top_right, bottom_right, bottom_left) = bbox
            # Wandelt die Koordinaten in ganze Zahlen um
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            # Zeichnet ein schwarzes Rechteck über das erkannte Kennzeichen
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 0), -1)

    # Speichert das bearbeitete Bild unter dem angegebenen Pfad
    cv2.imwrite(output_path, image)
    print(f"Das bearbeitete Bild wurde gespeichert unter: {output_path}")

# Führt den folgenden Block nur aus, wenn das Skript direkt gestartet wird
if __name__ == "__main__":
    # Fragt den Benutzer nach dem Pfad zum Eingabebild
    input_path = input("Pfad zum Eingabebild: ")
    # Fragt den Benutzer nach dem Pfad zum Ausgabebild
    output_path = input("Pfad zum Ausgabebild: ")
    # Ruft die Funktion zum Verpixeln des Kennzeichens auf
    blur_license_plate(input_path, output_path)