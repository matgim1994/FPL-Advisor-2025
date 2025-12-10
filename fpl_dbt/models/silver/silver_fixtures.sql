{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id',
    alias='fixtures_main'
) }}

with source_data as (
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
    from {{ ref('fixtures_snapshot') }}
)

select *
from source_data
