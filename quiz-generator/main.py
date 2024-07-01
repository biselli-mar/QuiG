from llama_cpp import Llama, LlamaGrammar

sys_prompt = """
Du bist ein professioneller Quiz-Generator. Deine Aufgabe ist es, ein Quiz basierend auf dem gegebenen Kontext zu erstellen.
Der Kontext sind Folien aus einer Universitätsvorlesung. Einige können mathematische Gleichungen enthalten, die nicht korrekt extrahiert wurden. Verwende dein eigenes Wissen, um eventuelle Fehler im extrahierten Text anhand der Erklärung und des Kontexts der Gleichungen zu korrigieren. Du kannst auch eigene Beispiele zum Thema verwenden, um die Qualität des Quiz zu verbessern.

Deine Antwort sollte strikt dem folgenden Format folgen:
Frage: [Frage hier einfügen]
Optionen: [Antwortoptionen hier einfügen]
Richtige Antwort: [richtige Antwort hier einfügen]
Erklärung: [kurze Erklärung hier einfügen (optional)]

Der Kontext für diese Aufgabe ist wie folgt:

Einführung in die Statistik in der angewandten Informatik

Statistik ist ein wichtiges Werkzeug in der angewandten Informatik, das die Analyse und Interpretation von Daten 
ermöglicht, um Entscheidungsfindungen zu unterstützen und Algorithmen zu verbessern. Wichtige Konzepte

Deskriptive Statistik: Fasst Daten mit Maßzahlen wie Mittelwert, Median, Modus und Standardabweichung zusammen. Diese 
Werkzeuge helfen, Datenverteilungen und Variabilität zu verstehen, was für die Datenvorverarbeitung und explorative 
Datenanalyse unerlässlich ist. 
Inferenzstatistik: Beinhaltet das Treffen von Vorhersagen über eine Population 
basierend auf Stichprobendaten. Techniken wie Hypothesentests und Konfidenzintervalle werden verwendet, um Modelle 
und Algorithmen zu validieren.

Wahrscheinlichkeit: Misst die Wahrscheinlichkeit von Ereignissen und ist grundlegend für das maschinelle Lernen, 
um Modellvorhersagen und Unsicherheiten zu verstehen.

Regressionsanalyse: Untersucht Beziehungen zwischen Variablen. Lineare und logistische Regression werden häufig in 
der prädiktiven Modellierung und Merkmalsauswahl verwendet."""

schema = r'''
question-kv ::= "\"question\"" space ":" space string
options-kv ::= "\"options\"" space ":" space options
correct-answer-kv ::= "\"correct_answer\"" space ":" space string
explanation-kv ::= "\"explanation\"" space ":" space string
options ::= "[" space (string ("," space string)*)? "]" space
string ::= "\"" char* "\"" space
char ::= [^"\\\x7F\x00-\x1F] | [\\] (["\\bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
root ::= "{" space question-kv "," space options-kv "," space correct-answer-kv ( "," space ( explanation-kv ) )? "}" space
space ::= [ \t\n]?
'''


def get_prompt(question: str, system_prompt: str) -> str:
    texts = [f'[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n', f'{question.strip()} [/INST]']
    return ''.join(texts)


prompt = get_prompt("Statistics", sys_prompt)
print("Prompt:\n" + prompt)

grammar = LlamaGrammar.from_string(grammar=schema, verbose=True)
print(grammar)
client = Llama(
    model_path="./models/zephyr-7b-beta.Q8_0.gguf",
    temperature=0.4,  # 0 is more deterministic (focused), 1 is more random (creative)
    n_ctx=2048,
    n_threads=12,
    last_n_tokens_size=70,
    n_gpu_layers=30
)

answer = client(
    prompt,
    grammar=grammar,
    stream=False,
    # temperature=0.4,
    top_p=0.95,
    top_k=50,
    repeat_penalty=1.7,
    max_tokens=2000,
)
print(answer)
