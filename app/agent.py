from dotenv import load_dotenv
import os
from prompts import context
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from engines.agro_engine import cards_engine, deposits_engine, transfer_engine, credits_engine
from llama_index.llms.groq import Groq


load_dotenv()

tools = [
    QueryEngineTool(
        query_engine=cards_engine,
        metadata=ToolMetadata(
            name="cards_data",
            description="This tool provides access to detailed information about various cards.",
        )
    ),
    QueryEngineTool(
        query_engine=deposits_engine,
        metadata=ToolMetadata(
            name="deposits_data",
            description="This tool provides access to detailed information about various deposits.",
        )
    ),
    QueryEngineTool(
        query_engine=transfer_engine,
        metadata=ToolMetadata(
            name="transfer_data",
            description="This tool provides access to detailed information about various transfers.",
        )
    ),
    QueryEngineTool(
        query_engine=credits_engine,
        metadata=ToolMetadata(
            name="credits_data",
            description="This tool provides access to detailed information about various credits.",
        )
    ),
]

try:
    groq_client = Groq(
        model="llama3-8b-8192",
        api_key=os.getenv('GROQ_API_KEY'),
    )
except Exception as e:
    raise e


agent = ReActAgent.from_tools(
    tools,
    llm=groq_client,
    verbose=True,
    context=context
)
