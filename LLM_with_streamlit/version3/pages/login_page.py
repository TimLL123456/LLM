import streamlit as st
from st_supabase_connection import execute_query
import time
from Menu import menu
from tools import is_username, is_valid_login

### Login page config
def show_login_page(conn):
    """
    Display the Login page
    """
    login_section = st.container(border=True)


    with login_section:
        login_section.title("Login")

        ### Input username/eamil & password
        username_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')


        if st.button("Log in") and username_n_email != "" and password != "":

            ### When user input is "username"
            if is_username(username_n_email):

                response = execute_query(conn.table("login_information").select("*").eq("username", username_n_email))

                if is_valid_login(response, username=username_n_email, password=password):

                    st.toast("Login successful")
                    time.sleep(1)

                    st.session_state.login_state = "verified"
                    st.switch_page("pages/blank_page.py")


            ### When user input is "email"
            else:
                response = execute_query(conn.table("login_information").select("*").eq("email", username_n_email))

                if is_valid_login(response, email=username_n_email, password=password):

                    st.toast("Login successful")
                    time.sleep(1)

                    st.session_state.login_state = "verified"
                    st.switch_page("pages/blank_page.py")


menu()
show_login_page(st.session_state.connection)