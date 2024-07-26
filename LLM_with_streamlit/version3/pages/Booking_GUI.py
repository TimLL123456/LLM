import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from Menu import menu
from tools import *
from st_supabase_connection import execute_query
from datetime import date, datetime


### Booking range: today + 1 month
class system_info:
    today = date.today()
    max_day = datetime(today.year, today.month+1, today.day)
    period = (7, 23)
    conn = st.session_state.connection
    curr_user_id = st.session_state.user_info["user_id"]


def main():

    st.title("📅 Booking System GUI")


    ### Display date input box
    date = st.date_input("Select a date",
                         value=system_info.today,
                         min_value=system_info.today,
                         max_value=system_info.max_day)


    if date:
        ### Check date available in database
        response = execute_query(system_info.conn.table("booking_history").select("*").eq("date", date),ttl=0)
        

        ### While response not empty
        if response.data:
            pass

            ### Construct dataframe template & merge database response to template
            # data = show_db_data(response.data)
            # template_df = data.construct_template(system_info.period)
            # booking_record = data.merge_data(date, template_df)
        
        else:
            

menu()
main()