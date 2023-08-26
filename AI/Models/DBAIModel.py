from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pyodbc


class DBAIModel(IModel):
    _llm: ChatOpenAI
    _agent: create_sql_agent

    def __init__(self, llm: ChatOpenAI):
        driver = 'ODBC+Driver+17+for+SQL+Server'
        server = 'ROWAD-SERVER'
        database = 'test'
        username = 'ai3'
        password = '12345'

        restricted_conn = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
        # admin_conn = f'mssql+pyodbc:///?driver={driver}&server={server}&database={database}&trusted_connection=yes'
        db = SQLDatabase.from_uri(restricted_conn)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        self._agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

    def handle(self, request: str):
        print("in the Model" + request)
        return self._agent.run(request)

