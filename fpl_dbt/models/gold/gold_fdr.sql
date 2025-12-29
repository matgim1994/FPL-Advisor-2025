{{ config(
    alias='fdr'
 )}}

with source_data as (
    select
            f.id,
            team.name as team,
            f.match_rank,
            opp.name as opponent_name,
            f.difficulty
        from {{ ref('silver_teams_future_fixtures') }} f
        left join {{ ref('silver_teams') }} team
            on f.id = team.id
        left join {{ ref('silver_teams') }} opp
            on f.opponent = opp.id
)

select
    id,
    team,
    max(opponent_name) filter (where match_rank = 1) as first_opponent,
    max(difficulty)     filter (where match_rank = 1) as first_opponent_difficulty,
    max(opponent_name) filter (where match_rank = 2) as second_opponent,
    max(difficulty)     filter (where match_rank = 2) as second_opponent_difficulty,
    max(opponent_name) filter (where match_rank = 3) as third_opponent,
    max(difficulty)     filter (where match_rank = 3) as third_opponent_difficulty,
    max(opponent_name) filter (where match_rank = 4) as fourth_opponent,
    max(difficulty)     filter (where match_rank = 4) as fourth_opponent_difficulty,
    max(opponent_name) filter (where match_rank = 5) as fifth_opponent,
    max(difficulty)     filter (where match_rank = 5) as fifth_opponent_difficulty
from
    source_data
group by
    id, team
order by
    id