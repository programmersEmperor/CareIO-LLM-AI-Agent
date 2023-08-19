from typing import Optional
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import DuckDuckGoSearchRun, Tool


class SearchTool(Tool):
    name: str
    description: str
    sites: list | None

    def __init__(self, name: str, description: str, sites: list | None = None):
        super().__init__(name=name, description=description, func=self.run)

        self.name = name
        self.description = description
        self.sites = []
        if sites is not None:
            self.sites = sites

    def run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None, **kwargs) -> str:
        search = f"({' | '.join([f'site:{site}' for site in self.sites])}) {query}"
        return DuckDuckGoSearchRun().run(search)

