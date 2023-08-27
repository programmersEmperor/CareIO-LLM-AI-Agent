from langchain import LLMChain
from langchain.prompts import StringPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

from AI.Utilities.CustomAgent import CustomAgent
from AI.Utilities.CustomAgentOutputParser import CustomAgentOutputParser
from AI.Utilities.CustomAgentPromptTemplate import CustomAgentPromptTemplate
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI

from Interface.Models.chatMessageModel import ChatMessage


class DoctorAIModel(IModel):
    _llm: ChatOpenAI
    _systemPrompt = '''you are a professional doctor who helps people diagnose their illnesses accurately.

RULES:  
You must answer only medical questions.
You must not ask more than one question in your turn.
You must ask only one question in your turn.
You must ask the next question based on the patients answers.
Questions must be in "Yes/No Questions Format". 
Questions must specific.
You must consider all the possibles.
Keep asking until you surly diagnose the correct illness.
Speak the same language as the last message.
'''

    def __init__(self, llm: ChatOpenAI):
        self._llm = llm

    def handle(self, request: str):
        messages = [
            SystemMessage(content=self._systemPrompt),
            HumanMessage(content=request)
        ]
        return self._llm(messages).content

    @staticmethod
    def prompt_format(**kwargs):
        summary = kwargs['summary']
        message = kwargs['message']

        if not isinstance(summary, str):
            raise Exception('summary argument must be str')
        if not isinstance(message, str):
            raise Exception('message argument must be str')

        context = ''

        if len(summary) > 0:
            context += f'SUMMARY:\n{summary}'
        context += f'CONVERSATION:\npatient: {message}' + '\ndr:'

        return context
