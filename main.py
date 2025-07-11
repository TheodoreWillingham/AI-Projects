from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv() # loads variable from env file

def main():
    model = ChatOpenAI(temperature=0) # tempature sets the randomness of the model
    
    tools = [] # fill with tools our agent can use
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm an AI assistant named Timmy created by Theo. Type 'gay' to exit.")
    print("You can ask me to perform mat hematical calculations or chat with me.")
    
    while True:
        user_input = input("\nYou: ").strip()  #.strip() gets rid of white space infront
        
        if user_input == "gay":
            break
        
        print("\nTimmy: ", end="") #this get's rid of the /n which is at the end of a python print by default
        