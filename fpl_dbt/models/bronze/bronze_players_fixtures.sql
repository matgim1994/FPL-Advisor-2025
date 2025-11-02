{{ 
    config(
        materialized='incremental',
        pre_hook = "{{ pre_truncate(this) }}",
        alias='players_fixtures'
    ) 
}}

with source_data as (
    select
        *
    from {{ source('raw', 'players_fixtures') }}

    {% if is_incremental() %}
        where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'players_fixtures') }})
    {% endif %}
)

select *
from source_data