{{ config(
    alias='all_top_midfielders'
)}}

with cte as(
	select
		p.id,
		p.first_name,
		p.second_name,
		t.name,
		p.total_points,
		rank() over (order by p.total_points desc) as rank
	from
		{{ ref('silver_players') }} p
	join {{ ref('silver_teams') }} t on p.team = t.id
	where element_type = 3
)
select
	id as "ID",
	first_name as "First Name",
	second_name as "Second Name",
	name as "Team",
	total_points as "Total Points"
from
	cte
where rank <= 20
order by total_points desc, name asc