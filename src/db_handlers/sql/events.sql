CREATE TABLE raw.events (
	id int4,
	name text,
	deadline_time timestamp,
	release_time timestamp,
	average_entry_score int4,
	finished bool,
	data_checked bool,
	highest_scoring_entry int4,
	deadline_time_epoch int8,
	deadline_time_game_offset int4,
	highest_score int4,
	is_previous bool,
	is_current bool,
	is_next bool,
	cup_leagues_created bool,
	h2h_ko_matches_created bool,
	can_enter bool,
	can_manage bool,
	released bool,
	ranked_count int4,
	overrides jsonb,
	chip_plays jsonb,
	most_selected int4,
	most_transferred_in int4,
	top_element int4,
	top_element_info jsonb,
	transfers_made int4,
	most_captained int4,
	most_vice_captained int4,
	ingestion_time timestamp
)
PARTITION BY RANGE (ingestion_time);

CREATE TABLE raw.events_october PARTITION OF raw.events
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE raw.events_november PARTITION OF raw.events
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE raw.events_december PARTITION OF raw.events
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE raw.events_january PARTITION OF raw.events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE raw.events_february PARTITION OF raw.events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE raw.events_march PARTITION OF raw.events
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE raw.events_april PARTITION OF raw.events
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE raw.events_may PARTITION OF raw.events
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');