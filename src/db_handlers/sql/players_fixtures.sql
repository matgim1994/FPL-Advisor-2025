CREATE TABLE raw.players_fixtures (
	"element" int4,
	id int4,
	code int8,
	team_h int4,
	team_h_score int4,
	team_a int4,
	team_a_score int4,
	"event" int4,
	finished bool,
	minutes int4,
	provisional_start_time bool,
	kickoff_time timestamp,
	event_name text,
	is_home bool,
	difficulty int4,
	ingestion_time timestamp
)
PARTITION BY RANGE (ingestion_time);

CREATE TABLE raw.players_fixtures_october PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE raw.players_fixtures_november PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE raw.players_fixtures_december PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE raw.players_fixtures_january PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE raw.players_fixtures_february PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE raw.players_fixtures_march PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE raw.players_fixtures_april PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE raw.players_fixtures_may PARTITION OF raw.players_fixtures
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');