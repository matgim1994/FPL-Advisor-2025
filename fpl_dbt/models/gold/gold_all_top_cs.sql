{{ config(
    alias='all_top_clean_sheets'
)}}

with cte as (select
			    p.id,
			    p.first_name,
			    p.second_name,
                p.element_type,
			    t.name,
			    p.clean_sheets,
			    rank() over (order by p.clean_sheets desc) r
			from {{ ref('silver_players') }} p 
			join {{ ref('silver_teams') }} t ON p.team = t.id
			where p.clean_sheets > 0
            and p.element_type != 4)
select
	id as "ID",
	first_name as "First Name",
	second_name as "Second Name",
    case when element_type = 1 then 'Goalkeeper'
         when element_type = 2 then 'Defender'
         when element_type = 3 then 'Midfielder'
         else 'Unknown' end as "Position",
	name as "Team",
	clean_sheets as "Clean Sheets"
from cte
where cte.r <= 30
order by clean_sheets desc, name asc