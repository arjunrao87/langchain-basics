from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

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

## Prompt construction
prompt = ChatPromptTemplate.from_template(
    """
            Answer the following question only based on the given context
                                                    
            <context>
            {context}
            </context>
                                                    
            Question: {input}
"""
)

## Retrieve context from vector store
docs_chain = create_stuff_documents_chain(llm, prompt)
retriever = vector_store.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, docs_chain)

## Winner winner chicken dinner
response = retrieval_chain.invoke({"input": "how can langsmith help with testing?"})
print(":::ROUND 2:::")
print(response["answer"])
