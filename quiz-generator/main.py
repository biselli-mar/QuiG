from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import MarkdownTextSplitter
from langchain.chains.summarize import load_summarize_chain
import re
import os
from Quiz import Quiz

os.environ["OPENAI_API_KEY"] = "x"

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

# pipe = pipeline(model=model_id,
#                 task="text-generation",
#                 max_new_tokens=500)
#                 # top_k=50,
#                 # temperature=0.1)
# huggingface_llm = HuggingFacePipeline(pipeline=pipe, model_id=model_id)

llm = ChatOpenAI(
    model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    base_url="http://localhost:1234/v1/",
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

generate_questions_prompt = PromptTemplate(input_variables=["text", "num_questions"],
                                           template="Generiere {num_questions} Quizfragen aus dem folgenden Text: \n\n "
                                                    "{text} \n\n "
                                                    "Fragen:")

structured_llm = llm.with_structured_output(Quiz)
# Create the LLM chain
question_chain = generate_questions_prompt | structured_llm


def split_text(text):
    splitter = MarkdownTextSplitter(
        chunk_size=1000,
        chunk_overlap=200)
    docs = splitter.create_documents([text])
    print("Text split into", len(docs), "documents.")
    return docs


# Function to generate questions
def generate_questions(text, num_questions=5):
    print("Splitting text...")
    docs = split_text(text)

    # text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    #     chunk_size=500, chunk_overlap=0
    # )
    # split_docs = text_splitter.split_documents(docs)

    # print("Text split into", len(docs), "documents.")

    sum_chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
    # result = chain.invoke(docs)

    print("Invoking map-reduce chain...")
    result = sum_chain.invoke(docs)
    print("Map-reduce chain finished.")

    print("Result:", result)

    # add parallel processing
    # https://github.com/langchain-ai/langchain/discussions/21009

    response = (question_chain.invoke({"text": result, "num_questions": num_questions}))
    return response


# # Function to parse questions with a regex pattern
# def parse_questions(generated_text):
#     questions = []
#     pattern = re.compile(r"Question: (.*?) Answer: (.*?)(?= Question:|$)", re.DOTALL)
#     matches = pattern.findall(generated_text)
#     for match in matches:
#         question, answer = match
#         questions.append({
#             "question": question.strip(),
#             "answer": answer.strip()
#         })
#     return questions


# Function to convert to GIFT format
def convert_to_gift(questions):
    gift_format = ""
    for q in questions:
        gift_format += str(q) + "\n\n"
    return gift_format
