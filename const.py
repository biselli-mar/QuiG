import os

APP_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
PERSISTENCE_PATH = os.path.join(APP_DIRECTORY, "persist")
RECENT_SUMMARIES_PATH = os.path.join(PERSISTENCE_PATH, "recent_summaries.json")

map_prompt_template = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}
                        
Identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
Achte darauf, Beispiele und Definitionen wortgetreu zu übernehmen.

Hilfreiche Antwort:"""

map_prompt_template_limited = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}

Identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
Übernehme nur die Inhalte, die zu dieser Prompt passen:

{summary_content}

Lasse irrelevante Informationen weg; wenn es sein muss, antworte gar nichts.
Achte darauf alle relevanten Definitionen exakt wortgetreu zu übernehmen und sei dabei dafür
umso umfangreicher.

Hilfreiche Antwort:"""


reduce_prompt_template = """Im Folgenden befindet sich eine Reihe von Zusammenfassungen:

{text}

Nutze die Zusammenfassungen, um sie zu einer endgültigen, 
alles umfassenden Zusammenfassung zu kombinieren. 
Achte darauf, Beispiele und Definitionen exakt wortgetreu zu übernehmen.

Hilfreiche Antwort:"""

reduce_prompt_template_limited = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}

Diese wurden anhand folgender Prompt zusammengefasst:

{summary_content}

Prüfe nochmal, ob alle Informationen zu dieser Prompt passen.
Nutze die Zusammenfassungen, um sie zu einer endgültigen,
alles umfassenden Zusammenfassung zu kombinieren.
Lasse irrelevante Informationen weg; wenn es sein muss, antworte gar nichts.
Achte darauf alle relevanten Definitionen exakt wortgetreu zu übernehmen.

Hilfreiche Antwort:"""

generate_query = """Generiere {num_questions} Quizfrage(n) aus dem folgenden Textauszug einer Vorlesung.
Die Fragen sollten auf den Hauptthemen und wichtigen Details basieren und Studenten helfen,
ihr Wissen zu testen und zu vertiefen.
                    
{text}"""

system_prompt = """You are an assistant tasked with generating quiz questions. You can only respond in the language
used in the input text, without clauses or unnecessary information.

{format_instructions}"""

# Config for chunking text with MarkdownTextSplitter
CHUNK_SIZE = 20000
CHUNK_OVERLAP = 5000

# load_summarize_chain: max. number of tokens to group documents into
MAX_TOKENS = 5000
