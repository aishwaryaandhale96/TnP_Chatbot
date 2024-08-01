from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from time import sleep

from flask import Flask, abort, render_template, redirect, url_for, flash, request, abort , jsonify
from flask_bootstrap import Bootstrap5
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, ValidationError, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, length
from time import sleep
import requests
import json 
from time import sleep

import os
os.environ["OPENAI_API_KEY"] = "Your_Open_Key"

reader = PdfReader('dataset.pdf')

raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
Bootstrap5(app)

answer_question_dict = {}



class chat_form(FlaskForm):
    query = StringField(validators=[DataRequired()])
    submit = SubmitField("Ask")
    
anser_dict = {}

@app.route("/", methods = ["POST", "GEt"])
def home():
    form = chat_form()
    if request.method == 'POST':
        if request.form.get("query") != "":
            query = request.form.get("query")
            query = query + "stictly remove all '\n' in the output"
            chain = load_qa_chain(OpenAI(), chain_type="stuff")
            docs = docsearch.similarity_search(query)
            chain.run(input_documents=docs, question=query)
            temp = docs[0]
            temp = str(temp)
            answer = temp.split("page_content='")
            print(answer[1])
            return jsonify(answer)
    return render_template("index.html", form = form, data_list = answer_question_dict)

if __name__ == "__main__":
    app.run(debug= True)

