#setting up api for groq and tavil
import os
from dotenv import load_dotenv 
from langgraph.prebuilt import create_react_agent


load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

#setting up the llm and tools
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages.ai import AIMessage

openai_llm = ChatOpenAI(model = "gpt-4o-mini", api_key=OPENAI_API_KEY)
groq_llm = ChatGroq(model = "llama-3.3-70b-versatile",api_key = GROQ_API_KEY)
tavily_search = TavilySearchResults(max_result= 2,api_key= TAVILY_API_KEY)


#set up ai agent with search functionality
system_prompt = "Act like a AI chatbot who is very smart and user friendly"

def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)
    tools=[TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_react_agent(
        model = llm,
        tools = [tavily_search], 
        state_modifier=system_prompt 
    )

    query = query
    # state = {"message": query}
    # praiser = StrOutputParser()
    # chain = agent | praiser
    # messages = chain.invoke(state)
    # ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    # return ai_messages[-1]
    state={"messages": query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]
