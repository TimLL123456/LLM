import streamlit as st
from st_supabase_connection import SupabaseConnection
from Menu import menu


### Connect to database
### ===================
@st.cache_resource
def connect_database():
    """
    Create connection to database
    """
    conn = st.connection("supabase", type=SupabaseConnection)
    return conn


### login_state: login, signup, verified
if "login_state" not in st.session_state:
    st.session_state.login_state = "login"


conn = connect_database()
if "connection" not in st.session_state:
    st.session_state.connection = conn


menu()