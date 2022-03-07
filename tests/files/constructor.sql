---
my_table_placeholder: !get_table
my_list_function: !add [1, 2, 3]
my_dict_function: !first
  first_item: this
  second_item: that
---

SELECT * FROM {{my_table_placeholder}} WHERE '{{my_list_function}}' and '{{my_dict_function}}'
