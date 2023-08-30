import subprocess

from crawler.WexAppCrawler import WexAppCrawler
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import (
    FewShotChatMessagePromptTemplate,
    ChatPromptTemplate,
)

class AppAssistant:
    def __init__(self):
        self.root = os.getcwd() + '/'

        # Update tree info
        self.crawler = WexAppCrawler(self.root, '.wex/ai/data/tree.yml')

        # Load .env file to get API token
        load_dotenv(dotenv_path=self.root + '.env')

        self.llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def create_chain(self, prompt_template):
        return LLMChain(
            llm=self.llm,
            prompt=prompt_template,
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

    def load_file(self, file_path):
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r') as f:
            return f.read()

    def load_example_patch(self, name):
        return {
            'prompt': self.load_file(f'{self.root}.wex/command/samples/examples/{name}/prompt.txt'),
            'source': self.load_file(f'{self.root}.wex/command/samples/examples/{name}/source.py'),
            'patch': self.load_file(f'{self.root}.wex/command/samples/examples/{name}/response.patch'),
        }

    def patch(self, question: str):
        # create our examples

        examples = [
            self.load_example_patch('generate/program_hello_world'),
            self.load_example_patch('explain/code_comment')
        ]

        # create a example template
        example_template = """
        User: {prompt}
        Source: {source}
        AI: {patch}
        """

        # create a prompt example from above template
        example_prompt = PromptTemplate(
            input_variables=["prompt", "source", "patch"],
            template=example_template
        )

        # now break our previous prompt into a prefix and suffix
        # the prefix is our instructions
        prefix = """You are a programming assistant. You generate Python code regarding the user request. Here are some
        examples: 
        """
        # and the suffix our user input and output indicator
        suffix = """
        User: {prompt}
        Source: {source}
        AI: """

        # now create the few shot prompt template
        few_shot_prompt_template = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=prefix,
            suffix=suffix,
            input_variables=["prompt", "source"],
            example_separator="\n\n"
        )

        prompt = "Explain how to pass arguments to prefix the output value"
        source = """       

import random

def create_random_process_id() -> int:
  return random.randint(1,1000)
"""

        return self.llm(
            few_shot_prompt_template.format(
                prompt=prompt,
                source=source
            )
        )

