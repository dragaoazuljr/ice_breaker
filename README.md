# Ice Breakers

A fork of [@emarco177/ice_breaker](https://github.com/emarco177/ice_breaker) project used on his Course [LangChain- Develop LLM powered applications with LangChain](https://www.udemy.com/course/langchain/?referralCode=D981B8213164A3EA91AC)
## About the Project

This project is designed to gather and analyze information about individuals using their LinkedIn and Twitter profiles. The primary goal is to extract key
 insights about a person's work experience, interesting facts, topics of interest, and ice breakers for starting conversations.

## Prerequisites

To run the project, you will need:

1. Python 3.x installed
2. A web driver (Chrome in this example) and its corresponding libraries
3. `llama2:13b` or any compatible Ollama model
5. The `langchain` library installed

## Instructions

First, ensure that you have all the required packages installed. To install them, run the following command in your terminal:

```
pip install -r requirements
```

Next, set up your environment variables by adding the following lines to your `.env` file:

```makefile
EMAIL=your_email@example.com
PASS=your_password
TWITTER_USERNAME=username_of_the_twitter_profile
MODEL=llama2:13b
```

Now, you can run the project by executing the `ice_breaker.py` script. The script will search for the LinkedIn and Twitter profiles of the person based on their 
name, extract relevant information, and save it as a JSON file named `person_intel.json`.

## Usage Example

To use the script, simply provide the full name of the person as an argument when you run the script:

```bash
python ice_breaker.py "John Doe"
```

The script will then output a JSON file `person_intel.json` containing the following fields: summary, facts, topics_of_interest, and ice_breakers.

## Important Notes

Please note that this project relies on web scraping to gather information from LinkedIn and Twitter profiles, so be sure to use it responsibly and ethica
lly. Scraping data without proper authorization may violate the terms of service of both platforms and lead to legal consequences.
