{{ config(
    alias='fdr'
 )}}

with source_data as (
    select
        *
    from
        {{ ref('silver_teams_future_fixtures') }}
)

select
    id,
    max(opponent) filter (where match_rank = 1) as first_opponent,
    max(difficulty) filter (where match_rank = 1) as first_opponent_difficulty,
    max(opponent) filter (where match_rank = 2) as second_opponent,
    max(difficulty) filter (where match_rank = 2) as second_opponent_difficulty,
    max(opponent) filter (where match_rank = 3) as third_opponent,
    max(difficulty) filter (where match_rank = 3) as third_opponent_difficulty,
    max(opponent) filter (where match_rank = 4) as fourth_opponent,
    max(difficulty) filter (where match_rank = 4) as fourth_opponent_difficulty,
    max(opponent) filter (where match_rank = 5) as fifth_opponent,
    max(difficulty) filter (where match_rank = 5) as fifth_opponent_difficulty
from
    source_data
group by
    id
order by
    id