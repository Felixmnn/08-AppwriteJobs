# 0_text_to_absatz.py

# Diese Funktion wird verwendet, um den extrahierten Text in Absätze zu unterteilen.
# Input: Ein langer Text (extrahiert aus der PDF)
# Output: Eine Liste von Absätzen

def text_to_absatz(text: str):
    """
    Teilt den extrahierten Text in Absätze auf.
    Hier könnte man zum Beispiel Text anhand von Zeilenumbrüchen oder
    spezifischen Regeln in Absätze unterteilen.
    """
    absätze = []
    copy_text = text    
    while len(copy_text) > 1500:
        letzter_zeilenumbruch = copy_text.rfind('\n', 0, 2000)
        if letzter_zeilenumbruch != -1:
            chunk = copy_text[:letzter_zeilenumbruch]
        else:
            chunk = copy_text[:2000]
        absätze.append(chunk)
        copy_text = copy_text[len(chunk):]
    if copy_text:
        absätze.append(copy_text)
    
    return absätze
