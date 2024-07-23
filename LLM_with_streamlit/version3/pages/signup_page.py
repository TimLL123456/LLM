import streamlit as st
from st_supabase_connection import execute_query
import time
from Menu import menu
from tools import is_valid_signup

### Signup page config
def show_signup_page(conn):
    """
    Display the signup page
    """
    signup_section = st.container(border=True)


    with signup_section:
        signup_section.title("Sign up")

        ### Input username & eamil & password
        user_name = st.text_input(label='Username', value='', placeholder="Enter your username")
        email = st.text_input(label='Email', value='', placeholder="Enter your email")
        password = st.text_input(label='Password', value='', placeholder="Enter your password", type="password")
        retype_password = st.text_input(label='Confirm password', value='', placeholder="Confirm your password", type="password")


        ### When (user_name not null), (email valid), (password == retype_password)
        if st.button("Create") and is_valid_signup(user_name, email, password, retype_password):
            
            execute_query(conn.table("login_information").insert([{"username":user_name, "email":email, "password":password}], count="None"), ttl=0)
            
            st.toast("Account create successful")
            time.sleep(1)

            st.session_state.login_state = "login"
            st.switch_page("pages/login_page.py")


menu()
show_signup_page(st.session_state.connection)
