from langchain.agents import AgentExecutor, LLMSingleActionAgent


class CustomAgent:
    _agent_executor: AgentExecutor

    def __init__(self, chain, output_parser, tools):
        agent = LLMSingleActionAgent(
            llm_chain=chain,
            output_parser=output_parser,
            stop=["\nObservation:"],
            allowed_tools=[tool.name for tool in tools])
        self._agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

    def handle(self, task: str):
        return self._agent_executor.run(task)