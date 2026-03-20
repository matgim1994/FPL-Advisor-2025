import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from db import get_connection

st.set_page_config(page_title="Query Players — FPL Advisor", layout="wide")

conn = get_connection()

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------
COLUMNS = [
    "ID",
    "First Name",
    "Second Name",
    "Team",
    "Position",
    "Price",
    "Points",
    "Points Per Game",
    "Minutes",
    "Goals",
    "Assists",
    "Clean Sheets",
    "Bonus",
    "xG",
    "xA",
    "xGI",
    "xG90",
    "xA90",
    "xGI90",
    "xGC90",
    "DC90",
    "Saves90",
    "Goals90",
    "Assists90",
    "GC90",
    "CS90",
]


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


SPIDER_CONFIG = {
    "Minutes":        {"label": "Minutes",             "positions": {"Forward", "Midfielder", "Defender", "Goalkeeper"}},
    "Points Per Game":{"label": "Pts per Game",        "positions": {"Forward", "Midfielder", "Defender", "Goalkeeper"}},
    "GC90":           {"label": "GC per 90",           "positions": {"Midfielder", "Defender", "Goalkeeper"}},
    "xGI90":          {"label": "xGI per 90",          "positions": {"Forward", "Midfielder", "Defender"}},
    "Goals90":        {"label": "Goals per 90",        "positions": {"Forward", "Midfielder", "Defender"}},
    "xG90":           {"label": "xG per 90",           "positions": {"Forward", "Midfielder", "Defender"}},
    "Assists90":      {"label": "Assists per 90",      "positions": {"Forward", "Midfielder", "Defender"}},
    "xA90":           {"label": "xA per 90",           "positions": {"Forward", "Midfielder", "Defender"}},
    "CS90":           {"label": "CS per 90",           "positions": {"Midfielder", "Defender", "Goalkeeper"}},
    "xGC90":          {"label": "xGC per 90",          "positions": {"Defender", "Goalkeeper"}},
    "DC90":           {"label": "Def. Contrib per 90", "positions": {"Defender", "Midfielder"}},
    "Saves90":        {"label": "Saves per 90",        "positions": {"Goalkeeper"}},
}


@st.cache_data(ttl=3600)
def load_players():
    select_clause = ", ".join(f'"{c}"' for c in COLUMNS)
    return conn.query(
        f"SELECT {select_clause} FROM gold.players ORDER BY \"Points\" DESC"
    )


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
st.title("Query Players")

players = load_players()
players["Player"] = players["First Name"] + " " + players["Second Name"]

# -- Filters ----------------------------------------------------------------
col_name, col_team, col_pos, col_price = st.columns(4)

with col_name:
    player_names = sorted(players["Player"].unique().tolist())
    selected_players = st.multiselect("Player Name", player_names, placeholder="Search...")

with col_team:
    teams = ["All"] + sorted(players["Team"].unique().tolist())
    selected_team = st.selectbox("Team", teams)

with col_pos:
    positions = ["All"] + sorted(players["Position"].unique().tolist())
    selected_position = st.selectbox("Position", positions)

filtered = players.copy()

if selected_players:
    filtered = filtered[filtered["Player"].isin(selected_players)]
if selected_team != "All":
    filtered = filtered[filtered["Team"] == selected_team]
if selected_position != "All":
    filtered = filtered[filtered["Position"] == selected_position]

with col_price:
    min_price = float(filtered["Price"].min()) if not filtered.empty else 0.0
    max_price = float(filtered["Price"].max()) if not filtered.empty else 0.0
    if min_price < max_price:
        price_range = st.slider("Price", min_price, max_price, (min_price, max_price), step=0.1)
        filtered = filtered[(filtered["Price"] >= price_range[0]) & (filtered["Price"] <= price_range[1])]
    else:
        st.slider("Price", min_price, max_price + 0.1, (min_price, max_price + 0.1), step=0.1, disabled=True)

# -- Table ------------------------------------------------------------------
TABLE_EXCLUDE = {"ID", "First Name", "Second Name", "xG90", "xA90", "xGI90", "xGC90", "DC90", "Saves90", "Goals90", "Assists90", "GC90", "CS90"}
display_columns = ["Player"] + [c for c in COLUMNS if c not in TABLE_EXCLUDE]

selection = st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True,
    selection_mode="multi-row",
    on_select="rerun",
)

# Combine multiselect + table row clicks
table_picked = filtered.iloc[selection.selection.rows]["Player"].tolist() if selection.selection.rows else []
all_selected = list(set(selected_players + table_picked))

# -- Spider chart --------------------------------------------------------------
if all_selected:
    st.subheader("Player Profile")

    chart_players = players[players["Player"].isin(all_selected)]
    palette = px.colors.qualitative.D3
    color_map = {name: palette[i % len(palette)] for i, name in enumerate(all_selected)}
    selected_positions = set(chart_players["Position"].unique())

    # Pick stats relevant to the union of selected players' positions
    spider_stats = [s for s, cfg in SPIDER_CONFIG.items() if cfg["positions"] & selected_positions]
    spider_labels = [SPIDER_CONFIG[s]["label"] for s in spider_stats]

    # Min-max scaling (0-100) — use only players with 60%+ of possible minutes for scale bounds
    # to prevent low-minute outliers from distorting axes
    min_minutes = players["Minutes"].max() * 0.6
    qualified = players[players["Minutes"] >= min_minutes]
    mins = qualified[spider_stats].min()
    maxs = qualified[spider_stats].max()
    ranges = maxs - mins
    ranges = ranges.replace(0, 1)
    scaled = ((players[spider_stats] - mins) / ranges * 100).clip(0, 100)

    fig = go.Figure()
    for idx in chart_players.index:
        player_name = players.loc[idx, "Player"]
        values = scaled.loc[idx, spider_stats].tolist()
        values += [values[0]]  # close the polygon
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=spider_labels + [spider_labels[0]],
            name=player_name,
            fill="toself",
            opacity=0.8,
            line=dict(color=color_map[player_name]),
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

    # -- Gameweek trends (expander) --------------------------------------------
    if len(all_selected) >= 2:
        with st.expander("Gameweek Trends"):
            selected_ids = tuple(
                int(players.loc[players["Player"] == name, "ID"].iloc[0])
                for name in all_selected
            )
            history = load_player_history(selected_ids)

            id_to_name = dict(zip(players["ID"], players["Player"]))
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
                        fig_trend = px.line(
                            history,
                            x="round",
                            y=db_col,
                            color="Player",
                            labels={"round": "Gameweek", db_col: stat},
                            title=stat,
                            color_discrete_map=color_map,
                        )
                        fig_trend.update_layout(
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
                            margin=dict(t=120, b=20),
                            height=350,
                        )
                        st.plotly_chart(fig_trend, use_container_width=True)
