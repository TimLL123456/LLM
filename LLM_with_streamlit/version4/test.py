import toml
import streamlit as st
from datetime import date, datetime
from supabase import create_client, Client

data = toml.load(".streamlit/secrets.toml")


supa_url = data["connections"]["supabase"]["SUPABASE_URL"]
supa_key = data["connections"]["supabase"]["SUPABASE_KEY"]
supabase: Client = create_client(supa_url, supa_key)


### Booking range: today + 1 month
class system_info:
    today = date.today()
    max_day = datetime(today.year, today.month+1, today.day)
    period = (7, 23)


st.title("📅 Booking System GUI")


### Display date input box
select_date = st.date_input("Select a date",
                        value=system_info.today,
                        min_value=system_info.today,
                        max_value=system_info.max_day)

start_options = [f"{i:02}:00" for i in range(7, 24)]
start_time = st.selectbox("Select start time", start_options, index=None)


end_options = [f"{i:02}:00" for i in range(int(start_time.split(":")[0])+1, 24)]
end_time = st.selectbox("Select end time", end_options, index=None)


### Find if any start time < user select end time & end time > user select start time
### |------|       |------|
### 8      10      11     13
### No record in database, available booking period
response = supabase.table("bookings").select("*")\
                                     .eq("booking_date", select_date)\
                                     .lt("booking_starttime", end_time)\
                                     .gt("booking_endtime", start_time).execute()


response.data