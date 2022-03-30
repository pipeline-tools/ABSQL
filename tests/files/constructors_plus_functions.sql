---
my_table_placeholder: !env_switch
  default: "{{env_var('somewhere', 'somewhere_else')}}"
---

SELECT * FROM {{my_table_placeholder}}
