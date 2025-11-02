{% macro create_index(this, columns, index_type='btree') %}
    {%- if columns is string -%}
        {%- set columns = [columns] -%}
    {%- endif -%}

    {%- set index_name = 'idx_' ~ this.identifier ~ '_' ~ ('_'.join(columns)) -%}

    create index if not exists {{ index_name }}
    on {{ this }} using {{ index_type }} ({{ columns | join(', ') }});
{% endmacro %}