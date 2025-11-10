{{ config(
    materialized='incremental',
    pre_hook = "{{ pre_truncate(this) }}",
    alias='teams_future_fixtures'
) }}

with future_fixtures as (
    select
        t.id,
        f.id as fixture_id,
        f.event,
        case
            when f.team_h = t.id then f.team_a
            else f.team_h
        end as opponent,
        case
            when f.team_h = t.id then f.team_a_difficulty
            else f.team_h_difficulty
        end as difficulty
    from {{ ref('bronze_teams') }} as t
    cross join lateral
        (
            select
                id,
                event,
                team_h,
                team_a,
                team_h_difficulty,
                team_a_difficulty
            from
                {{ ref('bronze_fixtures') }}
            where
                finished is not true
                and started is not true
                and (team_h = t.id or team_a = t.id)
            order by event asc
            limit 5
        ) as f
)

SELECT
    id,
    fixture_id,
    event,
    opponent,
    difficulty,
    ROW_NUMBER() over (partition by id order by event asc) as match_rank
FROM
    future_fixtures