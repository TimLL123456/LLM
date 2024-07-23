import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from Menu import menu
from st_supabase_connection import execute_query


# execute_query(st.session_state.connection.table("booking_history").select("*"), ttl=0)


def main():

    st.title("📅 Booking System GUI")

    ### Display date input box
    date = st.date_input("Select a date", value=None)

    if date:
        pass


menu()
main()