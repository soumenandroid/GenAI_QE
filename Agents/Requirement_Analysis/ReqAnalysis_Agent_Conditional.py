from pathlib import Path
import tempfile
from typing import Type
from crewai import LLM, Agent, Crew, Task
from langchain_groq import ChatGroq
import os
from crewai_tools import PDFSearchTool
import streamlit as st
from dotenv import load_dotenv,find_dotenv
from crewai.tools import BaseTool
from crewai_tools import PDFSearchTool
from pydantic import BaseModel, Field


load_dotenv(find_dotenv())
api_key=os.environ["GEMINI_API_KEY"]

#llm1 = ChatGroq(temperature = 0.5,groq_api_key=api_key,model="llama3-8b-8192")
llm = LLM(temperature = 0.5,api_key=api_key,model="gemini/gemini-1.5-flash-8b")



from crewai.tools import tool

@tool("Test case Generation tool")
def test_case_generation_tool(user_input: str) -> str:
    """
    This tool is used for generating test case for a given user input
    the input should be a str

    :param user_input: str, input text for which to retrieve secret code
    """
    return llm.invoke(user_input)




testcase_design_agent = Agent(
role="QA_Engineer",
goal="""You are a senior QA engineer. Your goal is to prepare 2 test cases for the provided {user_input}""",
backstory=(
    "You are a senior QA engineer. Your goal is to prepare 2 test cases for the provided {user_input}"
),
verbose=True,
allow_delegation=False,
tools=[test_case_generation_tool],
llm=llm,
)



testcase_design_task = Task(
    description=("Generate test cases for the provided {user_input}"),
    expected_output=("You should analyse the user_input and generate 2 test cases in BDD format"),
    agent=testcase_design_agent,
)

qa_crew = Crew(
    agents=[testcase_design_agent], 
    tasks=[testcase_design_task],
    verbose=True,
)



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
                provider="google", # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="gemini-1.5-flash-8b",
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

    
    user_input = st.text_input(label="Ask question")
    if user_input:
        if 'requirement' in user_input:
            result = rag_tool.run(user_input)
        else:
            inputs ={"user_input":user_input}
            result = qa_crew.kickoff(inputs)
        st.write(result)