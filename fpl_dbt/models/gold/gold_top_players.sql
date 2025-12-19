{{ config(
    alias='top_players'
) }}

select
    event,
    most_selected,
    most_transferred_in,
    top_element,
    top_element_points,
    most_captained,
    most_vice_captained
from {{ ref('silver_top_players') }}