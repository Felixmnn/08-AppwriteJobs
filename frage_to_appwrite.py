# 2_frage_to_appwrite.py

# Diese Funktion sendet die generierten Fragen an Appwrite (z. B. Datenbank).
# Input: Eine Liste von Fragen
# Output: Bestätigung der Speicherung oder Fehler
import json

import os

def frage_to_appwrite(fragen: list, databases,session_id,subject_id):
    """
    Sendet die generierten Fragen an Appwrite (z. B. zur Speicherung in einer Datenbank).
    Hier könnte man die Appwrite SDK verwenden, um Daten zu speichern.
    """
    # Appwrite Client initialisieren
    
    # Zugriff auf die Datenbank
    questionList =  []
    for frage in fragen:
        try:
            question = create_document(frage, databases,session_id,subject_id)
            newQuestion = {
                "id"    : question["$id"],
                "status": None
            }
            questionList.append(json.dumps(newQuestion))
        except Exception as e:
            print(f"Fehler beim Speichern der Frage: {e}")
    return questionList

def create_document(frage,databases,session_id,subject_id):
    document = databases.create_document(
        database_id="67c50ecf001b7baf5de3",  
        collection_id="67c54fc20037f246f948",    
        document_id="unique()",     
        data={
            "question": frage["question"],
            "answers": frage["answers"],
            "answerIndex": frage["answerIndex"],
            "public": frage["public"],
            "aiGenerated": True,
            "status": None,
            "tags": [],
            "sessionID": session_id,
            "subjectID": subject_id
        }
    )
    return document