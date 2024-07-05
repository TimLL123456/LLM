from turtle import onclick
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import json

### reference: [supabase in streamlit] - https://github.com/SiddhantSadangi/st_supabase_connection

# conn = st.connection("supabase", type=SupabaseConnection)

# result = execute_query(conn.table("login_information").select("*").eq("email", "testuser1@example.com"))

# print(result.data)

login_section = st.container(border=True)
signup_section = st.container(border=True)


def change_login_status(status):
    st.session_state.login_state = status

def show_login_page():

    with login_section:
        login_section.title("Login")

        user_name_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')

        st.button("Login")

        if st.button("Sign up"):
            change_login_status(False)
            st.experimental_rerun()

def show_signup_page():
    with signup_section:
        signup_section.title("Sign up")

        user_name = st.text_input(label='Username', value='', placeholder="Enter your username")
        email = st.text_input(label='Email', value='', placeholder="Enter your email")
        password = st.text_input(label='Password', value='', placeholder="Enter your password")
        retype_password = st.text_input(label='Confirm password', value='', placeholder="Confirm your password")

        st.button("Create")

        if st.button("Back"):
            change_login_status(True)
            st.experimental_rerun()

def main():
    if "login_state" not in st.session_state:
        st.session_state.login_state = True

    if st.session_state.login_state:
        show_login_page()
    else:
        show_signup_page()


main()