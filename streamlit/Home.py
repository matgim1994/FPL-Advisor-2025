import streamlit as st
from db import get_connection

st.set_page_config(page_title="FPL Advisor", layout="wide")

# ---------------------------------------------------------------------------
# Data layer — cached queries (shared across all users, refreshed hourly)
# ---------------------------------------------------------------------------
conn = get_connection()


@st.cache_data(ttl=3600)
def load_current_gw():
    return conn.query("SELECT * FROM gold.events WHERE is_current = true")


@st.cache_data(ttl=3600)
def load_gw_results():
    return conn.query("SELECT * FROM gold.gw_results")


@st.cache_data(ttl=3600)
def load_gw_top_forwards():
    return conn.query("SELECT * FROM gold.gw_top_forwards")


@st.cache_data(ttl=3600)
def load_gw_top_midfielders():
    return conn.query("SELECT * FROM gold.gw_top_midfielders")


@st.cache_data(ttl=3600)
def load_gw_top_defenders():
    return conn.query("SELECT * FROM gold.gw_top_defenders")


@st.cache_data(ttl=3600)
def load_gw_top_goalkeepers():
    return conn.query("SELECT * FROM gold.gw_top_goalkeepers")


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
st.title("FPL Advisor")

gw = load_current_gw()

# -- Metrics row -------------------------------------------------------------
st.header(f"{gw['name'][0]}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Deadline Day", str(gw["deadline_time"][0]))
col2.metric("Average Score", int(gw["average_entry_score"][0]))
col3.metric("Highest Score", int(gw["highest_score"][0]))

# -- Gameweek Results --------------------------------------------------------
st.subheader("Results")

results = load_gw_results()
results_display = results.copy()
st.dataframe(
    results_display[["Team Home", "Team Home Score", "Team Away Score", "Team Away"]],
    use_container_width=True,
    hide_index=True,
)

# -- Top Performers ----------------------------------------------------------
st.subheader("Top Performers")

tab_fw, tab_mid, tab_def, tab_gk = st.tabs(
    ["Forwards", "Midfielders", "Defenders", "Goalkeepers"]
)

loaders = {
    tab_fw: load_gw_top_forwards,
    tab_mid: load_gw_top_midfielders,
    tab_def: load_gw_top_defenders,
    tab_gk: load_gw_top_goalkeepers,
}

for tab, loader in loaders.items():
    with tab:
        df = loader()
        df_display = df.copy()
        df_display["Player"] = df_display["First Name"] + " " + df_display["Second Name"]
        st.dataframe(
            df_display[["Player", "Team", "Total Points"]],
            use_container_width=True,
            hide_index=True,
        )
