##################################### Reference #####################################
### https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/
### https://decoder.sh/videos/llm-chat-app-in-python-w_-ollama_py-and-streamlit
#####################################################################################
import streamlit as st
import ollama
from openai import OpenAI
from pydantic import BaseModel, Field
import instructor
import re
import pandas as pd

import sys
sys.path.append('/media/admin1/ea78b76e-5f68-4af3-a29b-36a4428c73a0/myfile/LLM/00_my_llm/LLM/LLM/LLM_with_streamlit/tool')
from tools import mytools

def check_valid_date(date_str: str):
    """
    Return True if the date is valid in pattern (YYYY-MM-DD)
    """
    
    return re.search("\d{4}-\d{2}-\d{2}", date_str) != None

def check_valid_time(time_str: str):
    """
    Return True if the time is valid in pattern (HH:SS-HH:SS)
    """
    
    return re.search("\d{2}:00-\d{2}:00", time_str) != None

def set_config():
    """
    Setup webpage configuration
    """
    
    global model_name
    model_name = "llama3"
    
    ### Set page tab config
    st.set_page_config(
        page_title = "LLM",
        page_icon = "👋",
    )
    
    ### Display the model using
    st.title(model_name)
    
    ### Create a header of this page in sidebar
    st.sidebar.header("LLM")
    
    ### Setup sidebar
    with st.sidebar:
        
        ### Stream mode
        global stream_mode
        stream_mode = st.toggle("Stream mode", value = True)
        
        if stream_mode:
            st.markdown("stream mode - ON")
        else:
            st.write("stream mode - OFF")

def initialize():
    """
    Initialize session state
    """
    
    if "message" not in st.session_state.keys():
        st.session_state.message = []
    
    if "instruction_prompt" not in st.session_state.keys():
        st.session_state.instruction_prompt = []
        
    if "token" not in st.session_state.keys():
        st.session_state.token = 0
    
def display_chat_history():
    """
    Display chat history
    """
    for message in st.session_state["message"]:
        if message["role"] == "assistant":
            with st.chat_message(message["role"], avatar="🦙"):
                st.markdown(message["content"])
        elif message["role"] == "user":
            with st.chat_message(message["role"], avatar="😜"):
                st.markdown(message["content"])
                
def create_chat_record(role:str, prompt:str) -> dict:
    """
    Generate chat records
    """
    
    return {"role":role, "content":prompt}

def structured_llm_output(query:str):
    """
    Standardize LLM output in json format
    """
    
    class output(BaseModel):
        date: str = Field(...,
                          description="Get the date of booking from user input (date format=YYYY-MM-DD",
                          examples=["2024-02-02", "None", "Check"])
        period: str = Field(...,
                            description="Get the period of the booking from user input (output format=HH:SS-HH:SS",
                            examples=["10:00-14:00", "None", "Check"])
        
    client = instructor.from_openai(
    OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key = "Ollama"
    ),
    mode = instructor.Mode.JSON
    )
    
    prompt = """
    ### Instruction:
    - Return the date and period based on the user input.
    - If the user input contains only a day name without an exact date (e.g., Monday), return "None" for the date.
    - Follow the examples below as references to answer the question.
    - If the user does not provide a clear date and period, return "None" for both date and period.
    - If the user asks for the available period or what period/time/vacancy can be booked, return "check" for the period.
    - If the user asks for availability or to check a date without providing a period, prompt them to specify a period. For example, "Please provide the time period you want to book on 2024-10-22."

    ### Examples:
    1. Unclear Date and Period
       - Question: Any booking available on Wednesday / Good morning / Hi
       - Return: {'date': 'None', 'period': 'None'}

    2. Check Vacancy
       - Question: Any vacancy on 2024-10-22
       - Return: {'date': '2024-10-22', 'period': 'check'}

    3. Time Period Conversion
       - Question: I want to book on 2024-01-12 from 03:00 PM - 06:00 PM
       - Return: {'date': '2024-01-12', 'period': '15:00-18:00'}
    
    Query:
    """
    
    response = client.chat.completions.create(
        model = 'llama3',
        messages = [
            {
                "role": "user",
                "content": prompt + query
            }
        ],
        response_model = output,
        max_retries = 3
    )
    
    st.write(response)
    
    return response

def model_inference(chat_hist: list, stream_mode: bool = True):
    """
    Generate model output in 2 mode: stream or not stream
    """
    
    def stream_output(response:str):
        """
        Isolated function for using the "yield" to output the stream response,
        Cannot user "yield" function together with "return function (return --> [], empty object)
        """
        
        for resp in response:
            yield resp["message"]["content"]
    
    ### Model inference
    response = ollama.chat(model = model_name,
                           messages=chat_hist,
                           stream=stream_mode,
                           keep_alive=-1)
    
    if stream_mode:
        return stream_output(response)
    else:
        return response["message"]["content"]

def main():
    
    
    set_config()
    
    ### Initialize session state
    initialize()
    
    display_chat_history()
    
    instruction = f"""
    You are an assistant that helps customers to complete their bookings. You need to guide the customer to provide a valid date and period that they want to book. Here are the instructions you must follow for a successful booking.

    ### Instruction:
    - If the user does not provide a clear date and period, ask the user to give a clear and exact date and period. 
      - The date format should be `YYYY-MM-DD` (e.g., 2024-03-01).
      - The period format should be `HH:00-HH:00` (e.g., 09:00-17:00).

    Query:
    """
    
    ### Create input box
    prompt = st.chat_input("Type and Press Enter!")
    
    if prompt:
        
        ### Display user input
        with st.chat_message("user", avatar="😜"):
            st.markdown(prompt)
            
        ### Append chat record into session state
        st.session_state.message.append(create_chat_record("user", prompt))
        st.session_state.instruction_prompt.append(create_chat_record("user", instruction+prompt))
        
        ### Standardize and Structure LLM output
        structure_response = structured_llm_output(prompt)
        
        if structure_response.date == "None" or structure_response.period == "None":
            with st.chat_message(model_name, avatar="🦙"):
                llm_output = st.write_stream(model_inference(st.session_state.instruction_prompt, stream_mode))

            st.session_state.message.append(create_chat_record("assistant", llm_output))

        elif structure_response.date == "check" or structure_response.period == "check":
            st.write("check available booking")

        elif check_valid_date(structure_response.date) and check_valid_time(structure_response.period):
            _, df = mytools.connect_to_gspreadsheet(structure_response.date)
            df
            st.write(structure_response.date, structure_response.period)
            st.write("Booking the timeslot for you")

############################################################
############################################################
main()