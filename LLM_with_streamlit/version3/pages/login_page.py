import streamlit as st
from st_supabase_connection import execute_query
from Menu import menu
from tools import is_username, is_valid_login


def show_login_page(conn):
    login_section = st.container(border=True)


    with login_section:
        login_section.title("Login")


        username_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')


        if st.button("Log in") and username_n_email != "" and password != "":

            ### When user input is "username"
            if is_username(username_n_email):

                response = execute_query(conn.table("login_information").select("*").eq("username", username_n_email))

                if is_valid_login(response, username=username_n_email, password=password):
                    st.session_state.login_state = "verified"
                    st.success("Login successful")
                    st.switch_page("pages/blank_page.py")




menu()
show_login_page(st.session_state.connection)