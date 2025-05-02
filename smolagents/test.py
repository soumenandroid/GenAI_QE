from smolagents import CodeAgent, HfApiModel, DuckDuckGoSearchTool


model = HfApiModel(token="")
agent = CodeAgent(tools=[DuckDuckGoSearchTool()],
                  model=model,
                  additional_authorized_imports=
                    ["selenium",
                    "selenium.webdriver.common.keys",
                    "selenium.webdriver.common.by",
                    ]
                  )

agent.run(
    """Write a selenium test to run to open makemytrip and book a flight from Delhi to London """, 
)