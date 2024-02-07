/*
my_table_placeholder: "{{get_table()}}"
the_name: "{{env_var('name', 'Ron')}}"
*/

SELECT * FROM {{my_table_placeholder}} WHERE name = '{{the_name}}'
