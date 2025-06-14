import requests
import json

def generate_with_llama3(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt
    }

    response = requests.post(url, json=payload, stream=True)
    output = ""

    for line in response.iter_lines():
        if line:
            try:
                json_data = json.loads(line.decode("utf-8"))
                output += json_data.get("response", "")
            except json.JSONDecodeError as e:
                print(f"Fehler beim Parsen: {e}")

    return output  # oder return output, je nach Bedarf

if __name__ == "__main__":
  print(generate_with_llama3("Hello, world!"))
