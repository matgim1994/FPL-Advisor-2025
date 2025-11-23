CREATE TABLE IF NOT EXISTS raw.points_explain (
	id int4 NULL,
	fixture int4 NULL,
	identifier varchar(40) NULL,
	points int4 NULL,
	value int4 NULL,
	points_modification int4 NULL,
    data_hash text NULL,
	ingestion_time timestamp NULL,
    PRIMARY KEY (id, fixture, identifier)
);