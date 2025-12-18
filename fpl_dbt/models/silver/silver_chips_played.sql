{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='event',
    alias='chips_played'
) }}

with source_data as (
    select
    id as event,
    (chip_plays->0->'num_played')::INT as bboost,
    (chip_plays->1->'num_played')::INT as freehit,
    (chip_plays->2->'num_played')::INT as wildcard,
    (chip_plays->3->'num_played')::INT as triple_cpt
    from {{ ref('events_snapshot') }}
    where dbt_valid_to is null
    order by event   
)

select *
from source_data
