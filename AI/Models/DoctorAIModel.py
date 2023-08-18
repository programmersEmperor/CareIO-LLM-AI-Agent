from langchain import LLMChain
from langchain.prompts import StringPromptTemplate
from AI.Utilities.CustomAgent import CustomAgent
from AI.Utilities.CustomAgentOutputParser import CustomAgentOutputParser
from AI.Utilities.CustomAgentPromptTemplate import CustomAgentPromptTemplate
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI


class DoctorAIModel(IModel):
    _llm: ChatOpenAI
    _tools: list
    _template: str
    _agent: CustomAgent
    _prompt: StringPromptTemplate

    def __init__(self, llm: ChatOpenAI, tools: list):
        self._llm = llm
        self._tools = tools
        self._template = """
You are a helpful assistant who can answer anything.
Complete the objective as best you can.
You have access to the following tools:

{tools}

if no tool is 

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question following by the ending

These were previous tasks you completed:



Begin! 

Question: {input}
{agent_scratchpad}"""
        self._prompt = CustomAgentPromptTemplate(
            template=self._template,
            tools=self._tools,
            input_variables=["input", "intermediate_steps"]
        )
        self._agent = CustomAgent(chain=LLMChain(llm=llm, prompt=self._prompt), output_parser=CustomAgentOutputParser(),
                                  tools=self._tools)

    def handle(self, request: str):
        return self._agent.handle(request)

