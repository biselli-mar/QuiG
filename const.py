import os

APP_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PERSISTENCE_PATH = os.path.join(APP_DIRECTORY, "persist")
RECENT_SUMMARIES_PATH = os.path.join(PERSISTENCE_PATH, "recent_summaries.json")

map_prompt_template = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}
                        
Du bist ein Lehrer und sollst anhand der Dokumenten die Hauptthemen und wichtigsten Details identifizieren.
Gib die Inhalte der Dokumente kurzgefasst aber so genau wie möglich wieder.
Achte darauf, Formeln, Fakten und Definitionen wortgetreu zu übernehmen. Ignoriere Beispiele und Übungsaufgaben komplett.

Hilfreiche Antwort:"""

map_prompt_template_limited = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}

Identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
Übernehme nur die Inhalte, die zu dieser Prompt passen:

{summary_content}

Du bist ein Lehrer und sollst anhand der Dokumenten die Hauptthemen und wichtigsten Details identifizieren.
Gib die Inhalte der Dokumente kurzgefasst aber so genau wie möglich wieder.
Achte darauf, Formeln, Fakten und Definitionen wortgetreu zu übernehmen. Ignoriere Beispiele und Übungsaufgaben komplett.

Hilfreiche Antwort:"""


reduce_prompt_template = """Im Folgenden befindet sich eine Reihe von Zusammenfassungen:

{text}

Du bist ein Lehrer und sollst mithilfe der Zusammenfassungen eine endgültige, alles umfassende Zusammenfassung erstellen.
Gib die Inhalte der Zusammenfassungen kurzgefasst aber so genau wie möglich wieder.
Achte darauf, Formeln, Fakten und Definitionen wortgetreu zu übernehmen. Ignoriere Beispiele und Übungsaufgaben komplett.


Hilfreiche Antwort:"""

reduce_prompt_template_limited = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}

Diese wurden anhand folgender Prompt zusammengefasst:

{summary_content}

Du bist ein Lehrer und sollst mithilfe der Zusammenfassungen eine endgültige, alles umfassende Zusammenfassung erstellen.
Gib die Inhalte der Zusammenfassungen kurzgefasst aber so genau wie möglich wieder.
Achte darauf, Formeln, Fakten und Definitionen wortgetreu zu übernehmen. Ignoriere Beispiele und Übungsaufgaben komplett.

Hilfreiche Antwort:"""

generate_query = """Generiere {num_questions} Quizfrage(n) aus dem folgenden Textauszug einer Vorlesung.
Die Fragen sollten auf den Hauptthemen und wichtigen Details basieren und Studenten helfen,
ihr Wissen zu testen und zu vertiefen.
                    
{text}"""

generate_query_limited = """Generiere {num_questions} Quizfrage(n) aus dem folgenden Textauszug einer Vorlesung.
Die Fragen sollten auf den Hauptthemen und wichtigen Details basieren und Studenten helfen,
ihr Wissen zu testen und zu vertiefen. Achte besonders darauf, nur Fragen zu generieren, die zu dieser Prompt passen:

{summary_content}

Folgender Textauszug:
                    
{text}"""

system_prompt = """You are an assistant tasked with generating quiz questions. You can only respond in the language
used in the input text, without clauses or unnecessary information.

{format_instructions}"""

# Config for chunking text with MarkdownTextSplitter
CHUNK_SIZE = 20000
CHUNK_OVERLAP = 5000

# load_summarize_chain: max. number of tokens to group documents into
MAX_TOKENS = 5000
