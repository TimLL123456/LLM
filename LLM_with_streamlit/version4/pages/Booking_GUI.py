import streamlit as st
from Menu import menu
from datetime import date, datetime


class system_info:
    today = date.today()
    max_day = datetime(today.year, today.month+1, today.day)
    period = (7, 23)


def GUI():
    st.title("📅 Booking System GUI")


    ### Display date input box
    select_date = st.date_input("Select a date",
                            # value=system_info.today,
                            # min_value=system_info.today,
                            value=datetime(2024, 8, 4).date(),
                            min_value=datetime(2024, 8, 4).date(),
                            max_value=system_info.max_day)

    
    start_options = [f"{i:02}:00" for i in range(system_info.period[0], system_info.period[1]+1)]
    start_time = st.selectbox("Select start time", start_options, index=None)


    if start_time:

        end_time_range = int(start_time.split(":")[0]) + 1
        end_options = [f"{i:02}:00" for i in range(end_time_range, 24)]
        end_time = st.selectbox("Select end time", end_options, index=None)


        ### Find if any start time < user select end time & end time > user select start time
        ### |------|       |------|
        ### 8      10      11     13
        ### No record in database, available booking period
        response = st.session_state.connection.table("bookings").select("*")\
                                              .eq("booking_date", select_date)\
                                              .lt("booking_starttime", end_time)\
                                              .gt("booking_endtime", start_time).execute()


        if response.data == []:
            ### Booking function
            pass
        else:
            ### Recommendation
            pass


if __name__ == "__main__":
    menu()
    GUI()