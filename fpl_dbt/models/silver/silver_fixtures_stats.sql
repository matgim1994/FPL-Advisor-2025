{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['fixture', 'element', 'identifier'],
    alias='fixtures_stats',
    post_hook = ["{{ create_index(this, 'element')}}",
                 "{{ create_index(this, 'fixture')}}"]
) }}

with flattened_stats AS (
    select
        id as fixture,
        event,
        team_a,
        team_h,
        jsonb_array_elements(stats) as stat_obj
    from {{ ref('fixtures_snapshot') }}
    where dbt_valid_to is null
),

stats_away AS (
    select
        fixture,
        event,
        (stat_obj->>'identifier')::varchar as identifier,
        jsonb_array_elements(stat_obj->'a')->>'element' as element,
        (jsonb_array_elements(stat_obj->'a')->>'value')::int as value,
        'away' as side,
        team_a as team
    from flattened_stats
),

stats_home AS (
    select
        fixture,
        event,
        (stat_obj->>'identifier')::varchar as identifier,
        jsonb_array_elements(stat_obj->'h')->>'element' as element,
        (jsonb_array_elements(stat_obj->'h')->>'value')::int as value,
        'home' as side,
        team_h as team
    from flattened_stats
),

unioned_stats as (
    select * from stats_away
    union all
    select * from stats_home
)

select
    fixture,
    event,
    element::int,
    team,
    identifier,
    value,
    side
from unioned_stats
where element is not null