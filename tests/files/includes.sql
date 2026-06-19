{% if env_var("GITHUB_WORKSPACE") %}
    {%- include env_var("GITHUB_WORKSPACE") ~ '/tests/files/includes.md' -%}
{% else %}
    {%- include '/ABSQL/tests/files/includes.md' -%}
{% endif %}
