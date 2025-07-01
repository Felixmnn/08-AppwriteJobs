from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.services.databases import Databases
from appwrite.services.storage import Storage
import fitz
import os
import json
import requests
from text_to_absatz import text_to_absatz
from abstatz_to_frage import absatz_to_frage
from frage_to_appwrite import frage_to_appwrite
from dotenv import load_dotenv
import tempfile
from PIL import Image
import pytesseract
import io


load_dotenv()

def get_jobs(client):
    databases = Databases(client)
    documents = databases.list_documents("67c50ecf001b7baf5de3", "681dd825000e6990368a")
    return documents


# Diese Appwrite-Funktion wird jedes Mal ausgeführt, wenn sie aufgerufen wird
def document_to_questions(sessionID, subjectID, documentID,client):
    apiKey = os.getenv("OPNEAI_API_KEY")
    databases = Databases(client)
    storage = Storage(client)

    try:
        # 1. Schritt: Text aus einer PDF-Datei extrahieren
        file_bytes = storage.get_file_download("67dc11e000003ae76023", documentID)
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp_pdf:
            tmp_pdf.write(file_bytes)
            tmp_pdf.flush()  # WICHTIG: Schreibpuffer leeren
            temp_pdf_name = tmp_pdf.name

        text = ""
        pdf_document = fitz.open(temp_pdf_name)

        for page in pdf_document:
            text += page.get_text()

        # Wenn OCR nötig ist
        if len(text.strip()) < 100:
            print("Wenig extrahierbarer Text gefunden – OCR wird gestartet.")
            text = ""  # Vorherigen Text löschen

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                page_text = pytesseract.image_to_string(img, lang='deu')
                text += page_text
                print(f"Seite {page_num + 1} verarbeitet.")

        pdf_document.close()

        # Lösche die temporäre Datei manuell
        os.remove(temp_pdf_name)
        
        
        # 2. Schritt: Text in Absätze unterteilen
        print("Unterteile den Text in Absätze...")
        absätze = text_to_absatz(text)
        print(f"Absätze: {absätze}")
        
        # 3. Schritt: Absätze in Fragen umwandeln
        print("Wandeln Absätze in Fragen um...")
        fragen = absatz_to_frage(absätze,apiKey)

        print(f"Generierte Fragen: {fragen}")
        
        # 4. Schritt: Fragen in Appwrite speichern
        print("Speichern der Fragen in Appwrite...")
        questionList = frage_to_appwrite(fragen, databases, sessionID, subjectID)

        return questionList
        
        # Erfolgreiche Antwort
        
      
    
    except Exception as e:
        print(f"General error: {str(e)}")

    # Wenn keine "ping"-Anfrage, gebe eine JSON-Antwort zurück

    
    

#document_to_questions("f663c082-5d0f-4a3c-9a7d-feab105563e6", "681de08cbec675bba6b8", "67fc840f002c06f94732")


def main ():

    client = (
        Client()
        .set_endpoint("https://cloud.appwrite.io/v1")  # Setze den Endpunkt
        .set_project(os.getenv("PROJECT_ID"))  # Setze die Projekt-ID
        .set_key(os.getenv("APPWRITE_API_KEY"))  # Setze den API-Schlüssel
    )

    # 1. Get Job
    print("Get Job", get_jobs(client))
    # 2. Do Job
    for job in get_jobs(client)["documents"]:
        sessionID = job["sessionID"]
        subjectID = job["subjectID"]
        documentID = job["databucketID"]
        questionList = document_to_questions(sessionID, subjectID, documentID, client)
        # 3. Success delete Job
        databases = Databases(client)
        databases.delete_document("67c50ecf001b7baf5de3", "681dd825000e6990368a", job["$id"])
       # 4. Update Session
        module = databases.get_document("67c50ecf001b7baf5de3", "67c54fcb0017adfea948", subjectID)
        print("Module", module)
        Sessions = module["sessions"]  # Direktes Array verwenden
        parsedSessions = []
        for session in Sessions:
            parsedSessions.append(json.loads(session))
        print("Parsed Sessions", parsedSessions)

        for session in parsedSessions:
            if session["id"] == sessionID:  # Verwende hier "id" statt "sessionID"
                print("Match found")
                print(session["tags"])
                session["tags"] = "JOB-DONE"       # Überschreibe tags mit einem leeren Array
                print("Session", session)
                break
        
        # Jedes Feld im Array einzeln in einen JSON-String umwandeln
        sessions_serialized = []
        for session in parsedSessions:
            session_serialized = json.dumps(session)
            sessions_serialized.append(session_serialized)
        print("Serialized Sessions", sessions_serialized)

        oldModule = databases.get_document("67c50ecf001b7baf5de3", "67c54fcb0017adfea948", subjectID)
        
        databases.update_document(
            "67c50ecf001b7baf5de3",
            "67c54fcb0017adfea948",
            subjectID,
            {
                "sessions": sessions_serialized,  # Das finale JSON-Array
                "questions": len(questionList) + oldModule["questions"],  # Anzahl der Fragen
                "questionList": oldModule["questionList"] + questionList if "questionList" in oldModule else questionList

            }
        )
        print("Job Done Carry On 🫡")
    

main()
