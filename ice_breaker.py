import json
import sys
import os

from dotenv import load_dotenv

from langchain.chains import LLMChain
from langchain.globals import set_verbose
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.ollama import ChatOllama
from langchain_community.llms.ollama import Ollama

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_twitter_profile

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from output_parsers import person_intel_parser

# get the name from command line arguments
name = sys.argv[1]

def ice_breaker(name): 
    load_dotenv()

    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url)

    twitter_profile_url = twitter_lookup_agent(name=name)
    twitter_data = scrape_twitter_profile(twitter_profile_url)

    summary_template = """
Use the following pieces of information about a person and answer the request.
----
LinkedIn Information: {linkedin_information}
----
Twitter Information: {twitter_information}
----

Request:
1. A short summary about the work experience of the person
2. A list of interesting related facts about him
3. A list of topics that you think they would be interested in discussing
4. A list of creative Ice Breakers to open a conversation with him

{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"], 
        template=summary_template,
        partial_variables={"format_instructions": person_intel_parser.get_format_instructions()}
    )

    model = os.getenv("MODEL", "llama2:13b")
    llm = Ollama(temperature=0, model=model)

    set_verbose(True)

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    res = chain.invoke(input={"linkedin_information": linkedin_data, "twitter_information": twitter_data})
    
    if (model=="mistral"):
        output = res['text'].replace("`", "")
    else:
        output = res['text']

    try:
        return person_intel_parser.parse(output)
    except Exception as e:
        print("Failed to parse JSON directly. Trying using llm to fix")
        try:
            template_text = """
The output received from the model was not in the expected format. Remove possible json formatting issues and try again.
The output was: {action_input}
Format the output in the following format:
{format_instructions}
                """

            template = PromptTemplate(
                input_variables=["action_input"],
                template=template_text,
                partial_variables={"format_instructions": person_intel_parser.get_format_instructions()}
            )

            chain = LLMChain(llm=llm, prompt=template)

            res = chain.invoke(input={"action_input": output})

            return person_intel_parser.parse(res['text'])
        except OutputParserException as e:
            try:
                print("Error parsing output from llm. Attempting to parse JSON directly.")

                try_formatting_json = json.loads(output)
            except json.JSONDecodeError as e:
                print("Error parsing to json. Returning content as is")
                return output

        return try_formatting_json

if __name__ == "__main__":
    result = ice_breaker(name)   

    #save the result to a json file
    with open('person_intel.json', 'w') as f:
        json.dump(result, f, indent=4)
