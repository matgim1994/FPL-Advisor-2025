{{ config(
    alias='all_top_assists'
)}}

with cte as (select
			    p.id,
			    p.first_name,
			    p.second_name,
			    t.name,
			    p.assists,
			    rank() over (order by p.assists desc) r
			from {{ ref('silver_players') }} p 
			join {{ ref('silver_teams') }} t ON p.team = t.id
			where p.assists > 0)
select
	id as "ID",
	first_name as "First Name",
	second_name as "Second Name",
	name as "Team",
	assists as "Assists"
from cte
where cte.r <= 20