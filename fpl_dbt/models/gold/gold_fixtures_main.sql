{{ config(
    alias = 'fixtures_main'
) }}

select 
    id,
    code,
    event,
    finished,
    kickoff_time,
    started,
    team_a,
    team_a_score,
    team_h,
    team_h_score,
    team_h_difficulty,
    team_a_difficulty
from {{ ref('silver_fixtures') }}
order by id asc