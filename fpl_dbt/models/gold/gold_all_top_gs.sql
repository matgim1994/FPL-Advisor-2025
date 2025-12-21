{{ config(
    alias='all_top_goalscorers'
)}}

with cte as (select
			    p.id,
			    p.first_name,
			    p.second_name,
			    t.name,
			    p.goals_scored,
			    rank() over (order by p.goals_scored desc) r
			from {{ ref('silver_players') }} p 
			join {{ ref('silver_teams') }} t ON p.team = t.id
			where p.goals_scored > 0)
select
	id as "ID",
	first_name as "First Name",
	second_name as "Second Name",
	name as "Team",
	goals_scored as "Goals Scored"
from cte
where cte.r <= 20