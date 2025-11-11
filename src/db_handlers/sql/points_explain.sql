CREATE TABLE raw.points_explain (
	id int4 NULL,
	fixture int4 NULL,
	identifier varchar(40) NULL,
	points int4 NULL,
	value int4 NULL,
	points_modification int4 NULL,
	ingestion_time timestamp NULL
)
PARTITION BY RANGE (ingestion_time);

CREATE TABLE raw.points_explain_october PARTITION OF raw.points_explain
    FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');
CREATE TABLE raw.points_explain_november PARTITION OF raw.points_explain
    FOR VALUES FROM ('2025-11-01') TO ('2025-12-01');
CREATE TABLE raw.points_explain_december PARTITION OF raw.points_explain
    FOR VALUES FROM ('2025-12-01') TO ('2026-01-01');
CREATE TABLE raw.points_explain_january PARTITION OF raw.points_explain
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE raw.points_explain_february PARTITION OF raw.points_explain
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE raw.points_explain_march PARTITION OF raw.points_explain
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE raw.points_explain_april PARTITION OF raw.points_explain
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE raw.points_explain_may PARTITION OF raw.points_explain
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');