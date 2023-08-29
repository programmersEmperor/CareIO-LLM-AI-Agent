from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.utilities import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain_experimental.sql import SQLDatabaseChain
from AI.Models.IModel import IModel
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pyodbc


class DBAIModel(IModel):
    _llm: ChatOpenAI
    _agent: create_sql_agent
    _custom_table_schema = {
        "Clients": """CREATE TABLE Clients (
    "Id" INTEGER NOT NULL, 
    "Name" NVARCHAR(200) NOT NULL,
    PRIMARY KEY ("Id")
)
""",
    }

    def __init__(self, llm: ChatOpenAI):
        driver = 'ODBC+Driver+17+for+SQL+Server'
        server = 'DESKTOP-P7P68FP'  # 'ROWAD-SERVER'
        database = 'test'  # 'drAI'
        username = 'ai'  # 'ai3'
        password = '12345'

        # conn = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
        conn = f'mssql+pyodbc:///?driver={driver}&server={server}&database={database}&trusted_connection=yes'
        db = SQLDatabase.from_uri(conn, include_tables=['Clients', 'Doctors', 'Appointments', 'Specialisms'], custom_table_info=self._custom_table_schema)
        self._chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=False, use_query_checker=True)

        # toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        #
        # self._agent = create_sql_agent(
        #     llm=llm,
        #     toolkit=toolkit,
        #     verbose=True,
        #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #
        # )

    def handle(self, request: str):
        return self._chain.run(request)
        # return self._agent.run(request)
