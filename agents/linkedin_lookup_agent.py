import os

from langchain.globals import set_verbose
from langchain_community.chat_models.ollama import ChatOllama
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain import hub
from dotenv import load_dotenv

from tools.tools import get_first_google_search


def lookup(name: str) -> str:
    load_dotenv()

    set_verbose(True)

    model = os.getenv("MODEL", "llama2:13b")
    llm = ChatOllama(temperature=0, model=model)
    
    template = """
    given the full name {name_of_person} I want you to get it me a link to their LinkedIn profile page.
    Your answer should be a valid LinkedIn profile URL. 
    If the url contains a < or > remove them
    If the url has a different domain than www.linkedin.com, replace it with www, like br.linkedin.com will be www.linkedin.com 
    """

    func = lambda name: get_first_google_search(name, "LinkedIn")

    tools_for_agents = [
        Tool(
            name="Crawl Google 4 LinkedIn profile pages",
            func=func,
            description="Useful for when you need to find a link of LinkedIn profile for a person",
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
