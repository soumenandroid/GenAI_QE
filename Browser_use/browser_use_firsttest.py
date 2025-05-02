from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.service import Agent
from pydantic import SecretStr
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

async def testAIAutomation():
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(os.getenv('GEMINI_API_KEY')))

    task = """Open www.amazon.com. 
    Then search for 'laptop' and click on the first link.
    Then add to cart the first laptop"""

    agent = Agent(
        task = task,
        llm= llm,
        use_vision=True
    )

    result = await agent.run()
    print(result.final_result())


asyncio.run(testAIAutomation())
