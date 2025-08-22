import os 
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_chroma import Chroma 
from langchain.chains.combine_documents import create_stuff_documents_chain  
from langchain_openai import ChatOpenAI
import streamlit as st 

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="HR_BOT"
os.environ["LANGSMITH_ENDPOINT"]=os.getenv("LANGSMITH_ENDPOINT")

llm=ChatOpenAI(model="gpt-5")

embedding=OpenAIEmbeddings(model="text-embedding-3-large")

db2=Chroma(persist_directory="../vector_data/hr_csv",embedding_function=embedding)

retriever=db2.as_retriever()

prompt = ChatPromptTemplate.from_template(
    """

    <user_input>
    {input}
    </user_input>

    You are **FinSolve HR**, a professional and friendly HR assistant for the FinSolve company.
    - answer question of user using below context 
    - answer qestion structure format 
    - provide answer asked by user, if not found, say "I don't know".
    
    <context>
    {context}
    </context>
    """
)


chain=create_stuff_documents_chain(llm,prompt)



# Streamlit framework

st.title("FinSolve HR Chatbot")
st.write("Welcome to the FinSolve HR Chatbot! How can I assist you today?")
input_text=st.text_input("what question for HR bot ??")
if input_text:
    st.write(chain.invoke({"input":input_text,"context":retriever.get_relevant_documents(input_text)}))