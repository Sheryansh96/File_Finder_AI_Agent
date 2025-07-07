#main.py
# from langchain_community.llms import Ollama
# from langchain.agents import initialize_agent, AgentType
# from tool import search_pdfs_semantic
# from langgraph.prebuilt import create_react_agent
# from llama_llm import llm
# import time


# agent = create_react_agent(llm, tools = [search_pdfs_semantic])

# def main():
#     print("📁 AI PDF Search Agent is ready!")
#     while True:
#         query = input("\nAsk me to find a PDF (or type 'exit'): ")
#         if query.lower() == "exit":
#             break
#         try:
#             start = time.time()
#             response = agent.invoke({"messages": query})
#             end = time.time()
#             for message in response['messages']:
#                 message.pretty_print()
#             print("\n⏱️ Runtime: {:.2f} seconds".format(end - start))
#         except Exception as e:
#             print(f"⚠️ Error: {e}")

# if __name__ == "__main__":
#     main()


# main.py
from langgraph.prebuilt import create_react_agent
from pdf_semantic_agent import hybrid_pdf_search
from llama_llm import llm
import time

agent = create_react_agent(llm, tools=[hybrid_pdf_search])

def main():
    print("📁 Hybrid AI PDF Agent is ready!")
    while True:
        query = input("\nAsk me to find a PDF (or type 'exit'): ")
        if query.lower() == "exit":
            break
        try:
            # start = time.time()
            response = agent.invoke({"messages": query})
            # end = time.time()
            for message in response['messages']:
                message.pretty_print()
            # print("\n⏱️ Runtime: {:.2f} seconds".format(end - start))
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
