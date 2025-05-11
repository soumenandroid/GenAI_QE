import os
from crewai import Agent
from tools.search_tool import SearchTools
from tools.calculator_tool import CalculatorTools
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from crewai import LLM

load_dotenv(find_dotenv())
#llm = ChatGroq(temperature = 0.5,groq_api_key=os.getenv("GROQ_API_KEY"),model_name="llama3-70b-8192")
llm = LLM(temperature = 0.5,api_key=os.getenv("GEMINI_API_KEY"),model="gemini/gemini-1.5-flash-8b")


class TripAgents():
   

  def customer_interest_search_agent(self):
    return Agent(
        role='Customer_Interest_Search_Expert',
        goal='Get list of places of customer interested topic in the city',
        backstory=
        'You will find out places of custoner interested topic',
        tools=[
            SearchTools.search_internet,
            #BrowserTools.scrape_and_summarize_website,
        ],
        
        verbose=True,
        llm = llm,
        )

  def local_expert(self):
    return Agent(
        role='Local Expert at this city',
        goal='Provide the BEST insights about the selected city',
        backstory="""A knowledgeable local guide with extensive information
        about the city for the date range, it's attractions and customs""",
        tools=[
            SearchTools.search_internet,
            #BrowserTools.scrape_and_summarize_website,
        ],
        verbose=True,
        llm = llm,
        )

  def travel_concierge(self):
    return Agent(
        role='Amazing Travel Concierge',
        goal="""Create the most amazing travel itineraries with budget and 
        packing suggestions for the city for the date range""",
        backstory="""Specialist in travel planning and logistics with 
        decades of experience""",
        tools=[
            SearchTools.search_internet,
            #BrowserTools.scrape_and_summarize_website,
            CalculatorTools.calculate,
        ],
        verbose=True,
        llm = llm,
        )