map_prompt_template = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}
                        
Identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
Achte darauf, Beispiele und Definitionen wortgetreu zu übernehmen.

Hilfreiche Antwort:"""

reduce_prompt_template = """Im Folgenden befindet sich eine Reihe von Zusammenfassungen:

{text}

Nutze die Zusammenfassungen, um sie zu einer endgültigen, 
alles umfassenden Zusammenfassung zu kombinieren.

Hilfreiche Antwort:"""

generate_query = """Generiere {num_questions} Quizfragen aus dem folgenden Text:
                    
{text}"""

# Variables for chunking text with MarkdownTextSplitter
CHUNK_SIZE = 30000
CHUNK_OVERLAP = 1000

# load_summarize_chain: max. number of tokens to group documents into
MAX_TOKENS = 5000
