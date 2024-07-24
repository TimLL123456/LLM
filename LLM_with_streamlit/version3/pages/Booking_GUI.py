import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from Menu import menu
from tools import gen_period
from st_supabase_connection import execute_query
from datetime import date, datetime


### Booking range: today + 1 month
class system_info:
    today = date.today()
    max_day = datetime(today.year, today.month+1, today.day)


class template:
    df = {"user_id":None,
          "date": None,
          "period": gen_period(7, 23),
          "vacancy": None}


def main():

    st.title("📅 Booking System GUI")


    ### Display date input box
    date = st.date_input("Select a date",
                         value=system_info.today,
                         min_value=system_info.today,
                         max_value=system_info.max_day)


    ### Check available period in that day
    if date:
        response = execute_query(st.session_state.connection.table("booking_history").select("*").eq("date", date),ttl=0)
        st.code(response.data)


menu()
main()