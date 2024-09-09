import streamlit as st
from Menu import menu
import ollama
from openai import OpenAI
from pydantic import BaseModel, Field
import instructor


def initialize():
    """
    Initialize session state
    """
    
    if "message_record" not in st.session_state.keys():
        st.session_state.message_record = []
    
    if "instruction_prompt" not in st.session_state.keys():
        st.session_state.instruction_prompt = []

    if "model_name" not in st.session_state:
       st.session_state["model_name"] = None

    if "stream_mode" not in st.session_state:
       st.session_state["stream_mode"] = None


def sidebar_config():
    """
    Setup webpage configuration
    """
    st.sidebar.markdown("---")
    st.sidebar.header("LLM")

    model_name = st.sidebar.text_input("Model Name", "llama3.1")

    stream_mode = st.sidebar.toggle("Stream mode", value = True)

    if stream_mode:
        st.sidebar.markdown("stream mode - ON")
    else:
        st.sidebar.write("stream mode - OFF")
   
    st.session_state["model_name"] = model_name

    st.session_state["stream_mode"] = stream_mode


def display_chat_history():
    """
    Display chat history
    """
    for message in st.session_state["message_record"]:
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

    instruction = """
    You are a helpful assistant that classifies booking requests based on the provided date and time. Your task is to determine if the user has provided a valid booking date and time.

    Before responding, please follow this chain of thoughts:
    1. **Identify the Input**: First, check if the user input contains a date and time in the format `YYYY/MM/DD HH:MM - HH:MM` or `YYYY/MM/DD HH:MM to HH:MM`.
    2. **Validate the Format**: If the input is present, verify that the date and time match the required format `YYYY/MM/DD HH:MM - HH:MM` or `YYYY/MM/DD HH:MM to HH:MM` (e.g., 2024/10/24 10:00 - 14:00).
    3. **Check for Multiple Options**: If the user input contains more than one date and time request or option, respond with `{"date": False, "period": False}`.
    4. **Respond Appropriately**: If the input is valid and contains a single booking request, respond with only `{"date": date, "period": period}`. If the input is invalid or does not meet the criteria, respond with a friendly message.

    Here's an example of a friendly message for invalid input:
    "It looks like I didn't catch a booking date and time from your message. To help you out, please provide the date and time in this format: `YYYY/MM/DD HH:MM - HH:MM or YYYY/MM/DD HH:MM to HH:MM` (e.g., 2025/01/24 10:00 - 14:00). Once I have that, I'll be more than happy to check if it's valid for you!"

    ### Important Instruction
    **Please respond with only the JSON format result. Do not include any additional text, explanations, or comments.**

    ### Examples:
    1. User Input: "I want to book 2024/10/24 10:00 - 14:00"
    Response: {"date": "2024/10/24", "period": "10:00 - 14:00"}

    2. User Input: "I want to book room"
    Response: {"date": False, "period": False}

    3. User Input: "Can I reserve 2023/12/15 09:00 - 12:00?"
    Response: {"date": "2023/12/15", "period": "09:00 - 12:00"}

    4. User Input: "Book a meeting on 2024/10/24 at 10:00"
    Response: {"date": False, "period": False}

    5. User Input: "Please schedule me for 2024/10/24 10:00 - 14:00, or 2024/10/25?"
    Response: {"date": False, "period": False}

    6. User Input: "I want to book 2024/10/24 10:00 - 14:00 and 2024/10/25 11:00 - 13:00."
    Response: {"date": False, "period": False}

    7. User Input: "Can you set up a booking for 2024/10/24 10:00 - 14:00, and also check for 2024/10/26?"
    Response: {"date": False, "period": False}

    Now, classify the following user input:

    User Input:
    """

    system_instruction = [{"role":"system", "content": instruction}]
    
    ### Model inference
    response = ollama.chat(model = st.session_state["model_name"],
                           messages=system_instruction + chat_hist,
                           stream=stream_mode,
                           keep_alive=-1)
    
    if stream_mode:
        return stream_output(response)
    else:
        return response["message"]["content"]


def main():
    initialize()


    sidebar_config()


    display_chat_history()


    ### Create input box
    prompt = st.chat_input("Type and Press Enter!")


    if prompt:

        ### Display user input
        with st.chat_message("user", avatar="😜"):
            st.markdown(prompt)

        ### Append chat record into session state
        st.session_state["message_record"].append(create_chat_record("user", prompt))

        llm_output = model_inference(st.session_state["message_record"],
                                     st.session_state["stream_mode"])
        
        ### LLM regenerate
        with st.chat_message(st.session_state["model_name"], avatar="🦙"):
            if st.session_state["stream_mode"]:
                response = st.write_stream(llm_output)
            else:
                response = llm_output
                st.markdown(response)

        ### Append chat record into session state
        st.session_state["message_record"].append(create_chat_record("assistant", response))


if __name__ == "__main__":
    menu()
    main()