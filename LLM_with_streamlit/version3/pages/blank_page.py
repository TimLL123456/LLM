import streamlit as st
from Menu import menu

if st.session_state.login_state == "verified":
    st.write("Welcome, Please start booking")

menu()