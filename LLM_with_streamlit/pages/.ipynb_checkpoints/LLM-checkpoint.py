import streamlit as st
import ollama
import time
from openai import OpenAI
from pydantic import BaseModel, Field
import instructor
from datetime import datetime

### streamlit run app.py
### https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/
### https://decoder.sh/videos/llm-chat-app-in-python-w_-ollama_py-and-streamlit
### All will be rerun

model_name = "llama3"

### Set page tab config
st.set_page_config(
    page_title="LLM",
    page_icon="👋",
)

### Display the model using
st.title(model_name)

### Create a header of this page in sidebar
st.sidebar.header("LLM")

def create_chat_record(role:str, prompt:str) -> dict:
    """
    Generate chat records
    """
    return {"role":role, "content":prompt}

### Function: Generate model output
def model_inference(chat_hist: list, stream_mode: bool = True):
    """
    Generate model output in 2 mode: stream or not stream
    """
    def stream_output(response:str):
        """
        Isolated function for using the "yield" to output the stream response,
        Cannot use "yield" function together with "return" function (return --> [], empty object)
        """
        for resp in response:
            yield resp['message']['content']

    ### Model inference
    response = ollama.chat(model=model_name,
                            messages=chat_hist,
                            stream=stream_mode,
                            keep_alive=-1,)
    
    ### Output stream or not stream response
    if stream_mode:
        return stream_output(response)
    else:
        return response['message']['content']
    
def display_chat_history():
    """
    Display chat history
    """
    for message in st.session_state["message"]:
        if message['role'] == 'assistant':
            with st.chat_message(message["role"], avatar="🦙"):
                st.markdown(message["content"])
        elif message['role'] == 'user':
            with st.chat_message(message["role"], avatar="😜"):
                st.markdown(message["content"])

def structured_llm_output(query:str):
    """
    Standardize LLM output in json format
    """
    class output(BaseModel):
        date: str = Field(..., description="Get the date of booking from user input",
                          examples=["2-2-2024", "None", "check"])
        period: str = Field(..., description="Get the period of booking from user input")

    client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="Ollama"
    ),
    mode=instructor.Mode.JSON,
    )

    today = datetime.now().strftime("%Y-%m-%d, %A")

    prompt = """
    Instruction:
    - Return the date and period based on the user input.
    - If user input only day Name without exact date (e.g., Monday), return "None" in date
    - You must follow below examples as reference to answer question.
    - If user do not provide a clear date and period, return "None" in date and period.
    - If user ask for available period or what period / time / vacancy can book, return "check" in period.
    - User are only to book 1 hour. If user ask for booking more than 1 hour, return "None"
    ----------------------------------------------------------------
    ### Example of unclear date and period
    Qurestion: Any Booking available at Wednesday / Good morning / Hi
    return: {'date' = 'None', 'period'= 'None'}

    ### Example of check vacancy
    Qurestion: Any vacancy at 1-6-2024
    return: {'date' = '1-6-2024', 'period'= 'check'} 

    ### Example of time period conversion
    Qurestion: I want to book at 1/6/2022 from 05:00 pm - 06:00 pm
    return: {'date' = '1/6/2022', 'period' = '17:00 - 18:00'}
    ----------------------------------------------------------------
    Query:
    """

    response = client.chat.completions.create(
        model='llama3',
        messages=[
            {
                "role": "user",
                "content": prompt + query
            }
        ],
        response_model=output,
        max_retries=3
    )
    st.write(response)
    return response



##############################################################################
##############################################################################

### Initialize session state
if "message" not in st.session_state.keys():
    st.session_state.message = []

if "instruction_prompt" not in st.session_state.keys():
    st.session_state.instruction_prompt = []

if "token" not in st.session_state.keys():
    st.session_state.token = 0

### Display chat history
display_chat_history()

### Setup sidebar
with st.sidebar:
    ### Stream mode
    stream_mode = st.toggle("Stream mode", value=True)
    if stream_mode:
        st.markdown("stream mode - ON")
    else:
        st.write("stream mode - OFF")

instruction = f"""
Instruction:
- If user do not provide a clear date and period, ask the user to give a clear and exact date and period. (e.g., 2024/3/1, 11:00 - 12:00)
- User are only to book 1 hour. If user ask for booking more than 1 hour, tell the user only can book 1 hour.

Here is the recommendation period that system found. Please recommend the the user to select these period:
09:00 - 10:00
12:00 - 13:00

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

    structure_response = structured_llm_output(prompt)

    if structure_response.date == "None" or structure_response.period == "None":
        with st.chat_message(model_name, avatar="🦙"):
            st.write_stream(model_inference(st.session_state.instruction_prompt, stream_mode))
    elif structure_response.date == "check" or structure_response.period == "check":
        st.write("check available booking")
    else:
        st.write(structure_response.date, structure_response.period)
        st.write("Booking the timeslot for you")

    with st.status("In progress..."):
        time.sleep(0.1)

    ### Display model output
    #with st.chat_message(model_name, avatar="🦙"):
        #if stream_mode:
        #    stream_response = st.write_stream(model_inference(st.session_state.message, stream_mode))
        #    ### Append chat record into session state
        #    st.session_state.message.append(create_chat_record("assistant", stream_response))
        #else:
        #    response = model_inference(st.session_state.message, stream_mode)
        #    st.write(response)
        #    ### Append chat record into session state
        #    st.session_state.message.append(create_chat_record("assistant", response))

### Count tokens
#token_list = [len(i['content'].split()) for i in st.session_state.message]
#for num_token in token_list:
#    st.session_state.token += num_token

### Display current tokens in sidebar
#st.sidebar.write(f"Number of tokens: {st.session_state.token}")