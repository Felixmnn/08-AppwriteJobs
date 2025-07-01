from openai import OpenAI
import json

# 1_abstatz_to_frage.py

# Diese Funktion generiert Fragen basierend auf den Absätzen des Textes.
# Input: Eine Liste von Absätzen
# Output: Eine Liste von Fragen

def absatz_to_frage(absätze: list, api_key: str):
    fragen = []
    """
    Wandelt Absätze in Fragen um.
    Hier könnte man eine einfache Logik oder ein Modell verwenden, um Fragen zu generieren.
    """
    for absatz in absätze:
        try:
            # Anfrage an GPT-3 (oder GPT-4) formulieren
            anfrage = f"""
            Erstelle auf Basis dieses Textes {absatz} so viele Fragen, dass der gesamte Text abgedeckt ist.
            Die Fragen sollen dabei als JSON-Array zurückgegeben werden. Es soll immer 4 Antworten geben, 
            wobei die Anzahl der richtigen Antworten >= 1 ist. Die Struktur der Fragen soll dabei wie folgt aussehen:
            [
                {{
                    "question": "DIE FRAGE",
                    "answers": ["EINE ANTWORT", "NOCH EINE ANTWORT", "UND NOCH EINE ANTWORT", ...],
                    "answerIndex": [0, 1, 2, ...],
                    "public": false,
                    "aiGenerated": true,
                    "status": null,
                    "tags": [],
                    "sessionID": null,
                    "subjectID": null
                }}
            ]
            Dabei sollen die Frage sowie die einzlenen Antworten nie 190 Zeichen überschreiten.
            """
            # Anfrage an OpenAI API senden
            response = createOpenAiRequest(anfrage, api_key)
            cleaned_response = clean_response(response)
            try:
                parsed_response = json.loads(cleaned_response)
                for question in parsed_response:
                    fragen.append(question)
            except json.JSONDecodeError as e:
                print(f"Fehler beim Parsen der Antwort: {e}")
                continue           
            

        except Exception as e:
            print(f"Fehler beim Generieren der Frage: {e}")
            continue

    return fragen


def createOpenAiRequest (anfrage,api_key): 
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": anfrage
        }
    ]
)

    return(completion.choices[0].message.content)

def clean_response(response: str):
    """
    Entfernt alles vor dem ersten '[' und nach dem letzten ']'.
    Diese Funktion stellt sicher, dass nur der JSON-Teil des Textes übrig bleibt.
    """
    start_index = response.find('[')  # Finde den Index des ersten '['
    end_index = response.rfind(']')   # Finde den Index des letzten ']'

    if start_index != -1 and end_index != -1 and start_index < end_index:
        # Extrahiere den Text zwischen den ersten '[' und dem letzten ']'
        cleaned_response = response[start_index:end_index+1]
        return cleaned_response
    else:
        # Falls kein gültiger JSON-Bereich gefunden wurde, gib den Originaltext zurück
        print("Kein gültiger JSON-Bereich gefunden.")
        return response