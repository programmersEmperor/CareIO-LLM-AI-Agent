from langchain import PromptTemplate
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
    _template = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: "Question here"
    SQLQuery: "SQL Query to run"
    SQLResult: "Result of the SQLQuery"
    Answer: "Final answer here"

    Only use the following tables:

    {table_info}

    Rules:
    You must never include any primary keys or foreign keys in the answer.
    You must use SQL Like Operator when comparing with string value column.
    You must return "Appointments" rows which their userId is equal to keyId.  
    You must return "Users" rows which their userId is equal to keyId.  
    Question: {input}"""
    _prompt = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=_template
    )

    def __init__(self, llm: ChatOpenAI):
        driver = 'ODBC+Driver+17+for+SQL+Server'
        server = 'DESKTOP-P7P68FP'  # 'ROWAD-SERVER'
        database = 'test'  # 'drAI'
        username = 'ai'  # 'ai3'
        password = '12345'

        # conn = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
        conn = f'mssql+pyodbc:///?driver={driver}&server={server}&database={database}&trusted_connection=yes'
        db = SQLDatabase.from_uri(conn, include_tables=['Clients', 'Doctors', 'Appointments', 'Specialisms'], custom_table_info=self._custom_table_schema)
        self._chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=False, use_query_checker=True, prompt=self._prompt)

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
