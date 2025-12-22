{{ config(
    alias='all_top_goalscorers'
)}}

with cte as (select
			    p.id,
			    p.first_name,
			    p.second_name,
				p.element_type,
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
	case when element_type = 1 then 'Goalkeeper'
			when element_type = 2 then 'Defender'
			when element_type = 3 then 'Midfielder'
			when element_type = 4 then 'Forward'
			else 'Unknown' end as "Position",
	name as "Team",
	goals_scored as "Goals Scored"
from cte
where cte.r <= 20
order by goals_scored desc, name asc, element_type asc