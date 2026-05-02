from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from tavily import TavilyClient


load_dotenv()

@tool
def search(query: str) -> str:
    """ Tool for performing a search query. 
    Args:
        query (str): The search query to perform.
    Returns:
        str: The search results.
    """
    # This is where you would implement your search logic, e.g., using an API or a database query.
    # For demonstration purposes, we'll return a dummy search result.
    print(f"Performing search for query: {query}")
    return tavily.search(query=query)


tavily = TavilyClient()
llm = ChatOllama(model="gemma4:e2b", temperature=0.1)
tools = [search]
agent = create_agent(model=llm, tools=tools)

def main():
    print("Hello from aisearchagent!")
    # query = "What is the weather in Bangalore today?"
    query = "Please look for 3 job openings for senior mobile developer with AI & ML exposure in bangalore with an experience of 10+ years(Android, windows, TIZEN)."
    results = agent.invoke({"messages": [HumanMessage(content=query)]})
    print(f"Search results: {results}")


if __name__ == "__main__":
    main()
