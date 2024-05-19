import streamlit as st
import ollama
import time

### streamlit run app.py
### https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/

### Input box
prompt = st.chat_input("Enter")

if prompt:

    ### Display User Input
    with st.chat_message("user"):
        st.write(prompt)

    ### Model inference
    with st.spinner("Processing"):
        response = ollama.chat(model='llama3',
                               keep_alive=-1,
                               messages=[{
                                   "role":"user",
                                   "content":prompt
                               }])
        #st.write(response['message']['content'])