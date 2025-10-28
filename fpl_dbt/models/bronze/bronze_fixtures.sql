{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id',
    alias='fixtures'
) }}

with source_data as (
    select
        *
    from {{ source('raw', 'fixtures') }}
    {% if is_incremental() %}
      where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'fixtures') }})
    {% endif %}
)

select *
from source_data
