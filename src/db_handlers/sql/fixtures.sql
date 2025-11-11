CREATE TABLE raw.fixtures (
	id int4,
	code int8,
	"event" int4,
	finished bool,
	finished_provisional bool,
	kickoff_time timestamp,
	minutes int4,
	provisional_start_time bool,
	started bool,
	team_a int4,
	team_a_score int4,
	team_h int4,
	team_h_score int4,
	stats jsonb,
	team_h_difficulty int4,
	team_a_difficulty int4,
	pulse_id int8,
	ingestion_time timestamp
)
PARTITION BY RANGE (ingestion_time);

CREATE TABLE raw.fixtures_october PARTITION OF raw.fixtures
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE raw.fixtures_november PARTITION OF raw.fixtures
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE raw.fixtures_december PARTITION OF raw.fixtures
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE raw.fixtures_january PARTITION OF raw.fixtures
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE raw.fixtures_february PARTITION OF raw.fixtures
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE raw.fixtures_march PARTITION OF raw.fixtures
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE raw.fixtures_april PARTITION OF raw.fixtures
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE raw.fixtures_may PARTITION OF raw.fixtures
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');