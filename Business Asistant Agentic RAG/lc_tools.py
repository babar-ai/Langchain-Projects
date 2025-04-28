from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import load_agent,load_tools
from langchain.tools import BaseTool
from typing import Optional






class CalculatorTool(BaseTool):

    name : str = "CalculatorTool"
    description : str = """
    Useful for when you need to answer questions about math.
    This tool is only for math questions and nothing else.
    Formulate the input as python code.
    """

    def _run(
        self, 
        question: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        return eval(question)
    
    async def _arun(
        self, 
        question: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ):
        raise NotImplementedError("This tool does not support async")



def retriever_tool(retriever):
    Retriever_tool = create_retriever_tool(
        retriever,
        "uet_mardan_search",
        "use this tool when searching about Univesity of Engineering and Technology Mardan, khyber phukhtunkhwa Pakistan."
        )
    return Retriever_tool



def all_tools(llm,retriever_tool):
    
    # Load the LLM
    tools = load_tools(["ddg-search","llm-math","wikipedia"],llm=llm)
    tools.append(retriever_tool)
    tools.append(CalculatorTool())

    return tools
    