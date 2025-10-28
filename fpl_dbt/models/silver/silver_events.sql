{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id',
    alias='events'
) }}

with source_data as (
    select
        id,
        name,
        deadline_time,
        average_entry_score,
        finished,
        data_checked,
        highest_scoring_entry,
        deadline_time_epoch,
        deadline_time_game_offset,
        highest_score,
        is_previous,
        is_current,
        is_next,
        cup_leagues_created,
        h2h_ko_matches_created,
        can_enter,
        can_manage,
        ranked_count,
        transfers_made
    from {{ ref('bronze_events') }}
)

select *
from source_data
