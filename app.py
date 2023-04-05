import io
import csv
from flask import Flask, render_template, request, jsonify
from langchain.document_loaders import TextLoader
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

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_query():
    content = request.form["content"]
    query = request.form["query"]
    file_ext = request.form["file_ext"]

    if not content or not query or not file_ext:
        return jsonify({"error": "Invalid input."})

    if file_ext == ".txt":
        loader = StringIOTextLoader(io.StringIO(content))
    elif file_ext == ".csv":
        loader = StringIOCSVLoader(io.StringIO(content))
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