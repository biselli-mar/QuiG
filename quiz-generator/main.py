from langchain_community.llms import Ollama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain.chains.prompt_selector import ConditionalPromptSelector
from langchain_core.prompts import PromptTemplate
import re


# stream tokens as they are being generated
ollama_llm = Ollama(
    model="llama3",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
    format="json",

)

DEFAULT_LLAMA_SEARCH_PROMPT = PromptTemplate(
    input_variables=["text", "num_questions"],
    template="""<<SYS>> \n Du bist ein Assistent, der damit beauftragt ist, Quizfragen zu generieren.
    Du kannst nur auf Deutsch und im JSON-Format antworten, ohne Beisätze oder unnötige Informationen. \n\n
    Nutze das folgende Format: \n\n
    {{ "question": "Fragetext", \n
    "answer": "Antworttext" }} \n\n
    <</SYS>> \n\n 
    [INST] Generiere {num_questions} Quizfragen aus dem folgenden Text: \n\n {text} \n\n Fragen: \n\n
    [/INST]""",
)

DEFAULT_SEARCH_PROMPT = PromptTemplate(
    input_variables=["text", "num_questions"],
    template="""Du bist ein Assistent, der damit beauftragt ist, Quizfragen zu generieren. \
    Du kannst nur auf Deutsch und im JSON-Format antworten, ohne Beisätze oder unnötige Informationen. \n\n
    Nutze das folgende Format: \n\n
    {{ "question": "Fragetext", \n
    "answer": "Antworttext" }} \n\n
    Generiere {num_questions} Quizfragen aus dem folgenden Text: \n\n {text} \n\n Fragen:""",
)

QUESTION_PROMPT_SELECTOR = ConditionalPromptSelector(
    default_prompt=DEFAULT_SEARCH_PROMPT,
    conditionals=[(lambda llm: isinstance(ollama_llm, Ollama), DEFAULT_LLAMA_SEARCH_PROMPT)],
)

prompt = QUESTION_PROMPT_SELECTOR.get_prompt(ollama_llm)

# Create the LLM chain
llm_chain = prompt | ollama_llm


# Function to generate questions
def generate_questions(text, num_questions=5):
    response = (llm_chain.invoke({"text": text, "num_questions": num_questions}))
    return response


# Function to parse questions with a regex pattern
def parse_questions(generated_text):
    questions = []
    pattern = re.compile(r"Question: (.*?) Answer: (.*?)(?= Question:|$)", re.DOTALL)
    matches = pattern.findall(generated_text)
    for match in matches:
        question, answer = match
        questions.append({
            "question": question.strip(),
            "answer": answer.strip()
        })
    return questions


# Function to convert to GIFT format
def convert_to_gift(questions):
    gift_format = ""
    for q in questions:
        gift_format += str(q) + "\n"
    return gift_format
