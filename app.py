import streamlit as st
import pandas as pd
import altair as alt

# ----------------------------------------------------------------------
# Page setup and data loading
# ----------------------------------------------------------------------
st.set_page_config(page_title="NBA Player Stats Explorer", layout="wide")
st.title("NBA Top 50 Scorers Stats Explorer")
st.write("Explore the top 50 NBA scorers of the 2026 season.")

# Load the dataset once. Streamlit caches this so it doesn't reload on every rerun.
@st.cache_data
def load_data():
    return pd.read_csv("nba_player_stats_2026.csv")

df = load_data()

# The dataset doesn't include conference, so we map each team to one.
# This covers every team that appears in the dataset.
EAST_TEAMS = ["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DET", "IND",
              "MIA", "MIL", "NYK", "ORL", "PHI", "TOR"]
WEST_TEAMS = ["DAL", "DEN", "HOU", "LAC", "LAL", "MIN", "NOP", "OKC",
              "PHX", "POR", "SAC", "SAS", "UTA"]
df["CONFERENCE"] = df["TEAM"].apply(lambda t: "East" if t in EAST_TEAMS else "West")

# Points per game (PPG) isn't in the raw data, so we compute it once here.
# Both the metrics and the charts below reuse this column.
# Rounded to 1 decimal place so it never shows long, repeating decimals.
df["PPG"] = (df["PTS"] / df["GP"]).round(1)

# ----------------------------------------------------------------------
# Session state defaults
# We use session_state to remember filter choices across reruns, and to
# power a "Reset filters" button that has a real, visible effect on the app.
# ----------------------------------------------------------------------
default_conferences = ["East", "West"]
default_min_gp = int(df["GP"].min())

if "selected_conferences" not in st.session_state:
    st.session_state.selected_conferences = default_conferences
if "min_gp" not in st.session_state:
    st.session_state.min_gp = default_min_gp

# ----------------------------------------------------------------------
# Sidebar filters
# ----------------------------------------------------------------------
st.sidebar.header("Filters")

# Filter 1: which conference(s) to include
st.session_state.selected_conferences = st.sidebar.multiselect(
    "Conference",
    options=default_conferences,
    default=st.session_state.selected_conferences,
)

# Filter 2: minimum games played
st.session_state.min_gp = st.sidebar.slider(
    "Minimum games played",
    min_value=int(df["GP"].min()),
    max_value=int(df["GP"].max()),
    value=st.session_state.min_gp,
)

# Reset button: clears both filters back to their defaults.
# This is the visible functional effect of session_state in this app.
if st.sidebar.button("Reset filters"):
    st.session_state.selected_conferences = default_conferences
    st.session_state.min_gp = default_min_gp
    st.rerun()

# ----------------------------------------------------------------------
# Apply filters to the data
# ----------------------------------------------------------------------
filtered_df = df[
    (df["CONFERENCE"].isin(st.session_state.selected_conferences))
    & (df["GP"] >= st.session_state.min_gp)
]

# ----------------------------------------------------------------------
# Summary metrics: all three describe the top scorer within the FILTERED
# data, so all of them change as the filters change.
# ----------------------------------------------------------------------
col1, col2, col3 = st.columns(3)

if len(filtered_df) == 0:
    st.warning("No players match the current filters.")
else:
    top_scorer = filtered_df.loc[filtered_df["PTS"].idxmax()]
    col1.metric("Top scorer", top_scorer["PLAYER"])
    col2.metric("Points Per Game", f"{top_scorer['PPG']:.1f}")
    col3.metric("Field Goal %", f"{top_scorer['FG_PCT']:.1%}")

# ----------------------------------------------------------------------
# Data table
# ----------------------------------------------------------------------
st.subheader("Player data")
# PLAYER_ID and RANK are just internal identifiers, not useful to display.
table_df = filtered_df.drop(columns=["PLAYER_ID", "RANK"]).reset_index(drop=True)
table_df.index = table_df.index + 1  # start row numbering at 1 instead of 0
st.dataframe(table_df)

# ----------------------------------------------------------------------
# Charts
# ----------------------------------------------------------------------
st.subheader("Top 20 players by points per game")
# Aggregated chart: PPG is an average (points divided by games played),
# not a raw column, and we further summarize it down to the top 20.
top20_ppg = filtered_df.nlargest(20, "PPG").set_index("PLAYER")["PPG"]
st.bar_chart(top20_ppg)

st.subheader("Points per game vs. field goal %")
# Scatter chart: one point per player. We use Altair (bundled with Streamlit)
# instead of st.scatter_chart because it lets us add a tooltip with the
# player's name and format FG% as a percentage.
scatter = alt.Chart(filtered_df).mark_circle(size=90).encode(
    x=alt.X("PPG", title="Points per game"),
    y=alt.Y("FG_PCT", title="Field goal %", axis=alt.Axis(format=".0%")),
    tooltip=[
        alt.Tooltip("PLAYER", title="Player"),
        alt.Tooltip("PPG", title="PPG", format=".1f"),
        alt.Tooltip("FG_PCT", title="FG%", format=".1%"),
    ],
)
st.altair_chart(scatter, use_container_width=True)
