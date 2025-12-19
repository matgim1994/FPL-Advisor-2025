{{ config(
    alias='teams'
) }}

select
    id,
    code,
    name,
    short_name,
    position,
    strength,
    strength_overall_home,
    strength_overall_away, 
    strength_attack_home,
    strength_attack_away,
    strength_defence_home,
    strength_defence_away,
    pulse_id
from {{ ref('silver_teams') }}