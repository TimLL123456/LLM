import streamlit as st
import time
from Menu import menu


### Signout page config
def show_logout_page():
    """
    Display the signup page
    """
    logout_section = st.container(border=True)


    with logout_section:
        logout_section.title("Logout")


        ### Logout
        if st.button("Logout"):
            st.toast("Logout successful")
            time.sleep(1)

            st.session_state.login_state = "login"
            st.switch_page("pages/login_page.py")

menu()
show_logout_page()