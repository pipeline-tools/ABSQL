/*
my_table_placeholder: my_table
my_var_dict:
  extra: something different!
*/

SELECT * FROM {{my_table_placeholder}} WHERE {{extra}}
