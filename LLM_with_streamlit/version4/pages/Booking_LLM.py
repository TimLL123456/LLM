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
    
    ### Model inference
    response = ollama.chat(model = st.session_state["model_name"],
                           messages=chat_hist,
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