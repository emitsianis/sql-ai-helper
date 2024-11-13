from gc import callbacks

from dotenv import load_dotenv
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

from handlers.chat_model_start_handler import ChatModelStartHandler
from tools.report import write_report_tool
from tools.sql import run_query_tool, list_tables, describe_tables_tool

load_dotenv()

handler = ChatModelStartHandler()
chat = ChatOpenAI(
    callbacks=[
        handler,
        handler,
        handler,
    ]
)

tables = list_tables()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=(
            "You are an AI that has access to an SQLite db.\n"
            f"The tables in the database are: {tables}\n"
            "Do not make any assumptions about what tables exist "
            "or what columns exist. Instead use the 'describe_tables' function."
        )),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

tools = [
    run_query_tool,
    describe_tables_tool,
    write_report_tool,
]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools,
    memory=memory,
)

agent_executor("How many orders are there?")
agent_executor("Repeat the same for users.")
