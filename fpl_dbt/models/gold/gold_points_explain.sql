{{ config(
    alias='points_explain'
) }}

select
    id,
    fixture,
    identifier,
    points,
    value,
    points_modification
from {{ ref('silver_points_explain') }}