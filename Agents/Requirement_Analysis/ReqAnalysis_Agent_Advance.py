from pathlib import Path
import tempfile
from crewai import LLM, Agent, Crew, Task
from langchain_groq import ChatGroq
import os
from crewai_tools import PDFSearchTool
import streamlit as st
from dotenv import load_dotenv,find_dotenv
from langchain_community.utilities import GoogleSerperAPIWrapper
from crewai.tools import BaseTool
from pydantic import Field
from crewai_tools import PDFSearchTool

load_dotenv(find_dotenv())
api_key=os.environ["GROQ_API_KEY"]

llm1 = ChatGroq(temperature = 0.5,groq_api_key=api_key,model="llama3-8b-8192")
llm = LLM(temperature = 0.5,api_key=api_key,model="groq/llama3-8b-8192")
config = {
    
    "llm": {
        "provider": "groq",
        "config": {
            "model": "llama3-8b-8192",
            "api_key": api_key
        }
    },
    "embedding_model": {
        "provider": "huggingface",
        "config": {
            "model": "BAAI/bge-small-en-v1.5"
        }
    }
}





st.title("Requirement Anlaysis")
TMP_DIR = Path(__file__).resolve().parent.joinpath('data','tmp')
# Store paths of saved files
saved_pdf_paths = []


req_docs = st.file_uploader(label="Upload requirement document", type=['pdf'],accept_multiple_files=True)


if req_docs:
    for source_docs in req_docs:
            with tempfile.NamedTemporaryFile(delete=False,dir=TMP_DIR.as_posix(),suffix='.pdf') as temp_file:
                temp_file.write(source_docs.read())
                saved_pdf_paths.append(temp_file.name)  # Store the path
    
    st.write(saved_pdf_paths[0])





""" Tool section"""

search = GoogleSerperAPIWrapper

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find relevant information from internet"
    search: GoogleSerperAPIWrapper = Field(default_factory=GoogleSerperAPIWrapper)

    def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"
        
class GenerationTool(BaseTool):
    name: str = "Generation_tool"
    description: str = "Useful for generic-based queries. Use this to find  information based on your own knowledge."

    def _run(self, query: str) -> str:
      llm=llm
      """Execute the search query and return results"""
      return llm.invoke(query)
    

generation_tool=GenerationTool()
web_search_tool = SearchTool()
pdf_search_tool = PDFSearchTool(pdf=saved_pdf_paths[0],
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

""" AGENT """

Router_Agent = Agent(
  role='Router',
  goal='Route user question to a vectorstore or web search',
  backstory=(
    "You are an expert at routing a user question to a vectorstore or web search ."
    "Use the vectorstore for questions on requirement document or tiny llm or finetuning of llm."
    "use web-search for question on industry best practices."
    "use generation for generic questions otherwise"
  ),
  verbose=True,
  allow_delegation=False,
  llm=llm,
)
Retriever_Agent = Agent(
role="Retriever",
goal="Use the information retrieved from the vectorstore to answer the question",
backstory=(
    "You are an assistant for question-answering tasks."
    "Use the information present in the retrieved context to answer the question."
    "You have to provide a clear concise answer within 200 words."
),
verbose=True,
allow_delegation=False,
llm=llm,
)




router_task = Task(
    description=("Analyse the keywords in the question {question}"
    "Based on the keywords decide whether it is eligible for a vectorstore search or a web search or generation."
    "Return a single word 'vectorstore' if it is eligible for vectorstore search."
    "Return a single word 'websearch' if it is eligible for web search."
    "Return a single word 'generate' if it is eligible for generation."
    "Do not provide any other premable or explaination."
    ),
    expected_output=("Give a  choice 'websearch' or 'vectorstore' or 'generate' based on the question"
    "Do not provide any other premable or explaination."),
    agent=Router_Agent,
   )

retriever_task = Task(
    description=("Based on the response from the router task extract information for the question {question} with the help of the respective tool."
    "Use the web_serach_tool to retrieve information from the web in case the router task output is 'websearch'."
    "Use the rag_tool to retrieve information from the vectorstore in case the router task output is 'vectorstore'."
    "otherwise generate the output basedob your own knowledge in case the router task output is 'generate"
    ),
    expected_output=("You should analyse the output of the 'router_task'"
    "If the response is 'websearch' then use the web_search_tool to retrieve information from the web."
    "If the response is 'vectorstore' then use the rag_tool to retrieve information from the vectorstore."
    "If the response is 'generate' then use then use generation_tool ."
    "otherwise say i dont know if you dont know the answer"

    "Return a claer and consise text as response."),
    agent=Retriever_Agent,
    context=[router_task],
    tools=[pdf_search_tool,web_search_tool,generation_tool],
)

rag_crew = Crew(
    agents=[Router_Agent, Retriever_Agent], 
    tasks=[router_task, retriever_task],
    verbose=True,

)



    # Add content from a file
question=st.text_input(label="Ask question")
if question:
    inputs ={"question":question}
    result = rag_crew.kickoff(inputs=inputs)
    st.write(result)