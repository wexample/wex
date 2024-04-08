from typing import TYPE_CHECKING, Optional

from langchain.chains.llm import LLMChain
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject
from addons.ai.src.assistant.utils.identities import AI_IDENTITY_FILE_INSPECTION
from addons.ai.src.model.open_ai_model import MODEL_NAME_OPEN_AI_GPT_4
from src.const.types import StringKeysDict, StringsList
from src.helper.file import file_read_if_exists, file_read

if TYPE_CHECKING:
    from addons.ai.src.assistant.assistant import Assistant

SUBJECT_FILE_CHAT_COMMAND_PATCH = "patch"


class FileChatSubject(AbstractChatSubject):
    def name(self) -> str:
        return "file"

    def introduce(self) -> str:
        return f"Chatting about file {self.get_path()}"

    def __init__(self, assistant: "Assistant", file_path: str) -> None:
        super().__init__(assistant)
        self.file_path = file_path

    def get_path(self) -> str:
        self._validate__should_not_be_none(self.file_path)

        return self.file_path

    def get_completer_commands(self) -> StringsList:
        return [
            SUBJECT_FILE_CHAT_COMMAND_PATCH
        ]

    def process_user_input(
        self,
        user_input_split: StringKeysDict,
        identity: StringKeysDict,
        identity_parameters: StringKeysDict,
    ) -> Optional[str]:
        user_command = user_input_split["command"]
        user_input = user_input_split["input"]

        # Avoid empty input error.
        if not user_input:
            return None

        if user_command == SUBJECT_FILE_CHAT_COMMAND_PATCH:
            examples = [
                self.load_example_patch('generate/program_hello_world'),
                self.load_example_patch('explain/code_comment'),
                self.load_example_patch('patch/hello_world_capitalized')
            ]

            example_template_base = (
                "User request:\n{prompt}\n\n"
                "Complete source code of the application:\n{source}\n\n"
                "AI-generated Git patch:\n")

            example_prompt = PromptTemplate(
                input_variables=["prompt", "source", "patch"],
                template=example_template_base + """{patch}"""
            )

            few_shot_prompt_template = FewShotPromptTemplate(
                examples=examples,
                example_prompt=example_prompt,
                # The prefix is our instructions
                prefix=identity["system"],
                # The suffix our user input and output indicator
                suffix=example_template_base,
                input_variables=["prompt", "source"],
                example_separator="\n----------------------------------\n"
            )

            model = self.assistant.get_model()

            chain = LLMChain(
                llm=model.get_llm(),
                prompt=few_shot_prompt_template,
                verbose=False
            )

            identity_parameters.update({
                "prompt": user_input,
                "source": file_read(self.get_path())
            })

            return str(chain.invoke(
                model.chat_merge_parameters(user_input, identity_parameters)
            )["text"].strip())


        embedding_function = self.assistant.get_model(
            MODEL_NAME_OPEN_AI_GPT_4
        ).create_embeddings()
        chroma = Chroma(
            persist_directory=self.assistant.chroma_path,
            embedding_function=embedding_function,
            collection_name="single_files",
        )
        results = chroma.similarity_search_with_relevance_scores(
            user_input, k=3, filter={"source": self.get_path()}
        )

        return self.assistant.get_model().chat(
            user_input,
            self.assistant.identities[AI_IDENTITY_FILE_INSPECTION],
            identity_parameters
            or {
                "context": "\n\n---\n\n".join(
                    [doc.page_content for doc, _score in results]
                )
            },
        )

    def load_example_patch(self, name):
        base_path = f'{self.kernel.directory.path}addons/ai/samples/examples/{name}/'

        return {
            'prompt': file_read_if_exists(f'{base_path}prompt.txt'),
            'source': file_read_if_exists(f'{base_path}source.py'),
            'patch': file_read_if_exists(f'{base_path}response.patch'),
        }
