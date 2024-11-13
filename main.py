from dotenv import load_dotenv
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

from tools.sql import run_query_tool, list_tables, describe_tables_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
print(tables)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content=f"You are an AI that has access to an SQLite db.\n{tables}"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [
    run_query_tool,
    describe_tables_tool,
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
)

agent_executor("How many users have provided a shipping address?")
