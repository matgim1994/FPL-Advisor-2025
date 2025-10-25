{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id'
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
    from {{ source('raw', 'teams') }}
    {% if is_incremental() %}
      where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'elements') }})
    {% endif %}
)

select *
from source_data