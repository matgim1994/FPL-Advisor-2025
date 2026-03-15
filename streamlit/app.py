import streamlit as st
from db import get_connection

st.set_page_config(page_title="FPL Advisor", layout="wide")

st.title("FPL Advisor")
st.write("Fantasy Premier League analytics dashboard.")

# DB health check
try:
    conn = get_connection()
    conn.query("SELECT 1", ttl=0)
except Exception as e:
    st.error(f"Database connection failed: {e}")
