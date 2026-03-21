import pandas as pd
import streamlit as st
from db import get_connection

st.set_page_config(page_title="FDR — FPL Advisor", layout="wide")

conn = get_connection()

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------
MATCH_KEYS = ["first", "second", "third", "fourth", "fifth"]
DISPLAY_LABELS = ["Match 1", "Match 2", "Match 3", "Match 4", "Match 5"]

DIFFICULTY_COLORS = {
    1: "#2ca02c",  # D3 green
    2: "#98df8a",  # D3 light green
    3: "#ffe0b2",  # soft amber
    4: "#ff9896",  # D3 light red
    5: "#d62728",  # D3 red
}


@st.cache_data(ttl=3600)
def load_fdr():
    return conn.query("SELECT * FROM gold.fdr ORDER BY team")


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
st.title("Fixture Difficulty Rating")
st.caption("Next 5 fixtures per team, color-coded by difficulty")

fdr = load_fdr()

# Build HTML table
rows_html = ""
for _, row in fdr.iterrows():
    cells = f'<td style="font-weight:bold; padding:8px 12px;">{row["team"]}</td>'
    for key in MATCH_KEYS:
        opp = row.get(f"{key}_opponent", "")
        diff = row.get(f"{key}_opponent_difficulty")
        if opp and pd.notna(diff):
            bg = DIFFICULTY_COLORS.get(int(diff), "#333")
            cells += f'<td style="background-color:{bg}; color:#000; padding:8px 12px; text-align:center;">{opp}</td>'
        else:
            cells += '<td style="padding:8px 12px;"></td>'
    rows_html += f'<tr style="border-bottom:1px solid #555;">{cells}</tr>'

header_cells = '<th style="padding:8px 12px; text-align:left;">Team</th>'
for label in DISPLAY_LABELS:
    header_cells += f'<th style="padding:8px 12px; text-align:center;">{label}</th>'

html = f"""
<table style="width:100%; border-collapse:collapse; font-size:14px;">
    <thead><tr style="border-bottom:2px solid #555;">{header_cells}</tr></thead>
    <tbody>{rows_html}</tbody>
</table>
"""

st.markdown(html, unsafe_allow_html=True)
