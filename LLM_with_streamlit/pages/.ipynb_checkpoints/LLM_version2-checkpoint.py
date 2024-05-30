import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime

def main():
    ### Set page tab config
    st.set_page_config(page_title="Booking System version2",
                       page_icon="📅")

    st.title("📅 Booking System version2")

    