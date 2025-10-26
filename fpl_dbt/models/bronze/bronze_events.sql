{{ 
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='id',
        alias='events'
    ) 
}}

with source_data as (
    select
        *
    from {{ source('raw', 'events') }}

    {% if is_incremental() %}
        where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'events') }})
    {% endif %}
)

select *
from source_data