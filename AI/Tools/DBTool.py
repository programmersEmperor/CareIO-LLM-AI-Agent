from typing import Optional
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import DuckDuckGoSearchRun, Tool

from AI.Models.DBAIModel import DBAIModel


class DBTool(Tool):
    name: str
    description: str
    model: DBAIModel

    def __init__(self, name: str, description: str, model: DBAIModel):
        super().__init__(name=name, description=description, func=self.run, model=model)

        self.name = name
        self.description = description
        self.model = model

    def run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None, **kwargs) -> str:
        return self.model.handle(query)

