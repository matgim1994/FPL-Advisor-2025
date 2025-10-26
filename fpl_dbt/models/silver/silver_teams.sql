{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id',
    alias='teams'
) }}

with source_data as (
    select
        id,
        code,
        name,
        short_name,
        position,
        strength,
        strength_overall_home,
        strength_overall_away, 
        strength_attack_home,
        strength_attack_away,
        strength_defence_home,
        strength_defence_away,
        pulse_id
    from {{ ref('bronze_teams') }}
)

select *
from source_data