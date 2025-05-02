import os
from crewai import Agent
from tools.search_tool import SearchTools
from tools.calculator_tool import CalculatorTools
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq

load_dotenv(find_dotenv())
llm = ChatGroq(temperature = 0.5,groq_api_key=os.getenv("GROQ_API_KEY"),model_name="llama3-70b-8192")


class TripAgents():
   

  def city_selection_agent(self):
    return Agent(
        role='City Selection Expert',
        goal='Select the best city based on weather, season, and prices',
        backstory=
        'An expert in analyzing travel data to pick ideal destinations',
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
        about the city, it's attractions and customs""",
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
        packing suggestions for the city""",
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