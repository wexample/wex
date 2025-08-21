from addons.ai.src.assistant.subject.abstract_chat_subject import \
    AbstractChatSubject

SUBJECT_DEFAULT_COMMAND_CHAT = "chat"
SUBJECT_DEFAULT_COMMAND_DEFAULT = "default"
SUBJECT_DEFAULT_COMMAND_INVESTIGATE = "investigate"
SUBJECT_DEFAULT_COMMAND_FORMAT = "format"


class DefaultChatSubject(AbstractChatSubject):
    @staticmethod
    def name() -> str:
        return "default"
