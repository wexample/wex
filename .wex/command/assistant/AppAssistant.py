from crawler.WexAppCrawler import WexAppCrawler
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI

from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator


class AppAssistant:
    def __init__(self):
        self.root = os.getcwd()

        # Update tree info
        self.crawler = WexAppCrawler(self.root, '.wex/ai/data/tree.yml')

        # Load .env file to get API token
        load_dotenv(dotenv_path=self.root + '/.env')

        self.model = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

        print(self.get_joke())

    def get_joke(self):
        class Joke(BaseModel):
            setup: str = Field(description="question to set up a joke")
            punchline: str = Field(description="answer to resolve the joke")

            @field_validator('setup')
            def question_ends_with_question_mark(cls, field):
                if field[-1] != '?':
                    raise ValueError("Badly formed question!")
                return field

        parser = PydanticOutputParser(pydantic_object=Joke)

        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )

        joke_query = "Tell me a joke."
        _input = prompt.format_prompt(query=joke_query)

        output = self.model(_input.to_string())

        return parser.parse(output)
