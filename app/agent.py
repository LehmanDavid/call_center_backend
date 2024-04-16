from dotenv import load_dotenv
import os
from prompts import context
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms import openai
from engines.agro_engine import cards_engine, deposits_engine, transfer_engine, credits_engine


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

llm = openai.OpenAI(model="gpt-3.5-turbo-0613",
                    api_key=os.getenv('OPENAI_API_KEY'),
                    max_tokens=512,
                    temperature=0.7,
                    )

agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)
