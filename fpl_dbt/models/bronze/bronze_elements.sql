{{ 
    config(
        materialized='incremental',
        incremental_strategy='merge',
        unique_key='id',
        alias='elements'
    ) 
}}

with source_data as (
    select
        *
    from {{ source('raw', 'elements') }}

    {% if is_incremental() %}
        where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'elements') }})
    {% endif %}
)

select *
from source_data