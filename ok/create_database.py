from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import os
import shutil
from dotenv import dotenv_values

CHROMA_PATH = "chroma"
DATA_PATH = "ok/data/books"
api_key = dotenv_values(".env").get("OPENAI_API_KEY")


def generate_data_store():
    chunks = split_text()
    save_to_chroma(chunks)


def split_text():
    from langchain.text_splitter import CharacterTextSplitter
    from langchain_community.document_loaders import TextLoader

    file_path = "ok/data/books/README.md"
    text_splitter = CharacterTextSplitter()
    loader = TextLoader(file_path)
    loader.load()

    return loader.load_and_split(text_splitter=text_splitter)


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(openai_api_key=api_key), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    generate_data_store()
