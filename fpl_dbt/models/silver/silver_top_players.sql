{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='event',
    alias='top_players'
) }}

with source_data as (
    select
        id as event,
        most_selected,
        most_transferred_in,
        top_element,
        (top_element_info -> 'points')::INT as top_element_points,
        most_captained,
        most_vice_captained
    from {{ ref('bronze_events') }}
)

select *
from source_data
