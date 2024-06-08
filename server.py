from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_fireworks import ChatFireworks
from langserve import add_routes
import getpass

#create prompt template

system_template="Translate the following into {language}:"
prompt_template=ChatPromptTemplate.from_messages([("system",system_template),("user","{text}")])

#create model
fireworks_api_key=getpass.getpass()
model=ChatFireworks(fireworks_api_key=fireworks_api_key)

#create parser
parser=StrOutputParser()

#create chain
chain=prompt_template|model|parser

#app definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

#adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)