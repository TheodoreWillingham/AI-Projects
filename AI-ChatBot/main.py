from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv() # loads variable from env file

#create tools which can be used by the AI model
#we do this using a decorator


#for the parameters make sure to define a type for them( do this using colon)

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers"""
    print("Tool has been called.")
    return f"The sum of {a} and {b} is {a + b}"

@tool
def creator() -> str:
    """use this when someone asks who created you"""
    print("Tool has been called.")
    return "I have been carefully created by Theodore Willingham"
    

def main():
    model = ChatOpenAI(temperature=0) # tempature sets the randomness of the model
    
    tools = [calculator, creator] # fill with tools our agent can use
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I'm an AI assistant named Timmy created by Theo. Type 'sybau' to exit.")
    print("You can ask me to perform mathematical calculations or chat with me.")
    
    while True:
        user_input = input("\nYou: ").strip()  #.strip() gets rid of white space infront
        
        if user_input == "sybau":
            break
        
        print("\nTimmy: ", end="") #this get's rid of the /n which is at the end of a python print by default
         
        #How we call the Agent
        for chunk in agent_executor.stream( #we can stream our LLM's response from the agent_executor
            {"messages": [HumanMessage(content=user_input)]} # we give our agent input (messages: which is our userinput) HumanMessage rather than system Message
        ):
            #Chuncks are parts of responses coming from agent
            if "agent" in chunk and "messages" in chunk["agent"]: #grab all messages from agent
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="") # print all message content #steam let's it us see word by word and not just enitre string at once
        
        print() #print new line
    
if __name__ == "__main__":
    main()
                    
        
        
        