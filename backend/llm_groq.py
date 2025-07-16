import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)
# embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")


os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

base_dir = os.path.join(os.path.dirname(__file__), "..", "lessons_faiss")
base_dir = os.path.abspath(base_dir) 

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def get_all_messages(x):
    return " ".join(msg.content for msg in x["messages"])

def build_rag_chain(file_name: str): 
    path = os.path.join(base_dir, file_name)
    vectorstore = FAISS.load_local(
        folder_path=path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    print(f"Vectorstore loaded from: {path}")

    prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are a Python programming tutor. Only answer questions if the provided <context> is relevant. 
    If the question is not related to the context, say "Sorry, I can't only answer questions out of the lessons."

    <context>
    {context}
    </context>
    """),
        MessagesPlaceholder(variable_name="messages")
    ])

    # Ambil context dari pertanyaan terakhir
    rag_chain = (
        RunnablePassthrough.assign(
            context=lambda x: retriever.invoke(get_all_messages(x))
        )
        | prompt
        | llm
    )

    print(f"RAG chain built for: {file_name}")

    rag_with_memory = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="messages"
    )

    return rag_with_memory

# def get_rag_response(user_input: str) -> str:
#     config = {"configurable": {"session_id": "chat-rag-ui"}}
#     response = rag_with_memory.invoke(
#         {"messages": [HumanMessage(content=user_input)]},
#         config=config
#     )
#     return response.content

# response = rag_with_memory.invoke(
#     {
#         "messages": [HumanMessage(content="Halo, nama aku Fikry. Belajar apa kita di materi ini?")]
#     },
#     config=config
# )

# print("🤖", response.content)

# ⌨️ Percakapan 2
# response = rag_with_memory.invoke(
#     {"messages": [HumanMessage(content="Bisa kasih contoh penggunaannya?")]},
#     config=config
# )
# print("🤖", response.content)
# # ⌨️ Percakapan 2
# response = rag_with_memory.invoke(
#     {"messages": [HumanMessage(content="""
# if:
# print("")
                               
# itu adalah code yang aku tulis, tetapi terdapat error ini:
                               

#   Cell In[21],   line 1
#     if:
#       ^
# SyntaxError: invalid syntax
                               
# """)]},
#     config=config
# )
# print("🤖", response.content)