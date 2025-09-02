from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain.tools import tool

load_dotenv()

@tool
def calculator(a: int ,b: int) -> str:
    """doing basic arithmetic operations like sum on numbers"""
    # print(f"calc done on {a} and {b}")
    return f"{a} + {b} = {a+b}"

@tool
def greet(a: str) -> str:
    """used for greeting a user"""
    return "hey dude, I'm your AI!"

def main():
    model = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2)
    tools=[calculator,greet]
    agent_executor=create_react_agent(model,tools)
    print("Hey I'm your AI bot ,can help you anytime!")
    while True:
        user_input=input("\nYou: ").strip()
        if user_input=="quit":
            break
        print("\nAssistant:",end="")
        for chunk in agent_executor.stream({"messages":[HumanMessage(content=user_input)]}):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="");
        print()
if __name__=="__main__":
    main()