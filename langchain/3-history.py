from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        (
            "user",
            "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation",
        ),
    ]
)

# Invoke chain with RAG context

llm = Ollama(model="mistral")

## Load page content
loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
docs = loader.load()

## Vector store things
embeddings = OllamaEmbeddings(model="nomic-embed-text")
text_splitter = RecursiveCharacterTextSplitter()
split_documents = text_splitter.split_documents(docs)
vector_store = FAISS.from_documents(split_documents, embeddings)
retriever = vector_store.as_retriever()

# history
retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
chat_history = [
    HumanMessage(content="Can LangSmith help test my LLM applications?"),
    AIMessage(content="Yes!"),
]

document_chain = create_stuff_documents_chain(llm, prompt)
# TODO: doesn't work with retriever_chain instead of retriever
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke(
    {"chat_history": chat_history, "input": "Tell me how?"}
)

print(response["answer"])
