import os

from assistant.AppAssistant import AppAssistant


assistant = AppAssistant()

print(
    assistant.patch('I want this program return the text in uppercase.')
)

# assistant.assist(
#     """
#     Ask here when OpenAI website is Down...
#     """
# )

