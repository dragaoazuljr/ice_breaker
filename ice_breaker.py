import os

from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.ollama import ChatOllama

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

if __name__ == "__main__":
    load_dotenv()

    linkedin_profile_url = linkedin_lookup_agent(name="Danillo Moraes")

    # mistral fix to remove the < and > from the url
    valid_url = linkedin_profile_url.replace("<", "").replace(">", "")

    linkedin_data = scrape_linkedin_profile(valid_url)

    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary about the work experience of the person
    2. two interesting work related facts about them
    3. A topic that you think they would be interested in discussing
    4. 2 creative Ice Breakers to open a conversation with them
    """

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    model = os.getenv("MODEL", "llama2:13b")
    llm = ChatOllama(temperature=0, model=model)

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    res = chain.invoke(input={"information": linkedin_data})

    print(res['text'])

