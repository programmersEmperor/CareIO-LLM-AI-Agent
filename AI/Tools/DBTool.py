from typing import Optional
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import DuckDuckGoSearchRun, Tool

from AI.Models.DBAIModel import DBAIModel


class DBTool(Tool):
    name: str
    description: str
    db_model: DBAIModel

    def __init__(self, name: str, description: str, db_model: DBAIModel):
        super().__init__(name=name, description=description, func=self.run, db_model=db_model)

        self.name = name
        self.description = description
        self.db_model = db_model

    def run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None, **kwargs) -> str:
        print("in the tool" + query)
        return self.db_model.handle(query)

