{{ 
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key=['id', 'fixture', 'identifier'],
        alias='points_explain'
    ) 
}}

with source_data as (
    select
        *
    from {{ source('raw', 'points_explain') }}

    {% if is_incremental() %}
        where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'players_history') }})
    {% endif %}
)

select *
from source_data