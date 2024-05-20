import streamlit as st
import ollama
import time

### streamlit run app.py
### https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/
### https://decoder.sh/videos/llm-chat-app-in-python-w_-ollama_py-and-streamlit
### All will be rerun

model = "llama3"

def create_chat_record(role:str, prompt:str) -> dict:
    """
    Generate chat records
    """
    return {"role":role, "content":prompt}

### Function: Generate model output
def model_inference(prompt: str, stream_mode: bool = True):
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
    response = ollama.chat(model=model,
                            messages=[create_chat_record("user", prompt)],
                            stream=stream_mode,
                            keep_alive=-1)
    
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

##############################################################################
##############################################################################

### Initialize session state
if "message" not in st.session_state.keys():
    first_chat = create_chat_record("assistent", "What can i help you?")
    st.session_state.message = [first_chat]



### Display chat history
display_chat_history()

### Setup sidebar
with st.sidebar:
    ### Stream mode
    stream_mode = st.toggle("Stream mode", value=True)
    if stream_mode:
        st.write("stream mode - ON")
    else:
        st.write("stream mode - OFF")

### Create input box
prompt = st.chat_input("Type and Press Enter!")

if prompt:

    ### Display user input
    with st.chat_message("user", avatar="😜"):
        st.markdown(prompt)
    ### Append chat record into session state
    st.session_state.message.append(create_chat_record("user", prompt))

    with st.status("In progress..."):
        time.sleep(0.1)

    ### Display model output
    with st.chat_message(model, avatar="🦙"):
        if stream_mode:
            stream_response = st.write_stream(model_inference(prompt, stream_mode))
            ### Append chat record into session state
            st.session_state.message.append(create_chat_record("assistant", stream_response))
        else:
            response = model_inference(prompt, stream_mode)
            st.write(response)
            ### Append chat record into session state
            st.session_state.message.append(create_chat_record("assistant", response))

print("@*#&(*@#&(*@#&(*@)))")