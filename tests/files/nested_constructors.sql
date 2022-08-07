---
my_table_placeholder: !env_switch
  dev: !env_var my_env_var
  default: my_default
my_condition: !env_switch
  dev: !env_switch
    dev: !env_switch
      default: bar
    default: baz
my_other_condition: !env_switch
  default: !previous_date
    - !env_var my_timezone
---

SELECT * FROM {{my_table_placeholder}} WHERE {{my_condition}} AND {{my_other_condition}}
