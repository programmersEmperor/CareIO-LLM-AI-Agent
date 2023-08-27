from langchain import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI
from Interface.Models.chatMessageModel import ChatMessage


class IfModel(IModel):
    _llm: ChatOpenAI
    _prompt: str
    _template: str

    def __init__(self, llm: ChatOpenAI):
        self._llm = llm
        self._template = '''rules:
{rules}
task: give an output

input: {value}
output:'''
        self._prompt = PromptTemplate(
            input_variables=['rules', 'value'],
            template=self._template
        )

    def handle(self, **kwargs):
        messages = [
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content=self.prompt_format(**kwargs))
        ]
        return self._llm(messages).content

    def prompt_format(self, **kwargs):
        rules = kwargs['rules']
        value = kwargs['value']

        if (not isinstance(rules, dict)) or len(rules) < 1:
            raise Exception('rules argument must be dict')
        if (not isinstance(value, str)) or len(rules) < 1:
            raise Exception('value argument must be string ')

        rules_block = ',\n'.join([f'if {rule} then the output is "{result}"' for rule, result in rules.items()])
        return self._prompt.format(value=value, rules=rules_block)
