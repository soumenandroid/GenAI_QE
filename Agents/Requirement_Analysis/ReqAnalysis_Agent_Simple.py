from pathlib import Path
import tempfile
from langchain_groq import ChatGroq
import os
from crewai_tools import PDFSearchTool
import streamlit as st
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
api_key=os.environ["GROQ_API_KEY"]

#llm = ChatGroq(temperature = 0.5,groq_api_key=api_key,model_name="llama3-8b-8192")
st.title("Requirement Anlaysis")
TMP_DIR = Path(__file__).resolve().parent.joinpath('data','tmp')
req_docs = st.file_uploader(label="Upload requirement document", type=['pdf'],accept_multiple_files=True)

# Store paths of saved files
saved_pdf_paths = []

if req_docs:
    for source_docs in req_docs:
            with tempfile.NamedTemporaryFile(delete=False,dir=TMP_DIR.as_posix(),suffix='.pdf') as temp_file:
                temp_file.write(source_docs.read())
                saved_pdf_paths.append(temp_file.name)  # Store the path


    rag_tool = PDFSearchTool(pdf=saved_pdf_paths[0],
        config=dict(
            llm=dict(
                provider="groq", # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="llama3-8b-8192",
                    api_key=api_key
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="huggingface", # or openai, ollama, ...
                config=dict(
                    model="BAAI/bge-small-en-v1.5",
                    #task_type="retrieval_document",
                    # title="Embeddings",
                ),
            ),
        )
    )

    
    question = st.text_input(label="Ask question")
    if question:
        result = rag_tool.run(question)
        st.write(result)