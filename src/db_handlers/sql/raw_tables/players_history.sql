CREATE TABLE IF NOT EXISTS raw.players_history (
	"element" int4,
	fixture int4,
	opponent_team int4,
	total_points int4,
	was_home bool,
	kickoff_time timestamp,
	team_h_score int4,
	team_a_score int4,
	round int4,
	modified bool,
	minutes int4,
	goals_scored int4,
	assists int4,
	clean_sheets int4,
	goals_conceded int4,
	own_goals int4,
	penalties_saved int4,
	penalties_missed int4,
	yellow_cards int4,
	red_cards int4,
	saves int4,
	bonus int4,
	bps int4,
	influence float8,
	creativity float8,
	threat float8,
	ict_index float8,
	clearances_blocks_interceptions int4,
	recoveries int4,
	tackles int4,
	defensive_contribution int4,
	starts int4,
	expected_goals float8,
	expected_assists float8,
	expected_goal_involvements float8,
	expected_goals_conceded float8,
	value int4,
	transfers_balance int4,
	selected int4,
	transfers_in int4,
	transfers_out int4,
	ingestion_time timestamp
)
PARTITION BY RANGE (ingestion_time);

CREATE TABLE IF NOT EXISTS raw.players_history_october PARTITION OF raw.players_history
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE IF NOT EXISTS raw.players_history_november PARTITION OF raw.players_history
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE IF NOT EXISTS raw.players_history_december PARTITION OF raw.players_history
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE IF NOT EXISTS raw.players_history_january PARTITION OF raw.players_history
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE IF NOT EXISTS raw.players_history_february PARTITION OF raw.players_history
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE IF NOT EXISTS raw.players_history_march PARTITION OF raw.players_history
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE IF NOT EXISTS raw.players_history_april PARTITION OF raw.players_history
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE IF NOT EXISTS raw.players_history_may PARTITION OF raw.players_history
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');