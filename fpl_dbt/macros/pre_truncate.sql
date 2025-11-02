{% macro pre_truncate(this) %}
do $$
begin
    if exists (
        select from pg_tables
        where schemaname = '{{ this.schema }}'
        and tablename = '{{ this.identifier }}'
    ) then
        execute 'truncate table {{ this }}';
    end if;
end
$$;
{% endmacro %}