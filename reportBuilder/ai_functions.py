from bs4 import BeautifulSoup
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

from .prompt_templates import PR_PROMPT_TEMPLATE, GLOSSARY_PROMPT_TEMPLATE


def get_prompt(pr_data):
    # Create the prompt for the AI
    prompt = []

    for pr in pr_data:
        # Collect all PR descriptions
        soup = BeautifulSoup(pr['body_html'], 'html.parser')
        description = "Title - " + pr['title'] + "\nPR Description - " + \
            soup.find('h2', string='Description').find_next('p').text + "\nClosing Issue - " + \
            soup.find('h2', string='Related Issue').find_next('p').text

        if "Please describe your pull request." in description:
            description = description.replace(
                "Please describe your pull request.", '')

        # Collect info on what type of PR it is
        checked_items = []

        checkboxes = soup.find_all(
            'input', {'type': 'checkbox', 'checked': True})
        for checkbox in checkboxes:
            text = "\n Type of change - " + \
                checkbox.find_previous('li').text.strip() + " \n\n"
            checked_items.append(text)

        combined_string = description + " " + " ".join(checked_items)

        prompt.append(combined_string)

    # Combine into one string and use as prompt for AI
    combined_prompt = " ".join(prompt)
    # print(combined_prompt)
    return combined_prompt


def get_ai_description(parsed_pr_data):
    # Call on the AI to generate a description of the PRs
    openai_api_token = os.getenv('OPENAI_API_TOKEN')

    llm = OpenAI(openai_api_key=openai_api_token, temperature=0.7)

    prompt_description = PromptTemplate(
        input_variables=["pr_data"],
        template=PR_PROMPT_TEMPLATE
    )

    prompt_glossary = PromptTemplate(
        input_variables=["description"],
        template=GLOSSARY_PROMPT_TEMPLATE
    )

    chain_description = LLMChain(
        llm=llm, prompt=prompt_description, verbose=True)
    # chain_glossary = LLMChain(llm=llm, prompt = prompt_glossary)
    # overall_chain = SimpleSequentialChain(chains=[chain_description, chain_glossary], verbose = True)

    overall = chain_description.run(parsed_pr_data)

    return overall
