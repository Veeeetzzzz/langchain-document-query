import io
import csv
import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from langchain.document_loaders import TextLoader, PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders.csv_loader import CSVLoader
from pydantic import BaseModel

class StringIODocument(BaseModel):
    page_content: str
    metadata: dict = {}

class CSVDocument(BaseModel):
    page_content: str
    metadata: dict = {}

class StringIOTextLoader:
    def __init__(self, string_io):
        self.string_io = string_io

    def load(self):
        return [StringIODocument(page_content=self.string_io.getvalue())]

class StringIOCSVLoader(CSVLoader):
    def __init__(self, string_io):
        self.string_io = string_io

    def load(self):
        documents = []
        with self.string_io as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            for row in reader:
                content = " ".join([f"{header}: {value}" for header, value in zip(headers, row)])
                documents.append(CSVDocument(page_content=content))
        return documents

class PDFLoader:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def load(self):
        loader = PyMuPDFLoader(self.pdf_file)
        return loader.load()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_query():
    content = request.files.get("content")
    query = request.form["query"]
    file_ext = request.form["file_ext"]
    pdf_file = request.files.get("upload-pdf")

    if not query or not file_ext:
        return jsonify({"error": "Invalid input."})

    if file_ext == ".txt":
        loader = StringIOTextLoader(io.StringIO(content.read().decode("utf-8")))
    elif file_ext == ".csv":
        loader = StringIOCSVLoader(io.StringIO(content.read().decode("utf-8")))
    elif pdf_file:
        pdf_filename = secure_filename(pdf_file.filename)
        pdf_file.save(pdf_filename)
        loader = PDFLoader(pdf_filename)
    else:
        return jsonify({"error": "Unsupported file type."})
        
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(texts, embeddings)
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 1}))

    response = qa.run(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
