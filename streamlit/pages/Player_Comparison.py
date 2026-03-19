import streamlit as st
import plotly.express as px
from db import get_connection

st.set_page_config(page_title="Player Comparison — FPL Advisor", layout="wide")

conn = get_connection()

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------
HISTORY_COLUMNS = {
    "Total Points": "cumulative_points",
    "Points": "total_points",
    "Goals": "goals_scored",
    "xG": "expected_goals",
    "Assists": "assists",
    "xA": "expected_assists",
    "Minutes": "minutes",
    "Clean Sheets": "clean_sheets",
    "xGI": "expected_goal_involvements",
    "Price": "value",
    "Defensive Contribution": "defensive_contribution",
    "xGC": "expected_goals_conceded",
    "Transfer Balance": "transfers_balance",
    "ICT Index": "ict_index",
    "Clearances Blocks Interceptions": "clearances_blocks_interceptions",
    "Bonus": "bonus",
    "Saves": "saves",
    "Tackles": "tackles",
}


@st.cache_data(ttl=3600)
def load_players():
    return conn.query('SELECT "ID", "First Name", "Second Name", "Team" FROM gold.players ORDER BY "Second Name"')


@st.cache_data(ttl=3600)
def load_player_history(player_ids: tuple):
    placeholders = ", ".join([":id" + str(i) for i in range(len(player_ids))])
    params = {"id" + str(i): pid for i, pid in enumerate(player_ids)}
    computed = {"cumulative_points"}
    history_cols = ", ".join(c for c in HISTORY_COLUMNS.values() if c not in computed)
    return conn.query(
        f"SELECT element, round, {history_cols} FROM gold.players_history WHERE element IN ({placeholders}) ORDER BY round",
        params=params,
    )


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
st.title("Player Comparison")

players = load_players()
players["Player"] = players["First Name"] + " " + players["Second Name"] + " (" + players["Team"] + ")"
players["Player Short"] = players["First Name"] + " " + players["Second Name"]

player_options = dict(zip(players["Player"], players["ID"]))
selected = st.multiselect("Select players to compare", options=player_options.keys())

if len(selected) < 2:
    st.info("Select at least 2 players to compare.")
    st.stop()

selected_ids = tuple(player_options[name] for name in selected)

# -- Per-stat trend charts (2-column grid) -----------------------------------
st.subheader("Gameweek Trends")

history = load_player_history(selected_ids)

id_to_name = dict(zip(players["ID"], players["Player Short"]))
history["Player"] = history["element"].map(id_to_name)

history["cumulative_points"] = history.groupby("Player")["total_points"].cumsum()

stat_names = list(HISTORY_COLUMNS.keys())

for i in range(0, len(stat_names), 2):
    col_left, col_right = st.columns(2, gap="large")

    for col, stat in zip(
        [col_left, col_right], stat_names[i : i + 2]
    ):
        with col:
            db_col = HISTORY_COLUMNS[stat]
            fig = px.line(
                history,
                x="round",
                y=db_col,
                color="Player",
                labels={"round": "Gameweek", db_col: stat},
                title=stat,
                color_discrete_sequence=px.colors.qualitative.D3
            )
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
                margin=dict(t=120, b=20),
                height=350,
            )
            st.plotly_chart(fig, use_container_width=True)
