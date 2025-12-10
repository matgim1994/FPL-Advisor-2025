{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['id', 'fixture', 'identifier'],
    alias='points_explain',
    post_hook = "{{ create_index(this, ['id', 'fixture'])}}",
) }}

with source_data as (
    select
        id,
        fixture,
        identifier,
        points,
        value,
        points_modification
    from {{ ref('points_explain_snapshot') }}
)

select *
from source_data