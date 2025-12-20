{{ config(
    alias = 'fixtures_stats'
) }}

select
    fixture,
    event,
    element,
    team,
    identifier,
    value,
    side
from {{ ref('silver_fixtures_stats') }}
order by fixture, event, element asc