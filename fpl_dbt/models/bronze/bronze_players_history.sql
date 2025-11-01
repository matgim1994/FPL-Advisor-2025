{{ 
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=['element', 'fixture'],
        alias='players_history'
    ) 
}}

with source_data as (
    select
        *
    from {{ source('raw', 'players_history') }}

    {% if is_incremental() %}
        where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'players_history') }})
    {% endif %}
)

select *
from source_data