{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='id',
    alias='teams'
) }}

with source_data as (
    select
        *
    from {{ source('raw', 'teams') }}
    {% if is_incremental() %}
      where ingestion_time = (select max(ingestion_time) from {{ source('raw', 'teams') }})
    {% endif %}
)

select *
from source_data