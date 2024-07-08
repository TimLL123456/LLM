from turtle import onclick
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import json

### reference: [supabase in streamlit] - https://github.com/SiddhantSadangi/st_supabase_connection

login_section = st.container(border=True)
signup_section = st.container(border=True)


def change_login_status(status:bool) -> None:

    """
    Change the login_status to redirect the page
    """

    st.session_state.login_state = status

def check_username_email(string_input:str) -> bool:
    """
    Check whether the user input is username or email

    username --> True, email --> False
    """

    if "@" in string_input:
        return False
    else:
        return True

def check_valid_login(response:json,
                      email:str = None,
                      username:str = None,
                      password:str = None):
    """
    Check username/email and password if a valid login

    Valid --> True, Invalid --> False
    """

    if (email != None) and (password != None):
        email_db = response.data[0]['email']
        password_db = response.data[0]['password']

        if (email_db == email) and (password_db == password):
            return True

    elif (username != None) and (password != None):
        username_db = response.data[0]['username']
        password_db = response.data[0]['password']

        st.write(username_db, password_db)

        if (username_db == username) and (password_db == password):
            return True
        
    return False

def show_login_page():
    """
    Display the login page
    """

    with login_section:
        login_section.title("Login")

        username_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')

        if st.button("Login"):

            ### Connect to database
            conn = st.connection("supabase", type=SupabaseConnection)

            ### When user input is "username"
            if check_username_email(username_n_email):

                response = execute_query(conn.table("login_information").select("*").eq("username", username_n_email))

                if check_valid_login(response, username=username_n_email, password=password):
                    st.balloons()

            ### When user input is "email"
            else:
                response = execute_query(conn.table("login_information").select("*").eq("email", username_n_email))
                
                if check_valid_login(response, email=username_n_email, password=password):
                    st.balloons()

        if st.button("Sign up"):
            change_login_status(False)
            st.experimental_rerun()

def show_signup_page():
    """
    Display the sign up page
    """

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

        ### Display the login page
        show_login_page()
    else:

        ### Display the sign up page
        show_signup_page()


main()