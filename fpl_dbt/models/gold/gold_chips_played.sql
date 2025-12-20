{{ config(
    alias='chips_played'
)}}

select
    event,
    bboost,
    freehit,
    wildcard,
    triple_cpt
from {{ ref('silver_chips_played') }}
order by event asc