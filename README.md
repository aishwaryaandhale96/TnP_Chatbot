Here's a `README.md` file for your project:


# 📚 VIIT College Training and Placement Chatbot 🤖

Welcome to the VIIT College Training and Placement Chatbot project! This chatbot is designed to assist students with training and placement-related queries using data extracted from college documents.

## 🌟 Features

- **PDF Data Extraction**: Extracts text data from PDF documents.
- **Text Splitting**: Splits large text data into manageable chunks.
- **Embeddings and Search**: Uses OpenAI embeddings and FAISS for similarity search.
- **Question Answering**: Provides answers to user queries based on the extracted data.
- **Web Interface**: User-friendly web interface using Flask and Flask-Bootstrap.

## 🛠️ Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/aishwaryaandhale96/TnP_Chatbot.git
    cd viit-chatbot
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:
    ```bash
    export OPENAI_API_KEY='Your_OpenAI_API_Key'
    ```

4. **Run the Application**:
    ```bash
    python index.py
    ```

## 📋 Usage

1. **Upload Dataset**:
    - Place your `dataset.pdf` file in the project directory.

2. **Start the Application**:
    - Navigate to `http://127.0.0.1:5000` in your web browser.

3. **Ask Questions**:
    - Use the chat form on the web page to submit your queries.

## 🧩 Code Overview

### PDF Data Extraction
```python
from PyPDF2 import PdfReader

reader = PdfReader('dataset.pdf')
raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text
```

### Text Splitting
```python
from langchain.text_splitter import CharacterTextSplitter

text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
texts = text_splitter.split_text(raw_text)
```

### Embeddings and Search
```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)
```

### Flask Application
```python
from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap5
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
Bootstrap5(app)

class ChatForm(FlaskForm):
    query = StringField(validators=[DataRequired()])
    submit = SubmitField("Ask")

@app.route("/", methods=["POST", "GET"])
def home():
    form = ChatForm()
    if request.method == 'POST':
        if form.query.data != "":
            query = form.query.data + " strictly remove all '\\n' in the output"
            chain = load_qa_chain(OpenAI(), chain_type="stuff")
            docs = docsearch.similarity_search(query)
            answer = chain.run(input_documents=docs, question=query)
            return jsonify(answer)
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
```

## 🌐 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.


Happy coding! 🎉

This `README.md` file provides an interactive and comprehensive overview of your project, including installation instructions, usage guidelines, and a brief code overview. Feel free to customize it further based on your specific needs and preferences.
