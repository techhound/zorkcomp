import streamlit as st
from streamlit_chat import message
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    # setup streamlit page
    st.set_page_config(
        page_title="Compliance Scenarios",
        page_icon="🤖"
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0, model="gpt-4o")

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=""""I want to create a Zork-like text adventure game for compliance training focused on the risk area of financial crimes within a corporation. The game should be from the perspective of office colleagues rather than a compliance officer. The objective is to teach players about the impact of financial crimes and how people may unknowingly violate regulations.
Here are the details:
1. Setting: The game is set in a modern corporate office of a company called Crestfield Industries, known for its innovative products.
2. Player Character: The player is Alex, a diligent office employee.
3. Gameplay Elements:
- Exploration: Players navigate through various office locations such as meeting rooms, break rooms, the finance department, and personal workspaces.
- Interaction: Players interact with different colleagues, including the helpful finance officer, the overly ambitious project manager, and other office staff, each providing clues or misleading information.
- Decision-Making: Players make choices during conversations and tasks that affect the game's outcome.
- Discovery: Players uncover hidden documents, suspicious transactions, and covert communications.
4. Key Scenarios:
- The Expense Report: A colleague submits a suspiciously high expense report. Players must decide whether to approve it, ask for clarification, or report it.
- The Vendor Contract: During a meeting, a senior manager insists on choosing a specific vendor despite higher costs. Players must decide whether to agree, raise concerns, or investigate the vendor.
- The Gift Offer: Players receive an expensive gift from a potential client before a major contract decision. They must decide whether to accept it, decline politely, or report the offer.
5. Learning Objectives:
- Understand various forms of financial crimes within a corporation.
- Recognize signs and red flags of financial misconduct.
- Learn the importance of ethical decision-making and potential consequences.
- Develop strategies for reporting and addressing suspected financial crimes.
6. Ending: The game concludes with a summary of decisions and their impact on the company, highlighting key learnings and providing tips for real-world application.
Using this prompt, please create a detailed Zork-like text adventure game script, including dialogue, decision points, and descriptions of scenarios.
            REALLY IMPORTANT!!! Do not play out the scenario yourself. Start the game for the user to play!""")
        ]

    st.header("Scenario Blueprints! 🤖")

    # pdf = st.file_uploader("Upload your Scenario Blueprint (PDF)", type='pdf')
    # if pdf is not None:
    #     pdf_reader = PdfReader(pdf)
    #     text = ""
    #     for page in pdf_reader.pages:
    #         text += page.extract_text()

    #     # Set the PDF content as the first system message
    #     st.session_state.messages.append(SystemMessage(content=text))
    
    # sidebar with user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")

        # handle user input
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))

    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages):
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True, key=str(i) + '_user')
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
