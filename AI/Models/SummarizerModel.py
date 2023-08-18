from langchain import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI
from Interface.Models.chatMessageModel import ChatMessage


class SummarizerModel(IModel):
    _llm: ChatOpenAI
    _prompt: str
    _template: str

    def __init__(self, llm: ChatOpenAI):
        self._llm = llm
        self._template = '''
Progressively summarize the lines of conversation provided, adding onto the previous summary returning a new summary.
EXAMPLE
Current summary:
The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good.
New lines of conversation:
Human: Why do you think artificial intelligence is a force for good?
AI: Because artificial intelligence will help humans reach their full potential.
New summary:
The human asks what the AI thinks of artificial intelligence. The AI thinks artificial intelligence is a force for good because it will help humans reach their full potential.
END OF EXAMPLE
{memory}
New summary:'''
        self._prompt = PromptTemplate(
            input_variables=['memory'],
            template=self._template
        )

    def handle(self, request: str):
        messages = [
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content=request)
            ]

        return self._llm(messages).content

    def prompt_format(self, **kwargs):
        summary = kwargs['summary']
        conversation = kwargs['conversation']

        if not isinstance(summary, str):
            raise Exception('summary argument must be string')
        if not isinstance(conversation, list):
            raise Exception('conversation argument must be list of ChatMessage')

        memory = ''

        if len(summary) > 0:
            memory += f'Current summary:\n{summary}'

        if len(conversation) > 0:
            memory += '\nCurrent conversation:'
            for message in conversation:
                memory += f'\n{message.role.value}: {message.content}'

        return self._prompt.format(memory=memory)
