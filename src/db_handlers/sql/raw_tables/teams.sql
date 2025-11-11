CREATE TABLE IF NOT EXISTS raw.teams (
	id int4 NULL,
	code int4 NULL,
	draw int4 NULL,
	form text NULL,
	loss int4 NULL,
	"name" text NULL,
	played int4 NULL,
	points int4 NULL,
	"position" int4 NULL,
	short_name text NULL,
	strength int4 NULL,
	team_division text NULL,
	unavailable bool NULL,
	win int4 NULL,
	strength_overall_home int4 NULL,
	strength_overall_away int4 NULL,
	strength_attack_home int4 NULL,
	strength_attack_away int4 NULL,
	strength_defence_home int4 NULL,
	strength_defence_away int4 NULL,
	pulse_id int4 NULL,
	ingestion_time timestamp NULL
)
PARTITION BY RANGE (ingestion_time);

CREATE TABLE IF NOT EXISTS raw.teams_october PARTITION OF raw.teams
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE IF NOT EXISTS raw.teams_november PARTITION OF raw.teams
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE IF NOT EXISTS raw.teams_december PARTITION OF raw.teams
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE IF NOT EXISTS raw.teams_january PARTITION OF raw.teams
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE IF NOT EXISTS raw.teams_february PARTITION OF raw.teams
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE IF NOT EXISTS raw.teams_march PARTITION OF raw.teams
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE IF NOT EXISTS raw.teams_april PARTITION OF raw.teams
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE IF NOT EXISTS raw.teams_may PARTITION OF raw.teams
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');