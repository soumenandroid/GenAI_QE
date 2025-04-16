from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.service import Agent
from pydantic import SecretStr
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

async def testAIAutomation():
    # Initialize the model
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

    # Create agent with the model
    agent = Agent(
        task="Open www.google.com",
        llm=llm,
        use_vision=True
    )

    history = await agent.run()
    print(history.final_result())

asyncio.run(testAIAutomation())