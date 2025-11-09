{{ config(
    alias = 'goalkeepers'
) }}

select 
	p.first_name,
	p.second_name,
	t.name,
	p.now_cost,
	p.form,
	p.total_points,
	p.points_per_game,
    p.selected_by_percent
from {{ ref('silver_players') }} p
left join {{ ref('silver_teams') }} t on p.team = t.id
where p.element_type = 1
order by p.total_points desc