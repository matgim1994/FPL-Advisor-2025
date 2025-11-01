{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['element', 'fixture'],
    alias='players_history'
) }}

with source_data as (
    select
        element,
        fixture,
        opponent_team,
        total_points,
        was_home,
        kickoff_time,
        team_h_score,
        team_a_score,
        round,
        modified,
        minutes,
        goals_scored,
        assists,
        clean_sheets,
        goals_conceded,
        own_goals,
        penalties_saved,
        penalties_missed,
        yellow_cards,
        red_cards,
        saves,
        bonus,
        bps,
        influence,
        creativity,
        threat,
        ict_index,
        clearances_blocks_interceptions,
        recoveries,
        tackles,
        defensive_contribution,
        starts,
        expected_goals,
        expected_assists,
        expected_goal_involvements,
        expected_goals_conceded,
        value,
        transfers_balance,
        selected,
        transfers_in,
        transfers_out
    from {{ ref('bronze_players_history') }}
)

select *
from source_data