import streamlit as st
from st_supabase_connection import SupabaseConnection
from st_supabase_connection import execute_query

date = "2024-08-01"

conn = st.connection("supabase", type=SupabaseConnection)

response = execute_query(conn.table("bookings").select("*").eq("booking_date", date),ttl=0)

response.data