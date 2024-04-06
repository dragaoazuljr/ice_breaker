import os

from dotenv import load_dotenv

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool

from tools.tools import get_first_google_search


def lookup(name: str) -> str:
    load_dotenv()

    model = os.getenv("MODEL", "llama2:13b")
    llm = ChatOllama(temperature=0, model=model)

    template = """
    given the full name {name_of_person} I want you to get it me a link to their Twitter profile page.
    Your answer should be a valid Twitter profile URL.
    If the url contains a < or > remove them
    """

    func = lambda name: get_first_google_search(name, "Twitter")

    tools_for_agents = [
        Tool(
            name="Crawl Google 4 Twitter profile pages",
            func=func,
            description="Useful for when you need to find a link of Twitter profile for a person",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools=tools_for_agents,
        prompt=react_prompt
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agents, verbose=True)
    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    output = result["output"]

    # if model is mistral, remove the < and > from the output
    if model == "mistral":
        output = output.replace("<", "").replace(">", "")

    return output
    
