{{ config(
    alias='gw_results'
)}}

select
	fm.id,
	fm.event,
	fm.kickoff_time,
	th.name as "Team Home",
	ta.name as "Team Away",
	fm.team_h_score "Team Home Score",
	fm.team_a_score "Team Away Score"
from {{ ref('silver_fixtures') }} fm
join {{ ref('silver_teams') }} ta on fm.team_a = ta.id
join {{ ref('silver_teams') }} th on fm.team_h = th.id
where fm.event = (
	select
		id
	from
		{{ ref('silver_events') }}
	where is_current = true)
order by fm.kickoff_time asc