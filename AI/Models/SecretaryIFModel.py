from langchain import LLMChain
from langchain.prompts import StringPromptTemplate

from AI.Models.DBAIModel import DBAIModel
from AI.Models.DoctorAIModel import DoctorAIModel
from AI.Models.IFModel import IfModel
from AI.Utilities.CustomAgent import CustomAgent
from AI.Utilities.CustomAgentOutputParser import CustomAgentOutputParser
from AI.Utilities.CustomAgentPromptTemplate import CustomAgentPromptTemplate
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI


class SecretaryIFModel(IModel):
    _llm: ChatOpenAI
    _ifModel: IfModel
    _rules: dict
    _doctor: DoctorAIModel
    _databaser: DBAIModel

    def __init__(self, llm: ChatOpenAI):
        self._llm = llm
        self._ifModel = IfModel(self._llm)
        self._doctor = DoctorAIModel(self._llm)
        self._databaser = DBAIModel(self._llm)
        self._rules = {"input is about 'appointments' or 'doctors' or 'health centers'": '1', 'not': '0'}

    def handle(self, user_id: int, summary: str, message: str) -> str:
        response = ''
        match self._ifModel.handle(rules=self._rules, value=message):
            case '1':  # call database agent
                print('databaser is called')
                response = self._databaser.handle(message, user_id=user_id)
            case '0':  # call medical model
                print('doctor is called')
                context = self._doctor.prompt_format(summary=summary, message=message)
                response = self._doctor.handle(context)
                response += self.suggest_doctors(user_id, response)

        # context = self._doctor.prompt_format(summary=summary, message=message)
        # response = self._doctor.handle(context)

        return response

    def suggest_doctors(self, user_id: int, diagnosis: str) -> str:
        rules = {"input is a diagnosis": 'the diagnosis disease', 'not': '0'}
        response = ''
        disease = self._ifModel.handle(rules=rules, value=diagnosis)
        if disease != '0':
            message = "recommend the best 3 doctors which their specialism is the most related to " + disease + " based on rating and number of appointments"
            response = '.\n' + self._databaser.handle(message, user_id=user_id)

        return response


