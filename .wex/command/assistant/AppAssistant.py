import subprocess

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
        self.root = os.getcwd() + '/'

        # Update tree info
        self.crawler = WexAppCrawler(self.root, '.wex/ai/data/tree.yml')

        # Load .env file to get API token
        load_dotenv(dotenv_path=self.root + '.env')

        self.llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def create_chain(self, prompt_template):
        return LLMChain(
            llm=self.llm,
            prompt=ChatPromptTemplate.from_messages(
                prompt_template
            ),
        )

    def assist(self, question: str):
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            '{text}'
        )

        chain = self.create_chain(
            ChatPromptTemplate.from_messages([
                human_message_prompt
            ])
        )

        print(
            chain.run(question)
        )

    def test_patch(self):
        self.patch('I want this program return the text in uppercase.')

    def patch(self, question: str):
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            """
            You are a world class computer programming assistant.
            Below base information about the program named __PROGRAM__.
            At the end user will pass in question with and code of an application.
            """
        )

        git_message_prompt = SystemMessagePromptTemplate.from_template(
            """
            You should generate a git patch to apply on the code to change the program behaviour.
            ONLY return a git patch without any other text.
            """
        )

        files_structure_message_prompt = HumanMessagePromptTemplate.from_template(
            """
            File structure of the program __PROGRAM__ :
            .git
              type: folder
            .wex
              type: folder
              children:
                command:
                  type:folder
                  children:
                    samples:
                    children:
                      main.py:
                        type: file
                        description: The main entrypoint of the program.
            """
        )

        code_message_prompt = HumanMessagePromptTemplate.from_template(
            """
            Full code of the program __PROGRAM__,
            after this line there is NO extra empty line at the beginning of the file :
            def my_program_main_function():
                return 'Hello World!'
            """
        )

        human_message_prompt = HumanMessagePromptTemplate.from_template(
            '{text}'
        )

        chain = self.create_chain(
            ChatPromptTemplate.from_messages([
                system_message_prompt,
                git_message_prompt,
                files_structure_message_prompt,
                code_message_prompt,
                human_message_prompt
            ]))

        # TODO : validate patch structure

        patch_content = chain.run(question)
        patch_path = self.root + 'autocode.patch'

        # Save the patch content to a file
        with open(patch_path, 'w') as file:
            file.write(patch_content + '\n')

        # Apply patch
        subprocess.run(['git', 'apply', '--ignore-whitespace', patch_path], cwd=self.root)

        # Delete patch
        # os.remove(patch_path)

        return patch_content
