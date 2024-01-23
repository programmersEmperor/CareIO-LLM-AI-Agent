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
import pymysql



class DBAIModel(IModel):
    _llm: ChatOpenAI
    _agent: create_sql_agent
    _custom_table_schema = {
        "clients": """CREATE TABLE Clients (
"Id" INTEGER NOT NULL, 
"Name" NVARCHAR(200) NOT NULL,
PRIMARY KEY ("Id")
)
""",
    }
    _custom_sql_prefix = """Your name is Careio, You are an expert agent designed to interact with a MySQL database.
Given an input question, create a syntactically correct MYSQL query to run, 
then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, 
always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, 
only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, 
rewrite the query and try again.
Wrap each column name in square brackets ([]) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CAST(NOW() as date) function to get the current date and time, if the question involves "today".

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.  

If the question does not seem related to the database, just return "I don't know" as the answer.
    """
    _custom_sql_instructions = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question."""
    _custom_sql_suffix = "I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables."

#     _mssql_template = """You are an MS SQL expert. Given an input question, first create a syntactically correct MS SQL query to run, then look at the results of the query and return the answer to the input question.
#     Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the TOP clause as per MS SQL. You can order the results to return the most informative data in the database.
#     Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in square brackets ([]) to denote them as delimited identifiers.
#     Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
#     Pay attention to use CAST(GETDATE() as date) function to get the current date, if the question involves "today".
#
#     Use the following format:
#
#     Question: Question here
#     SQLQuery: SQL Query to run
#     SQLResult: Result of the SQLQuery
#     Answer: Final answer here
#
#     Only use the following tables:
#     {table_info}
#
#     Rules:
#     You must never include any "Primary Keys", "Foreign Keys" or "IDs" in the Answer.
#     You must use "SQL Like Operator" when comparing with string value columns.
#     You must return "Appointments" rows which only their ClientId is equal to keyId.
#     You must return "Clients" rows which only their Id is equal to keyId.
#     Answer must be like a normal humane chat
#
# Question: {input}"""
#     _prompt = PromptTemplate(
#         input_variables=["input", "table_info", "top_k"],
#         template=_mssql_template,
#     )

    def __init__(self, llm: ChatOpenAI):
        # mysql connection
        conn = "mysql+pymysql://root:@127.0.0.1:3306/careiodb"

        # sql server connection
        # driver = 'ODBC+Driver+17+for+SQL+Server'
        # server = 'DESKTOP-P7P68FP'  # 'ROWAD-SERVER'
        # database = 'test'  # 'drAI'
        # username = 'ai'  # 'ai3'
        # password = '12345'
        # conn = f'mssql+pyodbc:///?driver={driver}&server={server}&database={database}&trusted_connection=yes'

        db = SQLDatabase.from_uri(conn, include_tables=['patients', 'doctors', 'appointments', 'specialisms', 'degrees', 'qualifications', 'experiences'], custom_table_info=self._custom_table_schema)
        # self._chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=False, use_query_checker=True, prompt=self._prompt)

        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        self._agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            prefix=self._custom_sql_prefix,
            # format_instructions=self._custom_sql_instructions,
            # suffix=self._custom_sql_suffix
        )

    def handle(self, request: str, user_id: int):
        command = (
                request + ".\n" +
                f"keyId={user_id}.\n" +
                """RULES:
You MUST NOT return "IDs"
You MUST use "SQL Like Operator" when comparing with string value columns.
You MUST filter "appointments" rows by comparing ClientId with keyId.  
You MUST filter "patients" rows by comparing Id with keyId. 
You MUST NEVER mention the database in your answer whatsoever.

Create Query Based On the RULES.
Run Query.
Query Result:""")
        # return self._chain.run(command)

        return self._agent.run(command)
