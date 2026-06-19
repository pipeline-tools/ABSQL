{% if env_var("GITHUB_WORKSPACE") %}
    {%- include '/home/runner/work/ABSQL/ABSQL/tests/files/includes.md' -%}
{% else %}
    {%- include '/ABSQL/tests/files/includes.md' -%}
{% endif %}
