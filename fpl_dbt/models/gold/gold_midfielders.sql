{{ config(
    alias = 'midfielders'
) }}

select 
	p.first_name,
	p.second_name,
	t.name,
	p.now_cost,
	p.cost_change_start,
	p.cost_change_event,
	p.form,
	p.total_points,
	p.points_per_game,
    p.selected_by_percent,
	p.transfers_in,
	p.transfers_in_event,
	p.transfers_out,
	p.transfers_out_event,
	p.minutes,
	p.goals_scored,
	p.assists,
	p.clean_sheets,
	p.bonus,
	p.ict_index,
	p.clearances_blocks_interceptions,
	p.recoveries,
	p.tackles,
	p.defensive_contribution,
	p.starts,
	p.expected_goals,
	p.expected_assists,
	p.expected_goal_involvements,
	p.expected_goals_conceded,
	p.ict_index_rank_type,
	p.expected_goals_per_90,
	p.expected_assists_per_90,
	p.expected_goal_involvements_per_90,
	p.expected_goals_conceded_per_90,
	p.goals_conceded_per_90,
	p.form_rank_type,
	p.points_per_game_rank_type,
	p.selected_rank_type,
	p.clean_sheets_per_90,
	p.defensive_contribution_per_90
from {{ ref('silver_players') }} p
left join {{ ref('silver_teams') }} t on p.team = t.id
where p.element_type = 3
order by p.total_points desc