{{ config(
    alias='gw_top_defenders'
)}}

with cte as (
		select
			ph.element,
			p.first_name,
			p.second_name,
			t.name,
			ph.total_points,
			rank() over (order by ph.total_points desc)
		from
			{{ ref('silver_players_history') }} ph
		join {{ ref('silver_players') }} p on ph.element = p.id
		join {{ ref('silver_teams') }} t on p.team = t.id
		where ph.round = (
				select
					id
				from
					{{ ref('silver_events') }}
				where is_current = True
			)
		and element_type = 2
		order by total_points desc
)
select
	element as "ID",
	first_name as "First Name",
	second_name as "Second Name",
	name as "Team",
	total_points as "Total Points"
from
	cte
where rank <= 10
order by total_points desc, name asc