import csv, io
from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename

from langchain.agents import AgentExecutor, create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader, PyMuPDFLoader, CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
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

class PDFLoader:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file

    def load(self):
        loader = PyMuPDFLoader(self.pdf_file)
        return loader.load()
    
@app.route("/")
def home():
    return render_template("index.html")    

@app.route("/ask", methods=["POST"])
def ask_query():
    content = request.files.get("content")
    query = request.form["query"]
    file_ext = request.form["file_ext"]
    pdf_file = request.files.get("upload-pdf")
    db_file = request.files.get("upload-db")

    if not query:
        return jsonify({"error": "Invalid input."})

    if file_ext in [".txt", ".csv"]:
        if file_ext == ".txt":
            loader = StringIOTextLoader(io.StringIO(content.read().decode("utf-8")))
        elif file_ext == ".csv":
            loader = StringIOCSVLoader(io.StringIO(content.read().decode("utf-8")))

        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)
        qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 1}))

        response = qa.run(query)
    elif pdf_file:
        pdf_filename = secure_filename(pdf_file.filename)
        pdf_file.save(pdf_filename)
        loader = PDFLoader(pdf_filename)

        # Similar processing steps for PDF as for text and csv files

    elif db_file:
        db_filename = secure_filename(db_file.filename)
        db_file.save(db_filename)
        db = SQLDatabase.from_uri(f"sqlite:///{db_filename}")
        toolkit = SQLDatabaseToolkit(db=db)

        agent_executor = create_sql_agent(
            llm=OpenAI(temperature=0),
            toolkit=toolkit,
            verbose=True
        )

        response = agent_executor.run(query)
    else:
        return jsonify({"error": "Unsupported file type."})

    return jsonify({"response": response})
    
    
        
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
