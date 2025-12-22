{{ config(
    alias='gw_top_defensive_contributions',
)}}

select
    ph.element as "ID",
    p.first_name as "First Name",
    p.second_name as "Second Name",
    case when p.element_type = 1 then 'Goalkeeper'
         when p.element_type = 2 then 'Defender'
         when p.element_type = 3 then 'Midfielder'
         when p.element_type = 4 then 'Forward'
         else 'Unknown' end as "Position",
    t.name as "Team",
    opp_t.name as "Opponent",
    ph.defensive_contribution as "Defensive Contribution"
from {{ ref('silver_players_history') }} ph
join {{ ref('silver_events') }} e on ph.round = e.id and e.is_current = True
join {{ ref('silver_players') }} p on ph.element = p.id
join {{ ref('silver_teams') }} t on p.team = t.id
join {{ ref('silver_teams') }} opp_t on ph.opponent_team = opp_t.id
where (p.element_type = 2 and ph.defensive_contribution >= 10)
or (p.element_type in (3,4) and ph.defensive_contribution >= 12)
order by ph.defensive_contribution desc, t.name asc, p.element_type asc