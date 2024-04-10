import os
import re
import pandas as pd
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader, IMSDbLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_secret():
    if load_dotenv():
        print("Environment variables loaded successfully.")
        return os.getenv('OPENAI_TOKEN')
    else:
        print("Failed to load .env file.")
        return None


def create_rag_chain():
    os.environ["OPENAI_API_KEY"] = get_secret()
    llm = ChatOpenAI(model="gpt-4-turbo")
    #llm = ChatOpenAI(model="gpt-3.5-turbo")
    # Loading a script from IMSDb
    loader = IMSDbLoader("https://imsdb.com/scripts/Hunt-for-Red-October,-The.html")
    docs = loader.load()
    # Splitting text and creating vectorstore
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    # Setting up retriever and prompt
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    # Creating Rag Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def question_rag_chain(rag_chain):
    # Example invocations
    questions = [
        "What is the protagonist of this movie?",
        "How many characters die in this movie?",
        "What are the main themes of this movie?",
        "How many lines are there in the script?",
        "What is the first date mentioned in the script?",
        "Count the number of scenes in this script",
        "What is Ramius' first name"
    ]
    for question in questions:
        print(rag_chain.invoke(question))


def main():
    rag_chain = create_rag_chain()
    question_rag_chain(rag_chain)