{{ config(
    alias='gw_clean_sheets'
)}}

select
    ph.element as "ID",
    p.first_name as "First Name",
    p.second_name as "Second Name",
    case when p.element_type = 1 then 'Goalkeeper'
         when p.element_type = 2 then 'Defender'
         when p.element_type = 3 then 'Midfielder'
         else 'Unknown' end as "Position",
    t.name as "Team",
    opp_t.name as "Opponent",
    ph.clean_sheets as "Clean Sheets"
from {{ ref('silver_players_history') }} ph
join {{ ref('silver_events') }} e on ph.round = e.id and e.is_current = True
join {{ ref('silver_players') }} p on ph.element = p.id
join {{ ref('silver_teams') }} t on p.team = t.id
join {{ ref('silver_teams') }} opp_t on ph.opponent_team = opp_t.id
where ph.clean_sheets > 0
and p.element_type != 4
order by ph.clean_sheets desc, t.name asc, p.element_type asc