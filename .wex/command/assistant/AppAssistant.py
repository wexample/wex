from crawler.WexAppCrawler import WexAppCrawler
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


class AppAssistant:
    def __init__(self):
        self.root = os.getcwd()

        # Update tree info
        self.crawler = WexAppCrawler(self.root, '.wex/ai/data/tree.yml')

        # Load .env file to get API token
        load_dotenv(dotenv_path=self.root + '/.env')

        system_message_prompt = SystemMessagePromptTemplate.from_template(
            """
            You are a world class computer programming assistant.
            User will pass in question with and code of an application.
            You should generate a git patch to apply on the code to change the program behaviour.
            ONLY return a git patch without any other text.
            """
        )

        code_message_prompt = HumanMessagePromptTemplate.from_template(
            """
            print('Hello World!')
            """
        )

        human_message_prompt = HumanMessagePromptTemplate.from_template(
            '{text}'
        )

        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            code_message_prompt,
            human_message_prompt
        ])

        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY")),
            prompt=chat_prompt,
        )

        print(
            chain.run('I want this code this code to format text in uppercase.')
        )

