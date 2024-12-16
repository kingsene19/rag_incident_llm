import chainlit as cl
from chainlit.types import ThreadDict
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.runnable.config import RunnableConfig
from langchain.memory import ConversationBufferWindowMemory
from utils.user_info import verify_user
from utils.retriever import retrieve
from utils.prompts import CONTEXT_PROMPT, SYSTEM_PROMPT
from operator import itemgetter
import re
import json

import warnings
warnings.filterwarnings("ignore")

llm = ChatOpenAI(
  openai_api_base="",
  model = "llama-3.3-70b-versatile",
  temperature=1,
  api_key=""
)

def setup_runnable():
  memory = cl.user_session.get("memory")

  runnable_context = RunnablePassthrough.assign(
    chat_history = RunnableLambda(memory.load_memory_variables) | itemgetter("history")
  ) | CONTEXT_PROMPT | llm | StrOutputParser()

  runnable = (
      RunnablePassthrough.assign(
          question = runnable_context,
          industries = RunnableLambda(get_industry)
      )
      | retrieve
      | SYSTEM_PROMPT
      | llm
      | StrOutputParser()
  )
  cl.user_session.set("runnable", runnable)

def get_industry(input):
  return input['industries']

@cl.password_auth_callback
def auth_callback(username: str, password: str):
  user, verified = verify_user(username, password)
  if verified:
    return cl.User(
        identifier=user['user'], metadata=user
    )
  else:
    raise ValueError("Invalid username or password")

@cl.on_chat_start
async def on_chat_start():
  cl.user_session.set("memory", ConversationBufferWindowMemory())
  user = cl.user_session.get("user")
  if user.metadata['role'] == 'admin':
      cl.user_session.set('industries', 'all')
  else:
    cl.user_session.set("industries", user['industries'])
  setup_runnable()


@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
  memory = ConversationBufferWindowMemory(return_messages=True)
  root_messages = [m for m in thread["steps"] if m["parentId"] == None]
  for message in root_messages:
      if message["type"] == "user_message":
          memory.chat_memory.add_user_message(message["output"])
      else:
          memory.chat_memory.add_ai_message(message["output"])
  cl.user_session.set("memory", memory)
  setup_runnable()


@cl.on_message
async def on_message(message: cl.Message):
  memory = cl.user_session.get("memory")
  runnable = cl.user_session.get("runnable")
  res = cl.Message(content="")
  async for chunk in runnable.astream(
      {"question": message.content, "industries": cl.user_session.get('industries')},
      config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
  ):
    await res.stream_token(chunk)
  await res.send()
  memory.chat_memory.add_user_message(message.content)
  memory.chat_memory.add_ai_message(res.content)
