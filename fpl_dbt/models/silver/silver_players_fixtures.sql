{{ config(
    materialized='incremental',
    pre_hook = "{{ pre_truncate(this) }}",
    post_hook = "{{ create_index(this, 'element')}}",
    alias='players_fixtures'
) }}

with source_data as (
    select
        element,
        id,
        team_h,
        team_h_score,
        team_a,
        team_a_score,
        event,
        finished,
        minutes,
        provisional_start_time,
        kickoff_time,
        event_name,
        is_home,
        difficulty
    from {{ ref('bronze_players_fixtures') }}
)

select *
from source_data