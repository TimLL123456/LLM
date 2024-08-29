import toml
import streamlit as st
from supabase import create_client, Client
from Menu import menu


@st.cache_resource
def connect_database() -> None:
    """
    Link to .toml file, Connect to supabase
    """
    data = toml.load(".streamlit/secrets.toml")


    supa_url = data["connections"]["supabase"]["SUPABASE_URL"]
    supa_key = data["connections"]["supabase"]["SUPABASE_KEY"]
    supabase: Client = create_client(supa_url, supa_key)

    return supabase

if __name__ == "__main__":
    ### login_state: (login, signup, verified)
    if "login_state" not in st.session_state:
        st.session_state.login_state = "login"


    if "user_info" not in st.session_state:
        st.session_state.user_info = None


    ### Connect to database
    conn = connect_database()
    if "connection" not in st.session_state:
        st.session_state.connection = conn


    ### Display the sidebar menu on each page
    menu()