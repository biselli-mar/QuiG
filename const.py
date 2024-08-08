map_prompt_template = """Im Folgenden befindet sich eine Reihe von Dokumenten:

{text}
                        
Identifiziere anhand der Liste von Dokumenten die Hauptthemen und wichtige Details.
Achte darauf, Beispiele und Definitionen wortgetreu zu übernehmen.

Hilfreiche Antwort:"""

reduce_prompt_template = """Im Folgenden befindet sich eine Reihe von Zusammenfassungen:

{text}

Nutze die Zusammenfassungen, um sie zu einer endgültigen, 
alles umfassenden Zusammenfassung zu kombinieren. 
Achte darauf, Beispiele und Definitionen wortgetreu zu übernehmen.

Hilfreiche Antwort:"""

generate_query = """Generiere {num_questions} Quizfrage(n) aus dem folgenden Textauszug einer Vorlesung.
Die Fragen sollten auf den Hauptthemen und wichtigen Details basieren und Studenten helfen,
ihr Wissen zu testen und zu vertiefen.
                    
{text}"""

system_prompt = """You are an assistant tasked with generating quiz questions. You can only respond in the language
used in the input text, without clauses or unnecessary information.

{format_instructions}"""

# Variables for chunking text with MarkdownTextSplitter
CHUNK_SIZE = 20000
CHUNK_OVERLAP = 5000

# load_summarize_chain: max. number of tokens to group documents into
MAX_TOKENS = 5000
