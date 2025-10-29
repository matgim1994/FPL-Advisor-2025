{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['fixture', 'element'],
    alias='penalty_missed_home'
) }}

with source_data as (
    select
        f.id AS fixture,
        (a_elem->>'element')::INT AS element,
        (a_elem->>'value')::INT AS value
    from {{ ref('bronze_fixtures') }} f
    CROSS JOIN LATERAL jsonb_array_elements(stats->4->'h') AS a_elem
    order by f.id
)

select *
from source_data