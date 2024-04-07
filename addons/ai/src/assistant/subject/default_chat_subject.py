from addons.ai.src.assistant.subject.abstract_chat_subject import AbstractChatSubject


class DefaultSubject(AbstractChatSubject):
    def name(self) -> str:
        return "default"
