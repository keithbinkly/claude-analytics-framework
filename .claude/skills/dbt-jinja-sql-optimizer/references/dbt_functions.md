# Jinja-Sql-Optimizer - Dbt Functions

**Pages:** 67

---

## ignore some folders in a directory

**URL:** llms-txt#ignore-some-folders-in-a-directory

**Contents:**
  - About adapter object
  - About adapter-specific behavior changes
  - About as_bool filter
  - About as_native filter
  - About as_number filter
  - About builtins Jinja variable
  - About config property
  - About config variable
  - About data tests property
  - About dbt --version

path/to/folders/subfolder/**

{%- set target_relation = api.Relation.create(
      database='database_name',
      schema='schema_name',
      identifier='table_name') -%}

{% for col in adapter.get_missing_columns(target_relation, this) %}
  alter table {{this}} add column "{{col.name}}" {{col.data_type}};
{% endfor %}

{% set tmp_relation = adapter.get_relation(...) %}
{% set target_relation = adapter.get_relation(...) %}

{% do adapter.expand_target_column_types(tmp_relation, target_relation) %}

{%- set source_relation = adapter.get_relation(
      database="analytics",
      schema="dbt_drew",
      identifier="orders") -%}

{{ log("Source Relation: " ~ source_relation, info=true) }}

{% set relation_exists = load_relation(ref('my_model')) is not none %}
{% if relation_exists %}
      {{ log("my_model has already been built", info=true) }}
{% else %}
      {{ log("my_model doesn't exist in the warehouse. Maybe it was dropped?", info=true) }}
{% endif %}

{%- set columns = adapter.get_columns_in_relation(this) -%}

{% for column in columns %}
  {{ log("Column: " ~ column, info=true) }}
{% endfor %}

{% do adapter.create_schema(api.Relation.create(database=target.database, schema="my_schema")) %}

{% do adapter.drop_schema(api.Relation.create(database=target.database, schema="my_schema")) %}

{% do adapter.drop_relation(this) %}

{%- set old_relation = adapter.get_relation(
      database=this.database,
      schema=this.schema,
      identifier=this.identifier) -%}

{%- set backup_relation = adapter.get_relation(
      database=this.database,
      schema=this.schema,
      identifier=this.identifier ~ "__dbt_backup") -%}

{% do adapter.rename_relation(old_relation, backup_relation) %}

select 
      'abc' as {{ adapter.quote('table_name') }},
      'def' as {{ adapter.quote('group by') }}

{% set dest_columns = adapter.get_columns_in_table(schema, identifier) %}
{% set dest_cols_csv = dest_columns | map(attribute='quoted') | join(', ') %}

insert into {{ this }} ({{ dest_cols_csv }}) (
  select {{ dest_cols_csv }}
  from {{ref('another_table')}}
);

select * from {{ref('raw_table')}}

{% if adapter.already_exists(this.schema, this.name) %}
  where id > (select max(id) from {{this}})
{% endif %}

{% macro concat(fields) -%}
  {{ adapter_macro('concat', fields) }}
{%- endmacro %}

{% macro default__concat(fields) -%}
    concat({{ fields|join(', ') }})
{%- endmacro %}

{% macro redshift__concat(fields) %}
    {{ fields|join(' || ') }}
{% endmacro %}

{% macro snowflake__concat(fields) %}
    {{ fields|join(' || ') }}
{% endmacro %}

models:
  my_project:
    for_export:
      enabled: "{{ (target.name == 'prod') | as_bool }}"

my_profile:
  outputs:
    dev:
      type: postgres
      port: "{{ env_var('PGPORT') | as_number }}"

-- extract user-provided positional and keyword arguments
{% set version = kwargs.get('version') or kwargs.get('v') %}
{% set packagename = none %}
{%- if (varargs | length) == 1 -%}
    {% set modelname = varargs[0] %}
{%- else -%}
    {% set packagename = varargs[0] %}
    {% set modelname = varargs[1] %}
{% endif %}

-- call builtins.ref based on provided positional arguments
{% set rel = None %}
{% if packagename is not none %}
    {% set rel = builtins.ref(packagename, modelname, version=version) %}
{% else %}
    {% set rel = builtins.ref(modelname, version=version) %}
{% endif %}

-- finally, override the database name with "dev"
{% set newrel = rel.replace_path(database="dev") %}
{% do return(newrel) %}

-- render identifiers without a database
  {% do return(rel.include(database=false)) %}

models:
  - name: <model_name>
    config:
      <model_config>: <config_value>
      ...

seeds:
  - name: <seed_name>
    config:
      <seed_config>: <config_value>
      ...

snapshots:
  - name: <snapshot_name>
    config:
      <snapshot_config>: <config_value>
      ...

<resource_type>:
  - name: <resource_name>
    data_tests:
      - <test_name>:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            <argument_name>: <argument_value>
          config:
            <test_config>: <config-value>
            ...

columns:
      - name: <column_name>
        data_tests:
          - <test_name>
          - <test_name>:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                <argument_name>: <argument_value>
              config:
                <test_config>: <config-value>
                ...

unit_tests:
  - name: <test-name>
    config:
      enabled: true | false
      meta: {dictionary}
      tags: <string>

sources:
  - name: <source_name>
    config:
      <source_config>: <config_value>
    tables:
      - name: <table_name>
        config:
          <source_config>: <config_value>

metrics:
  - name: <metric_name>
    config:
      enabled: true | false
      group: <string>
      meta: {dictionary}

exposures:
  - name: <exposure_name>
    config:
      enabled: true | false
      meta: {dictionary}

semantic_models:
  - name: <semantic_model_name>
    config:
      enabled: true | false
      group: <string>
      meta: {dictionary}

saved-queries:
  - name: <saved_query_name>
    config:
      cache: 
        enabled: true | false
      enabled: true | false
      group: <string>
      meta: {dictionary}
      schema: <string>
    exports:
      - name: <export_name>
        config:
          export_as: view | table 
          alias: <string>
          schema: <string>

{% materialization incremental, default -%}
  {%- set unique_key = config.get('unique_key') -%}
  ...

{{
  config(
    materialized='incremental',
    unique_key='id'
  )
}}

{% materialization incremental, default -%}
  -- Example w/ no default. unique_key will be None if the user does not provide this configuration
  {%- set unique_key = config.get('unique_key') -%}

-- Example w/ alternate value. Use alternative of 'id' if 'unique_key' config is provided, but it is None
  {%- set unique_key = config.get('unique_key') or 'id' -%}

-- Example w/ default value. Default to 'id' if the 'unique_key' config does not exist
  {%- set unique_key = config.get('unique_key', default='id') -%}

-- Example of a custom config nested under `meta` as required in v1.10 and higher.
  {% set my_custom_config = config.get('meta').custom_config_key %}
  ...

{% materialization incremental, default -%}
  {%- set unique_key = config.require('unique_key') -%}
  ...

models:
  - name: <model_name>
    data_tests:
      - <test_name>:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            <argument_name>: <argument_value>
          config:
            <test_config>: <config-value>

columns:
      - name: <column_name>
        data_tests:
          - <test_name>
          - <test_name>:
              arguments:
                <argument_name>: <argument_value>
              config:
                <test_config>: <config-value>

sources:
  - name: <source_name>
    tables:
    - name: <table_name>
      data_tests:
        - <test_name>
        - <test_name>:
            arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
              <argument_name>: <argument_value>
            config:
              <test_config>: <config-value>

columns:
        - name: <column_name>
          data_tests:
            - <test_name>
            - <test_name>:
                arguments:
                  <argument_name>: <argument_value>
                config:
                  <test_config>: <config-value>

seeds:
  - name: <seed_name>
    data_tests:
      - <test_name>
      - <test_name>:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            <argument_name>: <argument_value>
          config:
            <test_config>: <config-value>

columns:
      - name: <column_name>
        data_tests:
          - <test_name>
          - <test_name>:
              arguments:
                <argument_name>: <argument_value>
              config:
                <test_config>: <config-value>

snapshots:
  - name: <snapshot_name>
    data_tests:
      - <test_name>
      - <test_name>:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            <argument_name>: <argument_value>
          config:
            <test_config>: <config-value>

columns:
      - name: <column_name>
        data_tests:
          - <test_name>
          - <test_name>:
              arguments:
                <argument_name>: <argument_value>
              config:
                <test_config>: <config-value>

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - not_null

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique:
              config:
                where: "order_id > 21"

models:
  - name: orders
    columns:
      - name: status
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['placed', 'shipped', 'completed', 'returned']

- name: status_id
        data_tests:
          - accepted_values:
              arguments:
                values: [1, 2, 3, 4]
                quote: false

models:
  - name: orders
    columns:
      - name: customer_id
        data_tests:
          - relationships:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                to: ref('customers')
                field: id

models:
  - name: orders
    description: 
        Order overview data mart, offering key details for each order including if it's a customer's first order and a food vs. drink item breakdown. One row per order.
    data_tests:
      - dbt_utils.expression_is_true:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            expression: "order_items_subtotal = subtotal"
      - dbt_utils.expression_is_true:
          arguments:
            expression: "order_total = subtotal + tax_paid"

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - primary_key  # name of my custom generic test

models:
  - name: orders
    columns:
      - name: status
        data_tests:
          - accepted_values:
              name: unexpected_order_status_today
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['placed', 'shipped', 'completed', 'returned']
              config:
                where: "order_date = current_date"

$ dbt test --select unexpected_order_status_today
12:43:41  Running with dbt=1.1.0
12:43:41  Found 1 model, 1 test, 0 snapshots, 0 analyses, 167 macros, 0 operations, 1 seed file, 0 sources, 0 exposures, 0 metrics
12:43:41
12:43:41  Concurrency: 5 threads (target='dev')
12:43:41
12:43:41  1 of 1 START test unexpected_order_status_today ................................ [RUN]
12:43:41  1 of 1 PASS unexpected_order_status_today ...................................... [PASS in 0.03s]
12:43:41
12:43:41  Finished running 1 test in 0.13s.
12:43:41
12:43:41  Completed successfully
12:43:41
12:43:41  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1

models:
  - name: orders
    columns:
      - name: status
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['placed', 'shipped', 'completed', 'returned']
              config:
                where: "order_date = current_date"
          - accepted_values:
              arguments:
                values: ['placed', 'shipped', 'completed', 'returned']
              config:
                # only difference is in the 'where' config
                where: "order_date = (current_date - interval '1 day')" # PostgreSQL syntax

Compilation Error
  dbt found two tests with the name "accepted_values_orders_status__placed__shipped__completed__returned" defined on column "status" in "models.orders".

Since these resources have the same name, dbt will be unable to find the correct resource
  when running tests.

To fix this, change the name of one of these resources:
  - test.testy.accepted_values_orders_status__placed__shipped__completed__returned.69dce9e5d5 (models/one_file.yml)
  - test.testy.accepted_values_orders_status__placed__shipped__completed__returned.69dce9e5d5 (models/one_file.yml)

models:
  - name: orders
    columns:
      - name: status
        data_tests:
          - accepted_values:
              name: unexpected_order_status_today
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['placed', 'shipped', 'completed', 'returned']
              config:
                where: "order_date = current_date"
          - accepted_values:
              name: unexpected_order_status_yesterday
              arguments:
                values: ['placed', 'shipped', 'completed', 'returned']
              config:
                where: "order_date = (current_date - interval '1 day')" # PostgreSQL

$ dbt test
12:48:03  Running with dbt=1.1.0-b1
12:48:04  Found 1 model, 2 tests, 0 snapshots, 0 analyses, 167 macros, 0 operations, 1 seed file, 0 sources, 0 exposures, 0 metrics
12:48:04
12:48:04  Concurrency: 5 threads (target='dev')
12:48:04
12:48:04  1 of 2 START test unexpected_order_status_today ................................ [RUN]
12:48:04  2 of 2 START test unexpected_order_status_yesterday ............................ [RUN]
12:48:04  1 of 2 PASS unexpected_order_status_today ...................................... [PASS in 0.04s]
12:48:04  2 of 2 PASS unexpected_order_status_yesterday .................................. [PASS in 0.04s]
12:48:04
12:48:04  Finished running 2 tests in 0.21s.
12:48:04
12:48:04  Completed successfully
12:48:04
12:48:04  Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2

models:
  - name: orders
    columns:
      - name: status
        data_tests:
          - name: unexpected_order_status_today
            test_name: accepted_values  # name of the generic test to apply
            arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
              values:
                - placed
                - shipped
                - completed
                - returned
            config:
              where: "order_date = current_date"

$ dbt --version
Core:
  - installed: 1.7.6
  - latest:    1.7.6 - Up to date!
Plugins:
  - snowflake: 1.7.1 - Up to date!

$ dbt --version
Cloud CLI - 0.35.7 (fae78a6f5f6f2d7dff3cab3305fe7f99bd2a36f3 2024-01-18T22:34:52Z)

{{ config(
    pre_hook = [
        "alter external table {{ source('sys', 'customers').render() }} refresh"
    ]
) }}

$ dbt build
Running with dbt=1.9.0-b2
Found 1 model, 4 tests, 1 snapshot, 1 analysis, 341 macros, 0 operations, 1 seed file, 2 sources, 2 exposures

18:49:43 | Concurrency: 1 threads (target='dev')
18:49:43 |
18:49:43 | 1 of 7 START seed file dbt_jcohen.my_seed............................ [RUN]
18:49:43 | 1 of 7 OK loaded seed file dbt_jcohen.my_seed........................ [INSERT 2 in 0.09s]
18:49:43 | 2 of 7 START view model dbt_jcohen.my_model.......................... [RUN]
18:49:43 | 2 of 7 OK created view model dbt_jcohen.my_model..................... [CREATE VIEW in 0.12s]
18:49:43 | 3 of 7 START test not_null_my_seed_id................................ [RUN]
18:49:43 | 3 of 7 PASS not_null_my_seed_id...................................... [PASS in 0.05s]
18:49:43 | 4 of 7 START test unique_my_seed_id.................................. [RUN]
18:49:43 | 4 of 7 PASS unique_my_seed_id........................................ [PASS in 0.03s]
18:49:43 | 5 of 7 START snapshot snapshots.my_snapshot.......................... [RUN]
18:49:43 | 5 of 7 OK snapshotted snapshots.my_snapshot.......................... [INSERT 0 5 in 0.27s]
18:49:43 | 6 of 7 START test not_null_my_model_id............................... [RUN]
18:49:43 | 6 of 7 PASS not_null_my_model_id..................................... [PASS in 0.03s]
18:49:43 | 7 of 7 START test unique_my_model_id................................. [RUN]
18:49:43 | 7 of 7 PASS unique_my_model_id....................................... [PASS in 0.02s]
18:49:43 |
18:49:43 | Finished running 1 seed, 1 view model, 4 tests, 1 snapshot in 1.01s.

Completed successfully

Done. PASS=7 WARN=0 ERROR=0 SKIP=0 TOTAL=7

dbt build --select "resource_type:function"
dbt-fusion 2.0.0-preview.45
 Succeeded [  0.98s] function dbt_schema.whoami (function)
 Succeeded [  1.12s] function dbt_schema.area_of_circle (function)

dbt clean --clean-project-files-only

dbt clean --no-clean-project-files-only

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About adapter object

Your database communicates with dbt using an internal database adapter object. For example, BaseAdapter and SnowflakeAdapter. The Jinja object `adapter` is a wrapper around this internal database adapter object.

`adapter` grants the ability to invoke adapter methods of that internal class via:

* `{% do adapter.<method name> %}` -- invoke internal adapter method
* `{{ adapter.<method name> }}` -- invoke internal adapter method and capture its return value for use in materialization or other macros

For example, the adapter methods below will be translated into specific SQL statements depending on the type of adapter your project is using:

* [adapter.dispatch](https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch.md)
* [adapter.get\_missing\_columns](#get_missing_columns)
* [adapter.expand\_target\_column\_types](#expand_target_column_types)
* [adapter.get\_relation](#get_relation) or [load\_relation](#load_relation)
* [adapter.get\_columns\_in\_relation](#get_columns_in_relation)
* [adapter.create\_schema](#create_schema)
* [adapter.drop\_schema](#drop_schema)
* [adapter.drop\_relation](#drop_relation)
* [adapter.rename\_relation](#rename_relation)
* [adapter.quote](#quote)

##### Deprecated adapter functions[​](#deprecated-adapter-functions "Direct link to Deprecated adapter functions")

The following adapter functions are deprecated, and will be removed in a future release.

* [adapter.get\_columns\_in\_table](#get_columns_in_table) **(deprecated)**
* [adapter.already\_exists](#already_exists) **(deprecated)**
* [adapter\_macro](#adapter_macro) **(deprecated)**

#### dispatch[​](#dispatch "Direct link to dispatch")

Moved to separate page: [dispatch](https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch.md)

#### get\_missing\_columns[​](#get_missing_columns "Direct link to get_missing_columns")

**Args**:

* `from_relation`: The source [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation)
* `to_relation`: The target [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation)

Returns a list of [Columns](https://docs.getdbt.com/reference/dbt-classes.md#column) that is the difference of the columns in the `from_table` and the columns in the `to_table`, i.e. (`set(from_relation.columns) - set(to_table.columns)`). Useful for detecting new columns in a source table.

**Usage**:

models/example.sql
```

Example 2 (unknown):
```unknown
#### expand\_target\_column\_types[​](#expand_target_column_types "Direct link to expand_target_column_types")

**Args**:

* `from_relation`: The source [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation) to use as a template
* `to_relation`: The [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation) to mutate

Expand the `to_relation` table's column types to match the schema of `from_relation`. Column expansion is constrained to string and numeric types on supported databases. Typical usage involves expanding column types (from eg. `varchar(16)` to `varchar(32)`) to support insert statements.

**Usage**:

example.sql
```

Example 3 (unknown):
```unknown
#### get\_relation[​](#get_relation "Direct link to get_relation")

**Args**:

* `database`: The database of the relation to fetch
* `schema`: The schema of the relation to fetch
* `identifier`: The identifier of the relation to fetch

Returns a cached [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation) object identified by the `database.schema.identifier` provided to the method, or `None` if the relation does not exist.

**Usage**:

example.sql
```

Example 4 (unknown):
```unknown
#### load\_relation[​](#load_relation "Direct link to load_relation")

**Args**:

* `relation`: The [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation) to try to load

A convenience wrapper for [get\_relation](#get_relation). Returns the cached version of the [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation) object, or `None` if the relation does not exist.

**Usage**:

example.sql
```

---

## Import custom packages from Conda environments

**URL:** llms-txt#import-custom-packages-from-conda-environments

**Contents:**
  - About Fusion local installation [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - Install Fusion from the CLI [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - Install the dbt VS Code extension [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - dbt platform
  - Connect Teradata [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")

import nltk
import gensim

def model(dbt, session):
    dbt.config(materialized="table")
    dbt.config(conda_env_name="dbt_py_env")  # Refer the conda environment
    dbt.config(async_flag=True) # Use async mode for long running Python jobs
    dbt.config(timeout=900)
    # oml.core.DataFrame referencing a dbt-sql model
    promotion_cost = dbt.ref("direct_sales_channel_promo_cost")
    return promotion_cost

company-name:
  target: dev
  outputs:
    dev:
      type: postgres
      host: [hostname]
      user: [username]
      password: [password]
      port: [port]
      dbname: [database name] # or database instead of dbname
      schema: [dbt schema]
      threads: [optional, 1 or more]
      keepalives_idle: 0 # default 0, indicating the system default. See below
      connect_timeout: 10 # default 10 seconds
      retries: 1  # default 1 retry on error/timeout when opening connections
      search_path: [optional, override the default postgres search_path]
      role: [optional, set the role dbt assumes when executing queries]
      sslmode: [optional, set the sslmode used to connect to the database]
      sslcert: [optional, set the sslcert to control the certifcate file location]
      sslkey: [optional, set the sslkey to control the location of the private key]
      sslrootcert: [optional, set the sslrootcert config value to a new file path in order to customize the file location that contain root certificates]

pip install dbt-postgres
if [[ $(pip show psycopg2-binary) ]]; then
    PSYCOPG2_VERSION=$(pip show psycopg2-binary | grep Version | cut -d " " -f 2)
    pip uninstall -y psycopg2-binary && pip install psycopg2==$PSYCOPG2_VERSION
fi

sudo apt-get update
sudo apt-get install libpq-dev python-dev

brew install postgresql
pip install psycopg2

company-name:
  target: dev
  outputs:
    dev:
      type: redshift
      host: hostname.region.redshift.amazonaws.com
      user: username
      password: password1
      dbname: analytics
      schema: analytics
      port: 5439

# Optional Redshift configs:
      sslmode: prefer
      role: None
      ra3_node: true 
      autocommit: true 
      threads: 4
      connect_timeout: None

my-redshift-db:
  target: dev
  outputs:
    dev:
      type: redshift
      method: iam
      cluster_id: CLUSTER_ID
      host: hostname.region.redshift.amazonaws.com
      user: alice
      iam_profile: analyst
      region: us-east-1
      dbname: analytics
      schema: analytics
      port: 5439

# Optional Redshift configs:
      threads: 4
      connect_timeout: None 
      retries: 1 
      role: None
      sslmode: prefer 
      ra3_node: true  
      autocommit: true  
      autocreate: true  
      db_groups: ['ANALYSTS']

profile-to-my-RS-target:
  target: dev
  outputs:
    dev:
      type: redshift
      ...
      autocommit: False
      
  
  profile-to-my-RS-target-with-autocommit-enabled:
  target: dev
  outputs:
    dev:
      type: redshift
      ...
      autocommit: True

default:
  outputs:
    dev:
      type: risingwave
      host: [host name] 
      user: [user name]
      pass: [password]
      dbname: [database name]
      port: [port]
      schema: [dbt schema]
  target: dev

rockset:
  target: dev
  outputs:
    dev:
      type: rockset
      workspace: [schema]
      api_key: [api_key]
      api_server: [api_server] # (Default is api.rs2.usw2.rockset.com)

singlestore:
  target: dev
  outputs:
    dev:
      type: singlestore
      host: [hostname]  # optional, default localhost
      port: [port number]  # optional, default 3306
      user: [user]  # optional, default root
      password: [password]  # optional, default empty
      database: [database name]  # required
      schema: [prefix for tables that dbt will generate]  # required
      threads: [1 or more]  # optional, default 1

-- macros/generate_alias_name.sql
{% macro generate_alias_name(custom_alias_name=none, node=none) -%}
    {%- if custom_alias_name is none -%}
        {{ node.schema }}__{{ node.name }}
    {%- else -%}
        {{ node.schema }}__{{ custom_alias_name | trim }}
    {%- endif -%}
{%- endmacro %}

my-snowflake-db:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: [account id]
      
      # The following fields are retrieved from the Snowflake configuration
      authenticator: oauth
      oauth_client_id: [OAuth client id]
      oauth_client_secret: [OAuth client secret]
      token: [OAuth refresh token]

your_profile_name:
  target: dev
  outputs:
    dev:
      type: sqlite
      threads: 1
      database: 'database'
      schema: 'main'
      schemas_and_paths:
        main: 'file_path/database_name.db'
      schema_directory: 'file_path'
      #optional fields
      extensions:
        - "/path/to/sqlean/crypto.so"

trino:
  target: dev
  outputs:
    dev:
      type: trino
      method: ldap 
      user: [user]
      password: [password]
      host: [hostname]
      database: [database name]
      schema: [your dbt schema]
      port: [port number]
      threads: [1 or more]

trino:
  target: dev
  outputs:
    dev:
      type: trino
      method: kerberos
      user: commander
      keytab: /tmp/trino.keytab
      krb5_config: /tmp/krb5.conf
      principal: trino@EXAMPLE.COM
      host: trino.example.com
      port: 443
      database: analytics
      schema: public

trino:
  target: dev
  outputs:
    dev:
      type: trino
      method: jwt 
      jwt_token: [my_long_jwt_token_string]
      host: [hostname]
      database: [database name]
      schema: [your dbt schema]
      port: [port number]
      threads: [1 or more]

trino:
  target: dev
  outputs:
    dev:
      type: trino
      method: certificate 
      cert: [path/to/cert_file]
      client_certificate: [path/to/client/cert]
      client_private_key: [path to client key]
      database: [database name]
      schema: [your dbt schema]
      port: [port number]
      threads: [1 or more]

sandbox-galaxy:
  target: oauth
  outputs:
    oauth:
      type: trino
      method: oauth
      host: bunbundersders.trino.galaxy-dev.io
      catalog: dbt_target
      schema: dataders
      port: 443

sandbox-galaxy:
  target: oauth_console
  outputs:
    oauth:
      type: trino
      method: oauth_console
      host: bunbundersders.trino.galaxy-dev.io
      catalog: dbt_target
      schema: dataders
      port: 443

trino:
  target: dev
  outputs:
    dev:
      type: trino
      method: none
      user: commander
      host: trino.example.com
      port: 443
      database: analytics
      schema: public

my-starrocks-db:
  target: dev
  outputs:
    dev:
      type: starrocks
      host: localhost
      port: 9030
      schema: analytics
      
      # User/password auth
      username: your_starrocks_username
      password: your_starrocks_password

<profile-name>:
  target: <target-name>
  outputs:
    <target-name>:
      type: teradata
      user: <username>
      password: <password>
      schema: <database-name>
      tmode: ANSI
      threads: [optional, 1 or more]
      #optional fields
      <field-name: <field-value>

CREATE DATABASE GLOBAL_FUNCTIONS AS PERMANENT = 60e6, SPOOL = 120e6;
   
   GRANT CREATE FUNCTION ON GLOBAL_FUNCTIONS TO <CURRENT_USER>;
   DATABASE GLOBAL_FUNCTIONS;
   .run file = hash_md5.btq
   
   GRANT EXECUTE FUNCTION ON GLOBAL_FUNCTIONS TO PUBLIC WITH GRANT OPTION;
   
vars:
  md5_udf: Custom_database_name.hash_method_function

dbt-tidb:
  target: dev
  outputs:
    dev:
      type: tidb
      server: 127.0.0.1
      port: 4000
      schema: database_name
      username: tidb_username
      password: tidb_password

# optional
      retries: 3 # default 1

my-upsolver-db:
  target: dev
  outputs:
    dev:
      type: upsolver
      api_url: https://mt-api-prod.upsolver.com

user: [username]
      token: [token]

database: [database name]
      schema: [schema name]
      threads: [1 or more]

your-profile:
  outputs:
    dev:
      type: vertica # Don't change this!
      host: [hostname]
      port: [port] # or your custom port (optional)
      username: [your username]
      password: [your password]
      database: [database name]
      oauth_access_token: [access token]
      schema: [dbt schema]
      connection_load_balance: True
      backup_server_node: [list of backup hostnames or IPs]
      retries: [1 or more]
      autocommit: False
      
      threads: [1 or more]
  target: dev

profile-name:
  target: dev
  outputs:
    dev:
      type: ydb
      host: localhost
      port: 2136
      database: /local
      schema: empty_string
      secure: False
      root_certificates_path: empty_string

# Static credentials
      username: empty_string
      password: empty_string

# Access token credentials
      token: empty_string

# Service account credentials
      service_account_credentials_file: empty_string

company-name:
  target: dev
  outputs:
    dev:
      type: yellowbrick
      host: [hostname]
      user: [username]
      password: [password]
      port: [port]
      dbname: [database name]
      schema: [dbt schema]
      role: [optional, set the role dbt assumes when executing queries]
      sslmode: [optional, set the sslmode used to connect to the database]
      sslrootcert: [optional, set the sslrootcert config value to a new file path to customize the file location that contains root certificates]

git clone https://github.com/dbt-labs/dbt-core.git
cd dbt-core
python -m pip install -r requirements.txt

python -m pip install -e editable-requirements.txt`

git clone https://github.com/dbt-labs/dbt-redshift.git
cd dbt-redshift
python -m pip install .

sudo yum install redhat-rpm-config gcc libffi-devel \
  python-devel openssl-devel

sudo apt-get install git libpq-dev python-dev python3-pip
sudo apt-get remove python-cffi
sudo pip install --upgrade cffi
pip install cryptography~=3.4

python3 -m venv dbt-env				# create the environment
source dbt-env/bin/activate			# activate the environment for Mac and Linux
dbt-env\Scripts\activate			# activate the environment for Windows

python -m pip install --upgrade pip wheel setuptools

docker pull ghcr.io/dbt-labs/<db_adapter_name>:<version_tag>

docker run \
--network=host \
--mount type=bind,source=path/to/project,target=/usr/app \
--mount type=bind,source=path/to/profiles.yml,target=/root/.dbt/profiles.yml \
<dbt_image_name> \
ls

docker run \
--network=host \
--mount type=bind,source=path/to/project,target=/usr/app \
--mount type=bind,source=path/to/profiles.yml.dbt,target=/root/.dbt/ \
<dbt_image_name> \
ls

sudo yum install redhat-rpm-config gcc libffi-devel \
  python-devel openssl-devel

sudo apt-get install git libpq-dev python-dev python3-pip
sudo apt-get remove python-cffi
sudo pip install --upgrade cffi
pip install cryptography~=3.4

source env/bin/activate

.env\Scripts\activate

alias env_dbt='source <PATH_TO_VIRTUAL_ENV_CONFIG>/bin/activate'

python -m pip install dbt-core dbt-ADAPTER_NAME

python -m pip install dbt-core dbt-postgres

$ dbt --version
installed version: 1.0.0
   latest version: 1.0.0

Plugins:
  - postgres: 1.0.0

python -m pip install --upgrade dbt-ADAPTER_NAME

python -m pip install dbt-core

python -m pip install --upgrade dbt-core

python -m pip install --upgrade dbt-core==1.9

python -m pip install \
  dbt-core \
  dbt-postgres \
  dbt-redshift \
  dbt-snowflake \
  dbt-bigquery \
  dbt-trino

python3 -m pip install --pre dbt-core dbt-adapter-name

python3 -m pip install --pre dbt-core dbt-snowflake

dbt --version
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install --pre dbt-core dbt-adapter-name
source .venv/bin/activate
dbt --version

source .venv/bin/activate
which python
.venv/bin/python

python3 -m pip install --pre dbt-core dbt-adapter-name
source .venv/bin/activate
dbt --version

.venv\Scripts\activate
where python
.venv\Scripts\python

py -m pip install --pre dbt-core dbt-adapter-name
.venv\Scripts\activate
dbt --version

curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | sh -s -- --update

irm https://public.cdn.getdbt.com/fs/install/install.ps1 | iex

Start-Process powershell

dbtf system uninstall

dbt init --fusion-upgrade

mkdir ~/.dbt # macOS
mkdir %USERPROFILE%\.dbt # Windows

mv ~/Downloads/dbt_cloud.yml ~/.dbt/dbt_cloud.yml

move %USERPROFILE%\Downloads\dbt_cloud.yml %USERPROFILE%\.dbt\dbt_cloud.yml

dbt-cloud:
project-id: 12345 # Required

dbname: jaffle_shop      
schema: dbt_alice      
threads: 4
username: alice
password: '{{ env_var(''DBT_ENV_SECRET_PASSWORD'') }}'

curl --request POST \
   --url https://cloud.getdbt.com/api/v3/accounts/XXXXX/projects/YYYYY/environment-variables/bulk/ \
   --header 'Accept: application/json' \
   --header 'Authorization: Bearer ZZZZZ' \
   --header 'Content-Type: application/json' \
   --data '{
   "env_var": [
   {
       "new_name": "DBT_ENV_SECRET_PROJECTXXX_PRIVATE_KEY",
       "project": "Value by default for the entire project",
       "ENVIRONMENT_NAME_1": "Optional, if wanted, value for environment name 1",
       "ENVIRONMENT_NAME_2": "Optional, if wanted, value for environment name 2"
   }
   ]
   }'
   
   keyfile_json:
     type: service_account
     project_id: xxx
     private_key_id: xxx
     private_key: '{{ env_var(''DBT_ENV_SECRET_PROJECTXXX_PRIVATE_KEY'') }}'
     client_email: xxx
     client_id: xxx
     auth_uri: xxx
     token_uri: xxx
     auth_provider_x509_cert_url: xxx
     client_x509_cert_url: xxx
   
   priority: interactive
   keyfile_json:
     type: xxx
     project_id: xxx
     private_key_id: xxx
     private_key: '{{ env_var(''DBT_ENV_SECRET_PROJECTXXX_PRIVATE_KEY'') }}'
     client_email: xxx
     client_id: xxx
     auth_uri: xxx
     token_uri: xxx
     auth_provider_x509_cert_url: xxx
     client_x509_cert_url: xxx
   execution_project: buck-stops-here-456
   
   curl --request POST \
   --url https://cloud.getdbt.com/api/v3/accounts/XXXXX/projects/YYYYY/extended-attributes/ \
   --header 'Accept: application/json' \
   --header 'Authorization: Bearer ZZZZZ' \
   --header 'Content-Type: application/json' \
   --data '{
   "id": null,
   "extended_attributes": {"type":"service_account","project_id":"xxx","private_key_id":"xxx","private_key":"{{ env_var('DBT_ENV_SECRET_PROJECTXXX_PRIVATE_KEY')    }}","client_email":"xxx","client_id":xxx,"auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"xxx"},
   "state": 1
   }'
   
   curl --request POST \
   --url https://cloud.getdbt.com/api/v3/accounts/XXXXX/projects/YYYYY/environments/EEEEE/ \
   --header 'Accept: application/json' \
   --header 'Authorization: Bearer ZZZZZZ' \
   --header 'Content-Type: application/json' \
   --data '{
     "extended_attributes_id": FFFFF
   }'
   
      +materialized: table | incremental
      +file_format: hudi
      +location_root: <storage_uri>
      +tblproperties:
         hoodie.table.type: mor | cow

models:
  jaffle_shop:
    +file_format: hudi
    +location_root: s3://lakehouse/demolake/dbt_ecomm/
    +tblproperties:
      hoodie.table.type: mor
    staging:
      +materialized: incremental
    marts:
      +materialized: table

sudo groupadd dbtcloud
   sudo useradd -m -g dbtcloud dbtcloud
   sudo su - dbtcloud
   mkdir ~/.ssh
   chmod 700 ~/.ssh
   touch ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   
host: my-production-instance.myregion.redshift-serverless.amazonaws.com
method: iam
region: us-east-2
access_key_id: '{{ env_var(''DBT_ENV_ACCESS_KEY_ID'') }}'
secret_access_key: '{{ env_var(''DBT_ENV_SECRET_ACCESS_KEY'') }}'

sudo groupadd dbtcloud
   sudo useradd -m -g dbtcloud dbtcloud
   sudo su - dbtcloud
   mkdir ~/.ssh
   chmod 700 ~/.ssh
   touch ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/authorized_keys
   
  authenticator: username_password_mfa
  
  connect_retries: 0
  
   alter user jsmith set rsa_public_key='MIIBIjANBgkqh...';   
   
-----BEGIN ENCRYPTED PRIVATE KEY-----
< encrypted private key contents here - line 1 >
< encrypted private key contents here - line 2 >
< ... >
-----END ENCRYPTED PRIVATE KEY-----

host: https://custom_domain_to_snowflake.com

**Examples:**

Example 1 (unknown):
```unknown
#### Supported features[​](#supported-features "Direct link to Supported features")

* Table materialization
* View materialization
* Materialized View
* Incremental materialization
* Seeds
* Data sources
* Singular tests
* Generic tests; Not null, Unique, Accepted values and Relationships
* Operations
* Analyses
* Exposures
* Document generation
* Serve project documentation as a website
* Python Models (from dbt-oracle version 1.5.1)
* Integration with Conda to use any Python packages from Anaconda's repository
* All dbt commands are supported

#### Not supported features[​](#not-supported-features "Direct link to Not supported features")

* Ephemeral materialization

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

##### Postgres setup

`profiles.yml` file is for dbt Core and dbt fusion only

If you're using dbt platform, you don't need to create a `profiles.yml` file. This file is only necessary when you use dbt Core or dbt Fusion locally. To learn more about Fusion prerequisites, refer to [About Fusion installation](https://docs.getdbt.com/docs/fusion/install-fusion.md). To connect your data platform to dbt, refer to [About data platforms](https://docs.getdbt.com/docs/cloud/connect-data-platform/about-connections.md).

<!-- -->

* **Maintained by**:
  <!-- -->
  dbt Labs
* **Authors**:
  <!-- -->
  core dbt maintainers
* **GitHub repo**: [dbt-labs/dbt-adapters](https://github.com/dbt-labs/dbt-adapters) [![](https://img.shields.io/github/stars/dbt-labs/dbt-adapters?style=for-the-badge)](https://github.com/dbt-labs/dbt-adapters)
* **PyPI package**: `dbt-postgres` [![](https://badge.fury.io/py/dbt-postgres.svg)](https://badge.fury.io/py/dbt-postgres)
* **Slack channel**: [#db-postgres](https://getdbt.slack.com/archives/C0172G2E273)
* **Supported dbt Core version**:
  <!-- -->
  v0.4.0
  <!-- -->
  and newer
* **dbt support**:
  <!-- -->
  Supported
* **Minimum data platform version**:
  <!-- -->
  n/a

#### Installing <!-- -->dbt-postgres

Use `pip` to install the adapter. Before 1.8, installing the adapter would automatically install `dbt-core` and any additional dependencies. Beginning in 1.8, installing an adapter does not automatically install `dbt-core`. This is because adapters and dbt Core versions have been decoupled from each other so we no longer want to overwrite existing dbt-core installations. Use the following command for installation:

`python -m pip install dbt-core dbt-postgres`

#### Configuring <!-- -->dbt-postgres<!-- -->

For <!-- -->Postgres<!-- -->-specific configuration, please refer to [Postgres<!-- --> configs.](https://docs.getdbt.com/reference/resource-configs/postgres-configs.md)

#### Profile Configuration[​](#profile-configuration "Direct link to Profile Configuration")

Postgres targets should be set up using the following configuration in your `profiles.yml` file.

\~/.dbt/profiles.yml
```

Example 2 (unknown):
```unknown
##### Configurations[​](#configurations "Direct link to Configurations")

###### search\_path[​](#search_path "Direct link to search_path")

The `search_path` config controls the Postgres "search path" that dbt configures when opening new connections to the database. By default, the Postgres search path is `"$user, public"`, meaning that unqualified table names will be searched for in the `public` schema, or a schema with the same name as the logged-in user. **Note:** Setting the `search_path` to a custom value is not necessary or recommended for typical usage of dbt.

###### role[​](#role "Direct link to role")

The `role` config controls the Postgres role that dbt assumes when opening new connections to the database.

###### sslmode[​](#sslmode "Direct link to sslmode")

The `sslmode` config controls how dbt connects to Postgres databases using SSL. See [the Postgres docs](https://www.postgresql.org/docs/9.1/libpq-ssl.html) on `sslmode` for usage information. When unset, dbt will connect to databases using the Postgres default, `prefer`, as the `sslmode`.

###### sslcert[​](#sslcert "Direct link to sslcert")

The `sslcert` config controls the location of the certificate file used to connect to Postgres when using client SSL connections. To use a certificate file that is not in the default location, set that file path using this value. Without this config set, dbt uses the Postgres default locations. See [Client Certificates](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-CLIENTCERT) in the Postgres SSL docs for the default paths.

###### sslkey[​](#sslkey "Direct link to sslkey")

The `sslkey` config controls the location of the private key for connecting to Postgres using client SSL connections. If this config is omitted, dbt uses the default key location for Postgres. See [Client Certificates](https://www.postgresql.org/docs/current/libpq-ssl.html#LIBPQ-SSL-CLIENTCERT) in the Postgres SSL docs for the default locations.

###### sslrootcert[​](#sslrootcert "Direct link to sslrootcert")

When connecting to a Postgres server using a client SSL connection, dbt verifies that the server provides an SSL certificate signed by a trusted root certificate. These root certificates are in the `~/.postgresql/root.crt` file by default. To customize the location of this file, set the `sslrootcert` config value to a new file path.

##### `keepalives_idle`[​](#keepalives_idle "Direct link to keepalives_idle")

If the database closes its connection while dbt is waiting for data, you may see the error `SSL SYSCALL error: EOF detected`. Lowering the [`keepalives_idle` value](https://www.postgresql.org/docs/9.3/libpq-connect.html) may prevent this, because the server will send a ping to keep the connection active more frequently.

[dbt's default setting](https://github.com/dbt-labs/dbt-core/blob/main/plugins/postgres/dbt/adapters/postgres/connections.py#L28) is 0 (the server's default value), but can be configured lower (perhaps 120 or 60 seconds), at the cost of a chattier network connection.

###### retries[​](#retries "Direct link to retries")

If `dbt-postgres` encounters an operational error or timeout when opening a new connection, it will retry up to the number of times configured by `retries`. The default value is 1 retry. If set to 2+ retries, dbt will wait 1 second before retrying. If set to 0, dbt will not retry at all.

##### `psycopg2` vs `psycopg2-binary`[​](#psycopg2-vs-psycopg2-binary "Direct link to psycopg2-vs-psycopg2-binary")

`psycopg2-binary` is installed by default when installing `dbt-postgres`. Installing `psycopg2-binary` uses a pre-built version of `psycopg2` which may not be optimized for your particular machine. This is ideal for development and testing workflows where performance is less of a concern and speed and ease of install is more important. However, production environments will benefit from a version of `psycopg2` which is built from source for your particular operating system, and architecture. In this scenario, speed and ease of install is less important as the on-going usage is the focus.

To use `psycopg2`:

1. Install `dbt-postgres`
2. Uninstall `psycopg2-binary`
3. Install the equivalent version of `psycopg2`
```

Example 3 (unknown):
```unknown
Installing `psycopg2` often requires OS level dependencies. These dependencies may vary across operating systems and architectures.

For example, on Ubuntu, you need to install `libpq-dev` and `python-dev`:
```

Example 4 (unknown):
```unknown
whereas on Mac, you need to install `postgresql`:
```

---

## tests on all sources

**URL:** llms-txt#tests-on-all-sources

dbt test --select "source:*"

---

## Local package

**URL:** llms-txt#local-package

**Contents:**
  - About dbt docs commands
  - About dbt environment command
  - About dbt init command
  - About dbt invocation command
  - About dbt ls (list) command
  - About dbt parse command
  - About dbt retry command
  - About dbt rpc command

dbt deps --add-package /opt/dbt/redshift --source local

dbt docs generate --select +orders

dbt docs generate --no-compile

dbt docs generate --empty-catalog

dbt docs generate --static

dbt docs serve --port 8001

❯ dbt env show
Local Configuration:
  Active account ID              185854
  Active project ID              271692
  Active host name               cloud.getdbt.com
  dbt_cloud.yml file path        /Users/cesar/.dbt/dbt_cloud.yml
  dbt_project.yml file path      /Users/cesar/git/cloud-cli-test-project/dbt_project.yml
  <Constant name="cloud" /> CLI version          0.35.7
  OS info                        darwin arm64

Cloud Configuration:
  Account ID                     185854
  Project ID                     271692
  Project name                   Snowflake
  Environment ID                 243762
  Environment name               Development
  Defer environment ID           [N/A]
  dbt version                    1.6.0-latest
  Target name                    default
  Connection type                snowflake

Snowflake Connection Details:
  Account                        ska67070
  Warehouse                      DBT_TESTING_ALT
  Database                       DBT_TEST
  Schema                         CLOUD_CLI_TESTING
  Role                           SYSADMIN
  User                           dbt_cloud_user
  Client session keep alive      false

dbt environment [command] --help
  
    ❯ dbt help environment
    Interact with dbt environments

Usage:
    dbt environment [command]

Aliases:
    environment, env

Available Commands:
    show        Show the working environment

Flags:
    -h, --help   help for environment

Use "dbt environment [command] --help" for more information about a command.
  
  dbt environment show --help
  dbt env show -h
  
fixed:
  account: abc123
  authenticator: externalbrowser
  database: analytics
  role: transformer
  type: snowflake
  warehouse: transforming
prompts:
  target:
    type: string
    hint: your desired target name
  user:
    type: string
    hint: yourname@jaffleshop.com
  schema:
    type: string
    hint: usually dbt_<yourname>
  threads:
    hint: "your favorite number, 1-10"
    type: int
    default: 8

$ dbt init
Running with dbt=1.0.0
Setting up your profile.
user (yourname@jaffleshop.com): summerintern@jaffleshop.com
schema (usually dbt_<yourname>): dbt_summerintern
threads (your favorite number, 1-10) [8]: 6
Profile internal-snowflake written to /Users/intern/.dbt/profiles.yml using project's profile_template.yml and your supplied values. Run 'dbt debug' to validate the connection.

dbt invocation help
Manage invocations

Usage:
  dbt invocation [command]

Available Commands:
  list        List active invocations

Flags:
  -h, --help   help for invocation

Global Flags:
      --log-format LogFormat   The log format, either json or plain. (default plain)
      --log-level LogLevel     The log level, one of debug, info, warning, error or fatal. (default info)
      --no-color               Disables colorization of the output.
  -q, --quiet                  Suppress all non-error logging to stdout.

Use "dbt invocation [command] --help" for more information about a command.

Active Invocations:
  ID                             6dcf4723-e057-48b5-946f-a4d87e1d117a
  Status                         running
  Type                           cli
  Args                           [run --select test.sql]
  Started At                     2025-01-24 11:03:19

➜  jaffle-shop git:(test-cli) ✗

dbt ls
     [--resource-type {model,semantic_model,source,seed,snapshot,metric,test,exposure,analysis,function,default,all}]
     [--select SELECTION_ARG [SELECTION_ARG ...]]
     [--models SELECTOR [SELECTOR ...]]
     [--exclude SELECTOR [SELECTOR ...]]
     [--selector YML_SELECTOR_NAME]
     [--output {json,name,path,selector}]
     [--output-keys KEY_NAME [KEY_NAME]]

dbt ls --select snowplow.*
snowplow.snowplow_base_events
snowplow.snowplow_base_web_page_context
snowplow.snowplow_id_map
snowplow.snowplow_page_views
snowplow.snowplow_sessions
...

dbt ls --select tag:nightly --resource-type test
my_project.schema_test.not_null_orders_order_id
my_project.schema_test.unique_orders_order_id
my_project.schema_test.not_null_products_product_id
my_project.schema_test.unique_products_product_id
...

dbt ls --select config.materialized:incremental,test_type:schema
model.my_project.logs_parsed
model.my_project.events_categorized

dbt ls --select snowplow.* --output json
{"name": "snowplow_events", "resource_type": "model", "package_name": "snowplow",  ...}
{"name": "snowplow_page_views", "resource_type": "model", "package_name": "snowplow",  ...}
...

dbt ls --select snowplow.* --output json --output-keys "name resource_type description"
{"name": "snowplow_events", "description": "This is a pretty cool model",  ...}
{"name": "snowplow_page_views", "description": "This model is even cooler",  ...}
...

dbt ls -s +semantic_model:orders

dbt ls --select snowplow.* --output path
models/base/snowplow_base_events.sql
models/base/snowplow_base_web_page_context.sql
models/identification/snowplow_id_map.sql
...

dbt list --select "resource_type:function" # or dbt ls --resource-type function
jaffle_shop.area_of_circle
jaffle_shop.whoami

$ dbt parse
13:02:52  Running with dbt=1.5.0
13:02:53  Performance info: target/perf_info.json

{
    "path_count": 7,
    "is_partial_parse_enabled": false,
    "parse_project_elapsed": 0.20151838900000008,
    "patch_sources_elapsed": 0.00039490800000008264,
    "process_manifest_elapsed": 0.029363873999999957,
    "load_all_elapsed": 0.240095269,
    "projects": [
        {
            "project_name": "my_project",
            "elapsed": 0.07518750299999999,
            "parsers": [
                {
                    "parser": "model",
                    "elapsed": 0.04545303199999995,
                    "path_count": 1
                },
                {
                    "parser": "operation",
                    "elapsed": 0.0006415469999998535,
                    "path_count": 1
                },
                {
                    "parser": "seed",
                    "elapsed": 0.026538173000000054,
                    "path_count": 2
                }
            ],
            "path_count": 4
        },
        {
            "project_name": "dbt_postgres",
            "elapsed": 0.0016448299999998195,
            "parsers": [
                {
                    "parser": "operation",
                    "elapsed": 0.00021672399999994596,
                    "path_count": 1
                }
            ],
            "path_count": 1
        },
        {
            "project_name": "dbt",
            "elapsed": 0.006580432000000025,
            "parsers": [
                {
                    "parser": "operation",
                    "elapsed": 0.0002488560000000195,
                    "path_count": 1
                },
                {
                    "parser": "docs",
                    "elapsed": 0.002500640000000054,
                    "path_count": 1
                }
            ],
            "path_count": 2
        }
    ]
}

Running with dbt=1.6.1
Registered adapter: duckdb=1.6.0
Found 5 models, 3 seeds, 20 tests, 0 sources, 0 exposures, 0 metrics, 348 macros, 0 groups, 0 semantic models
 
Nothing to do. Try checking your model configs and model specification args

Running with dbt=1.6.1
Registered adapter: duckdb=1.6.0
Found 5 models, 3 seeds, 20 tests, 0 sources, 0 exposures, 0 metrics, 348 macros, 0 groups, 0 semantic models

Concurrency: 24 threads (target='dev')
 
1 of 5 START sql view model main.stg_customers ................................. [RUN]
2 of 5 START sql view model main.stg_orders .................................... [RUN]
3 of 5 START sql view model main.stg_payments .................................. [RUN]
1 of 5 OK created sql view model main.stg_customers ............................ [OK in 0.06s]
2 of 5 OK created sql view model main.stg_orders ............................... [OK in 0.06s]
3 of 5 OK created sql view model main.stg_payments ............................. [OK in 0.07s]
4 of 5 START sql table model main.customers .................................... [RUN]
5 of 5 START sql table model main.orders ....................................... [RUN]
4 of 5 ERROR creating sql table model main.customers ........................... [ERROR in 0.03s]
5 of 5 OK created sql table model main.orders .................................. [OK in 0.04s]
 
Finished running 3 view models, 2 table models in 0 hours 0 minutes and 0.15 seconds (0.15s).
  
Completed with 1 error and 0 warnings:
  
Runtime Error in model customers (models/customers.sql)
 Parser Error: syntax error at or near "selct"

Done. PASS=4 WARN=0 ERROR=1 SKIP=0 TOTAL=5

Running with dbt=1.6.1
Registered adapter: duckdb=1.6.0
Found 5 models, 3 seeds, 20 tests, 0 sources, 0 exposures, 0 metrics, 348 macros, 0 groups, 0 semantic models

Concurrency: 24 threads (target='dev')

1 of 1 START sql table model main.customers .................................... [RUN]
1 of 1 ERROR creating sql table model main.customers ........................... [ERROR in 0.03s]

Done. PASS=4 WARN=0 ERROR=1 SKIP=0 TOTAL=5

Running with dbt=1.6.1
Registered adapter: duckdb=1.6.0
Found 5 models, 3 seeds, 20 tests, 0 sources, 0 exposures, 0 metrics, 348 macros, 0 groups, 0 semantic models
 
Concurrency: 24 threads (target='dev')

1 of 1 START sql table model main.customers .................................... [RUN]
1 of 1 OK created sql table model main.customers ............................... [OK in 0.05s]

Finished running 1 table model in 0 hours 0 minutes and 0.09 seconds (0.09s).
 
Completed successfully
  
Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1

$ dbt-rpc serve
Running with dbt=1.5.0

16:34:31 | Concurrency: 8 threads (target='dev')
16:34:31 |
16:34:31 | Done.
Serving RPC server at 0.0.0.0:8580
Send requests to http://localhost:8580/jsonrpc

{
    "jsonrpc": "2.0",
    "method": "{ a valid rpc server command }",
    "id": "{ a unique identifier for this query }",
    "params": {
        "timeout": { timeout for the query in seconds, optional },
    }
}

{
    "jsonrpc": "2.0",
    "method": "status",
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d"
}

{
    "result": {
        "status": "ready",
        "error": null,
        "logs": [..],
        "timestamp": "2019-10-07T16:30:09.875534Z",
        "pid": 76715
    },
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "jsonrpc": "2.0"
}

{
    "jsonrpc": "2.0",
    "method": "poll",
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "params": {
        "request_token": "f86926fa-6535-4891-8d24-2cfc65d2a347",
        "logs": true,
        "logs_start": 0
    }
}

{
    "result": {
        "results": [],
        "generated_at": "2019-10-11T18:25:22.477203Z",
        "elapsed_time": 0.8381369113922119,
        "logs": [],
        "tags": {
            "command": "run --select my_model",
            "branch": "abc123"
        },
        "status": "success"
    },
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "jsonrpc": "2.0"
}

{
    "jsonrpc": "2.0",
    "method": "ps",
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "params": {
        "completed": true
    }
}

{
    "result": {
        "rows": [
            {
                "task_id": "561d4a02-18a9-40d1-9f01-cd875c3ec56d",
                "request_id": "3db9a2fe-9a39-41ef-828c-25e04dd6b07d",
                "request_source": "127.0.0.1",
                "method": "run",
                "state": "success",
                "start": "2019-10-07T17:09:49.865976Z",
                "end": null,
                "elapsed": 1.107261,
                "timeout": null,
                "tags": {
                    "command": "run --select my_model",
                    "branch": "feature/add-models"
                }
            }
        ]
    },
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "jsonrpc": "2.0"
}

{
    "jsonrpc": "2.0",
    "method": "kill",
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "params": {
        "task_id": "{ the task id to terminate }"
    }
}

{
    "jsonrpc": "2.0",
    "method": "cli_args",
    "id": "<request id>",
    "params": {
        "cli": "run --select abc+ --exclude +def",
        "task_tags": {
            "branch": "feature/my-branch",
            "commit": "c0ff33b01"
        }
    }
}

{
	"jsonrpc": "2.0",
	"method": "compile",
	"id": "<request id>",
	"params": {
            "threads": "<int> (optional)",
            "select": "<str> (optional)",
            "exclude": "<str> (optional)",
            "selector": "<str> (optional)",
            "state": "<str> (optional)"
        }
}

{
	"jsonrpc": "2.0",
	"method": "run",
	"id": "<request id>",
	"params": {
            "threads": "<int> (optional)",
            "select": "<str> (optional)",
            "exclude": "<str> (optional)",
            "selector": "<str> (optional)",
            "state": "<str> (optional)",
            "defer": "<bool> (optional)"
        }
}

{
	"jsonrpc": "2.0",
	"method": "test",
	"id": "<request id>",
	"params": {
            "threads": "<int> (optional)",
            "select": "<str> (optional)",
            "exclude": "<str> (optional)",
            "selector": "<str> (optional)",
            "state": "<str> (optional)",
            "data": "<bool> (optional)",
            "schema": "<bool> (optional)"
        }
}

{
	"jsonrpc": "2.0",
	"method": "seed",
	"id": "<request id>",
	"params": {
            "threads": "<int> (optional)",
            "select": "<str> (optional)",
            "exclude": "<str> (optional)",
            "selector": "<str> (optional)",
            "show": "<bool> (optional)",
            "state": "<str> (optional)"
        }
}

{
	"jsonrpc": "2.0",
	"method": "snapshot",
	"id": "<request id>",
	"params": {
            "threads": "<int> (optional)",
            "select": "<str> (optional)",
            "exclude": "<str> (optional)",
            "selector": "<str> (optional)",
            "state": "<str> (optional)"
        }
}

{
	"jsonrpc": "2.0",
	"method": "build",
	"id": "<request id>",
	"params": {
            "threads": "<int> (optional)",
            "select": "<str> (optional)",
            "exclude": "<str> (optional)",
            "selector": "<str> (optional)",
            "state": "<str> (optional)",
            "defer": "<str> (optional)"
        }
}

{
	"jsonrpc": "2.0",
	"method": "ls",
	"id": "<request id>",
	"params": {
        "select": "<str> (optional)",
        "exclude": "<str> (optional)",
        "selector": "<str> (optional)",
        "resource_types": ["<list> (optional)"],
        "output_keys": ["<list> (optional)"],
    }
}

{
	"jsonrpc": "2.0",
	"method": "docs.generate",
	"id": "<request id>",
	"params": {
            "compile": "<bool> (optional)",
            "state": "<str> (optional)"
        }
}

{
    "jsonrpc": "2.0",
    "method": "compile_sql",
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "params": {
        "timeout": 60,
        "sql": "c2VsZWN0IHt7IDEgKyAxIH19IGFzIGlk",
        "name": "my_first_query"
    }
}

{
    "jsonrpc": "2.0",
    "method": "run_sql",
    "id": "2db9a2fe-9a39-41ef-828c-25e04dd6b07d",
    "params": {
        "timeout": 60,
        "sql": "c2VsZWN0IHt7IDEgKyAxIH19IGFzIGlk",
        "name": "my_first_query"
    }
}

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt docs commands

`dbt docs` has two supported subcommands: `generate` and `serve`.

##### dbt docs generate[​](#dbt-docs-generate "Direct link to dbt docs generate")

The command is responsible for generating your project's documentation website by

1. Copying the website `index.html` file into the `target/` directory.
2. Compiling the resources in your project, so that their `compiled_code` will be included in [`manifest.json`](https://docs.getdbt.com/reference/artifacts/manifest-json.md).
3. Running queries against database metadata to produce the [`catalog.json`](https://docs.getdbt.com/reference/artifacts/catalog-json.md) file, which contains metadata about the tables and views produced by the models in your project.

**Example**:
```

Example 2 (unknown):
```unknown
Use the `--select` argument to limit the nodes included within `catalog.json`. When this flag is provided, step (3) will be restricted to the selected nodes. All other nodes will be excluded. Step (2) is unaffected.

**Example**:
```

Example 3 (unknown):
```unknown
Use the `--no-compile` argument to skip re-compilation. When this flag is provided, `dbt docs generate` will skip step (2) described above.

**Example**:
```

Example 4 (unknown):
```unknown
Use the `--empty-catalog` argument to skip running the database queries to populate `catalog.json`. When this flag is provided, `dbt docs generate` will skip step (3) described above.

This is not recommended for production environments, as it means that your documentation will be missing information gleaned from database metadata (the full set of columns in each table, and statistics about those tables). It can speed up `docs generate` in development, when you just want to visualize lineage and other information defined within your project. To learn how to build your documentation in dbt, refer to [build your docs in dbt](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md).

**Example**:
```

---

## use a 'decorator' for more readable code

**URL:** llms-txt#use-a-'decorator'-for-more-readable-code

**Contents:**
  - Ratio metrics
  - Release tracks in dbt platform
  - Retry your dbt jobs
  - Run visibility
  - Saved queries
  - Semantic models
  - Set up automatic exposures in Tableau EnterpriseEnterprise +
  - Set up automatic exposures in Tableau [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up local MCP
  - Set up remote MCP

@F.udf(returnType=T.DoubleType())
def add_random(x):
    random_number = numpy.random.normal()
    return x + random_number

def model(dbt, session):
    dbt.config(
        materialized = "table",
        packages = ["numpy"]
    )

temps_df = dbt.ref("temperatures")

# warm things up, who knows by how much
    df = temps_df.withColumn("degree_plus_random", add_random("degree"))
    return df

def model(dbt, session):
      dbt.config(
          materialized = "table"
      )

df = dbt.ref("my_source_table").df()

# One option for debugging: write messages to temporary table column
      # Pros: visibility
      # Cons: won't work if table isn't building for some reason
      msg = "something"
      df["debugging"] = f"My debug message here: {msg}"

return df
  
metrics:
  - name: The metric name # Required
    description: the metric description # Optional
    type: ratio # Required
    label: String that defines the display value in downstream tools. (such as orders_total or "orders_total") #Required
    type_params: # Required
      numerator: The name of the metric used for the numerator, or structure of properties # Required
        name: Name of metric used for the numerator # Required
        filter: Filter for the numerator # Optional
        alias: Alias for the numerator # Optional
      denominator: The name of the metric used for the denominator, or structure of properties # Required
        name: Name of metric used for the denominator # Required
        filter: Filter for the denominator # Optional
        alias: Alias for the denominator # Optional

metrics:
  - name: food_order_pct
    description: "The food order count as a ratio of the total order count"
    label: Food order ratio
    type: ratio
    type_params: 
      numerator: food_orders
      denominator: orders

metrics:
  - name: food_order_pct
    description: "The food order count as a ratio of the total order count, filtered by location"
    label: Food order ratio by location
    type: ratio
    type_params:
      numerator:
        name: food_orders
        filter: location = 'New York'
        alias: ny_food_orders
      denominator:
        name: orders
        filter: location = 'New York'
        alias: ny_orders

select
  subq_15577.metric_time as metric_time,
  cast(subq_15577.mql_queries_created_test as double) / cast(nullif(subq_15582.distinct_query_users, 0) as double) as mql_queries_per_active_user
from (
  select
    metric_time,
    sum(mql_queries_created_test) as mql_queries_created_test
  from (
    select
      cast(query_created_at as date) as metric_time,
      case when query_status in ('PENDING','MODE') then 1 else 0 end as mql_queries_created_test
    from prod_dbt.mql_query_base mql_queries_test_src_2552 
  ) subq_15576
  group by
    metric_time
) subq_15577
inner join (
  select
    metric_time,
    count(distinct distinct_query_users) as distinct_query_users
  from (
    select
      cast(query_created_at as date) as metric_time,
      case when query_status in ('MODE','PENDING') then email else null end as distinct_query_users
    from prod_dbt.mql_query_base mql_queries_src_2585 
  ) subq_15581
  group by
    metric_time
) subq_15582
on
  (
    (
      subq_15577.metric_time = subq_15582.metric_time
    ) or (
      (
        subq_15577.metric_time is null
      ) and (
        subq_15582.metric_time is null
      )
    )
  )

metrics:
  - name: frequent_purchaser_ratio
    description: Fraction of active users who qualify as frequent purchasers
    type: ratio
    type_params:
      numerator:
        name: distinct_purchasers
        filter: |
          {{Dimension('customer__is_frequent_purchaser')}}
        alias: frequent_purchasers
      denominator:
        name: distinct_purchasers

filter: | 
  {{ Entity('entity_name') }}

filter: |  
  {{ Dimension('primary_entity__dimension_name') }}

filter: |  
  {{ TimeDimension('time_dimension', 'granularity') }}

filter: |  
  {{ Metric('metric_name', group_by=['entity_name']) }}

saved-queries:
  my_saved_query:
    +cache:
      enabled: true

semantic_models:
  - name: the_name_of_the_semantic_model ## Required
    description: same as always ## Optional
    model: ref('some_model') ## Required
    defaults: ## Required
      agg_time_dimension: dimension_name ## Required if the model contains measures
    entities: ## Required
      - see more information in entities
    measures: ## Optional
      - see more information in the measures section
    dimensions: ## Required
      - see more information in the dimensions section
    primary_entity: >-
      if the semantic model has no primary entity, then this property is required. #Optional if a primary entity exists, otherwise Required

semantic_models:
  - name: transaction # A semantic model with the name Transactions
    model: ref('fact_transactions') # References the dbt model named `fact_transactions`
    description: "Transaction fact table at the transaction level. This table contains one row per transaction and includes the transaction timestamp."
    defaults:
      agg_time_dimension: transaction_date

entities: # Entities included in the table are defined here. MetricFlow will use these columns as join keys.
      - name: transaction
        type: primary
        expr: transaction_id
      - name: customer
        type: foreign
        expr: customer_id

dimensions: # dimensions are qualitative values such as names, dates, or geographical data. They provide context to metrics and allow "metric by group" data slicing.
      - name: transaction_date
        type: time
        type_params:
          time_granularity: day

- name: transaction_location
        type: categorical
        expr: order_country

measures: # Measures are columns we perform an aggregation over. Measures are inputs to metrics.
      - name: transaction_total
        description: "The total value of the transaction."
        agg: sum

- name: sales
        description: "The total sale of the transaction."
        agg: sum
        expr: transaction_total

- name: median_sales
        description: "The median sale of the transaction."
        agg: median
        expr: transaction_total

- name: customers # Another semantic model called customers.
    model: ref('dim_customers')
    description: "A customer dimension table."

entities:
      - name: customer
        type: primary
        expr: customer_id

dimensions:
      - name: first_name
        type: categorical

semantic_models:
    - name: orders
      config:
        enabled: true | false
        group: some_group
        meta:
          some_key: some_value
  
  semantic-models:
    my_project_name:
      +enabled: true | false
      +group: some_group
      +meta:
        some_key: some_value
  
semantic_model:
  name: bookings_monthly_source
  description: bookings_monthly_source
  defaults:
    agg_time_dimension: ds
  model: ref('bookings_monthly_source')
  measures:
    - name: bookings_monthly
      agg: sum
      create_metric: true
  primary_entity: booking_id

entity:
  - name: transaction
    type: primary
  - name: order
    type: foreign
    expr: id_order
  - name: user
    type: foreign
    expr: substring(id_order FROM 2)

query {
           workbooks {
             name
             uri
             id
             luid
             projectLuid
             projectName
             upstreamTables {
               id
               name
               schema
               database {
                 name
                 connectionType
             }
           }
         }
       }
     
   DBT_HOST=cloud.getdbt.com
   DBT_PROD_ENV_ID=your-production-environment-id
   DBT_DEV_ENV_ID=your-development-environment-id
   DBT_USER_ID=your-user-id
   DBT_ACCOUNT_ID=your-account-id
   DBT_TOKEN=your-service-token
   DBT_PROJECT_DIR=/path/to/your/dbt/project
   DBT_PATH=/path/to/your/dbt/executable
   MULTICELL_ACCOUNT_PREFIX=your-account-prefix
   
   uvx --env-file <path-to-.env-file> dbt-mcp
   
   {
     "mcpServers": {
       "dbt-mcp": {
         "command": "uvx",
         "args": [
           "--env-file",
           "<path-to-.env-file>",
           "dbt-mcp"
         ]
       }
     }
   }
   
{
  "mcpServers": {
    "dbt": {
      "command": "uvx",
      "args": [
        "dbt-mcp"
      ],
      "env": {
        "DBT_HOST": "https://<your-dbt-host-with-custom-subdomain>",
        "DBT_PROJECT_DIR": "/path/to/project",
        "DBT_PATH": "path/to/dbt/executable"
      }
    }
  }
}

{
  "mcpServers": {
    "dbt": {
      "command": "uvx",
      "args": [
        "dbt-mcp"
      ],
      "env": {
        "DBT_HOST": "https://<your-dbt-host-with-custom-subdomain>",
        "DISABLE_DBT_CLI": "true"
      }
    }
  }
}

{
  "mcpServers": {
    "dbt": {
      "url": "https://<host>/api/ai/v1/mcp/",
      "headers": {
       "Authorization": "token <token>",
        "x-dbt-prod-environment-id": "<prod-id>",
        "x-dbt-user-id": "<user-id>",
        "x-dbt-dev-environment-id": "<dev-id>"
      }
    }
  }
}

create role cortex_user_role;
   grant database role SNOWFLAKE.CORTEX_USER to role cortex_user_role;
   grant role cortex_user_role to user SL_USER;
   grant role cortex_user_role to user DEPLOYMENT_USER;
   
models:
  - name: dim_wizards
    config:
      freshness: 
        build_after:
          count: 4         # how long to wait before rebuilding
          period: hour     # unit of time
          updates_on: all  # only rebuild if all upstream dependencies have new data
  - name: dim_worlds
    config:
      freshness:
        build_after:
          count: 4
          period: hour
          updates_on: all

models:
  <resource-path>:
    +freshness:
      build_after: 
        count: 4
        period: hour
        updates_on: all

{{
    config(
        freshness={
            "build_after": {
                "count": 4,
                "period": "hour",
                "updates_on": "all"
            }
        }
    )
}}

models:
  +freshness:
    build_after:
      count: 4
      period: hour
  jaffle_shop: # this needs to match your project `name:` in dbt_project.yml
    staging:
      +materialized: view
    marts:
      +materialized: table

models:
  +freshness:
    build_after:
      count: 4
      period: hour
  marts: # only applies to models inside the marts folder
    +freshness:
      build_after:
        count: 1
        period: hour

freshness:
      build_after:
        count: 1
        period: hour
        updates_on: any

metrics:
  - name: The metric name # Required
    description: the metric description # Optional
    type: simple # Required
    label: The value that will be displayed in downstream tools # Required
    type_params: # Required
      measure: 
        name: The name of your measure # Required
        alias: The alias applied to the measure. # Optional
        filter: The filter applied to the measure. # Optional
        fill_nulls_with: Set value instead of null  (such as zero) # Optional
        join_to_timespine: true/false # Boolean that indicates if the aggregated measure should be joined to the time spine table to fill in missing dates. # Optional

metrics: 
    - name: customers
      description: Count of customers
      type: simple # Pointers to a measure you created in a semantic model
      label: Count of customers
      type_params:
        measure: 
          name: customers # The measure you are creating a proxy of.
          fill_nulls_with: 0 
          join_to_timespine: true
          alias: customer_count
          filter: {{ Dimension('customer__customer_total') }} >= 20
    - name: large_orders
      description: "Order with order values over 20."
      type: simple
      label: Large orders
      type_params:
        measure: 
          name: orders
      filter: | # For any metric you can optionally include a filter on dimension values
        {{Dimension('customer__order_total_dim')}} >= 20

CREATE CATALOG INTEGRATION my_polaris_catalog_int 
  CATALOG_SOURCE = POLARIS 
  TABLE_FORMAT = ICEBERG 
  REST_CONFIG = (
    CATALOG_URI = 'https://<org>-<account>.snowflakecomputing.com/polaris/api/catalog' 
    CATALOG_NAME = '<open_catalog_name>' 
  ) 
  REST_AUTHENTICATION = (
    TYPE = OAUTH 
    OAUTH_CLIENT_ID = '<client_id>' 
    OAUTH_CLIENT_SECRET = '<client_secret>' 
    OAUTH_ALLOWED_SCOPES = ('PRINCIPAL_ROLE:ALL') 
  ) 
  ENABLED = TRUE;

CREATE CATALOG INTEGRATION my_glue_catalog_int
  CATALOG_SOURCE = GLUE
  CATALOG_NAMESPACE = 'dbt_database' 
  TABLE_FORMAT = ICEBERG
  GLUE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/myGlueRole'
  GLUE_CATALOG_ID = '123456789012'
  GLUE_REGION = 'us-east-2'
  ENABLED = TRUE;

CREATE CATALOG INTEGRATION my_iceberg_catalog_int
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'dbt_database'
  REST_CONFIG = (
    restConfigParams
  )
  REST_AUTHENTICATION = (
    restAuthenticationParams
  )
  ENABLED = TRUE
  REFRESH_INTERVAL_SECONDS = <value> 
  COMMENT = 'catalog integration for dbt iceberg tables'

CREATE OR REPLACE CATALOG INTEGRATION my_unity_catalog_int_pat
  CATALOG_SOURCE = ICEBERG_REST
  TABLE_FORMAT = ICEBERG
  CATALOG_NAMESPACE = 'my_namespace'
  REST_CONFIG = (
    CATALOG_URI = 'https://my-api/api/2.1/unity-catalog/iceberg'
    CATALOG_NAME= '<catalog_name>'
  )
  REST_AUTHENTICATION = (
    TYPE = BEARER
    BEARER_TOKEN = '<bearer_token>'
  )
  ENABLED = TRUE;

catalogs:
  - name: catalog_horizon
    active_write_integration: snowflake_write_integration
    write_integrations:
      - name: snowflake_write_integration
        external_volume: dbt_external_volume
        table_format: iceberg
        catalog_type: built_in
        adapter_properties:
          change_tracking: True

{{
    config(
        materialized='table',
        catalog_name = 'catalog_horizon'

select * from {{ ref('jaffle_shop_customers') }}

with customer_orders as (
    select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

from jaffle_shop.orders

select
    customers.customer_id,
    customers.first_name,
    customers.last_name,
    customer_orders.first_order_date,
    customer_orders.most_recent_order_date,
    coalesce(customer_orders.number_of_orders, 0) as number_of_orders

from jaffle_shop.customers

left join customer_orders using (customer_id)

create view dbt_alice.customers as (
    with customer_orders as (
        select
            customer_id,
            min(order_date) as first_order_date,
            max(order_date) as most_recent_order_date,
            count(order_id) as number_of_orders

from jaffle_shop.orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

from jaffle_shop.customers

left join customer_orders using (customer_id)
)

$ dbt run --select customers
Running with dbt=1.9.0
Found 3 models, 9 tests, 0 snapshots, 0 analyses, 133 macros, 0 operations, 0 seed files, 0 sources

14:04:12 | Concurrency: 1 threads (target='dev')
14:04:12 |
14:04:12 | 1 of 1 START view model dbt_alice.customers.......................... [RUN]
14:04:13 | 1 of 1 ERROR creating view model dbt_alice.customers................. [ERROR in 0.81s]
14:04:13 |
14:04:13 | Finished running 1 view model in 1.68s.

Completed with 1 error and 0 warnings:

Database Error in model customers (models/customers.sql)
  Syntax error: Expected ")" but got identifier `your-info-12345` at [13:15]
  compiled SQL at target/run/jaffle_shop/customers.sql

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

select 1 as my_column

-- you can't create or replace on redshift, so use a transaction to do this in an atomic way

create table "dbt_alice"."test_model__dbt_tmp" as (
    select 1 as my_column
);

alter table "dbt_alice"."test_model" rename to "test_model__dbt_backup";

alter table "dbt_alice"."test_model__dbt_tmp" rename to "test_model"

drop table if exists "dbt_alice"."test_model__dbt_backup" cascade;

-- Make an API call to create a dataset (no DDL interface for this)!!;

create or replace table `dbt-dev-87681`.`dbt_alice`.`test_model` as (
  select 1 as my_column
);

create schema if not exists analytics.dbt_alice;

create or replace table analytics.dbt_alice.test_model as (
    select 1 as my_column
);

models
├── staging
└── marts
    └── marketing

name: jaffle_shop
config-version: 2
...

models:
  jaffle_shop: # this matches the `name:`` config
    +materialized: view # this applies to all models in the current project
    marts:
      +materialized: table # this applies to all models in the `marts/` directory
      marketing:
        +schema: marketing # this applies to all models in the `marts/marketing/`` directory

{{ config(
    materialized="view",
    schema="marketing"
) }}

with customer_orders as ...

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

create view dbt_alice.customers as (
  with customers as (

select * from dbt_alice.stg_customers

select * from dbt_alice.stg_orders

create view analytics.customers as (
  with customers as (

select * from analytics.stg_customers

select * from analytics.stg_orders

model-paths: ["transformations"]

name: jaffle_shop
...

models:
  jaffle_shop:
    marketing:
      schema: marketing # seeds in the `models/mapping/ subdirectory will use the marketing schema

{{
  config(
    schema='core'
  )
}}

select
    id,
    created::timestamp as created
from some_other_table

create table dbt_alice.my_table
  id integer,
  created timestamp;

insert into dbt_alice.my_table (
  select id, created from some_other_table
)

create table dbt_alice.my_table as (
  select id, created from some_other_table
)

select * from {{ ref('stg_customers') }}

accepted_email_domains as (

select * from {{ ref('top_level_email_domains') }}

),
	
check_valid_emails as (

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customers.email,
	      coalesce (regexp_like(
            customers.email, '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'
        )
        = true
        and accepted_email_domains.tld is not null,
        false) as is_valid_email_address
    from customers
		left join accepted_email_domains
        on customers.email_top_level_domain = lower(accepted_email_domains.tld)

select * from check_valid_emails

unit_tests:
  - name: test_is_valid_email_address
    description: "Check my is_valid_email_address logic captures all known edge cases - emails without ., emails without @, and emails from invalid domains."
    model: dim_customers
    given:
      - input: ref('stg_customers')
        rows:
          - {email: cool@example.com,    email_top_level_domain: example.com}
          - {email: cool@unknown.com,    email_top_level_domain: unknown.com}
          - {email: badgmail.com,        email_top_level_domain: gmail.com}
          - {email: missingdot@gmailcom, email_top_level_domain: gmail.com}
      - input: ref('top_level_email_domains')
        rows:
          - {tld: example.com}
          - {tld: gmail.com}
    expect:
      rows:
        - {email: cool@example.com,    is_valid_email_address: true}
        - {email: cool@unknown.com,    is_valid_email_address: false}
        - {email: badgmail.com,        is_valid_email_address: false}
        - {email: missingdot@gmailcom, is_valid_email_address: false}

dbt run --select "stg_customers top_level_email_domains" --empty

dbt test --select test_is_valid_email_address
16:03:49  Running with dbt=1.8.0-a1
16:03:49  Registered adapter: postgres=1.8.0-a1
16:03:50  Found 6 models, 5 seeds, 4 data tests, 0 sources, 0 exposures, 0 metrics, 410 macros, 0 groups, 0 semantic models, 1 unit test
16:03:50  
16:03:50  Concurrency: 5 threads (target='postgres')
16:03:50  
16:03:50  1 of 1 START unit_test dim_customers::test_is_valid_email_address ................... [RUN]
16:03:51  1 of 1 FAIL 1 dim_customers::test_is_valid_email_address ............................ [FAIL 1 in 0.26s]
16:03:51  
16:03:51  Finished running 1 unit_test in 0 hours 0 minutes and 0.67 seconds (0.67s).
16:03:51  
16:03:51  Completed with 1 error and 0 warnings:
16:03:51  
16:03:51  Failure in unit_test test_is_valid_email_address (models/marts/unit_tests.yml)
16:03:51

actual differs from expected:

@@ ,email           ,is_valid_email_address
→  ,cool@example.com,True→False
   ,cool@unknown.com,False
...,...             ,...

16:03:51  
16:03:51    compiled Code at models/marts/unit_tests.yml
16:03:51  
16:03:51  Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

dbt test --select test_is_valid_email_address
16:09:11  Running with dbt=1.8.0-a1
16:09:12  Registered adapter: postgres=1.8.0-a1
16:09:12  Found 6 models, 5 seeds, 4 data tests, 0 sources, 0 exposures, 0 metrics, 410 macros, 0 groups, 0 semantic models, 1 unit test
16:09:12  
16:09:13  Concurrency: 5 threads (target='postgres')
16:09:13  
16:09:13  1 of 1 START unit_test dim_customers::test_is_valid_email_address ................... [RUN]
16:09:13  1 of 1 PASS dim_customers::test_is_valid_email_address .............................. [PASS in 0.26s]
16:09:13  
16:09:13  Finished running 1 unit_test in 0 hours 0 minutes and 0.75 seconds (0.75s).
16:09:13  
16:09:13  Completed successfully
16:09:13  
16:09:13  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1

dbt run --select "config.materialized:incremental" --empty

{{
    config(
        materialized='incremental'
    )
}}

select * from {{ ref('events') }}
{% if is_incremental() %}
where event_time > (select max(event_time) from {{ this }})
{% endif %}

unit_tests:
  - name: my_incremental_model_full_refresh_mode
    model: my_incremental_model
    overrides:
      macros:
        # unit test this model in "full refresh" mode
        is_incremental: false 
    given:
      - input: ref('events')
        rows:
          - {event_id: 1, event_time: 2020-01-01}
    expect:
      rows:
        - {event_id: 1, event_time: 2020-01-01}

- name: my_incremental_model_incremental_mode
    model: my_incremental_model
    overrides:
      macros:
        # unit test this model in "incremental" mode
        is_incremental: true 
    given:
      - input: ref('events')
        rows:
          - {event_id: 1, event_time: 2020-01-01}
          - {event_id: 2, event_time: 2020-01-02}
          - {event_id: 3, event_time: 2020-01-03}
      - input: this 
        # contents of current my_incremental_model
        rows:
          - {event_id: 1, event_time: 2020-01-01}
    expect:
      # what will be inserted/merged into my_incremental_model
      rows:
        - {event_id: 2, event_time: 2020-01-02}
        - {event_id: 3, event_time: 2020-01-03}

unit_tests:
  - name: my_unit_test
    model: dim_customers
    given:
      - input: ref('ephemeral_model')
        format: sql
        rows: |
          select 1 as id, 'emily' as name
    expect:
      rows:
        - {id: 1, first_name: emily}

#dbt_project.yml
vars:
  surrogate_key_treat_nulls_as_empty_strings: true #turn on legacy behavior

models:
  - name: old_syntax
    tests:
      - dbt_utils.expression_is_true:
          expression: "col_a + col_b = total"
          #replace this...
          condition: "created_at > '2018-12-31'"

- name: new_syntax
    tests:
      - dbt_utils.expression_is_true:
          expression: "col_a + col_b = total"
          # ...with this...
          where: "created_at > '2018-12-31'"

packages:
  - git: https://github.com/dbt-labs/dbt-labs-experimental-features
    subdirectory: insert_by_period
    revision: XXXX #optional but highly recommended. Provide a full git sha hash, e.g. 1c0bfacc49551b2e67d8579cf8ed459d68546e00. If not provided, uses the current HEAD.

{% set relation = adapter.get_relation(
database=db_name,
schema=db_schema,
identifier='a')
%}
{{ print('relation: ' ~ relation) }}

{% set relation_via_api = api.Relation.create(
database=db_name,
schema=db_schema,
identifier='a'
) %}
{{ print('relation_via_api: ' ~ relation_via_api) }}

relation: None
relation_via_api: my_db.my_schema.my_table

relation: my_db.my_schema.my_table
relation_via_api: my_db.my_schema.my_table

error: dbt8999: Cannot combine non-exact versions: =0.8.3 and =1.1.1

select
  id as payment_id,
  # my_nonexistent_macro is a macro that DOES NOT EXIST
  {{ my_nonexistent_macro('amount') }} as amount_usd,
from app_data.payments

{{ adapter.does_not_exist() }}

models:
  - name: dim_wizards
    data_tests:
      - does_not_exist

select {{ var('does_not_exist') }} as my_column

dbt found two docs with the same name: 'docs_block_title in files: 'models/crm/_crm.md' and 'docs/crm/business_class_marketing.md'

animal,  
dog,  
cat,  
bear,

**Examples:**

Example 1 (unknown):
```unknown
###### Code reuse[​](#code-reuse "Direct link to Code reuse")

Currently, Python functions defined in one dbt model can't be imported and reused in other models. This is something dbt Labs would like to support, so there are two patterns we're considering:

* Creating and registering **"named" UDFs** — This process is different across data platforms and has some performance limitations. For example, Snowpark supports [vectorized UDFs](https://docs.snowflake.com/en/developer-guide/udf/python/udf-python-batch.html) for pandas-like functions that you can execute in parallel.
* **Private Python packages** — In addition to importing reusable functions from public PyPI packages, many data platforms support uploading custom Python assets and registering them as packages. The upload process looks different across platforms, but your code’s actual `import` looks the same.

❓ dbt questions

* Should dbt have a role in abstracting over UDFs? Should dbt support a new type of DAG node, `function`? Would the primary use case be code reuse across Python models or defining Python-language functions that can be called from SQL models?
* How can dbt help users when uploading or initializing private Python assets? Is this a new form of `dbt deps`?
* How can dbt support users who want to test custom functions? If defined as UDFs: "unit testing" in the database? If "pure" functions in packages: encourage adoption of `pytest`?

💬 Discussion: ["Python models: package, artifact/object storage, and UDF management in dbt"](https://github.com/dbt-labs/dbt-core/discussions/5741)

##### DataFrame API and syntax[​](#dataframe-api-and-syntax "Direct link to DataFrame API and syntax")

Over the past decade, most people writing [data transformations](https://www.getdbt.com/analytics-engineering/transformation/) in Python have adopted DataFrame as their common abstraction. dbt follows this convention by returning `ref()` and `source()` as DataFrames, and it expects all Python models to return a DataFrame.

A DataFrame is a two-dimensional data structure (rows and columns). It supports convenient methods for transforming that data and creating new columns from calculations performed on existing columns. It also offers convenient ways for previewing data while developing locally or in a notebook.

That's about where the agreement ends. There are numerous frameworks with their own syntaxes and APIs for DataFrames. The [pandas](https://pandas.pydata.org/docs/) library offered one of the original DataFrame APIs, and its syntax is the most common to learn for new data professionals. Most newer DataFrame APIs are compatible with pandas-style syntax, though few can offer perfect interoperability. This is true for BigQuery DataFrames, Snowpark, and PySpark, which have their own DataFrame APIs.

When developing a Python model, you will find yourself asking these questions:

**Why pandas?** — It's the most common API for DataFrames. It makes it easy to explore sampled data and develop transformations locally. You can “promote” your code as-is into dbt models and run it in production for small datasets.

**Why *not* pandas?** — Performance. pandas runs "single-node" transformations, which cannot benefit from the parallelism and distributed computing offered by modern data warehouses. This quickly becomes a problem as you operate on larger datasets. Some data platforms support optimizations for code written using pandas DataFrame API, preventing the need for major refactors. For example, [pandas on PySpark](https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_ps.html) offers support for 95% of pandas functionality, using the same API while still leveraging parallel processing.

❓ dbt questions

* When developing a new dbt Python model, should we recommend pandas-style syntax for rapid iteration and then refactor?
* Which open source libraries provide compelling abstractions across different data engines and vendor-specific APIs?
* Should dbt attempt to play a longer-term role in standardizing across them?

💬 Discussion: ["Python models: the pandas problem (and a possible solution)"](https://github.com/dbt-labs/dbt-core/discussions/5738)

#### Limitations[​](#limitations "Direct link to Limitations")

Python models have capabilities that SQL models do not. They also have some drawbacks compared to SQL models:

* **Time and cost.** Python models are slower to run than SQL models, and the cloud resources that run them can be more expensive. Running Python requires more general-purpose compute. That compute might sometimes live on a separate service or architecture from your SQL models. **However:** We believe that deploying Python models via dbt—with unified lineage, testing, and documentation—is, from a human standpoint, **dramatically** faster and cheaper. By comparison, spinning up separate infrastructure to orchestrate Python transformations in production and different tooling to integrate with dbt is much more time-consuming and expensive.

* **Syntax differences** are even more pronounced. Over the years, dbt has done a lot, via dispatch patterns and packages such as `dbt_utils`, to abstract over differences in SQL dialects across popular data warehouses. Python offers a **much** wider field of play. If there are five ways to do something in SQL, there are 500 ways to write it in Python, all with varying performance and adherence to standards. Those options can be overwhelming. As the maintainers of dbt, we will be learning from state-of-the-art projects tackling this problem and sharing guidance as we develop it.

* **These capabilities are very new.** As data warehouses develop new features, we expect them to offer cheaper, faster, and more intuitive mechanisms for deploying Python transformations. **We reserve the right to change the underlying implementation for executing Python models in future releases.** Our commitment to you is around the code in your model `.py` files, following the documented capabilities and guidance we're providing here.

* **Lack of `print()` support.** The data platform runs and compiles your Python model without dbt's oversight. This means it doesn't display the output of commands such as Python's built-in [`print()`](https://docs.python.org/3/library/functions.html#print) function in dbt's logs.

*  Alternatives to using print() in Python models

  The following explains other methods you can use for debugging, such as writing messages to a dataframe column:

  * Using platform logs: Use your data platform's logs to debug your Python models.
  * Return logs as a dataframe: Create a dataframe containing your logs and build it into the warehouse.
  * Develop locally with DuckDB: Test and debug your models locally using DuckDB before deploying them.

  Here's an example of debugging in a Python model:
```

Example 2 (unknown):
```unknown
As a general rule, if there's a transformation you could write equally well in SQL or Python, we believe that well-written SQL is preferable: it's more accessible to a greater number of colleagues, and it's easier to write code that's performant at scale. If there's a transformation you *can't* write in SQL, or where ten lines of elegant and well-annotated Python could save you 1000 lines of hard-to-read Jinja-SQL, Python is the way to go.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Ratio metrics

Ratio allows you to create a ratio between two metrics. You simply specify a numerator and a denominator metric. Additionally, you can apply a dimensional filter to both the numerator and denominator using a constraint string when computing the metric.

The parameters, description, and type for ratio metrics are:

| Parameter     | Description                                                                                                                         | Required | Type           |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------- |
| `name`        | The name of the metric.                                                                                                             | Required | String         |
| `description` | The description of the metric.                                                                                                      | Optional | String         |
| `type`        | The type of the metric (cumulative, derived, ratio, or simple).                                                                     | Required | String         |
| `label`       | Defines the display value in downstream tools. Accepts plain text, spaces, and quotes (such as `orders_total` or `"orders_total"`). | Required | String         |
| `type_params` | The type parameters of the metric.                                                                                                  | Required | Dict           |
| `numerator`   | The name of the metric used for the numerator, or structure of properties.                                                          | Required | String or dict |
| `denominator` | The name of the metric used for the denominator, or structure of properties.                                                        | Required | String or dict |
| `filter`      | Optional filter for the numerator or denominator.                                                                                   | Optional | String         |
| `alias`       | Optional alias for the numerator or denominator.                                                                                    | Optional | String         |

The following displays the complete specification for ratio metrics, along with an example.

models/metrics/file\_name.yml
```

Example 3 (unknown):
```unknown
For advanced data modeling, you can use `fill_nulls_with` and `join_to_timespine` to [set null metric values to zero](https://docs.getdbt.com/docs/build/fill-nulls-advanced.md), ensuring numeric values for every data row.

#### Ratio metrics example[​](#ratio-metrics-example "Direct link to Ratio metrics example")

These examples demonstrate how to create ratio metrics in your model. They cover basic and advanced use cases, including applying filters to the numerator and denominator metrics.

###### Example 1[​](#example-1 "Direct link to Example 1")

This example is a basic ratio metric that calculates the ratio of food orders to total orders:

models/metrics/file\_name.yml
```

Example 4 (unknown):
```unknown
###### Example 2[​](#example-2 "Direct link to Example 2")

This example is a ratio metric that calculates the ratio of food orders to total orders, with a filter and alias applied to the numerator. Note that in order to add these attributes, you'll need to use an explicit key for the name attribute too.

models/metrics/file\_name.yml
```

---

## autouse fixture below

**URL:** llms-txt#autouse-fixture-below

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "skip_profile(profile): skip test for the given profile",
    )

@pytest.fixture(scope="session")
def dbt_profile_target(request):
    profile_type = request.config.getoption("--profile")
    elif profile_type == "databricks_sql_endpoint":
        target = databricks_sql_endpoint_target()
    elif profile_type == "apache_spark":
        target = apache_spark_target()
    else:
        raise ValueError(f"Invalid profile type '{profile_type}'")
    return target

def apache_spark_target():
    return {
        "type": "spark",
        "host": "localhost",
        ...
    }

def databricks_sql_endpoint_target():
    return {
        "type": "spark",
        "host": os.getenv("DBT_DATABRICKS_HOST_NAME"),
        ...
    }

@pytest.fixture(autouse=True)
def skip_by_profile_type(request):
    profile_type = request.config.getoption("--profile")
    if request.node.get_closest_marker("skip_profile"):
        for skip_profile_type in request.node.get_closest_marker("skip_profile").args:
            if skip_profile_type == profile_type:
                pytest.skip("skipped on '{profile_type}' profile")

**Examples:**

Example 1 (unknown):
```unknown
If there are tests that *shouldn't* run for a given profile:

tests/functional/adapter/basic.py
```

---

## Refresh the workbook

**URL:** llms-txt#refresh-the-workbook

**Contents:**
  - Set up your dbt project with Databricks
  - Trigger PagerDuty alarms when dbt jobs fail
  - Use Databricks workflows to run dbt jobs

refresh_url = f"{server_url}/api/{api_version}/sites/{site_id}/workbooks/{workbook_id}/refresh"
refresh_data = {}
refresh_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Tableau-Auth": auth_token
}

refresh_trigger = requests.post(refresh_url, data=json.dumps(refresh_data), headers=refresh_headers)
return {"message": "Workbook refresh has been queued"}

create catalog if not exists dev;
create catalog if not exists prod;

#example: replace with your actual path
cd ~/Documents/GitHub/dbt-cloud-webhooks-pagerduty

flyctl secrets set DBT_CLOUD_SERVICE_TOKEN=abc123 DBT_CLOUD_AUTH_TOKEN=def456 PD_ROUTING_KEY=ghi789

**Examples:**

Example 1 (unknown):
```unknown
#### Test and deploy[​](#test-and-deploy "Direct link to Test and deploy")

To make changes to your code, you can modify it and test it again. When you're happy with it, you can publish your Zap.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Set up your dbt project with Databricks

[Back to guides](https://docs.getdbt.com/guides.md)

Databricks

dbt Core

dbt platform

Intermediate

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

Databricks and dbt Labs are partnering to help data teams think like software engineering teams and ship trusted data, faster. The dbt-databricks adapter enables dbt users to leverage the latest Databricks features in their dbt project. Hundreds of customers are now using dbt and Databricks to build expressive and reliable data pipelines on the Lakehouse, generating data assets that enable analytics, ML, and AI use cases throughout the business.

In this guide, we discuss how to set up your dbt project on the Databricks Lakehouse Platform so that it scales from a small team all the way up to a large organization.

#### Configuring the Databricks Environments[​](#configuring-the-databricks-environments "Direct link to Configuring the Databricks Environments")

To get started, we will use Databricks’s Unity Catalog. Without it, we would not be able to design separate [environments](https://docs.getdbt.com/docs/environments-in-dbt.md) for development and production per our [best practices](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview.md). It also allows us to ensure the proper access controls have been applied using SQL. You will need to be using the dbt-databricks adapter to use it (as opposed to the dbt-spark adapter).

We will set up two different *catalogs* in Unity Catalog: **dev** and **prod**. A catalog is a top-level container for *schemas* (previously known as databases in Databricks), which in turn contain tables and views.

Our dev catalog will be the development environment that analytics engineers interact with through their Studio IDE. Developers should have their own sandbox to build and test objects in without worry of overwriting or dropping a coworker’s work; we recommend creating personal schemas for this purpose. In terms of permissions, they should only have access to the **dev** catalog.

Only production runs will have access to data in the **prod** catalog. In a future guide, we will discuss a **test** catalog where our continuous integration/continuous deployment (CI/CD) system can run `dbt test`.

For now, let’s keep things simple and [create two catalogs](https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-catalog.html) either using the Data Catalog or in the SQL editor with these commands:
```

Example 2 (unknown):
```unknown
As long as your developer is given write access to the dev data catalog, there is no need to create the sandbox schemas ahead of time.

#### Setting up Service Principals[​](#setting-up-service-principals "Direct link to Setting up Service Principals")

When an analytics engineer runs a dbt project from their Studio IDE, it is perfectly fine for the resulting queries to execute with that user’s identity. However, we want production runs to execute with a *service principal's* identity. As a reminder, a service principal is a headless account that does not belong to an actual person.

Service principals are used to remove humans from deploying to production for convenience and security. Personal identities should not be used to build production pipelines because they could break if the user leaves the company or changes their credentials. Also, there should not be ad hoc commands modifying production data. Only scheduled jobs and running code that has passed CI tests and code reviews should be allowed to modify production data. If something breaks, there is an auditable trail of changes to find the root cause, easily revert to the last working version of the code, and minimize the impact on end users.

[Let’s create a service principal](https://docs.databricks.com/administration-guide/users-groups/service-principals.html#add-a-service-principal-to-your-databricks-account) in Databricks:

1. Have your Databricks Account admin [add a service principal](https://docs.databricks.com/administration-guide/users-groups/service-principals.html#add-a-service-principal-to-your-databricks-account) to your account. The service principal’s name should differentiate itself from a user ID and make its purpose clear (eg dbt\_prod\_sp).
2. Add the service principal added to any groups it needs to be a member of at this time. There are more details on permissions in our ["Unity Catalog best practices" guide](https://docs.getdbt.com/best-practices/dbt-unity-catalog-best-practices.md).
3. [Add the service principal to your workspace](https://docs.databricks.com/administration-guide/users-groups/service-principals.html#add-a-service-principal-to-a-workspace) and apply any [necessary entitlements](https://docs.databricks.com/administration-guide/users-groups/service-principals.html#add-a-service-principal-to-a-workspace-using-the-admin-console), such as Databricks SQL access and Workspace access.

#### Setting up Databricks Compute[​](#setting-up-databricks-compute "Direct link to Setting up Databricks Compute")

When you run a dbt project, it generates SQL, which can run on All Purpose Clusters or SQL warehouses. We strongly recommend running dbt-generated SQL on a Databricks SQL warehouse. Since SQL warehouses are optimized for executing SQL queries, you can save on the cost with lower uptime needed for the cluster to run the queries. If you need to debug, you will also have access to a Query Profile.

We recommend using a serverless cluster if you want to minimize the time spent on spinning up a cluster and remove the need to change cluster sizes depending on workflows. If you use a Databricks serverless SQL warehouse, you still need to choose a [cluster size](https://docs.databricks.com/aws/en/compute/sql-warehouse/create#configure-sql-warehouse-settings) (for example, 2X-Small, X-Small, Small, Medium, Large). For more information on serverless SQL warehouses, see the [Databricks docs](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#sizing-a-serverless-sql-warehouse).

Let’s [create a Databricks SQL warehouse](https://docs.databricks.com/sql/admin/sql-endpoints.html#create-a-sql-warehouse):

1. Click **SQL Warehouses** in the sidebar.
2. Click **Create SQL Warehouse**.
3. Enter a name for the warehouse.
4. If using a serverless SQL warehouse, select a [cluster size](https://docs.databricks.com/aws/en/compute/sql-warehouse/warehouse-behavior#sizing-a-serverless-sql-warehouse) (2X-Small through 4X-Large) or leave the default, but ensure it suits your workload.
5. Accept the default warehouse settings or edit them.
6. Click **Create**.
7. Configure warehouse permissions to ensure our service principal and developer have the right access.

We are not covering python in this post but if you want to learn more, check out these [docs](https://docs.getdbt.com/docs/build/python-models.md#specific-data-platforms). Depending on your workload, you may wish to create a larger SQL Warehouse for production workflows while having a smaller development SQL Warehouse (if you’re not using Serverless SQL Warehouses). As your project grows, you might want to apply [compute per model configurations](https://docs.getdbt.com/reference/resource-configs/databricks-configs.md#specifying-the-compute-for-models).

#### Configure your dbt project[​](#configure-your-dbt-project "Direct link to Configure your dbt project")

Now that the Databricks components are in place, we can configure our dbt project. This involves connecting dbt to our Databricks SQL warehouse to run SQL queries and using a version control system like GitHub to store our transformation code.

If you are migrating an existing dbt project from the dbt-spark adapter to dbt-databricks, follow this [migration guide](https://docs.getdbt.com/guides/migrate-from-spark-to-databricks.md) to switch adapters without needing to update developer credentials and other existing configs.

If you’re starting a new dbt project, follow the steps below. For a more detailed setup flow, check out our [quickstart guide.](https://docs.getdbt.com/guides/databricks.md)

##### Connect dbt to Databricks[​](#connect-dbt-to-databricks "Direct link to Connect dbt to Databricks")

First, you’ll need to connect your dbt project to Databricks so it can send transformation instructions and build objects in Unity Catalog. Follow the instructions for [dbt](https://docs.getdbt.com/guides/databricks.md?step=4) or [Core](https://docs.getdbt.com/docs/core/connect-data-platform/databricks-setup.md) to configure your project’s connection credentials.

Each developer must generate their Databricks PAT and use the token in their development credentials. They will also specify a unique developer schema that will store the tables and views generated by dbt runs executed from their Studio IDE. This provides isolated developer environments and ensures data access is fit for purpose.

Let’s generate a [Databricks personal access token (PAT)](https://docs.databricks.com/sql/user/security/personal-access-tokens.html) for Development:

1. In Databricks, click on your Databricks username in the top bar and select User Settings in the drop down.
2. On the Access token tab, click Generate new token.
3. Click Generate.
4. Copy the displayed token and click Done. (don’t lose it!)

For your development credentials/profiles.yml:

1. Set your default catalog to dev.
2. Your developer schema should be named after yourself. We recommend dbt\_\<first\_name\_initial>\<last\_name>.

During your first invocation of `dbt run`, dbt will create the developer schema if it doesn't already exist in the dev catalog.

#### Defining your dbt deployment environment[​](#defining-your-dbt-deployment-environment "Direct link to Defining your dbt deployment environment")

We need to give dbt a way to deploy code outside of development environments. To do so, we’ll use dbt [environments](https://docs.getdbt.com/docs/environments-in-dbt.md) to define the production targets that end users will interact with.

Core projects can use [targets in profiles](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles.md#understanding-targets-in-profiles) to separate environments. [dbt environments](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md#set-up-and-access-the-cloud-ide) allow you to define environments via the UI and [schedule jobs](https://docs.getdbt.com/guides/databricks.md#create-and-run-a-job) for specific environments.

Let’s set up our deployment environment:

1. Follow the Databricks instructions to [set up your service principal’s token](https://docs.databricks.com/dev-tools/service-principals.html#use-curl-or-postman). Note that the `lifetime_seconds` will define how long this credential stays valid. You should use a large number here to avoid regenerating tokens frequently and production job failures.
2. Now let’s pop back over to dbt to fill out the environment fields. Click on environments in the dbt UI or define a new target in your profiles.yml.
3. Set the Production environment’s *catalog* to the **prod** catalog created above. Provide the [service token](https://docs.databricks.com/administration-guide/users-groups/service-principals.html#manage-access-tokens-for-a-service-principal) for your **prod** service principal and set that as the *token* in your production environment’s deployment credentials.
4. Set the schema to the default for your prod environment. This can be overridden by [custom schemas](https://docs.getdbt.com/docs/build/custom-schemas.md#what-is-a-custom-schema) if you need to use more than one.
5. Provide your Service Principal token.

#### Connect dbt to your git repository[​](#connect-dbt-to-your-git-repository "Direct link to Connect dbt to your git repository")

Next, you’ll need somewhere to store and version control your code that allows you to collaborate with teammates. Connect your dbt project to a git repository with [dbt](https://docs.getdbt.com/guides/databricks.md#set-up-a-dbt-cloud-managed-repository). [Core](https://docs.getdbt.com/guides/manual-install.md#create-a-repository) projects will use the git CLI.

##### Next steps[​](#next-steps "Direct link to Next steps")

Now that your project is configured, you can start transforming your Databricks data with dbt. To help you scale efficiently, we recommend you follow our best practices, starting with the [Unity Catalog best practices](https://docs.getdbt.com/best-practices/dbt-unity-catalog-best-practices.md), then you can [Optimize dbt models on Databricks](https://docs.getdbt.com/guides/optimize-dbt-models-on-databricks.md).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Trigger PagerDuty alarms when dbt jobs fail

[Back to guides](https://docs.getdbt.com/guides.md)

Webhooks

Advanced

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

This guide will teach you how to build and host a basic Python app which will monitor dbt jobs and create PagerDuty alarms based on failure. To do this, when a dbt job completes it will:

* Check for any failed nodes (e.g. non-passing tests or errored models), and
* create a PagerDuty alarm based on those nodes by calling the PagerDuty Events API. Events are deduplicated per run ID.

![Screenshot of the PagerDuty UI, showing an alarm created by invalid SQL in a dbt model](/assets/images/pagerduty-example-alarm-b963e5d15b2ec724c8fd76abd58ec13c.png)

In this example, we will use fly.io for hosting/running the service. fly.io is a platform for running full stack apps without provisioning servers etc. This level of usage should comfortably fit inside of the Free tier. You can also use an alternative tool such as [AWS Lambda](https://adem.sh/blog/tutorial-fastapi-aws-lambda-serverless) or [Google Cloud Run](https://github.com/sekR4/FastAPI-on-Google-Cloud-Run).

##### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

This guide assumes some familiarity with:

* [dbt Webhooks](https://docs.getdbt.com/docs/deploy/webhooks.md)
* CLI apps
* Deploying code to a serverless code runner like fly.io or AWS Lambda

#### Clone the `dbt-cloud-webhooks-pagerduty` repo[​](#clone-the-dbt-cloud-webhooks-pagerduty-repo "Direct link to clone-the-dbt-cloud-webhooks-pagerduty-repo")

[This repository](https://github.com/dpguthrie/dbt-cloud-webhooks-pagerduty) contains the sample code for validating a webhook and creating events in PagerDuty.

#### Install `flyctl` and sign up for fly.io[​](#install-flyctl-and-sign-up-for-flyio "Direct link to install-flyctl-and-sign-up-for-flyio")

Follow the directions for your OS in the [fly.io docs](https://fly.io/docs/hands-on/install-flyctl/), then from your command line, run the following commands:

Switch to the directory containing the repo you cloned in step 1:
```

Example 3 (unknown):
```unknown
Sign up for fly.io:
```

Example 4 (unknown):
```unknown
Your console should show `successfully logged in as YOUR_EMAIL` when you're done, but if it doesn't then sign in to fly.io from your command line:
```

---

## Snapshot freshness for a particular source <Term id="table" />:

**URL:** llms-txt#snapshot-freshness-for-a-particular-source-<term-id="table"-/>:

$ dbt source freshness --select source:jaffle_shop.orders

---

## iterate through all source nodes, create if missing, refresh metadata

**URL:** llms-txt#iterate-through-all-source-nodes,-create-if-missing,-refresh-metadata

$ dbt run-operation stage_external_sources

---

## ❌ this will raise an error

**URL:** llms-txt#❌-this-will-raise-an-error

models:
  - name: my_model
    tests:
    config: ...

---

## get environment variables

**URL:** llms-txt#get-environment-variables

#------------------------------------------------------------------------------
api_base        = os.getenv('DBT_URL', 'https://cloud.getdbt.com/') # default to multitenant url
job_cause       = os.getenv('DBT_JOB_CAUSE', 'API-triggered job') # default to generic message
git_branch      = os.getenv('DBT_JOB_BRANCH', None) # default to None
schema_override = os.getenv('DBT_JOB_SCHEMA_OVERRIDE', None) # default to None
api_key         = os.environ['DBT_API_KEY']  # no default here, just throw an error here if key not provided
account_id      = os.environ['DBT_ACCOUNT_ID'] # no default here, just throw an error here if id not provided
project_id      = os.environ['DBT_PROJECT_ID'] # no default here, just throw an error here if id not provided
job_id          = os.environ['DBT_PR_JOB_ID'] # no default here, just throw an error here if id not provided

my_awesome_project
├── python
│   └── run_and_monitor_dbt_job.py
├── .github
│   ├── workflows
│   │   └── dbt_run_on_merge.yml
│   │   └── lint_on_push.yml

name: run dbt job on push

**Examples:**

Example 1 (unknown):
```unknown
**Required input:**

In order to call the dbt API, there are a few pieces of info the script needs. The easiest way to get these values is to open up the job you want to run in dbt. The URL when you’re inside the job has all the values you need:

* `DBT_ACCOUNT_ID` - this is the number just after `accounts/` in the URL
* `DBT_PROJECT_ID` - this is the number just after `projects/` in the URL
* `DBT_PR_JOB_ID` - this is the number just after `jobs/` in the URL

![Image of a dbt job URL with the pieces for account, project, and job highlighted](/assets/images/dbt-cloud-job-url-30ca274dcf77589fb60b72371b59597c.png)

##### 4. Update your project to include the new API call[​](#4-update-your-project-to-include-the-new-api-call "Direct link to 4. Update your project to include the new API call")

* GitHub
* GitLab
* Azure DevOps
* Bitbucket

For this new job, we'll add a file for the dbt API call named `dbt_run_on_merge.yml`.
```

Example 2 (unknown):
```unknown
The YAML file will look pretty similar to our earlier job, but there is a new section called `env` that we’ll use to pass in the required variables. Update the variables below to match your setup based on the comments in the file.

It’s worth noting that we changed the `on:` section to now run **only** when there are pushes to a branch named `main` (for example, a pull request is merged). Have a look through [GitHub documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows) on these filters for additional use cases.

For information about `github` context property names and their use cases, refer to the [GitHub documentation](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/accessing-contextual-information-about-workflow-runs).
```

---

## Assuming 'my_var' is configured to 5 for the current model

**URL:** llms-txt#assuming-'my_var'-is-configured-to-5-for-the-current-model

print(f"{dbt.config.get('my_var')}")  # Output after change: 5

def model(dbt, session):

# setting configuration
    dbt.config(materialized="table")

models:
  - name: my_python_model
    config:
      materialized: table
      target_name: "{{ target.name }}"
      specific_var: "{{ var('SPECIFIC_VAR') }}"
      specific_env_var: "{{ env_var('SPECIFIC_ENV_VAR') }}"

def model(dbt, session):
    target_name = dbt.config.get("target_name")
    specific_var = dbt.config.get("specific_var")
    specific_env_var = dbt.config.get("specific_env_var")

orders_df = dbt.ref("fct_orders")

# limit data in dev
    if target_name == "dev":
        orders_df = orders_df.limit(500)

def model(dbt, session):
    dbt.config(materialized="table")
    
    # Dynamic configuration access within Python f-strings, 
    # which allows for real-time retrieval and use of configuration values.
    # Assuming 'my_var' is set to 5, this will print: Dynamic config value: 5
    print(f"Dynamic config value: {dbt.config.get('my_var')}")

import snowflake.snowpark.functions as F

def model(dbt, session):
    dbt.config(materialized = "incremental")
    df = dbt.ref("upstream_table")

if dbt.is_incremental:

# only new rows compared to max in current table
        max_from_this = f"select max(updated_at) from {dbt.this}"
        df = df.filter(df.updated_at >= session.sql(max_from_this).collect()[0][0])

# or only rows from the past 3 days
        df = df.filter(df.updated_at >= F.dateadd("day", F.lit(-3), F.current_timestamp()))

def model(dbt, session):
  dbt.config(materialized = "incremental")
  bdf = dbt.ref("upstream_table")

if dbt.is_incremental:

# only new rows compared to max in current table
    max_from_this = f"select max(updated_at) from {dbt.this}"

bdf = bdf[bdf['updated_at'] >= bpd.read_gbq(max_from_this).values[0][0]]
    # or only rows from the past 3 days
    bdf = bdf[bdf['updated_at'] >= datetime.date.today() - datetime.timedelta(days=3)]

import pyspark.sql.functions as F

def model(dbt, session):
    dbt.config(materialized = "incremental")
    df = dbt.ref("upstream_table")

if dbt.is_incremental:

# only new rows compared to max in current table
        max_from_this = f"select max(updated_at) from {dbt.this}"
        df = df.filter(df.updated_at >= session.sql(max_from_this).collect()[0][0])

# or only rows from the past 3 days
        df = df.filter(df.updated_at >= F.date_add(F.current_timestamp(), F.lit(-3)))

def add_one(x):
    return x + 1

def model(dbt, session):
    dbt.config(materialized="table")
    temps_df = dbt.ref("temperatures")

# warm things up just a little
    df = temps_df.withColumn("degree_plus_one", add_one(temps_df["degree"]))
    return df

def is_holiday(date_col):
    # Chez Jaffle
    french_holidays = holidays.France()
    is_holiday = (date_col in french_holidays)
    return is_holiday

def model(dbt, session):
    dbt.config(
        materialized = "table",
        packages = ["holidays"]
    )

orders_df = dbt.ref("stg_orders")

df = orders_df.to_pandas()

# apply our function
    # (columns need to be in uppercase on Snowpark)
    df["IS_HOLIDAY"] = df["ORDER_DATE"].apply(is_holiday)
    df["ORDER_DATE"].dt.tz_localize('UTC') # convert from Number/Long to tz-aware Datetime

# return final dataset (Pandas DataFrame)
    return df

def model(dbt, session):
    dbt.config(submission_method="bigframes")

data = {
    'id': [0, 1, 2],
    'name': ['Brian Davis', 'Isaac Smith', 'Marie White'],
    'birthday': ['2024-03-14', '2024-01-01', '2024-11-07']
    }
    bdf = bpd.DataFrame(data)
    bdf['birthday'] = bpd.to_datetime(bdf['birthday'])
    bdf['birthday'] = bdf['birthday'].dt.date

us_holidays = holidays.US(years=2024)

return bdf[bdf['birthday'].isin(us_holidays)]

def is_holiday(date_col):
    # Chez Jaffle
    french_holidays = holidays.France()
    is_holiday = (date_col in french_holidays)
    return is_holiday

def model(dbt, session):
    dbt.config(
        materialized = "table",
        packages = ["holidays"]
    )

orders_df = dbt.ref("stg_orders")

df = orders_df.to_pandas_on_spark()  # Spark 3.2+
    # df = orders_df.toPandas() in earlier versions

# apply our function
    df["is_holiday"] = df["order_date"].apply(is_holiday)

# convert back to PySpark
    df = df.to_spark()               # Spark 3.2+
    # df = session.createDataFrame(df) in earlier versions

# return final dataset (PySpark DataFrame)
    return df

def model(dbt, session):
    dbt.config(
        packages = ["numpy==1.23.1", "scikit-learn"]
    )

models:
  - name: my_python_model
    config:
      packages:
        - "numpy==1.23.1"
        - scikit-learn

import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F
import numpy

def register_udf_add_random():
    add_random = F.udf(
        # use 'lambda' syntax, for simple functional behavior
        lambda x: x + numpy.random.normal(),
        return_type=T.FloatType(),
        input_types=[T.FloatType()]
    )
    return add_random

def model(dbt, session):

dbt.config(
        materialized = "table",
        packages = ["numpy"]
    )

temps_df = dbt.ref("temperatures")

add_random = register_udf_add_random()

# warm things up, who knows by how much
    df = temps_df.withColumn("degree_plus_random", add_random("degree"))
    return df

def model(dbt, session):
    dbt.config(submission_method="bigframes")

# You can also use @bpd.udf
    @bpd.remote_function(dataset='jialuo_test_us')
    def my_func(x: int) -> int:
        return x * 1100

data = {"int": [1, 2], "str": ['a', 'b']}
    bdf = bpd.DataFrame(data=data)
    bdf['int'] = bdf['int'].apply(my_func)

import pyspark.sql.types as T
import pyspark.sql.functions as F
import numpy

**Examples:**

Example 1 (unknown):
```unknown
This also means you can use `dbt.config.get()` within Python models to ensure that configuration values are effectively retrievable and usable within Python f-strings.

#### Configuring Python models[​](#configuring-python-models "Direct link to Configuring Python models")

Just like SQL models, there are three ways to configure Python models:

1. In `dbt_project.yml`, where you can configure many models at once
2. In a dedicated `.yml` file, within the `models/` directory
3. Within the model's `.py` file, using the `dbt.config()` method

Calling the `dbt.config()` method will set configurations for your model within your `.py` file, similar to the `{{ config() }}` macro in `.sql` model files:

models/my\_python\_model.py
```

Example 2 (unknown):
```unknown
There's a limit to how complex you can get with the `dbt.config()` method. It accepts *only* literal values (strings, booleans, and numeric types) and dynamic configuration. Passing another function or a more complex data structure is not possible. The reason is that dbt statically analyzes the arguments to `config()` while parsing your model without executing your Python code. If you need to set a more complex configuration, we recommend you define it using the [`config` property](https://docs.getdbt.com/reference/resource-properties/config.md) in a YAML file.

###### Accessing project context[​](#accessing-project-context "Direct link to Accessing project context")

dbt Python models don't use Jinja to render compiled code. Python models have limited access to global project contexts compared to SQL models. That context is made available from the `dbt` class, passed in as an argument to the `model()` function.

Out of the box, the `dbt` class supports:

* Returning DataFrames referencing the locations of other resources: `dbt.ref()` + `dbt.source()`
* Accessing the database location of the current model: `dbt.this()` (also: `dbt.this.database`, `.schema`, `.identifier`)
* Determining if the current model's run is incremental: `dbt.is_incremental`

It is possible to extend this context by "getting" them with `dbt.config.get()` after they are configured in the [model's config](https://docs.getdbt.com/reference/model-configs.md). The `dbt.config.get()` method supports dynamic access to configurations within Python models, enhancing flexibility in model logic. This includes inputs such as `var`, `env_var`, and `target`. If you want to use those values for the conditional logic in your model, we require setting them through a dedicated YAML file config:

models/config.yml
```

Example 3 (unknown):
```unknown
Then, within the model's Python code, use the `dbt.config.get()` function to *access* values of configurations that have been set:

models/my\_python\_model.py
```

Example 4 (unknown):
```unknown
###### Dynamic configurations[​](#dynamic-configurations "Direct link to Dynamic configurations")

In addition to the existing methods of configuring Python models, you also have dynamic access to configuration values set with `dbt.config()` within Python models using f-strings. This increases the possibilities for custom logic and configuration management.

models/my\_python\_model.py
```

---

## This command uses the `--scopes` flag to request access to Google Sheets. This makes it possible to transform data in Google Sheets using dbt. If your dbt project does not transform data in Google Sheets, then you may omit the `--scopes` flag.

**URL:** llms-txt#this-command-uses-the-`--scopes`-flag-to-request-access-to-google-sheets.-this-makes-it-possible-to-transform-data-in-google-sheets-using-dbt.-if-your-dbt-project-does-not-transform-data-in-google-sheets,-then-you-may-omit-the-`--scopes`-flag.

**Contents:**
  - Connection profiles

default:
  target: dev
  outputs:
    dev:
      type: bigquery
      threads: 16
      database: ABC123
      schema: JAFFLE_SHOP
      method: oauth
      location: us-east1
      dataproc_batch: null

**Examples:**

Example 1 (unknown):
```unknown
A browser window should open, and you should be prompted to log into your Google account. Once you've done that, dbt will use your OAuth'd credentials to connect to BigQuery.

###### Example gcloud configuration[​](#example-gcloud-configuration "Direct link to Example gcloud configuration")

profiles.yml
```

Example 2 (unknown):
```unknown
#### More information[​](#more-information "Direct link to More information")

Find BigQuery-specific configuration information in the [BigQuery adapter reference guide](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Connection profiles

When you invoke dbt from the command line, dbt parses your `dbt_project.yml` and obtains the `profile` name, which dbt needs to connect to your data warehouse.

dbt\_project.yml
```

---

## override the Snowflake virtual warehouse for just this model

**URL:** llms-txt#override-the-snowflake-virtual-warehouse-for-just-this-model

**Contents:**
  - Snowflake permissions
  - Source configurations
  - Source properties
  - Sources JSON file
  - sql_header
  - Starburst/Trino configurations
  - Starrocks configurations
  - Static analysis
  - static_analysis
  - store_failures

{{
  config(
    materialized='table',
    snowflake_warehouse='EXTRA_LARGE'
  )
}}

aggregated_page_events as (

select
        session_id,
        min(event_time) as session_start,
        max(event_time) as session_end,
        count(*) as count_page_views
    from {{ source('snowplow', 'event') }}
    group by 1

select
        *,
        row_number() over (
            partition by session_id
            order by session_start
        ) as page_view_in_session_index
    from aggregated_page_events

select * from index_sessions

models:
  +copy_grants: true

name: my_project
version: 1.0.0

models:
  my_project:
    sensitive:
      +materialized: view
      +secure: true

use role sysadmin;
create database raw;
create database analytics;

create warehouse loading
    warehouse_size = xsmall
    auto_suspend = 3600
    auto_resume = false
    initially_suspended = true;

create warehouse transforming
    warehouse_size = xsmall
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true;

create warehouse reporting
    warehouse_size = xsmall
    auto_suspend = 60
    auto_resume = true
    initially_suspended = true;

use role securityadmin;

create role loader;
grant all on warehouse loading to role loader;

create role transformer;
grant all on warehouse transforming to role transformer;

create role reporter;
grant all on warehouse reporting to role reporter;

create user stitch_user -- or fivetran_user
    password = '_generate_this_'
    default_warehouse = loading
    default_role = loader;

create user claire -- or amy, jeremy, etc.
    password = '_generate_this_'
    default_warehouse = transforming
    default_role = transformer
    must_change_password = true;

create user dbt_cloud_user
    password = '_generate_this_'
    default_warehouse = transforming
    default_role = transformer;

create user looker_user -- or mode_user etc.
    password = '_generate_this_'
    default_warehouse = reporting
    default_role = reporter;

-- then grant these roles to each user
grant role loader to user stitch_user; -- or fivetran_user
grant role transformer to user dbt_cloud_user;
grant role transformer to user claire; -- or amy, jeremy
grant role reporter to user looker_user; -- or mode_user, periscope_user

use role sysadmin;
grant all on database raw to role loader;

grant usage on database raw to role transformer;
grant usage on future schemas in database raw to role transformer;
grant select on future tables in database raw to role transformer;
grant select on future views in database raw to role transformer;

grant usage on all schemas in database raw to role transformer;
grant select on all tables in database raw to role transformer;
grant select on all views in database raw to role transformer;

grant all on database analytics to role transformer;

grant usage on database analytics to role reporter;
grant usage on future schemas in database analytics to role reporter;
grant select on future tables in database analytics to role reporter;
grant select on future views in database analytics to role reporter;

grant usage on all schemas in database analytics to role reporter;
grant select on all tables in database analytics to role reporter;
grant select on all views in database analytics to role reporter;

grant all on warehouse warehouse_name to role role_name;
grant usage on database database_name to role role_name;
grant create schema on database database_name to role role_name; 
grant usage on schema database.an_existing_schema to role role_name;
grant create table on schema database.an_existing_schema to role role_name;
grant create view on schema database.an_existing_schema to role role_name;
grant usage on future schemas in database database_name to role role_name;
grant monitor on future schemas in database database_name to role role_name;
grant select on future tables in database database_name to role role_name;
grant select on future views in database database_name to role role_name;
grant usage on all schemas in database database_name to role role_name;
grant monitor on all schemas in database database_name to role role_name;
grant select on all tables in database database_name to role role_name;
grant select on all views in database database_name to role role_name;

sources:
  events:
    +enabled: false

sources:
  - name: my_source
    config:
      enabled: true
    tables:
      - name: my_source_table  # enabled
      - name: ignore_this_one  # not enabled
        config:
          enabled: false

sources:
  - name: my_source
    tables:
      - name: my_source_table
        config:
          enabled: "{{ var('my_source_table_enabled', false) }}"

sources:
  events:
    clickstream:
      +enabled: false

sources:
  events:
    clickstream:
      pageviews:
        +enabled: false

sources:
  events:
    clickstream:
      +meta:
        source_system: "Google analytics"
        data_owner: "marketing_team"

sources:
  <resource-path>:
    +freshness:
      warn_after:  
        count: 4
        period: hour

name: jaffle_shop
config-version: 2
...
sources:
  # project names
  jaffle_shop:
    +enabled: true

events:
    # source names
    clickstream:
      # table names
      pageviews:
        +enabled: false
      link_clicks:
        +enabled: true

sources:
  - name: <string> # required
    description: <markdown_string>
    database: <database_name>
    schema: <schema_name>
    loader: <string>

# requires v1.1+
    config:
      <source_config>: <config_value>
      freshness:
      # changed to config in v1.10
      loaded_at_field: <column_name>
        warn_after:
          count: <positive_integer>
          period: minute | hour | day
        error_after:
          count: <positive_integer>
          period: minute | hour | day
        filter: <where-condition>
      meta: {<dictionary>} # changed to config in v1.10
      tags: [<string>] # changed to config in v1.10

# deprecated in v1.10
    overrides: <string>

quoting:
      database: true | false
      schema: true | false
      identifier: true | false

tables:
      - name: <string> #required
        description: <markdown_string>
        identifier: <table_name>
        data_tests:
          - <test>
          - ... # declare additional tests
        config:
          loaded_at_field: <column_name>
          meta: {<dictionary>}
          tags: [<string>]
          freshness:
            warn_after:
              count: <positive_integer>
              period: minute | hour | day
            error_after:
              count: <positive_integer>
              period: minute | hour | day
            filter: <where-condition>

quoting:
          database: true | false
          schema: true | false
          identifier: true | false
        external: {<dictionary>}
        columns:
          - name: <column_name> # required
            description: <markdown_string>
            quote: true | false
            data_tests:
              - <test>
              - ... # declare additional tests
            config:
              meta: {<dictionary>}
              tags: [<string>]
          - name: ... # declare properties of additional columns

- name: ... # declare properties of additional source tables

- name: ... # declare properties of additional sources

sources:
  - name: jaffle_shop
    database: raw
    schema: public
    loader: emr # informational only (free text)

config:
      # changed to config in v1.10
      loaded_at_field: _loaded_at # configure for all sources
      # meta fields are rendered in auto-generated documentation
      meta: # changed to config in v1.10
        contains_pii: true
        owner: "@alice"

# Add tags to this source
      tags: # changed to config in v1.10
        - ecom
        - pii

quoting:
      database: false
      schema: false
      identifier: false

tables:
      - name: orders
        identifier: Orders_
        config:
          # changed to config in v1.10
          loaded_at_field: updated_at # override source defaults
        columns:
          - name: id
            data_tests:
              - unique

- name: price_in_usd
            data_tests:
              - not_null

- name: customers
        quoting:
          identifier: true # override source defaults
        columns:
            data_tests:
              - unique

{{ config(
  sql_header="<sql-statement>"
) }}

models:
  <resource-path>:
    +sql_header: <sql-statement>

{% snapshot snapshot_name %}

{{ config(
  sql_header="<sql-statement>"
) }}

snapshots:
  <resource-path>:
    +sql_header: <sql-statement>

{{ config(
  sql_header="alter session set timezone = 'Australia/Sydney';"
) }}

select * from {{ ref('other_model') }}

models:
  +sql_header: "alter session set timezone = 'Australia/Sydney';"

-- Supply a SQL header:
{% call set_sql_header(config) %}
  CREATE TEMPORARY FUNCTION yes_no_to_boolean(answer STRING)
  RETURNS BOOLEAN AS (
    CASE
    WHEN LOWER(answer) = 'yes' THEN True
    WHEN LOWER(answer) = 'no' THEN False
    ELSE NULL
    END
  );
{%- endcall %}

-- Supply your model code:

select yes_no_to_boolean(yes_no) from {{ ref('other_model') }}

{{
  config(
    pre_hook="set session query_max_run_time='10m'"
  )
}}

hive.metastore-cache-ttl=0s
hive.metastore-refresh-interval=5s

{{
  config(
    materialized='table',
    properties= {
      "format": "'PARQUET'",
      "partitioning": "ARRAY['bucket(id, 2)']",
    }
  )
}}

{% macro trino__get_batch_size() %}
  {{ return(10000) }} -- Adjust this number as you see fit
{% endmacro %}

{{
  config(
    materialized = 'table',
    on_table_exists = 'drop`
  )
}}

models:
  path:
    materialized: table
    +on_table_exists: drop

TrinoUserError(type=USER_ERROR, name=NOT_SUPPORTED, message="Table rename is not yet supported by Glue service")

{{
  config(
    materialized = 'view',
    view_security = 'invoker'
  )
}}

models:
  path:
    materialized: view
    +view_security: invoker

{{
    config(
      materialized = 'incremental', 
      unique_key='<optional>',
      incremental_strategy='<optional>',)
}}
select * from {{ ref('events') }}
{% if is_incremental() %}
  where event_ts > (select max(event_ts) from {{ this }})
{% endif %}

{{
    config(
      materialized = 'incremental')
}}
select * from {{ ref('events') }}
{% if is_incremental() %}
  where event_ts > (select max(event_ts) from {{ this }})
{% endif %}

{{
    config(
      materialized = 'incremental',
      unique_key='user_id',
      incremental_strategy='delete+insert',
      )
}}
select * from {{ ref('users') }}
{% if is_incremental() %}
  where updated_ts > (select max(updated_ts) from {{ this }})
{% endif %}

{{
    config(
      materialized = 'incremental',
      unique_key='user_id',
      incremental_strategy='merge',
      )
}}
select * from {{ ref('users') }}
{% if is_incremental() %}
  where updated_ts > (select max(updated_ts) from {{ this }})
{% endif %}

<hive-catalog-name>.insert-existing-partitions-behavior=OVERWRITE

trino-incremental-hive:
  target: dev
  outputs:
    dev:
      type: trino
      method: none
      user: admin
      password:
      catalog: minio
      schema: tiny
      host: localhost
      port: 8080
      http_scheme: http
      session_properties:
        minio.insert_existing_partitions_behavior: OVERWRITE
      threads: 1

{{
    config(
        materialized = 'incremental',
        properties={
          "format": "'PARQUET'",
          "partitioned_by": "ARRAY['day']",
        }
    )
}}

{{
  config(
    materialized = 'materialized_view',
    properties = {
      'format': "'PARQUET'"
    },
  )
}}

models:
  path:
    materialized: materialized_view
    properties:
      format: "'PARQUET'"

{% macro trino__current_timestamp() %}
    current_timestamp(6)
{% endmacro %}

models:
  - name: NAME_OF_YOUR_MODEL
    config:
      grants:
        select: ['reporter', 'bi']

models:
  <resource-path>:
    materialized: table       // table or view or materialized_view
    keys: ['id', 'name', 'some_date']
    table_type: 'PRIMARY'     // PRIMARY or DUPLICATE or UNIQUE
    distributed_by: ['id']
    buckets: 3                // default 10
    partition_by: ['some_date']
    partition_by_init: ["PARTITION p1 VALUES [('1971-01-01 00:00:00'), ('1991-01-01 00:00:00')),PARTITION p1972 VALUES [('1991-01-01 00:00:00'), ('1999-01-01 00:00:00'))"]
    properties: [{"replication_num":"1", "in_memory": "true"}]
    refresh_method: 'async' // only for materialized view default manual

models:
  - name: <model-name>
    config:
      materialized: table       // table or view or materialized_view
      keys: ['id', 'name', 'some_date']
      table_type: 'PRIMARY'     // PRIMARY or DUPLICATE or UNIQUE
      distributed_by: ['id']
      buckets: 3                // default 10
      partition_by: ['some_date']
      partition_by_init: ["PARTITION p1 VALUES [('1971-01-01 00:00:00'), ('1991-01-01 00:00:00')),PARTITION p1972 VALUES [('1991-01-01 00:00:00'), ('1999-01-01 00:00:00'))"]
      properties: [{"replication_num":"1", "in_memory": "true"}]
      refresh_method: 'async' // only for materialized view default manual

{{ config(
    materialized = 'table',
    keys=['id', 'name', 'some_date'],
    table_type='PRIMARY',
    distributed_by=['id'],
    buckets=3,
    partition_by=['some_date'],
    ....
) }}

CREATE EXTERNAL CATALOG `hive_catalog`
PROPERTIES (
    "hive.metastore.uris"  =  "thrift://127.0.0.1:8087",
    "type"="hive"
);

sources:
  - name: external_example
    schema: hive_catalog.hive_db
    tables:
      - name: hive_table_name

{{ source('external_example', 'hive_table_name') }}

dbt run --static-analysis off
dbt run --static-analysis unsafe

models:
  resource-path:
    +static_analysis: on | unsafe | off

models:
  - name: model_name
    config:
      static_analysis: on | unsafe | off

{{ config(static_analysis='on' | 'unsafe' | 'off') }}

select 
  user_id,
  my_cool_udf(ip_address) as cleaned_ip
from {{ ref('my_model') }}

dbt run --static-analysis off # disable static analysis for all models
dbt run --static-analysis unsafe # use JIT analysis for all models

models:
  jaffle_shop:
    marts:
      +materialized: table

a_package_with_introspective_queries:
    +static_analysis: off

models:
  - name: model_with_static_analysis_off
    config:
      static_analysis: off

{{ config(static_analysis='off') }}

select
  user_id,
  my_cool_udf(ip_address) as cleaned_ip
from {{ ref('my_model') }}

models:
  - name: my_model
    columns:
      - name: my_column
        data_tests:
          - unique:
              config:
                store_failures: true  # always store failures
          - not_null:
              config:
                store_failures: false  # never store failures

{{ config(store_failures = true) }}

{% test <testname>(model, column_name) %}

{{ config(store_failures = false) }}

data_tests:
  +store_failures: true  # all tests
  
  <package_name>:
    +store_failures: false # tests in <package_name>

create schema if not exists dev_username_dbt_test__audit authorization username;

{{ config(store_failures_as="table") }}

-- custom singular test
select 1 as id
where 1=0

models:
  - name: my_model
    columns:
      - name: id
        data_tests:
          - not_null:
              config:
                store_failures_as: view
          - unique:
              config:
                store_failures_as: ephemeral

name: "my_project"
version: "1.0.0"
config-version: 2
profile: "sandcastle"

data_tests:
  my_project:
    +store_failures_as: table
    my_subfolder_1:
      +store_failures_as: view
    my_subfolder_2:
      +store_failures_as: ephemeral

snapshots:
  <resource-path>:
    +strategy: timestamp
    +updated_at: column_name

snapshots:
  <resource-path>:
    +strategy: check
    +check_cols: [column_name] | all

unit_tests:
  - name: test_my_model
    model: my_model
    given:
      - input: ref('my_model_a')
        format: dict
        rows:
          - {id: 1, name: gerda}
          - {id: 2, b: michelle}

unit_tests:
  - name: test_my_model
    model: my_model
    given:
      - input: ref('my_model_a')
        format: csv
        rows: |
          id,name
          1,gerda
          2,michelle

unit_tests:
  - name: test_my_model
    model: my_model
    given:
      - input: ref('my_model_a')
        format: csv
        fixture: my_model_a_fixture

unit_tests:
  - name: test_my_model
    model: my_model
    given:
      - input: ref('my_model_a')
        format: sql
        rows: |
          select 1 as id, 'gerda' as name, null as loaded_at union all
          select 2 as id, 'michelle', null as loaded_at as name

unit_tests:
  - name: test_my_model
    model: my_model
    given:
      - input: ref('my_model_a')
        format: sql
        fixture: my_model_a_fixture

dbt run --select "my_dbt_project_name"   # runs all models in your project
dbt run --select "my_dbt_model"          # runs a specific model
dbt run --select "path/to/my/models"     # runs all models in a specific directory
dbt run --select "my_package.some_model" # run a specific model in a specific package
dbt run --select "tag:nightly"           # run models with the "nightly" tag
dbt run --select "path/to/models"        # run models contained in path/to/models
dbt run --select "path/to/my_model.sql"  # run a specific model by its path

**Examples:**

Example 1 (unknown):
```unknown
#### Copying grants[​](#copying-grants "Direct link to Copying grants")

When the `copy_grants` config is set to `true`, dbt will add the `copy grants` DDL qualifier when rebuilding tables and views. The default value is `false`.

dbt\_project.yml
```

Example 2 (unknown):
```unknown
<!-- -->

#### Secure views[​](#secure-views "Direct link to Secure views")

To create a Snowflake [secure view](https://docs.snowflake.net/manuals/user-guide/views-secure.html), use the `secure` config for view models. Secure views can be used to limit access to sensitive data. Note: secure views may incur a performance penalty, so you should only use them if you need them.

The following example configures the models in the `sensitive/` folder to be configured as secure views.

dbt\_project.yml
```

Example 3 (unknown):
```unknown
#### Source freshness known limitation[​](#source-freshness-known-limitation "Direct link to Source freshness known limitation")

Snowflake calculates source freshness using information from the `LAST_ALTERED` column, meaning it relies on a field updated whenever any object undergoes modification, not only data updates. No action must be taken, but analytics teams should note this caveat.

Per the [Snowflake documentation](https://docs.snowflake.com/en/sql-reference/info-schema/tables#usage-notes):

> The `LAST_ALTERED` column is updated when the following operations are performed on an object:
>
> * DDL operations.
> * DML operations (for tables only).
> * Background maintenance operations on metadata performed by Snowflake.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Snowflake permissions

In Snowflake, permissions are used to control who can perform certain actions on different database objects. Use SQL statements to manage permissions in a Snowflake database.

#### Set up Snowflake account[​](#set-up-snowflake-account "Direct link to Set up Snowflake account")

This section explains how to set up permissions and roles within Snowflake. In Snowflake, you would perform these actions using SQL commands and set up your data warehouse and access control within Snowflake's ecosystem.

1. Set up databases
```

Example 4 (unknown):
```unknown
2. Set up warehouses
```

---

## The following dbt_project.yml configures a project that looks like this:

**URL:** llms-txt#the-following-dbt_project.yml-configures-a-project-that-looks-like-this:

---

## job 2

**URL:** llms-txt#job-2

**Contents:**
  - Building metrics
  - Building semantic models
  - Clone incremental models as the first step of your CI job
  - Conclusion
  - Configuring materializations
  - dbt Mesh FAQs
  - Deciding how to structure your dbt Mesh
  - Don't nest your curlies
  - Examining our builds
  - How we structure our dbt projects

dbt source freshness # must be run again to compare current to previous state
dbt build --select source_status:fresher+ --state path/to/prod/artifacts

select
*
from event_tracking.events
{% if target.name == 'dev' %}
where created_at >= dateadd('day', -3, current_date)
{% endif %}

{% if env_var('DBT_CLOUD_INVOCATION_CONTEXT') != 'prod' %}

metrics:
  - name: revenue
    description: Sum of the order total.
    label: Revenue
    type: simple
    type_params:
      measure: order_total

dbt sl query revenue --group-by metric_time__month
dbt sl list dimensions --metrics revenue # list all dimensions available for the revenue metric

semantic_models:
  - name: orders
    entities: ... # we'll define these later
    dimensions: ... # we'll define these later
    measures: ... # we'll define these later

semantic_models:
  - name: orders
    description: |
      Model containing order data. The grain of the table is the order id.
    model: ref('stg_orders')
    entities: ...
    dimensions: ...
    measures: ...

----------  ids
        id as order_id,
        store_id as location_id,
        customer as customer_id,

---------- properties
        (order_total / 100.0) as order_total,
        (tax_paid / 100.0) as tax_paid,

---------- timestamps
        ordered_at

semantic_models:
  - name: orders
    ...
    entities:
      # we use the column for the name here because order is a reserved word in SQL
      - name: order_id
        type: primary
      - name: location
        type: foreign
        expr: location_id
      - name: customer
        type: foreign
        expr: customer_id

dimensions:
      ...
    measures:
      ...

----------  ids -> entities
    id as order_id,
    store_id as location_id,
    customer as customer_id,

---------- numerics -> measures
    (order_total / 100.0) as order_total,
    (tax_paid / 100.0) as tax_paid,

---------- timestamps -> dimensions
    ordered_at

dimensions:
  - name: ordered_at
    expr: date_trunc('day', ordered_at)
    type: time
    type_params:
      time_granularity: day

dimensions:
  - name: ordered_at
    expr: date_trunc('day', ordered_at)
    type: time
    type_params:
      time_granularity: day
  - name: is_large_order
    type: categorical
    expr: case when order_total > 50 then true else false end

----------  ids -> entities
    id as order_id,
    store_id as location_id,
    customer as customer_id,

---------- numerics -> measures
    (order_total / 100.0) as order_total,
    (tax_paid / 100.0) as tax_paid,

---------- timestamps -> dimensions
    ordered_at

measures:
  - name: order_total
    description: The total amount for each order including taxes.
    agg: sum
  - name: tax_paid
    description: The total tax paid on each order.
    agg: sum

- name: order_count
  description: The count of individual orders.
  expr: 1
  agg: sum

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: ordered_at
    description: |
      Order fact table. This table is at the order grain with one row per order.

model: ref('stg_orders')

entities:
      - name: order_id
        type: primary
      - name: location
        type: foreign
        expr: location_id
      - name: customer
        type: foreign
        expr: customer_id

dimensions:
      - name: ordered_at
        expr: date_trunc('day', ordered_at)
        # use date_trunc(ordered_at, DAY) if using BigQuery
        type: time
        type_params:
          time_granularity: day
      - name: is_large_order
        type: categorical
        expr: case when order_total > 50 then true else false end

measures:
      - name: order_total
        description: The total revenue for each order.
        agg: sum
      - name: order_count
        description: The count of individual orders.
        expr: 1
        agg: sum
      - name: tax_paid
        description: The total tax paid on each order.
        agg: sum

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: ordered_at
    description: |
      Order fact table. This table is at the order grain with one row per order.

model: ref('stg_orders')

entities:
      - name: order_id
        type: primary
      - name: location
        type: foreign
        expr: location_id
      - name: customer
        type: foreign
        expr: customer_id

dimensions:
      - name: ordered_at
        expr: date_trunc('day', ordered_at)
        # use date_trunc(ordered_at, DAY) if using BigQuery
        type: time
        type_params:
          time_granularity: day
      - name: is_large_order
        type: categorical
        expr: case when order_total > 50 then true else false end

measures:
      - name: order_total
        description: The total revenue for each order.
        agg: sum
      - name: order_count
        description: The count of individual orders.
        expr: 1
        agg: sum
      - name: tax_paid
        description: The total tax paid on each order.
        agg: sum

dbt clone --select state:modified+,config.materialized:incremental,state:old

dbt build --select state:modified+

{{
    config(
        materialized='incremental',
        unique_key='unique_id',
        on_schema_change='fail'
    )
}}

{{
        config(
            materialized='view'
        )
    }}

{{
    config(
        materialized='table'
    )
}}

def model(dbt, session):

dbt.config(materialized="table")

semantic_models:
  - name: customer_orders
    defaults:
      agg_time_dimension: first_ordered_at
    description: |
      Customer grain mart that aggregates customer orders.
    model: ref('jaffle_finance', 'fct_orders') # ref('project_name', 'model_name')
    entities:
      ...rest of configuration...
    dimensions:
      ...rest of configuration...
    measures:
      ...rest of configuration...

{{ dbt_utils.date_spine(
      datepart="day",
      start_date=[ USE JINJA HERE ]
      )
  }}

{{ dbt_utils.date_spine(
      datepart="day",
      start_date=var('start_date')
      )
  }}

-- Do not do this! It will not work!

{{ dbt_utils.date_spine(
      datepart="day",
      start_date="{{ var('start_date') }}"
      )
  }}

{# Either of these work #}

{% set query_sql = 'select * from ' ~ ref('my_model') %}

{% set query_sql %}
select * from {{ ref('my_model') }}
{% endset %}

{# This does not #}
{% set query_sql = "select * from {{ ref('my_model')}}" %}

{{ config(post_hook="grant select on {{ this }} to role bi_role") }}

20:24:51  5 of 10 START sql view model main.stg_products ......... [RUN]
20:24:51  5 of 10 OK created sql view model main.stg_products .... [OK in 0.13s]

jaffle_shop
├── README.md
├── analyses
├── seeds
│   └── employees.csv
├── dbt_project.yml
├── macros
│   └── cents_to_dollars.sql
├── models
│   ├── intermediate
│   │   └── finance
│   │       ├── _int_finance__models.yml
│   │       └── int_payments_pivoted_to_orders.sql
│   ├── marts
│   │   ├── finance
│   │   │   ├── _finance__models.yml
│   │   │   ├── orders.sql
│   │   │   └── payments.sql
│   │   └── marketing
│   │       ├── _marketing__models.yml
│   │       └── customers.sql
│   ├── staging
│   │   ├── jaffle_shop
│   │   │   ├── _jaffle_shop__docs.md
│   │   │   ├── _jaffle_shop__models.yml
│   │   │   ├── _jaffle_shop__sources.yml
│   │   │   ├── base
│   │   │   │   ├── base_jaffle_shop__customers.sql
│   │   │   │   └── base_jaffle_shop__deleted_customers.sql
│   │   │   ├── stg_jaffle_shop__customers.sql
│   │   │   └── stg_jaffle_shop__orders.sql
│   │   └── stripe
│   │       ├── _stripe__models.yml
│   │       ├── _stripe__sources.yml
│   │       └── stg_stripe__payments.sql
│   └── utilities
│       └── all_dates.sql
├── packages.yml
├── snapshots
└── tests
    └── assert_positive_value_for_total_amount.sql

select * from {{ source('ecom', 'raw_orders') }}

----------  ids
        id as order_id,
        store_id as location_id,
        customer as customer_id,

---------- strings
        status as order_status,

---------- numerics
        (order_total / 100.0)::float as order_total,
        (tax_paid / 100.0)::float as tax_paid,

---------- booleans
        is_fulfilled,

---------- dates
        date(order_date) as ordered_date,

---------- timestamps
        ordered_at

select * from renamed

{% macro make_cool(uncool_id) %}

do_cool_thing({{ uncool_id }})

select
    entity_id,
    entity_type,
    {% if this %}

{{ the_other_thing }},

{% endif %}
    {{ make_cool('uncool_id') }} as cool_id

def model(dbt, session):
    # set length of time considered a churn
    pd.Timedelta(days=2)

dbt.config(enabled=False, materialized="table", packages=["pandas==1.5.2"])

orders_relation = dbt.ref("stg_orders")

# converting a DuckDB Python Relation into a pandas DataFrame
    orders_df = orders_relation.df()

orders_df.sort_values(by="ordered_at", inplace=True)
    orders_df["previous_order_at"] = orders_df.groupby("customer_id")[
        "ordered_at"
    ].shift(1)
    orders_df["next_order_at"] = orders_df.groupby("customer_id")["ordered_at"].shift(
        -1
    )
    return orders_df

select
        order_id,
        customer_id,
        order_total,
        order_date

from {{ ref('orders') }}

where order_date >= '2020-01-01'

{{
    config(
      materialized = 'table',
      sort = 'id',
      dist = 'id'
    )
}}

{# CTE comments go here #}
filtered_events as (

select * from filtered_events

select
        field_1,
        field_2,
        field_3,
        cancellation_date,
        expiration_date,
        start_date

from {{ ref('my_data') }}

select
        id,
        field_4,
        field_5

from {{ ref('some_cte') }}

select
        id,
        sum(field_4) as total_field_4,
        max(field_5) as max_field_5

select
        my_data.field_1,
        my_data.field_2,
        my_data.field_3,

-- use line breaks to visually separate calculations into blocks
        case
            when my_data.cancellation_date is null
                and my_data.expiration_date is not null
                then expiration_date
            when my_data.cancellation_date is null
                then my_data.start_date + 7
            else my_data.cancellation_date
        end as cancellation_date,

some_cte_agg.total_field_4,
        some_cte_agg.max_field_5

left join some_cte_agg
        on my_data.id = some_cte_agg.id

where my_data.field_1 = 'abc' and
        (
            my_data.field_2 = 'def' or
            my_data.field_2 = 'ghi'
        )

models:
  - name: events
    columns:
      - name: event_id
        description: This is a unique identifier for the event
        data_tests:
          - unique
          - not_null

- name: event_time
        description: "When the event occurred in UTC (eg. 2018-01-01 12:00:00)"
        data_tests:
          - not_null

- name: user_id
        description: The ID of the user who recorded the event
        data_tests:
          - not_null
          - relationships:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                to: ref('users')
                field: id

**Examples:**

Example 1 (unknown):
```unknown
To learn more, read the docs on [state](https://docs.getdbt.com/reference/node-selection/syntax.md#about-node-selection).

#### Pro-tips for dbt Projects[​](#pro-tips-for-dbt-projects "Direct link to Pro-tips for dbt Projects")

##### Limit the data processed when in development[​](#limit-the-data-processed-when-in-development "Direct link to Limit the data processed when in development")

In a development environment, faster run times allow you to iterate your code more quickly. We frequently speed up our runs by using a pattern that limits data based on the [target](https://docs.getdbt.com/reference/dbt-jinja-functions/target.md) name:
```

Example 2 (unknown):
```unknown
Another option is to use the [environment variable `DBT_CLOUD_INVOCATION_CONTEXT`](https://docs.getdbt.com/docs/build/environment-variables.md#dbt-platform-context). This environment variable provides metadata about the execution context of dbt. The possible values are `prod`, `dev`, `staging`, and `ci`.

**Example usage**:
```

Example 3 (unknown):
```unknown
##### Use grants to manage privileges on objects that dbt creates[​](#use-grants-to-manage-privileges-on-objects-that-dbt-creates "Direct link to Use grants to manage privileges on objects that dbt creates")

Use `grants` in [resource configs](https://docs.getdbt.com/reference/resource-configs/grants.md) to ensure that permissions are applied to the objects created by dbt. By codifying these grant statements, you can version control and repeatably apply these permissions.

##### Separate source-centric and business-centric transformations[​](#separate-source-centric-and-business-centric-transformations "Direct link to Separate source-centric and business-centric transformations")

When modeling data, we frequently find there are two stages:

1. Source-centric transformations to transform data from different sources into a consistent structure, for example, re-aliasing and recasting columns, or unioning, joining or deduplicating source data to ensure your model has the correct grain; and
2. Business-centric transformations that transform data into models that represent entities and processes relevant to your business, or implement business definitions in SQL.

We find it most useful to separate these two types of transformations into different models, to make the distinction between source-centric and business-centric logic clear.

##### Managing whitespace generated by Jinja[​](#managing-whitespace-generated-by-jinja "Direct link to Managing whitespace generated by Jinja")

If you're using macros or other pieces of Jinja in your models, your compiled SQL (found in the `target/compiled` directory) may contain unwanted whitespace. Check out the [Jinja documentation](http://jinja.pocoo.org/docs/2.10/templates/#whitespace-control) to learn how to control generated whitespace.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Updating our permissioning guidelines: grants as configs in dbt Core v1.2](https://docs.getdbt.com/blog/configuring-grants)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Building metrics

#### How to build metrics[​](#how-to-build-metrics "Direct link to How to build metrics")

* 💹 We'll start with one of the most important metrics for any business: **revenue**.
* 📖 For now, our metric for revenue will be **defined as the sum of order totals excluding tax**.

#### Defining revenue[​](#defining-revenue "Direct link to Defining revenue")

* 🔢 Metrics have four basic properties:

  <!-- -->

  * `name:` We'll use 'revenue' to reference this metric.
  * `description:` For documentation.
  * `label:` The display name for the metric in downstream tools.
  * `type:` one of `simple`, `ratio`, or `derived`.

* 🎛️ Each type has different `type_params`.

* 🛠️ We'll build a **simple metric** first to get the hang of it, and move on to ratio and derived metrics later.

* 📏 Simple metrics are built on a **single measure defined as a type parameter**.

* 🔜 Defining **measures as their own distinct component** on semantic models is critical to allowing the **flexibility of more advanced metrics**, though simple metrics act mainly as **pass-through that provide filtering** and labeling options.

models/marts/orders.yml
```

Example 4 (unknown):
```unknown
#### Query your metric[​](#query-your-metric "Direct link to Query your metric")

You can use the Cloud CLI for metric validation or queries during development, via the `dbt sl` set of subcommands. Here are some useful examples:
```

---

## ✅ this is fine

**URL:** llms-txt#✅-this-is-fine

**Contents:**
  - Upgrading to v1.6
  - Upgrading to v1.7
  - Upgrading to v1.8
  - Upgrading to v1.9
  - User-defined functions Beta
  - User-defined functions [Beta](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - Validations
  - Version upgrade guides
  - View documentation
  - Visualize and orchestrate downstream exposures EnterpriseEnterprise +

models:
  - name: my_model
    tests: [] # todo! add tests later
    config: ...

--cache-selected-only | --no-cache-selected-only
--debug, -d | --no-debug
--deprecated-print | --deprecated-no-print
--enable-legacy-logger | --no-enable-legacy-logger
--fail-fast, -x | --no-fail-fast
--log-cache-events | --no-log-cache-events
--log-format
--log-format-file
--log-level
--log-level-file
--log-path
--macro-debugging | --no-macro-debugging
--partial-parse | --no-partial-parse
--partial-parse-file-path
--populate-cache | --no-populate-cache
--print | --no-print
--printer-width
--quiet, -q | --no-quiet
--record-timing-info, -r
--send-anonymous-usage-stats | --no-send-anonymous-usage-stats
--single-threaded | --no-single-threaded
--static-parser | --no-static-parser
--use-colors | --no-use-colors
--use-colors-file | --no-use-colors-file
--use-experimental-parser | --no-use-experimental-parser
--version, -V, -v
--version-check | --no-version-check
--warn-error
--warn-error-options
--write-json | --no-write-json

{{ return(load_result('collect_freshness')) }}

dbt ls --select "tag:team_*"

{% materialization view, default %}
  {{ return(my_cool_package.materialization_view_default()) }}
  {% endmaterialization %}
  
  {% materialization view, default %}
  {{ return(my_cool_package.materialization_view_default()) }}
  {% endmaterialization %}
  
pip install dbt-core dbt-ADAPTER_NAME

pip install dbt-core dbt-snowflake

dbt test --select "test_type:unit"           # run all unit tests
dbt test --select "test_type:data"           # run all data tests

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null

{% materialization view, default %}
  {{ return(my_cool_package.materialization_view_default()) }}
  {% endmaterialization %}
  
python3 -m pip install dbt-core dbt-snowflake

REGEXP_CONTAINS(a_string, r'^[0-9]+$')
   
   functions:
     - name: is_positive_int # required
       description: My UDF that determines if a string represents a positive (+) integer # required
       config:
         schema: udf_schema
         database: udf_db
       arguments: # optional
         - name: a_string # required if arguments is specified
           data_type: string # required if arguments is specified
           description: The string that I want to check if it's representing a positive integer (like "10") 
       returns: # required
         data_type: boolean # required
   
   CREATE OR REPLACE FUNCTION udf_db.udf_schema.is_positive_int(a_string STRING)
   RETURNS BOOLEAN
   LANGUAGE SQL
   AS $$
     REGEXP_CONTAINS(a_string, r'^[0-9]+$')
   $$;
   
   CREATE OR REPLACE FUNCTION udf_db.udf_schema.is_positive_int(VARCHAR)
   RETURNS BOOLEAN
   VOLATILE # Technically this function could be set as STABLE, but we don't support setting volatility yet
   AS $$
     REGEXP_CONTAINS($1, r'^[0-9]+$')
   $$ LANGUAGE SQL;
   
   CREATE OR REPLACE FUNCTION udf_db.udf_schema.is_positive_int(a_string STRING)
   RETURNS BOOLEAN
   AS (
     REGEXP_CONTAINS(a_string, r'^[0-9]+$')
   );
   
   CREATE OR REPLACE FUNCTION udf_db.udf_schema.is_positive_int(a_string STRING)
   RETURNS BOOLEAN
   LANGUAGE SQL
   RETURN
     REGEXP_CONTAINS(a_string, r'^[0-9]+$');
   
   CREATE OR REPLACE FUNCTION udf_db.udf_schema.is_positive_int(a_string STRING)
   RETURNS BOOLEAN
   AS $$
     REGEXP_CONTAINS(a_string, r'^[0-9]+$')
   $$ LANGUAGE SQL;
   
   select
       maybe_positive_int_column,
       {{ function('is_positive_int') }}(maybe_positive_int_column)
   from {{ ref('a_model_i_like') }}
   
   select
       maybe_positive_int_column,
       udf_db.udf_schema.is_positive_int(maybe_positive_int_column) as is_positive
   from analytics.dbt_schema.a_model_i_like
   
dbt build --select "+my_model_to_test" --empty

unit_tests:
  - name: test_is_positive_int 
    description: "Check my is_positive_int logic captures edge cases"
    model: my_model
    given:
      - input: ref('a_model_i_like')
        rows:
          - { maybe_positive_int_column: 10 }
          - { maybe_positive_int_column: -4 }
          - { maybe_positive_int_column: +8 }
          - { maybe_positive_int_column: 1.0 }
    expect:
      rows:
        - { maybe_positive_int_column: 10,  is_positive: true }
        - { maybe_positive_int_column: -4,  is_positive: false }
        - { maybe_positive_int_column: +8,  is_positive: true }
        - { maybe_positive_int_column: 1.0, is_positive: true }

{% macro cents_to_dollars(column_name, scale=2) %}
  {{ function('cents_to_dollars') }}({{ column_name }}, {{scale}})
{% endmacro %}

dbt sl validate # <Constant name="cloud" /> users
mf validate-configs # <Constant name="core" /> users

auth_header = request.headers.get('authorization', None)
app_secret = os.environ['MY_DBT_CLOUD_AUTH_TOKEN'].encode('utf-8')
signature = hmac.new(app_secret, request_body, hashlib.sha256).hexdigest()
return signature == auth_header

curl -H 'Authorization: 123' -X POST https://<your-webhook-endpoint>

{
  "accountId": 1,
  "webhookId": "wsu_12345abcde",
  "eventId": "wev_2L6Z3l8uPedXKPq9D2nWbPIip7Z",
  "timestamp": "2023-01-31T19:28:15.742843678Z",
  "eventType": "job.run.started",
  "webhookName": "test",
  "data": {
    "jobId": "123",
    "jobName": "Daily Job (dbt build)",
    "runId": "12345",
    "environmentId": "1234",
    "environmentName": "Production",
    "dbtVersion": "1.0.0",
    "projectName": "Snowflake Github Demo",
    "projectId": "167194",
    "runStatus": "Running",
    "runStatusCode": 3,
    "runStatusMessage": "None",
    "runReason": "Kicked off from the UI by test@test.com",
    "runStartedAt": "2023-01-31T19:28:07Z"
  }
}

{
  "accountId": 1,
  "webhookId": "wsu_12345abcde",
  "eventId": "wev_2L6ZDoilyiWzKkSA59Gmc2d7FDD",
  "timestamp": "2023-01-31T19:29:35.789265936Z",
  "eventType": "job.run.completed",
  "webhookName": "test",
  "data": {
    "jobId": "123",
    "jobName": "Daily Job (dbt build)",
    "runId": "12345",
    "environmentId": "1234",
    "environmentName": "Production",
    "dbtVersion": "1.0.0",
    "projectName": "Snowflake Github Demo",
    "projectId": "167194",
    "runStatus": "Success",
    "runStatusCode": 10,
    "runStatusMessage": "None",
    "runReason": "Kicked off from the UI by test@test.com",
    "runStartedAt": "2023-01-31T19:28:07Z",
    "runFinishedAt": "2023-01-31T19:29:32Z"
  }
}

{
  "accountId": 1,
  "webhookId": "wsu_12345abcde",
  "eventId": "wev_2L6m5BggBw9uPNuSmtg4MUiW4Re",
  "timestamp": "2023-01-31T21:15:20.419714619Z",
  "eventType": "job.run.errored",
  "webhookName": "test",
  "data": {
    "jobId": "123",
    "jobName": "dbt Vault",
    "runId": "12345",
    "environmentId": "1234",
    "environmentName": "dbt Vault Demo",
    "dbtVersion": "1.0.0",
    "projectName": "Snowflake Github Demo",
    "projectId": "167194",
    "runStatus": "Errored",
    "runStatusCode": 20,
    "runStatusMessage": "None",
    "runReason": "Kicked off from the UI by test@test.com",
    "runStartedAt": "2023-01-31T21:14:41Z",
    "runErroredAt": "2023-01-31T21:15:20Z"
  }
}

GET https://{your access URL}/api/v3/accounts/{account_id}/webhooks/subscriptions

{
    "data": [
        {
            "id": "wsu_12345abcde",
            "account_identifier": "act_12345abcde",
            "name": "Webhook for jobs",
            "description": "A webhook for when jobs are started",
            "job_ids": [
                "123",
                "321"
            ],
            "event_types": [
                "job.run.started"
            ],
            "client_url": "https://test.com",
            "active": true,
            "created_at": "1675735768491774",
            "updated_at": "1675787482826757",
            "account_id": "123",
            "http_status_code": "0"
        },
        {
            "id": "wsu_12345abcde",
            "account_identifier": "act_12345abcde",
            "name": "Notification Webhook",
            "description": "Webhook used to trigger notifications in Slack",
            "job_ids": [],
            "event_types": [
                "job.run.completed",
                "job.run.started",
                "job.run.errored"
            ],
            "client_url": "https://test.com",
            "active": true,
            "created_at": "1674645300282836",
            "updated_at": "1675786085557224",
            "http_status_code": "410",
            "dispatched_at": "1675786085548538",
            "account_id": "123"
        }
    ],
    "status": {
        "code": 200
    },
    "extra": {
        "pagination": {
            "total_count": 2,
            "count": 2
        },
        "filters": {
            "offset": 0,
            "limit": 10
        }
    }
}

GET https://{your access URL}/api/v3/accounts/{account_id}/webhooks/subscription/{webhook_id}

{
    "data": {
        "id": "wsu_12345abcde",
        "account_identifier": "act_12345abcde",
        "name": "Webhook for jobs",
        "description": "A webhook for when jobs are started",
        "event_types": [
            "job.run.started"
        ],
        "client_url": "https://test.com",
        "active": true,
        "created_at": "1675789619690830",
        "updated_at": "1675793192536729",
        "dispatched_at": "1675793192533160",
        "account_id": "123",
        "job_ids": [],
        "http_status_code": "0"
    },
    "status": {
        "code": 200
    }
}

POST https://{your access URL}/api/v3/accounts/{account_id}/webhooks/subscriptions

{
	"event_types": [
			"job.run.started"
	],
	"name": "Webhook for jobs",
	"client_url": "https://test.com",
	"active": true,
	"description": "A webhook for when jobs are started",
	"job_ids": [
			123,
			321
	]
}

{
    "data": {
        "id": "wsu_12345abcde",
        "account_identifier": "act_12345abcde",
        "name": "Webhook for jobs",
        "description": "A webhook for when jobs are started",
        "job_ids": [
            "123",
						"321"
        ],
        "event_types": [
            "job.run.started"
        ],
        "client_url": "https://test.com",
        "hmac_secret": "12345abcde",
        "active": true,
        "created_at": "1675795644808877",
        "updated_at": "1675795644808877",
        "account_id": "123",
        "http_status_code": "0"
    },
    "status": {
        "code": 201
    }
}

PUT https://{your access URL}/api/v3/accounts/{account_id}/webhooks/subscription/{webhook_id}

{
	"event_types": [
			"job.run.started"
	],
	"name": "Webhook for jobs",
	"client_url": "https://test.com",
	"active": true,
	"description": "A webhook for when jobs are started",
	"job_ids": [
			123,
			321
	]
}

{
    "data": {
        "id": "wsu_12345abcde",
        "account_identifier": "act_12345abcde",
        "name": "Webhook for jobs",
        "description": "A webhook for when jobs are started",
        "job_ids": [
            "123"
        ],
        "event_types": [
            "job.run.started"
        ],
        "client_url": "https://test.com",
        "active": true,
        "created_at": "1675798888416144",
        "updated_at": "1675804719037018",
        "http_status_code": "200",
        "account_id": "123"
    },
    "status": {
        "code": 200
    }
}

GET https://{your access URL}/api/v3/accounts/{account_id}/webhooks/subscription/{webhook_id}/test

{
    "data": {
        "verification_error": null,
        "verification_status_code": "200"
    },
    "status": {
        "code": 200
    }
}

DELETE https://{your access URL}/api/v3/accounts/{account_id}/webhooks/subscription/{webhook_id}

{
    "data": {
        "id": "wsu_12345abcde"
    },
    "status": {
        "code": 200,
        "is_success": true
    }
}

curl -H 'Authorization: 123' -X POST https://<your-webhook-endpoint>

dbt sl export --saved-query sq_name

Polling for export status - query_id: 2c1W6M6qGklo1LR4QqzsH7ASGFs..
Export completed.

dbt sl export --saved-query sq_name --select export_1,export2

dbt sl export --saved-query sq_number1 --export-as table --alias new_export

Exports completed:
- Created TABLE at `DBT_SL_TEST.new_customer_orders`
- Created VIEW at `DBT_SL_TEST.new_customer_orders_export_alias`
- Created TABLE at `DBT_SL_TEST.order_data_key_metrics`
- Created TABLE at `DBT_SL_TEST.weekly_revenue`

dbt build --select orders+
   
Compilation Error
  In dispatch: Could not find package 'my_project'

country_code,country_name
US,United States
CA,Canada
GB,United Kingdom
...

select * from {{ ref('country_codes') }}

name: jaffle_shop
...

models:
  jaffle_shop:
    marketing:
      schema: marketing # seeds in the `models/mapping/ subdirectory will use the marketing schema

{{
  config(
    schema='core'
  )
}}

name: jaffle_shop
...

seeds:
  jaffle_shop:
    schema: mappings # all seeds in this project will use the schema "mappings" by default
    marketing:
      schema: marketing # seeds in the "seeds/marketing/" subdirectory will use the schema "marketing"

test-paths: ["my_cool_tests"]

model-paths: ["transformations"]

seed-paths: ["custom_seeds"]

snapshot-paths: ["snapshots"]

select
  country_code || '-' || order_id as surrogate_key,
  ...

models:
  - name: orders
    columns:
      - name: surrogate_key
        data_tests:
          - unique

models:
  - name: orders
    data_tests:
      - unique:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            column_name: "(country_code || '-' || order_id)"

models:
  - name: orders
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            combination_of_columns:
              - country_code
              - order_id

{% snapshot snappy %}
  {{ config(materialized = 'table', ...) }}
  ...
{% endsnapshot %}

A snapshot must have a materialized value of 'snapshot'

sudo yum install redhat-rpm-config gcc libffi-devel \
  python-devel openssl-devel

sudo apt-get install git libpq-dev python-dev python3-pip
sudo apt-get remove python-cffi
sudo pip install --upgrade cffi
pip install cryptography~=3.4

**Examples:**

Example 1 (unknown):
```unknown
Some options that could previously be specified *after* a subcommand can now only be specified *before*. This includes the inverse of the option, `--write-json` and `--no-write-json`, for example. The list of affected options are:

List of affected options
```

Example 2 (unknown):
```unknown
Additionally, some options that could be previously specified *before* a subcommand can now only be specified *after*. Any option *not* in the above list must appear *after* the subcommand from v1.5 and later. For example, `--profiles-dir`.

The built-in [collect\_freshness](https://github.com/dbt-labs/dbt-core/blob/1.5.latest/core/dbt/include/global_project/macros/adapters/freshness.sql) macro now returns the entire `response` object, instead of just the `table` result. If you're using a custom override for `collect_freshness`, make sure you're also returning the `response` object; otherwise, some of your dbt commands will never finish. For example:
```

Example 3 (unknown):
```unknown
Finally: The [built-in `generate_alias_name` macro](https://github.com/dbt-labs/dbt-core/blob/1.5.latest/core/dbt/include/global_project/macros/get_custom_name/get_custom_alias.sql) now includes logic to handle versioned models. If your project has reimplemented the `generate_alias_name` macro with custom logic, and you want to start using [model versions](https://docs.getdbt.com/docs/mesh/govern/model-versions.md), you will need to update the logic in your macro. Note that, while this is **not** a prerequisite for upgrading to v1.5—only for using the new feature—we recommend that you do this during your upgrade, whether you're planning to use model versions tomorrow or far in the future.

Likewise, if your project has reimplemented the `ref` macro with custom logic, you will need to update the logic in your macro as described [here](https://docs.getdbt.com/reference/dbt-jinja-functions/builtins.md).

##### For consumers of dbt artifacts (metadata)[​](#for-consumers-of-dbt-artifacts-metadata "Direct link to For consumers of dbt artifacts (metadata)")

The [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json.md) schema version will be updated to `v9`. Specific changes:

* Addition of `groups` as a top-level key
* Addition of `access`, `constraints`, `version`, `latest_version` as a top-level node attributes for models
* Addition of `constraints` as a column-level attribute
* Addition of `group` and `contract` as node configs
* To support model versions, the type of `refs` has changed from `List[List[str]]` to `List[RefArgs]`, with nested keys `name: str`, `package: Optional[str] = None`, and `version: Union[str, float, NoneType] = None)`.

##### For maintainers of adapter plugins[​](#for-maintainers-of-adapter-plugins "Direct link to For maintainers of adapter plugins")

For more detailed information and to ask questions, please read and comment on the GH discussion: [dbt-labs/dbt-core#7213](https://github.com/dbt-labs/dbt-core/discussions/7213).

#### New and changed documentation[​](#new-and-changed-documentation "Direct link to New and changed documentation")

##### Model governance[​](#model-governance "Direct link to Model governance")

The first phase of supporting dbt deployments at scale, across multiple projects with clearly defined ownership and interface boundaries. [Read about model governance](https://docs.getdbt.com/docs/mesh/govern/about-model-governance.md), all of which is new in v1.5.

##### Revamped CLI[​](#revamped-cli "Direct link to Revamped CLI")

Compile and preview dbt models and `--inline` dbt-SQL queries on the CLI using:

* [`dbt compile`](https://docs.getdbt.com/reference/commands/compile.md)
* [`dbt show`](https://docs.getdbt.com/reference/commands/show.md) (new!)

[Node selection methods](https://docs.getdbt.com/reference/node-selection/methods.md) can use Unix-style wildcards to glob nodes matching a pattern:
```

Example 4 (unknown):
```unknown
And (!): a first-ever entry point for [programmatic invocations](https://docs.getdbt.com/reference/programmatic-invocations.md), at parity with CLI commands.

Run `dbt --help` to see new & improved help documentation :)

##### Quick hits[​](#quick-hits "Direct link to Quick hits")

* The [`version: 2` top-level key](https://docs.getdbt.com/reference/project-configs/version.md) is now **optional** in all YAML files. Also, the [`config-version: 2`](https://docs.getdbt.com/reference/project-configs/config-version.md) and `version:` top-level keys are now optional in `dbt_project.yml` files.
* [Events and logging](https://docs.getdbt.com/reference/events-logging.md): Added `node_relation` (`database`, `schema`, `identifier`) to the `node_info` dictionary, available on node-specific events
* Support setting `--project-dir` via environment variable: [`DBT_PROJECT_DIR`](https://docs.getdbt.com/reference/dbt_project.yml.md)
* More granular configurations for logging (to set [log format](https://docs.getdbt.com/reference/global-configs/logs.md#log-formatting), [log levels](https://docs.getdbt.com/reference/global-configs/logs.md#log-level), and [colorization](https://docs.getdbt.com/reference/global-configs/logs.md#color)) and [cache population](https://docs.getdbt.com/reference/global-configs/cache.md#cache-population)
* [dbt overwrites the `manifest.json` file](https://docs.getdbt.com/reference/node-selection/state-comparison-caveats.md#overwrites-the-manifestjson) during parsing, which means when you reference `--state` from the `target/ directory`, you may encounter a warning indicating that the saved manifest wasn't found.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Upgrading to v1.6

dbt Core v1.6 has three significant areas of focus:

1. Next milestone of [multi-project deployments](https://github.com/dbt-labs/dbt-core/discussions/6725): improvements to contracts, groups/access, versions; and building blocks for cross-project `ref`
2. Semantic layer re-launch: dbt Core and [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md) integration
3. Mechanisms to support mature deployment at scale (`dbt clone` and `dbt retry`)

#### Resources[​](#resources "Direct link to Resources")

* [Changelog](https://github.com/dbt-labs/dbt-core/blob/1.6.latest/CHANGELOG.md)
* [dbt Core installation guide](https://docs.getdbt.com/docs/core/installation-overview.md)
* [Cloud upgrade guide](https://docs.getdbt.com/docs/dbt-versions/upgrade-dbt-version-in-cloud.md)
* [Release schedule](https://github.com/dbt-labs/dbt-core/issues/7481)

#### What to know before upgrading[​](#what-to-know-before-upgrading "Direct link to What to know before upgrading")

dbt Labs is committed to providing backward compatibility for all versions 1.x, with the exception of any changes explicitly mentioned below. If you encounter an error upon upgrading, please let us know by [opening an issue](https://github.com/dbt-labs/dbt-core/issues/new).

##### Behavior changes[​](#behavior-changes "Direct link to Behavior changes")

Action required if your project defines `metrics`

The [spec for metrics](https://github.com/dbt-labs/dbt-core/discussions/7456) has changed and now uses [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md).

If your dbt project defines metrics, you must migrate to dbt v1.6 because the YAML spec has moved from dbt\_metrics to MetricFlow. Any tests you have won't compile on v1.5 or older.

* dbt Core v1.6 does not support Python 3.7, which reached End Of Life on June 23. Support Python versions are 3.8, 3.9, 3.10, and 3.11.
* As part of the [dbt Semantic layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md) re-launch (in beta), the spec for `metrics` has changed significantly. Refer to the [migration guide](https://docs.getdbt.com/guides/sl-migration.md) for more info on how to migrate to the re-launched dbt Semantic Layer.
* The manifest schema version is now v10.
* dbt Labs is ending support for Homebrew installation of dbt Core and adapters. See [the discussion](https://github.com/dbt-labs/dbt-core/discussions/8277) for more details.

##### For consumers of dbt artifacts (metadata)[​](#for-consumers-of-dbt-artifacts-metadata "Direct link to For consumers of dbt artifacts (metadata)")

The [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json.md) schema version has been updated to `v10`. Specific changes:

* Addition of `semantic_models` and changes to `metrics` attributes
* Addition of `deprecation_date` as a model property
* Addition of `on_configuration_change` as default node configuration (to support materialized views)
* Small type changes to `contracts` and `constraints`
* Manifest `metadata` includes `project_name`

##### For maintainers of adapter plugins[​](#for-maintainers-of-adapter-plugins "Direct link to For maintainers of adapter plugins")

For more detailed information and to ask questions, please read and comment on the GH discussion: [dbt-labs/dbt Core#7958](https://github.com/dbt-labs/dbt-core/discussions/7958).

#### New and changed documentation[​](#new-and-changed-documentation "Direct link to New and changed documentation")

##### MetricFlow[​](#metricflow "Direct link to MetricFlow")

* [**Build your metrics**](https://docs.getdbt.com/docs/build/build-metrics-intro.md) with MetricFlow, a key component of the Semantic Layer. You can define your metrics and build semantic models with MetricFlow, available on the command line (CLI) for dbt Core v1.6 beta or higher.

##### Materialized views[​](#materialized-views "Direct link to Materialized views")

Supported on:

* [Postgres](https://docs.getdbt.com/reference/resource-configs/postgres-configs.md#materialized-view)
* [Redshift](https://docs.getdbt.com/reference/resource-configs/redshift-configs.md#materialized-view)
* [Snowflake](https://docs.getdbt.com/reference/resource-configs/snowflake-configs.md#dynamic-tables)
* [Databricks](https://docs.getdbt.com/reference/resource-configs/databricks-configs.md#materialized-views-and-streaming-tables)

##### New commands for mature deployment[​](#new-commands-for-mature-deployment "Direct link to New commands for mature deployment")

[`dbt retry`](https://docs.getdbt.com/reference/commands/retry.md) executes the previously run command from the point of failure. Rebuild just the nodes that errored or skipped in a previous run/build/test, rather than starting over from scratch.

[`dbt clone`](https://docs.getdbt.com/reference/commands/clone.md) leverages each data platform's functionality for creating lightweight copies of dbt models from one environment into another. Useful when quickly spinning up a new development environment, or promoting specific models from a staging environment into production.

##### Multi-project collaboration[​](#multi-project-collaboration "Direct link to Multi-project collaboration")

[**Deprecation date**](https://docs.getdbt.com/reference/resource-properties/deprecation_date.md): Models can declare a deprecation date that will warn model producers and downstream consumers. This enables clear migration windows for versioned models, and provides a mechanism to facilitate removal of immature or little-used models, helping to avoid project bloat.

[Model names](https://docs.getdbt.com/faqs/Project/unique-resource-names.md) can be duplicated across different namespaces (projects/packages), so long as they are unique within each project/package. We strongly encourage using [two-argument `ref`](https://docs.getdbt.com/reference/dbt-jinja-functions/ref.md#ref-project-specific-models) when referencing a model from a different package/project.

More consistency and flexibility around packages. Resources defined in a package will respect variable and global macro definitions within the scope of that package.

* `vars` defined in a package's `dbt_project.yml` are now available in the resolution order when compiling nodes in that package, though CLI `--vars` and the root project's `vars` will still take precedence. See ["Variable Precedence"](https://docs.getdbt.com/docs/build/project-variables.md#variable-precedence) for details.
* `generate_x_name` macros (defining custom rules for database, schema, alias naming) follow the same pattern as other "global" macros for package-scoped overrides. See [macro dispatch](https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch.md) for an overview of the patterns that are possible.

Closed Beta - dbt Enterprise

[**Project dependencies**](https://docs.getdbt.com/docs/mesh/govern/project-dependencies.md): Introduces `dependencies.yml` and dependent `projects` as a feature of dbt Enterprise. Allows enforcing model access (public vs. protected/private) across project/package boundaries. Enables cross-project `ref` of public models, without requiring the installation of upstream source code.

##### Deprecated functionality[​](#deprecated-functionality "Direct link to Deprecated functionality")

The ability for installed packages to override built-in materializations without explicit opt-in from the user is being deprecated.

* Overriding a built-in materialization from an installed package raises a deprecation warning.

* Using a custom materialization from an installed package does not raise a deprecation warning.

* Using a built-in materialization package override from the root project via a wrapping materialization is still supported. For example:
```

---

## tests on everything _except_ sources

**URL:** llms-txt#tests-on-everything-_except_-sources

dbt test --exclude "source:*"

dbt test --select "assert_total_payment_amount_is_positive" # directly select the test by name
dbt test --select "payments,test_type:singular" # indirect selection, v1.2

**Examples:**

Example 1 (unknown):
```unknown
##### More complex selection[​](#more-complex-selection "Direct link to More complex selection")

Through the combination of direct and indirect selection, there are many ways to accomplish the same outcome. Let's say we have a data test named `assert_total_payment_amount_is_positive` that depends on a model named `payments`. All of the following would manage to select and execute that test specifically:
```

Example 2 (unknown):
```unknown
As long as you can select a common property of a group of resources, indirect selection allows you to execute all the tests on those resources, too. In the example above, we saw it was possible to test all table-materialized models. This principle can be extended to other resource types, too:
```

---

## rest of dbt_project.yml

**URL:** llms-txt#rest-of-dbt_project.yml

**Contents:**
  - external
  - fail_calc
  - Failing fast
  - Firebolt configurations

exposures:
  +enabled: true

sources:
  - name: <source_name>
    tables:
      - name: <table_name>
        external:
          location: <string>
          file_format: <string>
          row_format: <string>
          tbl_properties: <string>      
          partitions:
            - name: <column_name>
              data_type: <string>
              description: <string>
              config:
                meta: {dictionary} # changed to config in v1.10
            - ...
          <additional_property>: <additional_value>

None is not of type 'integer'

Failed validating 'type' in schema['properties']['failures']:
    {'type': 'integer'}

On instance['failures']:
    None

fail_calc: "case when count(*) > 0 then sum(n_records) else 0 end"

models:
  - name: my_model
    columns:
      - name: my_columns
        data_tests:
          - unique:
              config:
                fail_calc: "case when count(*) > 0 then sum(n_records) else 0 end"

{{ config(fail_calc = "sum(total_revenue) - sum(revenue_accounted_for)") }}

{% test <testname>(model, column_name) %}

{{ config(fail_calc = "missing_in_a + missing_in_b") }}

data_tests:
  +fail_calc: count(*)  # all tests
  
  <package_name>:
    +fail_calc: count(distinct id) # tests in <package_name>

$ dbt run -x --threads 1
Running with dbt=1.0.0
Found 4 models, 1 test, 1 snapshot, 2 analyses, 143 macros, 0 operations, 1 seed file, 0 sources

14:47:39 | Concurrency: 1 threads (target='dev')
14:47:39 |
14:47:39 | 1 of 4 START table model test_schema.model_1........... [RUN]
14:47:40 | 1 of 4 ERROR creating table model test_schema.model_1.. [ERROR in 0.06s]
14:47:40 | 2 of 4 START view model test_schema.model_2............ [RUN]
14:47:40 | CANCEL query model.debug.model_2....................... [CANCEL]
14:47:40 | 2 of 4 ERROR creating view model test_schema.model_2... [ERROR in 0.05s]

Database Error in model model_1 (models/model_1.sql)
  division by zero
  compiled SQL at target/run/debug/models/model_1.sql

Encountered an error:
FailFast Error in model model_1 (models/model_1.sql)
  Failing early due to test failure or runtime error

seeds:
  +quote_columns: false  #or `true` if you have CSV column headers with spaces

models:
  <resource-path>:
    +materialized: table
    +table_type: fact
    +primary_index: [ <column-name>, ... ]
    +indexes:
      - index_type: aggregating
        key_columns: [ <column-name>, ... ]
        aggregation: [ <agg-sql>, ... ]
      ...

models:
  - name: <model-name>
    config:
      materialized: table
      table_type: fact
      primary_index: [ <column-name>, ... ]
      indexes:
        - index_type: aggregating
          key_columns: [ <column-name>, ... ]
          aggregation: [ <agg-sql>, ... ]
        ...

{{ config(
    materialized = "table"
    table_type = "fact"
    primary_index = [ "<column-name>", ... ],
    indexes = [
      {
        "index_type": "aggregating"
        "key_columns": [ "<column-name>", ... ],
        "aggregation": [ "<agg-sql>", ... ],
      },
      ...
    ]
) }}

{{ config(
    materialized = "table",
    table_type = "fact",
    primary_index = "id",
    indexes = [
      {
        "index_type": "aggregating",
        "key_columns": "order_id",
        "aggregation": ["COUNT(DISTINCT status)", "AVG(customer_id)"]
      }
    ]
) }}

models:
  <resource-path>:
    +materialized: table
    +table_type: dimension
    ...

models:
  - name: <model-name>
    config:
      materialized: table
      table_type: dimension
    ...

{{ config(
    materialized = "table",
    table_type = "dimension",
    ...
) }}

<table-name>__<key-column>__<index-type>_<unix-timestamp-at-execution>

packages:
     - package: dbt-labs/dbt_external_tables
       version: <version>
   
   dispatch:
     - macro_namespace: dbt_external_tables
       search_order: ['dbt', 'dbt_external_tables']
   
sources:
  - name: firebolt_external
    schema: "{{ target.schema }}"
    loader: S3

tables:
      - name: <table-name>
        external:
          url: 's3://<bucket_name>/'
          object_pattern: '<regex>'
          type: '<type>'
          credentials:
            aws_key_id: <key-id>
            aws_secret_key: <key-secret>
          object_pattern: '<regex>'
          compression: '<compression-type>'
          partitions:
            - name: <partition-name>
              data_type: <partition-type>
              regex: '<partition-definition-regex>'
          columns:
            - name: <column-name>
              data_type: <type>

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### external

models/\<filename>.yml
```

Example 2 (unknown):
```unknown
#### Definition[​](#definition "Direct link to Definition")

An extensible dictionary of metadata properties specific to sources that point to external tables. There are optional built-in properties, with simple type validation, that roughly correspond to the Hive external table spec. You may define and use as many additional properties as you'd like.

You may wish to define the `external` property in order to:

* Power macros that introspect [`graph.sources`](https://docs.getdbt.com/reference/dbt-jinja-functions/graph.md)
* Define metadata that you can later extract from the [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json.md)

For an example of how this property can be used to power custom workflows, see the [`dbt-external-tables`](https://github.com/dbt-labs/dbt-external-tables) package.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### fail_calc

Test queries are written to return a set of failing records, ones not matching the expectation or assertion declared by that test: duplicate records, null values, etc.

Most often, this is the count of rows returned by the test query: the default value of `fail_calc` is `count(*)`. But it can also be a custom calculation, whether an aggregate calculation or simply the name of a column to be selected from the test query.

Most tests do not use the `fail_calc` config, preferring to return a count of failing rows. For the tests that do, the most common place to set the `fail_calc` config is right within a generic test block, alongside its query definition. All the same, `fail_calc` can be set in all the same places as other configs.

For instance, you can configure a `unique` test to return `sum(n_records)` instead of `count(*)` as the failure calculation: that is, the number of rows in the model containing a duplicated column value, rather than the number of distinct column values that are duplicated.

Tip

Beware using functions like `sum()` for `fail_calc` in any test that has the potential to return no rows at all.

If no rows are returned, the test won't pass or fail but will return the following error:
```

Example 3 (unknown):
```unknown
To avoid this issue, use a case statement to ensure that `0` is returned when no rows exist:
```

Example 4 (unknown):
```unknown
* Specific test
* One-off test
* Generic test block
* Project level

Configure a specific instance of a generic (schema) test:

models/\<filename>.yml
```

---

## legacy -- renamed to dbt_packages in dbt v1

**URL:** llms-txt#legacy----renamed-to-dbt_packages-in-dbt-v1

**Contents:**
  - Set up Azure DevOps [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - dbt audit log [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Enterprise permissions [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Migrating to Auth0 for SSO [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up BigQuery OAuth [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up Databricks OAuth [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up external OAuth with Redshift [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up external OAuth with Snowflake [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up SCIM [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Set up Snowflake OAuth [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

<<<<<< HEAD
    your current code
======
    conflicting code
>>>>>> (some branch identifier)

https://github.com/dbt-labs/jaffle_shop/compare/{{destination}}..{{source}}

https://github.com/dbt-labs/jaffle_shop/compare/master..my-branch

https://github.com/<org>/<repo>/compare/{{destination}}..{{source}}

https://git.<mycompany>.com/<org>/<repo>/compare/{{destination}}..{{source}}

https://gitlab.com/<org>/<repo>/-/merge_requests/new?merge_request[source_branch]={{source}}&merge_request[target_branch]={{destination}}

https://bitbucket.org/<org>/<repo>/pull-requests/new?source={{source}}&dest={{destination}}

https://<bitbucket-server>/projects/<proj>/repos/<repo>/pull-requests?create&sourceBranch={{source}}&targetBranch={{destination}}

https://console.aws.amazon.com/codesuite/codecommit/repositories/<repo>/pull-requests/new/refs/heads/{{destination}}/.../refs/heads/{{source}}

https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequestcreate?sourceRef={{source}}&targetRef={{destination}}

{
    "bit": 1,
    "displayName": "View Subscriptions",
    "name": "ViewSubscriptions"
}

az devops security permission update --organization https://dev.azure.com/<org_name> --namespace-id cb594ebe-87dd-4fc9-ac2c-6a10a4c92046 --subject <service_account>@xxxxxx.onmicrosoft.com --token PublisherSecurity/<azure_devops_project_object_id> --allow-bit 1

{
    "bit": 2,
    "displayName": "Edit Subscription",
    "name": "EditSubscriptions"
}

az devops security permission update --organization https://dev.azure.com/<org_name> --namespace-id cb594ebe-87dd-4fc9-ac2c-6a10a4c92046 --subject <service_account>@xxxxxx.onmicrosoft.com --token PublisherSecurity/<azure_devops_project_object_id> --allow-bit 2

{
    "bit": 4,
    "displayName": "Delete Subscriptions",
    "name": "DeleteSubscriptions"
}

az devops security permission update --organization https://dev.azure.com/<org_name> --namespace-id cb594ebe-87dd-4fc9-ac2c-6a10a4c92046 --subject <service_account>@xxxxxx.onmicrosoft.com --token PublisherSecurity/<azure_devops_project_object_id> --allow-bit 4

{ 	
    "bit": 16384,  
    "displayName": "Contribute to pull requests",
    "name": "PullRequestContribute"
}

az devops security permission update --organization https://dev.azure.com/<org_name> --namespace-id 2e9eb7ed-3c0a-47d4-87c1-0ffdd275fd87 --subject <service_account>@xxxxxx.onmicrosoft.com --token repoV2/<azure_devops_project_object_id>/<azure_devops_repository_object_id> --allow-bit 16384

{
    "bit": 4,
    "displayName": "Contribute",
    "name": "GenericContribute"
}

az devops security permission update --organization https://dev.azure.com/<org_name> --namespace-id 2e9eb7ed-3c0a-47d4-87c1-0ffdd275fd87 --subject <service_account>@xxxxxx.onmicrosoft.com --token repoV2/<azure_devops_project_object_id>/<azure_devops_repository_object_id> --allow-bit 4

dbt_packages/
logs/
target/

curl -X POST -H "Content-Type: application/x-www-form-urlencoded" \
     -d 'client_id=<client-id> \
     &scope=<application-ID-URI>/.default \
     &client_secret=<client-secret> \
     &grant_type=client_credentials' \
     'https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token'
   
   curl -X POST -H "Content-Type: application/x-www-form-urlencoded" \
     -d 'client_id=<client-id> \
     &scope=<application-ID-URI>/.default \
     &client_secret=<client-secret> \
     &grant_type=client_credentials' \
     'https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token'

create security integration your_integration_name
type = external_oauth
enabled = true
external_oauth_type = okta
external_oauth_issuer = ''
external_oauth_jws_keys_url = ''
external_oauth_audience_list = ('')
external_oauth_token_user_mapping_claim = 'sub'
external_oauth_snowflake_user_mapping_attribute = 'email_address'
external_oauth_any_role_mode = 'ENABLE'

create security integration your_integration_name
type = external_oauth
enabled = true
external_oauth_type = okta
external_oauth_issuer = ''
external_oauth_jws_keys_url = ''
external_oauth_audience_list = ('')
external_oauth_token_user_mapping_claim = 'sub'
external_oauth_snowflake_user_mapping_attribute = 'email_address'
external_oauth_any_role_mode = 'ENABLE'

create or replace security integration <whatever you want to name it>
   type = external_oauth
   enabled = true
   external_oauth_type = azure
   external_oauth_issuer = '<AZURE_AD_ISSUER>'
   external_oauth_jws_keys_url = '<AZURE_AD_JWS_KEY_ENDPOINT>'
   external_oauth_audience_list = ('<SNOWFLAKE_APPLICATION_ID_URI>')
   external_oauth_token_user_mapping_claim = 'upn'
   external_oauth_any_role_mode = 'ENABLE'
   external_oauth_snowflake_user_mapping_attribute = 'login_name';

Failed to connect to DB: xxxxxxx.snowflakecomputing.com:443. The role requested in the connection, or the default role if none was requested in the connection ('xxxxx'), is not listed in the Access Token or was filtered. 
   Please specify another role, or contact your OAuth Authorization server administrator.
   
   ALTER INTEGRATION <my_int_name> SET EXTERNAL_OAUTH_SCOPE_MAPPING_ATTRIBUTE = 'scp';
   
   Failed to connect to DB: xxxxxxx.snowflakecomputing.com:443. Incorrect username or password was specified.
   
CREATE OR REPLACE SECURITY INTEGRATION DBT_CLOUD
  TYPE = OAUTH
  ENABLED = TRUE
  OAUTH_CLIENT = CUSTOM
  OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
  OAUTH_REDIRECT_URI = '<REDIRECT_URI>'
  OAUTH_ISSUE_REFRESH_TOKENS = TRUE
  OAUTH_REFRESH_TOKEN_VALIDITY = 7776000
  OAUTH_USE_SECONDARY_ROLES = 'IMPLICIT';  -- Required for secondary roles

integration_secrets as (
  select parse_json(system$show_oauth_client_secrets('DBT_CLOUD')) as secrets
)

select
  secrets:"OAUTH_CLIENT_ID"::string     as client_id,
  secrets:"OAUTH_CLIENT_SECRET"::string as client_secret
from
  integration_secrets;

ALTER SECURITY INTEGRATION <security_integration_name>
SET NETWORK_POLICY = <network_policy_name> ;

OAUTH_USE_SECONDARY_ROLES = 'IMPLICIT';

-----BEGIN CERTIFICATE-----
    MIIC8DCCAdigAwIBAgIQSANTIKwxA1221kqhkiG9w0dbtLabsBAQsFADA0MTIwMAYDVQQD
    EylNaWNyb3NvZnQgQXp1cmUgRmVkZXJhdGVkIFNTTyBDZXJ0aWZpY2F0ZTAeFw0yMzEyMjIwMDU1
    MDNaFw0yNjEyMjIwMDU1MDNaMDQxMjAwBgNVBAMTKU1pY3Jvc29mdCBBenVyZSBGZWRlcmF0ZWQg
    U1NPIENlcnRpZmljYXRlMIIBIjANBgkqhkiG9w0BAEFAAFRANKIEMIIBCgKCAQEAqfXQGc/D8ofK
    aXbPXftPotqYLEQtvqMymgvhFuUm+bQ9YSpS1zwNQ9D9hWVmcqis6gO/VFw61e0lFnsOuyx+XMKL
    rJjAIsuWORavFqzKFnAz7hsPrDw5lkNZaO4T7tKs+E8N/Qm4kUp5omZv/UjRxN0XaD+o5iJJKPSZ
    PBUDo22m+306DE6ZE8wqxT4jTq4g0uXEitD2ZyKaD6WoPRETZELSl5oiCB47Pgn/mpqae9o0Q2aQ
    LP9zosNZ07IjKkIfyFKMP7xHwzrl5a60y0rSIYS/edqwEhkpzaz0f8QW5pws668CpZ1AVgfP9TtD
    Y1EuxBSDQoY5TLR8++2eH4te0QIDAQABMA0GCSqGSIb3DmAKINgAA4IBAQCEts9ujwaokRGfdtgH
    76kGrRHiFVWTyWdcpl1dNDvGhUtCRsTC76qwvCcPnDEFBebVimE0ik4oSwwQJALExriSvxtcNW1b
    qvnY52duXeZ1CSfwHkHkQLyWBANv8ZCkgtcSWnoHELLOWORLD4aSrAAY2s5hP3ukWdV9zQscUw2b
    GwN0/bTxxQgA2NLZzFuHSnkuRX5dbtrun21USPTHMGmFFYBqZqwePZXTcyxp64f3Mtj3g327r/qZ
    squyPSq5BrF4ivguYoTcGg4SCP7qfiNRFyBUTTERFLYU0n46MuPmVC7vXTsPRQtNRTpJj/b2gGLk
    1RcPb1JosS1ct5Mtjs41
    -----END CERTIFICATE-----
    
    -----BEGIN CERTIFICATE-----
    MIIC8DCCAdigAwIBAgIQSANTIKwxA1221kqhkiG9w0dbtLabsBAQsFADA0MTIwMAYDVQQD
    EylNaWNyb3NvZnQgQXp1cmUgRmVkZXJhdGVkIFNTTyBDZXJ0aWZpY2F0ZTAeFw0yMzEyMjIwMDU1
    MDNaFw0yNjEyMjIwMDU1MDNaMDQxMjAwBgNVBAMTKU1pY3Jvc29mdCBBenVyZSBGZWRlcmF0ZWQg
    U1NPIENlcnRpZmljYXRlMIIBIjANBgkqhkiG9w0BAEFAAFRANKIEMIIBCgKCAQEAqfXQGc/D8ofK
    aXbPXftPotqYLEQtvqMymgvhFuUm+bQ9YSpS1zwNQ9D9hWVmcqis6gO/VFw61e0lFnsOuyx+XMKL
    rJjAIsuWORavFqzKFnAz7hsPrDw5lkNZaO4T7tKs+E8N/Qm4kUp5omZv/UjRxN0XaD+o5iJJKPSZ
    PBUDo22m+306DE6ZE8wqxT4jTq4g0uXEitD2ZyKaD6WoPRETZELSl5oiCB47Pgn/mpqae9o0Q2aQ
    LP9zosNZ07IjKkIfyFKMP7xHwzrl5a60y0rSIYS/edqwEhkpzaz0f8QW5pws668CpZ1AVgfP9TtD
    Y1EuxBSDQoY5TLR8++2eH4te0QIDAQABMA0GCSqGSIb3DmAKINgAA4IBAQCEts9ujwaokRGfdtgH
    76kGrRHiFVWTyWdcpl1dNDvGhUtCRsTC76qwvCcPnDEFBebVimE0ik4oSwwQJALExriSvxtcNW1b
    qvnY52duXeZ1CSfwHkHkQLyWBANv8ZCkgtcSWnoHELLOWORLD4aSrAAY2s5hP3ukWdV9zQscUw2b
    GwN0/bTxxQgA2NLZzFuHSnkuRX5dbtrun21USPTHMGmFFYBqZqwePZXTcyxp64f3Mtj3g327r/qZ
    squyPSq5BrF4ivguYoTcGg4SCP7qfiNRFyBUTTERFLYU0n46MuPmVC7vXTsPRQtNRTpJj/b2gGLk
    1RcPb1JosS1ct5Mtjs41
    -----END CERTIFICATE-----
    
Subject: New Multi-Tenant PrivateLink Request
- Type: Postgres Interface-type
- VPC Endpoint Service Name:
- Postgres server AWS Region (for example, us-east-1, eu-west-2):
- dbt AWS multi-tenant environment (US, EMEA, AU):

Subject: New Multi-Tenant PrivateLink Request
     - Type: Redshift-managed
     - Redshift cluster name:
     - Redshift cluster AWS account ID:
     - Redshift cluster AWS Region (for example, us-east-1, eu-west-2):
     - <Constant name="cloud" /> multi-tenant environment (US, EMEA, AU):
     
     Subject: New Multi-Tenant PrivateLink Request
     - Type: Redshift-managed - Serverless
     - Redshift workgroup name:
     - Redshift workgroup AWS account ID:
     - Redshift workgroup AWS Region (for example, us-east-1, eu-west-2):
     - <Constant name="cloud" /> multi-tenant environment (US, EMEA, AU):
     
Subject: New Multi-Tenant PrivateLink Request
- Type: Redshift Interface-type
- VPC Endpoint Service Name:
- Redshift cluster AWS Region (for example, us-east-1, eu-west-2):
- dbt AWS multi-tenant environment (US, EMEA, AU):

Subject: New Multi-Tenant GCP PSC Request
- Type: BigQuery
- BigQuery project region: 
- dbt GCP multi-tenant environment:

Subject: New Azure Multi-Tenant Private Link Request
   - Type: Databricks
   - Databricks instance name:
   - Azure Databricks Workspace URL (for example, adb-################.##.azuredatabricks.net)
   - Databricks Azure resource ID:
   - dbt Azure multi-tenant environment (EMEA):
   - Azure Databricks workspace region (like WestEurope, NorthEurope):
   
   Subject: New AWS Multi-Tenant PrivateLink Request
   - Type: Databricks
   - Databricks instance name:
   - Databricks cluster AWS Region (for example, us-east-1, eu-west-2):
   - dbt AWS multi-tenant environment (US, EMEA, AU):
   
     Subject: New Azure Multi-Tenant Private Link Request
   - Type: Azure Database for Postgres Flexible Server
   - Postgres Flexible Server name:
   - Azure Database for Postgres Flexible Server resource ID:
   - dbt Azure multi-tenant environment (EMEA):
   - Azure Postgres server region (for example, WestEurope, NorthEurope):
   
     Subject: New Azure Multi-Tenant Private Link Request
   - Type: Azure Synapse
   - Server name:
   - Azure Synapse workspace resource ID:
   - dbt Azure multi-tenant environment (EMEA):
   - Azure Synapse workspace region (for example, WestEurope, NorthEurope):
   
Subject: New Multi-Tenant PrivateLink Request
- Type: VCS Interface-type
- VPC Endpoint Service Name:
- Custom DNS (if HTTPS)
    - Private hosted zone:
    - DNS record:
- VCS install AWS Region (for example, us-east-1, eu-west-2):
- dbt AWS multi-tenant environment (US, EMEA, AU):

USE ROLE ACCOUNTADMIN;
SELECT SYSTEM$GET_PRIVATELINK_CONFIG();

Subject: New Multi-Tenant Azure PrivateLink Request
- Type: Snowflake
- The output from SYSTEM$GET_PRIVATELINK_CONFIG:
  - Include the privatelink-pls-id
  - Enable Internal Stage Private Link? Y/N (If Y, output must include `privatelink-internal-stage`)
- dbt Azure multi-tenant environment (EMEA):

USE ROLE ACCOUNTADMIN;

-- Azure Private Link
SELECT SYSTEMS$AUTHORIZE_STAGE_PRIVATELINK_ACCESS ( `AZURE PRIVATE ENDPOINT RESOURCE ID` );

select
  value:linkIdentifier, REGEXP_SUBSTR(value: endpointId, '([^\/]+$)')
from
  table(
    flatten(
      input => parse_json(system$get_privatelink_authorized_endpoints())
    )
  );

CREATE NETWORK RULE allow_dbt_cloud_access
  MODE = INGRESS
  TYPE = AZURELINKID
  VALUE_LIST = ('<Azure Link ID>'); -- Replace '<Azure Link ID>' with the actual ID obtained above

ALTER NETWORK POLICY <network_policy_name>
  ADD ALLOWED_NETWORK_RULE_LIST =('allow_dbt_cloud_access');

Subject: New Multi-Tenant GCP PSC Request
- Type: Snowflake
- SYSTEM$GET_PRIVATELINK_CONFIG output:
- *Use privatelink-account-url or regionless-privatelink-account-url?: 
- dbt GCP multi-tenant environment:

CREATE NETWORK RULE allow_dbt_cloud_access
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('<CIDR_RANGE>'); -- Replace '<CIDR_RANGE>' with the actual CIDR provided

ALTER NETWORK POLICY <network_policy_name>
  ADD ALLOWED_NETWORK_RULE_LIST =('allow_dbt_cloud_access');

Subject: New Multi-Tenant (Azure or AWS) PrivateLink Request
- Type: Snowflake
- SYSTEM$GET_PRIVATELINK_CONFIG output:
- *Use privatelink-account-url or regionless-privatelink-account-url?:
- **Create Internal Stage PrivateLink endpoint? (Y/N): 
- dbt AWS multi-tenant environment (US, EMEA, AU):

s3_stage_vpce_dns_name: '*.vpce-012345678abcdefgh-4321dcba.s3.us-west-2.vpce.amazonaws.com'

CREATE NETWORK RULE allow_dbt_cloud_access
  MODE = INGRESS
  TYPE = AWSVPCEID
  VALUE_LIST = ('<VPCE_ID>'); -- Replace '<VPCE_ID>' with the actual ID provided

ALTER NETWORK POLICY <network_policy_name>
  ADD ALLOWED_NETWORK_RULE_LIST =('allow_dbt_cloud_access');

-- and in a where clause
where <condition_1> and <condition_2> and…

-- and in a case statement
case when <condition_1> and <condition_2> then <result_1> …

-- and in a join
from <table_a>
join <table_b> on
<a_id_1> = <b_id_1> and <a_id_2> = <b_id_2>

select
	order_id,
	status,
	round(amount) as amount
from {{ ref('orders') }}
where status = 'shipped' and amount > 20
limit 3

select
    order_id,
    status
from {{ ref('orders') }}
where status like any ('return%', 'ship%')

select
    date_trunc('month', order_date) as order_month,
    array_agg(distinct status) as status_array
from  {{ ref('orders') }}
group by 1
order by 1

select
	date_trunc('month', order_date) as order_month,
	round(avg(amount)) as avg_order_amount
from {{ ref('orders') }}
where status not in ('returned', 'return_pending')
group by 1

select
    customer_id,
    order_id,
    order_date
from {{ ref('orders') }}
where order_date between '2018-01-01' and '2018-01-31'

case when time_engaged between 0 and 9 then 'low_engagement'
     when time_engaged between 10 and 29 then 'medium_engagement'
     else 'high_engagement' end as engagement

case when [scenario 1] then [result 1]
     when [scenario 2] then [result 2]
    -- …as many scenarios as you want
     when [scenario n] then [result n]
     else [fallback result] -- this else is optional
end as <new_field_name>

select
    order_id,
    round(amount) as amount,
    case when amount between 0 and 10 then 'low'
         when amount between 11 and 20 then 'medium'
         else 'high'
    end as order_value_bucket
from {{ ref('orders') }}

cast(<column_name> as <new_data_type>)

select 
	cast(order_id as string) as order_id,
	cast(customer_id as string) as customer_id,
	order_date,
	status
from {{ ref('orders') }}

/* these lines form a multi-line SQL comment; if it’s uncommented, 
it will make this query error out */
select
	customer_id,
	-- order_id, this row is commented out
	order_date
from {{ ref ('orders') }}

comment on [database object type] <database object name> is 'comment text here';

select
	user_id,
	first_name,
	last_name,
	concat(first_name, ' ', last_name) as full_name
from {{ ref('customers') }}
limit 3

select
	date_part('month', order_date) as order_month,
	count(order_id) as count_all_orders,
	count(distinct(customer_id)) as count_distinct_customers
from {{ ref('orders') }}
group by 1

select
    <fields>
from <table_1> as t1
cross join <table_2> as t2

select
   users.user_id as user_id,
   date.date as date
from {{ ref('users') }} as users
cross join {{ ref('date_spine') }} as date
order by 1

select
	date_part('month', order_date) as order_month,
	round(avg(amount)) as avg_order_amount
from {{ ref('orders') }}
group by 1

date_trunc(<date_part>, <date/time field>)

date_trunc(<date/time field>, <date part>)

select
   order_id,
   order_date,
   {{ date_trunc("week", "order_date") }} as order_week,
   {{ date_trunc("month", "order_date") }} as order_month,
   {{ date_trunc("year", "order_date") }} as order_year
from {{ ref('orders') }}

dateadd( {{ datepart }}, {{ interval }}, {{ from_date }} )

date_add( {{ startDate }}, {{ numDays }} )

date_add( {{ from_date }}, INTERVAL {{ interval }} {{ datepart }} )

{{ from_date }} + (interval '{{ interval }} {{ datepart }}')

{{ dateadd(datepart, interval, from_date_or_timestamp) }}

{{ dateadd(datepart="month", interval=1, from_date_or_timestamp="'2021-08-12'") }}

datediff(<date part>, <start date/time>, <end date/time>)

select
   *,
   {{ datediff("order_date", "'2022-06-09'", "day") }}
from {{ ref('orders') }}

select
	distinct
	row_1,
	row_2
from my_data_source

select
	count(customer_id) as cnt_all_orders,
	count(distinct customer_id) as cnt_distinct_customers
from {{ ref('orders') }}

select
	order_id, --select your columns
	customer_id,
	order_date
from {{ ref('orders') }} --the table/view/model you want to select from
limit 3

select 
	my_first_field,
	count(id) as cnt --or any other aggregate function (sum, avg, etc.) 
from my_table
where my_first_field is not null
group by 1 --grouped by my_first_field
order by 1 desc

select
    customer_id,
    count(order_id) as num_orders
from {{ ref('orders') }}
group by 1
order by 1
limit 5

select
	-- query
from <table>
group by <field(s)>
having condition
[optional order by]

select
    customer_id,
    count(order_id) as num_orders
from {{ ref('orders') }}
group by 1
having num_orders > 1 --if you replace this with `where`, this query would not successfully run

with counts as (
	select
		customer_id,
		count(order_id) as num_orders
	from {{ ref('orders') }}
	group by 1
)
select
	customer_id,
	num_orders
from counts
where num_orders > 1

select
   payment_id,
   order_id,
   payment_method,
   case when payment_method ilike '%card' then 'card_payment' else 'non_card_payment' end as was_card
from {{ ref('payments') }}

select * from {{ source('backend_db', 'orders') }}
where status != 'employee_order'

select * from {{ source('backend_db', 'orders') }}
where status not in ('employee_order', 'influencer_order') --list of order statuses to filter out

where status in (select …)

select
    <fields>
from <table_1> as t1
inner join <table_2> as t2
on t1.id = t2.id

select
   car_type.user_id as user_id,
   car_type.car_type as type,
   car_color.car_color as color
from {{ ref('car_type') }} as car_type
inner join {{ ref('car_color') }} as car_color
on car_type.user_id = car_color.user_id

select
    <fields>
from <table_1> as t1
left join <table_2> as t2
on t1.id = t2.id

select
   car_type.user_id as user_id,
   car_type.car_type as type,
   car_color.car_color as color
from {{ ref('car_type') }} as car_type
left join {{ ref('car_color') }} as car_color
on car_type.user_id = car_color.user_id

select
    user_id,
    first_name
from {{ ref('customers') }}
where first_name like 'J%'
order by 1

select
	some_rows
from my_data_source
limit <integer>

select
	order_id,
	order_date,
	rank () over (order by order_date) as order_rnk
from {{ ref('orders') }}
order by 2
limit 5

lower(<string_column>)

select 
	customer_id,
	lower(first_name) as first_name,
	lower(last_name) as last_name
from {{ ref('customers') }}

select
	date_part('month', order_date) as order_month,
	max(amount) as max_amaount
from {{ ref('orders') }}
group by 1

select
	customer_id,
	min(order_date) as first_order_date,
	max(order_date) as last_order_date
from {{ ref('orders') }}
group by 1
limit 3

select
   payment_id,
   order_id,
   payment_method
from {{ ref('payments') }}
where payment_method not like '%card'

select
	order_id,
	customer_id,
	order_date,
	status,
	amount
from {{ ref('orders') }}
where status = 'shipped' or status = 'completed'
limit 3

select
	column_1,
	column_2
from source_table
order by <field(s)> <asc/desc> --comes after FROM, WHERE, and GROUP BY statements

select
	date_trunc('month, order_date') as order_month,
	round(avg(amount)) as avg_order_amount
from {{ ref('orders') }}
group by 1
order by 1 desc

select
    <fields>
from <table_1> as t1
full outer join <table_1> as t2
on t1.id = t2.id

select
   car_type.user_id as user_id,
   car_type.car_type as type,
   car_color.car_color as color
from {{ ref('car_type') }} as car_type
full outer join {{ ref('car_color') }} as car_color
on car_type.user_id = car_color.user_id
order by 1

select
	order_id,
	order_date,
	rank() over (order by order_date) as order_rank
from {{ ref('orders') }}

select
    <fields>
from <table_1> as t1
right join <table_2> as t2
on t1.id = t2.id

select
   car_type.user_id as user_id,
   car_type.car_type as type,
   car_color.car_color as color
from {{ ref('car_type') }} as car_type
right join {{ ref('car_color') }} as car_color
on car_type.user_id = car_color.user_id

round(<numeric column or data>, [optional] <number of decimal places>)

select 
	cast(order_id as string) as order_id,
	order_date,
	amount,
	round(amount, 1) as rounded_amount
from {{ ref('orders') }}

select
    customer_id,
    order_id,
    order_date,
    row_number() over (partition by customer_id order by order_date) as row_n
from {{ ref('orders') }}
order by 1

select
	order_id, --your first column you want selected
	customer_id, --your second column you want selected
	order_date --your last column you want selected (and so on)
from {{ ref('orders') }} --the table/view/model you want to select from
limit 3

select
	<fields>
from <table_1> as t1
[<join_type>] join <table_2> as t2
on t1.id = t2.id

select
   products.sku_id,
   products.sku_name,
   products.parent_id,
   parents.sku_name as parent_name
from {{ ref('products') }} as products
left join {{ ref('products') }} as parents
on products.parent_id = parents.sku_id

select
	date_trunc('month', order_date)::string as order_month,
	round(avg(amount)) as avg_order_amount
from {{ ref('orders') }}
where status not in ('returned', 'return_pending')
group by 1

select
	customer_id,
	sum(order_amount) as all_orders_amount
from {{ ref('orders') }}
group by 1
limit 3

trim(<field_name> [, <characters_to_remove>])

select
    first_name,
    concat('*', first_name, '**') as test_string,
    trim(test_string, '*') as back_to_first_name
from {{ ref('customers') }}
limit 3

upper(<string_column>)

select 
	customer_id,
	upper(first_name) as first_name,
	last_name
from {{ ref('customers') }}

select
	order_id,
	customer_id,
	amount
from {{ ref('orders') }}
where status != 'returned'
```

In this query, you’re filtering for any order from the [Jaffle Shop’s](https://github.com/dbt-labs/jaffle_shop) `orders` model whose status is not `returned` by adding a WHERE clause after the FROM statement. You could additionally filter on string, numeric, date, or other data types to meet your query conditions.

You will likely see WHERE clauses show up 99.99% of the time in a typical query or dbt model. The other .01% is probably in a DML statement, such as DELETE or ALTER, to modify specific rows in tables.

#### SQL WHERE clause syntax in Snowflake, Databricks, BigQuery, and Redshift[​](#sql-where-clause-syntax-in-snowflake-databricks-bigquery-and-redshift "Direct link to SQL WHERE clause syntax in Snowflake, Databricks, BigQuery, and Redshift")

Since the WHERE clause is a SQL fundamental, Google BigQuery, Amazon Redshift, Snowflake, and Databricks all support the ability to filter queries and data models using it. In addition, the syntax to round is the same across all of them using the WHERE clause.

#### SQL WHERE clause use cases[​](#sql-where-clause-use-cases "Direct link to SQL WHERE clause use cases")

WHERE clauses are probably some of the most widely used SQL capabilities, right after SELECT and FROM statements. Below is a non-exhaustive list of where you’ll commonly see WHERE clauses throughout dbt projects and data work:

* Removing source-deleted rows from staging models to increase accuracy and improve downstream model performance
* Filtering out employee records from models
* Performing ad-hoc analysis on specific rows or users, either in a dbt model, BI tool, or ad-hoc query
* Paired with IN, LIKE, NOT IN clauses to create more generalized or a group of specific requirements to filter on

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### 17 docs tagged with "Metrics"

#### [About MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md)

Learn more about MetricFlow and its key concepts

### 19 docs tagged with "Quickstart"

#### [Analyze your data in dbt](https://docs.getdbt.com/guides/analyze-your-data.md)

### 2 docs tagged with "analyst"

#### [Analyze your data in dbt](https://docs.getdbt.com/guides/analyze-your-data.md)

### 2 docs tagged with "API"

#### [JDBC](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md)

Integrate and use the JDBC API to query your metrics.

### 2 docs tagged with "CI"

#### [Customizing CI/CD with custom pipelines](https://docs.getdbt.com/guides/custom-cicd-pipelines.md)

Learn the benefits of version-controlled analytics code and custom pipelines in dbt for enhanced code testing and workflow automation during the development process.

### 2 docs tagged with "dbt Fusion engine"

#### [Coalesce dbt Fusion Engine in platform Quickstart Guide](https://docs.getdbt.com/guides/coalesce-fusion-platform-qs.md)

### 2 docs tagged with "dbt Insights"

#### [Access the dbt Insights interface](https://docs.getdbt.com/docs/explore/access-dbt-insights.md)

Learn how to access the dbt Insights interface and run queries

### 2 docs tagged with "Redshift"

#### [Quickstart for dbt and Redshift](https://docs.getdbt.com/guides/redshift.md)

### 2 docs tagged with "SAO"

#### [About state-aware orchestration](https://docs.getdbt.com/docs/deploy/state-aware-about.md)

Learn about how state-aware orchestration automatically determines which models to build by detecting changes in code or data every time a job runs.

### 2 docs tagged with "Troubleshooting"

#### [Debug errors](https://docs.getdbt.com/guides/debug-errors.md)

Learn about errors and the art of debugging them.

### 20 docs tagged with "dbt Core"

#### [BigQuery configurations](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md)

Reference guide for Big Query configurations in dbt.

### 24 docs tagged with "dbt platform"

#### [Airflow and dbt](https://docs.getdbt.com/guides/airflow-and-dbt-cloud.md)

### 3 docs tagged with "APIs"

#### [GraphQL](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md)

Integrate and use the GraphQL API to query your metrics.

### 3 docs tagged with "BigQuery"

#### [BigQuery configurations](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md)

Reference guide for Big Query configurations in dbt.

### 3 docs tagged with "IDE"

#### [About the Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md)

Develop, test, run, and build in the Studio IDE. You can compile dbt code into SQL and run it against your database directly

### 3 docs tagged with "platform"

#### [Quickstart for dbt and BigQuery](https://docs.getdbt.com/guides/bigquery.md)

### 39 docs tagged with "Semantic Layer"

#### [About dbt Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md)

Learn how to query data and perform exploratory data analysis using dbt Insights

### 4 docs tagged with "dbt Fusion"

#### [BigQuery configurations](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md)

Reference guide for Big Query configurations in dbt.

### 4 docs tagged with "Orchestration"

#### [Airflow and dbt](https://docs.getdbt.com/guides/airflow-and-dbt-cloud.md)

### 5 docs tagged with "Snowflake"

#### [Leverage dbt to generate analytics and ML-ready pipelines with SQL and Python with Snowflake](https://docs.getdbt.com/guides/dbt-python-snowpark.md)

Leverage dbt to generate analytics and ML-ready pipelines with SQL and Python with Snowflake

### 6 docs tagged with "Databricks"

#### [Databricks configurations](https://docs.getdbt.com/reference/resource-configs/databricks-configs.md)

### 6 docs tagged with "Migration"

#### [Legacy dbt Semantic Layer migration guide](https://docs.getdbt.com/guides/sl-migration.md)

Learn how to migrate from the legacy dbt Semantic Layer to the latest one.

### 6 docs tagged with "Webhooks"

#### [Create Datadog events from dbt results](https://docs.getdbt.com/guides/serverless-datadog.md)

Configure a serverless app to add dbt events to Datadog logs.

### 9 docs tagged with "scheduler"

#### [About state-aware orchestration](https://docs.getdbt.com/docs/deploy/state-aware-about.md)

Learn about how state-aware orchestration automatically determines which models to build by detecting changes in code or data every time a job runs.

### One doc tagged with "Adapter creation"

#### [Build, test, document, and promote adapters](https://docs.getdbt.com/guides/adapter-creation.md)

Create an adapter that connects dbt to you platform, and learn how to maintain and version that adapter.

### One doc tagged with "Amazon"

#### [Quickstart for dbt and Amazon Athena](https://docs.getdbt.com/guides/athena.md)

### One doc tagged with "Athena"

#### [Quickstart for dbt and Amazon Athena](https://docs.getdbt.com/guides/athena.md)

### One doc tagged with "Best practices"

#### [Integrate with dbt Semantic Layer using best practices](https://docs.getdbt.com/guides/sl-partner-integration-guide.md)

Learn about partner integration guidelines, roadmap, and connectivity.

### One doc tagged with "BigFrames"

#### [Using BigQuery DataFrames with dbt Python models](https://docs.getdbt.com/guides/dbt-python-bigframes.md)

Use this guide to help you set up dbt with BigQuery DataFrames (BigFrames).

### One doc tagged with "Canvas"

#### [Quickstart for dbt Canvas](https://docs.getdbt.com/guides/canvas.md)

### One doc tagged with "Catalog"

#### [Quickstart for the dbt Catalog workshop](https://docs.getdbt.com/guides/explorer-quickstart.md)

Use this guide to build and define metrics, set up the dbt Semantic Layer, and query them using Google Sheets.

### One doc tagged with "cost savings"

#### [Navigating the state-aware interface](https://docs.getdbt.com/docs/deploy/state-aware-interface.md)

Learn how to navigate the state-aware orchestration interface for better visibility into model builds and cost tracking.

### One doc tagged with "dbt Cloud"

#### [Quickstart for the dbt Fusion engine](https://docs.getdbt.com/guides/fusion.md)

### One doc tagged with "Dremio"

#### [Build a data lakehouse with dbt Core and Dremio Cloud](https://docs.getdbt.com/guides/build-dremio-lakehouse.md)

Learn how to build a data lakehouse with dbt Core and Dremio Cloud.

### One doc tagged with "Explorer"

#### [Quickstart for the dbt Catalog workshop](https://docs.getdbt.com/guides/explorer-quickstart.md)

Use this guide to build and define metrics, set up the dbt Semantic Layer, and query them using Google Sheets.

### One doc tagged with "GCP"

#### [Using BigQuery DataFrames with dbt Python models](https://docs.getdbt.com/guides/dbt-python-bigframes.md)

Use this guide to help you set up dbt with BigQuery DataFrames (BigFrames).

### One doc tagged with "Git"

#### [How to migrate git providers](https://docs.getdbt.com/faqs/Git/git-migration.md)

Learn how to migrate git providers in dbt with minimal disruption.

### One doc tagged with "Google"

#### [Using BigQuery DataFrames with dbt Python models](https://docs.getdbt.com/guides/dbt-python-bigframes.md)

Use this guide to help you set up dbt with BigQuery DataFrames (BigFrames).

### One doc tagged with "Governance"

#### [Build your metrics](https://docs.getdbt.com/docs/build/build-metrics-intro.md)

Learn about MetricFlow and build your metrics with semantic models

### One doc tagged with "Jan-1-2020"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "Jan-1-2021"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "Jinja"

#### [Use Jinja to improve your SQL code](https://docs.getdbt.com/guides/using-jinja.md)

Learn how to improve your SQL code using Jinja.

### One doc tagged with "model"

#### [Quickstart for dbt Canvas](https://docs.getdbt.com/guides/canvas.md)

### One doc tagged with "models built"

#### [Navigating the state-aware interface](https://docs.getdbt.com/docs/deploy/state-aware-interface.md)

Learn how to navigate the state-aware orchestration interface for better visibility into model builds and cost tracking.

### One doc tagged with "SQL"

#### [Refactoring legacy SQL to dbt](https://docs.getdbt.com/guides/refactoring-legacy-sql.md)

This guide walks through refactoring a long SQL query (perhaps from a stored procedure) into modular dbt data models.

### One doc tagged with "Teradata"

#### [Quickstart for dbt and Teradata](https://docs.getdbt.com/guides/teradata.md)

### One doc tagged with "v0.5.0"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.01"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.02"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.03"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.04"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.05"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.06"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.07"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.08"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.09"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.10"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.11"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.12"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.13"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.14"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.15"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.16"

#### [Changelog 2019 and 2020](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2019-2020.md)

2019 and 2020 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.18"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.19"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.20"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.21"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.22"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.23"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.24"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.25"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.26"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.27"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.28"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.29"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.30"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.31"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.32"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.33"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.34"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.35"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.36"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.37"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.38"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.39"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.40"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "v1.1.41"

#### [Changelog 2021](https://docs.getdbt.com/docs/dbt-versions/release-notes/dbt-cloud-changelog-2021.md)

2021 Changelog for the dbt Cloud application

### One doc tagged with "Visual Editor"

#### [Quickstart for dbt Canvas](https://docs.getdbt.com/guides/canvas.md)

#### A[​](#A "Direct link to A")

* [Adapter creation1](https://docs.getdbt.com/tags/adapter-creation.md)
* [Amazon1](https://docs.getdbt.com/tags/amazon.md)
* [analyst2](https://docs.getdbt.com/tags/analyst.md)
* [API2](https://docs.getdbt.com/tags/api.md)
* [APIs3](https://docs.getdbt.com/tags/ap-is.md)
* [Athena1](https://docs.getdbt.com/tags/athena.md)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

**Examples:**

Example 1 (unknown):
```unknown
5. Commit (save) the file.
6. Delete the following folders from the dbt project root, if they exist. No data or code will be lost:
   <!-- -->
   * `target`, `dbt_modules`, `dbt_packages`, `logs`
7. Commit (save) the deleted folders.
8. Open a merge request using the git provider web interface. The merge request should attempt to merge the changes into the 'main' branch that all development branches are created from.
9. Follow the necessary procedures to get the branch approved and merged into the 'main' branch. You can delete the branch after the merge is complete.
10. Once the merge is complete, go back to the Studio IDE, and open the project that you're fixing.
11. [Rollback your repo to remote](https://docs.getdbt.com/docs/cloud/git/version-control-basics.md#the-git-button-in-the-cloud-ide) in the Studio IDE by clicking on the three dots next to the **Studio IDE Status** button on the lower right corner of the Studio IDE screen, then select **Rollback to remote**.
    <!-- -->
    * **Note** — Rollback to remote resets your repo back to an earlier clone from your remote. Any saved but uncommitted changes will be lost, so make sure you copy any modified code that you want to keep in a temporary location outside of dbt.
12. Once you rollback to remote, open the `.gitignore` file in the branch you're working in. If the new changes aren't included, you'll need to merge the latest commits from the main branch into your working branch.
13. Go to the **File Explorer** to verify the `.gitignore` file contains the correct entries and make sure the untracked files/folders in the .gitignore file are in *italics*.
14. Great job 🎉! You've configured the `.gitignore` correctly and can continue with your development!

For more info, refer to this [detailed video](https://www.loom.com/share/9b3b8e2b617f41a8bad76ec7e42dd014) for additional guidance.

How to migrate git providers

To migrate from one git provider to another, refer to the following steps to avoid minimal disruption:

1. Outside of dbt, you'll need to import your existing repository into your new provider. By default, connecting your repository in one account won't automatically disconnected it from another account.

   As an example, if you're migrating from GitHub to Azure DevOps, you'll need to import your existing repository (GitHub) into your new Git provider (Azure DevOps). For detailed steps on how to do this, refer to your Git provider's documentation (Such as [GitHub](https://docs.github.com/en/migrations/importing-source-code/using-github-importer/importing-a-repository-with-github-importer), [GitLab](https://docs.gitlab.com/ee/user/project/import/repo_by_url.html), [Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/repos/git/import-git-repository?view=azure-devops))

2. Go back to dbt and set up your [integration for the new Git provider](https://docs.getdbt.com/docs/cloud/git/git-configuration-in-dbt-cloud.md), if needed.

3. Disconnect the old repository in dbt by going to **Account Settings** and then **Projects**.

4. Click on the **Repository** link, then click **Edit** and **Disconnect**.

   [![Disconnect and reconnect your Git repository in your dbt Account settings page.](/img/docs/dbt-cloud/disconnect-repo.png?v=2 "Disconnect and reconnect your Git repository in your dbt Account settings page.")](#)Disconnect and reconnect your Git repository in your dbt Account settings page.

5. Click **Confirm Disconnect**.

6. On the same page, connect to the new Git provider repository by clicking **Configure Repository**

   * If you're using the native integration, you may need to OAuth to it.

7. That's it, you should now be connected to the new Git provider! 🎉

Note — As a tip, we recommend you refresh your page and Studio IDE before performing any actions.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

##### Connect with managed repository

Managed repositories are a great way to trial dbt without needing to create a new repository. If you don't already have a Git repository for your dbt project, you can let dbt host and manage a repository for you.

If in the future you choose to host this repository elsewhere, you can export the information from dbt at any time. Refer to [Move from a managed repository to a self-hosted repository](https://docs.getdbt.com/faqs/Git/managed-repo.md) for more information on how to do that.

info

dbt Labs recommends against using a managed repository in a production environment. You can't use Git features like pull requests, which are part of our recommended version control best practices.

To set up a project with a managed repository:

1. From your **Account settings** in dbt, select the project you want to set up with a managed repository. If the project already has a repository set up, you need to edit the repository settings and disconnect the existing repository.
2. Click **Edit** for the project.
3. Under Repository, click **Configure repository**.
4. Select **Managed**.
5. Enter a name for the repository. For example, "analytics" or "dbt-models."
6. Click **Create**.
   <!-- -->
   [![Adding a managed repository](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/managed-repo.png?v=2 "Adding a managed repository")](#)Adding a managed repository

#### Download managed repository[​](#download-managed-repository "Direct link to Download managed repository")

To download a copy of your managed repository from dbt to your local machine:

1. Use the **Project** selector on the main left-side menu to navigate to a project that's using a managed repository.
2. Click **Dashboard** from the main left-side menu.
3. From the dashboard, click **Settings**.
4. Locate the **Repository** field and click the hyperlink for the repo.
5. Below the **Deploy key** you will find the **Download repository** option. Click the button to download. If you don't see this option, you're either not assigned a [permission set](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions.md#account-permissions) with `write` access to Git repositories, or you don't have a managed repo for your project.

[![The download button for a managed repo.](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/download-managed-repo.png?v=2 "The download button for a managed repo.")](#)The download button for a managed repo.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

##### Merge conflicts

[Merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts) in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md) often occur when multiple users are simultaneously making edits to the same section in the same file. This makes it difficult for Git to decide what changes to incorporate in the final merge.

The merge conflict process provides users the ability to choose which lines of code they'd like to preserve and commit. This document will show you how to resolve merge conflicts in the Studio IDE.

#### Identify merge conflicts[​](#identify-merge-conflicts "Direct link to Identify merge conflicts")

You can experience a merge conflict in two possible ways:

* Pulling changes from your main branch when someone else has merged a conflicting change.
* Committing your changes to the same branch when someone else has already committed their change first.

The way to [resolve](#resolve-merge-conflicts) either scenario will be exactly the same.

For example, if you and a teammate make changes to the same file and commit, you will encounter a merge conflict as soon as you **Commit and sync**.

The Studio IDE will display:

* **Commit and resolve** git action bar under **Version Control** instead of **Commit** — This indicates that the Cloud Studio IDE has detected some conflicts that you need to address.
* A 2-split editor view — The left view includes your code changes and is read-only. The right view includes the additional changes, allows you to edit and marks the conflict with some flags:
```

Example 2 (unknown):
```unknown
* The file and path colored in red in the **File Catalog**, with a warning icon to highlight files that you need to resolve.
* The file name colored in red in the **Changes** section, with a warning icon.
* If you press commit without resolving the conflict, the Studio IDE will prompt a pop up box with a list which files need to be resolved.

[![Conflicting section that needs resolution will be highlighted](/img/docs/dbt-cloud/cloud-ide/merge-conflict.png?v=2 "Conflicting section that needs resolution will be highlighted")](#)Conflicting section that needs resolution will be highlighted

[![Pop up box when you commit without resolving the conflict](/img/docs/dbt-cloud/cloud-ide/commit-without-resolve.png?v=2 "Pop up box when you commit without resolving the conflict")](#)Pop up box when you commit without resolving the conflict

#### Resolve merge conflicts[​](#resolve-merge-conflicts "Direct link to Resolve merge conflicts")

You can seamlessly resolve merge conflicts that involve competing line changes in the Cloud Studio IDE.

1. In the Studio IDE, you can edit the right-side of the conflict file, choose which lines of code you'd like to preserve, and delete the rest.
   <!-- -->
   * Note: The left view editor is read-only and you cannot make changes.
2. Delete the special flags or conflict markers `<<<<<<<`, `=======`, `>>>>>>>` that highlight the merge conflict and also choose which lines of code to preserve.
3. If you have more than one merge conflict in your file, scroll down to the next set of conflict markers and repeat steps one and two to resolve your merge conflict.
4. Press **Save**. You will notice the line highlights disappear and return to a plain background. This means that you've resolved the conflict successfully.
5. Repeat this process for every file that has a merge conflict.

[![Choosing lines of code to preserve](/img/docs/dbt-cloud/cloud-ide/resolve-conflict.png?v=2 "Choosing lines of code to preserve")](#)Choosing lines of code to preserve

Edit conflict files

* If you open the conflict file under **Changes**, the file name will display something like `model.sql (last commit)` and is fully read-only and cannot be edited. <br />
* If you open the conflict file under **File Catalog**, you can edit the file in the right view.

#### Commit changes[​](#commit-changes "Direct link to Commit changes")

When you've resolved all the merge conflicts, the last step would be to commit the changes you've made.

1. Click the git action bar **Commit and resolve**.
2. The **Commit Changes** pop up box will confirm that all conflicts have been resolved. Write your commit message and click **Commit Changes**.
3. The Studio IDE will return to its normal state and you can continue developing!

[![Conflict has been resolved](/img/docs/dbt-cloud/cloud-ide/commit-resolve.png?v=2 "Conflict has been resolved")](#)Conflict has been resolved

[![Commit Changes pop up box to commit your changes](/img/docs/dbt-cloud/cloud-ide/commit-changes.png?v=2 "Commit Changes pop up box to commit your changes")](#)Commit Changes pop up box to commit your changes

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

##### PR template

#### Configure pull request (PR) template URLs[​](#configure-pull-request-pr-template-urls "Direct link to Configure pull request (PR) template URLs")

When you commit changes to a branch in the Studio IDE, dbt can prompt users to open a new Pull Request for the code changes. To enable this functionality, ensure that a PR Template URL is configured in the **Repository details** page in your **Account Settings**. If this setting is blank, the Studio IDE will prompt users to merge the changes directly into their default branch.

[![Configure a PR template in the 'Repository details' page.](/img/docs/collaborate/repo-details.jpg?v=2 "Configure a PR template in the 'Repository details' page.")](#)Configure a PR template in the 'Repository details' page.

##### PR Template URL by git provider[​](#pr-template-url-by-git-provider "Direct link to PR Template URL by git provider")

The PR Template URL setting will be automatically set for most repositories, depending on the connection method.

* If you connect to your repository via in-app integrations with your git provider or the "Git Clone" method via SSH, this URL setting will be auto-populated and editable.
  <!-- -->
  * For AWS CodeCommit, this URL setting isn't auto-populated and must be [manually configured](https://docs.getdbt.com/docs/cloud/git/import-a-project-by-git-url.md#step-5-configure-pull-request-template-urls-optional).
* If you connect via a dbt [Managed repository](https://docs.getdbt.com/docs/cloud/git/managed-repository.md), this URL will not be set, and the Studio IDE will prompt users to merge the changes directly into their default branch.

The PR template URL supports two variables that can be used to build a URL string. These variables, `{{source}}` and `{{destination}}` return branch names based on the state of the configured Environment and active branch open in the IDE. The `{{source}}` variable represents the active development branch, and the `{{destination}}` variable represents the configured base branch for the environment, eg. `master`.

A typical PR build URL looks like:

* Template
* Rendered
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
#### Example templates[​](#example-templates "Direct link to Example templates")

Some common URL templates are provided below, but please note that the exact value may vary depending on your configured git provider.

##### GitHub[​](#github "Direct link to GitHub")
```

---

## Configure the models in models/facts/ to be materialized as views

**URL:** llms-txt#configure-the-models-in-models/facts/-to-be-materialized-as-views

---

## these arguments can be projects, models, directory paths, tags, or sources

**URL:** llms-txt#these-arguments-can-be-projects,-models,-directory-paths,-tags,-or-sources

dbt run --select "tag:nightly my_model finance.base.*"

---

## Find the server PID using `ps`:

**URL:** llms-txt#find-the-server-pid-using-`ps`:

**Contents:**
  - About dbt run command
  - About dbt run-operation command
  - About dbt seed command
  - About dbt show command
  - About dbt snapshot command
  - About dbt source command

ps aux | grep 'dbt-rpc serve' | grep -v grep

dbt run --full-refresh

select * from all_events

-- if the table already exists and `--full-refresh` is
-- not set, then only add new records. otherwise, select
-- all records.
{% if is_incremental() %}
   where collector_tstamp > (
     select coalesce(max(max_tstamp), '0001-01-01') from {{ this }}
   )
{% endif %}

$ dbt run-operation {macro} --args '{args}'
  {macro}        Specify the macro to invoke. dbt will call this macro
                        with the supplied arguments and then exit
  --args ARGS           Supply arguments to the macro. This dictionary will be
                        mapped to the keyword arguments defined in the
                        selected macro. This argument should be a YAML string,
                        eg. '{my_variable: my_value}'

$ dbt seed --select "country_codes"
Found 2 models, 3 tests, 0 archives, 0 analyses, 53 macros, 0 operations, 2 seed files

14:46:15 | Concurrency: 1 threads (target='dev')
14:46:15 |
14:46:15 | 1 of 1 START seed file analytics.country_codes........................... [RUN]
14:46:15 | 1 of 1 OK loaded seed file analytics.country_codes....................... [INSERT 3 in 0.01s]
14:46:16 |
14:46:16 | Finished running 1 seed in 0.14s.

dbt show --select "model_name.sql"

dbt show --inline "select * from {{ ref('model_name') }}"

dbt show --select "stg_orders"
21:17:38 Running with dbt=1.5.0-b5
21:17:38 Found 5 models, 20 tests, 0 snapshots, 0 analyses, 425 macros, 0 operations, 3 seed files, 0 sources, 0 exposures, 0 metrics, 0 groups
21:17:38
21:17:38 Concurrency: 24 threads (target='dev')
21:17:38
21:17:38 Previewing node 'stg_orders' :
| order_id | customer_id | order_date | status    |
|----------+-------------+------------+--------   |
| 1        |           1 | 2023-01-01 | returned  |
| 2        |           3 | 2023-01-02 | completed |
| 3        |          94 | 2023-01-03 | completed |
| 4        |          50 | 2023-01-04 | completed |
| 5        |          64 | 2023-01-05 | completed |

$ dbt build -s "my_model_with_duplicates"
13:22:47 .0
...
13:22:48 Completed with 1 error and 0 warnings:
13:22:48
13:22:48 Failure in test unique_my_model_with_duplicates (models/schema.yml)
13:22:48   Got 1 result, configured to fail if not 0
13:22:48
13:22:48   compiled code at target/compiled/my_dbt_project/models/schema.yml/unique_my_model_with_duplicates_id.sql
13:22:48
13:22:48 Done. PASS=1 WARN=0 ERROR=1 SKIP=0 TOTAL=2

$ dbt show -s "unique_my_model_with_duplicates_id"
13:22:53 Running with dbt=1.5.0
13:22:53 Found 4 models, 2 tests, 0 snapshots, 0 analyses, 309 macros, 0 operations, 0 seed files, 0 sources, 0 exposures, 0 metrics, 0 groups
13:22:53
13:22:53 Concurrency: 5 threads (target='dev')
13:22:53
13:22:53 Previewing node 'unique_my_model_with_duplicates_id':
| unique_field | n_records |
| ------------ | --------- |
|            1 |         2 |

$ dbt snapshot --help
usage: dbt snapshot [-h] [--profiles-dir PROFILES_DIR]
                                     [--profile PROFILE] [--target TARGET]
                                     [--vars VARS] [--bypass-cache]
                                     [--threads THREADS]
                                     [--select SELECTOR [SELECTOR ...]]
                                     [--exclude EXCLUDE [EXCLUDE ...]]

optional arguments:
  --select SELECTOR [SELECTOR ...]
                        Specify the snapshots to include in the run.
  --exclude EXCLUDE [EXCLUDE ...]
                        Specify the snapshots to exclude in the run.

sources:
  - name: jaffle_shop
    database: raw
    config:
      freshness: # changed to config in v1.9
        warn_after: {count: 12, period: hour}
        error_after: {count: 24, period: hour}

loaded_at_field: _etl_loaded_at # changed to config in v1.10

tables:
      - name: customers

- name: orders
        config:
          freshness: 
            warn_after: {count: 6, period: hour}
            error_after: {count: 12, period: hour}
            filter: datediff('day', _etl_loaded_at, current_timestamp) < 2

- name: product_skus
        config:
          freshness: null

**Examples:**

Example 1 (unknown):
```unknown
After finding the PID for the process (eg. 12345), send a signal to the running server using the `kill` command:
```

Example 2 (unknown):
```unknown
When the server receives the HUP (hangup) signal, it will re-parse the files on disk and use the updated project code when handling subsequent requests.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt run command

#### Overview[​](#overview "Direct link to Overview")

The `dbt run` command only applies to models. It doesn't run tests, snapshots, seeds, or other resource types. To run those commands, use the appropriate dbt commands found in the [dbt commands](https://docs.getdbt.com/reference/dbt-commands.md) section — such as `dbt test`, `dbt snapshot`, or `dbt seed`. Alternatively, use `dbt build` with a [resource type selector](https://docs.getdbt.com/reference/node-selection/methods.md#resource_type).

You can use the `dbt run` command when you want to build or rebuild models in your project.

##### How does `dbt run` work?[​](#how-does-dbt-run-work "Direct link to how-does-dbt-run-work")

* `dbt run` executes compiled SQL model files against the current `target` database.
* dbt connects to the target database and runs the relevant SQL required to materialize all data models using the specified materialization strategies.
* Models are run in the order defined by the dependency graph generated during compilation. Intelligent multi-threading is used to minimize execution time without violating dependencies.
* Deploying new models frequently involves destroying prior versions of these models. In these cases, `dbt run` minimizes downtime by first building each model with a temporary name, then dropping and renaming within a single transaction (for adapters that support transactions).

#### Refresh incremental models[​](#refresh-incremental-models "Direct link to Refresh incremental models")

If you provide the `--full-refresh` flag to `dbt run`, dbt will treat incremental models as table models. This is useful when

1. The schema of an incremental model changes and you need to recreate it.
2. You want to reprocess the entirety of the incremental model because of new logic in the model code.

bash
```

Example 3 (unknown):
```unknown
You can also supply the flag by its short name: `dbt run -f`.

In the dbt compilation context, this flag will be available as [flags.FULL\_REFRESH](https://docs.getdbt.com/reference/dbt-jinja-functions/flags.md). Further, the `is_incremental()` macro will return `false` for *all* models in response when the `--full-refresh` flag is specified.

models/example.sql
```

Example 4 (unknown):
```unknown
#### Running specific models[​](#running-specific-models "Direct link to Running specific models")

dbt will also allow you select which specific models you'd like to materialize. This can be useful during special scenarios where you may prefer running a different set of models at various intervals. This can also be helpful when you may want to limit the tables materialized while you develop and test new models.

For more information, see the [Model Selection Syntax Documentation](https://docs.getdbt.com/reference/node-selection/syntax.md).

For more information on running parents or children of specific models, see the [Graph Operators Documentation](https://docs.getdbt.com/reference/node-selection/graph-operators.md).

#### Treat warnings as errors[​](#treat-warnings-as-errors "Direct link to Treat warnings as errors")

See [global configs](https://docs.getdbt.com/reference/global-configs/warnings.md)

#### Failing fast[​](#failing-fast "Direct link to Failing fast")

See [global configs](https://docs.getdbt.com/reference/global-configs/failing-fast.md)

#### Enable or Disable Colorized Logs[​](#enable-or-disable-colorized-logs "Direct link to Enable or Disable Colorized Logs")

See [global configs](https://docs.getdbt.com/reference/global-configs/print-output.md#print-color)

#### The `--empty` flag[​](#the---empty-flag "Direct link to the---empty-flag")

The `run` command supports the `--empty` flag for building schema-only dry runs. The `--empty` flag limits the refs and sources to zero rows. dbt will still execute the model SQL against the target data warehouse but will avoid expensive reads of input data. This validates dependencies and ensures your models will build properly.

#### Status codes[​](#status-codes "Direct link to Status codes")

When calling the [list\_runs api](https://docs.getdbt.com/dbt-cloud/api-v2#/operations/List%20Runs), you will get a status code for each run returned. The available run status codes are as follows:

* Queued = 1
* Starting = 2
* Running = 3
* Success = 10
* Error = 20
* Canceled = 30
* Skipped = 40

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt run-operation command

##### Overview[​](#overview "Direct link to Overview")

The `dbt run-operation` command is used to invoke a macro. For usage information, consult the docs on [operations](https://docs.getdbt.com/docs/build/hooks-operations.md#about-operations).

##### Usage[​](#usage "Direct link to Usage")
```

---

## Snapshot freshness for a particular source table:

**URL:** llms-txt#snapshot-freshness-for-a-particular-source-table:

$ dbt source freshness --select "source:snowplow.event"

{
    "meta": {
        "generated_at": "2019-02-15T00:53:03.971126Z",
        "elapsed_time": 0.21452808380126953
    },
    "sources": {
        "source.project_name.source_name.table_name": {
            "max_loaded_at": "2019-02-15T00:45:13.572836+00:00Z",
            "snapshotted_at": "2019-02-15T00:53:03.880509+00:00Z",
            "max_loaded_at_time_ago_in_s": 481.307673,
            "state": "pass",
            "criteria": {
                "warn_after": {
                    "count": 12,
                    "period": "hour"
                },
                "error_after": {
                    "count": 1,
                    "period": "day"
                }
            }
        }
    }
}

**Examples:**

Example 1 (unknown):
```unknown
##### Configuring source freshness output[​](#configuring-source-freshness-output "Direct link to Configuring source freshness output")

When `dbt source freshness` completes, a JSON file containing information about the freshness of your sources will be saved to `target/sources.json`. An example `sources.json` will look like:

target/sources.json
```

Example 2 (unknown):
```unknown
To override the destination for this `sources.json` file, use the `-o` (or `--output`) flag:
```

---

## clone all of my models from specified state to my target schema(s) and recreate all pre-existing relations in the current target

**URL:** llms-txt#clone-all-of-my-models-from-specified-state-to-my-target-schema(s)-and-recreate-all-pre-existing-relations-in-the-current-target

dbt clone --state path/to/artifacts --full-refresh

---

## reuse this manifest in subsequent commands to skip parsing

**URL:** llms-txt#reuse-this-manifest-in-subsequent-commands-to-skip-parsing

dbt = dbtRunner(manifest=manifest)
cli_args = ["run", "--select", "tag:my_tag"]
res = dbt.invoke(cli_args)

from dbt.cli.main import dbtRunner
from dbt_common.events.base_types import EventMsg

def print_version_callback(event: EventMsg):
    if event.info.name == "MainReportVersion":
        print(f"We are thrilled to be running dbt{event.data.version}")

dbt = dbtRunner(callbacks=[print_version_callback])
dbt.invoke(["list"])

from dbt.cli.main import dbtRunner
dbt = dbtRunner()

**Examples:**

Example 1 (unknown):
```unknown
##### Registering callbacks[​](#registering-callbacks "Direct link to Registering callbacks")

Register `callbacks` on dbt's `EventManager`, to access structured events and enable custom logging. The current behavior of callbacks is to block subsequent steps from proceeding; this functionality is not guaranteed in future versions.
```

Example 2 (unknown):
```unknown
##### Overriding parameters[​](#overriding-parameters "Direct link to Overriding parameters")

Pass in parameters as keyword arguments, instead of a list of CLI-style strings. At present, dbt will not do any validation or type coercion on your inputs. The subcommand must be specified, in a list, as the first positional argument.
```

---

## Then, add 'group' + 'access' modifier to specific models

**URL:** llms-txt#then,-add-'group'-+-'access'-modifier-to-specific-models

**Contents:**
  - Model contracts
  - Model notifications

models:
  # This is a public model -- it's a stable & mature interface for other teams/projects
  - name: dim_customers
    config:
      group: customer_success # changed to config in v1.10
      access: public # changed to config in v1.10
    
  # This is a private model -- it's an intermediate transformation intended for use in this context *only*
  - name: int_customer_history_rollup
    config:
      group: customer_success # changed to config in v1.10
      access: private # changed to config in v1.10
    
  # This is a protected model -- it might be useful elsewhere in *this* project,
  # but it shouldn't be exposed elsewhere
  - name: stg_customer__survey_results
    config:
      group: customer_success # changed to config in v1.10
      access: protected # changed to config in v1.10

{{ config(materialized='ephemeral') }}

models:
  - name: my_model
    config:
      access: public # changed to config in v1.10

❯ dbt parse
02:19:30  Encountered an error:
Parsing Error
  Node model.jaffle_shop.my_model with 'ephemeral' materialization has an invalid value (public) for the access field

restrict-access: True  # default is False

select
        customer_id,
        customer_name,
        -- ... many more ...
    from ...

models:
  - name: dim_customers
    config:
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: int
        constraints:
          - type: not_null
      - name: customer_name
        data_type: string
      ...

groups:
  - name: finance
    owner:
      # Email is required to receive model-level notifications, additional properties are also allowed.
      name: "Finance team"
      email: finance@dbtlabs.com
      favorite_food: donuts

- name: marketing
    owner:
      name: "Marketing team"
      email: marketing@dbtlabs.com
      favorite_food: jaffles

**Examples:**

Example 1 (unknown):
```unknown
Models with `materialized` set to `ephemeral` cannot have the access property set to public.

For example, if you have a model config set as:

models/my\_model.sql
```

Example 2 (unknown):
```unknown
And the model access is defined:

models/my\_project.yml
```

Example 3 (unknown):
```unknown
It will lead to the following error:
```

Example 4 (unknown):
```unknown
#### FAQs[​](#faqs "Direct link to FAQs")

##### How does model access relate to database permissions?[​](#how-does-model-access-relate-to-database-permissions "Direct link to How does model access relate to database permissions?")

These are different!

Specifying `access: public` on a model does not trigger dbt to automagically grant `select` on that model to every user or role in your data platform when you materialize it. You have complete control over managing database permissions on every model/schema, as makes sense to you & your organization.

Of course, dbt can facilitate this by means of [the `grants` config](https://docs.getdbt.com/reference/resource-configs/grants.md), and other flexible mechanisms. For example:

* Grant access to downstream queriers on public models
* Restrict access to private models, by revoking default/future grants, or by landing them in a different schema

As we continue to develop multi-project collaboration, `access: public` will mean that other teams are allowed to start taking a dependency on that model. This assumes that they've requested, and you've granted them access, to select from the underlying dataset.

##### How do I ref a model from another project?[​](#how-do-i-ref-a-model-from-another-project "Direct link to How do I ref a model from another project?")

You can `ref` a model from another project in two ways:

1. [Project dependency](https://docs.getdbt.com/docs/mesh/govern/project-dependencies.md): In dbt Enterprise, you can use project dependencies to `ref` a model. dbt uses a behind-the-scenes metadata service to resolve the reference, enabling efficient collaboration across teams and at scale.
2. ["Package" dependency](https://docs.getdbt.com/docs/build/packages.md): Another way to `ref` a model from another project is to treat the other project as a package dependency. This requires installing the other project as a package, including its full source code, as well as its upstream dependencies.

##### How do I restrict access to models defined in a package?[​](#how-do-i-restrict-access-to-models-defined-in-a-package "Direct link to How do I restrict access to models defined in a package?")

Source code installed from a package becomes part of your runtime environment. You can call macros and run models as if they were macros and models that you had defined in your own project.

For this reason, model access restrictions are "off" by default for models defined in packages. You can reference models from that package regardless of their `access` modifier.

The project is installed as a package can optionally restrict external `ref` access to just its public models. The package maintainer does this by setting a `restrict-access` config to `True` in `dbt_project.yml`.

By default, the value of this config is `False`. This means that:

* Models in the package with `access: protected` may be referenced by models in the root project, as if they were defined in the same project
* Models in the package with `access: private` may be referenced by models in the root project, so long as they also have the same `group` config

When `restrict-access: True`:

* Any `ref` from outside the package to a protected or private model in that package will fail.
* Only models with `access: public` can be referenced outside the package.

dbt\_project.yml
```

---

## You can also set the DBT_STATE environment variable instead of the --state flag.

**URL:** llms-txt#you-can-also-set-the-dbt_state-environment-variable-instead-of-the---state-flag.

**Contents:**
  - on_configuration_change
  - on-run-start & on-run-end
  - Oracle configurations
  - Other artifact files
  - overrides
  - packages-install-path
  - Parsing
  - persist_docs
  - Platform-specific configs
  - Platform-specific data types

dbt source freshness # must be run again to compare current to previous state
dbt build --select "source_status:fresher+" --state path/to/prod/artifacts

dbt test --select "state:new" --state path/to/artifacts      # run all tests on new models + and new tests on old models
dbt run --select "state:modified" --state path/to/artifacts  # run all models that have been modified
dbt ls --select "state:modified" --state path/to/artifacts   # list all modified nodes (not just models)

dbt run --select "tag:nightly"    # run all models with the `nightly` tag

dbt test --select "test_name:unique"            # run all instances of the `unique` test
dbt test --select "test_name:equality"          # run all instances of the `dbt_utils.equality` test
dbt test --select "test_name:range_min_max"     # run all instances of a custom schema test defined in the local project, `range_min_max`

dbt test --select "test_type:unit"           # run all unit tests
dbt test --select "test_type:data"           # run all data tests
dbt test --select "test_type:generic"        # run all generic data tests
dbt test --select "test_type:singular"       # run all singular data tests

dbt list --select "unit_test:*"                        # list all unit tests 
dbt list --select "+unit_test:orders_with_zero_items"  # list your unit test named "orders_with_zero_items" and all upstream resources

dbt list --select "version:latest"      # only 'latest' versions
dbt list --select "version:prerelease"  # versions newer than the 'latest' version
dbt list --select "version:old"         # versions older than the 'latest' version

dbt list --select "version:none"        # models that are *not* versioned

models:
  <resource-path>:
    +materialized: <materialization_name>
    +on_configuration_change: apply | continue | fail

models:
  - name: [<model-name>]
    config:
      materialized: <materialization_name>
      on_configuration_change: apply | continue | fail

{{ config(
    materialized="<materialization_name>",
    on_configuration_change="apply" | "continue" | "fail"
) }}

on-run-start: sql-statement | [sql-statement]
on-run-end: sql-statement | [sql-statement]

on-run-end:
  - "{% for schema in schemas %}grant usage on schema {{ schema }} to group reporter; {% endfor %}"

on-run-end: "{{ grant_select(schemas) }}"

sources:
  - name: <source_name>
    overrides: <package name> # deprecated in v1.10

database: ...
    schema: ...

sources:
  - name: github
    overrides: github_source # deprecated in v1.10

database: RAW
    schema: github_data

sources:
  - name: github
    overrides: github_source # deprecated in v1.10
    config:
      freshness: # changed to config in v1.9
        warn_after:
          count: 1
          period: day
        error_after:
          count: 2
          period: day

tables:
      - name: issue_assignee
        config:
          freshness:
            warn_after:
              count: 2
              period: day
            error_after:
              count: 4
              period: day

packages-install-path: directorypath

packages-install-path: packages

flags:
  partial_parse: true

dbt run --no-partial-parse

config:
  static_parser: true

models:
  <resource-path>:
    +persist_docs:
      relation: true
      columns: true

{{ config(
  persist_docs={"relation": true, "columns": true}
) }}

seeds:
  <resource-path>:
    +persist_docs:
      relation: true
      columns: true

snapshots:
  <resource-path>:
    +persist_docs:
      relation: true
      columns: true

{% snapshot snapshot_name %}

{{ config(
  persist_docs={"relation": true, "columns": true}
) }}

{{ config(materialized='table') }}

select 1 as "ca_net_ht_N" # note the use of double quotes for the column name
     
     models:
       - name: <modelname>
         description: This is the table description

columns:
       - name: "ca_net_ht_N"
         description: This should be the description of the column
         quote: true
     
     alter table analytics.<schema>.<modelname> alter
         "ca_net_ht_N" COMMENT $$This should be the description of the column$$;

models:
  - name: dim_customers
    description: One record per customer
    columns:
      - name: customer_id
        description: Primary key

models:
  +persist_docs:
    relation: true
    columns: true

unit_tests:
  - name: test_my_data_types
    model: fct_data_types
    given:
      - input: ref('stg_data_types')
        rows:
         - int_field: 1
           float_field: 2.0
           str_field: my_string
           str_escaped_field: "my,cool'string"
           date_field: 2020-01-02
           timestamp_field: 2013-11-03 00:00:00-0
           timestamptz_field: 2013-11-03 00:00:00-0
           number_field: 3
           variant_field: 3
           geometry_field: POINT(1820.12 890.56)
           geography_field: POINT(-122.35 37.55)
           object_field: {'Alberta':'Edmonton','Manitoba':'Winnipeg'}
           str_array_field: ['a','b','c']
           int_array_field: [1, 2, 3]
           binary_field: 19E1FFDCCB6CDEE788BF631C1C4905D1

unit_tests:
  - name: test_my_data_types
    model: fct_data_types
    given:
      - input: ref('stg_data_types')
        rows:
         - int_field: 1
           float_field: 2.0
           str_field: my_string
           str_escaped_field: "my,cool'string"
           date_field: 2020-01-02
           timestamp_field: 2013-11-03 00:00:00-0
           timestamptz_field: 2013-11-03 00:00:00-0
           bigint_field: 1
           geography_field: 'st_geogpoint(75, 45)'
           json_field: {"name": "Cooper", "forname": "Alice"}
           str_array_field: ['a','b','c']
           int_array_field: [1, 2, 3]
           date_array_field: ['2020-01-01']
           struct_field: 'struct("Isha" as name, 22 as age)'
           struct_of_struct_field: 'struct(struct(1 as id, "blue" as color) as my_struct)'
           struct_array_field: ['struct(st_geogpoint(75, 45) as my_point)', 'struct(st_geogpoint(75, 35) as my_point)']
           # Make sure to include all the fields in a BigQuery `struct` within the unit test.
           # It's not currently possible to use only a subset of columns in a 'struct'

unit_tests:
  - name: test_my_data_types
    model: fct_data_types
    given:
      - input: ref('stg_data_types')
        rows:
         - int_field: 1
           float_field: 2.0
           str_field: my_string
           str_escaped_field: "my,cool'string"
           date_field: 2020-01-02
           timestamp_field: 2013-11-03 00:00:00-0
           timestamptz_field: 2013-11-03 00:00:00-0
           json_field: '{"bar": "baz", "balance": 7.77, "active": false}'

unit_tests:
  - name: test_my_data_types
    model: fct_data_types
    given:
      - input: ref('stg_data_types')
        rows:
         - int_field: 1
           float_field: 2.0
           str_field: my_string
           str_escaped_field: "my,cool'string"
           bool_field: true
           date_field: 2020-01-02
           timestamp_field: 2013-11-03 00:00:00-0
           timestamptz_field: 2013-11-03 00:00:00-0
           int_array_field: 'array(1, 2, 3)'
           map_field: 'map("10", "t", "15", "f", "20", NULL)'
           named_struct_field: 'named_struct("a", 1, "b", 2, "c", 3)'

unit_tests:
  - name: test_my_data_types
    model: fct_data_types
    given:
      - input: ref('stg_data_types')
        rows:
         - int_field: 1
           float_field: 2.0
           numeric_field: 1
           str_field: my_string
           str_escaped_field: "my,cool'string"
           bool_field: true
           date_field: 2020-01-02
           timestamp_field: 2013-11-03 00:00:00-0
           timestamptz_field: 2013-11-03 00:00:00-0
           json_field: '{"bar": "baz", "balance": 7.77, "active": false}'

{{ config(materialized='table', unlogged=True) }}

models:
  +unlogged: true

{{ config(
    materialized = 'table',
    indexes=[
      {'columns': ['column_a'], 'type': 'hash'},
      {'columns': ['column_a', 'column_b'], 'unique': True},
    ]
)}}

create index if not exists
"3695050e025a7173586579da5b27d275"
on "my_target_database"."my_target_schema"."indexed_model" 
using hash
(column_a);

create unique index if not exists
"1bf5f4a6b48d2fd1a9b0470f754c1b0d"
on "my_target_database"."my_target_schema"."indexed_model" 
(column_a, column_b);

models:
  project_name:
    subdirectory:
      +indexes:
        - columns: ['column_a']
          type: hash

models:
  <resource-path>:
    +materialized: materialized_view
    +on_configuration_change: apply | continue | fail
    +indexes:
      - columns: [<column-name>]
        unique: true | false
        type: hash | btree

models:
  - name: [<model-name>]
    config:
      materialized: materialized_view
      on_configuration_change: apply | continue | fail
      indexes:
        - columns: [<column-name>]
          unique: true | false
          type: hash | btree

{{ config(
    materialized="materialized_view",
    on_configuration_change="apply" | "continue" | "fail",
    indexes=[
        {
            "columns": ["<column-name>"],
            "unique": true | false,
            "type": "hash" | "btree",
        }
    ]
) }}

grant connect on database database_name to user_name;

-- Grant read permissions on the source schema
grant usage on schema source_schema to user_name;
grant select on all tables in schema source_schema to user_name;
alter default privileges in schema source_schema grant select on tables to user_name;

-- Create destination schema and make user_name the owner
create schema if not exists destination_schema;
alter schema destination_schema owner to user_name;

-- Grant write permissions on the destination schema
grant usage on schema destination_schema to user_name;
grant create on schema destination_schema to user_name;
grant insert, update, delete, truncate on all tables in schema destination_schema to user_name;
alter default privileges in schema destination_schema grant insert, update, delete, truncate on tables to user_name;

models:
  <resource-path>:
    +pre-hook: SQL-statement | [SQL-statement]
    +post-hook: SQL-statement | [SQL-statement]

{{ config(
    pre_hook="SQL-statement" | ["SQL-statement"],
    post_hook="SQL-statement" | ["SQL-statement"],
) }}

models:
  - name: [<model_name>]
    config:
      pre_hook: <sql-statement> | [<sql-statement>]
      post_hook: <sql-statement> | [<sql-statement>]

seeds:
  <resource-path>:
    +pre-hook: SQL-statement | [SQL-statement]
    +post-hook: SQL-statement | [SQL-statement]

seeds:
  - name: [<seed_name>]
    config:
      pre_hook: <sql-statement> | [<sql-statement>]
      post_hook: <sql-statement> | [<sql-statement>]

snapshots:
  <resource-path>:
    +pre-hook: SQL-statement | [SQL-statement]
    +post-hook: SQL-statement | [SQL-statement]

snapshots:
  - name: [<snapshot_name>]
    config:
      pre_hook: <sql-statement> | [<sql-statement>]
      post_hook: <sql-statement> | [<sql-statement>]

{{ config(
    pre_hook = [
        "alter external table {{ source('sys', 'customers').render() }} refresh"
    ]
) }}

{{ config(
  post_hook = "unload ('select from {{ this }}') to 's3:/bucket_name/{{ this }}"
) }}

models:
  jaffle_shop: # this is the project name
    marts:
      finance:
        +post-hook:
          # this can be a list
          - "analyze table {{ this }} compute statistics for all columns"
          # or call a macro instead
          - "{{ analyze_table() }}"

{{
  config(
    pre_hook=before_begin("SQL-statement"),
    post_hook=after_commit("SQL-statement")
  )
}}

{{
  config(
    pre_hook={
      "sql": "SQL-statement",
      "transaction": False
    },
    post_hook={
      "sql": "SQL-statement",
      "transaction": False
    }
  )
}}

models:
  +pre-hook:
    sql: "SQL-statement"
    transaction: false
  +post-hook:
    sql: "SQL-statement"
    transaction: false

config:
  printer_width: 120

config:
  use_colors: False

dbt run --use-colors
dbt run --no-use-colors

config:
  use_colors_file: False

dbt run --use-colors-file
dbt run --no-use-colors-file

from dbt.cli.main import dbtRunner, dbtRunnerResult

**Examples:**

Example 1 (unknown):
```unknown
##### state[​](#state "Direct link to state")

**N.B.** [State-based selection](https://docs.getdbt.com/reference/node-selection/state-selection.md) is a powerful, complex feature. Read about [known caveats and limitations](https://docs.getdbt.com/reference/node-selection/state-comparison-caveats.md) to state comparison.

The `state` method is used to select nodes by comparing them against a previous version of the same project, which is represented by a [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json.md). The file path of the comparison manifest *must* be specified via the `--state` flag or `DBT_STATE` environment variable.

`state:new`: There is no node with the same `unique_id` in the comparison manifest

`state:modified`: All new nodes, plus any changes to existing nodes.
```

Example 2 (unknown):
```unknown
Because state comparison is complex, and everyone's project is different, dbt supports subselectors that include a subset of the full `modified` criteria:

* `state:modified.body`: Changes to node body (e.g. model SQL, seed values)
* `state:modified.configs`: Changes to any node configs, excluding `database`/`schema`/`alias`
* `state:modified.relation`: Changes to `database`/`schema`/`alias` (the database representation of this node), irrespective of `target` values or `generate_x_name` macros
* `state:modified.persisted_descriptions`: Changes to relation- or column-level `description`, *if and only if* `persist_docs` is enabled at each level
* `state:modified.macros`: Changes to upstream macros (whether called directly or indirectly by another macro)
* `state:modified.contract`: Changes to a model's [contract](https://docs.getdbt.com/reference/resource-configs/contract.md), which currently include the `name` and `data_type` of `columns`. Removing or changing the type of an existing column is considered a breaking change, and will raise an error.

Remember that `state:modified` includes *all* of the criteria above, as well as some extra resource-specific criteria, such as modifying a source's `freshness` or `quoting` rules or an exposure's `maturity` property. (View the source code for the full set of checks used when comparing [sources](https://github.com/dbt-labs/dbt-core/blob/9e796671dd55d4781284d36c035d1db19641cd80/core/dbt/contracts/graph/parsed.py#L660-L681), [exposures](https://github.com/dbt-labs/dbt-core/blob/9e796671dd55d4781284d36c035d1db19641cd80/core/dbt/contracts/graph/parsed.py#L768-L783), and [executable nodes](https://github.com/dbt-labs/dbt-core/blob/9e796671dd55d4781284d36c035d1db19641cd80/core/dbt/contracts/graph/parsed.py#L319-L330).)

There are two additional `state` selectors that complement `state:new` and `state:modified` by representing the inverse of those functions:

* `state:old` — A node with the same `unique_id` exists in the comparison manifest
* `state:unmodified` — All existing nodes with no changes

These selectors can help you shorten run times by excluding unchanged nodes. Currently, no subselectors are available at this time, but that might change as use cases evolve.

###### `state:modified` node and reference impacts[​](#statemodified-node-and-reference-impacts "Direct link to statemodified-node-and-reference-impacts")

`state:modified` identifies any new nodes added, changes to existing nodes, and any changes made to:

* [access](https://docs.getdbt.com/reference/resource-configs/access.md) permissions
* [`deprecation_date`](https://docs.getdbt.com/reference/resource-properties/deprecation_date.md)
* [`latest_version`](https://docs.getdbt.com/reference/resource-properties/latest_version.md)

If a node changes its group, downstream references may break, potentially causing build failures.

As `group` is a config, and configs are generally included in `state:modified` detection, modifying the group name everywhere it's referenced will flag those nodes as "modified".

Depending on whether partial parsing is enabled, you will catch the breakage as part of CI workflows.

* If you change a group name everywhere it's referenced, and partial parsing is enabled, dbt may only re-parse the changed model.
* If you update a group name in all its references without partial parsing enabled, dbt will re-parse all models and identify any invalid downstream references.

An error along the lines of "there's nothing to do" can occur when you change the group name *and* something is picked up to be run via `dbt build --select state:modified`. This error will be caught at runtime so long as the CI job is selecting `state:modified+` (including downstreams).

Certain factors can affect how references are used or resolved later on, including:

* Modifying access: if permissions or access rules change, some references might stop working.
* Modifying `deprecation_date`: if a reference or model version is marked deprecated, new warnings might appear that affect how references are processed.
* Modifying `latest_version`: if there's no tie to a specific version, the reference or model will point to the latest version.
  <!-- -->
  * If a newer version is released, the reference will automatically resolve to the new version, potentially changing the behavior or output of the system that relies on it.

###### Overwrites the `manifest.json`[​](#overwrites-the-manifestjson "Direct link to overwrites-the-manifestjson")

<!-- -->

dbt overwrites the `manifest.json` file during parsing, which means when you reference `--state` from the `target/ directory`, you may encounter a warning indicating that the saved manifest wasn't found.

[![Saved manifest not found error](/img/docs/reference/saved-manifest-not-found.png?v=2 "Saved manifest not found error")](#)Saved manifest not found error

During the next job run, dbt follows a sequence of steps that lead to the issue. First, it overwrites `target/manifest.json` before it can be used for change detection. Then, when dbt tries to read `target/manifest.json` again to detect changes, it finds none because the previous state has already been overwritten/erased.

Avoid setting `--state` and `--target-path` to the same path with state-dependent features like `--defer` and `state:modified` as it can lead to non-idempotent behavior and won't work as expected.

###### Recommendation[​](#recommendation "Direct link to Recommendation")

<!-- -->

To prevent the `manifest.json` from being overwritten before dbt reads it for change detection, update your workflow using one of these methods:

* Move the `manifest.json` to a dedicated folder (for example `state/`) after dbt generates it in the `target/ folder`. This makes sure dbt references the correct saved state instead of comparing the current state with the just-overwritten version. It also avoids issues caused by setting `--state` and `--target-path` to the same location, which can lead to non-idempotent behavior.

* Write the manifest to a different `--target-path` in the build stage (where dbt would generate the `target/manifest.json`) or before it gets overwritten during job execution to avoid issues with change detection. This allows dbt to detect changes instead of comparing the current state with the just-overwritten version.

* Pass the `--no-write-json` flag: `dbt ls --no-write-json --select state:modified --state target`: during the reproduction stage.

##### tag[​](#tag "Direct link to tag")

The `tag:` method is used to select models that match a specified [tag](https://docs.getdbt.com/reference/resource-configs/tags.md).
```

Example 3 (unknown):
```unknown
##### test\_name[​](#test_name "Direct link to test_name")

The `test_name` method is used to select tests based on the name of the generic test that defines it. For more information about how generic tests are defined, read about [data tests](https://docs.getdbt.com/docs/build/data-tests.md).
```

Example 4 (unknown):
```unknown
##### The test\_type[​](#the-test_type "Direct link to The test_type")

The `test_type` method is used to select tests based on their type:

* [Unit tests](https://docs.getdbt.com/docs/build/unit-tests.md)

* [Data tests](https://docs.getdbt.com/docs/build/data-tests.md):

  <!-- -->

  * [Singular](https://docs.getdbt.com/docs/build/data-tests.md#singular-data-tests)
  * [Generic](https://docs.getdbt.com/docs/build/data-tests.md#generic-data-tests)
```

---

## Note that only one of these targets is required

**URL:** llms-txt#note-that-only-one-of-these-targets-is-required

my-bigquery-db:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: GCP_PROJECT_ID
      dataset: DBT_DATASET_NAME # You can also use "schema" here
      threads: 4 # Must be a value of 1 or greater 
      OPTIONAL_CONFIG: VALUE

my-bigquery-db:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth-secrets
      project: GCP_PROJECT_ID
      dataset: DBT_DATASET_NAME # You can also use "schema" here
      threads: 4 # Must be a value of 1 or greater
      refresh_token: TOKEN
      client_id: CLIENT_ID
      client_secret: CLIENT_SECRET
      token_uri: REDIRECT_URI
      OPTIONAL_CONFIG: VALUE

my-bigquery-db:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth-secrets
      project: GCP_PROJECT_ID
      dataset: DBT_DATASET_NAME # You can also use "schema" here
      threads: 4 # Must be a value of 1 or greater
      token: TEMPORARY_ACCESS_TOKEN # refreshed + updated by external process
      OPTIONAL_CONFIG: VALUE

my-bigquery-db:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: GCP_PROJECT_ID
      dataset: DBT_DATASET_NAME
      threads: 4 # Must be a value of 1 or greater
      keyfile: /PATH/TO/BIGQUERY/keyfile.json
      OPTIONAL_CONFIG: VALUE

my-bigquery-db:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account-json
      project: GCP_PROJECT_ID
      dataset: DBT_DATASET_NAME
      threads: 4 # Must be a value of 1 or greater
      OPTIONAL_CONFIG: VALUE

# These fields come from the service account JSON keyfile
      keyfile_json:
        type: xxx
        project_id: xxx
        private_key_id: xxx
        private_key: xxx
        client_email: xxx
        client_id: xxx
        auth_uri: xxx
        token_uri: xxx
        auth_provider_x509_cert_url: xxx
        client_x509_cert_url: xxx

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      priority: interactive

Operation did not complete within the designated timeout.

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      job_execution_timeout_seconds: 600 # 10 minutes

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      job_creation_timeout_seconds: 30
      job_execution_timeout_seconds: 600
      job_retries: 5
      job_retry_deadline_seconds: 1200

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      location: US # Optional, one of US or EU, or a regional location

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      # If a query would bill more than a gigabyte of data, then
      # BigQuery will reject the query
      maximum_bytes_billed: 1000000000

Database Error in model debug_table (models/debug_table.sql)
  Query exceeded limit for bytes billed: 1000000000. 2000000000 or higher required.
  compiled SQL at target/run/bq_project/models/debug_table.sql

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      scopes:
        - https://www.googleapis.com/auth/bigquery

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      impersonate_service_account: dbt-runner@yourproject.iam.gserviceaccount.com

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      execution_project: buck-stops-here-456

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      quota_project: my-bq-quota-project

my-profile:
  target: dev
  outputs:
    dev:
      compute_region: us-central1
      dataset: my_dataset
      gcs_bucket: dbt-python
      job_execution_timeout_seconds: 300
      job_retries: 1
      location: US
      method: oauth
      priority: interactive
      project: abc-123
      threads: 1
      type: bigquery

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      
      # for dbt Python models to be run on a Dataproc cluster
      gcs_bucket: dbt-python
      dataproc_cluster_name: dbt-python
      dataproc_region: us-central1

my-profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: oauth
      project: abc-123
      dataset: my_dataset
      
      # for dbt Python models to be run on Dataproc Serverless
      gcs_bucket: dbt-python
      dataproc_region: us-central1
      submission_method: serverless
      dataproc_batch:
        batch_id: MY_CUSTOM_BATCH_ID # Supported in v1.7+
        environment_config:
          execution_config:
            service_account: dbt@abc-123.iam.gserviceaccount.com
            subnetwork_uri: regions/us-central1/subnetworks/dataproc-dbt
        labels:
          project: my-project
          role: dev
        runtime_config:
          properties:
            spark.executor.instances: "3"
            spark.driver.memory: 1g

gcloud auth application-default login \           
  --scopes=https://www.googleapis.com/auth/bigquery,\
https://www.googleapis.com/auth/drive.readonly,\
https://www.googleapis.com/auth/iam.test,\
https://www.googleapis.com/auth/cloud-platform

clickhouse-service:
  target: dev
  outputs:
    dev:
      type: clickhouse
      schema: [ default ]  # ClickHouse database for dbt models

# optional
      host: [ <your-clickhouse-host> ]  # Your clickhouse cluster url for example, abc123.clickhouse.cloud. Defaults to `localhost`.
      port: [ 8123 ]  # Defaults to 8123, 8443, 9000, 9440 depending on the secure and driver settings 
      user: [ default ]  # User for all database operations
      password: [ <empty string> ]  # Password for the user
      secure: [ False ]  # Use TLS (native protocol) or HTTPS (http protocol)

dbt init project_name

profile: 'clickhouse-service'

your_profile_name:
  target: dev
  outputs:
    dev:
      type: hive
      host: localhost
      port: PORT # default value: 10000
      schema: SCHEMA_NAME

your_profile_name:
  target: dev
  outputs:
    dev:
     type: hive
     host: HOST_NAME
     http_path: YOUR/HTTP/PATH # optional, http path to Hive default value: None
     port: PORT # default value: 10000
     auth_type: ldap
     use_http_transport: BOOLEAN # default value: true
     use_ssl: BOOLEAN # TLS should always be used with LDAP to ensure secure transmission of credentials, default value: true
     user: USERNAME
     password: PASSWORD
     schema: SCHEMA_NAME

your_profile_name:
  target: dev
  outputs:
    dev:
      type: hive
      host: HOSTNAME
      port: PORT # default value: 10000
      auth_type: GSSAPI
      kerberos_service_name: KERBEROS_SERVICE_NAME # default value: None
      use_http_transport: BOOLEAN # default value: true
      use_ssl: BOOLEAN # TLS should always be used to ensure secure transmission of credentials, default value: true
      schema: SCHEMA_NAME

python -m pip install dbt-hive

your_profile_name:
  target: dev
  outputs:
    dev:
      type: impala
      host: [host] # default value: localhost
      port: [port] # default value: 21050
      dbname: [db name]  # this should be same as schema name provided below, starting with 1.1.2 this parameter is optional
      schema: [schema name]

your_profile_name:
  target: dev
  outputs:
    dev:
     type: impala
     host: [host name]
     http_path: [optional, http path to Impala]
     port: [port] # default value: 21050
     auth_type: ldap
     use_http_transport: [true / false] # default value: true
     use_ssl: [true / false] # TLS should always be used with LDAP to ensure secure transmission of credentials, default value: true
     user: [username]
     password: [password]
     dbname: [db name]  # this should be same as schema name provided below, starting with 1.1.2 this parameter is optional
     schema: [schema name]
     retries: [retries] # number of times Impala attempts retry connection to warehouse, default value: 3

your_profile_name:
  target: dev
  outputs:
    dev:
      type: impala
      host: [hostname]
      port: [port] # default value: 21050
      auth_type: [GSSAPI]
      kerberos_service_name: [kerberos service name] # default value: None
      use_http_transport: true # default value: true
      use_ssl: true # TLS should always be used with LDAP to ensure secure transmission of credentials, default value: true
      dbname: [db name]  # this should be same as schema name provided below, starting with 1.1.2 this parameter is optional
      schema: [schema name]
      retries: [retries] # number of times Impala attempts retry connection to warehouse, default value: 3

**Examples:**

Example 1 (unknown):
```unknown
**Default project**

If you do not specify a `project`/`database` and are using the `oauth` method, dbt will use the default `project` associated with your user, as defined by `gcloud config set`.

##### OAuth Token-Based[​](#oauth-token-based "Direct link to OAuth Token-Based")

See [docs](https://developers.google.com/identity/protocols/oauth2) on using OAuth 2.0 to access Google APIs.

###### Refresh token[​](#refresh-token "Direct link to Refresh token")

Using the refresh token and client information, dbt will mint new access tokens as necessary.

\~/.dbt/profiles.yml
```

Example 2 (unknown):
```unknown
###### Temporary token[​](#temporary-token "Direct link to Temporary token")

dbt will use the one-time access token, no questions asked. This approach makes sense if you have an external deployment process that can mint new access tokens and update the profile file accordingly.

\~/.dbt/profiles.yml
```

Example 3 (unknown):
```unknown
##### Service Account File[​](#service-account-file "Direct link to Service Account File")

\~/.dbt/profiles.yml
```

Example 4 (unknown):
```unknown
##### Service Account JSON[​](#service-account-json "Direct link to Service Account JSON")

Note

This authentication method is only recommended for production environments where using a Service Account Keyfile is impractical.

\~/.dbt/profiles.yml
```

---

## This filter says only run this job when there is a push to the main branch

**URL:** llms-txt#this-filter-says-only-run-this-job-when-there-is-a-push-to-the-main-branch

---

## Previously, attempting to access a configuration value like this would result in None

**URL:** llms-txt#previously,-attempting-to-access-a-configuration-value-like-this-would-result-in-none

print(f"{dbt.config.get('my_var')}")  # Output before change: None

---

## details on linter rules: https://docs.sqlfluff.com/en/stable/rules.html

**URL:** llms-txt#details-on-linter-rules:-https://docs.sqlfluff.com/en/stable/rules.html

**Contents:**
  - Integrate with dbt Semantic Layer using best practices
  - Legacy dbt Semantic Layer migration guide
  - Leverage dbt to generate analytics and ML-ready pipelines with SQL and Python with Snowflake
  - Migrate from dbt-spark to dbt-databricks
  - Migrate from DDL, DML, and stored procedures
  - Move from dbt Core to the dbt platform: Get started
  - Move from dbt Core to the dbt platform: Optimization tips
  - Move from dbt Core to the dbt platform: What you need to know
  - Optimize and troubleshoot dbt models on Databricks
  - Post to Microsoft Teams when a job finishes

lint-project:
  stage: pre-build
  rules:
    - if: $CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH != 'main'
  script:
    - python -m pip install sqlfluff
    - sqlfluff lint models --dialect snowflake

my_awesome_project
├── bitbucket-pipelines.yml
├── dbt_project.yml

pipelines:
  branches:
    '**': # this sets a wildcard to run on every branch
      - step:
          name: Lint dbt project
          script:
            - python -m pip install sqlfluff==0.13.1
            - sqlfluff lint models --dialect snowflake --rules L019,L020,L021,L022

'main': # override if your default branch doesn't run on a branch named "main"
      - step:
          script:
            - python --version

python -m pip install "dbt-metricflow[snowflake]"
   
   mf query --metrics revenue --group-by metric_time
   
   mf query --metrics orders,revenue --group-by metric_time__month,customer_type --explain
   
   select * 
   from {{ metrics.calculate(  
   [metric('orders)',
   metric('revenue)'],
       grain='week',
       dimensions=['metric_time', 'customer_type'],
   ) }}
   
   create or replace warehouse COMPUTE_WH with warehouse_size=XSMALL
   
   -- create and define our formula1 database
   create or replace database formula1;
   use database formula1; 
   create or replace schema raw; 
   use schema raw;

-- define our file format for reading in the CSVs 
   create or replace file format CSVformat
   type = CSV
   field_delimiter =','
   field_optionally_enclosed_by = '"', 
   skip_header=1;

--
   create or replace stage formula1_stage
   file_format = CSVformat 
   url = 's3://formula1-dbt-cloud-python-demo/formula1-kaggle-data/';

-- load in the 8 tables we need for our demo 
   -- we are first creating the table then copying our data in from s3
   -- think of this as an empty container or shell that we are then filling
   create or replace table formula1.raw.circuits (
       CIRCUITID NUMBER(38,0),
       CIRCUITREF VARCHAR(16777216),
       NAME VARCHAR(16777216),
       LOCATION VARCHAR(16777216),
       COUNTRY VARCHAR(16777216),
       LAT FLOAT,
       LNG FLOAT,
       ALT NUMBER(38,0),
       URL VARCHAR(16777216)
   );
   -- copy our data from public s3 bucket into our tables 
   copy into circuits 
   from @formula1_stage/circuits.csv
   on_error='continue';

create or replace table formula1.raw.constructors (
       CONSTRUCTORID NUMBER(38,0),
       CONSTRUCTORREF VARCHAR(16777216),
       NAME VARCHAR(16777216),
       NATIONALITY VARCHAR(16777216),
       URL VARCHAR(16777216)
   );
   copy into constructors 
   from @formula1_stage/constructors.csv
   on_error='continue';

create or replace table formula1.raw.drivers (
       DRIVERID NUMBER(38,0),
       DRIVERREF VARCHAR(16777216),
       NUMBER VARCHAR(16777216),
       CODE VARCHAR(16777216),
       FORENAME VARCHAR(16777216),
       SURNAME VARCHAR(16777216),
       DOB DATE,
       NATIONALITY VARCHAR(16777216),
       URL VARCHAR(16777216)
   );
   copy into drivers 
   from @formula1_stage/drivers.csv
   on_error='continue';

create or replace table formula1.raw.lap_times (
       RACEID NUMBER(38,0),
       DRIVERID NUMBER(38,0),
       LAP NUMBER(38,0),
       POSITION FLOAT,
       TIME VARCHAR(16777216),
       MILLISECONDS NUMBER(38,0)
   );
   copy into lap_times 
   from @formula1_stage/lap_times.csv
   on_error='continue';

create or replace table formula1.raw.pit_stops (
       RACEID NUMBER(38,0),
       DRIVERID NUMBER(38,0),
       STOP NUMBER(38,0),
       LAP NUMBER(38,0),
       TIME VARCHAR(16777216),
       DURATION VARCHAR(16777216),
       MILLISECONDS NUMBER(38,0)
   );
   copy into pit_stops 
   from @formula1_stage/pit_stops.csv
   on_error='continue';

create or replace table formula1.raw.races (
       RACEID NUMBER(38,0),
       YEAR NUMBER(38,0),
       ROUND NUMBER(38,0),
       CIRCUITID NUMBER(38,0),
       NAME VARCHAR(16777216),
       DATE DATE,
       TIME VARCHAR(16777216),
       URL VARCHAR(16777216),
       FP1_DATE VARCHAR(16777216),
       FP1_TIME VARCHAR(16777216),
       FP2_DATE VARCHAR(16777216),
       FP2_TIME VARCHAR(16777216),
       FP3_DATE VARCHAR(16777216),
       FP3_TIME VARCHAR(16777216),
       QUALI_DATE VARCHAR(16777216),
       QUALI_TIME VARCHAR(16777216),
       SPRINT_DATE VARCHAR(16777216),
       SPRINT_TIME VARCHAR(16777216)
   );
   copy into races 
   from @formula1_stage/races.csv
   on_error='continue';

create or replace table formula1.raw.results (
       RESULTID NUMBER(38,0),
       RACEID NUMBER(38,0),
       DRIVERID NUMBER(38,0),
       CONSTRUCTORID NUMBER(38,0),
       NUMBER NUMBER(38,0),
       GRID NUMBER(38,0),
       POSITION FLOAT,
       POSITIONTEXT VARCHAR(16777216),
       POSITIONORDER NUMBER(38,0),
       POINTS NUMBER(38,0),
       LAPS NUMBER(38,0),
       TIME VARCHAR(16777216),
       MILLISECONDS NUMBER(38,0),
       FASTESTLAP NUMBER(38,0),
       RANK NUMBER(38,0),
       FASTESTLAPTIME VARCHAR(16777216),
       FASTESTLAPSPEED FLOAT,
       STATUSID NUMBER(38,0)
   );
   copy into results 
   from @formula1_stage/results.csv
   on_error='continue';

create or replace table formula1.raw.status (
       STATUSID NUMBER(38,0),
       STATUS VARCHAR(16777216)
   );
   copy into status 
   from @formula1_stage/status.csv
   on_error='continue';
   
      select * from formula1.raw.circuits
      
   # Name your project! Project names should contain only lowercase characters
   # and underscores. A good package name should reflect your organization's
   # name or the intended use of these models
   name: 'snowflake_dbt_python_formula1'
   version: '1.3.0'
   require-dbt-version: '>=1.3.0'
   config-version: 2

# This setting configures which "profile" dbt uses for this project.
   profile: 'default'

# These configurations specify where dbt should look for different types of files.
   # The `model-paths` config, for example, states that models in this project can be
   # found in the "models/" directory. You probably won't need to change these!
   model-paths: ["models"]
   analysis-paths: ["analyses"]
   test-paths: ["tests"]
   seed-paths: ["seeds"]
   macro-paths: ["macros"]
   snapshot-paths: ["snapshots"]

target-path: "target"  # directory which will store compiled SQL files
   clean-targets:         # directories to be removed by `dbt clean`
    - "target"
    - "dbt_packages"

models:
    snowflake_dbt_python_formula1:
      staging:

+docs:
      node_color: "CadetBlue"
    marts:
     +materialized: table
     aggregates:
      +docs:
        node_color: "Maroon"
      +tags: "bi"

core:
      +docs:
        node_color: "#800080"
    intermediate:
      +docs:
        node_color: "MediumSlateBlue"
    ml:
      prep:
        +docs:
          node_color: "Indigo"
      train_predict:
        +docs:
          node_color: "#36454f"
   
   marts:     
     +materialized: table
   
version: 2

sources:
  - name: formula1
    description: formula 1 datasets with normalized tables 
    database: formula1 
    schema: raw
    tables:
      - name: circuits
        description: One record per circuit, which is the specific race course. 
        columns:
          - name: circuitid
            data_tests:
            - unique
            - not_null
      - name: constructors 
        description: One record per constructor. Constructors are the teams that build their formula 1 cars. 
        columns:
          - name: constructorid
            data_tests:
            - unique
            - not_null
      - name: drivers
        description: One record per driver. This table gives details about the driver. 
        columns:
          - name: driverid
            data_tests:
            - unique
            - not_null
      - name: lap_times
        description: One row per lap in each race. Lap times started being recorded in this dataset in 1984 and joined through driver_id.
      - name: pit_stops 
        description: One row per pit stop. Pit stops do not have their own id column, the combination of the race_id and driver_id identify the pit stop.
        columns:
          - name: stop
            data_tests:
              - accepted_values:
                    arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                        values: [1,2,3,4,5,6,7,8]
                        quote: false            
      - name: races 
        description: One race per row. Importantly this table contains the race year to understand trends. 
        columns:
          - name: raceid
            data_tests:
            - unique
            - not_null        
      - name: results
        columns:
          - name: resultid
            data_tests:
            - unique
            - not_null   
        description: One row per result. The main table that we join out for grid and position variables.
      - name: status
        description: One status per row. The status contextualizes whether the race was finished or what issues arose e.g. collisions, engine, etc. 
        columns:
          - name: statusid
            data_tests:
            - unique
            - not_null

select * from {{ source('formula1','circuits') }}

renamed as (
       select
           circuitid as circuit_id,
           circuitref as circuit_ref,
           name as circuit_name,
           location,
           country,
           lat as latitude,
           lng as longitude,
           alt as altitude
           -- omit the url
       from source
   )
   select * from renamed
   
   with

select * from {{ source('formula1','constructors') }}

renamed as (
       select
           constructorid as constructor_id,
           constructorref as constructor_ref,
           name as constructor_name,
           nationality as constructor_nationality
           -- omit the url
       from source
   )

select * from renamed
   
   with

select * from {{ source('formula1','drivers') }}

renamed as (
       select
           driverid as driver_id,
           driverref as driver_ref,
           number as driver_number,
           code as driver_code,
           forename,
           surname,
           dob as date_of_birth,
           nationality as driver_nationality
           -- omit the url
       from source
   )

select * from renamed
   
   with

select * from {{ source('formula1','lap_times') }}

renamed as (
       select
           raceid as race_id,
           driverid as driver_id,
           lap,
           position,
           time as lap_time_formatted,
           milliseconds as lap_time_milliseconds
       from source
   )

select * from renamed
   
   with

select * from {{ source('formula1','pit_stops') }}

renamed as (
       select
           raceid as race_id,
           driverid as driver_id,
           stop as stop_number,
           lap,
           time as lap_time_formatted,
           duration as pit_stop_duration_seconds,
           milliseconds as pit_stop_milliseconds
       from source
   )

select * from renamed
   order by pit_stop_duration_seconds desc
   
   with

select * from {{ source('formula1','races') }}

renamed as (
       select
           raceid as race_id,
           year as race_year,
           round as race_round,
           circuitid as circuit_id,
           name as circuit_name,
           date as race_date,
           to_time(time) as race_time,
           -- omit the url
           fp1_date as free_practice_1_date,
           fp1_time as free_practice_1_time,
           fp2_date as free_practice_2_date,
           fp2_time as free_practice_2_time,
           fp3_date as free_practice_3_date,
           fp3_time as free_practice_3_time,
           quali_date as qualifying_date,
           quali_time as qualifying_time,
           sprint_date,
           sprint_time
       from source
   )

select * from renamed
   
   with

select * from {{ source('formula1','results') }}

renamed as (
       select
           resultid as result_id,
           raceid as race_id,
           driverid as driver_id,
           constructorid as constructor_id,
           number as driver_number,
           grid,
           position::int as position,
           positiontext as position_text,
           positionorder as position_order,
           points,
           laps,
           time as results_time_formatted,
           milliseconds as results_milliseconds,
           fastestlap as fastest_lap,
           rank as results_rank,
           fastestlaptime as fastest_lap_time_formatted,
           fastestlapspeed::decimal(6,3) as fastest_lap_speed,
           statusid as status_id
       from source
   )

select * from renamed
   
   with

select * from {{ source('formula1','status') }}

renamed as (
       select
           statusid as status_id,
           status
       from source
   )

select * from renamed
   
   with lap_times as (

select * from {{ ref('stg_f1_lap_times') }}

select * from {{ ref('stg_f1_races') }}

expanded_lap_times_by_year as (
       select
           lap_times.race_id,
           driver_id,
           race_year,
           lap,
           lap_time_milliseconds
       from lap_times
       left join races
           on lap_times.race_id = races.race_id
       where lap_time_milliseconds is not null
   )

select * from expanded_lap_times_by_year
   
   with stg_f1__pit_stops as
   (
       select * from {{ ref('stg_f1_pit_stops') }}
   ),

pit_stops_per_race as (
       select
           race_id,
           driver_id,
           stop_number,
           lap,
           lap_time_formatted,
           pit_stop_duration_seconds,
           pit_stop_milliseconds,
           max(stop_number) over (partition by race_id,driver_id) as total_pit_stops_per_race
       from stg_f1__pit_stops
   )

select * from pit_stops_per_race
   
   with results as (

select * from {{ ref('stg_f1_results') }}

select * from {{ ref('stg_f1_races') }}

select * from {{ ref('stg_f1_drivers') }}

select * from {{ ref('stg_f1_constructors') }}
   ),

select * from {{ ref('stg_f1_status') }}
   ),

int_results as (
       select
           result_id,
           results.race_id,
           race_year,
           race_round,
           circuit_id,
           circuit_name,
           race_date,
           race_time,
           results.driver_id,
           results.driver_number,
           forename ||' '|| surname as driver,
           cast(datediff('year', date_of_birth, race_date) as int) as drivers_age_years,
           driver_nationality,
           results.constructor_id,
           constructor_name,
           constructor_nationality,
           grid,
           position,
           position_text,
           position_order,
           points,
           laps,
           results_time_formatted,
           results_milliseconds,
           fastest_lap,
           results_rank,
           fastest_lap_time_formatted,
           fastest_lap_speed,
           results.status_id,
           status,
           case when position is null then 1 else 0 end as dnf_flag
       from results
       left join races
           on results.race_id=races.race_id
       left join drivers
           on results.driver_id = drivers.driver_id
       left join constructors
           on results.constructor_id = constructors.constructor_id
       left join status
           on results.status_id = status.status_id
   )

select * from int_results
   
   # the intent of this .md is to allow for multi-line long form explanations for our intermediate transformations

# below are descriptions 
   {% docs int_results %} In this query we want to join out other important information about the race results to have a human readable table about results, races, drivers, constructors, and status. 
   We will have 4 left joins onto our results table. {% enddocs %}

{% docs int_pit_stops %} There are many pit stops within one race, aka a M:1 relationship. 
   We want to aggregate this so we can properly join pit stop information without creating a fanout.  {% enddocs %}

{% docs int_lap_times_years %} Lap times are done per lap. We need to join them out to the race year to understand yearly lap time trends. {% enddocs %}
   
   version: 2

models:
    - name: int_results
      description: '{{ doc("int_results") }}'
    - name: int_pit_stops
      description: '{{ doc("int_pit_stops") }}'
    - name: int_lap_times_years
      description: '{{ doc("int_lap_times_years") }}'
   
   with int_results as (

select * from {{ ref('int_results') }}

int_pit_stops as (
       select
           race_id,
           driver_id,
           max(total_pit_stops_per_race) as total_pit_stops_per_race
       from {{ ref('int_pit_stops') }}
       group by 1,2
   ),

select * from {{ ref('stg_f1_circuits') }}
   ),
   base_results as (
       select
           result_id,
           int_results.race_id,
           race_year,
           race_round,
           int_results.circuit_id,
           int_results.circuit_name,
           circuit_ref,
           location,
           country,
           latitude,
           longitude,
           altitude,
           total_pit_stops_per_race,
           race_date,
           race_time,
           int_results.driver_id,
           driver,
           driver_number,
           drivers_age_years,
           driver_nationality,
           constructor_id,
           constructor_name,
           constructor_nationality,
           grid,
           position,
           position_text,
           position_order,
           points,
           laps,
           results_time_formatted,
           results_milliseconds,
           fastest_lap,
           results_rank,
           fastest_lap_time_formatted,
           fastest_lap_speed,
           status_id,
           status,
           dnf_flag
       from int_results
       left join circuits
           on int_results.circuit_id=circuits.circuit_id
       left join int_pit_stops
           on int_results.driver_id=int_pit_stops.driver_id and int_results.race_id=int_pit_stops.race_id
   )

select * from base_results
   
   with base_results as (

select * from {{ ref('fct_results') }}

select * from {{ ref('int_pit_stops') }}

pit_stops_joined as (

select 
           base_results.race_id,
           race_year,
           base_results.driver_id,
           constructor_id,
           constructor_name,
           stop_number,
           lap, 
           lap_time_formatted,
           pit_stop_duration_seconds, 
           pit_stop_milliseconds
       from base_results
       left join pit_stops
           on base_results.race_id=pit_stops.race_id and base_results.driver_id=pit_stops.driver_id
   )
   select * from pit_stops_joined
   
   import numpy as np
   import pandas as pd

def model(dbt, session):
       # dbt configuration
       dbt.config(packages=["pandas","numpy"])

# get upstream data
       pit_stops_joined = dbt.ref("pit_stops_joined").to_pandas()

# provide year so we do not hardcode dates 
       year=2021

# describe the data
       pit_stops_joined["PIT_STOP_SECONDS"] = pit_stops_joined["PIT_STOP_MILLISECONDS"]/1000
       fastest_pit_stops = pit_stops_joined[(pit_stops_joined["RACE_YEAR"]==year)].groupby(by="CONSTRUCTOR_NAME")["PIT_STOP_SECONDS"].describe().sort_values(by='mean')
       fastest_pit_stops.reset_index(inplace=True)
       fastest_pit_stops.columns = fastest_pit_stops.columns.str.upper()
       
       return fastest_pit_stops.round(2)
   
   dbt run --select fastest_pit_stops_by_constructor
   
   select * from {{ ref('fastest_pit_stops_by_constructor') }}
   
   import pandas as pd

def model(dbt, session):
       # dbt configuration
       dbt.config(packages=["pandas"])

# get upstream data
       lap_times = dbt.ref("int_lap_times_years").to_pandas()

# describe the data
       lap_times["LAP_TIME_SECONDS"] = lap_times["LAP_TIME_MILLISECONDS"]/1000
       lap_time_trends = lap_times.groupby(by="RACE_YEAR")["LAP_TIME_SECONDS"].mean().to_frame()
       lap_time_trends.reset_index(inplace=True)
       lap_time_trends["LAP_MOVING_AVG_5_YEARS"] = lap_time_trends["LAP_TIME_SECONDS"].rolling(5).mean()
       lap_time_trends.columns = lap_time_trends.columns.str.upper()
       
       return lap_time_trends.round(1)
   
    dbt run --select lap_times_moving_avg
    
        def model(dbt, session):

# setting configuration
            dbt.config(materialized="table")
    
   import pandas as pd

def model(dbt, session):
       # dbt configuration
       dbt.config(packages=["pandas"])

# get upstream data
       fct_results = dbt.ref("fct_results").to_pandas()

# provide years so we do not hardcode dates in filter command
       start_year=2010
       end_year=2020

# describe the data for a full decade
       data =  fct_results.loc[fct_results['RACE_YEAR'].between(start_year, end_year)]

# convert string to an integer
       data['POSITION'] = data['POSITION'].astype(float)

# we cannot have nulls if we want to use total pit stops 
       data['TOTAL_PIT_STOPS_PER_RACE'] = data['TOTAL_PIT_STOPS_PER_RACE'].fillna(0)

# some of the constructors changed their name over the year so replacing old names with current name
       mapping = {'Force India': 'Racing Point', 'Sauber': 'Alfa Romeo', 'Lotus F1': 'Renault', 'Toro Rosso': 'AlphaTauri'}
       data['CONSTRUCTOR_NAME'].replace(mapping, inplace=True)

# create confidence metrics for drivers and constructors
       dnf_by_driver = data.groupby('DRIVER').sum(numeric_only=True)['DNF_FLAG']
       driver_race_entered = data.groupby('DRIVER').count()['DNF_FLAG']
       driver_dnf_ratio = (dnf_by_driver/driver_race_entered)
       driver_confidence = 1-driver_dnf_ratio
       driver_confidence_dict = dict(zip(driver_confidence.index,driver_confidence))

dnf_by_constructor = data.groupby('CONSTRUCTOR_NAME').sum(numeric_only=True)['DNF_FLAG']
       constructor_race_entered = data.groupby('CONSTRUCTOR_NAME').count()['DNF_FLAG']
       constructor_dnf_ratio = (dnf_by_constructor/constructor_race_entered)
       constructor_relaiblity = 1-constructor_dnf_ratio
       constructor_relaiblity_dict = dict(zip(constructor_relaiblity.index,constructor_relaiblity))

data['DRIVER_CONFIDENCE'] = data['DRIVER'].apply(lambda x:driver_confidence_dict[x])
       data['CONSTRUCTOR_RELAIBLITY'] = data['CONSTRUCTOR_NAME'].apply(lambda x:constructor_relaiblity_dict[x])

#removing retired drivers and constructors
       active_constructors = ['Renault', 'Williams', 'McLaren', 'Ferrari', 'Mercedes',
                           'AlphaTauri', 'Racing Point', 'Alfa Romeo', 'Red Bull',
                           'Haas F1 Team']
       active_drivers = ['Daniel Ricciardo', 'Kevin Magnussen', 'Carlos Sainz',
                       'Valtteri Bottas', 'Lance Stroll', 'George Russell',
                       'Lando Norris', 'Sebastian Vettel', 'Kimi Räikkönen',
                       'Charles Leclerc', 'Lewis Hamilton', 'Daniil Kvyat',
                       'Max Verstappen', 'Pierre Gasly', 'Alexander Albon',
                       'Sergio Pérez', 'Esteban Ocon', 'Antonio Giovinazzi',
                       'Romain Grosjean','Nicholas Latifi']

# create flags for active drivers and constructors so we can filter downstream              
       data['ACTIVE_DRIVER'] = data['DRIVER'].apply(lambda x: int(x in active_drivers))
       data['ACTIVE_CONSTRUCTOR'] = data['CONSTRUCTOR_NAME'].apply(lambda x: int(x in active_constructors))
       
       return data
   
   dbt run --select ml_data_prep
   
   import pandas as pd
   import numpy as np
   from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
   from sklearn.linear_model import LogisticRegression

def model(dbt, session):
       # dbt configuration
       dbt.config(packages=["pandas","numpy","scikit-learn"])

# get upstream data
       data = dbt.ref("ml_data_prep").to_pandas()

# list out covariates we want to use in addition to outcome variable we are modeling - position
       covariates = data[['RACE_YEAR','CIRCUIT_NAME','GRID','CONSTRUCTOR_NAME','DRIVER','DRIVERS_AGE_YEARS','DRIVER_CONFIDENCE','CONSTRUCTOR_RELAIBLITY','TOTAL_PIT_STOPS_PER_RACE','ACTIVE_DRIVER','ACTIVE_CONSTRUCTOR', 'POSITION']]

# filter covariates on active drivers and constructors
       # use fil_cov as short for "filtered_covariates"
       fil_cov = covariates[(covariates['ACTIVE_DRIVER']==1)&(covariates['ACTIVE_CONSTRUCTOR']==1)]

# Encode categorical variables using LabelEncoder
       # TODO: we'll update this to both ohe in the future for non-ordinal variables! 
       le = LabelEncoder()
       fil_cov['CIRCUIT_NAME'] = le.fit_transform(fil_cov['CIRCUIT_NAME'])
       fil_cov['CONSTRUCTOR_NAME'] = le.fit_transform(fil_cov['CONSTRUCTOR_NAME'])
       fil_cov['DRIVER'] = le.fit_transform(fil_cov['DRIVER'])
       fil_cov['TOTAL_PIT_STOPS_PER_RACE'] = le.fit_transform(fil_cov['TOTAL_PIT_STOPS_PER_RACE'])

# Simply target variable "position" to represent 3 meaningful categories in Formula1
       # 1. Podium position 2. Points for team 3. Nothing - no podium or points!
       def position_index(x):
           if x<4:
               return 1
           if x>10:
               return 3
           else :
               return 2

# we are dropping the columns that we filtered on in addition to our training variable
       encoded_data = fil_cov.drop(['ACTIVE_DRIVER','ACTIVE_CONSTRUCTOR'],axis=1))
       encoded_data['POSITION_LABEL']= encoded_data['POSITION'].apply(lambda x: position_index(x))
       encoded_data_grouped_target = encoded_data.drop(['POSITION'],axis=1))

return encoded_data_grouped_target
   
   dbt run --select covariate_encoding
   
   import pandas as pd

def model(dbt, session):

# dbt configuration
       dbt.config(packages=["pandas"], tags="train")

# get upstream data
       encoding = dbt.ref("covariate_encoding").to_pandas()

# provide years so we do not hardcode dates in filter command
       start_year=2010
       end_year=2019

# describe the data for a full decade
       train_test_dataset =  encoding.loc[encoding['RACE_YEAR'].between(start_year, end_year)]

return train_test_dataset
   
   import pandas as pd

def model(dbt, session):
       # dbt configuration
       dbt.config(packages=["pandas"], tags="predict")

# get upstream data
       encoding = dbt.ref("covariate_encoding").to_pandas()
       
       # variable for year instead of hardcoding it 
       year=2020

# filter the data based on the specified year
       hold_out_dataset =  encoding.loc[encoding['RACE_YEAR'] == year]
       
       return hold_out_dataset
   
   dbt run --select train_test_dataset hold_out_dataset_for_prediction
   
   import snowflake.snowpark.functions as F
   from sklearn.model_selection import train_test_split
   import pandas as pd
   from sklearn.metrics import confusion_matrix, balanced_accuracy_score
   import io
   from sklearn.linear_model import LogisticRegression
   from joblib import dump, load
   import joblib
   import logging
   import sys
   from joblib import dump, load

logger = logging.getLogger("mylog")

def save_file(session, model, path, dest_filename):
       input_stream = io.BytesIO()
       joblib.dump(model, input_stream)
       session._conn.upload_stream(input_stream, path, dest_filename)
       return "successfully created file: " + path

def model(dbt, session):
       dbt.config(
           packages = ['numpy','scikit-learn','pandas','numpy','joblib','cachetools'],
           materialized = "table",
           tags = "train"
       )
       # Create a stage in Snowflake to save our model file
       session.sql('create or replace stage MODELSTAGE').collect()

#session._use_scoped_temp_objects = False
       version = "1.0"
       logger.info('Model training version: ' + version)

# read in our training and testing upstream dataset
       test_train_df = dbt.ref("train_test_dataset")

#  cast snowpark df to pandas df
       test_train_pd_df = test_train_df.to_pandas()
       target_col = "POSITION_LABEL"

# split out covariate predictors, x, from our target column position_label, y.
       split_X = test_train_pd_df.drop([target_col], axis=1)
       split_y = test_train_pd_df[target_col]

# Split out our training and test data into proportions
       X_train, X_test, y_train, y_test  = train_test_split(split_X, split_y, train_size=0.7, random_state=42)
       train = [X_train, y_train]
       test = [X_test, y_test]
       # now we are only training our one model to deploy
       # we are keeping the focus on the workflows and not algorithms for this lab!
       model = LogisticRegression()

# fit the preprocessing pipeline and the model together 
       model.fit(X_train, y_train)   
       y_pred = model.predict_proba(X_test)[:,1]
       predictions = [round(value) for value in y_pred]
       balanced_accuracy =  balanced_accuracy_score(y_test, predictions)

# Save the model to a stage
       save_file(session, model, "@MODELSTAGE/driver_position_"+version, "driver_position_"+version+".joblib" )
       logger.info('Model artifact:' + "@MODELSTAGE/driver_position_"+version+".joblib")

# Take our pandas training and testing dataframes and put them back into snowpark dataframes
       snowpark_train_df = session.write_pandas(pd.concat(train, axis=1, join='inner'), "train_table", auto_create_table=True, create_temp_table=True)
       snowpark_test_df = session.write_pandas(pd.concat(test, axis=1, join='inner'), "test_table", auto_create_table=True, create_temp_table=True)

# Union our training and testing data together and add a column indicating train vs test rows
       return  snowpark_train_df.with_column("DATASET_TYPE", F.lit("train")).union(snowpark_test_df.with_column("DATASET_TYPE", F.lit("test")))
   
   dbt run --select train_test_position
   
   list @modelstage
   
   import logging
   import joblib
   import pandas as pd
   import os
   from snowflake.snowpark import types as T

DB_STAGE = 'MODELSTAGE'
   version = '1.0'
   # The name of the model file
   model_file_path = 'driver_position_'+version
   model_file_packaged = 'driver_position_'+version+'.joblib'

# This is a local directory, used for storing the various artifacts locally
   LOCAL_TEMP_DIR = f'/tmp/driver_position'
   DOWNLOAD_DIR = os.path.join(LOCAL_TEMP_DIR, 'download')
   TARGET_MODEL_DIR_PATH = os.path.join(LOCAL_TEMP_DIR, 'ml_model')
   TARGET_LIB_PATH = os.path.join(LOCAL_TEMP_DIR, 'lib')

# The feature columns that were used during model training
   # and that will be used during prediction
   FEATURE_COLS = [
           "RACE_YEAR"
           ,"CIRCUIT_NAME"
           ,"GRID"
           ,"CONSTRUCTOR_NAME"
           ,"DRIVER"
           ,"DRIVERS_AGE_YEARS"
           ,"DRIVER_CONFIDENCE"
           ,"CONSTRUCTOR_RELAIBLITY"
           ,"TOTAL_PIT_STOPS_PER_RACE"]

def register_udf_for_prediction(p_predictor ,p_session ,p_dbt):

def predict_position(p_df: T.PandasDataFrame[int, int, int, int,
                                           int, int, int, int, int]) -> T.PandasSeries[int]:
           # Snowpark currently does not set the column name in the input dataframe
           # The default col names are like 0,1,2,... Hence we need to reset the column
           # names to the features that we initially used for training.
           p_df.columns = [*FEATURE_COLS]
       
           # Perform prediction. this returns an array object
           pred_array = p_predictor.predict(p_df)
           # Convert to series
           df_predicted = pd.Series(pred_array)
           return df_predicted

# The list of packages that will be used by UDF
       udf_packages = p_dbt.config.get('packages')

predict_position_udf = p_session.udf.register(
           predict_position
           ,name=f'predict_position'
           ,packages = udf_packages
       )
       return predict_position_udf

def download_models_and_libs_from_stage(p_session):
       p_session.file.get(f'@{DB_STAGE}/{model_file_path}/{model_file_packaged}', DOWNLOAD_DIR)

def load_model(p_session):
       # Load the model and initialize the predictor
       model_fl_path = os.path.join(DOWNLOAD_DIR, model_file_packaged)
       predictor = joblib.load(model_fl_path)
       return predictor

# -------------------------------
   def model(dbt, session):
       dbt.config(
           packages = ['snowflake-snowpark-python' ,'scipy','scikit-learn' ,'pandas' ,'numpy'],
           materialized = "table",
           tags = "predict"
       )
       session._use_scoped_temp_objects = False
       download_models_and_libs_from_stage(session)
       predictor = load_model(session)
       predict_position_udf = register_udf_for_prediction(predictor, session ,dbt)

# Retrieve the data, and perform the prediction
       hold_out_df = (dbt.ref("hold_out_dataset_for_prediction")
           .select(*FEATURE_COLS)
       )

# Perform prediction.
       new_predictions_df = hold_out_df.withColumn("position_predicted"
           ,predict_position_udf(*FEATURE_COLS)
       )

return new_predictions_df
   
   dbt run --select predict_position
   
   select * from {{ ref('predict_position') }} order by position_predicted

models:
    - name: fastest_pit_stops_by_constructor
      description: Use the python .describe() method to retrieve summary statistics table about pit stops by constructor. Sort by average stop time ascending so the first row returns the fastest constructor.
      columns:
        - name: constructor_name
          description: team that makes the car
          data_tests:
            - unique

- name: lap_times_moving_avg
      description: Use the python .rolling() method to calculate the 5 year rolling average of pit stop times alongside the average for each year. 
      columns:
        - name: race_year
          description: year of the race
          data_tests:
            - relationships:
                arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                    to: ref('int_lap_times_years')
                    field: race_year

{% macro test_all_values_gte_zero(table, column) %}

select * from {{ ref(table) }} where {{ column }} < 0

{{
       config(
           enabled=true,
           severity='warn',
           tags = ['bi']
       )
   }}

{{ test_all_values_gte_zero('fastest_pit_stops_by_constructor', 'mean') }}
   
   {{
       config(
           enabled=true,
           severity='error',
           tags = ['bi']
       )
   }}

with lap_times_moving_avg as ( select * from {{ ref('lap_times_moving_avg') }} )

select *
   from lap_times_moving_avg 
   where lap_moving_avg_5_years < 0 and lap_moving_avg_5_years is not null
   
   dbt test --select fastest_pit_stops_by_constructor lap_times_moving_avg
   
dbt docs generate

your_profile_name:
  target: dev
  outputs:
    dev:
      type: spark
      method: odbc
      driver: '/opt/simba/spark/lib/64/libsparkodbc_sb64.so'
      schema: my_schema
      host: dbc-l33t-nwb.cloud.databricks.com
      endpoint: 8657cad335ae63e3
      token: [my_secret_token]

your_profile_name:
  target: dev
  outputs:
    dev:
      type: databricks
      schema: my_schema
      host:  dbc-l33t-nwb.cloud.databricks.com
      http_path: /sql/1.0/endpoints/8657cad335ae63e3
      token: [my_secret_token]

INSERT INTO returned_orders (order_id, order_date, total_return)

SELECT order_id, order_date, total FROM orders WHERE type = 'return'

SELECT
    order_id as order_id,
    order_date as order_date,
    total as total_return

FROM {{ ref('orders') }}

WHERE type = 'return'

CREATE TABLE all_customers

INSERT INTO all_customers SELECT * FROM us_customers

INSERT INTO all_customers SELECT * FROM eu_customers

SELECT * FROM {{ ref('us_customers') }}

SELECT * FROM {{ ref('eu_customers') }}

SELECT
    CASE
        WHEN total < 0 THEN 'return'
        ELSE type
    END AS type,

order_id,
    order_date

FROM {{ ref('stg_orders') }}

SELECT
    {{ dbt_utils.star(from=ref('stg_orders'), except=['type']) }},
    CASE
        WHEN total < 0 THEN 'return'
        ELSE type
    END AS type,

FROM {{ ref('stg_orders') }}

DELETE FROM stg_orders WHERE order_status IS NULL

SELECT * FROM {{ ref('stg_orders') }} WHERE order_status IS NOT NULL

SELECT
        *,
        CASE
            WHEN order_status IS NULL THEN true
            ELSE false
        END AS to_delete

FROM {{ ref('stg_orders') }}

SELECT * FROM soft_deletes WHERE to_delete = false

MERGE INTO ride_details USING (
    SELECT
        ride_id,
        subtotal,
        tip

FROM rides_to_load AS rtl

ON ride_details.ride_id = rtl.ride_id

WHEN MATCHED THEN UPDATE

SET ride_details.tip = rtl.tip

WHEN NOT MATCHED THEN INSERT (ride_id, subtotal, tip)
    VALUES (rtl.ride_id, rtl.subtotal, NVL(rtl.tip, 0, rtl.tip)
);

SELECT
        ride_id,
        subtotal,
        tip

FROM {{ ref('rides_to_load') }}

SELECT
        ride_id,
        subtotal,
        tip

SELECT
        ride_id,
        subtotal,
        NVL(tip, 0, tip)

{{
    config(
        materialized='incremental',
        unique_key='ride_id',
        incremental_strategy='merge'
    )
}}

SELECT
        ride_id,
        subtotal,
        tip,
        max(load_timestamp) as load_timestamp

FROM {{ ref('rides_to_load') }}

{% if is_incremental() %}

WHERE load_timestamp > (SELECT max(load_timestamp) FROM {{ this }})

SELECT
        ride_id,
        subtotal,
        tip,
        load_timestamp

{% if is_incremental() %}

WHERE ride_id IN (SELECT ride_id FROM {{ this }})

SELECT
        ride_id,
        subtotal,
        NVL(tip, 0, tip),
        load_timestamp

WHERE ride_id NOT IN (SELECT ride_id FROM updates)

SELECT * FROM updates UNION inserts

materialized='incremental',

zorder="column_A" | ["column_A", "column_B"]

ANALYZE TABLE mytable COMPUTE STATISTICS FOR

COLUMNS col1, col2, col3

materialized='incremental',

incremental_strategy = 'merge',

incremental_predicates = [

"dbt_internal_target.create_at >= '2023-01-01'",	"dbt_internal_source.create_at >= '2023-01-01'"],

store = StoreClient('abc123') #replace with your UUID secret
store.set('DBT_WEBHOOK_KEY', 'abc123') #replace with webhook secret
store.set('DBT_CLOUD_SERVICE_TOKEN', 'abc123') #replace with your dbt API token
`
import hashlib
import hmac
import json
import re

auth_header = input_data['auth_header']
raw_body = input_data['raw_body']

**Examples:**

Example 1 (unknown):
```unknown
Create a `bitbucket-pipelines.yml` file in your **root directory** to define the triggers for when to execute the script below. You’ll put the code below into this file.
```

Example 2 (unknown):
```unknown
**Key pieces:**

* `image: python:3.11.1` - this defines the virtual image we’re using to run the job
* `'**':` - this is used to filter when the pipeline runs. In this case we’re telling it to run on every push event, and you can see at line 12 we're creating a dummy pipeline for `main`. More information on filtering when a pipeline is run can be found in [Bitbucket's documentation](https://support.atlassian.com/bitbucket-cloud/docs/pipeline-triggers/)
* `script:` - this is how we’re telling the Bitbucket runner to execute the Python script we defined above.
```

Example 3 (unknown):
```unknown
##### 2. Commit and push your changes to make sure everything works[​](#2-commit-and-push-your-changes-to-make-sure-everything-works "Direct link to 2. Commit and push your changes to make sure everything works")

After you finish creating the YAML files, commit and push your code to trigger your pipeline for the first time. If everything goes well, you should see the pipeline in your code platform. When you click into the job you’ll get a log showing that SQLFluff was run. If your code failed linting you’ll get an error in the job with a description of what needs to be fixed. If everything passed the lint check, you’ll see a successful job run.

* GitHub
* GitLab
* Bitbucket

In your repository, click the *Actions* tab

![Image showing the GitHub action for lint on push](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAR8AAAC9CAIAAAAFlu5LAAAQp0lEQVR4Aeycg5MkSxDGz7Zt27Zt27Zt27Zt27bvv3m/3e+9iomZN9M755vNiC82srKrq7o76jeZld13ceImSGr6GTKZjC6TyegymYwuk8lkdJlMRpfJZHSZTKaIp8tkMrpMJqPLZDIZXSaT0WUyGV3JUqVHsmvWazJk5ISESVJix0IlTpaGRxE/UfJfMBezMBcz2gKNWLqy5cr/9O1XlDZD1qQp0j558wV74PCxsfNJ3X36ltvv2W/IL5hr4LCxzHX78WtboBFLV/bcBRxdNC/efPj49ecqNep5Dnr60i3WYtdeA7AjRvefv/t1dA2PZXQZXSiGedGdJ284a/iYyUZXjGR0GV2Xbz8iItVp0Az76t2n2F16Drhw/T4Z48OXH9ds2gV7BYuWxq+zHr36hF24eNnQV5A+U45te4+wkhjnyu3HC5atlT/4LN6Eb951kBOnzl60dc9hzkJ7j5zOU6CYgz/6wsqoOWrCNJo79h9Ts32X3szLdATqS7ceVq/d0Jeu0ROnE5k5ev/5+/Xb9vrN26RFO4Zi/LQZs8lTr3FLedhHuas6cPw8g/N8uNnM2fMcO3tFd7dj3zHuzuiKjXSxGrBbte+KzeLA1k7MqWGzNrCkbjqKXaxU+RBTpEid4dq9p45GGaxCDoWYxfOuTl64EXjijfvPVSdQs3T5quo8b+kammev3sVmcB3lqoQTyleouOgKHHPWguV+RSB1GDB0jDwQSJOkOthVAZ6vE96MrigZXfzGp0qXmZhw+/Ermpt2Hgg3M5w+d4nWlta6VhWqUKWW1yzedKHeA4YTDfir5tBRE0PTxeDYx85d1aGNO/YzVNtOPUSXVnymbLmp9xBmaRJU/aY+dPIC/kOnLrpHoYjnrooYlTt/kZRpMjKUu3cu8tSlm27AgUaX0dVvyCj1XLZmM83r956FS9eR05fpuWXXIecRQmMmzfSaxZsu1qtvoQUPtISmSzYrHsw6dusD1X77rskzF6g5eeZ8mjhdB5dY4ufKAaZA4ZKaS4miroqRHbo0uTA1x02ZRfPWo1dGV5SMrsYt2qknv81KvcKlSyxNmbXQDwx485rFm651W/c4zwYyNBC6cic0XWnSZ7l44wFNp92HTimf9KtqdOs9MJqu94GvqnTZ7LhAEePM5du+V8VvhJprt+ymye+LmsPGTPqRdJmMLoWUtZt3OQ+hCQ8Z4/fTpfRMOnrmCp6dB46LLq1+HVq5fpujSypTodqMeUsdZvOWrI45XYjihG7q3LW7GLy8+mF0mYwu7SiWrd3iOf2ilRvo+eDFB03B5yBu6X8/XSR4cCJaVDaYMG2uu5EV67Zi85Zc8VN0TZg6Z9XGHS3adPYdZ9fBE550UdicNGM+o2HXbdRCh3QNVG5+GF0mo0u1AVXeVHALJmoV7PJVMKSwJgbY2fO91ffTJQl1xERZc+RVwHSHAFu26KLiLyT2HT1DTqhDvBYPTZfbX1Hc11GhhYiZNI2uULIvoWgKgxZtO7t174rjrCrfekOJMpVgwG97E0ylylVR/Q0xLMtRP/Zes3jTBeQQq5FvPnhBYNTRnHkLKV6pIL5971FtyVRS5+WbIBfz46fO9v0Sqkfff+kCOVfVoABIT/dD4Ch1ZEonzl/Hs2TVRjVJHX3TV+qZji4K+tF0Rdkm+0b+f0T8SZQsNVkW70+DSZmbvpH1fO/s5DmmixJ6W00NPXAQ4liwuKpyH6E7rG98VRiUDp44r2jJE7BFZnT9LO0/dpZ1FkyUoX/GmL50/WINHjHeBUbFPZPR9bPE2yo+Rwomvqv6GWPyl5yNV1K//oFSLFHGqNcMJqPLZDL96XSZTCajy2Qyukwmo8tkMhldJpPRlS5T9tIVqv/4kU0mo6tKzQYLVob7OthkMrqMLpPRlbdQiWnzli9bv3PGwlXFy1TGkz5zjiVrt7fv1m/puh1zlqyrXKO+ejZq0SF3/qLuRNezeduu9Fy8emurDj3kn79iY8GiZWRPmLGwWp3GGMXLVJq3bMPyDbtmLVqTM29hR9egkZOYnVMKFSsbOc/dZHQlTZEOKoaPn1G4RLm+Q8awytkLZcqaGwagokjJCoNHT6aDPnvF2WvgSGwn9YSZEmWrNG7ZAbtMxRr4GadoqQrqA5/1mrTBWLRqS7e+Q7PlKjBy4qyJMxeLLk5hXsCbOncZPSPnuZuMrhJlK0NCgsQpseMlTAYANeo1FTPZcxdU4QE7a8782Fly5EucPE0gXcVKVVRz1KRZ/YeND0YXzl4DRyVPlcE3M8TJvNjlq9RmKAyTKULoatyy49yl611z8uwlnXsNEjMOJOy8BYu7PoF0pUyTSc2OPQZMmbM0GF3V6zQhjaQ/iWiBIqX89l3knEaXKaLoImKwZXJNcjxICJeuPP8dHTRq0pDRUzAYs2K1unIuWLlJdCk8whUMA5XRZYpwulKny0Kcad2xJ/8EsG7jVqxv9kXB6OrSaxA7MT+6tENLnjoDZQyGYhD8s5esHTFhJv8FRbnKtegAXcQ3gljJclU52qpjT1JQoyvyZTVDAGCts7JJ22rVb4bHjy5FJ6oaRKQO3fsH0jVg+Hj+ooEjJ8pfvmptSMND2gk/dRu3Vt6IBz8Tlf+HvXtAqgUA4zg6fH7Ztm03zFpKi2kz7a5/tl1n5tS1v981phav1NXQ8uXqQl3HcuPzkJ+curLOWYe//hZf+QB87gT+L664vg/HD9LuAl5NvnIr95JAXbktKquqzxJQF6AuUBeoC1AXqAtQF6gL1AWoC9QF6gLUBeoCdQHqAnWBugB1gbpAXYC6QF2gLkBdoC5QF6AuUBeoC1AXqAvU9Q2AukBdgLpAXaAuQF2gLlAXoC5QF6gLUBeoC9QFqAvUBeoC1AXqAnUB6gJ1gboAdYG6QF2Vtc3dA+OD43NDE/NfHmTUM/AZ+9et6+ffohxM9+BEe89wc0f/NwEZ+Ix9hj8JvFZd2feu/rHvef5Chj8JvEpduWVMvt/5zIUkkBBevq5U6w4h7iImhJeva3B8zpkLCeHl6xqamHfOQkJQ1zOBukBdoC51gbpAXaAudYG6QF3d6xNDu4uTe8uL+zuRJVn53JMH6kpIKepGT28M1HU1rScF1tE70tU/dqylc+CAnbPQjWNZAui/hJkTMzNvzMwvzMycmJmZmcPMzAx/845uXZVWmSwovPaVSlF3dU1vz6TOFNjen/uM5i9xSspYExIV/82d+cTkzHVOHv7GIyHWjyoyfc5i9JUNHfuP5dk8TOaazY0dA5UN7TINCo9h3DkwsXiFm7mZ7rZx+/4L1++7egdNOef+jy5F6wcBu//8/ZM3X0Qev/584/5zePjxpwMJvSMXzHfese+YrvoERV6580RX7z59e+hkofmRHrz4YP2oIjXN3ejZ/NKtR9bPA8ZyjLGLN5nOW7yKMZpbD1+udPVRM/PdeobPY5C9bpuVbbmR8rq26MTMKQgArzbent8EY/aCFY5NF+TYKRRm1unCn86UVOeV1nYPnWOM4DQ/+HSIErjm4MSVLbsOQc6dJ2+YmuLTWPILjnr48iPTrqFz+46eqahvF2yO55fZpIuzFVc1qSSm/89OumCAj8hcs0WmXMi0rrVXpka6JLSGRydZ33btlt3sk19WO9W42rjzUFF1K1JQ2RwUGS96v9BopqLftOswCYtD0mU9cLEKUXaFL4Mrl9W2qrtcvvXo4s0H5pZdg2cZ4NaMYeb249f44rW7T400ssQ+muBhAEUSFTsGJlg6VVSpxl4B4UK1TbrQW+EBWrDRTG/04o2bD18yAHKJVFB97tq9k4WVgjdK7PlTom/ull9Wx2pA6GqciQHHHvhnH67lCWBw+GSR+T7iTMQ6LkfDR58oKEejT4xXGFGaF42j0xUZl5Zf0bTSzZdbzl6/g7FkK0CVtX4Hj8vJ3R/MYlNyHJIuGoNW0PoKP4ztp6uhvR932Xv4tCzhDbqEfuLKHQbNXYPiUsPnr0lQ6ugfN99THBr9hRsPqHaEMRWST5ZmzF1itMeVf4SuvrFLbLLc2Uv01+8/E2KJimSALHHgwop6AOBGmPJeaOsb1eMZWcUmzJTAURkgvDJILDGQT0nP3Qirug+XRMamCH5MMdYnKU8M4WNbe0YcnS43n2BP/3CNV0AFUX4hq2Ug+t1H8o7mVTCYMXfplj1HC6ta4C13024HoEvJEXisoCViMzM8fKoI6Rm58K/ruHjbpIs3MWPeXlxidHp6FVyLmQhemJq9Qd1Xt1UprmrEbNfBEzbrLmKCioBkky5FRTM9UkSmJMMytYcumJEoV1Bez5TQbcwMpdQMjoyTjg6X3HjwQp9YeV0r40kjXgERpviM06X1a7bsZerqFQRd85c6y6okjQyik7IIbq7ewYERcTAGlo5El5RVMGZES8XOroZEpOx1W9HbogtPTRY92SNT486At2bTTnoDoCKb87JHj88Z4alt6cFgzaZdNuki9Kn8TrrOXb0rBnEp2Uyrm7qMdMmd0mkUYYzwHHhi+umTRo7klUNLXnmjT7BJ/rvPlDUQr0KiEsgPoYtV9CnZG6HL3TfUITNDxtbrMZuZIe7u4RtCs0GKn1Vufka6eHZf0RUQFi1L56/fY2q9CMYXsSE2Ko1SHeFwdPNwX9mEmPnjmaH2AMHvJ9IlzUaE3owluqQMGxi/LELg4l8yT31ik629MXcJ8EDRrAXLmS5z8tp/vIiQBXgAdqKoRppD+44VSijL3bgLR3Kwrgb8GJXf0dWQ9Izy3bwzIekQP7Oyny7cESzRqyY2OQsbepKMaaOLCzImv2IslZgc40footphH4m9nAFf/z10acpHH4XpUidPmVJGUokxmGR0RcWnewdGKmCQExAey1fNuHgFqQ1NRUovnc5b4hSXmoulKSHjb6dLWoJ2CvZ20gVI8valicd06Nw1KZnoCkj3wv7YNX7pFsqJy7f3HjlNj06Sug3b9klBItySO1G8MRDRwkxKQforKum5m+yhiyYe+3DU08XV0rf41XR5+oUx5mC0QOUH0FIZctcgJw2PyUdX1rrtlFtEKgKRMEO5RYwiiKXmbMTAN8SEkoYH44w1W3cePAV7/Iwxv6LRlJA5tX6ajOgUv8QPaD0zJl3UzgSdLqWrqXNQ+3sI+BnpIvEDLfNyDsbMex7khyjVQNNCQymI4MqdelQrPJCDyWHErekTsqR1naCiv7chjRn76SIuiUFUXKoeSTsZiOQ83KbWmQBOe83wxBxeZi9YvuvQGf15V0RsqujDo1MATCouMkNRrnD1OVVSK8Z7juSRQ06h34SyKZRhi5a7ft+1BMPoxAxLXoXXmuLTaULIz3YBA+WPC6eV0vG3CTfy//bugANhIIzjMCAEASEQIKpFNmRA3/879YeJjkBnunt4BAi5n13nnUvYH0em5+X0rFXZE17uj/I/9jQ/81lOveVo3hTvOvKsu43evmH1ugrlGyhfp59AXaAudYG6QF2gLnWBukBd6gJ1gbpAXW52hUVCcCs5/M+t5PvD8TQYEaRrSSAh/L6uSLUZ1/cT06cs/uXBVaGuzXaXb0++3W0RsSEcpiz+JFCrrvcW8ToO45zDk+ZBlnoWfLEhrFAXoK42oS5AXaAuUBegLlAXqAtQF6gL1AWoC9QF6gLUBeoCdQHqAnWBugB1gbpAXYC6QF2gLkBdoC5QF6AuUBeoC1AXqAvUBagL1AW8APd3BlmN0NC+AAAAAElFTkSuQmCC)

Sample output from SQLFluff in the `Run SQLFluff linter` job:

![Image showing the logs in GitHub for the SQLFluff run](/assets/images/lint-on-push-logs-github-d1b1d9efc65a86cf416ce9fd081cc1e1.png)

In the menu option go to *CI/CD > Pipelines*

![Image showing the GitLab action for lint on push](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAATAAAAChCAMAAAB3aBOTAAACl1BMVEX////8/Pz29vby8vLw8PD7+/v09PT6+vr9/f1LS0twcHDHx8eCgoLR0dGAgIBAQED+/v7m5ua1tbXi4uK4uLgmJiYAAAANDQ1NTU3S0tLs7OwcHByPj4+kpKQyMjLe3t7Ly8tmZma+vr6QkJCIiIj5+fnFxcVoaGh4eHjKysrT09Ph4eF1dXVJSUnr6+vv7+/c3Nzo6OiLi4vd3d3b29vY2Nh3d3eGhobg4OCBgYGWlpbMzMxubm7GxsZiYmKYmJgqKipTU1OHh4dtbW0WFhY4ODicnJxVVVU7OzuVlZX4+PhWVlaTk5MiIiJzc3OhoaFCQkK7u7t8fHzt7e1ra2uzs7PX19eDg4POzs7IyMjQ0NDW1tZ9fX25ublxcXGUlJTx8fHj4+OysrLa2tpsbGyFhYVvb2+qqqrn5+fq6uqsrKxqamqEhIQuLi6wsLD19fWmpqZjY2N6enqnp6e8vLzBwcGOjo6Xl5egoKDk5OSenp6/v7+rq6vNzc3u7u7ExMStra1FRUW3t7eSkpL39/fPz8/p6emfn5+dnZ15eXlfX19dXV2vr6/CwsLV1dWlpaVcXFxpaWk1NTWampqxsbHAwMCMjIyjo6O2traurq7Jycnf39+bm5taWlqpqanz8/N2dnZlZWV+fn7l5eWNjY1mZsRhYWEwMDA6OjpXV1dGRkaKiopQUFBycnJeXl5BQUGZmZlZWVmioqJKSkpnZ2e9vb1/f3/Z2dnDw8PS6N2FwKFLo3UlkFgQhUjV6t9drIMTh0s9nGtSpnoUh0uezrVZqoC22sf8/f2NxacnkVqz2MU7m2nk8eq6urpSUlJgYGCHwqNMpHaRkZFPT09MTExbW1tkZGRHR0eJiYnD4NG0tLSoqKiNxaj5DcKcAAALs0lEQVR4AezMxQHEMAADMIdzWNx/1TIzPGsNIBARERE9lpBKN5QU9687mbHOeQDu9cbM5/vDP7DYExqUvMeiKMYWE6KVpFgg9YjEnDCVnNa6cG4b3aIAflzZYfhK1yn3GiqnYWYu6r2woei4EN4Nc8rMzAz/6FpWFcNIo8UTMH1z7vgntP7+epd5mUW2E5GzYAd20i4gNbtpD/bSPlhlP7sAwO2BYbJZwDxePgA9LtlgQZo9JQZbUOZYfEhO4UGzriLzMiuw4rwSchahqNQYrKwcsAbjiv8MTN8nNldyleluUV1TU1tXU1OP5DQ0Gnc1ZXFzi3GZNZgEtFKbo70D2e2dXYcOHwFw4Kjz2HENrLW9TGn/3/+7D/VkAL19zoJ+I7CegQwNbPC43xcAEPTIoRMAmhrkugALnPTJvlPmYKc98pmzKlh22D8UAc7lyOHzMWabXcuFi8MbYHYbABjh6OO1cQPMI1ViNCwPjyGxa7x5z+DE5GbzMiuw36ghnX5HP5HzGNEUTjudre00FAPLp53TRIfyiU5ihrpnD1GhAVg9T8TAvHM9rnlewJjcubjE9Sji0OIys9jMK6fcHDEDW5WHF9d4HS72b9niDwnRFcq9xE2JO0VhYCwOtskETB//a9zlnryTkov7C30+JHXJO+1XLi4al1mD2a7uon4NzLkZ1+g6uugGpEO7EsCKcJPORBeP4TLNGoDdWuByFew23wHWirEn7EBG7V30jiiAh8VJroCjZtoMbI+6bKgWLhWpkFcj7AKqdgKAZNdzJw4mmYDp4/Vx6nv3RhyI1IjEri33o/9CE8ZllmBqjqZrYA8AGznRTtcLCojGN8DagSZ6GCEqiL6/3QhM1IWVKNgjXl5eZk4fiT32IGcIwDYWZX75eIsXZmAhddljTnexAtziFuSxZ1sEauxGYHYTMH28Pk59L5dHep+IpK6nw9F/u+8ZllmDZT5rHvVCA5MBOEl0Ez9//uJ5xQbYXuAgPbxD9Dz6fq0RGK7IL6Ng8zwzM3OzV/Grj0tbcKYNgIsFyl41cFgyAdOWZfMtF9sAB7+G8voN84W/DKaP18ep76HobQ9XJoG980X/Nbz/m2AS1Ghg3dM4ScfQSieA0ydtKWA4dGgTxIeDhmA4wOxBNk8DyhXcGwCQJuFlrQDaWCjTQDVfRUqezAgUcS7uqcvehuHicuACf7RJAlLXy798SOrj9XENN4FpBZjiwcSuJnncPjh5daPs74PRi/AhcqtyQwPUnpEKlkfXP32mZmMw7GYPIv668uo5H57w23OX5bfI5ZX6bcziLGdH1NNcSnJ5S9ESS3gSXbbOo3Bx8ZMnxT2Oczx/JSgHku8071if9PXx+riXXUFlqau8rE12JHbtzOod/HLxzt886X+FGkcMbPY6ObMEsGc7UV8V3DQTBRvcpINlfDtE9H3aBEzye4CqOeYfFcDrMHOjArzzc3iehbLMrAKk5iUzrwN4HGZ5RcAlTzHP/QS2yMzLCgDYjMBsRmDL2Bivjysf4eB4HvPIDiR1XW7mi9kpZX8j/VSLMgdi2ZkGo4ixdFjk1i3tUdKahIRYMiIwSlnRr4FfhfbomNYe/2DHHrjlBgMgDNe2bdt2j+o2SW27U9u2bc930+Qa+/O6Ol3XzrzHWD27m2Syqlb6mElU5Qsvn3i5RpETzfQamcNoaOqTfT/Yn+47p9F3P9f3P1m4UW/3/XGd7xzfiX7++P6udHtHKaWUUkoppdS7n5LABJarYeqrE9j3gEF9dQITmMAEJjCBKYEJTGACE5gSmMAEJjCBCUwJTGACE5jAlMAEJjCBCUxgGVW1V62qgRzdXXkeKc18b2PiHERrurJZEMFakTROa2TN4VCklMdBoIto9bk7mGAfZvak6fh1YOfXQmADAIs3qnn+GPcAFvsm/wESYKcvF7xcgMZeA2CRVwjLOx8FO+cXvLobYLAxXGmTLHpw3RjLY3ECjJNL2KpNU5YCdTkF79k4Ata4gK08BhbsRV2X92xyEbCNZRhQ4KLqwHA14HAbXrznvHSwk9xQAy+DChbJX2WzFQCPrxyHfDORjAA6HAtsZGE62BA2A44EFWzriPXzq8FmHoASlo8eXTR69XwnXAUc1gd2cGVTvgJ6JMAiP0T0CPAxDIiDWTwHXO/9ArEcPgV6scl5mhq4kQDbwynAfoEB91hS3JVejU9gXObTrIbL0v1MgA0je+1mUMHaINLxKBiutiJ3DUO8qbxg6PUAQoZmfxRsUwQM81qx4CktbclwjW0k9+I8ItVoWhUpDa6h8Z01jW8lMIEJTGACUwITmMAEJjCBKYEJTGACE5gSmMAEJjCBCUwJTGACE5jAPlJDBxgUAkEYgEembQlKB1gQWKw1i+4REDCCTjFA3SAodNUH752h/31H+CzrJAWNTJoNMCz1orMbPaHxo5tV+oQVlvS2mnDVdmsCCtsCEzoOG0oYx8MTPn9EhggzYfoPLAYQZsURoiqve3ue7b7mir5csdfDWCC/nnAtAzdd1/CwXOH5jQm/HRaZ8HyosQvmxo0wjOOP5wI+DpUhpxmHOQ7DcJmOmawcMzMzMzOvylyHNszM+GWqVSxnL0oqF7f53YX5L+3Ou7bsnuLcCLeNzim7LdB4RQkOtuoEXpaXX1BIaWFBfh6ECUnK9AJ4XplJIdCcWCU0WFywFbyiYkpLSsvKSsspLS6CGMeSL/hhCL8LycfAWIPjRAZzeIFXQWllVTVU1VWVlFZAiKQLGMaFJGi8HAKDxd0Fr4bW1sGtrpbWQIDdmX4Yhl/mbmjuxokL5n/g5furvgGchnoR99jDO15wkW9I0o0bTgzwuvMQzAF/ccHs3vz+RWv5XqxYLS3Cfy1YDyRLkiyzZjKcN6ByBoPxtgsLdsABTjGtwxB1tBhu13KwbS881ngdf0XInY16L9n9iixBtfFOCBjHAVHBEmbw8wSthEElzYNu6kr8+B3ctmfiDzU1Y6jYfRthJmE+30u/1SQw8xPAzEgQFczBD/n5tAqcFjBVNJ8P9pD7grA5JnuRMc5xsgpmcgLBOLlebFmCCcwB4+MQFSwtBIMKSqr5XrQVquqSAj5YYhuuha1sn2qzoJmQjtnQxHds71Si7cDytunKHVzrUsbtB2xHgfnfKjOzAcz/XPnxEKZNJd2TYOK4l+uugu6GpALjdRxMSJqoYHYrBhWWgu81EAylhXyw6Cd4h3x3JJVEILRJ2rsUmgVEef9aU4cPssi4aycaSWJQFrHj80lwKOOCTpMcRClrj/SQIP/3yaH5MHHQ13Vbwcj3IBirXVSwJHBomStVL9cLZdQQLBbouMEvyQXkJOAgvyLrAyvw3XQgpL2NBfuo3RfWH9/GR93HgKs/ebIkLdf9MCK/69Ak/Z+CUUp79V7DBpsK4Mm3A8HGdXR0dKrBZgNo/wFZEwAL6QOwTmLBOsi6detIE9ZOAjNKg5ksyRbKsF4jLMkOAJNcwYI2bdp0SA1mB/BBG7LWAR+TRgA3vmPBppKMjIzT/ehaZx6MW5JGsixsSZpv+i1cL37TNwR7MrgkZwFjSIAWDE1vA37f2ViwG80AxizFsyYrEHpeDRYIDzd9SXUDOumGyaYvdKxo0XsZxwo+mK17/sfuTf/ggixl9UCwXWRW0lGSyYLNJZ/eDVWO4g2SGH+EbMVq8ukqD8cKNZfMDWJOsWOFyeDaO+Lg+ugJLrJgE74FFnSQN/Rg7yik6Q4wjgXzOzqVtPeBBcORdkLmfAxMU18m+gI2stbDwVWS+MFVhoDB9W8ejYz8QqAHS7B68R9YClVzD1RLvaFZagXjbfHwaCTJ/NEIMByNRvHhmwWDgUQi/s7h+4YTsrYsZf1W4w/fo/zhnRn9G2HQn/S3H95x3rjBmsHl9/btkAoAGAZiqH+PFTNevOwN/EgIvKYfzDt7QJw9II4B0UTtCHIXZzaH3BapgBilRe4kqGuRbIqCE2TnHhueCgNhhBFGGGHIhBEGwggjjDDCcABMDQkF7368eAAAAABJRU5ErkJggg==)

Sample output from SQLFluff in the `Run SQLFluff linter` job:

![Image showing the logs in GitLab for the SQLFluff run](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmgAAABhCAIAAADtHcr/AAAl6UlEQVR4AezVJQICQRiGYfK6a8fqTsMjVCi4c/8j8Ccq7u+z7jLyldyLAQCAPwxOAAAITgAACE4AAAhOAAAITgAACE7f9+v1eqfTqVQqnued9odhqJTq9XpFUcRx7OLRjL6hj3Qnd1zcwa7a8hvNpukCeAGCM0mS7XZ7OBwmk4nMZT3Pc9kfRdFqtZI9y+VS5rKeZdltz9aHujE4knMWzq3tuB+/SRps6DEzMzMzMzPz+8EyMzMzMzMzM+Pfs5/OZ0fTPalOe9LzJnfeejx3HMexbEnWV5LdO6zZVh456b6ya12+fXl2wHSn6eCBQfelKwMwrMMrhjF+dNaowuKvWe69sMevhhcO0/6krEu08YfGln9uGZ8y3lrUZMdtVlb74m7JkO4r3FG395zeQtY4Pn4M9cF9g+jpP9yHja0vtarpzJOg5ApZVUyelG122Ho32H+kH+Kb7jOtnwAhw3b8m2jdMePJQZO1wg7qGlNN9p/UTjTcRIzJ7PzMgyWZ7l7OmbJlW5iZI5YTzafaBNHprlMWX1C/6V7T0ZmjyRET+JMsZnHAee6554KLe++9N+0DDzyQ9tlnn0379NNPp33EEUfQ3meffWgTes5Hu/2+dvc13drNBLbSuvT5pdkBSx9bigGj80edN3biY/9p/Q1SGTw4iF91X9JN+5OSE60MnNNdpq0vtpY+xU6fwDLdY7qy2r9vKTnnKwOsf1lM/n9w5wDqrW+1cuCsrjPVS+etHSQyPnaBTk+uqNXF5OCtOfnR/EkzNjU+oX62957eW1GMTxcVY3LopPGbhnRb324Fi1AheDt7XvA76Vnp/9sW5qyNqJ1/bAQTmt9pTvabhI8uUWrnTZ11XM8Txwxr/Lkx6zej0k4CIeCznGj3Zd3G7xv2g2RzEoUJL1phgpxcvm3ZTggFUaiMzh3li1kEcF5yySWAIhlac7O0gVLaV1555QMPPGA/hXiU0LMqVbJnSAJ2UBu/aJBPq2c3eignr0QemRFUjaDIsOnOU9wTGq2vtSoBJ7aY8d1Xd1cm2Xea9idlXaKj00YoBMsrX4bOl7qyWOCksCNSCFsVcCIC2Ih7Pr/OVC/YNX2yRYJJrpCK6ckEnCQM2BTbeWKB8zNFxdCCN37bkHTn7Z3gGI5v4bws37Qsz9vvajueZFtdRNk1sNF5R4d0goi19MklFRuQ5mPzh03luHzLclUMEwjF+8YvGzT4NyXqIn/QZJJNAicJEmdofr9pQyxk7wQ/eIHN7zYF8mwxiwFO7jUFy/333//CCy+kve+++64JnHysSlVBwgIara+0+k9dB7HIv6ExAm3zZ004KPxgJe1pf7ANv/r/23d8/3/6s0YQdocfRIMKPvkVEVtgWEQhDGh/uE2baWkjEtqMcRKFLdG0PysJUaNw10aNqAXrz0eAFh+T/fLD6d5T+lEpj2jsaHDvIM0PXz1kQPPHK2xsf4TTu8I3OYALKSc5Gzi5stckGOpIJ+dztSFYvmGZw8NHdgrngVX7x0eOZy0y38JGmcP43vPrTOSS4em8s8MKWSebEjg9SMFGTFUMH9wzANh0nhq/agwekl2pzjBPcKb1zVbYZfjPptiOVpLAjs7OWzoFHdCuJSXlDOfCZUMX60BWyv5ZMXEXzkhW/h8RCXRf30kUMhFTzpkATvSHhTEGbcw5U1uBEGvGPhpJkJqCXfRotdFbT0SMVxaxjHJFxZNA+QUDwakqhpEp9URw9UOOwan8Cl6BWAXgRJr0EEKZLae99PGluogWEtf0N3/apD24fyDwkGmgx+zLHBimIvnwgobJsIwoRTcLzm8GODka9Hdf1Z0cOFEte8/qmdwKVXcxcCNZzIIeB/H2B7y0nHDCCXaaqj388MMjVUvZfvvtKxk7IRC930iqlly26tJ9bZdsA6cXH5N+fms/5zySUZkR1G9a+txSZORoE4tkGDa4axBWmGlpA2m0uQPjh/pxOFa0l29ezvsrAyfWk9+qKKGdw8uGfFQbJEESkv72e9qtL7f8il9Rh1cOywMy4ntnwNjxLz4ayV5tE4xFfT1pXgY7syFUGAJOgm1st5z3eGcW2UgOv2eF/59dwn7VqL647UzuvmwossnhE7gxaywwN2T2QDhdASq6lOkM51+GtL7Rkl0wyjSAH6nwHxOsbiDKkB2AR7v3jNxLyDkTOTEkQgOHj841xTQ5ZEIDj4FLIOwIwABU0NN7bi9VyERMGWds81sbRE7lnKmrrE67wUwCCJyVUEICejUzB85UUYUTXWEEh/jmAE7jIabFjYhcKHjpt7PAiStDT+cNHVmt+OolalEcEjJSBLO5z45jMgeG+VuUja9CHzKils0Dp7E1akxkJVE0s5D6ppNIgHa2mAUAp6h53nnn8bCWtK33mj4Ouueee+Jx0L333hsZ3Y0XLH5ctKC+JpHKgZOKoSHHWwhbsRQ66eXAWVCCuG2uBpwF0pFhzvsrAGd+xylwYgTxtjwM2MqqqVqBkwNpiph43UsUVNOwiclNyVJxKcDgOGk8p9IQhCfIJATlZAL+TX371CLjWWu7B3cPdPmzokHEPSrU4UVDjN1sPydZe+SJcmHld5wY3/5j/c6bO0hTK8DdSaYz7hpIYKdUk2NcGoWry5mP3Hv1VG3KGSdH1TGUmng6MzGhFfgHCFc7qzXBn0gVMhFTxpkAMGOOcs6kLsJLirJDjYkkZmVaiHQ5hnGXXxU4M0UlInHxJLoQ5XypWsyOpwPLg10SxpgtA05CZBegRMS/eolSdHpALBYgQqvSjOw9u+euq2IYF5x06sDhwWg94GFGtC7gxKHR0KHhoGAhRkfh5TBZej5mi1kAcN5444133nmnbXARgLz66qtpi50EoLwVOuyww84//3y+qkpVJRDt1s1amARzpJrH66k4Whw/2mjYkx44sY/mjQW8+YATznjP73kAVPRGiUhW233ycjynDIQmaayahidYqDg3mUXGZChoZygPwgi4ZyeH/x7XQsV6krumYaa0///9cuAEcvBPI3up3QEtMp3RRylUxgNLzrCpO86cM6Gi46PHQSgTk1cY2gvMIpEZDZ5QVgPOnDM0orKGcs5kO3XCqO6XFHShM8QXdFHvmKQqcGaKikmFCu3AgzmA0wUIY0jKNjF3BpwUoMvA19PN8uol2nlbx698WhyGy6BTpQWN5sAwxce/JHIIlE08ZETrAk5lZNBJap0GtMKUGUjE5NliFgCcwOFtt90WH4kyb7/99vgYgEo/t55z/OWA93m4EqZty8fr1OPnIvgASNv6uQrJfu9EjeI3CJxkyQrRPbfoYpXf1gWcCdH5gTOCDxLg8wEnl1thgyI9izZzNoyHghuKCS/HI43WWokImU0ZFQ5z2GXOPDt1EgZnBfeZSLdQOa5gzGw/e/eomPAn7VwOnCS44u2lNzea+0xn+MqAb/VOuVkUeKgszJGr96txLH/6Uc6ZiI1WA2cmJnxKIZNt2kB5yhWyIKZyztg/vGqo9cSFKuFM/nfJRdmh0uR7Z2XqpXvQJdBcnTmPTtOtAZyuWU/Cj+WKqi8IkhkrI4KqGBY8JCswOmcUjkgROJNH9QV7ghHjXLPCuYnqOSHuSF2oMy6D9XC9ql+YE00xTPcObwnOA1cqXkK0DDglAVFxt5xo+wPtcC+4ETBbph1z4xFr5hxYBHBeccUV5GBPPfVU/iLlzDPPpH3SSSf51RlnnMGLIV4PXXvttfTTrkpVC4Wu6yeSxS5P1YKR5KCwg/AxwIb7Tjlo52rgBHLiLhOGYg7KgZMjpIaR3mE8IBQ6qgtfN3AmRA+a0KDSKWna2KwS4NQfNCXFYExAVeDEkecwCDneFKLxGHTtlDM7QEPA7mxjmEizMxvjg0q84mMxHg+8XVyE/uN9Y6aIh2opsRgEHSGLDwRYAG0dfNokITEf8oq/a2RVESdlOoM4GK9+YjXYBbsDHnxqoe6hFVxzcvVQuGKBJwC5oXBSEs4kwJmJSbwX2xigTDOFzMRUwpl4HGT4wj0oippyppaSAKcWXKLwpACcSEFZs35fkWSKSjYYlcYKcxbwMwJuy4GTDcIuq+8EzXZAka/ivoDrAwZE+O54zhoboQGvXGchOPZIkqmej6hpfANKB7Nl/TnFpMJ4N1lCVAyjBlHG+Le8chL+O1sJUWfmo6ThOe2wS6RVnH9dovwk5rfBjR46Fi8AHCxSZotZAHDusssuF198sf8HAtHnBRdcEC+AvNek8O2RRx5ZlaTehCqrnSr/gwESszqGVvLsJnAwK0yiRDnPAZyW/lP6qkvBcIRViqKHiAqqiwGrRoRUj0H7vTPAeV1Mm/RnJSHqRUihcmDKgZPzH5f27Hod4Hy8CJwGBM6gosdrXg6VnZgq+Ryn2lNh5WHL6tfIBKn2EwyFfx3qTkK1RvUl9gq3ScQSOF1wodIfQQZsxwoID5nO6JUb/Vv5if4sD2eUdSGH6YE36AzOJCXhTAKcmZj4N8JH8MDIIFPIVEw5Z+IFCvppf+8FvZQz9ZU1Uxf9/+ureCYMAzjlA9yON3Qlirp867KdbhZbtJFUbdQIBMk3rP6TSp0exRE1dkFdnabmMK4mwXa8tZmPKK5ADAtxOE+4U1R8x3KiYlhUdc9TptEQsxlWTjS0NGqEmLyS1eaXE43nPwWOgQWFwQJqtpgFAGckY/fcc881O/fYY4/NkQY+K/wHCDi5xASIsJDpQlPpxOUP4KyxcIH63/P/3pGBhMmFTm4LZh9QyHnG4zVvhD+42yTnnaf2Yk5i41ZbnQGWKsy/P7pX/MNco0D6y0nXzZkQU/2lBs488QV941RueHiiqATNR07o5NtNFpBsg6E2ekKumAQj1Nd4ffMXvYSaicoBdAzXZ5NE0XY4uUl2idZcb2/cM/4Xe3egwSAUBWDYBG5AhiBABERAhHqF3uDCBRj2dHuBvdfKZbMBDLbt+xBACD+c09k/09FP3p9HfvJi0/se4QT4HnlGLJzCb780O1z3hVrXUT5FOIfiUpSxrABAOAFAOAFAOAFAOAEA4QQA4QQA4QQA4QQA4QSAvw1n0zTjOC7L0vf9y6nqruumaRqGoa7rCgCEs23blNJ2AiXGuD3Xdb23c57nG3tnwEpNFgbgH2FtUoAIEQVFVBCBaEkhvwARqSqqoghRKigoSlS1KWxFbSFShEJLyUJEIKwg7NM97Wm6t++0I9/W3e99qu2dd87MGVPtc99zzvlG5/nYNd9R+VzfPzmwZkZHR393wLc/zXkzP1sADw8P69nx8fGMjAwCM/pTMN3d3QRm+Cjp5OQkwSdobGxsaWmxZnhg9WYEQRAEtxFnUVER4vT29ibmS5w4Mjw8nJgMsRJPSEgIcUpKCrFd+Mbnx8fH29sbYtPJubm53d1d8gMDAxwa8gY6OztpaaW/v9/agIxVVGZmZ2cfHx8JzLS3t3Nbgk/An3ZycmLNbG1tqU4FQRAEtxEn39osLCzUBRyC5POcxAkJCcR+fn7EWVlZqvQktsvExMT7+zuyqaurczpFXgnSnDeLs6qq6pd/CA0NtTYoKSmxZszExsbm5ub+x+Lc3t5+enoiEARBcGNEnBiIOD09nViXm8XFxerQLjc3N5ubm7e3txsbG99DnAjP9dTBwcFfDmpra3Xy9PR0fn6e5+H+Ozs7+sKamhrVmKs41HR0dFxcXKhymQut4pyZmXl9faVY7Orq0q+OIdzn52fO3t3d6R8Z+fn5qkfewPX1tYjzf4ggCDJUW1paSpyXl4dTmYRjdjMtLS05OZlTXl5etnplzREiYW5vamoK/TCf9+XiRId/Otjf39enKJExvdNQLYoiMzg42NDQQBfMgJJUvwxojN0RobUApTGzrampqViwr6/PKk46raiowL7cR02sYk3yzNHSmCfBoCTh/Pz84eGhvr6eW9HA7cUpCIIg4gwODsaIehEQssQi5LOzsxEqviTv6empFgoR2OoVkWALX19filqCysrKLxfnwsLCbw6mp6edGriK8+joSMWIltgwxxkdHc3li4uL8fHxrkO1/NogpjQnVq+LAvT+/r6np6e3txclk6+urg4ICCDgOWmg2jiJc3V1lasI3AZBEAQRJ/j4+CQmJuLIwMDAsrKynJwcklRaSqhhYWEcskqImMAWl5eXLy8vvzpAIXjiew/VmsWJX1W8trZ2dXVlECcMDQ3x8NyE8rG1tdUqTqtcmWSlECegsvzDAlUmVSn5goIC1f7s7MxJnCMjI+vr6wTuhCAIgohTw1Ig7KhqLPZuEjNgSwzsD2Gtja0uuQPawJ37DphEpOSy7hjhkKVD+tCQ/ypxMjf578WpoPI+PDzE5ex2/ZY4iRmI1mPFGpYm0aC5uZkYELASpxsjCIIg4qTcZGqTQcWIiAhGZRmqVeOxzEcyVEsBShnKv4GAROPi4mx1OTw8jDbQp16DwyH31A0oy1gyw/KZmJgYDg15W+LEzUgOOMsCHwIqQoM4OUsb5iBpQABqDyuODAoKYpx5eXkZcbLh1SDOlZUV2lCY8uODRxobG1MLelkQxDQn5TtbZVznOLkzGbVRxz0QBEEQcaJMpKgoLy9X+0/0qhk8Sh4yMzPtdokwWF9KoP2EWpaWlnQGNR4fH6MTSkwODXlb4mxqaiJvZW9vT4lTz4MiTkphFVMKO7VnRTGTsjwtMXAhAlaN29ratDijoqL0xC2vkU2ZHOpLIiMjyXNW3Yf/0hF/F0kNo7ucUl53DwRBEEScQInp7+//rf99U3LRgOBHg5qbujMpKelv9u4QV0IYCsPoBuC9SROWQXUxQ4Pq/lc0v0SiZpLmHEVwXPMFc2+eH8qssloof6L3lxnsGEMdAeYJJwAgnAAgnAAgnAAgnAAgnAAgnACAcAKAcAKAcAKAcP7Y374v1/WfzezTKyVfupynsc9kPY5M8vVwUyPblnGtWZDJdwhn7oG01nrvtdZSyv3Gde50vj/snQOT5UAUhefZ2JrS2rZt27Zt27Zt2979b/u9PVNdU5lKxk7q4ebmvk73Sd9zunvR/fqxSUgxmT3ZujUvDM5iEyeGV6zQK81WJKVzBA8cyPr7NzpnTpV/tHArLeVV9reODxjAQ0x0714NYS8sMraPr3796LRpkeXLI4sX5/Z73r0DSQYi2CWYNTwalVB2CJTJkWrcGLg8P34UDYFU06YG3ni+G1q4hyuc7JbFVl/sf8KeYnxOnDhR2tmzZ09OubRw4UJdrVWrVlESdfr0rF+/xOzeN2/w+O7fx9YLNXWFsyIIZ2zSpMCpU/Fhwwr1q9COHdw3smRJ2cAe2riRSqbYWb3iHjbI2B8SSF6kib1wlljWeD5/pgQwLDMEKpZw2iDAgo2Blz6WTxHu4QrnlClTUEeJIhtzopGtWrXCbt26NTt0KoaZKP5hsGph6Xjs2BzJfPXKf+GCujWDO+jA8/VrqQpnqlmzZJcuDOerw1ItLU2yd2nxaW7p0qKRY9nA7n35ktslunatMsKZ7NiRMKg82amTJReS7duDZA3t1eqYNa5wajMj4ALPoiHA6BN4mW4WSDjdwxVOdtxk70nZ7KiMQLIHVt4wxFVhhTrQSzpiaPNmw6qW7muhAP6Uwvv0KUNvrgb37En/l3M6tO/uXZyimPDatVryDR4+zBQ2tHMnTm4UGz3aLGrh1ys2fnzuymTit2+nKP+NGybHwitXoui8mC0R4Jw2LKkRE506FTu4bx+2/nDRf/MmdnjDBqiNV2TePOfRMcG+O3e4I5XBTvTurUvRWbMyldy6lQIzOHz4kGrQgPZGFi7UFATxiI0aZYryPXqkluI3TnCjbsBCCb7Hj0HVSGxk0SKVQ3uZwOGLjxjBz4mUE9t3+7bTBLdePf/FiyqZwZDI0QF2CR5OwmgO8eHVq3Hy6P1XrlAON/Vfvmx6AmtoqjyRVDU2bhzO8MaNlIBHfQBbncoBmbw3BQc81DkH6hkz1H9sm5qdrdGepoPBQ4dSDRvihqBVjv/q1Yz/yBHqbI+M0zhAzdRiDD1ffqpkkBS/O2SNQUBwRebPx5OvbJAFtAs7Oneu/KSVgOLlv37djE4YkJERGcFWR+3b1z5VC4cACUiB9AGd0go9L5vK2GcHWfDggeBiXq5Ie96wQUDlT5liFU77jhobM4a64edFGtL2aq0wrnBOmjTJElO3bl38/CFooW4J76jrJ3r1ksOZAhh05zDU0aPe58+xA8eO4Y8PHgwjMIA16QRH44ffVb4MYkxKB06cINKyZqhg/JJzREvZJT8yJoOct2uQSM3QAemELbI2DEgKyUjXrWsrnM2bK0ZCJdI3Km7qGTh3jmKhTvjCUklBKvEOnDljWaoNnD/PKbwGgBhmxY8/RdMp4wYoQEyNZgOX0R7s0K5/7JyFj+xGDIcFj5kZV1BmZmYUlJmZKygJC8L3N/e7fnduOrv2QsrJaHTKZrMzHo/tn2Fy32aUS6HbJBvlRsF2OR9GkKnxeHDw5Rh2Fkpcr9GVH+msC2YKbDteeIHBmVTiud7x0kvcTziTTHrkiCPIDWVMfys7b8IGgZfbPvwQE6zMyDFHxl7zgAKZciZvIC4AoBiwIibyPuDHxyC11hoe5g7Axs+NR6mYzgVOxaMrqDAQeUPF0L6uNimfW7/7jtXBxh3YilxVl+IAMCb3CKb5hN5xzemelJhEO9QCcTpStandSDiQAWcmqNDsSnHItn32Get1FcNtY6r2xRdf/KN4H3j22WfB16NHjy41Jc6gcqk/XgOn0s8djD4xHN6cvwV9sV+77r8fAcWGWunB5Qzg1MXWyjBjUWxzwD1XX82BhSi4EoFpF/RzewKn1lwFYwlzgXPP5ZezQIk3valpgAZWbQKKB7RNqj1honYqq3Hu22A7oSSclEiDPM0HYBOx4wqpWiGKHYHt2se6xhmcj3AQACOO1AZBIV2Lj9G0UhWCIZFFqrbgzPSka898/TU3+bvnyiu1s2sczhtzbX/3XaITjKmmVuD0t3AAjnGN6KacKRsBnACc1T5r4BTY3F/YSMJDH2IucBpmETHrOpgNIk1CHI8urKvt8ePKjAvcfeedrKtW1WU5QKiq1qC5wj8/TIlJtCOrcSZ2I+FAApyZoAqcdLK7mJQRYAYHnBydBSzjcBAACUx2H3jooYe4f/HFF69Qe1O2ULlFgJPIgDtNR0Bx6CI+o3Ohby5wmod0NABpLnCibOIWP+GmBpGsHdfoT0/g9AyhBKP2c4Ezzn1obsI0AGPd5121zjXTcU0AlAGnbkHTibfkgOP0qXE6CPDMNSi1OHCazbOBRtNEEs0QL7o1dY2z5kw2KY0nFSR2xz2qz4U6iFlBDajAGWhH0p5rAqOEM385cLZslMisJYIKbsUJPuel+04RuCiT/YoNKlR1WQ6AQDyDHslGUx0pMYl2ZMCZ2I1EVRPgzATV8oEfdVZM4w+ljcBpJpbXTu64447JZPLSSy891kle3XXXXaDm1au6VFo6/FMdwygr6ik3mIpYGzGQCLLvvvlmcE4t4nSurm4DnFi3pYATSgI4zXQFruCQ1sAZIQs64xIa4ETxuDZ3ahhUA6dFX7Uazdc0TBt0nXcnIm2obmfAiYnxI/ZdNlKmElokMggzNWojqOIrZue6buaiLcoSgS0BnJ3pOMRr0B97jSEjuIQhYSiniTS+xHbXnMkmtRlkFD6EzcyBAokLaORRA2fOmf7AmWqNiI4Yy0a3uwbOMP0hqObwGYooDQBotgAemocX5ApVXZYDMJYYzmFjZzNiEu1IgXOm3cg4EGXL8L1qQY1XiRAMV+1KB9RG4Ix29uxZYPLGG2/kOt5IuaHHIUYFUTWwnu/9EFmsAyZbO4tyxikMzuBgAc2MUVkR20irqgw1cJKcQbXEbCblmqpPBpxeS8kiNU6jUrTdULUBTsizvkjPPNBmUrQ08saZaSAdpFGACf6Q90Yy4PSshNVWWcHgbET4yJ5nwZR0T1LAW9dFSM10GeUOIvfEFU1GxvYMwyKqoFKFU7/lhx9YHfYISyrxUoKQdMMLZ0QqcF8wWBlnauDkgSiN19KLEMpGFgIPa+DMObMccMIZWEeXP6yLa5Ay0xonhTB4whawKOsOWQtBdSj63skE2JONwIkYFljFVm779NOdTz/NRggquaquwgGiTJ+MPG1CTAqcu2+5hTtCo9/SCX9n2o2MAw5lAl/3i0GI7DNBZXwEA4wHdI2/4dIIMwMCTsJNSpvnz5/n5ROytaRqD/9WP7jqqqtAzeeee+7KjbZCttazi817nJE02/zLL3HIIk7N+bCdB8znaI7p2PoaOCOA63ZUKANObR/jE7tofCUma6T+hDpmkSpKiUFA2AvNfQ2crFSQoAMDBXDiy4ddmDZGlJAb4AyrESYJ42L0FuO0Yevp0x4R9PmaeMy09FvTwnwUbA/Od2NH4UdnxQ7/rWNBvMPa43yyFUeDTmWj5kxMmkU5Hv2ti/TKmLm4GjgLztS5yhgq3kLhTtMBp0xrWGAUAp1ajtXA6VGayI4aRLr7npUNrAoO+BVbkKvqKhwwOR8qkxKTA+f2V16Z5hjom9iNlAPx3rnHlCwDZYKKW6wUhahbFBhKG4ETyAQgba+88gpBp/fvvffeuB/f9nmrEqXSo6wbz/Awvh6BVDOCd/70RjYG7EHurcoIJ3XDuAPAM18Ow3v1kF7RArk1hREV1Y3lc5ho+jALyD0T7VBvPGhSWA3bMbUkAPu8asmAkC0lPRtkQOQ0x9gRiGQJq3MmaWQy9XvIBC5IIRHG8pz5WxszojLI1eJTU4lkaQ0brR3M3Av+1qranwM5Mas37UbJgdUFFdeKmwrS4NqYqiXEPHfu3DHEa5Ct8VUJYf/q98qbkLfPf0cCL393+cc2D13cpvXjYKu1sY1tbCNwjm37G29s+emnzRcu/MreHeIwCIMBGDWMiYllwyIQaAgOyQW4A6YcAgsKgSHcd6tfsmVLpt7TFU3N17+m52mKT5pfSec5OY5rUXx42X8uTpfl152HkOz7aV0vff9+bCXL4nFtW6xmnML/ABBOABBOAEA4AUA4AUA4AUA4AUA4AUA4AQDhBADhBADhBADhBADhBADhzPO8bduu66qqur/6NaKu66ZpbgAgnGVZhhDGcRyGB3vn4CRL1kTxMrqLD2N75tm2bdvv+9a2bdu2bdv8e/bkZr87rjV6I0/c6Mg6lZM3K/SLvNPYiddVq1YpdipqwofS36eBXdaA7F/DD90L3fyWfFrk8o/y8SBxW/yrsktSJLtnu6lIJBKJigKca9euBTgrKioQT5gwAYDs6OhQd0tLS/fs2bN79+7fDU79c137UeMFQmTx5khf+0GzHrbSIpf+oY4HCeeGvyY5qU6QrH2npUUhkUgkEnCCi2vWrOG4pKQEgFy4cKG6u2jRovXr18+dO/d3g9O+wzafM/UviCXuRf85cAo4RSKRSMC5evVqvmxpacFlXV3dHwEny77JBh7UxJlfm9c/0EELANW92E0HdYLTeMUw3jJwy3jNiDvibOTYd9n6Z0Qp/SvdO81j33zWhBlOCRFjF8TI5ENj70yPJmCA6lvNucYp1KmjOqgAH3dz+3OF5DMomU0qPiDN8MNZIT+R+STtrsAZjYvMF0342NF8wcQlb+r/z8ezUxvXOcUNTpFIJJKj2s2bNxMgBg7csWPHnDlzEP8J4LyxE5xAGmIsBqTy/SMInAwk9u1b7Iya7gUuFXnZcM91rUcsjLbs6x93covrAI2UfxblM5vBMHCO8xGzbz5lGu8a9q1UxzvFI/NrzbrPwiti/Ocywwfmmd9scgNJZcI8Np83eRfAMilLktKEc7jVYgKnSCQSCTibm5sBRfXmIAygOJuFP2PGDMSDBw/+08HJsXWvxaMn84bByUzCAArqkP8J/H5F6AIFXzdyO3I8U2aDk4+LveM8ToubYnrtiBld0fioq89TI6bh/Mq8c5VDG71h9OeDhVwEbcStsQJnbm+OYYlkLGZqsCwIlgfkv09PhxwBZzFJJBIJOKHq6urJkydPmzatoaFhy5YtS5Ysgblr1y68J2jtz0IMcCLA4e0fB6f5tKl9r/nH+HxMihgrHUjgRIAJMoUGp+wnFUnajzC5gpGcBvB4x3vs6x+RGc4pgBMxg5Mzo9ERYqVgUQCTya3EyT0W5uD+fOxFwaeFIqjGDWAU7p3v/993zyHfvttGMvpBLOAsJolEIgGnUm1tLQA5fvx4njjnHdLWrVvhIwBZ01+tYHEQzgg5xuko8OCdTGyzb7cR84kocggbX2k8cSo+RRMjFWdpQAo+OZc7VORbLS0hD5McLvNr8nFLjECBU/+SfP+Az3+alJEZDY84Jx4ad/WxNTV8mhdODwtrZtifn1Qz/qkBFaMxMJKBqpKD+UHcGOfX5+HjdJdm7o35QvNFIZFIJBJwYtzEvzbr6+uHDh2K01p1PKvER7X4P2j6G+UfTdgw3jSwmCXAJMFyYcCX1oMWkIkA86gCJw+dOBEl/y47e4oFg/3DfPC4AMiqhPzbbMT6e7ral8HpXF3gq/WAZd9pG28ZjF7jbYPhbd9i46099k02JzO5nesd9xIXkEPZDJ+LGO8YjG0GJx3bfouY/nuK6RPdat9oAGdSmXCO+YwJR8ApEolExQROIHP/IW3btg1DJ8w/Dk4+BeX5jJd9g93J1GN9JgqW9bAFkJB5OIETBGKWgGTh5DCjPg2a32m8AFp+kw4EYuESJsDJd5PahEdJ8FL9ifm4yfnxsNh43VA+MMzJIKIy0VK2T0Mkd/KhzruHs6j5YGmAibOzz48Kb/HFf0nZAVO5TioSiUSiYjmqxYhZV1dXVlaW/gWK2+JoQtTHvyoH0Uc1mCJ93BoT4fUXlZQnyIzb495HuNGwqHc+kw/9xE1xT78uiSb26qeEmoxGRAiyfFV5VN+bYjsq3tCteFKf9NH5T+3cIQEAAADCsAr0T0sHDGYrcXcATN4BQDgBQDgBAOEEAOEEAOEEAOEcBACuCmr/QJP0VtbpAAAAAElFTkSuQmCC)

In the left menu pane, click on *Pipelines*

![Image showing the Bitbucket action for lint on push](/assets/images/lint-on-push-bitbucket-746ed122c51527e3a775d29d3506ad5f.png)

Sample output from SQLFluff in the `Run SQLFluff linter` job:

![Image showing the logs in Bitbucket for the SQLFluff run](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoYAAABhCAIAAADENvc9AAAeh0lEQVR4AezXAQaAQBCG0blHAHSCEBASgKQrJHT/A3SBwYKdxeMBBgN8/pjmtRwAIMkAIMkAgCQDgCQDAG1JXrZ7P5/jegGAPiLtcf1nACDJQ+xjAJDk5A4AkGQAkGQAQJIBQJIBAEkuAQCSDABIMgBIMgAgyQAgyd/PnjkoWRfDcPzpPtta27Zt27Zt27Yf5fvNduasu7p79i5mMnfaFGmanPzTXPfYqIx6Qd8N3c6dY2gbHJvdVFg/kVHe/8/c1zsiX8yPSKu9rjhEhCRW5teNZVcOOvgmK/y3v2zYFmZezUhwYoVkB7n0l1/NU4u73UOytdbGpo7hHJ5zSuYoFvEIzbn3A7sFZ/lEFijdbwauOdXD+taBCufGxnpkZO+ThO8V1I3zi31voLvwjYei728TL8VRzV2i7usYhnYh3Py7X7ZXnI8DOwek48B3Kp2Y6Rqcae0R/+GPnWSJ+tIVUl/6Jx1HG88E4omOpd8zJMuif/PQduvIbsf4Afd1dgJMhphQ2b7ATHC0uGmKRvvYPnwx5+ofA/uwsLJjoXFgI6mgQ8FROOxW071S17Na1bEo2UQu/f1v28N9lq9+KjIA78h81WxMcsMJX3+3lMxBQYhptd0r9+6UmKOhf0PpOgekcbDE/LarrL2xq6hvLI2YFa+u6lzEyXHpG+gel9PCZJGuaT+RzSuOKr7lO6KW4R0iw7nxREgXdDxx5A6TCtph1vWuHl+SXNihzG8a3AQkNC7dziepbXRP4eMAhFDJEtWkQ0b2oWgNHyilq6b00pYZwRREV+bnz4VrW6/EiyCZcIxhzmZbyUWd142zmRX9LCG3OsUnpYIfllItX35F6bjdN32Xq2+FgiQEWgXJgmp7VrUPkkUsjnvzw0ojxhKkWWOpT3wdKFjWMiPX/ZFBskIqQPK5HwJMRDv4pnzWdcIxaOtZBYjnO7kRXQHJp7LJ3JqRL7rOMVlNtCva5jUu3SUoI6Woi2oidvQMz4Vf3bUkWaKa9OjMRgURRYVSTd3zakd5H7/9af3T2KPmcLmlW8wzJN8EkuFTstZInK3qXMLGZ/nxh5GImrb2R/lnSD5Lz5BM2RYFA2JLniFZNUgm7iM3p2pIdMtaZ+lmlPXRBgx4qwXFl1MtOw7JALAoYIiuwBLSd81KP0XNg1tNg1uSJepIh2hQ6eS/sOOQrJr04+QVnscSTvIkIJmEnWxdlMvwv+LGKWWIlw25IVeMv1J24LJefbOQQDLJJi9a+LnVwzSgr3rOkljz3cCNPfmfRqkd0fWPKaZNWspyaiYN/f/JuQsd2Y0lDMBPePmGmZmZmZmZmTmCoCAMwtDb5NP5pZLjOVvx8c44MFJpZfe63d3V1fUXeX7Kqw467hLtjCbXUstelfYjT7tmtpb3fiMiqm3Qzjx8E7ztd/QFL7z3vV4eOO7sG2uBWOG/LkKNQnR69T37ivt0IW0HHHvRGx//hJn88sTMn3z988RtLDM24CrnszWBZGNZSEJAIvZJsfSQbIa0TExdHW99+K1NCKKl3f/sh/iZ5QSSrcjyQ6tHWszqqTe/JHLIA1fd/ly/Wc3a/3nwGUQiQ3uV4MqMzQo59hkigcpMm5x7rWziwy9+ahR01R3PVxc7RROFvdR6dJDnjz3zBtcOl7m5IE4aJdKOPPVq4XTPX3n7c5mVwoh+7cib6cc6iV4ygmRM8AABO+TEy3p2rYu4L2Zy1uX33fbIOxkoTqTKDO38oYpXu+UV9ZDsyJOHbOLTb37ldMwQ4AYYbrjvVW+Iejn3qgdri/ew7sycrxEkG26YFFO2osvl3rDW0UdZVe3ErOmyzOiI9s4pHkLyYqMP6dm3v/Yv27QVkEyTWq3owUXXP3bHY+9FnYUcjLi86k3EEwIMDSTnmSHJxDS6htLMVpXOdcspdH3HY++OXkWxaj/xvFuqpWg2JFMllFpiU8N2YpHzjywBKMZ2cz5XR6dKGqDyAC3jqOeFUS747L9pZAOZRjQRpd9z/qEXPslsxZR0yax6SH7j4x/N36mQv7HXov2bCMNGI3v/TQ+87lgGkllR2PvgnjmrXVotODB/eJa9FvloNqtZOzPRtX/pdenNT6n4c4BnbFYsIW8Ww+S/gkB2/emX3JWCtSgRnDSNobckRx7Mw+EEP6++8wWGYy7+eciZGRcSMz11DyCNKOeoF1SN3P2b7n89ssHPHkKyHGdGZ//17Fojgfmkw2OFMyuz7xauhcHturQwo7aBZJyPoOIn/8kDSgJnCHADDFF09L69YAU6fU4WztQDq5A8eiAFNHi+odFtonOku4umyzKjhxpIXmb0QnSacFvKu+IIKt0ctUPoqLkKn/aQHDudYaVdBakLxPyfB8mUmu5OuA3Oq7w8z7imdj2Zdsb4LmOhhGOvkEwXUPel3YI9RqTdiJSLUO87ljGR4gUM5C6T0WCSgYbaDZY0nOdm5ZlS09F0PSRbnRGVV2xOCkGXmRCJvQauDzv5ylVINiuH0y7XvveQ3KwdSq0GgWdsFmISxUjKxEKB5GwfiU0CLMIPSIJJo3VFfbNFkh5LzA00kij/IrECcYHPzAoHmrVnVsJ9uQXtI0i2uTFKGBA9uzYByZXke/adb2ZDsu3T6NuK3Cp5cztDgBtgEJGK+RIbUSTj6be+ctFAsvl4gIYUFHG4sljdNzG6qIAIBxk79KQr+i4LjN5A8sKjq830JIW/RRXXUu4RNayEjhg31LN4NB2SQ9r5PXU7D5LLQKZPd/Ls63ZDkFw6hVPrdkZ6MpCsGM11PIBkaMxf4XqU8tAGZyc2nL/s5qdcJBKLooUp9x6S73z8fY9FQQc1e2JF5fkiCr0WPmxPTC8ris07EZKjypNbmgjJzdqtK/xZSy6ZvAV9yUAEIJAcWC0llb1LmuaB5z4aBZZY+soghJGFOk3Pzgp4CF/73imPCfZ6TMhniqDyC7Uw1HaC5IQoxIensGuN+559rMMubCCUPQ+Sk4oCh5kwjiVQOV2Ae2CIYZ1plLCJbdjoBpKROLm3RT3KrbjQsvbR2XZW7TauUd9lgdEbSF5y9Ni+EH3rvktmgQIJWjUmf1wEZkvs/RDHd0OQHP8m3sOfB5JLYsrJgBzzIPn4c24KJIu8FSQTzVENoXYC3XD+2rtfimMtOFwkRddDckrKAxUJMPZztkzHb0hxDZGFDNuPOfP6nKgk/+oNlFoPyYwwLc5bJRF/F5KbtUvW+hefeC2QnHr+5BTQ5bc8XZCc9aIoF9AIFysNERJu1cJJNdUkPuCTRjJGDYnSz4BkQK4FZBbcjiCZe+ovI28Ku9a17wXJkeqiguSqvvRAD8llV9VUQ5ynXoCnA0PVD9uIqolJYr6H5GJOSky8QeRj7aMLzIRFU7osMHoDyYuNbtNjh23vT4VQ+vKmpYYSqKFwSwetHZKZ1VoEHiP0iVb9+SHZuZU22yUkR8tjeFlF8T8azgfbyPe8imvIB5wCGGsUwfi48Gbo0vWQ7Dr6N92Df5yhZrOate8UuN7XzVotNqFfKI4GktkBlZgIeT4zTwEXAmwB4HSZAcmEU0vKGLmexDXGXCA5shEesnV6dq2RGkimQLQrQMsZj8vbQ3LyheHwfAFugUG1nb7F9vgDvrSZAskhYY/y3Uv4BQZ2OXrilA7OxC4LjN5A8mKj24jktrYOkikUNrUqTZyKQxb3RZFFggYpD0EjSA6aunD+p0Oy5xEEKm2O9Uo0BfoMsWlIrtFHkKxSVHu0Xg/J+W+4RCUxnEUvZ0Cyt+V3IcLDfLenCLnnfL7P4ydRzT725T9FNddWKkHKGvM8HYex2EuLWV2MnqRU10jceq/lAuY7chNehWS/w2BWznDKvrQ4vSKBlGBUNuBpNqtZO28svycj4ceyFiaNM7qvmxV7wmv9ihAWiQN7rYU0kFx5MqE5jbRMKiWjyLLGGLuuEXmYCMm19sqzOghSm/mVnjJxqryLQ2mqWWnPrgUgmaWe+iz7a8LkYRWSRfItML5+mRrYpa8NJbHQd7YAx5ZioBTZghJUAVLo7rXZ08TnwnA8lLfOtUZmsap4u8b2otNqc4vojajB2aNHRANLwy72tOmyzOi2DB9iLTk7rnVfZnSFYDH0h+26b0t5V85MyHcIaa8azkTARrnknLpQBS1DwyDkTr+DU9+QcJXq84aUsUSfFiTbv11CcjN6QfIoSQZaGkimMsKZEH3XfCVSymgAyb8wfYJVrus9193z8l45jyHhfAro4g+FaKhKOZd7PdT+Bx9/aWq8ixywTXxla3VJwfpEhDJdheQQKRqyNEXXJukkY36zWf3aGZQ58yGPadzXzaqvd+phggGY66dp4P1vIfn++oawukge0+Npd1vJ4xfe/97tqIAD36YIKsGL+kupUQwanBxJJqDCxry2Z9e6CNtXIXn000u2NeWKQ31asxomaLCXEijOi1jOFuDwYUhK32MiZ4hQfXdXVXhFKR3Qa9jCVg6ri2IiJAwze/RYciNy3psuy4xeZ6GIvlpm9CQxR0Qtb1HgGssoGibMKDQhfJcs3RCS10v2LB9N/rVIUAHHdh9XAdtcNymWnTi/SkJnbEzPTI8tyyMaJcm5TZBMJ5U6fUpxjNRe9s9MX3tASIjMTHa3WbLjJ3sPALMp02cFcjbH3rik/zvi3Nns+kMOCC9/Ri9IvzkB9iqScO5VD+LMxN/YZz8xvwItq29jfTI7NjR63+VX9u4AA0AABsPopQIgdIDQFbr/GRqDgkDrh8cDYAw+ZWpy+rv8dF/veiQZgHqt0gdfpvN3kuueU5IB7td8H/2Jy3RJBgAkGQAkGQCQZACQZABAkgFAkgEASQYASQYAJBkAJHnbT3vJA0CSl/WwlzwAJLmrHHhWBgBJzgIAJBkAJBkAkGQAkGQAQJIBQJLnXOyYA4+1SwzHv8hr27Zt27Zt27a5tm3btr0x7i+Zm8XB854ne5icpElmOui00/Y/0837zt95+g1av/OU8ujY6Svvv/xl4RR0/8XPXkOnM01Q1/4TNdm8fc/R+07c/Gnr+93Ke97KXU38xev2v/vu9MchYP/JWyoXSst69sF66fqDBjfduJmrr97/oG50+sLN4vynrjzV88GOXXi4YPUe0e4zfCbGHzR2vnw3MEVSdDlZep278ZJbMzaNzl5/IVSYMm+DfiRit1VbjnbqO/6fpp6/cjeGJUK1KKt9rzGL1+7fdeTahFlrFHLR5r3neg+boXtZiqRTWVPmb4TJfCaYYdUMyaOevLMIjMpKzauz94ykq+AraQUN4YmFdh4Rbv4JQ8YtYCbdjMLGoRMWabL5X4fA9IIGJ58Yr5CUJvQFMNjBOzTVxTf29VcHlQulZSVlV7/55khDmgaOmWflHNJv5Gwdme7Iuftop250+8HLqJCQWZmQVaXnO41LL3/1xU60Zy3dxiWSy2S7gXw6f/MV+KF7BWW4nCy9UnJrrz34SMOoyNE7GhUIBO3aFkPFppcrMHm6RaeU4DDJubVYY+7ynYLPCy8sPp8zbN1/oSm4IpOKmClo9dbjWpG1bMMhLis5p4YYR9wPGx8BZg6eUXQF8/TVZ7qTBZFw8BY4X/560NWpXiQH+PEZFTDDEwr+f9yYyVy49g1LU85Z7386KzscHqYhJONwzDx05q4Cn9jGlaXXai5LgvhVsJy/rEEgWdDD178NC8ltdwPNySMoydU/XucKync59DJdSBZEitcuJFs4BuEnCkyeMsBDj8FTsST4QfiLmhbSidmWkOwekMCLGQjp3G9CUHQO8MOStssCz0ZNWSYmUEhDYsc+4y7cek2gzVqyDSZ/A5ETdCSLNhjpE5oGdjZBso5kUWZoqh2u3XGyybxmMjFI5tWsCUr9sPbBXXBlIIFSnmAu33SYWCL14Cs85dTlLMJsz7HrYCdEA6JepA4mnX1iAZ6mH3BIbC6N2cu2X7rzlpmX775jOVENc8TkpbRFeNPYduCiXEj+be/PvxNqSk8iMN79cKaaTV5AL76nMFduPnrl3nuWX7z9RqggURi0dQtHC8xCFQ5zhcTlwafoRGmd+OTA/OkJKgUbwse8TZ/RwOhsupyN6JKAZNRx8YvjqEwmXIdPXKwtNHr73ZE75cBoLSCZd7cwl0LNc+Pus2gk3CAUZdVBlxq9SCUvP9uxVqjAr4U/ExZGHLvRgKYt2CT9nyahsxw7kKEExz8ic8/xG2yIYV98tIEp7hGlhBsjSHxNnr6zFKd98cmWBtcEDCu7nIReFA+p/aACB0A1iqItIZluVHKxtUuomExJhgTNqezcw0Upsu30xeI/9u1CR5pbiQLww1xmJsHlMDMzMzMzMzMzRxRmZlE4D5C3yCcdpTTpnvY/s7MdWK1UGnncbkO5XKfA/SxX6fwr77IuqzvvijtUUuXlbjq/Yu99SG5vTYex88IJ7klRpR9l5Az+9Pf/jfc2iRn6v+yGB1OW2/JIJGbxsSYbvPLuF3ZBgVAR18TtLE1Lx2qksVDiamIABcnjjNVNxmkpzfTDw8JVSCaUa8wq0VA2+JjTLmdaHn/mVVI+UUMONgUnu3nbA0/rZ0hniRs75xogBUTfDcEkFVC646xLbnVWFW69/6mEaPx6/ZEn31R58LHnK6uk+xTeYxPMCckWss/hZ3j94mvvq8qX3vncuqhXGJxYcazpyQkgZumQI2uZXtStQrwByWyL8tdTbNQ5U2OIh86wBnqA6DiJA8YagmT9G2j7PY+GGWdfetuv/rquysXpvsdfzuQpTRMIJINe87Sc2j6krKVdO+Kki+kUkxkSg6F1xcy312x8OU7xYcvpCExQcyox7zQDSGtvtrt3Yy3R7yrxFv5RhfoH88wglZwwi2I2qTTQvY+9xIkxN3+jEKE4TOqL3NC6eDDAz9JMngfmFQeqINkWWyn+aFbiAeyPOuXSws7FiVmW2KbrCBXVMJO9Dz1NIQKMOpDc3po+Y+eCEwctoOv4Gy6cqXxTB5KZX8+9/lHsMyZsLKFlHIsYlGfsBAUdDcoo99fvSGOFupA88lhuPFRiYpVWJiTDLXtMQU86YZQaKeFOVdC1HdmTjeM71t+5IBnRC1pWuKaIG8dzXSRw7Ux2ILl4omdrnCtwHZ37239sAHStJaqHn6QfGay0oYhTOZWHjB5PKUcjHnbChbGLhyCZ9+Mt7hHnw982UXNUdoj3P1QJvQx6xU0P9wPXuNeB5Gdf+6j2CAI1IHloXeZ/x0PPLjlwzdzRFW5vuv2BVQmSVYI9ZTKjDO/tskLJsKlCMoYXQGVPxLzT2HxYNg2R66wLEpdgAOBJSGZmYY7gUO2O7WMBaIBAgq4W369AsmknbunGA3U8CyS3t6bD2HnhRGDD6y5OwlrLZJEUTvQh+ZDjzveXbcoyyEYQ6eUaixrxlxKrfRc10b+t0VJXdnOksdqQPMZYTHOScMu9T/7AIHAVkln9pB/Fy1SgOIYaJ7ToGOciVZSU85NDvvIgWRCyIuefzQ/J8YD5HEJwUT05WrT/5EwYs1N5yG/z1I4UcdqGIBl4SD1oH4emfaGD//Hm1wQFhyolJnT47w12nAWSOZEwYBZInrou5r9KfF4klyyKgy36ITyuoQaS1dQt8eg1NuVH35ye9i6yYt2jT73F4TAlNx5IlKezQ7JsXzRpH5L1HHZVBsffxGBCVO3i+xVIZht1Xp8Rkhsi12HsXHASRGd0YsI//r81Pneym52/gF+uRPxAKscjQrj4WAX2ImrV2LtES0vGRyxCYDnSWC1IHmGsf62/I+llpv/wIHAVkqWOZGuQzXY4FZyE9ivUPZ1ry2XpgmSVHoPTywXJdV2LHSDG+N1CMuep1sWp9XpiRG1INu1A8rmX31Fesn4kKSvfrNIXMlN5yBBRsPzZr3dZVMKzrgQvLhvxmZIDg2TKDUjGfzHe7BeQGILkxrrAg+/i+tNwhT45vxkJ/HzwyZd6E3QtSE5kO5AsVTyZYNMAIkbreYu+Y6daDviZC5JNkr9bdxi9IkmpnISIMDiEK6kjz0lsLy+BZDDTh2SKO5kjk2lAcmdrGoydKw+aiwhJOlAdHWYO3T+Sf/EIAi0+VuK9yVIX2XRPKbEyoaRpRxqrBckjjGUU6msVTVd+4BrmOZZOrNsoTn7khgDRL4AcqBCUDiTTEYK34nWzQDInUmP9R8HRiY4K58OjxSG5MVapZjEAlQLIDUhGyo6Bd+PezQXJGEItepG+dh1DsFQ/U3mocVxe3LY1bmqUetI5r9RUC1eAZQBSDdWvw8VFQv8mc8t9T/nA0fT6kCwFG8BGHFmRRl9lQFDTHhKDxrrAG/1CwGh8lmKFSQ1qdGEArG58B4ylQrgJD1x49d2GgLJTIdnWJ/9i8kCoItv2RdnuS5cqmE9T5LrrMnpiHvRm3GLoXrnkP/9r01yUNSuVjA8Sq2cT5uKIQo8HyQbyRTXvlryZVQeSIZ8lcNyHtmYqYxtwguGOWIic5EZCGKgTSiNX//DZuCi32TMH0ps7cdhFwifXgrEEDK/mHatyCmK51fjHv/tPgkDsTg3igNrHkcZKnt4a3XSRsVYQfB5prIg3wa7K3CFdpRUIyXyvqC1EaGiufFyorIYFHSu72suWpbG7xJPGKZTt9AxO0rIipZRv9Bo9Ip1ZkMynVOmWdV/vuPXQmHxjrFBWgXbe7/goXFdh+5Bc9xiRyuRB+8Qx6kMyBQdX8i0monSk/Ro8dFU41nFihrRVdZ5K21EByQChSsc++LE4UR9ZphH7getQIWJgm6dIvyhQBH0xaKwrdl4qJx19TEtaEcH7oakK8OBhZqvz+BOXXv+AdzuQHOMyvEIQqAIz2TLY4KkJNEWuuy7rDebhA3uiPnXNZav0AwKTzrBYAqZN2nPcx4NkxycDMTJMtQPJeQSYh7ZmKmOHKNcYi5gC4Ty/LfJpsXXAq1lIz24ORqqTvZ68pei+cSqXMBa57Yzlyn3ATznrJbSjjtWp5J2PNBbqVObYrtKK/S6ZAdtRT/w8R7ebS16YWHzp9ntIjFxoyqxeMg8FAKbysE/MXqbxjN9MO7rLvt02YpaWvNuhJcy+LjWSAv2Pgugg+ftZLnklXLxGMgQnNc7KMlImOSOBnLQfmxiCLuvNvTXzM7ZtCkOLRtA7p8C58B3jVEESXetnypc8FsqlP3YAMRh/rEkaf6yv2DsDTymiOIz+O4GAoiABSEgSkIJ4hCIkFS8EoRRSFsgD5YFUQCQEhYJQAIT+iE4+1s/s7LjWbHdxOLh73+zsCL7m3pnviFUhs0dyEBHhLjY7/f5WK2Iks4qbZZYZERFh65d7RH9LjGQREREjWURERIxkERERI1lERESMZBEREdmRSOYdRHphAq8nVuFgJlMqshm8dUqHbePBlHKk22H6MW+sShtcCeVTFCMw2BVERMRIpmO2On8oFqBziu6eQRc0YgPmG4VfHFahliHzNBnRztPYPkG/FRqA6WNqaWI7KTWkram2avNzDEREpBtGMj37pCaFbS16hlpVP0GtcZ+b+SM5zZdp7RYRkW4YyZSmYllIAG8vklGGRUQfx071ltA7T/F1NP7pZ6ZdOQcPfgvjGMFJRxgxHHFbIpklaDr9OcPzl2+WnZc01VFgy005i+2ZBJqHSWLm47GvPgw6ihmIiIj0ieR496iWJaKQ6s8Yydhn7zx4BhFU0AiNZ5tM5QyDEwK6AoQ8/OeAbzF59uIeB0dsx8dAcnNado7ZkEbhwjGJZK6cM7DEHTUh1xxvBAvRnCSmvOgUoxdFGIDd6NOXXzWSyW8ctAxERET6RPLB4QfuTRkgJ0FIMmMkc/PKDTFUrSzfXY1kDEjRw5GLRCmDMHAYk6/R6h07da4uXMevlxJ5xgghoipCScuTaHTok9kIDTmA226SeHThmtX7/LSIiEifSCalkJShXsHhFbX7VveSRyM51lJAGMye7rpIRhSD0jhGOYTKBPBgL5mLj4CPdexo75DUBh5eYyk7JtHRSKadO946ERGRDpEc33WFHP3/kRyzLBy++zwRyYH3snDCsxkc5+iopp596wwyH/AMMnnz3iPGePHI6RrJON5jyBcREekQyTwMxa1kxsAKNvusNZLJ7KMnznB7WhMU4TmTLDVvHMl8nbefWyKZ2+J/F3DkJB8xz1+9vs/FRHfPc17rIpkxf2V/mujFFLv/cHHl2t1Mcv4Ll2/wyhNH1kjmxjpPgYmIiHSI5K8/frOHmjEsDt6y7RqBPMowQisgkK+RnEmCeTqSebBrNJLzdUJxecJb95+ui+QcfGnvNh+fLF7zwFdm+FOeGnv84hVr76uRzFL8959/cjCDHMwl5frff/zGInmNZPJb2XMrIiJGsmT9+fjp840HE8zcZNcZdpTpQhk9LUsC/vP+ba+OaQAAAAAE9W9tCU82OgCAkgFAyQCAkgFAyQCAkgFAyQCAkgFAyQCAkgHgoWQAUDIAoGQAUDIAoGQAUDIAoGQAIFuSF99xMhs6AAAAAElFTkSuQmCC)

#### Advanced: Create a release train with additional environments[​](#advanced-create-a-release-train-with-additional-environments "Direct link to Advanced: Create a release train with additional environments")

Large and complex enterprises sometimes require additional layers of validation before deployment. Learn how to add these checks with dbt.

Are you sure you need this?

This approach can increase release safety, but creates additional manual steps in the deployment process as well as a greater maintenance burden.

As such, it may slow down the time it takes to get new features into production.

The team at Sunrun maintained a SOX-compliant deployment in dbt while reducing the number of environments. Check out [their Coalesce presentation](https://www.youtube.com/watch?v=vmBAO2XN-fM) to learn more.

In this section, we will add a new **QA** environment. New features will branch off from and be merged back into the associated `qa` branch, and a member of your team (the "Release Manager") will create a PR against `main` to be validated in the CI environment before going live.

The git flow will look like this:

[![git flow diagram with an intermediary branch](/img/best-practices/environment-setup/many-branch-git.png?v=2 "git flow diagram with an intermediary branch")](#)git flow diagram with an intermediary branch

##### Advanced prerequisites[​](#advanced-prerequisites "Direct link to Advanced prerequisites")

* You have the **Development**, **CI**, and **Production** environments, as described in [the Baseline setup](https://docs.getdbt.com/guides/set-up-ci.md).

##### 1. Create a `release` branch in your git repo[​](#1-create-a-release-branch-in-your-git-repo "Direct link to 1-create-a-release-branch-in-your-git-repo")

As noted above, this branch will outlive any individual feature, and will be the base of all feature development for a period of time. Your team might choose to create a new branch for each sprint (`qa/sprint-01`, `qa/sprint-02`, etc), tie it to a version of your data product (`qa/1.0`, `qa/1.1`), or just have a single `qa` branch which remains active indefinitely.

##### 2. Update your Development environment to use the `qa` branch[​](#2-update-your-development-environment-to-use-the-qa-branch "Direct link to 2-update-your-development-environment-to-use-the-qa-branch")

See [Custom branch behavior](https://docs.getdbt.com/docs/dbt-cloud-environments.md#custom-branch-behavior). Setting `qa` as your custom branch ensures that the IDE creates new branches and PRs with the correct target, instead of using `main`.

[![A demonstration of configuring a custom branch for an environment](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/dev-environment-custom-branch.png?v=2 "A demonstration of configuring a custom branch for an environment")](#)A demonstration of configuring a custom branch for an environment

##### 3. Create a new QA environment[​](#3-create-a-new-qa-environment "Direct link to 3. Create a new QA environment")

See [Create a new environment](https://docs.getdbt.com/docs/dbt-cloud-environments.md#create-a-deployment-environment). The environment should be called **QA**. Just like your existing Production and CI environments, it will be a Deployment-type environment.

Set its branch to `qa` as well.

##### 4. Create a new job[​](#4-create-a-new-job "Direct link to 4. Create a new job")

Use the **Continuous Integration Job** template, and call the job **QA Check**.

In the Execution Settings, your command will be preset to `dbt build --select state:modified+`. Let's break this down:

* [`dbt build`](https://docs.getdbt.com/reference/commands/build.md) runs all nodes (seeds, models, snapshots, tests) at once in DAG order. If something fails, nodes that depend on it will be skipped.
* The [`state:modified+` selector](https://docs.getdbt.com/reference/node-selection/methods.md#state) means that only modified nodes and their children will be run ("Slim CI"). In addition to [not wasting time](https://discourse.getdbt.com/t/how-we-sped-up-our-ci-runs-by-10x-using-slim-ci/2603) building and testing nodes that weren't changed in the first place, this significantly reduces compute costs.

To be able to find modified nodes, dbt needs to have something to compare against. Normally, we use the Production environment as the source of truth, but in this case there will be new code merged into `qa` long before it hits the `main` branch and Production environment. Because of this, we'll want to defer the Release environment to itself.

##### Optional: also add a compile-only job[​](#optional-also-add-a-compile-only-job "Direct link to Optional: also add a compile-only job")

dbt uses the last successful run of any job in that environment as its [comparison state](https://docs.getdbt.com/reference/node-selection/syntax.md#about-node-selection). If you have a lot of PRs in flight, the comparison state could switch around regularly.

Adding a regularly-scheduled job inside of the QA environment whose only command is `dbt compile` can regenerate a more stable manifest for comparison purposes.

##### 5. Test your process[​](#5-test-your-process "Direct link to 5. Test your process")

When the Release Manager is ready to cut a new release, they will manually open a PR from `qa` into `main` from their git provider (e.g. GitHub, GitLab, Azure DevOps). dbt will detect the new PR, at which point the existing check in the CI environment will trigger and run. When using the [baseline configuration](https://docs.getdbt.com/guides/set-up-ci.md), it's possible to kick off the PR creation from inside of the Studio IDE. Under this paradigm, that button will create PRs targeting your QA branch instead.

To test your new flow, create a new branch in the Studio IDE then add a new file or modify an existing one. Commit it, then create a new Pull Request (not a draft) against your `qa` branch. You'll see the integration tests begin to run. Once they complete, manually create a PR against `main`, and within a few seconds you’ll see the tests run again but this time incorporating all changes from all code that hasn't been merged to main yet.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Integrate with dbt Semantic Layer using best practices

[Back to guides](https://docs.getdbt.com/guides.md)

Semantic Layer

Best practices

Advanced

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

To fit your tool within the world of the Semantic Layer, dbt Labs offers some best practice recommendations for how to expose metrics and allow users to interact with them seamlessly.

This is an evolving guide that is meant to provide recommendations based on our experience. If you have any feedback, we'd love to hear it!

📹 Learn about the dbt Semantic Layer with on-demand video courses!

Explore our [dbt Semantic Layer on-demand course](https://learn.getdbt.com/courses/semantic-layer) to learn how to define and query metrics in your dbt project.

Additionally, dive into mini-courses for querying the dbt Semantic Layer in your favorite tools: [Tableau](https://courses.getdbt.com/courses/tableau-querying-the-semantic-layer), [Excel](https://learn.getdbt.com/courses/querying-the-semantic-layer-with-excel), [Hex](https://courses.getdbt.com/courses/hex-querying-the-semantic-layer), and [Mode](https://courses.getdbt.com/courses/mode-querying-the-semantic-layer).

##### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

To build a Semantic Layer integration:

* We offer a [JDBC](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md) API and [GraphQL API](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md). Refer to the dedicated [Semantic Layer API](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) for more technical integration details.

* Familiarize yourself with the [Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md) and [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md)'s key concepts. There are two main objects:

  * [Semantic models](https://docs.getdbt.com/docs/build/semantic-models.md) — Nodes in your semantic graph, connected via entities as edges. MetricFlow takes semantic models defined in YAML configuration files as inputs and creates a semantic graph that you can use to query metrics.
  * [Metrics](https://docs.getdbt.com/docs/build/metrics-overview.md) — Can be defined in the same YAML files as your semantic models, or split into separate YAML files into any other subdirectories (provided that these subdirectories are also within the same dbt project repo).

##### Connection parameters[​](#connection-parameters "Direct link to Connection parameters")

The dbt Semantic Layer APIs authenticate with `environmentId`, `SERVICE_TOKEN`, and `host`.

We recommend you provide users with separate input fields with these components for authentication (dbt will surface these parameters for the user).

##### Exposing metadata to dbt Labs[​](#exposing-metadata-to-dbt-labs "Direct link to Exposing metadata to dbt Labs")

When building an integration, we recommend you expose certain metadata in the request for analytics and troubleshooting purpose.

Please send us the following header with every query:

`'X-dbt-partner-source': 'Your-Application-Name'`

Additionally, it would be helpful if you also included the email and username of the person generating the query from your application.

#### Use best practices when exposing metrics[​](#use-best-practices-when-exposing-metrics "Direct link to Use best practices when exposing metrics")

Best practices for exposing metrics are summarized into five themes:

* [Governance](#governance-and-traceability) — Recommendations on how to establish guardrails for governed data work.
* [Discoverability](#discoverability) — Recommendations on how to make user-friendly data interactions.
* [Organization](#organization) — Organize metrics and dimensions for all audiences, use [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md).
* [Query flexibility](#query-flexibility) — Allow users to query either one metric alone without dimensions or multiple metrics with dimensions.
* [Context and interpretation](#context-and-interpretation) — Contextualize metrics for better analysis; expose definitions, metadata, lineage, and freshness.

##### Governance and traceability[​](#governance-and-traceability "Direct link to Governance and traceability")

When working with more governed data, it's essential to establish clear guardrails. Here are some recommendations:

* **Aggregations control** — Users shouldn't generally be allowed to modify aggregations unless they perform post-processing calculations on Semantic Layer data (such as year-over-year analysis).

* **Time series alignment and using metric\_time** — Make sure users view metrics across the correct time series. When displaying metric graphs, using a non-default time aggregation dimension might lead to misleading interpretations. While users can still group by other time dimensions, they should be careful not to create trend lines with incorrect time axes.<br /><br />When looking at one or multiple metrics, users should use `metric_time` as the main time dimension to guarantee they are looking at the right time series for the metric(s).<br /><br />As such, when building an application, we recommend exposing `metric_time` as a separate, "special" time dimension on its own. This dimension is always going to align with all metrics and be common across them. Other time dimensions can still be looked at and grouped by, but having a clear delineation between the `metric_time` dimension and the other time dimensions is clarifying so that people do not confuse how metrics should be plotted.<br /><br />Also, when a user requests a time granularity change for the main time series, the query that your application runs should use `metric_time` as this will always give you the correct slice. Related to this, we also strongly recommend that you have a way to expose what dimension `metric_time` actually maps to for users who may not be familiar. Our APIs allow you to fetch the actual underlying time dimensions that makeup metric\_time (such as `transaction_date`) so you can expose them to your users.

* **Units consistency** — If units are supported, it's vital to avoid plotting data incorrectly with different units. Ensuring consistency in unit representation will prevent confusion and misinterpretation of the data.

* **Traceability of metric and dimension changes** — When users change names of metrics and dimensions for reports, it's crucial to have a traceability mechanism in place to link back to the original source metric name.

##### Discoverability[​](#discoverability "Direct link to Discoverability")

* Consider treating [metrics](https://docs.getdbt.com/docs/build/metrics-overview.md) as first-class objects rather than measures. Metrics offer a higher-level and more contextual way to interact with data, reducing the burden on end-users to manually aggregate data.

* **Easy metric interactions** — Provide users with an intuitive approach to:

  * Search for Metrics — Users should be able to easily search and find relevant metrics. Metrics can serve as the starting point to lead users into exploring dimensions.
  * Search for Dimensions — Users should be able to query metrics with associated dimensions, allowing them to gain deeper insights into the data.
  * Filter by Dimension Values — Expose and enable users to filter metrics based on dimension values, encouraging data analysis and exploration.
  * Filter additional metadata — Allow users to filter metrics based on other available metadata, such as metric type and default time granularity.

* **Suggested metrics** — Ideally, the system should intelligently suggest relevant metrics to users based on their team's activities. This approach encourages user exposure, facilitates learning, and supports collaboration among team members.

By implementing these recommendations, the data interaction process becomes more user-friendly, empowering users to gain valuable insights without the need for extensive data manipulation.

##### Organization[​](#organization "Direct link to Organization")

We recommend organizing metrics and dimensions in ways that a non-technical user can understand the data model, without needing much context:

* **Organizing dimensions** — To help non-technical users understand the data model better, we recommend organizing dimensions based on the entity they originated from. For example, consider dimensions like `user__country` and `product__category`.<br /><br />You can create groups by extracting `user` and `product` and then nest the respective dimensions under each group. This way, dimensions align with the entity or semantic model they belong to and make them more user-friendly and accessible. Additionally, we recommending adding a `label` parameter to dimensions in order to define the value displayed in downstream tools.

* **Organizing metrics** — The goal is to organize metrics into a hierarchy in our configurations, instead of presenting them in a long list.<br /><br />This hierarchy helps you organize metrics based on specific criteria, such as business unit or team. By providing this structured organization, users can find and navigate metrics more efficiently, enhancing their overall data analysis experience.

* **Using saved queries** — The Semantic Layer has a concept of [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md) which allows users to pre-build slices of metrics, dimensions, filters to be easily accessed. You should surface these as first class objects in your integration. Refer to the [JDBC](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md) and [GraphQL](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md) APIs for syntax.

##### Query flexibility[​](#query-flexibility "Direct link to Query flexibility")

Allow users to query either one metric alone without dimensions or multiple metrics with dimensions.

* Allow toggling between metrics/dimensions seamlessly.

* Be clear on exposing what dimensions are queryable with what metrics and hide things that don’t apply. (Our APIs provide calls for you to get relevant dimensions for metrics, and vice versa).

* Only expose time granularities (monthly, daily, yearly) that match the available metrics.

  * For example, if a dbt model and its resulting semantic model have a monthly granularity, make sure querying data with a 'daily' granularity isn't available to the user. Our APIs have functionality that will help you surface the correct granularities

* We recommend that time granularity is treated as a general time dimension-specific concept and that it can be applied to more than just the primary aggregation (or `metric_time`).

  Consider a situation where a user wants to look at `sales` over time by `customer signup month`; in this situation, having the ability to apply granularities to both time dimensions is crucial. Our APIs include information to fetch the granularities for the primary (metric\_time) dimensions, as well as all time dimensions.

  You can treat each time dimension and granularity selection independently in your application. Note: Initially, as a starting point, it makes sense to only support `metric_time` or the primary time dimension, but we recommend expanding that as your solution evolves.

* You should allow users to filter on date ranges and expose a calendar and nice presets for filtering these.

  * For example, last 30 days, last week, and so on.

##### Context and interpretation[​](#context-and-interpretation "Direct link to Context and interpretation")

For better analysis, it's best to have the context of the metrics close to where the analysis is happening. We recommend the following:

* Expose business definitions of the metrics as well as logical definitions.

* Expose additional metadata from the Semantic layer (measures, type parameters).

* Use the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) to enhance the metric and build confidence in its accuracy:

  * Check if the metric is fresh and when it was last updated.
  * Include lineage information to understand the metric's origin.

* Allow for creating other metadata that’s useful for the metric. We can provide some of this information in our configuration (Display name, Default Granularity for View, Default Time range), but there may be other metadata that your tool wants to provide to make the metric richer.

##### Transparency and using compile[​](#transparency-and-using-compile "Direct link to Transparency and using compile")

For transparency and additional context, we recommend you have an easy way for the user to obtain the SQL that MetricFlow generates. Depending on what API you are using, you can do this by using our `compile` parameter. This is incredibly powerful and emphasizes transparency and openness, particularly for technically inclined users.

##### Where filters and optimization[​](#where-filters-and-optimization "Direct link to Where filters and optimization")

In the cases where our APIs support either a string or a filter list for the `where` clause, we always recommend that your application utilizes the filter list in order to gain maximum pushdown benefits. The `where` string may be more intuitive for users writing queries during testing, but it will not have the performance benefits of the filter list in a production environment.

#### Understand stages of an integration[​](#understand-stages-of-an-integration "Direct link to Understand stages of an integration")

These are recommendations on how to evolve a Semantic Layer integration and not a strict runbook.

**Stage 1 - The basic**

* Supporting and using [JDBC](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md) or [GraphQL](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md) is the first step. Refer to the [Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) for more technical details.

**Stage 2 - More discoverability and basic querying**

* Support listing metrics defined in the project
* Listing available dimensions based on one or many metrics
* Querying defined metric values on their own or grouping by available dimensions
* Display metadata from [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) and other context
* Expose [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md), which are pre-built metrics, dimensions, and filters that Semantic Layer developers create for easier analysis. You can expose them in your application. Refer to the [JDBC](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md) and [GraphQL](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md) APIs for syntax.

**Stage 3 - More querying flexibility and better user experience (UX)**

* More advanced filtering

  <!-- -->

  * Time filters with good presets/calendar UX
  * Filtering metrics on a pre-populated set of dimension values

* Make dimension values more user-friendly by organizing them effectively

* Intelligent filtering of metrics based on available dimensions and vice versa

**Stage 4 - More custom user interface (UI) / Collaboration**

* A place where users can see all the relevant information about a given metric
* Organize metrics by hierarchy and more advanced search features (such as filter on the type of metric or other metadata)
* Use and expose more metadata
* Querying dimensions without metrics and other more advanced querying functionality
* Suggest metrics to users based on teams/identity, and so on.

##### Related docs[​](#related-docs "Direct link to Related docs")

* [Semantic Layer FAQs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-faqs.md)
* [Use the Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md) to learn about the product.
* [Build your metrics](https://docs.getdbt.com/docs/build/build-metrics-intro.md) for more info about MetricFlow and its components.
* [Semantic Layer integrations page](https://www.getdbt.com/product/semantic-layer-integrations) for information about the available partner integrations.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Legacy dbt Semantic Layer migration guide

[Back to guides](https://docs.getdbt.com/guides.md)

Semantic Layer

Migration

Intermediate

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

The legacy Semantic Layer will be deprecated in H2 2023. Additionally, the `dbt_metrics` package will not be supported in dbt v1.6 and later. If you are using `dbt_metrics`, you'll need to upgrade your configurations before upgrading to v1.6. This guide is for people who have the legacy dbt Semantic Layer setup and would like to migrate to the new dbt Semantic Layer. The estimated migration time is two weeks.

#### Migrate metric configs to the new spec[​](#migrate-metric-configs-to-the-new-spec "Direct link to Migrate metric configs to the new spec")

The metrics specification in dbt Core is changed in v1.6 to support the integration of MetricFlow. It's strongly recommended that you refer to [Build your metrics](https://docs.getdbt.com/docs/build/build-metrics-intro.md) and before getting started so you understand the core concepts of the Semantic Layer.

dbt Labs recommends completing these steps in a local dev environment (such as the [dbt CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md)) instead of the Studio IDE:

1. Create new Semantic Model configs as YAML files in your dbt project.\*

2. Upgrade the metrics configs in your project to the new spec.\*

3. Delete your old metrics file or remove the `.yml` file extension so they're ignored at parse time. Remove the `dbt-metrics` package from your project. Remove any macros that reference `dbt-metrics`, like `metrics.calculate()`. Make sure that any packages you’re using don't have references to the old metrics spec.

4. Install the [dbt CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md) to run MetricFlow commands and define your semantic model configurations.

   * If you're using dbt Core, install the [MetricFlow CLI](https://docs.getdbt.com/docs/build/metricflow-commands.md) with `python -m pip install "dbt-metricflow[your_adapter_name]"`. For example:
```

Example 4 (unknown):
```unknown
**Note** - MetricFlow commands aren't yet supported in the Studio IDE at this time.

5. Run `dbt parse`. This parses your project and creates a `semantic_manifest.json` file in your target directory. MetricFlow needs this file to query metrics. If you make changes to your configs, you will need to parse your project again.

6. Run `mf list metrics` to view the metrics in your project.

7. Test querying a metric by running `mf query --metrics <metric_name> --group-by <dimensions_name>`. For example:
```

---

## can hold the '_update' that's added

**URL:** llms-txt#can-hold-the-'_update'-that's-added

schema_seed_added_yml = """
version: 2
seeds:
  - name: added
    config:
      column_types:
        name: varchar(64)
"""

class TestSnapshotCheckColsRedshift(BaseSnapshotCheckCols):
    # Redshift defines the 'name' column such that it's not big enough
    # to hold the '_update' added in the test.
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "base.csv": seeds_base_csv,
            "added.csv": seeds_added_csv,
            "seeds.yml": schema_seed_added_yml,
        }

import pytest
from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations

class TestSimpleMaterializationsBigQuery(BaseSimpleMaterializations):
    @pytest.fixture(scope="class")
    def test_config(self):
        # effect: add '--full-refresh' flag in requisite 'dbt run' step
        return {"require_full_refresh": True}

def pytest_addoption(parser):
    parser.addoption("--profile", action="store", default="apache_spark", type=str)

**Examples:**

Example 1 (unknown):
```unknown
As another example, the `dbt-bigquery` adapter asks users to "authorize" replacing a table with a view by supplying the `--full-refresh` flag. The reason: In the table materialization logic, a view by the same name must first be dropped; if the table query fails, the model will be missing.

Knowing this possibility, the "base" test case offers a `require_full_refresh` switch on the `test_config` fixture class. For BigQuery, we'll switch it on:

tests/functional/adapter/test\_basic.py
```

Example 2 (unknown):
```unknown
It's always worth asking whether the required modifications represent gaps in perceived or expected dbt functionality. Are these simple implementation details, which any user of this database would understand? Are they limitations worth documenting?

If, on the other hand, they represent poor assumptions in the "basic" test cases, which fail to account for a common pattern in other types of databases-—please open an issue or PR in the `dbt-core` repository on GitHub.

##### Running with multiple profiles[​](#running-with-multiple-profiles "Direct link to Running with multiple profiles")

Some databases support multiple connection methods, which map to actually different functionality behind the scenes. For instance, the `dbt-spark` adapter supports connections to Apache Spark clusters *and* Databricks runtimes, which supports additional functionality out of the box, enabled by the Delta file format.

tests/conftest.py
```

---

## Configuring in a SQL file is a legacy method and not recommended. Use the YAML file instead.

**URL:** llms-txt#configuring-in-a-sql-file-is-a-legacy-method-and-not-recommended.-use-the-yaml-file-instead.

**Contents:**
  - Environment variable configs

{% snapshot snapshot_name %}

{{ config(
  enabled=true | false
) }}

data_tests:
  <resource-path>:
    +enabled: true | false

{% test <testname>() %}

{{ config(
  enabled=true | false
) }}

{{ config(
  enabled=true | false
) }}

unit_tests:
  <resource-path>:
    +enabled: true | false

unit_tests:
  - name: [<test-name>]
    config:
      enabled: true | false

sources:
  <resource-path>:
    +enabled: true | false

sources:
  - name: [<source-name>]
    config:
      enabled: true | false
    tables:
      - name: [<source-table-name>]
        config:
          enabled: true | false

metrics:
  <resource-path>:
    +enabled: true | false

metrics:
  - name: [<metric-name>]
    config:
      enabled: true | false

exposures:
  <resource-path>:
    +enabled: true | false

exposures:
  - name: [<exposure-name>]
    config:
      enabled: true | false

semantic-models:
  <resource-path>:
    +enabled: true | false

semantic_models:
  - name: [<semantic_model_name>]
    config:
      enabled: true | false

saved-queries:
  <resource-path>:
    +enabled: true | false

saved_queries:
  - name: [<saved_query_name>]
    config:
      enabled: true | false

models:
  segment:
    base:
      segment_web_page_views:
        +enabled: false

$ export DBT_<THIS-CONFIG>=True
dbt run

**Examples:**

Example 1 (unknown):
```unknown
dbt\_project.yml
```

Example 2 (unknown):
```unknown
tests/\<filename>.sql
```

Example 3 (unknown):
```unknown
tests/\<filename>.sql
```

Example 4 (unknown):
```unknown
💡Did you know...

Available from dbt v

<!-- -->

1.8

<!-- -->

or with the

<!-- -->

[dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md).

dbt\_project.yml
```

---

## clone one_specific_model of my models from specified state to my target schema(s)

**URL:** llms-txt#clone-one_specific_model-of-my-models-from-specified-state-to-my-target-schema(s)

dbt clone --select "one_specific_model" --state path/to/artifacts

---

## Snapshot freshness for multiple particular source tables:

**URL:** llms-txt#snapshot-freshness-for-multiple-particular-source-tables:

**Contents:**
  - How do I specify column types?
  - How do I test and document seeds?
  - How do I test one model at a time?
  - How do I transfer account ownership to another user?
  - How do I use the 'Custom Branch' settings in a dbt Environment?
  - How do I write long-form explanations in my descriptions?
  - How often should I run the snapshot command?
  - How should I structure my project?
  - How to delete a job or environment in dbt?
  - How to generate HAR files

$ dbt source freshness --select source:jaffle_shop.orders source:jaffle_shop.customers

select
    id,
    created::timestamp as created
from some_other_table

create table dbt_alice.my_table
  id integer,
  created timestamp;

insert into dbt_alice.my_table (
  select id, created from some_other_table
)

create table dbt_alice.my_table as (
  select id, created from some_other_table
)

seeds:
  - name: country_codes
    description: A mapping of two letter country codes to country names
    columns:
      - name: country_code
        data_tests:
          - unique
          - not_null
      - name: country_name
        data_tests:
          - unique
          - not_null

dbt test --select customers

models:
  - name: customers
    description: >
      Lorem ipsum **dolor** sit amet, consectetur adipisicing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
      quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
      consequat.

models:
  - name: customers
    description: |
      ### Lorem ipsum

* dolor sit amet, consectetur adipisicing elit, sed do eiusmod
      * tempor incididunt ut labore et dolore magna aliqua.

sources:
  - name: jaffle_shop
    database: raw
    quoting:
      database: true
      schema: true
      identifier: true

tables:
      - name: order_items
      - name: orders
        # This overrides the `jaffle_shop` quoting config
        quoting:
          identifier: false

Access denied: BigQuery BigQuery: Permission denied while getting Drive credentials

gcloud auth application-default login --disable-quota-project

gcloud auth login --enable-gdrive-access --update-adc

{
            "status": {
                "code": 403,
                "is_success": False,
                "user_message": ("Forbidden: Access denied"),
                "developer_message": None,
            },
            "data": {
                "account_id": <account_id>,
                "user_id": <user_id>,
                "is_service_token": <boolean describing if it's a service token request>,
                "account_access_denied": True,
            },
        }

git rev-list master..origin/main --count
fatal: ambiguous argument 'master..origin/main': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'

NoneType object has no attribute 
enumerate_fields'

Running with dbt=1.9.0
Encountered an error while reading the project:
  ERROR: Runtime Error
  Could not find profile named 'user'
Runtime Error
  Could not run dbt'

Your <Constant name="cloud_ide" /> session experienced an unknown error and was terminated. Please contact support.

Failed to connect to DB: xxxxxxx.snowflakecomputing.com:443. The role requested in the connection, or the default role if none was requested in the connection ('xxxxx'), is not listed in the Access Token or was filtered. 
   Please specify another role, or contact your OAuth Authorization server administrator.
   
   ALTER INTEGRATION <my_int_name> SET EXTERNAL_OAUTH_SCOPE_MAPPING_ATTRIBUTE = 'scp';
   
   Failed to connect to DB: xxxxxxx.snowflakecomputing.com:443. Incorrect username or password was specified.
   
$ dbt seed
Running with dbt=1.6.0-rc2
Found 0 models, 0 tests, 0 snapshots, 0 analyses, 130 macros, 0 operations, 1 seed file, 0 sources

12:12:27 | Concurrency: 8 threads (target='dev_snowflake')
12:12:27 |
12:12:27 | 1 of 1 START seed file dbt_claire.country_codes...................... [RUN]
12:12:30 | 1 of 1 ERROR loading seed file dbt_claire.country_codes.............. [ERROR in 2.78s]
12:12:31 |
12:12:31 | Finished running 1 seed in 10.05s.

Completed with 1 error and 0 warnings:

Database Error in seed country_codes (seeds/country_codes.csv)
  000904 (42000): SQL compilation error: error line 1 at position 62
  invalid identifier 'COUNTRY_NAME'

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

$ dbt seed
Running with dbt=1.6.0-rc2
Found 0 models, 0 tests, 0 snapshots, 0 analyses, 149 macros, 0 operations, 1 seed file, 0 sources

12:14:46 | Concurrency: 1 threads (target='dev_redshift')
12:14:46 |
12:14:46 | 1 of 1 START seed file dbt_claire.country_codes...................... [RUN]
12:14:46 | 1 of 1 ERROR loading seed file dbt_claire.country_codes.............. [ERROR in 0.23s]
12:14:46 |
12:14:46 | Finished running 1 seed in 1.75s.

Completed with 1 error and 0 warnings:

Database Error in seed country_codes (seeds/country_codes.csv)
  column "country_name" of relation "country_codes" does not exist

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

dbt seed --full-refresh

python3 -m venv dbt-env				# create the environment
source dbt-env/bin/activate			# activate the environment for Mac and Linux
dbt-env\Scripts\activate			# activate the environment for Windows

python -m pip install --upgrade pip wheel setuptools

$ dbt run --select customers
Running with dbt=1.9.0
Found 3 models, 9 tests, 0 snapshots, 0 analyses, 133 macros, 0 operations, 0 seed files, 0 sources

14:04:12 | Concurrency: 1 threads (target='dev')
14:04:12 |
14:04:12 | 1 of 1 START view model dbt_alice.customers.......................... [RUN]
14:04:13 | 1 of 1 ERROR creating view model dbt_alice.customers................. [ERROR in 0.81s]
14:04:13 |
14:04:13 | Finished running 1 view model in 1.68s.

Completed with 1 error and 0 warnings:

Database Error in model customers (models/customers.sql)
  Syntax error: Expected ")" but got identifier `your-info-12345` at [13:15]
  compiled SQL at target/run/jaffle_shop/customers.sql

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

sources:
  - name: jaffle_shop
    database: raw
    tables:
      - name: orders
      - name: customers

sources:
  - name: jaffle_shop
    schema: postgres_backend_public_schema
    database: raw
    tables:
      - name: orders
        identifier: api_orders

select * from {{ source('jaffle_shop', 'orders') }}

select * from raw.postgres_backend_public_schema.api_orders

{% macro cents_to_dollars(column_name, scale=2) %}
  {{ function('cents_to_dollars') }}({{ column_name }}, {{scale}})
{% endmacro %}

select 1 as my_column

-- you can't create or replace on redshift, so use a transaction to do this in an atomic way

create table "dbt_alice"."test_model__dbt_tmp" as (
    select 1 as my_column
);

alter table "dbt_alice"."test_model" rename to "test_model__dbt_backup";

alter table "dbt_alice"."test_model__dbt_tmp" rename to "test_model"

drop table if exists "dbt_alice"."test_model__dbt_backup" cascade;

-- Make an API call to create a dataset (no DDL interface for this)!!;

create or replace table `dbt-dev-87681`.`dbt_alice`.`test_model` as (
  select 1 as my_column
);

create schema if not exists analytics.dbt_alice;

create or replace table analytics.dbt_alice.test_model as (
    select 1 as my_column
);

Running with dbt=xxx
Runtime Error
  Failed to read package: Runtime Error
    Invalid config version: 1, expected 2  
  Error encountered in dbt_utils/dbt_project.yml

packages:
- package: dbt-labs/dbt_utils

{{ cents_to_dollars('amount') }} as amount_usd

$ dbt run
Running with dbt=1.7.0
Found 1 model, 0 tests, 0 snapshots, 0 analyses, 138 macros, 0 operations, 0 seed files, 0 sources

<profile-name>:
  target: <target-name> # this is the default target
  outputs:
    <target-name>:
      type: <bigquery | postgres | redshift | snowflake | other>
      schema: <schema_identifier>
      threads: <natural_number>

### database-specific connection details
      ...

<target-name>: # additional targets
      ...

<profile-name>: # additional profiles
  ...

default:
  target: dev
  outputs:
    dev:
      type: bigquery
      threads: 16
      database: ABC123
      schema: JAFFLE_SHOP
      method: service-account
      keyfile: /Users/mshaver/Downloads/CustomRoleDefinition.json
      location: us-east1
      dataproc_batch: null

gcloud auth application-default login \           
  --scopes=https://www.googleapis.com/auth/bigquery,\
https://www.googleapis.com/auth/drive.readonly,\
https://www.googleapis.com/auth/iam.test,\
https://www.googleapis.com/auth/cloud-platform

**Examples:**

Example 1 (unknown):
```unknown
See the [`source freshness` command reference](https://docs.getdbt.com/reference/commands/source.md) for more information.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### How do I specify column types?

Simply cast the column to the correct type in your model:
```

Example 2 (unknown):
```unknown
You might have this question if you're used to running statements like this:
```

Example 3 (unknown):
```unknown
In comparison, dbt would build this table using a `create table as` statement:
```

Example 4 (unknown):
```unknown
So long as your model queries return the correct column type, the table you create will also have the correct column type.

To define additional column options:

* Rather than enforcing uniqueness and not-null constraints on your column, use dbt's [data testing](https://docs.getdbt.com/docs/build/data-tests.md) functionality to check that your assertions about your model hold true.
* Rather than creating default values for a column, use SQL to express defaults (e.g. `coalesce(updated_at, current_timestamp()) as updated_at`)
* In edge-cases where you *do* need to alter a column (e.g. column-level encoding on Redshift), consider implementing this via a [post-hook](https://docs.getdbt.com/reference/resource-configs/pre-hook-post-hook.md).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### How do I test and document seeds?

To test and document seeds, use a [schema file](https://docs.getdbt.com/reference/configs-and-properties.md) and nest the configurations under a `seeds:` key

#### Example[​](#example "Direct link to Example")

seeds/schema.yml
```

---

## Output source freshness info to a different path

**URL:** llms-txt#output-source-freshness-info-to-a-different-path

**Contents:**
  - About dbt test command

$ dbt source freshness --output target/source_freshness.json

**Examples:**

Example 1 (unknown):
```unknown
##### Using source freshness[​](#using-source-freshness "Direct link to Using source freshness")

Snapshots of source freshness can be used to understand:

1. If a specific data source is in a delayed state
2. The trend of data source freshness over time

This command can be run manually to determine the state of your source data freshness at any time. It is also recommended that you run this command on a schedule, storing the results of the freshness snapshot at regular intervals. These longitudinal snapshots will make it possible to be alerted when source data freshness SLAs are violated, as well as understand the trend of freshness over time.

dbt makes it easy to snapshot source freshness on a schedule, and provides a dashboard out of the box indicating the state of freshness for all of the sources defined in your project. For more information on snapshotting freshness in dbt, check out the [docs](https://docs.getdbt.com/docs/build/sources.md#source-data-freshness).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt test command

`dbt test` runs data tests defined on models, sources, snapshots, and seeds and unit tests defined on SQL models. It expects that you have already created those resources through the appropriate commands.

The tests to run can be selected using the `--select` flag discussed [here](https://docs.getdbt.com/reference/node-selection/syntax.md).
```

---

## This works off the assumption that you've restricted this branch to only all PRs to push to the default branch

**URL:** llms-txt#this-works-off-the-assumption-that-you've-restricted-this-branch-to-only-all-prs-to-push-to-the-default-branch

---

## in development and a table in production/CI contexts

**URL:** llms-txt#in-development-and-a-table-in-production/ci-contexts

**Contents:**
  - About ref function
  - About References
  - About return function
  - About run_query macro
  - About run_started_at variable
  - About schemas variable
  - About selected_resources context variable
  - About set context method
  - About source function
  - About state in dbt

models:
  - name: dim_customers
    config:
      materialized: "{{ 'view' if target.name == 'dev' else 'table' }}"

select * from {{ ref("node_name") }}

select *
from public.raw_data

select *
from {{ref('model_a')}}

models:
  - name: model_name
    latest_version: 2
    versions:
      - v: 2
      - v: 1

-- returns the `Relation` object corresponding to version 1 of model_name
select * from {{ ref('model_name', version=1) }}

-- returns the `Relation` object corresponding to version 2 (the latest version) of model_name
select * from {{ ref('model_name') }}

select * from {{ ref('project_or_package', 'model_name') }}

--This macro already has its own `if execute` check, so this one is redundant and introduced solely to cause an error
{% if execute %}
  {% set sql_statement %}
      select max(created_at) from {{ ref('processed_orders') }}
  {% endset %}

{%- set newest_processed_order = dbt_utils.get_single_value(sql_statement, default="'2020-01-01'") -%}
{% endif %}

*,
    last_order_at > '{{ newest_processed_order }}' as has_unprocessed_order

from {{ ref('users') }}

--Now that this ref is outside of the if block, it will be detected during parsing
--depends_on: {{ ref('processed_orders') }}

{% if execute %}
  {% set sql_statement %}
      select max(created_at) from {{ ref('processed_orders') }}
  {% endset %}

{%- set newest_processed_order = dbt_utils.get_single_value(sql_statement, default="'2020-01-01'") -%}
{% endif %}

*,
    last_order_at > '{{ newest_processed_order }}' as has_unprocessed_order

from {{ ref('users') }}

{% macro get_data() %}

{{ return([1,2,3]) }}
  
{% endmacro %}

{% macro get_data() %}

{% do return([1,2,3]) %}
  
{% endmacro %}

select
  -- getdata() returns a list!
  {% for i in get_data() %}
    {{ i }}
    {%- if not loop.last %},{% endif -%}
  {% endfor %}

{% set results = run_query('select 1 as id') %}
{% do results.print_table() %}

-- do something with `results` here...

{% macro run_vacuum(table) %}

{% set query %}
    vacuum table {{ table }}
  {% endset %}

{% do run_query(query) %}
{% endmacro %}

{% set payment_methods_query %}
select distinct payment_method from app_data.payments
order by 1
{% endset %}

{% set results = run_query(payment_methods_query) %}

{% if execute %}
{# Return the first column #}
{% set results_list = results.columns[0].values() %}
{% else %}
{% set results_list = [] %}
{% endif %}

select
order_id,
{% for payment_method in results_list %}
sum(case when payment_method = '{{ payment_method }}' then amount end) as {{ payment_method }}_amount,
{% endfor %}
sum(amount) as total_amount
from {{ ref('raw_payments') }}
group by 1

{% macro run_vacuum(table) %}

{% set query %}
    vacuum table {{ table }}
  {% endset %}

{% do run_query(query) %}
{% endmacro %}

{% if execute %}
{% set results = run_query(payment_methods_query) %}
{% if results|length > 0 %}
  	-- do something with `results` here...
{% else %}
    -- do fallback here...
{% endif %}
{% endif %}

select
	'{{ run_started_at.strftime("%Y-%m-%d") }}' as date_day

select
	'{{ run_started_at.astimezone(modules.pytz.timezone("America/New_York")) }}' as run_started_est

on-run-end:
  - "{% for schema in schemas%}grant usage on schema {{ schema }} to group reporter;{% endfor%}"
  - "{% for schema in schemas %}grant select on all tables in schema {{ schema }} to group reporter;{% endfor%}"
  - "{% for schema in schemas %}alter default privileges in schema {{ schema }}  grant select on tables to group reporter;{% endfor %}"

["model.my_project.model1", "model.my_project.model2", "snapshot.my_project.my_snapshot"]

/*
  Check if a given model is selected and trigger a different action, depending on the result
*/

{% if execute %}
  {% if 'model.my_project.model1' in selected_resources %}
  
    {% do log("model1 is included based on the current selection", info=true) %}
  
  {% else %}

{% do log("model1 is not included based on the current selection", info=true) %}

{% endif %}
{% endif %}

/*
  Example output when running the code in on-run-start 
  when doing `dbt build`, including all nodels
---------------------------------------------------------------
  model1 is included based on the current selection

Example output when running the code in on-run-start 
  when doing `dbt run --select model2` 
---------------------------------------------------------------
  model1 is not included based on the current selection
*/

{% set my_list = [1, 2, 2, 3] %}
{% set my_set = set(my_list) %}
{% do log(my_set) %}  {# {1, 2, 3} #}

{% set my_invalid_iterable = 1234 %}
{% set my_set = set(my_invalid_iterable) %}
{% do log(my_set) %}  {# None #}

{% set email_id = "'admin@example.com'" %}

{% set my_list = [1, 2, 2, 3] %}
{% set my_set = set(my_list) %}
{% do log(my_set) %}  {# {1, 2, 3} #}

{% set my_invalid_iterable = 1234 %}
{% set my_set = set_strict(my_invalid_iterable) %}
{% do log(my_set) %}

Compilation Error in ... (...)
  'int' object is not iterable

select * from {{ source("source_name", "table_name") }}

sources:
  - name: jaffle_shop # this is the source_name
    database: raw

tables:
      - name: customers # this is the table_name
      - name: orders

from {{ source('jaffle_shop', 'customers') }}

left join {{ source('jaffle_shop', 'orders') }} using (customer_id)

-- depends_on: {{ ref('users') }}

{%- call statement('states', fetch_result=True) -%}

select distinct state from {{ ref('users') }}

statement(name=None, fetch_result=False, auto_begin=True)

-- depends_on: {{ ref('users') }}

{% call statement('states', fetch_result=True) -%}

select distinct state from {{ ref('users') }}

/*
    The unique states are: {{ load_result('states')['data'] }}
    */
{%- endcall %}

{% call statement('states', fetch_result=True) -%}

select distinct state from {{ ref('users') }}

/*
    The unique states are: {{ load_result('states')['data'] }}
    */

select id * 2 from {{ ref('users') }}

{%- set states = load_result('states') -%}
{%- set states_data = states['data'] -%}
{%- set states_status = states['response'] -%}

[
  ['PA'],
  ['NY'],
  ['CA'],
	...
]

select
  *
from source('web_events', 'page_views')
{% if target.name == 'dev' %}
where created_at >= dateadd('day', -3, current_date)
{% endif %}

sources:
  - name: source_name 
    database: |
      {%- if  target.name == "dev" -%} raw_dev
      {%- elif target.name == "qa"  -%} raw_qa
      {%- elif target.name == "prod"  -%} raw_prod
      {%- else -%} invalid_database
      {%- endif -%}
    schema: source_schema

{{ config(materialized='incremental') }}

select
    *,
    my_slow_function(my_column)

from raw_app_data.events

{% if is_incremental() %}
  where event_time > (select max(event_time) from {{ this }})
{% endif %}

{% set my_dict = {"abc": 123} %}
{% set my_json_string = tojson(my_dict) %}

{% do log(my_json_string) %}

{% set my_dict = {"abc": 123} %}
{% set my_yaml_string = toyaml(my_dict) %}

{% do log(my_yaml_string) %}

unit_tests:
  - name: <test-name> # this is the unique name of the test
    model: <model-name> 
      versions: #optional
        include: <list-of-versions-to-include> #optional
        exclude: <list-of-versions-to-exclude> #optional
    config: 
      meta: {dictionary}
      tags: <string> | [<string>]
      enabled: {boolean} # optional. v1.9 or higher. If not configured, defaults to `true`
    given:
      - input: <ref_or_source_call> # optional for seeds
        format: dict | csv | sql
        # either define rows inline or name of fixture
        rows: {dictionary} | <string>
        fixture: <fixture-name> # SQL or csv 
      - input: ... # declare additional inputs
    expect:
      format: dict | csv | sql
      # either define rows inline of rows or name of fixture
      rows: {dictionary} | <string>
      fixture: <fixture-name> # SQL or csv 
    overrides: # optional: configuration for the dbt execution environment
      macros:
        is_incremental: true | false
        dbt_utils.current_timestamp: <string>
        # ... any other Jinja function from https://docs.getdbt.com/reference/dbt-jinja-functions
        # ... any other context property
      vars: {dictionary}
      env_vars: {dictionary}
  - name: <test-name> ... # declare additional unit tests

unit_tests:
  - name: test_is_valid_email_address # this is the unique name of the test
    model: dim_customers # name of the model I'm unit testing
    given: # the mock data for your inputs
      - input: ref('stg_customers')
        rows:
         - {email: cool@example.com,     email_top_level_domain: example.com}
         - {email: cool@unknown.com,     email_top_level_domain: unknown.com}
         - {email: badgmail.com,         email_top_level_domain: gmail.com}
         - {email: missingdot@gmailcom,  email_top_level_domain: gmail.com}
      - input: ref('top_level_email_domains')
        rows:
         - {tld: example.com}
         - {tld: gmail.com}
    expect: # the expected output given the inputs above
      rows:
        - {email: cool@example.com,    is_valid_email_address: true}
        - {email: cool@unknown.com,    is_valid_email_address: false}
        - {email: badgmail.com,        is_valid_email_address: false}
        - {email: missingdot@gmailcom, is_valid_email_address: false}

unit_tests:
  - name: test_is_valid_email_address # this is the unique name of the test
    model: dim_customers # name of the model I'm unit testing
    given: # the mock data for your inputs
      - input: ref('stg_customers')
        rows:
         - {email: cool@example.com,     email_top_level_domain: example.com}
         - {email: cool@unknown.com,     email_top_level_domain: unknown.com}
         - {email: badgmail.com,         email_top_level_domain: gmail.com}
         - {email: missingdot@gmailcom,  email_top_level_domain: gmail.com}
      - input: ref('top_level_email_domains')
        format: csv
        rows: |
          tld
          example.com
          gmail.com
    expect: # the expected output given the inputs above
      format: csv
      fixture: valid_email_address_fixture_output

unit_tests:
  - name: test_is_valid_email_address # this is the unique name of the test
    model: dim_customers # name of the model I'm unit testing
    given: # the mock data for your inputs
      - input: ref('stg_customers')
        rows:
         - {email: cool@example.com,     email_top_level_domain: example.com}
         - {email: cool@unknown.com,     email_top_level_domain: unknown.com}
         - {email: badgmail.com,         email_top_level_domain: gmail.com}
         - {email: missingdot@gmailcom,  email_top_level_domain: gmail.com}
      - input: ref('top_level_email_domains')
        format: sql
        rows: |
          select 'example.com' as tld union all
          select 'gmail.com' as tld
    expect: # the expected output given the inputs above
      format: sql
      fixture: valid_email_address_fixture_output

select * from events where event_type = '{{ var("event_type") }}'

Encountered an error:
! Compilation error while compiling model package_name.my_model:
! Required var 'event_type' not found in config:
Vars supplied to package_name.my_model = {
}

name: my_dbt_project
version: 1.0.0

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About ref function
```

Example 2 (unknown):
```unknown
#### Definition[​](#definition "Direct link to Definition")

This function:

* Returns a [Relation](https://docs.getdbt.com/reference/dbt-classes.md#relation) for a [model](https://docs.getdbt.com/docs/build/models.md), [seed](https://docs.getdbt.com/docs/build/seeds.md), or [snapshot](https://docs.getdbt.com/docs/build/snapshots.md)
* Creates dependencies between the referenced node and the current model, which is useful for documentation and [node selection](https://docs.getdbt.com/reference/node-selection/syntax.md)
* Compiles to the full object name in the database

The most important function in dbt is `ref()`; it's impossible to build even moderately complex models without it. `ref()` is how you reference one model within another. This is a very common behavior, as typically models are built to be "stacked" on top of one another. Here is how this looks in practice:

model\_a.sql
```

Example 3 (unknown):
```unknown
model\_b.sql
```

Example 4 (unknown):
```unknown
`ref()` is, under the hood, actually doing two important things. First, it is interpolating the schema into your model file to allow you to change your deployment schema via configuration. Second, it is using these references between models to automatically build the dependency graph. This will enable dbt to deploy models in the correct order when using `dbt run`.

The `{{ ref }}` function returns a `Relation` object that has the same `table`, `schema`, and `name` attributes as the [{{ this }} variable](https://docs.getdbt.com/reference/dbt-jinja-functions/this.md).

#### Advanced ref usage[​](#advanced-ref-usage "Direct link to Advanced ref usage")

##### Versioned ref[​](#versioned-ref "Direct link to Versioned ref")

The `ref` function supports an optional keyword argument - `version` (or `v`). When a version argument is provided to the `ref` function, dbt returns to the `Relation` object corresponding to the specified version of the referenced model.

This functionality is useful when referencing versioned models that make breaking changes by creating new versions, but guarantees no breaking changes to existing versions of the model.

If the `version` argument is not supplied to a `ref` of a versioned model, the latest version is. This has the benefit of automatically incorporating the latest changes of a referenced model, but there is a risk of incorporating breaking changes.

###### Example[​](#example "Direct link to Example")

models/\<schema>.yml
```

---

## in dependencies.yml

**URL:** llms-txt#in-dependencies.yml

**Contents:**
  - Incremental models in-depth
  - Intermediate: Purpose-built transformation steps
  - Intro to dbt Mesh
  - Intro to the dbt Semantic Layer
  - Marts: Business-defined entities
  - Materializations best practices
  - More advanced metrics
  - Now it's your turn

projects:
  - name: jaffle_shop

where
  updated_at > (select max(updated_at) from {{ this }})

{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

{% if is_incremental() %}

where
  updated_at > (select max(updated_at) from {{ this }})

models/intermediate
└── finance
    ├── _int_finance__models.yml
    └── int_payments_pivoted_to_orders.sql

-- int_payments_pivoted_to_orders.sql

{%- set payment_methods = ['bank_transfer','credit_card','coupon','gift_card'] -%}

select * from {{ ref('stg_stripe__payments') }}

pivot_and_aggregate_payments_to_order_grain as (

select
      order_id,
      {% for payment_method in payment_methods -%}

sum(
            case
               when payment_method = '{{ payment_method }}' and
                    status = 'success'
               then amount
               else 0
            end
         ) as {{ payment_method }}_amount,

{%- endfor %}
      sum(case when status = 'success' then amount end) as total_amount

select * from pivot_and_aggregate_payments_to_order_grain

models/marts
├── finance
│   ├── _finance__models.yml
│   ├── orders.sql
│   └── payments.sql
└── marketing
    ├── _marketing__models.yml
    └── customers.sql

select * from {{ ref('stg_jaffle_shop__orders' )}}

select * from {{ ref('int_payments_pivoted_to_orders') }}

orders_and_order_payments_joined as (

select
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        coalesce(order_payments.total_amount, 0) as amount,
        coalesce(order_payments.gift_card_amount, 0) as gift_card_amount

left join order_payments on orders.order_id = order_payments.order_id

select * from orders_and_order_payments_joined

select * from {{ ref('stg_jaffle_shop__customers')}}

select * from {{ ref('orders')}}

select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders,
        sum(amount) as lifetime_value

customers_and_customer_orders_joined as (

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders,
        customer_orders.lifetime_value

left join customer_orders on customers.customer_id = customer_orders.customer_id

select * from customers_and_customer_orders_joined

- name: food_revenue
  description: The revenue from food in each order.
  label: Food Revenue
  type: simple
  type_params:
    measure: food_revenue

- name: food_revenue_pct
  description: The % of order revenue from food.
  label: Food Revenue %
  type: ratio
  type_params:
    numerator: food_revenue
    denominator: revenue

- name: revenue_growth_mom
  description: "Percentage growth of revenue compared to 1 month ago. Excluded tax"
  type: derived
  label: Revenue Growth % M/M
  type_params:
    expr: (current_revenue - revenue_prev_month) * 100 / revenue_prev_month
    metrics:
      - name: revenue
        alias: current_revenue
      - name: revenue
        offset_window: 1 month
        alias: revenue_prev_month

- name: cumulative_revenue
  description: The cumulative revenue for all orders.
  label: Cumulative Revenue (All Time)
  type: cumulative
  type_params:
    measure: revenue

**Examples:**

Example 1 (unknown):
```unknown
##### Best practices[​](#best-practices "Direct link to Best practices")

* When you’ve **confirmed the right groups**, it's time to split your projects.

  <!-- -->

  * **Do *one* group at a time**!
  * **Do *not* refactor as you migrate**, however tempting that may be. Focus on getting 1-to-1 parity and log any issues you find in doing the migration for later. Once you’ve fully migrated the project then you can start optimizing it for its new life as part of your mesh.

* Start by splitting your project within the same repository for full git tracking and easy reversion if you need to start from scratch.

#### Connecting existing projects[​](#connecting-existing-projects "Direct link to Connecting existing projects")

Some organizations may already be coordinating across multiple dbt projects. Most often this is via:

1. Installing parent projects as dbt packages
2. Using `{{ source() }}` functions to read the outputs of a parent project as inputs to a child project.

This has a few drawbacks:

1. If using packages, each project has to include *all* resources from *all* projects in its manifest, slowing down dbt and the development cycle.
2. If using sources, there are breakages in the lineage, as there's no real connection between the parent and child projects.

The migration steps here are much simpler than splitting up a monolith!

1. If using the `package` method:

   <!-- -->

   1. In the parent project:
      <!-- -->
      1. mark all models being referenced downstream as `public` and add a model contract.

   2. In the child project:

      <!-- -->

      1. Remove the package entry from `packages.yml`
      2. Add the upstream project to your `dependencies.yml`
      3. Update the `{{ ref() }}` functions to models from the upstream project to include the project name argument.

2. If using `source` method:

   <!-- -->

   1. In the parent project:
      <!-- -->
      1. mark all models being imported downstream as `public` and add a model contract.

   2. In the child project:

      <!-- -->

      1. Add the upstream project to your `dependencies.yml`
      2. Replace the `{{ source() }}` functions with cross project `{{ ref() }}` functions.
      3. Remove the unnecessary `source` definitions.

#### Additional Resources[​](#additional-resources "Direct link to Additional Resources")

##### Our example projects[​](#our-example-projects "Direct link to Our example projects")

We've provided a set of example projects you can use to explore the topics covered here. We've split our [Jaffle Shop](https://github.com/dbt-labs/jaffle-shop) project into 3 separate projects in a multi-repo Mesh. Note that you'll need to leverage dbt to use multi-project architecture, as cross-project references are powered via dbt's APIs.

* **[Platform](https://github.com/dbt-labs/jaffle-shop-mesh-platform)** - containing our centralized staging models.
* **[Marketing](https://github.com/dbt-labs/jaffle-shop-mesh-marketing)** - containing our marketing marts.
* **[Finance](https://github.com/dbt-labs/jaffle-shop-mesh-finance)** - containing our finance marts.

##### dbt-meshify[​](#dbt-meshify "Direct link to dbt-meshify")

We recommend using the `dbt-meshify` [command line tool](https://dbt-labs.github.io/dbt-meshify/) to help you do this. This comes with CLI operations to automate most of the above steps.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Quickstart with Mesh](https://docs.getdbt.com/guides/mesh-qs.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Incremental models in-depth

So far we’ve looked at tables and views, which map to the traditional objects in the data warehouse. As mentioned earlier, incremental models are a little different. This is where we start to deviate from this pattern with more powerful and complex materializations.

* 📚 **Incremental models generate tables.** They physically persist the data itself to the warehouse, just piece by piece. What’s different is **how we build that table**.

* 💅 **Only apply our transformations to rows of data with new or updated information**, this maximizes efficiency.
  <!-- -->
  * 🌍  If we have a very large set of data or compute-intensive transformations, or both, it can be very slow and costly to process the entire corpus of source data being input into a model or chain of models. If instead we can identify *only rows that contain new information* (that is, **new or updated records**), we then can process just those rows, building our models *incrementally*.

* 3️⃣  We need **3 key things** in order to accomplish the above:

  <!-- -->

  * a **filter** to select just the new or updated records
  * a **conditional block** that wraps our filter and only applies it when we want it
  * **configuration** that tells dbt we want to build incrementally and helps apply the conditional filter when needed

Let’s dig into how exactly we can do that in dbt. Let’s say we have an `orders` table that looks like the below:

| order\_id | order\_status | customer\_id | order\_item\_id | ordered\_at | updated\_at |
| --------- | ------------- | ------------ | --------------- | ----------- | ----------- |
| 123       | shipped       | 7            | 5791            | 2022-01-30  | 2022-01-30  |
| 234       | confirmed     | 15           | 1643            | 2022-01-31  | 2022-01-31  |

We did our last `dbt build` job on `2022-01-31`, so any new orders since that run won’t appear in our table. When we do our next run (for simplicity let’s say the next day, although for an orders model we’d more realistically run this hourly), we have two options:

* 🏔️ build the table from the **beginning of time again — a *table materialization***
  * Simple and solid, if we can afford to do it (in terms of time, compute, and money — which are all directly correlated in a cloud warehouse). It’s the easiest and most accurate option.
* 🤏 find a way to run **just new and updated rows since our previous run — *an* *incremental materialization***
  * If we *can’t* realistically afford to run the whole table — due to complex transformations or big source data, it takes too long — then we want to build incrementally. We want to just transform and add the row with id 567 below, *not* the previous two with ids 123 and 234 that are already in the table.

| order\_id | order\_status | customer\_id | order\_item\_id | ordered\_at | updated\_at |
| --------- | ------------- | ------------ | --------------- | ----------- | ----------- |
| 123       | shipped       | 7            | 5791            | 2022-01-30  | 2022-01-30  |
| 234       | confirmed     | 15           | 1643            | 2022-01-31  | 2022-01-31  |
| 567       | shipped       | 61           | 28              | 2022-02-01  | 2022-02-01  |

##### Writing incremental logic[​](#writing-incremental-logic "Direct link to Writing incremental logic")

Let’s think through the information we’d need to build such a model that only processes new and updated data. We would need:

* 🕜  **a timestamp indicating when a record was last updated**, let’s call it our `updated_at` timestamp, as that’s a typical convention and what we have in our example above.
* ⌛ the **most recent timestamp from this table *in our warehouse*** *—* that is, the one created by the previous run — to act as a cutoff point. We’ll call the model we’re working in `this`, for ‘this model we’re working in’.

That would lets us construct logic like this:
```

Example 2 (unknown):
```unknown
Let’s break down that `where` clause a bit, because this is where the action is with incremental models. Stepping through the code ***right-to-left*** we:

1. Get our **cutoff.**

   1. Select the `max(updated_at)` timestamp — the **most recent record**
   2. from `{{ this }}` — the table for this model as it exists in the warehouse, as **built in our last run**,
   3. so `max(updated_at) from {{ this }}` the ***most recent record processed in our last run,***
   4. that’s exactly what we want as a **cutoff**!

2. **Filter** the rows we’re selecting to add in this run.

   <!-- -->

   1. Use the `updated_at` timestamp from our input, the equivalent column to the one in the warehouse, but in the up-to-the-minute **source data we’re selecting from** and
   2. check if it’s **greater than our cutoff,**
   3. if so it will satisfy our where clause, so we’re **selecting all the rows more recent than our cutoff.**

This logic would let us isolate and apply our transformations to just the records that have come in since our last run, and I’ve got some great news: that magic `{{ this }}` keyword [does in fact exist in dbt](https://docs.getdbt.com/reference/dbt-jinja-functions/this.md), so we can write exactly this logic in our models.

##### Configuring incremental models[​](#configuring-incremental-models "Direct link to Configuring incremental models")

So we’ve found a way to isolate the new rows we need to process. How then do we handle the rest? We still need to:

* ➕  make sure dbt knows to ***add* new rows on top** of the existing table in the warehouse, **not replace** it.
* 👉  If there are **updated rows**, we need a way for dbt to know **which rows to update**.
* 🌍  Lastly, if we’re building into a new environment and there’s **no previous run to reference**, or we need to **build the model from scratch.** Put another way, we’ll want a means to skip the incremental logic and transform all of our input data like a regular table if needed.
* 😎 **Visualized below**, we’ve figured out how to get the red ‘new records’ portion selected, but we need to sort out the step to the right, where we stick those on to our model.

![Diagram visualizing how incremental models work](/assets/images/incremental-diagram-8816eec2768f76dbb493f70c7ec25d99.png)

info

😌 Incremental models can be confusing at first, **take your time reviewing** this visual and the previous steps until you have a **clear mental model.** Be patient with yourself. This materialization will become second nature soon, but it’s tough at first. If you’re feeling confused the [dbt Community is here for you on the Forum and Slack](https://www.getdbt.com/community/join-the-community).

Thankfully dbt has some additional configuration and special syntax just for incremental models.

First, let’s look at a config block for incremental materialization:
```

Example 3 (unknown):
```unknown
* 📚 The **`materialized` config** works just like tables and views, we just pass it the value `'incremental'`.
* 🔑 We’ve **added a new config option `unique_key`,** that tells dbt that if it finds a record in our previous run — the data in the warehouse already — with the same unique id (in our case `order_id` for our `orders` table) that exists in the new data we’re adding incrementally, to **update that record instead of adding it as a separate row**.
* 👯 This **hugely broadens the types of data we can build incrementally** from just immutable tables (data where rows only ever get added, never updated) to mutable records (where rows might change over time). As long as we’ve got a column that specifies when records were updated (such as `updated_at` in our example), we can handle almost anything.
* ➕ We’re now **adding records** to the table **and updating existing rows**. That’s 2 of 3 concerns.
* 🆕 We still need to **build the table from scratch** (via `dbt build` or `run` in a job) when necessary — whether because we’re in a new environment so don’t have an initial table to build on, or our model has drifted from the original over time due to data loading latency.
* 🔀 We need to wrap our incremental logic, that is our `where` clause with our `updated_at` cutoff, in a **conditional statement that will only apply it when certain conditions are met**. If you’re thinking this is **a case for a Jinja `{% if %}` statement**, you’re absolutely right!

##### Incremental conditions[​](#incremental-conditions "Direct link to Incremental conditions")

So we’re going to use an **if statement** to apply our cutoff filter **only when certain conditions are met**. We want to apply our cutoff filter *if* the **following things are true**:

* ➕  we’ve set the materialization **config** to incremental,
* 🛠️  there is an **existing table** for this model in the warehouse to build on,
* 🙅‍♀️  and the `--full-refresh` **flag was *not* passed.**
  * [full refresh](https://docs.getdbt.com/reference/resource-configs/full_refresh.md) is a configuration and flag that is specifically designed to let us override the incremental materialization and build a table from scratch again.

Thankfully, we don’t have to dig into the guts of dbt to sort out each of these conditions individually.

* ⚙️  dbt provides us with a **macro [`is_incremental`](https://docs.getdbt.com/docs/build/incremental-models.md#understand-the-is_incremental-macro)** that checks all of these conditions for this exact use case.
* 🔀  By **wrapping our cutoff logic** in this macro, it will only get applied when the macro returns true for all of the above conditions.

Let’s take a look at all these pieces together:
```

Example 4 (unknown):
```unknown
Fantastic! We’ve got a working incremental model. On our first run, when there is no corresponding table in the warehouse, `is_incremental` will evaluate to false and we’ll capture the entire table. On subsequent runs it will evaluate to true and we’ll apply our filter logic, capturing only the newer data.

##### Late arriving facts[​](#late-arriving-facts "Direct link to Late arriving facts")

Our last concern specific to incremental models is what to do when data is inevitably loaded in a less-than-perfect way. Sometimes data loaders will, for a variety of reasons, load data late. Either an entire load comes in late, or some rows come in on a load after those with which they should have. The following is best practice for every incremental model to slow down the drift this can cause.

* 🕐 For example if most of our records for `2022-01-30` come in the raw schema of our warehouse on the morning of `2022-01-31`, but a handful don’t get loaded til `2022-02-02`, how might we tackle that? There will already be `max(updated_at)` timestamps of `2022-01-31` in the warehouse, filtering out those late records. **They’ll never make it to our model.**
* 🪟 To mitigate this, we can add a **lookback window** to our **cutoff** point. By **subtracting a few days** from the `max(updated_at)`, we would capture any late data within the window of what we subtracted.
* 👯 As long as we have a **`unique_key` defined in our config**, we’ll simply update existing rows and avoid duplication. We process more data this way, but in a fixed way, and it keeps our model hewing closer to the source data.

##### Long-term considerations[​](#long-term-considerations "Direct link to Long-term considerations")

Late arriving facts point to the biggest tradeoff with incremental models:

* 🪢 In addition to extra **complexity**, they also inevitably **drift from the source data over time.** Due to the imperfection of loaders and the reality of late arriving facts, we can’t help but miss some day in-between our incremental runs, and this accumulates.
* 🪟 We can slow this entropy with the lookback window described above — **the longer the window the less efficient the model, but the slower the drift.** It’s important to note it will still occur though, however slowly. If we have a lookback window of 3 days, and a record comes in 4 days late from the loader, we’re still going to miss it.
* 🌍 Thankfully, there is a way we can reset the relationship of the model to the source data. We can run the model with the **`--full-refresh` flag passed** (such as `dbt build --full-refresh -s orders`). As we saw in the `is_incremental` conditions above, that will make our logic return false, and our `where` clause filter will not be applied, running the whole table.
* 🏗️ This will let us **rebuild the entire table from scratch,** a good practice to do regularly **if the size of the data will allow**.
* 📆 A common pattern for incremental models of manageable size is to run a **full refresh on the weekend** (or any low point in activity), either **weekly or monthly**, to consistently reset the drift from late arriving facts.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Intermediate: Purpose-built transformation steps

Once we’ve got our atoms ready to work with, we’ll set about bringing them together into more intricate, connected molecular shapes. The intermediate layer is where these molecules live, creating varied forms with specific purposes on the way towards the more complex proteins and cells we’ll use to breathe life into our data products.

##### Intermediate: Files and folders[​](#intermediate-files-and-folders "Direct link to Intermediate: Files and folders")

Let’s take a look at the intermediate layer of our project to understand the purpose of this stage more concretely.
```

---

## tests on one source

**URL:** llms-txt#tests-on-one-source

dbt test --select "source:jaffle_shop"

---

## Run tests downstream of a model (note this will select those tests directly!)

**URL:** llms-txt#run-tests-downstream-of-a-model-(note-this-will-select-those-tests-directly!)

dbt test --select "stg_customers+"

---

## use methods and intersections for more complex selectors

**URL:** llms-txt#use-methods-and-intersections-for-more-complex-selectors

**Contents:**
  - tags

dbt run --select "path:marts/finance,tag:nightly,config.materialized:table"

dbt ls --select "path/to/my/models" # Lists all models in a specific directory.
dbt ls --select "source_status:fresher+" # Shows sources updated since the last dbt source freshness run.
dbt ls --select state:modified+ # Displays nodes modified in comparison to a previous state.
dbt ls --select "result:<status>+" state:modified+ --state ./<dbt-artifact-path> # Lists nodes that match certain result statuses and are modified.

resource_type:
  - name: resource_name
    config:
      tags: <string> | [<string>] # Supports single strings or list of strings
    # Optional: Add the following specific properties for models
    columns:
      - name: column_name
        config:
          tags: <string> | [<string>] # changed to config in v1.10 and backported to 1.9
        data_tests:
          test-name:
            config:
              tags: "single-string" # Supports single string 
              tags: ["string-1", "string-2"] # Supports list of strings

models:
  - name: my_model
    description: A model description
    config:
      tags: ['example_tag']

{{ config(
    tags="<string>" | ["<string>"]
) }}

models:
  jaffle_shop:
    +tags: "contains_pii"

staging:
      +tags:
        - "hourly"

marts:
      +tags:
        - "hourly"
        - "published"

metrics:
      +tags:
        - "daily"
        - "published"

models:
  jaffle_shop:
    +tags: finance # jaffle_shop model is tagged with 'finance'.

models:
  - name: stg_customers
    description: Customer data with basic cleaning and transformation applied, one row per customer.
    config:
      tags: ['santi'] # stg_customers.yml model is tagged with 'santi'.
    columns:
      - name: customer_id
        description: The unique key for each customer.
        data_tests:
          - not_null
          - unique

{{ config(
    tags=["finance"] # stg_payments.sql model is tagged with 'finance'.
) }}

**Examples:**

Example 1 (unknown):
```unknown
As your selection logic gets more complex, and becomes unwieldly to type out as command-line arguments, consider using a [yaml selector](https://docs.getdbt.com/reference/node-selection/yaml-selectors.md). You can use a predefined definition with the `--selector` flag. Note that when you're using `--selector`, most other flags (namely `--select` and `--exclude`) will be ignored.

The `--select` and `--selector` arguments are similar in that they both allow you to select resources. To understand the difference between `--select` and `--selector` arguments, see [this section](https://docs.getdbt.com/reference/node-selection/yaml-selectors.md#difference-between---select-and---selector) for more details.

##### Troubleshoot with the `ls` command[​](#troubleshoot-with-the-ls-command "Direct link to troubleshoot-with-the-ls-command")

Constructing and debugging your selection syntax can be challenging. To get a "preview" of what will be selected, we recommend using the [`list` command](https://docs.getdbt.com/reference/commands/list.md). This command, when combined with your selection syntax, will output a list of the nodes that meet that selection criteria. The `dbt ls` command supports all types of selection syntax arguments, for example:
```

Example 2 (unknown):
```unknown
##### Questions from the Community[​](#questions-from-the-community "Direct link to Questions from the Community")

![Loading](/img/loader-icon.svg)[Ask the Community](https://discourse.getdbt.com/new-topic?category=help\&tags=node-selection "Ask the Community")

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### tags

* Project file
* Config property
* Config block

dbt\_project.yml

resource\_type/properties.yml
```

Example 3 (unknown):
```unknown
To apply tags to a model in your `models/` directory, add the `config` property similar to the following example:

models/model.yml
```

Example 4 (unknown):
```unknown
models/model.sql
```

---

## in development and tables in production/CI contexts

**URL:** llms-txt#in-development-and-tables-in-production/ci-contexts

**Contents:**
  - About dbt_version variable
  - About debug macro
  - About dispatch config
  - About doc function

models:
  my_project:
    facts:
      +materialized: "{{ 'view' if target.name == 'dev' else 'table' }}"

{% macro get_version() %}

{% do log("The installed version of dbt is: " ~ dbt_version, info=true) %}

$ dbt run-operation get_version
The installed version of dbt is 1.6.0

{% macro my_macro() %}

{% set something_complex = my_complicated_macro() %}
  
  {{ debug() }}

$ DBT_MACRO_DEBUGGING=write dbt compile
Running with dbt=1.0
> /var/folders/31/mrzqbbtd3rn4hmgbhrtkfyxm0000gn/T/dbt-macro-compiled-cxvhhgu7.py(14)root()
     13         environment.call(context, (undefined(name='debug') if l_0_debug is missing else l_0_debug)),
---> 14         environment.call(context, (undefined(name='source') if l_0_source is missing else l_0_source), 'src', 'seedtable'),
     15     )

ipdb> l 9,12
      9     l_0_debug = resolve('debug')
     10     l_0_source = resolve('source')
     11     pass
     12     yield '%s\nselect * from %s' % (

{% macro my_macro(arg1, arg2) -%}
  {{ return(adapter.dispatch('my_macro')(arg1, arg2)) }}
{%- endmacro %}

{% macro concat(fields) -%}
    {{ return(adapter.dispatch('concat')(fields)) }}
{%- endmacro %}

{% macro default__concat(fields) -%}
    concat({{ fields|join(', ') }})
{%- endmacro %}

{% macro redshift__concat(fields) %}
    {{ fields|join(' || ') }}
{% endmacro %}

{% macro snowflake__concat(fields) %}
    {{ fields|join(' || ') }}
{% endmacro %}

{% macro concat(fields) -%}
    {{ return(adapter.dispatch('concat')(fields)) }}
{%- endmacro %}

{% macro default__concat(fields) -%}
    {{ return(dbt_utils.concat(fields)) }}
{%- endmacro %}

{% macro redshift__concat(fields) %}
    {% for field in fields %}
        nullif({{ field }},'') {{ ' || ' if not loop.last }}
    {% endfor %}
{% endmacro %}

{% macro concat(fields) -%}
  {{ return(adapter.dispatch('concat', 'dbt_utils')(fields)) }}
{%- endmacro %}

dispatch:
  - macro_namespace: dbt_utils
    search_order: ['my_project', 'dbt_utils']

dispatch:
  - macro_namespace: dbt
    search_order: ['my_project', 'my_org_dbt_helpers', 'dbt']

packages:
  - package: dbt-labs/dbt_utils
    version: ...
  - package: dbt-labs/spark_utils
    version: ...

dispatch:
  - macro_namespace: dbt_utils
    search_order: ['my_project', 'spark_utils', 'dbt_utils']

{% macro dateadd(datepart, interval, from_date_or_timestamp) %}
    {{ return(adapter.dispatch('dateadd')(datepart, interval, from_date_or_timestamp)) }}
{% endmacro %}

{% macro default__dateadd(datepart, interval, from_date_or_timestamp) %}
    dateadd({{ datepart }}, {{ interval }}, {{ from_date_or_timestamp }})
{% endmacro %}

{% macro postgres__dateadd(datepart, interval, from_date_or_timestamp) %}
    {{ from_date_or_timestamp }} + ((interval '1 {{ datepart }}') * ({{ interval }}))
{% endmacro %}

{# Use default syntax instead of postgres syntax #}
{% macro redshift__dateadd(datepart, interval, from_date_or_timestamp) %}
    {{ return(default__dateadd(datepart, interval, from_date_or_timestamp) }}
{% endmacro %}

Compilation Error
  In dispatch: Could not find package 'my_project'

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt_version variable

The `dbt_version` variable returns the installed version of dbt that is currently running. It can be used for debugging or auditing purposes. For details about release versioning, refer to [Versioning](https://docs.getdbt.com/reference/commands/version.md#versioning).

#### Example usages[​](#example-usages "Direct link to Example usages")

macros/get\_version.sql
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About debug macro

Development environment only

The `debug` macro is only intended to be used in a development context with dbt. Do not deploy code to production that uses the `debug` macro.

The `{{ debug() }}` macro will open an iPython debugger in the context of a compiled dbt macro. The `DBT_MACRO_DEBUGGING` environment value must be set to use the debugger.

#### Usage[​](#usage "Direct link to Usage")

my\_macro.sql
```

Example 4 (unknown):
```unknown
When dbt hits the `debug()` line, you'll see something like:
```

---

## Now you can access the actual configuration value

**URL:** llms-txt#now-you-can-access-the-actual-configuration-value

---

## Configure this model to be materialized as a view

**URL:** llms-txt#configure-this-model-to-be-materialized-as-a-view

---

## iterate through all source nodes, create or replace (no refresh command is required as data is fetched live from remote)

**URL:** llms-txt#iterate-through-all-source-nodes,-create-or-replace-(no-refresh-command-is-required-as-data-is-fetched-live-from-remote)

**Contents:**
  - freshness
  - freshness Private previewEnterpriseEnterprise +
  - freshness [Private preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - full_refresh
  - Function configurations
  - Function properties
  - function-paths
  - grants
  - Graph operators
  - Greenplum configurations

$ dbt run-operation stage_external_sources --vars "ext_full_refresh: true"

{{ config(
   materialized = 'incremental',
   incremental_strategy='append'
) }}

/* All rows returned by this query will be appended to the existing model */

select * from {{ ref('raw_orders') }}
{% if is_incremental() %}
   where order_date > (select max(order_date) from {{ this }})
{% endif %}

CREATE DIMENSION TABLE IF NOT EXISTS orders__dbt_tmp AS
SELECT * FROM raw_orders
WHERE order_date > (SELECT MAX(order_date) FROM orders);

INSERT INTO orders VALUES ([columns])
SELECT ([columns])
FROM orders__dbt_tmp;

sources:
  <resource-path>:
    +freshness:
      warn_after:  
        count: <positive_integer>
        period: minute | hour | day

sources:
  - name: <source_name>
    config:
      freshness: # changed to config in v1.9
        warn_after:
          count: <positive_integer>
          period: minute | hour | day
        error_after:
          count: <positive_integer>
          period: minute | hour | day
        filter: <boolean_sql_expression>
      # changed to config in v1.10
      loaded_at_field: <column_name_or_expression>
      # or use loaded_at_query in v1.10 or higher. Should not be used if loaded_at_field is defined
      loaded_at_query: <sql_expression>

tables:
      - name: <table_name>
        config:
          # source.table.config.freshness overrides source.config.freshness
          freshness: 
            warn_after:
              count: <positive_integer>
              period: minute | hour | day
            error_after:
              count: <positive_integer>
              period: minute | hour | day
            filter: <boolean_sql_expression>
          # changed to config in v1.10
          loaded_at_field: <column_name_or_expression>
          # or use loaded_at_query in v1.10 or higher. Should not be used if loaded_at_field is defined
          loaded_at_query: <sql_expression>

loaded_at_field: "completed_date::timestamp"

loaded_at_field: "CAST(completed_date AS TIMESTAMP)"

loaded_at_field: "convert_timezone('Australia/Sydney', 'UTC', created_at_local)"

sources:
  - name: jaffle_shop
    database: raw
    config: 
      # changed to config in v1.9
      freshness: # default freshness
        warn_after: {count: 12, period: hour}
        error_after: {count: 24, period: hour}

loaded_at_field: _etl_loaded_at

tables:
      - name: customers # this will use the freshness defined above

- name: orders
        config:
          freshness: # make this a little more strict
            warn_after: {count: 6, period: hour}
            error_after: {count: 12, period: hour}
            # Apply a where clause in the freshness query
            filter: datediff('day', _etl_loaded_at, current_timestamp) < 2

- name: product_skus
        config:
          freshness: # do not check freshness for this table

select
  max(_etl_loaded_at) as max_loaded_at,
  convert_timezone('UTC', current_timestamp()) as snapshotted_at
from raw.jaffle_shop.orders

where datediff('day', _etl_loaded_at, current_timestamp) < 2

select
  max({{ loaded_at_field }}) as max_loaded_at,
  {{ current_timestamp() }} as snapshotted_at
from {{ source }}
{% if filter %}
where {{ filter }}
{% endif %}

models:
  <resource-path>:
    +freshness:
      build_after:  # build this model no more often than every X amount of time, as long as it has new data. Available only on dbt platform Enterprise tiers. 
        count: <positive_integer>
        period: minute | hour | day
        updates_on: any | all # optional config

models:
  - name: stg_orders
    config:
      freshness:
        build_after:  # build this model no more often than every X amount of time, as long as it has new data. Available only on dbt platform Enterprise tiers. 
          count: <positive_integer>
          period: minute | hour | day
          updates_on: any | all # optional config

{{
    config(
      freshness={
        "build_after": {     # build this model no more often than every X amount of time, as long as as it has new data
        "count": <positive_integer>,
        "period": "minute" | "hour" | "day",
        "updates_on": "any" | "all" # optional config
        } 
      }
    )
}}

build_after:
  count: 0
  period: minute
  updates_on: any

models:
  - name: stg_wizards
    config:
      freshness:
        build_after: 
          count: 4
          period: hour
          updates_on: all
  - name: stg_worlds
    config:
      freshness:
        build_after: 
          count: 4
          period: hour
          updates_on: all

models:
  - name: stg_wizards
    config: 
      freshness:
        build_after: 
          count: 1
          period: hour
          updates_on: any
  - name: stg_worlds
    config:
      freshness:
        build_after: 
          count: 1
          period: hour
          updates_on: any

+freshness:
  build_after:
    # wait at least 48 hours before building again, if Saturday or Sunday
    # otherwise, wait at least 1 hour before building again
    count: "{{ 48 if modules.datetime.datetime.today().weekday() in (5, 6) else 1 }}"
    period: hour
    updates_on: any

{{
    config(
      freshness={
        "build_after": {
        "count": 48 if modules.datetime.datetime.today().weekday() in (5, 6) else 1,
        "period": "hour",
        "updates_on": "any"
        } 
      }
    )
}}

models:
  <resource-path>:
    +full_refresh: false | true

{{ config(
    full_refresh = false | true
) }}

seeds:
  <resource-path>:
    +full_refresh: false | true

$ dbt seed
Running with dbt=1.6.0-rc2
Found 0 models, 0 tests, 0 snapshots, 0 analyses, 130 macros, 0 operations, 1 seed file, 0 sources

12:12:27 | Concurrency: 8 threads (target='dev_snowflake')
12:12:27 |
12:12:27 | 1 of 1 START seed file dbt_claire.country_codes...................... [RUN]
12:12:30 | 1 of 1 ERROR loading seed file dbt_claire.country_codes.............. [ERROR in 2.78s]
12:12:31 |
12:12:31 | Finished running 1 seed in 10.05s.

Completed with 1 error and 0 warnings:

Database Error in seed country_codes (seeds/country_codes.csv)
  000904 (42000): SQL compilation error: error line 1 at position 62
  invalid identifier 'COUNTRY_NAME'

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

$ dbt seed
Running with dbt=1.6.0-rc2
Found 0 models, 0 tests, 0 snapshots, 0 analyses, 149 macros, 0 operations, 1 seed file, 0 sources

12:14:46 | Concurrency: 1 threads (target='dev_redshift')
12:14:46 |
12:14:46 | 1 of 1 START seed file dbt_claire.country_codes...................... [RUN]
12:14:46 | 1 of 1 ERROR loading seed file dbt_claire.country_codes.............. [ERROR in 0.23s]
12:14:46 |
12:14:46 | Finished running 1 seed in 1.75s.

Completed with 1 error and 0 warnings:

Database Error in seed country_codes (seeds/country_codes.csv)
  column "country_name" of relation "country_codes" does not exist

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

dbt seed --full-refresh

functions:
  <resource-path>:
    # Function-specific configs are defined in the property file
    # See functions/schema.yml examples below

functions:
  - name: [<function-name>]
    config:
      # Standard configs that apply to functions
      database: <string>
      schema: <string>
      alias: <string>
      tags: <string> | [<string>]
      meta: {<dictionary>}

functions:
  <resource-path>:
    +enabled: true | false
    +tags: <string> | [<string>]
    +database: <string>
    +schema: <string>
    +alias: <string>
    +meta: {<dictionary>}

functions:
  - name: [<function-name>]
    config:
      enabled: true | false
      tags: <string> | [<string>]
      database: <string>
      schema: <string>
      alias: <string>
      meta: {<dictionary>}

functions:
  +schema: udf_schema

functions:
  jaffle_shop:
    +schema: udf_schema

functions:
  - name: is_positive_int
    config:
      schema: udf_schema

functions:
  jaffle_shop:
    is_positive_int:
      +schema: udf_schema

name: jaffle_shop
...
functions:
  jaffle_shop:
    +enabled: true
    +schema: udf_schema
    # This configures functions/is_positive_int.sql
    is_positive_int:
      +tags: ['validation']
    marketing:
      +schema: marketing_udfs # this will take precedence

functions:
  - name: is_positive_int
    description: Determines if a string represents a positive integer
    config:
      database: analytics
      schema: udf_schema
    arguments:
      - name: a_string
        data_type: string
        description: The string to check
    returns:
      data_type: boolean
      description: Returns true if the string represents a positive integer

functions:
  - name: <string> # required
    description: <markdown_string> # optional
    type: scalar  # optional, defaults to scalar. Eventually will include aggregate | table
    config: # optional
      <function_config>: <config_value>
      docs:
        show: true | false
        node_color: <color_id> # Use name (such as node_color: purple) or hex code with quotes (such as node_color: "#cd7f32")
    arguments: # optional
      - name: <string> # required if arguments is specified
        data_type: <string> # required if arguments is specified, warehouse-specific
        description: <markdown_string> # optional
      - name: ... # declare additional arguments
    returns: # required
      data_type: <string> # required, warehouse-specific
      description: <markdown_string> # optional

- name: ... # declare properties of additional functions

functions:
  - name: is_positive_int
    description: Determines if a string represents a positive (+) integer
    type: scalar
    config:
      database: analytics
      schema: udf_schema
    arguments:
      - name: a_string
        data_type: string
        description: The string that I want to check if it's representing a positive integer (like "10")
    returns:
      data_type: boolean
      description: Returns true if the input string represents a positive integer, false otherwise

function-paths: [directorypath]

function-paths: ["udfs"]

function-paths: ["functions", "custom_udfs"]

models:
  - name: specific_model
    config:
      grants:
        select: ['reporter', 'bi']

seeds:
  - name: seed_name
    config:
      grants:
        select: ['reporter', 'bi']

snapshots:
  - name: snapshot_name
    config:  
      grants:
        select: ['reporter', 'bi']

models:
  +grants:  # In this case the + is not optional, you must include it for your project to parse.
    select: ['user_a', 'user_b']

{{ config(grants = {'select': ['user_c']}) }}

{{ config(grants = {'+select': ['user_c']}) }}

models:
  +grants:
    select: "{{ ['user_a', 'user_b'] if target.name == 'prod' else ['user_c'] }}"

models:
  +grants:
    select: ['user_a', 'user_b']

models:
  +grants:
    select: ['user_b']

models:
  +grants:
    select: []

# this section intentionally left blank

{{ config(materialized = 'table', grants = {
    'select': 'bi_user'
}) }}

grant select on schema_name.table_model to bi_user;

{{ config(materialized = 'incremental', grants = {
    'select': ['bi_user', 'reporter']
}) }}

grant select on schema_name.incremental_model to bi_user, reporter;

{{ config(grants = {'roles/bigquery.dataViewer': ['user:someone@yourcompany.com']}) }}

models:
  - name: specific_model
    config:
      grants:
        roles/bigquery.dataViewer: ['user:someone@yourcompany.com']

dbt run --select "my_model+"         # select my_model and all descendants
dbt run --select "+my_model"         # select my_model and all ancestors
dbt run --select "+my_model+"        # select my_model, and all of its ancestors and descendants

dbt run --select "my_model+1"        # select my_model and its first-degree descendants
dbt run --select "2+my_model"        # select my_model, its first-degree ancestors ("parents"), and its second-degree ancestors ("grandparents")
dbt run --select "3+my_model+4"      # select my_model, its ancestors up to the 3rd degree, and its descendants down to the 4th degree

dbt run --select "@my_model"         # select my_model, its descendants, and the ancestors of its descendants

{{
    config(
        ...
        distributed_by='<field_name>'
        ...
    )
}}

{{
    config(
        ...
        distributed_replicated=true
        ...
    )
}}

{{
    config(
        ...
        orientation='column'
        ...
    )
}}

{{
    config(
        ...
        appendonly='true',
        compresstype='ZLIB',
        compresslevel=3,
        blocksize=32768
        ...
    )
}}

{% set fields_string %}
    some_filed int4 null,
    date_field timestamp NULL
{% endset %}

{% set raw_partition %}
   PARTITION BY RANGE (date_field)
   (
       START ('2021-01-01'::timestamp) INCLUSIVE
       END ('2023-01-01'::timestamp) EXCLUSIVE
       EVERY (INTERVAL '1 day'),
       DEFAULT PARTITION default_part
   );
{% endset %}

{{
   config(
       ...
       fields_string=fields_string,
       raw_partition=raw_partition,
       ...
   )
}}

<resource-path>:
    +group: GROUP_NAME

models:
  - name: MODEL_NAME
    config:
      group: GROUP # changed to config in v1.10

{{ config(
  group='GROUP_NAME'
) }}

models:
  <resource-path>:
    +group: GROUP_NAME

seeds:
  - name: [SEED_NAME]
    config:
      group: GROUP_NAME # changed to config in v1.10

snapshots:
  <resource-path>:
    +group: GROUP_NAME

{% snapshot snapshot_name %}

{{ config(
  group='GROUP_NAME'
) }}

data_tests:
  <resource-path>:
    +group: GROUP_NAME

<resource_type>:
  - name: <resource_name>
    data_tests:
      - <test_name>:
          config:
            group: GROUP_NAME

{% test <testname>() %}

{{ config(
  group='GROUP_NAME'
) }}

{{ config(
  group='GROUP_NAME'
) }}

analyses:
  - name: ANALYSIS_NAME
    config:
      group: GROUP_NAME # changed to config in v1.10

metrics:
  <resource-path>:
    +group: GROUP_NAME

metrics:
  - name: [METRIC_NAME]
    config:
      group: GROUP_NAME

semantic-models:
  <resource-path>:
    +group: GROUP_NAME

semantic_models:
  - name: SEMANTIC_MODEL_NAME
    config:
      group: GROUP_NAME

saved-queries:
  <resource-path>:
    +group: GROUP_NAME

saved_queries:
  - name: SAVED_QUERY_NAME
    config:
      group: GROUP_NAME

models:
  - name: finance_model
    config:
      group: finance # changed to config in v1.10
      access: private # changed to config in v1.10
  - name: marketing_model
    config:
      group: marketing # changed to config in v1.10

select * from {{ ref('finance_model') }}

$ dbt run -s marketing_model
...
dbt.exceptions.DbtReferenceError: Parsing Error
  Node model.jaffle_shop.marketing_model attempted to reference node model.jaffle_shop.finance_model, 
  which is not allowed because the referenced node is private to the finance group.

snapshots:
  - name: <snapshot_name>
    config:
      hard_deletes: 'ignore' | 'invalidate' | 'new_record'

snapshots:
  <resource-path>:
    +hard_deletes: "ignore" | "invalidate" | "new_record"

{{
    config(
        unique_key='id',
        strategy='timestamp',
        updated_at='updated_at',
        hard_deletes='ignore' | 'invalidate' | 'new_record'
    )
}}

snapshots:
  - name: my_snapshot
    config:
      hard_deletes: new_record  # options are: 'ignore', 'invalidate', or 'new_record'
      strategy: timestamp
      updated_at: updated_at
    columns:
      - name: dbt_valid_from
        description: Timestamp when the record became valid.
      - name: dbt_valid_to
        description: Timestamp when the record stopped being valid.
      - name: dbt_is_deleted
        description: Indicates whether the record was deleted.

{{
  config(
    pre_hook="set session query_max_run_time='10m'"
  )
}}

{{
  config(
    materialized='table',
    properties={
      "format": "'PARQUET'", -- Specifies the file format
      "partitioned_by": "ARRAY['id']", -- Defines the partitioning column(s)
    }
  )
}}

{{
  config(
    materialized='table',
    properties={
      "format": "'ORC'", -- Specifies the file format
      "partitioning": "ARRAY['bucket(id, 2)']", -- Defines the partitioning strategy
    }
  )
}}

PrestoUserError(type=USER_ERROR, name=NOT_SUPPORTED, message="This connector does not support creating tables with data", query_id=20241206_071536_00026_am48r)

{{
  config(
    pre_hook="set session query_max_run_time='10m'"
  )
}}

project_name:
  target: "dev"
  outputs:
    dev:
      type: watsonx_spark
      method: http
      schema: [schema name]
      host: [hostname]
      uri: [uri]
      catalog: [catalog name]
      use_ssl: false
      auth:
        instance: [Watsonx.data Instance ID]
        user: [username]
        apikey: [apikey]

{{
  config(
    materialized='table',
    file_format='iceberg' or 'hive' or 'delta' or 'hudi'
  )
}}

sources:
  - name: <source_name>
    database: <database_name>
    tables:
      - name: <table_name>
        identifier: <table_identifier>

sources:
  - name: jaffle_shop
    tables:
      - name: orders
        identifier: api_orders

select * from {{ source('jaffle_shop', 'orders') }}

select * from jaffle_shop.api_orders

sources:
  - name: ga
    tables:
      - name: events
        identifier: "events_*"

select * from {{ source('ga', 'events') }}

-- filter on shards by suffix
where _table_suffix > '20200101'

select * from `my_project`.`ga`.`events_*`

-- filter on shards by suffix
where _table_suffix > '20200101'

dbt test --indirect-selection cautious

$ export DBT_INDIRECT_SELECTION=cautious
dbt run

flags:
  indirect_selection: cautious

<profile-name>:
  target: <target-name>
  outputs:
    <target-name>:
      type: infer
      url: "<infer-api-endpoint>"
      username: "<infer-api-username>"
      apikey: "<infer-apikey>"
      data_config:
        [configuration for your underlying data warehouse]

unit_tests:
  - name: test_is_valid_email_address # this is the unique name of the test
    model: dim_customers # name of the model I'm unit testing
    given: # the mock data for your inputs
      - input: ref('stg_customers')
        rows:
         - {email: cool@example.com,     email_top_level_domain: example.com}
         - {email: cool@unknown.com,     email_top_level_domain: unknown.com}
         - {email: badgmail.com,         email_top_level_domain: gmail.com}
         - {email: missingdot@gmailcom,  email_top_level_domain: gmail.com}
      - input: ref('top_level_email_domains')
        rows:
         - {tld: example.com}
         - {tld: gmail.com}
...

snapshots:
  <resource-path>:
    +strategy: timestamp
    +invalidate_hard_deletes: true

dbt run --no-write-json

models:
  - name: model_name
    latest_version: 2
    versions:
      - v: 2
      - v: 1

models:
  - name: model_name
    versions:
      - v: 3
      - v: 2
      - v: 1

models:
  - name: model_name
    latest_version: 2
    versions:
      - v: 3
      - v: 2
      - v: 1

{ % snapshot orders_snapshot %}

{{ config(
    target_schema="<string>",
    target_database="<string>",
    unique_key="<column_name_or_expression>",
    strategy="timestamp" | "check",
    updated_at="<column_name>",
    check_cols=["<column_name>"] | "all"
    invalidate_hard_deletes : true | false
) 
}}

select * from {{ source('jaffle_shop', 'orders') }}

{{ config(
    enabled=true | false,
    tags="<string>" | ["<string>"],
    alias="<string>", 
    pre_hook="<sql-statement>" | ["<sql-statement>"],
    post_hook="<sql-statement>" | ["<sql-statement>"]
    persist_docs={<dict>}
    grants={<dict>}
) }}

{% snapshot orders_snapshot_timestamp %}

{{
        config(
          target_schema='snapshots',
          strategy='timestamp',
          unique_key='id',
          updated_at='updated_at',
        )
    }}

select * from {{ source('jaffle_shop', 'orders') }}

{% snapshot orders_snapshot_check %}

{{
        config(
          strategy='check',
          unique_key='id',
          check_cols=['status', 'is_cancelled'],
        )
    }}

select * from {{ source('jaffle_shop', 'orders') }}

{% snapshot orders_snapshot_check %}

{{
        config(
          strategy='check',
          unique_key='id',
          check_cols=['status', 'is_cancelled'],
        )
    }}

select * from {{ source('jaffle_shop', 'orders') }}

{% snapshot orders_snapshot_check %}

{{
        config(
          strategy='check',
          unique_key='id',
          check_cols='all',
        )
    }}

select * from {{ source('jaffle_shop', 'orders') }}

{% snapshot orders_snapshot %}

{% snapshot orders_snapshot %}

select * from {{ source('jaffle_shop', 'orders') }}

Running with dbt=1.8.0

15:07:36 | Concurrency: 8 threads (target='dev')
15:07:36 |
15:07:36 | 1 of 1 START snapshot snapshots.orders_snapshot...... [RUN]
15:07:36 | 1 of 1 OK snapshot snapshots.orders_snapshot..........[SELECT 3 in 1.82s]
15:07:36 |
15:07:36 | Finished running 1 snapshots in 0.68s.

Completed successfully

Done. PASS=2 ERROR=0 SKIP=0 TOTAL=1

select * from {{ ref('orders_snapshot') }}

{% snapshot orders_snapshot %}
    {{
        config(
          unique_key='id',
          strategy='timestamp',
          updated_at='updated_at'
        )
    }}
    -- Pro-Tip: Use sources in snapshots!
    select * from {{ source('jaffle_shop', 'orders') }}
{% endsnapshot %}

{{ config(
  strategy="timestamp",
  updated_at="column_name"
) }}

{{ config(
  unique_key="column_name"
) }}

{{
      config(
        unique_key="id"
      )
  }}
  
  {% snapshot transaction_items_snapshot %}

{{
          config(
            unique_key="transaction_id||'-'||line_item_id",
            ...
          )
      }}

select
      transaction_id||'-'||line_item_id as id,
      *
  from {{ source('erp', 'transactions') }}

{% endsnapshot %}
  
  {% snapshot transaction_items_snapshot %}

{{
          config(
            unique_key="id",
            ...
          )
      }}

select
      transaction_id || '-' || line_item_id as id,
      *
  from {{ source('erp', 'transactions') }}

models:
  - name: large_table
    columns:
      - name: very_unreliable_column
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ["a", "b", "c"]
              config:
                limit: 1000  # will only include the first 1000 failures

{{ config(limit = 1000) }}

{% test <testname>(model, column_name) %}

{{ config(limit = 500) }}

data_tests:
  +limit: 1000  # all tests
  
  <package_name>:
    +limit: 50 # tests in <package_name>

sources:
  - name: <source_name>
    database: <database_name>
    loader: <string>
    tables:
      - ...

sources:
  - name: jaffle_shop
    loader: fivetran
    tables:
      - name: orders
      - name: customers

- name: stripe
    loader: stitch
    tables:
      - name: payments

def log(msg: str, info: bool = False) -> str: 
        """Logs a line to either the log file or stdout.

:param msg: The message to log
        :param info: If `False`, write to the log file. If `True`, write to
            both the log file and stdout.

> macros/my_log_macro.sql

{% macro some_macro(arg1, arg2) %}
              {{ log("Running some_macro: " ~ arg1 ~ ", " ~ arg2) }}
            {% endmacro %}"
        """
        if info:
            fire_event(JinjaLogInfo(msg=msg, node_info=get_node_info()))
        else:
            fire_event(JinjaLogDebug(msg=msg, node_info=get_node_info()))
        return ""

{% macro some_macro(arg1, arg2) %}

{{ log("Running some_macro: " ~ arg1 ~ ", " ~ arg2) }}

dbt run --log-format json

23:30:16  Running with dbt=1.8.0
23:30:17  Registered adapter: postgres=1.8.0

============================== 16:12:08.555032 | 9089bafa-4010-4f38-9b42-564ec9106e07 ==============================
16:12:08.555032 [info ] [MainThread]: Running with dbt=1.8.0
16:12:08.751069 [info ] [MainThread]: Registered adapter: postgres=1.8.0

{"data": {"log_version": 3, "version": "=1.8.0"}, "info": {"category": "", "code": "A001", "extra": {}, "invocation_id": "82131fa0-d2b4-4a77-9436-019834e22746", "level": "info", "msg": "Running with dbt=1.8.0", "name": "MainReportVersion", "pid": 7875, "thread": "MainThread", "ts": "2024-05-29T23:32:54.993336Z"}}
{"data": {"adapter_name": "postgres", "adapter_version": "=1.8.0"}, "info": {"category": "", "code": "E034", "extra": {}, "invocation_id": "82131fa0-d2b4-4a77-9436-019834e22746", "level": "info", "msg": "Registered adapter: postgres=1.8.0", "name": "AdapterRegistered", "pid": 7875, "thread": "MainThread", "ts": "2024-05-29T23:32:56.437986Z"}}

dbt run --log-format-file json

dbt run --debug --log-format json

dbt run --log-level debug
  
  dbt run --log-level none
  
  dbt run --log-level-file error
  
  dbt run --log-level-file none
  
dbt run --debug

config:
  quiet: true

dbt compile --log-cache-events

config:
  use_colors_file: False

dbt run --use-colors-file
dbt run --no-use-colors-file

models:
  my_project:
    user_sessions:
      +lookback: 2

models:
  - name: user_sessions
    config:
      lookback: 2

{{ config(
    lookback=2
) }}

macros:
  - name: <macro name>
    description: <markdown_string>
    config:
      docs:
        show: true | false
      meta: {<dictionary>}
    arguments:
      - name: <arg name>
        type: <string>
        description: <markdown_string>
      - ... # declare properties of additional arguments

- name: ... # declare properties of additional macros

macro-paths: [directorypath]

macro-paths: ["macros"]
    
    macro-paths: ["/Users/username/project/macros"]
    
macro-paths: ["custom_macros"]

{{ config(materialized='materializedview', cluster='not_default') }}

models:
  project_name:
    +materialized: materializedview
    +cluster: not_default

{{ config(materialized='view',
          indexes=[{'columns': ['col_a'], 'cluster': 'cluster_a'}]) }}
          indexes=[{'columns': ['symbol']}]) }}

{{ config(materialized='view',
    indexes=[{'default': True}]) }}

data_tests:
  project_name:
    +store_failures: true
    +schema: test

models:
  <resource-path>:
    +materialized: <materialization_name>

models:
  - name: <model_name>
    config:
      materialized: <materialization_name>

{{ config(
  materialized="<materialization_name>"
) }}

models:
  <resource-path>:
    +meta: {<dictionary>}

models:
  - name: model_name
    config:
      meta: {<dictionary>}

columns:
      - name: column_name
        config:
          meta: {<dictionary>} # changed to config in v1.10 and backported to 1.9

sources:
  <resource-path>:
    +meta: {<dictionary>}

sources:
  - name: model_name
    config:
      meta: {<dictionary>}

tables:
      - name: table_name
        config:
          meta: {<dictionary>}

columns:
          - name: column_name
            config:
              meta: {<dictionary>} # changed to config in v1.10 and backported to 1.9

seeds:
  <resource-path>:
    +meta: {<dictionary>}

seeds:
  - name: seed_name
    config:
      meta: {<dictionary>}

columns:
      - name: column_name
        config:
          meta: {<dictionary>} # changed to config in v1.10 and backported to 1.9

snapshots:
  <resource-path>:
    +meta: {<dictionary>}

snapshots:
  - name: snapshot_name
    config:
      meta: {<dictionary>}

columns:
      - name: column_name
        config:
          meta: {<dictionary>} # changed to config in v1.10 and backported to 1.9

unit_tests:
  <resource-path>:
    +meta: {<dictionary>}

unit_tests:
  - name: <test-name>
    config:
      meta: {<dictionary>}

macros:
  <resource-path>:
    +meta: {<dictionary>}

macros:
  - name: macro_name
    config:
      meta: {<dictionary>} # changed to config in v1.10

arguments:
      - name: argument_name

exposures:
  <resource-path>:
    +meta: {<dictionary>}

exposures:
  - name: exposure_name
    config:
      meta: {<dictionary>} # changed to config in v1.10

metrics:
  <resource-path>:
    +meta: {<dictionary>}

metrics:
  - name: number_of_people
    label: "Number of people"
    description: Total count of people
    type: simple
    type_params:
      measure: people
    config:
      meta:
        my_meta_config: 'config_value'

saved-queries:
  <resource-path>:
    +meta: {<dictionary>}

saved_queries:
  - name: saved_query_name
    config:
      meta: {<dictionary>}

models:
  - name: users
    config:
      meta:
        owner: "@alice"
        model_maturity: in dev

sources:
  - name: salesforce
    tables:
      - name: account
        config:
          meta:
            contains_pii: true
        columns:
          - name: email
            config:
              meta: # changed to config in v1.10 and backported to 1.9
                contains_pii: true

seeds:
  +meta:
    favorite_color: red

{{ config(meta = {
    'single_key': 'override'
}) }}

models:
  jaffle_shop:
    +meta:
      owner: "@alice"
      favorite_color: red

semantic_models:
  - name: transaction 
    model: ref('fact_transactions')
    description: "Transaction fact table at the transaction level. This table contains one row per transaction and includes the transaction timestamp."
    defaults:
      agg_time_dimension: transaction_date
    config:
      meta:
        data_owner: "Finance team"
        used_in_reporting: true

semantic-models:
  jaffle_shop:
    +meta:
      used_in_reporting: true

{{
    config(
        index='HEAP',
        dist='ROUND_ROBIN'
        )
}}

models:
  your_project_name:
    materialized: view
    staging:
      materialized: table
      index: HEAP

{{
    config(
        materialized='table'
        )
}}

models:
  your_project_name:
    materialized: view
    staging:
      materialized: table

vars:
  max_batch_size: 200 # Any integer less than or equal to 2100 will do.

{{ config(
    materialized='incremental',
    incremental_strategy='append',
) }}

--  All rows returned by this query will be appended to the existing table

select * from {{ ref('events') }}
{% if is_incremental() %}
  where event_ts > (select max(event_ts) from {{ this }})
{% endif %}

create temporary view fabricspark_incremental__dbt_tmp as

select * from analytics.events

where event_ts >= (select max(event_ts) from {{ this }})

insert into table analytics.fabricspark_incremental
    select `date_day`, `users` from spark_incremental__dbt_tmp

{{ config(
    materialized='incremental',
    partition_by=['date_day'],
    file_format='parquet'
) }}

/*
  Every partition returned by this query will be overwritten
  when this model runs
*/

select * from {{ ref('events') }}

{% if is_incremental() %}
    where date_day >= date_add(current_date, -1)
    {% endif %}

select
    date_day,
    count(*) as users

from events
group by 1

create temporary view fabricspark_incremental__dbt_tmp as

select * from analytics.events

where date_day >= date_add(current_date, -1)

select
        date_day,
        count(*) as users

from events
    group by 1

insert overwrite table analytics.fabricspark_incremental
    partition (date_day)
    select `date_day`, `users` from spark_incremental__dbt_tmp

{{ config(
    materialized='incremental',
    file_format='delta',
    unique_key='user_id',
    incremental_strategy='merge'
) }}

select * from {{ ref('events') }}

{% if is_incremental() %}
    where date_day >= date_add(current_date, -1)
    {% endif %}

select
    user_id,
    max(date_day) as last_seen

from events
group by 1

create temporary view merge_incremental__dbt_tmp as

select * from analytics.events

where date_day >= date_add(current_date, -1)

select
        user_id,
        max(date_day) as last_seen

from events
    group by 1

merge into analytics.merge_incremental as DBT_INTERNAL_DEST
    using merge_incremental__dbt_tmp as DBT_INTERNAL_SOURCE
    on DBT_INTERNAL_SOURCE.user_id = DBT_INTERNAL_DEST.user_id
    when matched then update set *
    when not matched then insert *

models:
  +file_format: delta
  
seeds:
  +file_format: delta
  
snapshots:
  +file_format: delta

{{
    config(
        as_columnstore=false
        )
}}

models:
  your_project_name:
    materialized: view
    staging:
      materialized: table
      as_columnstore: False

vars:
  max_batch_size: 200 # Any integer less than or equal to 2100 will do.

{{
    config({
        "as_columnstore": false,
        "materialized": 'table',
        "post-hook": [
            "{{ create_clustered_index(columns = ['row_id', 'row_id_complement'], unique=True) }}",
            "{{ create_nonclustered_index(columns = ['modified_date']) }}",
            "{{ create_nonclustered_index(columns = ['row_id'], includes = ['modified_date']) }}",
        ]
    })

models:
  your_project_name:
    auto_provision_aad_principals: true

-- my_first_model.sql    
    {{
        config(
            materialized='predictor',
            integration='photorep',
            predict='name',
            predict_alias='name',
            using={
                'encoders.location.module': 'CategoricalAutoEncoder',
                'encoders.rental_price.module': 'NumericEncoder'
            }
        )
    }}
      select * from stores

{{ config(materialized='table', predictor_name='TEST_PREDICTOR_NAME', integration='photorep') }}
        select a, bc from ddd where name > latest

models:
  # Be sure to namespace your model configs to your project name
  dbt_labs:

# This configures models found in models/events/
    events:
      +enabled: true
      +materialized: view

# This configures models found in models/events/base
      # These models will be ephemeral, as the config above is overridden
      base:
        +materialized: ephemeral

{{
  config(
    materialized = "table",
    tags = ["core", "events"]
  )
}}

select * from {{ ref('raw_events') }}

models:
  - name: base_events
    description: "Standardized event data from raw sources"
    columns:
      - name: user_id
        description: "Unique identifier for a user"
        data_tests:
          - not_null
          - unique
      - name: event_type
        description: "Type of event recorded (click, purchase, etc.)"

models:
  # Model name must match the filename of a model -- including case sensitivity
  - name: model_name
    description: <markdown_string>
    latest_version: <version_identifier>
    deprecation_date: <YAML_DateTime>
    config:
      <model_config>: <config_value>
      docs:
        show: true | false
        node_color: <color_id> # Use name (such as node_color: purple) or hex code with quotes (such as node_color: "#cd7f32")
      access: private | protected | public
    constraints:
      - <constraint>
    data_tests:
      - <test>
      - ... # declare additional data tests
    columns:
      - name: <column_name> # required
        description: <markdown_string>
        quote: true | false
        constraints:
          - <constraint>
        data_tests:
          - <test>
          - ... # declare additional data tests
        config:
          meta: {<dictionary>}
          tags: [<string>]
        
        # only required in conjunction with time_spine key
        granularity: <any supported time granularity>

- name: ... # declare properties of additional columns

time_spine:
      standard_granularity_column: <column_name>

versions:
      - v: <version_identifier> # required
        defined_in: <definition_file_name>
        description: <markdown_string>
        constraints:
          - <constraint>
        config:
          <model_config>: <config_value>
          docs:
            show: true | false
          access: private | protected | public
        data_tests:
          - <test>
          - ... # declare additional data tests
        columns:
          # include/exclude columns from the top-level model properties
          - include: <include_value>
            exclude: <exclude_list>
          # specify additional columns
          - name: <column_name> # required
            quote: true | false
            constraints:
              - <constraint>
            data_tests:
              - <test>
              - ... # declare additional data tests
            tags: [<string>]
        - v: ... # declare additional versions

models:
  - name: model_name

model-paths: [directorypath]

model-paths: ["models"]
    
    model-paths: ["/Users/username/project/models"]
    
model-paths: ["transformations"]

Encountered an error while reading the project:
  ERROR: Runtime Error
  at path ['name']: 'jaffle-shop' does not match '^[^\\d\\W]\\w*$'
Runtime Error
  Could not run dbt

dbt list --select "*.folder_name.*"
dbt list --select "package:*_source"

dbt list --select "access:public"      # list all public models
dbt list --select "access:private"       # list all private models
dbt list --select "access:protected"       # list all protected models

dbt run --select "config.materialized:incremental"    # run all models that are materialized incrementally
dbt run --select "config.schema:audit"              # run all models that are created in the `audit` schema
dbt run --select "config.cluster_by:geo_country"      # run all models clustered by `geo_country`

{{ config(
  materialized = 'incremental',
  unique_key = ['column_a', 'column_b'],
  grants = {'select': ['reporter', 'analysts']},
  meta = {"contains_pii": true},
  transient = true
) }}

dbt ls -s config.materialized:incremental
dbt ls -s config.unique_key:column_a
dbt ls -s config.grants.select:reporter
dbt ls -s config.meta.contains_pii:true
dbt ls -s config.transient:true

dbt run --select "+exposure:weekly_kpis"                # run all models that feed into the weekly_kpis exposure
dbt test --select "+exposure:*"                         # test all resources upstream of all exposures
dbt ls --select "+exposure:*" --resource-type source    # list all source tables upstream of all exposures

dbt run --select "fqn:some_model"
dbt run --select "fqn:your_project.some_model"
dbt run --select "fqn:some_package.some_other_model"
dbt run --select "fqn:some_path.some_model"
dbt run --select "fqn:your_project.some_path.some_model"

dbt run --select "group:finance" # run all models that belong to the finance group.

dbt build --select "+metric:weekly_active_users"       # build all resources upstream of weekly_active_users metric
dbt ls    --select "+metric:*" --resource-type source  # list all source tables upstream of all metrics

**Examples:**

Example 1 (unknown):
```unknown
#### Incremental models[​](#incremental-models "Direct link to Incremental models")

The [`incremental_strategy` configuration](https://docs.getdbt.com/docs/build/incremental-strategy.md) controls how dbt builds incremental models. Firebolt currently supports `append`, `insert_overwrite` and `delete+insert` configuration. You can specify `incremental_strategy` in `dbt_project.yml` or within a model file's `config()` block. The `append` configuration is the default. Specifying this configuration is optional.

The `append` strategy performs an `INSERT INTO` statement with all the new data based on the model definition. This strategy doesn't update or delete existing rows, so if you do not filter the data to the most recent records only, it is likely that duplicate records will be inserted.

Example source code:
```

Example 2 (unknown):
```unknown
Example run code:
```

Example 3 (unknown):
```unknown
#### Seeds behavior[​](#seeds-behavior "Direct link to Seeds behavior")

When running the `dbt seed` command we perform a `DROP CASCADE` operation instead of `TRUNCATE`.

#### Practice[​](#practice "Direct link to Practice")

You can look at our modified version of the jaffle\_shop, [jaffle\_shop\_firebolt](https://github.com/firebolt-db/jaffle_shop_firebolt), to see how indexes, as well as external tables, can be set or clone and execute the commands listed in the README.md

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### freshness

* Project file
* Model YAML

dbt\_project.yml
```

Example 4 (unknown):
```unknown
models/\<filename>.yml
```

---

## class must begin with 'Test'

**URL:** llms-txt#class-must-begin-with-'test'

class TestExample:
    """
    Methods in this class will be of two types:
    1. Fixtures defining the dbt "project" for this test case.
       These are scoped to the class, and reused for all tests in the class.
    2. Actual tests, whose names begin with 'test_'.
       These define sequences of dbt commands and 'assert' statements.
    """
    
    # configuration in dbt_project.yml
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
          "name": "example",
          "models": {"+materialized": "view"}
        }

# everything that goes in the "seeds" directory
    @pytest.fixture(scope="class")
    def seeds(self):
        return {
            "my_seed.csv": my_seed_csv,
        }

# everything that goes in the "models" directory
    @pytest.fixture(scope="class")
    def models(self):
        return {
            "my_model.sql": my_model_sql,
            "my_model.yml": my_model_yml,
        }
        
    # continues below

# continued from above

# The actual sequence of dbt commands and assertions
    # pytest will take care of all "setup" + "teardown"
    def test_run_seed_test(self, project):
        """
        Seed, then run, then test. We expect one of the tests to fail
        An alternative pattern is to use pytest "xfail" (see below)
        """
        # seed seeds
        results = run_dbt(["seed"])
        assert len(results) == 1
        # run models
        results = run_dbt(["run"])
        assert len(results) == 1
        # test tests
        results = run_dbt(["test"], expect_pass = False) # expect failing test
        assert len(results) == 2
        # validate that the results include one pass and one failure
        result_statuses = sorted(r.status for r in results)
        assert result_statuses == ["fail", "pass"]

@pytest.mark.xfail
    def test_build(self, project):
        """Expect a failing test"""
        # do it all
        results = run_dbt(["build"])

$ python3 -m pytest tests/functional/test_example.py
=========================== test session starts ============================
platform ... -- Python ..., pytest-..., pluggy-...
rootdir: ...
plugins: ...

tests/functional/test_example.py .X                                  [100%]

======================= 1 passed, 1 xpassed in 1.38s =======================

pytest
pytest-dotenv
dbt-tests-adapter

python -m pip install -r dev_requirements.txt

[pytest]
filterwarnings =
    ignore:.*'soft_unicode' has been renamed to 'soft_str'*:DeprecationWarning
    ignore:unclosed file .*:ResourceWarning
env_files =
    test.env  # uses pytest-dotenv plugin
              # this allows you to store env vars for database connection in a file named test.env
              # rather than passing them in every CLI command, or setting in `PYTEST_ADDOPTS`
              # be sure to add "test.env" to .gitignore as well!
testpaths =
    tests/functional  # name per convention

import pytest
import os

**Examples:**

Example 1 (unknown):
```unknown
3. Now that we've set up our project, it's time to define a sequence of dbt commands and assertions. We define one or more methods in the same file, on the same class (`TestExampleFailingTest`), whose names begin with `test_`. These methods share the same setup (project scenario) from above, but they can be run independently by pytest—so they shouldn't depend on each other in any way.

tests/functional/example/test\_example\_failing\_test.py
```

Example 2 (unknown):
```unknown
3. Our test is ready to run! The last step is to invoke `pytest` from your command line. We'll walk through the actual setup and configuration of `pytest` in the next section.

terminal
```

Example 3 (unknown):
```unknown
You can find more ways to run tests, along with a full command reference, in the [pytest usage docs](https://docs.pytest.org/how-to/usage.html).

We've found the `-s` flag (or `--capture=no`) helpful to print logs from the underlying dbt invocations, and to step into an interactive debugger if you've added one. You can also use environment variables to set [global dbt configs](https://docs.getdbt.com/reference/global-configs/about-global-configs.md), such as `DBT_DEBUG` (to show debug-level logs).

##### Testing this adapter[​](#testing-this-adapter "Direct link to Testing this adapter")

Anyone who installs `dbt-core`, and wishes to define their own test cases, can use the framework presented in the first section. The framework is especially useful for testing standard dbt behavior across different databases.

To that end, we have built and made available a [package of reusable adapter test cases](https://github.com/dbt-labs/dbt-adapters/tree/main/dbt-tests-adapter), for creators and maintainers of adapter plugins. These test cases cover basic expected functionality, as well as functionality that frequently requires different implementations across databases.

For the time being, this package is also located within the `dbt-core` repository, but separate from the `dbt-core` Python package.

##### Categories of tests[​](#categories-of-tests "Direct link to Categories of tests")

In the course of creating and maintaining your adapter, it's likely that you will end up implementing tests that fall into three broad categories:

1. **Basic tests** that every adapter plugin is expected to pass. These are defined in `tests.adapter.basic`. Given differences across data platforms, these may require slight modification or reimplementation. Significantly overriding or disabling these tests should be with good reason, since each represents basic functionality expected by dbt users. For example, if your adapter does not support incremental models, you should disable the test, [by marking it with `skip` or `xfail`](https://docs.pytest.org/en/latest/how-to/skipping.html), as well as noting that limitation in any documentation, READMEs, and usage guides that accompany your adapter.

2. **Optional tests**, for second-order functionality that is common across plugins, but not required for basic use. Your plugin can opt into these test cases by inheriting existing ones, or reimplementing them with adjustments. For now, this category includes all tests located outside the `basic` subdirectory. More tests will be added as we convert older tests defined on dbt-core and mature plugins to use the standard framework.

3. **Custom tests**, for behavior that is specific to your adapter / data platform. Each data warehouse has its own specialties and idiosyncracies. We encourage you to use the same `pytest`-based framework, utilities, and fixtures to write your own custom tests for functionality that is unique to your adapter.

If you run into an issue with the core framework, or the basic/optional test cases—or if you've written a custom test that you believe would be relevant and useful for other adapter plugin developers—please open an issue or PR in the `dbt-core` repository on GitHub.

##### Getting started running basic tests[​](#getting-started-running-basic-tests "Direct link to Getting started running basic tests")

In this section, we'll walk through the three steps to start running our basic test cases on your adapter plugin:

1. Install dependencies
2. Set up and configure pytest
3. Define test cases

##### Install dependencies[​](#install-dependencies "Direct link to Install dependencies")

You should already have a virtual environment with `dbt-core` and your adapter plugin installed. You'll also need to install:

* [`pytest`](https://pypi.org/project/pytest/)
* [`dbt-tests-adapter`](https://pypi.org/project/dbt-tests-adapter/), the set of common test cases
* (optional) [`pytest` plugins](https://docs.pytest.org/en/7.0.x/reference/plugin_list.html)--we'll use `pytest-dotenv` below

Or specify all dependencies in a requirements file like:

dev\_requirements.txt
```

Example 4 (unknown):
```unknown

```

---

## this job calls the dbt API to run a job

**URL:** llms-txt#this-job-calls-the-dbt-api-to-run-a-job

**Contents:**
  - Debug errors
  - Debug schema names
  - Get started with Continuous Integration tests

run-dbt-cloud-job:
  stage: build
  rules:
    - if: $CI_PIPELINE_SOURCE == "push" && $CI_COMMIT_BRANCH == 'main'
  script:
    - python python/run_and_monitor_dbt_job.py

trigger: [ main ] # runs on pushes to main

variables:
  DBT_URL:                 https://cloud.getdbt.com # no trailing backslash, adjust this accordingly for single-tenant deployments
  DBT_JOB_CAUSE:           'Azure Pipeline CI Job' # provide a descriptive job cause here for easier debugging down the road
  DBT_ACCOUNT_ID:          00000 # enter your account id
  DBT_PROJECT_ID:          00000 # enter your project id
  DBT_PR_JOB_ID:           00000 # enter your job id

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.7'
    displayName: 'Use Python 3.7'

- script: |
      python -m pip install requests
    displayName: 'Install python dependencies'

- script: |
      python -u ./python/run_and_monitor_dbt_job.py
    displayName: 'Run dbt job '
    env:
      DBT_API_KEY: $(DBT_API_KEY) # Set these values as secrets in the Azure pipelines Web UI

pipelines:
  branches:
    'main': # override if your default branch doesn't run on a branch named "main"
      - step:
          name: 'Run dbt Job'
          script:
            - export DBT_URL="https://cloud.getdbt.com" # if you have a single-tenant deployment, adjust this accordingly
            - export DBT_JOB_CAUSE="Bitbucket Pipeline CI Job"
            - export DBT_ACCOUNT_ID=00000 # enter your account id here
            - export DBT_PROJECT_ID=00000 # enter your project id here
            - export DBT_PR_JOB_ID=00000 # enter your job id here
            - python python/run_and_monitor_dbt_job.py

pipelines:
  branches:
    '**': # this sets a wildcard to run on every branch unless specified by name below
      - step:
          name: Lint dbt project
          script:
            - python -m pip install sqlfluff==0.13.1
            - sqlfluff lint models --dialect snowflake --rules L019,L020,L021,L022

'main': # override if your default branch doesn't run on a branch named "main"
      - step:
          name: 'Run dbt Job'
          script:
            - export DBT_URL="https://cloud.getdbt.com" # if you have a single-tenant deployment, adjust this accordingly
            - export DBT_JOB_CAUSE="Bitbucket Pipeline CI Job"
            - export DBT_ACCOUNT_ID=00000 # enter your account id here
            - export DBT_PROJECT_ID=00000 # enter your project id here
            - export DBT_PR_JOB_ID=00000 # enter your job id here
            - python python/run_and_monitor_dbt_job.py

pipelines:
  # This job will run when pull requests are created in the repository
  pull-requests:
    '**':
      - step:
          name: 'Run dbt PR Job'
          script:
            # Check to only build if PR destination is master (or other branch). 
            # Comment or remove line below if you want to run on all PR's regardless of destination branch.
            - if [ "${BITBUCKET_PR_DESTINATION_BRANCH}" != "main" ]; then printf 'PR Destination is not master, exiting.'; exit; fi
            - export DBT_URL="https://cloud.getdbt.com"
            - export DBT_JOB_CAUSE="Bitbucket Pipeline CI Job"
            - export DBT_JOB_BRANCH=$BITBUCKET_BRANCH
            - export DBT_JOB_SCHEMA_OVERRIDE="DBT_CLOUD_PR_"$BITBUCKET_PROJECT_KEY"_"$BITBUCKET_PR_ID
            - export DBT_ACCOUNT_ID=00000 # enter your account id here
            - export DBT_PROJECT_ID=00000 # enter your project id here
            - export DBT_PR_JOB_ID=00000 # enter your job id here
            - python python/run_and_monitor_dbt_job.py

{# 
    This macro finds PR schemas older than a set date and drops them 
    The macro defaults to 10 days old, but can be configured with the input argument age_in_days
    Sample usage with different date:
        dbt run-operation pr_schema_cleanup --args "{'database_to_clean': 'analytics','age_in_days':'15'}"
#}
{% macro pr_schema_cleanup(database_to_clean, age_in_days=10) %}

{% set find_old_schemas %}
        select 
            'drop schema {{ database_to_clean }}.'||schema_name||';'
        from {{ database_to_clean }}.information_schema.schemata
        where
            catalog_name = '{{ database_to_clean | upper }}'
            and schema_name ilike 'DBT_CLOUD_PR%'
            and last_altered <= (current_date() - interval '{{ age_in_days }} days')
    {% endset %}

{{ log('Schema drop statements:' ,True) }}

{% set schema_drop_list = run_query(find_old_schemas).columns[0].values() %}

{% for schema_to_drop in schema_drop_list %}
            {% do run_query(schema_to_drop) %}
            {{ log(schema_to_drop ,True) }}
        {% endfor %}

Running with dbt=1.7.1
Encountered an error:
Runtime Error
  fatal: Not a dbt project (or any of the parent directories). Missing dbt_project.yml file

Running with dbt=1.7.1

Encountered an error:
Runtime Error
  Could not run dbt
  Could not find profile named 'jaffle_shops'

profile: jaffle_shops # note the plural

jaffle_shop: # this does not match the profile: key
  target: dev

outputs:
    dev:
      type: postgres
      schema: dbt_alice
      ... # other connection details

$ dbt debug --config-dir
Running with dbt=1.7.1
To view your profiles.yml file, run:

open /Users/alice/.dbt

Encountered an error:
Runtime Error
  Database error while listing schemas in database "analytics"
  Database Error
    250001 (08001): Failed to connect to DB: your_db.snowflakecomputing.com:443. Incorrect username or password was specified.

$ dbt debug
Running with dbt=1.7.1
Using profiles.yml file at /Users/alice/.dbt/profiles.yml
Using dbt_project.yml file at /Users/alice/jaffle-shop-dbt/dbt_project.yml

Configuration:
  profiles.yml file [OK found and valid]
  dbt_project.yml file [OK found and valid]

Required dependencies:
 - git [OK found]

Connection:
  ...
  Connection test: OK connection ok

Encountered an error while reading the project:
  ERROR: Runtime Error
  at path []: Additional properties are not allowed ('hello' was unexpected)

Error encountered in /Users/alice/jaffle-shop-dbt/dbt_project.yml
Encountered an error:
Runtime Error
  Could not run dbt

name: jaffle_shop
hello: world # this is not allowed

$ dbt run -s customers
Running with dbt=1.1.0

Encountered an error:
Compilation Error in model customers (models/customers.sql)
  Model 'model.jaffle_shop.customers' (models/customers.sql) depends on a node named 'stg_customer' which was not found

$ dbt run
Running with dbt=1.7.1
Compilation Error in macro (macros/cents_to_dollars.sql)
  Reached EOF without finding a close tag for macro (searched from line 1)

$ dbt run
Running with dbt=1.7.1

Encountered an error:
Compilation Error
  Error reading jaffle_shop: schema.yml - Runtime Error
    Syntax error near line 5
    ------------------------------
    2  |
    3  | models:
    4  | - name: customers
    5  |     columns:
    6  |       - name: customer_id
    7  |         data_tests:
    8  |           - unique

Raw Error:
    ------------------------------
    mapping values are not allowed in this context
      in "<unicode string>", line 5, column 12

models:
  - name: customers
      columns: # this is indented too far!
      - name: customer_id
        data_tests:
          - unique
          - not_null

$ dbt run
Running with dbt=1.7.1

Encountered an error:
Compilation Error
  Invalid models config given in models/schema.yml @ models: {'name': 'customers', 'hello': 'world', 'columns': [{'name': 'customer_id', 'tests': ['unique', 'not_null']}], 'original_file_path': 'models/schema.yml', 'yaml_key': 'models', 'package_name': 'jaffle_shop'} - at path []: Additional properties are not allowed ('hello' was unexpected)

$ dbt run
Running with dbt=1.7.1-rc

Encountered an error:
Found a cycle: model.jaffle_shop.customers --> model.jaffle_shop.stg_customers --> model.jaffle_shop.customers

$ dbt run
...
Completed with 1 error and 0 warnings:

Database Error in model customers (models/customers.sql)
  001003 (42000): SQL compilation error:
  syntax error line 14 at position 4 unexpected 'from'.
  compiled SQL at target/run/jaffle_shop/models/customers.sql

target/
  dbt_packages/
  logs/
  # legacy -- renamed to dbt_packages in dbt v1
  dbt_modules/
  
  Running with dbt=xxx
  Runtime Error
    Failed to read package: Runtime Error
      Invalid config version: 1, expected 2  
    Error encountered in dbt_utils/dbt_project.yml
  
  packages:
  - package: dbt-labs/dbt_utils

version: xxx
  
  Compilation Error
    In dispatch: Could not find package 'my_project'
  
  $ dbt run --select customers
  Running with dbt=1.9.0
  Found 3 models, 9 tests, 0 snapshots, 0 analyses, 133 macros, 0 operations, 0 seed files, 0 sources

14:04:12 | Concurrency: 1 threads (target='dev')
  14:04:12 |
  14:04:12 | 1 of 1 START view model dbt_alice.customers.......................... [RUN]
  14:04:13 | 1 of 1 ERROR creating view model dbt_alice.customers................. [ERROR in 0.81s]
  14:04:13 |
  14:04:13 | Finished running 1 view model in 1.68s.

Completed with 1 error and 0 warnings:

Database Error in model customers (models/customers.sql)
    Syntax error: Expected ")" but got identifier `your-info-12345` at [13:15]
    compiled SQL at target/run/jaffle_shop/customers.sql

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1
  
{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

{{ default_schema }}_{{ custom_schema_name | trim }}

{% macro generate_schema_name(custom_schema_name, node) -%}
    {{ generate_schema_name_for_env(custom_schema_name, node) }}
{%- endmacro %}

{% macro generate_schema_name_for_env(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if target.name == 'prod' and custom_schema_name is not none -%}

{{ custom_schema_name | trim }}

data_tests:
dbt_project_evaluator:
    +severity: "{{ env_var('DBT_PROJECT_EVALUATOR_SEVERITY', 'warn') }}"

dbt build --select state:modified+ --exclude package:dbt_project_evaluator
dbt build --select package:dbt_project_evaluator

my_awesome_project
├── .github
│   ├── workflows
│   │   └── lint_on_push.yml

name: lint dbt project on push

on:
  push:
    branches-ignore:
      - 'main'

jobs:
  # this job runs SQLFluff with a specific set of rules
  # note the dialect is set to Snowflake, so make that specific to your setup
  # details on linter rules: https://docs.sqlfluff.com/en/stable/rules.html
  lint_project:
    name: Run SQLFluff linter
    runs-on: ubuntu-latest
  
    steps:
      - uses: "actions/checkout@v3"
      - uses: "actions/setup-python@v4"
        with:
          python-version: "3.9"
      - name: Install SQLFluff
        run: "python -m pip install sqlfluff"
      - name: Lint project
        run: "sqlfluff lint models --dialect snowflake"

my_awesome_project
├── dbt_project.yml
├── .gitlab-ci.yml

stages:
  - pre-build

**Examples:**

Example 1 (unknown):
```unknown
For this new job, open the existing Azure pipeline you created above and select the *Edit* button. We'll want to edit the corresponding Azure pipeline YAML file with the appropriate configuration, instead of the starter code, along with including a `variables` section to pass in the required variables.

Copy the below YAML file into your Azure pipeline and update the variables below to match your setup based on the comments in the file. It's worth noting that we changed the `trigger` section so that it will run **only** when there are pushes to a branch named `main` (like a PR merged to your main branch).

Read through [Azure's docs](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops) on these filters for additional use cases.
```

Example 2 (unknown):
```unknown
For this job, we'll set it up using the `bitbucket-pipelines.yml` file as in the prior step (see Step 1 of the linting setup for more info). The YAML file will look pretty similar to our earlier job, but we’ll pass in the required variables to the Python script using `export` statements. Update this section to match your setup based on the comments in the file.

* Only job
* Lint and dbt job
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
##### 5. Test your new action[​](#5-test-your-new-action "Direct link to 5. Test your new action")

Now that you have a shiny new action, it’s time to test it out! Since this change is setup to only run on merges to your default branch, you’ll need to create and merge this change into your main branch. Once you do that, you’ll see a new pipeline job has been triggered to run the dbt job you assigned in the variables section.

Additionally, you’ll see the job in the run history of dbt. It should be fairly easy to spot because it will say it was triggered by the API, and the *INFO* section will have the branch you used for this guide.

* GitHub
* GitLab
* Azure DevOps
* Bitbucket

[![dbt run on merge job in GitHub](/img/guides/orchestration/custom-cicd-pipelines/dbt-run-on-merge-github.png?v=2 "dbt run on merge job in GitHub")](#)dbt run on merge job in GitHub

[![dbt job showing it was triggered by GitHub](/img/guides/orchestration/custom-cicd-pipelines/dbt-cloud-job-github-triggered.png?v=2 "dbt job showing it was triggered by GitHub")](#)dbt job showing it was triggered by GitHub

[![dbt run on merge job in GitLab](/img/guides/orchestration/custom-cicd-pipelines/dbt-run-on-merge-gitlab.png?v=2 "dbt run on merge job in GitLab")](#)dbt run on merge job in GitLab

[![dbt job showing it was triggered by GitLab](/img/guides/orchestration/custom-cicd-pipelines/dbt-cloud-job-gitlab-triggered.png?v=2 "dbt job showing it was triggered by GitLab")](#)dbt job showing it was triggered by GitLab

[![dbt run on merge job in ADO](/img/guides/orchestration/custom-cicd-pipelines/dbt-run-on-merge-azure.png?v=2 "dbt run on merge job in ADO")](#)dbt run on merge job in ADO

[![ADO-triggered job in dbt](/img/guides/orchestration/custom-cicd-pipelines/dbt-cloud-job-azure-triggered.png?v=2 "ADO-triggered job in dbt")](#)ADO-triggered job in dbt

[![dbt run on merge job in Bitbucket](/img/guides/orchestration/custom-cicd-pipelines/dbt-run-on-merge-bitbucket.png?v=2 "dbt run on merge job in Bitbucket")](#)dbt run on merge job in Bitbucket

[![dbt job showing it was triggered by Bitbucket](/img/guides/orchestration/custom-cicd-pipelines/dbt-cloud-job-bitbucket-triggered.png?v=2 "dbt job showing it was triggered by Bitbucket")](#)dbt job showing it was triggered by Bitbucket

#### Run a dbt job on pull request[​](#run-a-dbt-job-on-pull-request "Direct link to Run a dbt job on pull request")

If your git provider is not one with a native integration with dbt, but you still want to take advantage of CI builds, you've come to the right spot! With just a bit of work it's possible to setup a job that will run a dbt job when a pull request (PR) is created.

Run on PR

If your git provider has a native integration with dbt, you can take advantage of the setup instructions [here](https://docs.getdbt.com/docs/deploy/ci-jobs.md). This section is only for those projects that connect to their git repository using an SSH key.

The setup for this pipeline will use the same steps as the prior page. Before moving on, follow steps 1-5 from the [prior page](https://docs.getdbt.com/guides/custom-cicd-pipelines.md?step=2).

##### 1. Create a pipeline job that runs when PRs are created[​](#1-create-a-pipeline-job-that-runs-when-prs-are-created "Direct link to 1. Create a pipeline job that runs when PRs are created")

* Bitbucket

For this job, we'll set it up using the `bitbucket-pipelines.yml` file as in the prior step. The YAML file will look pretty similar to our earlier job, but we’ll pass in the required variables to the Python script using `export` statements. Update this section to match your setup based on the comments in the file.

**What is this pipeline going to do?**<br /><!-- -->The setup below will trigger a dbt job to run every time a PR is opened in this repository. It will also run a fresh version of the pipeline for every commit that is made on the PR until it is merged. For example: If you open a PR, it will run the pipeline. If you then decide additional changes are needed, and commit/push to the PR branch, a new pipeline will run with the updated code.

The following variables control this job:

* `DBT_JOB_BRANCH`: Tells the dbt job to run the code in the branch that created this PR
* `DBT_JOB_SCHEMA_OVERRIDE`: Tells the dbt job to run this into a custom target schema
  <!-- -->
  * The format of this will look like: `DBT_CLOUD_PR_{REPO_KEY}_{PR_NUMBER}`
```

---

## docs

**URL:** llms-txt#docs

**Contents:**
  - About env_var function

- go
- here
 
{% enddocs %}

models:
  - name: orders
    description: "{{ doc('orders') }}"

profile:
  target: prod
  outputs:
    prod:
      type: postgres
      host: 127.0.0.1
      # IMPORTANT: Make sure to quote the entire Jinja string here
      user: "{{ env_var('DBT_USER') }}"
      password: "{{ env_var('DBT_PASSWORD') }}"
      ....

...
models:
  jaffle_shop:
    +materialized: "{{ env_var('DBT_MATERIALIZATION', 'view') }}"

**Examples:**

Example 1 (unknown):
```unknown
schema.yml
```

Example 2 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About env_var function

The `env_var` function can be used to incorporate environment variables from the system into your dbt project. You can use the `env_var` function in your `profiles.yml` file, the `dbt_project.yml` file, the `sources.yml` file, your `schema.yml` files, and in model `.sql` files. Essentially, `env_var` is available anywhere dbt processes Jinja code.

When used in a `profiles.yml` file (to avoid putting credentials on a server), it can be used like this:

profiles.yml
```

Example 3 (unknown):
```unknown
If the `DBT_USER` and `DBT_ENV_SECRET_PASSWORD` environment variables are present when dbt is invoked, then these variables will be pulled into the profile as expected. If any environment variables are not set, then dbt will raise a compilation error.

Integer Environment Variables

If passing an environment variable for a property that uses an integer type (for example, `port`, `threads`), be sure to add a filter to the Jinja expression, as shown here. Otherwise, dbt will raise an `['threads']: '1' is not of type 'integer'` error. `{{ env_var('DBT_THREADS') | int }}` or `{{ env_var('DB_PORT') | as_number }}`

Quoting, Curly Brackets, & You

Be sure to quote the entire Jinja string (as shown above), or else the YAML parser will be confused by the Jinja curly brackets.

`env_var` accepts a second, optional argument for default value, like so:

dbt\_project.yml
```

Example 4 (unknown):
```unknown
This can be useful to avoid compilation errors when the environment variable isn't available.

##### Secrets[​](#secrets "Direct link to Secrets")

For certain configurations, you can use "secret" env vars. Any env var named with the prefix `DBT_ENV_SECRET` will be:

* Available for use in `profiles.yml` + `packages.yml`, via the same `env_var()` function
* Disallowed everywhere else, including `dbt_project.yml` and model SQL, to prevent accidentally writing these secret values to the data warehouse or metadata artifacts
* Scrubbed from dbt logs and replaced with `*****`, any time its value appears in those logs (even if the env var was not called directly)

The primary use case of secret env vars is git access tokens for [private packages](https://docs.getdbt.com/docs/build/packages.md#private-packages).

**Note:** When dbt is loading profile credentials and package configuration, secret env vars will be replaced with the string value of the environment variable. You cannot modify secrets using Jinja filters, including type-casting filters such as [`as_number`](https://docs.getdbt.com/reference/dbt-jinja-functions/as_number.md) or [`as_bool`](https://docs.getdbt.com/reference/dbt-jinja-functions/as_bool.md), or pass them as arguments into other Jinja macros. You can only use *one secret* per configuration:
```

---

## required

**URL:** llms-txt#required

**Contents:**
  - Customize dbt models database, schema, and alias
  - Customizing CI/CD with custom pipelines

config.require('required_config_name')

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

{%- elif  env_var('DBT_ENV_TYPE','DEV') == 'PROD' -%}
        
        {{ custom_schema_name | trim }}

{{ default_schema }}_{{ custom_schema_name | trim }}

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

{%- elif  env_var('DBT_ENV_TYPE','DEV') != 'CI' -%}
        
        {{ custom_schema_name | trim }}

{{ default_schema }}_{{ custom_schema_name | trim }}

{% macro generate_alias_name(custom_alias_name=none, node=none) -%}

{%- if  env_var('DBT_ENV_TYPE','DEV') == 'DEV' -%}

{%- if custom_alias_name -%}

{{ target.schema }}__{{ custom_alias_name | trim }}

{%- elif node.version -%}

{{ target.schema }}__{{ node.name ~ "_v" ~ (node.version | replace(".", "_")) }}

{{ target.schema }}__{{ node.name }}

{%- endif -%}
    
    {%- else -%}

{%- if custom_alias_name -%}

{{ custom_alias_name | trim }}

{%- elif node.version -%}

{{ return(node.name ~ "_v" ~ (node.version | replace(".", "_"))) }}

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if  env_var('DBT_ENV_TYPE','DEV') == 'DEV' -%}
    
        {#- we replace characters not allowed in the schema names by "_" -#}
        {%- set re = modules.re -%}
        {%- set cleaned_branch = re.sub("\W", "_", env_var('DBT_CLOUD_GIT_BRANCH')) -%}
        
        {%- if custom_schema_name is none -%}

{{ cleaned_branch }}_{{ custom_schema_name | trim }}

{%- endif -%}
        
    {%- else -%}

{{ default_schema }}_{{ custom_schema_name | trim }}

{% macro generate_schema_name(custom_schema_name=none, node=none) -%}

{%- set default_schema = target.schema -%}
    
    {# If the CI Job does not exist in its own environment, use the target.name variable inside the job instead #}
    {# {%- if target.name == 'CI' -%} #} 
    
    {%- if env_var('DBT_ENV_TYPE','DEV') == 'CI' -%}
        
        ci_schema
        
    {%- elif custom_schema_name is none -%}
        
        {{ default_schema }}
    
    {%- else -%}
        
        {{ default_schema }}_{{ custom_schema_name | trim }}
    
    {%- endif -%}

{% macro generate_alias_name(custom_alias_name=none, node=none) -%}

{# If the CI Job does not exist in its own environment, use the target.name variable inside the job instead #}
    {# {%- if target.name == 'CI' -%} #}   
    {%- if  env_var('DBT_ENV_TYPE','DEV') == 'CI' -%}

{%- if custom_alias_name -%}

{{ target.schema }}__{{ node.config.schema }}__{{ custom_alias_name | trim }}

{%- elif node.version -%}

{{ target.schema }}__{{ node.config.schema }}__{{ node.name ~ "_v" ~ (node.version | replace(".", "_")) }}

{{ target.schema }}__{{ node.config.schema }}__{{ node.name }}

{%- endif -%}
    
    {%- else -%}

{%- if custom_alias_name -%}

{{ custom_alias_name | trim }}

{%- elif node.version -%}

{{ return(node.name ~ "_v" ~ (node.version | replace(".", "_"))) }}

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

{%- else -%}
    # The following is incorrect as it omits {{ default_schema }} before {{ custom_schema_name | trim }}. 
        {{ custom_schema_name | trim }}

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none and node.resource_type == 'model' -%}
        
        {{ exceptions.raise_compiler_error("Error: No Custom Schema Defined for the model " ~ node.name ) }}
    
    {%- endif -%}

my_awesome_project
├── python
│   └── run_and_monitor_dbt_job.py

#------------------------------------------------------------------------------

**Examples:**

Example 1 (unknown):
```unknown
For more information on the `config` dbt Jinja function, see the [config](https://docs.getdbt.com/reference/dbt-jinja-functions/config.md) reference.

#### Materialization precedence[​](#materialization-precedence "Direct link to Materialization precedence")

dbt will pick the materialization macro in the following order (lower takes priority):

1. global project - default
2. global project - plugin specific
3. imported package - default
4. imported package - plugin specific
5. local project - default
6. local project - plugin specific

In each of the stated search spaces, a materialization can only be defined once. Two different imported packages may not supply the same materialization - an error will be raised.

Specific materializations can be selected by using the dot-notation when selecting a materialization from the context.

We recommend *not* overriding materialization names directly, and instead using a prefix or suffix to denote that the materialization changes the behavior of the default implementation (eg. my\_project\_incremental).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Customize dbt models database, schema, and alias

[Back to guides](https://docs.getdbt.com/guides.md)

Advanced

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

This guide explains how to customize the [schema](https://docs.getdbt.com/docs/build/custom-schemas.md), [database](https://docs.getdbt.com/docs/build/custom-databases.md), and [alias](https://docs.getdbt.com/docs/build/custom-aliases.md) naming conventions in dbt to fit your data warehouse governance and design needs. When we develop dbt models and execute certain [commands](https://docs.getdbt.com/reference/dbt-commands.md) (such as `dbt run` or `dbt build`), objects (like tables and views) get created in the data warehouse based on these naming conventions.

A word on naming

Different warehouses have different names for *logical databases*. The information in this document covers "databases" on Snowflake, Redshift, and Postgres; "projects" on BigQuery; and "catalogs" on Databricks Unity Catalog.

The following is dbt's out-of-the-box default behavior:

* The database where the object is created is defined by the database configured at the [environment level in dbt](https://docs.getdbt.com/docs/dbt-cloud-environments.md) or in the [`profiles.yml` file](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml.md) in dbt Core.

* The schema depends on whether you have defined a [custom schema](https://docs.getdbt.com/docs/build/custom-schemas.md) for the model:

  * If you haven't defined a custom schema, dbt creates the object in the default schema. In dbt, this is typically `dbt_username` for development and the default schema for deployment environments. In dbt Core, it uses the schema specified in the `profiles.yml` file.
  * If you define a custom schema, dbt concatenates the schema mentioned earlier with the custom one.
  * For example, if the configured schema is `dbt_myschema` and the custom one is `marketing`, the objects will be created under `dbt_myschema_marketing`.
  * Note that for automated CI jobs, the schema name derives from the job number and PR number: `dbt_cloud_pr_<job_id>_<pr_id>`.

* The object name depends on whether an [alias](https://docs.getdbt.com/reference/resource-configs/alias.md) has been defined on the model:

  * If no alias is defined, the object will be created with the same name as the model, without the `.sql` or `.py` at the end.
    <!-- -->
    * For example, suppose that we have a model where the SQL file is titled `fct_orders_complete.sql`, the custom schema is `marketing`, and no custom alias is configured. The resulting model will be created in `dbt_myschema_marketing.fct_orders_complete` in the dev environment.
  * If an alias is defined, the object will be created with the configured alias.
  * For example, suppose that we have a model where the SQL file is titled `fct_orders_complete.sql`, the custom schema is `marketing`, and the alias is configured to be `fct_orders`. The resulting model will be created in `dbt_myschema_marketing.fct_orders`

These default rules are a great starting point, and many organizations choose to stick with those without any customization required.

The defaults allow developers to work in their isolated schemas (sandboxes) without overwriting each other's work — even if they're working on the same tables.

#### How to customize this behavior[​](#how-to-customize-this-behavior "Direct link to How to customize this behavior")

While the default behavior will fit the needs of most organizations, there are occasions where this approach won't work.

For example, dbt expects that it has permission to create schemas as needed (and we recommend that the users running dbt have this ability), but it might not be allowed at your company.

Or, based on how you've designed your warehouse, you may wish to minimize the number of schemas in your dev environment (and avoid schema sprawl by not creating the combination of all developer schemas and custom schemas).

Alternatively, you may even want your dev schemas to be named after feature branches instead of the developer name.

For this reason, dbt offers three macros to customize what objects are created in the data warehouse:

* [`generate_database_name()`](https://docs.getdbt.com/docs/build/custom-databases.md#generate_database_name)
* [`generate_schema_name()`](https://docs.getdbt.com/docs/build/custom-schemas.md#how-does-dbt-generate-a-models-schema-name)
* [`generate_alias_name()`](https://docs.getdbt.com/docs/build/custom-aliases.md#generate_alias_name)

By overwriting one or multiple of those macros, we can tailor where dbt objects are created in the data warehouse and align with any existing requirement.

Key concept

Models run from two different contexts must result in unique objects in the data warehouse. For example, a developer named Suzie is working on enhancements to `fct_player_stats`, but Darren is developing against the exact same object.

In order to prevent overwriting each other's work, both Suzie and Darren should each have their unique versions of `fct_player_stats` in the development environment.

Further, the staging version of `fct_player_stats` should exist in a unique location apart from the development versions, and the production version.

We often leverage the following when customizing these macros:

* In dbt, we recommend utilizing [environment variables](https://docs.getdbt.com/docs/build/environment-variables.md) to define where the dbt invocation is occurring (dev/stg/prod).
  <!-- -->
  * They can be set at the environment level and all jobs will automatically inherit the default values. We'll add Jinja logic (`if/else/endif`) to identify whether the run happens in dev, prod, Ci, and more.
* Or as an alternative to environment variables, you can use `target.name`. For more information, you can refer to [About target variables](https://docs.getdbt.com/reference/dbt-jinja-functions/target.md).

[![Custom schema environmental variables target name.](</img/docs/dbt-cloud/using-dbt-cloud/Environment Variables/custom-schema-env-var.png?v=2> "Custom schema environmental variables target name.")](#)Custom schema environmental variables target name.

To allow the database/schema/object name to depend on the current branch, you can use the out-of-the-box `DBT_CLOUD_GIT_BRANCH` environment variable in dbt [special environment variables](https://docs.getdbt.com/docs/build/environment-variables.md#special-environment-variables).

#### Example use cases[​](#example-use-cases "Direct link to Example use cases")

Here are some typical examples we've encountered with dbt users leveraging those 3 macros and different logic.

note

Note that the following examples are not comprehensive and do not cover all the available options. These examples are meant to be templates for you to develop your own behaviors.

* [Use custom schema without concatenating target schema in production](https://docs.getdbt.com/guides/customize-schema-alias.md?step=3#1-custom-schemas-without-target-schema-concatenation-in-production)
* [Add developer identities to tables](https://docs.getdbt.com/guides/customize-schema-alias.md?step=3#2-static-schemas-add-developer-identities-to-tables)
* [Use branch name as schema prefix](https://docs.getdbt.com/guides/customize-schema-alias.md?step=3#3-use-branch-name-as-schema-prefix)
* [Use a static schema for CI](https://docs.getdbt.com/guides/customize-schema-alias.md?step=3#4-use-a-static-schema-for-ci)

##### 1. Custom schemas without target schema concatenation in production[​](#1-custom-schemas-without-target-schema-concatenation-in-production "Direct link to 1. Custom schemas without target schema concatenation in production")

The most common use case is using the custom schema without concatenating it with the default schema name when in production.

To do so, you can create a new file called `generate_schema_name.sql` under your macros folder with the following code:

macros/generate\_schema\_name.sql
```

Example 2 (unknown):
```unknown
This will generate the following outputs for a model called `my_model` with a custom schema of `marketing`, preventing any overlap of objects between dbt runs from different contexts.

| Context     | Target database | Target schema | Resulting object                     |
| ----------- | --------------- | ------------- | ------------------------------------ |
| Developer 1 | dev             | dbt\_dev1     | dev.dbt\_dev1\_marketing.my\_model   |
| Developer 2 | dev             | dbt\_dev2     | dev.dbt\_dev2\_marketing.my\_model   |
| CI PR 123   | ci              | dbt\_pr\_123  | ci.dbt\_pr\_123\_marketing.my\_model |
| CI PR 234   | ci              | dbt\_pr\_234  | ci.dbt\_pr\_234\_marketing.my\_model |
| Production  | prod            | analytics     | prod.marketing.my\_model             |

note

We added logic to check if the current dbt run is happening in production or not. This is important, and we explain why in the [What not to do](https://docs.getdbt.com/guides/customize-schema-alias.md?step=3#what-not-to-do) section.

##### 2. Static schemas: Add developer identities to tables[​](#2-static-schemas-add-developer-identities-to-tables "Direct link to 2. Static schemas: Add developer identities to tables")

Occasionally, we run into instances where the security posture of the organization prevents developers from creating schemas and all developers have to develop in a single schema.

In this case, we can:

* Create a new file called generate\_schema\_name.sql under your macros folder with the following code:

* Change `generate_schema_name()` to use a single schema for all developers, even if a custom schema is set.

* Update `generate_alias_name()` to append the developer alias and the custom schema to the front of the table name in the dev environment.

  * This method is not ideal, as it can cause long table names, but it will let developers see in which schema the model will be created in production.

macros/generate\_schema\_name.sql
```

Example 3 (unknown):
```unknown
macros/generate\_alias\_name.sql
```

Example 4 (unknown):
```unknown
This will generate the following outputs for a model called `my_model` with a custom schema of `marketing`, preventing any overlap of objects between dbt runs from different contexts.

| Context     | Target database | Target schema | Resulting object                     |
| ----------- | --------------- | ------------- | ------------------------------------ |
| Developer 1 | dev             | dbt\_dev1     | dev.marketing.dbt\_dev1\_my\_model   |
| Developer 2 | dev             | dbt\_dev2     | dev.marketing.dbt\_dev2\_my\_model   |
| CI PR 123   | ci              | dbt\_pr\_123  | ci.dbt\_pr\_123\_marketing.my\_model |
| CI PR 234   | ci              | dbt\_pr\_234  | ci.dbt\_pr\_234\_marketing.my\_model |
| Production  | prod            | analytics     | prod.marketing.my\_model             |

##### 3. Use branch name as schema prefix[​](#3-use-branch-name-as-schema-prefix "Direct link to 3. Use branch name as schema prefix")

For teams who prefer to isolate work based on the feature branch, you may want to take advantage of the `DBT_CLOUD_GIT_BRANCH` special environment variable. Please note that developers will write to the exact same schema when they are on the same feature branch.

note

The `DBT_CLOUD_GIT_BRANCH` variable is only available within the Studio IDE and not the Cloud CLI.

We’ve also seen some organizations prefer to organize their dev databases by branch name. This requires implementing similar logic in `generate_database_name()` instead of the `generate_schema_name()` macro. By default, dbt will not automatically create the databases.

Refer to the [Tips and tricks](https://docs.getdbt.com/guides/customize-schema-alias.md?step=5) section to learn more.

macros/generate\_schema\_name.sql
```

---

## In this example we set up a secret scope and key called "dbt-cloud" and "api-key" respectively.

**URL:** llms-txt#in-this-example-we-set-up-a-secret-scope-and-key-called-"dbt-cloud"-and-"api-key"-respectively.

databricks secrets create-scope --scope <YOUR_SECRET_SCOPE>
databricks secrets put --scope  <YOUR_SECRET_SCOPE> --key  <YOUR_SECRET_KEY> --string-value "<YOUR_DBT_CLOUD_API_KEY>"

import enum
import os
import time
import json
import requests
from getpass import getpass
     
dbutils.widgets.text("job_id", "Enter the Job ID")
job_id = dbutils.widgets.get("job_id")

account_id = <YOUR_ACCOUNT_ID>
base_url =  "<YOUR_BASE_URL>"
api_key =  dbutils.secrets.get(scope = "<YOUR_SECRET_SCOPE>", key = "<YOUR_SECRET_KEY>")

**Examples:**

Example 1 (unknown):
```unknown
4. Replace **`<YOUR_SECRET_SCOPE>`** and **`<YOUR_SECRET_KEY>`** with your own unique identifiers. Click [here](https://docs.databricks.com/security/secrets/index.html) for more information on secrets.

5. Replace **`<YOUR_DBT_CLOUD_API_KEY>`** with the actual API key value that you copied from dbt in step 1.

#### Create a Databricks Python notebook[​](#create-a-databricks-python-notebook "Direct link to Create a Databricks Python notebook")

1. [Create a **Databricks Python notebook**](https://docs.databricks.com/notebooks/notebooks-manage.html), which executes a Python script that calls the dbt job API.

2. Write a **Python script** that utilizes the `requests` library to make an HTTP POST request to the dbt job API endpoint using the required parameters. Here's an example script:
```

---

## this job runs SQLFluff with a specific set of rules

**URL:** llms-txt#this-job-runs-sqlfluff-with-a-specific-set-of-rules

---

## Define variables here

**URL:** llms-txt#define-variables-here

**Contents:**
  - About zip context method
  - access
  - Advanced configuration usage
  - alias
  - Amazon Athena configurations
  - Amazon Redshift adapter behavior changes
  - Analysis properties
  - analysis-paths
  - anchors
  - Anonymous usage stats

vars:
  event_type: activation

-- Use 'activation' as the event_type if the variable is not defined.
select * from events where event_type = '{{ var("event_type", "activation") }}'

{% set my_list_a = [1, 2] %}
{% set my_list_b = ['alice', 'bob'] %}
{% set my_zip = zip(my_list_a, my_list_b) | list %}
{% do log(my_zip) %}  {# [(1, 'alice'), (2, 'bob')] #}

{% set my_list_a = 12 %}
{% set my_list_b = ['alice', 'bob'] %}
{% set my_zip = zip(my_list_a, my_list_b, default = []) | list %}
{% do log(my_zip) %}  {# [] #}

{% set my_list_a = [1, 2] %}
{% set my_list_b = ['alice', 'bob'] %}
{% set my_zip = zip_strict(my_list_a, my_list_b) | list %}
{% do log(my_zip) %}  {# [(1, 'alice'), (2, 'bob')] #}

{% set my_list_a = 12 %}
{% set my_list_b = ['alice', 'bob'] %}
{% set my_zip = zip_strict(my_list_a, my_list_b) %}

Compilation Error in ... (...)
  'int' object is not iterable

models:
  - name: model_name
    config:
      access: private | protected | public # changed to config in v1.10

models:
    - name: my_public_model
      config:
        access: public # Older method, still supported
          # changed to config in v1.10

models:
    - name: my_public_model
      config:
        access: public
      
  
  models:
    my_project_name:
      subfolder_name:
        +group: my_group
        +access: private  # sets default for all models in this subfolder
  
  -- models/my_public_model.sql

{{ config(access = "public") }}

select ...
  
dbt run -s marketing_model
...
dbt.exceptions.DbtReferenceError: Parsing Error
  Node model.jaffle_shop.marketing_model attempted to reference node model.jaffle_shop.finance_model, 
  which is not allowed because the referenced node is private to the finance group.

{{ config(
    post-hook="grant select on {{ this }} to role reporter",
    materialized='table'
) }}

{{
  config({
    "post-hook": "grant select on {{ this }} to role reporter",
    "materialized": "table"
  })
}}

models:
  your_project:
    sales_total:
      +alias: sales_dashboard

models:
  - name: sales_total
    config:
      alias: sales_dashboard

{{ config(
    alias="sales_dashboard"
) }}

seeds:
  your_project:
    product_categories:
      +alias: categories_data

seeds:
  - name: product_categories
    config:
      alias: categories_data

seeds:
  jaffle_shop:
    country_codes:
      +alias: country_mappings

snapshots:
  your_project:
    your_snapshot:
      +alias: the_best_snapshot
`

snapshots:
  - name: your_snapshot_name
    config:
      alias: the_best_snapshot
</File>

In `snapshots/your_snapshot.sql` file:

<File name='snapshots/your_snapshot.sql'>

This would build your snapshot to `analytics.finance.the_best_snapshot` in the database.

Configure a data test's alias in your `dbt_project.yml` file, `properties.yml` file, or config block in the model file.

The following examples demonstrate how to `alias` a unique data test named `order_id` to `unique_order_id_test` to identify a specific data test.

In the `dbt_project.yml` file at the project level:

In the `models/properties.yml` file:

models/properties.yml

In `tests/unique_order_id_test.sql` file:

tests/unique\_order\_id\_test.sql

When using [`store_failures_as`](https://docs.getdbt.com/reference/resource-configs/store_failures_as.md), this would return the name `analytics.dbt_test__audit.orders_order_id_unique_order_id_test` in the database.

#### Definition[​](#definition "Direct link to Definition")

Optionally specify a custom alias for a [model](https://docs.getdbt.com/docs/build/models.md), [data test](https://docs.getdbt.com/docs/build/data-tests.md), [snapshot](https://docs.getdbt.com/docs/build/snapshots.md), or [seed](https://docs.getdbt.com/docs/build/seeds.md).

When dbt creates a relation (table/view) in a database, it creates it as: `{{ database }}.{{ schema }}.{{ identifier }}`, e.g. `analytics.finance.payments`

The standard behavior of dbt is:

* If a custom alias is *not* specified, the identifier of the relation is the resource name (i.e. the filename).
* If a custom alias is specified, the identifier of the relation is the `{{ alias }}` value.

**Note** With an [ephemeral model](https://docs.getdbt.com/docs/build/materializations.md), dbt will always apply the prefix `__dbt__cte__` to the CTE identifier. This means that if an alias is set on an ephemeral model, then its CTE identifier will be `__dbt__cte__{{ alias }}`, but if no alias is set then its identifier will be `__dbt__cte__{{ filename }}`.

To learn more about changing the way that dbt generates a relation's `identifier`, read [Using Aliases](https://docs.getdbt.com/docs/build/custom-aliases.md).

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Amazon Athena configurations

#### Models[​](#models "Direct link to Models")

##### Table configuration[​](#table-configuration "Direct link to Table configuration")

| Parameter                 | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `external_location`       | None    | The full S3 path to where the table is saved. It only works with incremental models. It doesn't work with Hive tables with `ha` set to `true`.                                                                                                                                                                                                                                                             |
| `partitioned_by`          | None    | An array list of columns by which the table will be partitioned. Currently limited to 100 partitions.                                                                                                                                                                                                                                                                                                      |
| `bucketed_by`             | None    | An array list of the columns to bucket data. Ignored if using Iceberg.                                                                                                                                                                                                                                                                                                                                     |
| `bucket_count`            | None    | The number of buckets for bucketing your data. This parameter is ignored if using Iceberg.                                                                                                                                                                                                                                                                                                                 |
| `table_type`              | Hive    | The type of table. Supports `hive` or `iceberg`.                                                                                                                                                                                                                                                                                                                                                           |
| `ha`                      | False   | Build the table using the high-availability method. Only available for Hive tables.                                                                                                                                                                                                                                                                                                                        |
| `format`                  | Parquet | The data format for the table. Supports `ORC`, `PARQUET`, `AVRO`, `JSON`, and `TEXTFILE`.                                                                                                                                                                                                                                                                                                                  |
| `write_compression`       | None    | The compression type for any storage format that allows compressions.                                                                                                                                                                                                                                                                                                                                      |
| `field_delimeter`         | None    | Specify the custom field delimiter to use when the format is set to `TEXTFIRE`.                                                                                                                                                                                                                                                                                                                            |
| `table_properties`        | N/A     | The table properties to add to the table. This is only for Iceberg.                                                                                                                                                                                                                                                                                                                                        |
| `native_drop`             | N/A     | Relation drop operations will be performed with SQL, not direct Glue API calls. No S3 calls will be made to manage data in S3. Data in S3 will only be cleared up for Iceberg tables. See the [AWS docs](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-managing-tables.html) for more info. Iceberg DROP TABLE operations may timeout if they take longer than 60 seconds.                 |
| `seed_by_insert`          | False   | Creates seeds using an SQL insert statement. Large seed files can't exceed the Athena 262144 bytes limit.                                                                                                                                                                                                                                                                                                  |
| `force_batch`             | False   | Run the table creation directly in batch insert mode. Useful when the standard table creation fails due to partition limitation.                                                                                                                                                                                                                                                                           |
| `unique_tmp_table_suffix` | False   | Replace the "\_\_dbt\_tmp table" suffix with a unique UUID for incremental models using insert overwrite on Hive tables.                                                                                                                                                                                                                                                                                   |
| `temp_schema`             | None    | Defines a schema to hold temporary create statements used in incremental model runs. Scheme will be created in the models target database if it does not exist.                                                                                                                                                                                                                                            |
| `lf_tags_config`          | None    | [AWS Lake Formation](#aws-lake-formation-integration) tags to associate with the table and columns. Existing tags will be removed.<br />\* `enabled` (`default=False`) whether LF tags management is enabled for a model<br />\* `tags` dictionary with tags and their values to assign for the model<br />\* `tags_columns` dictionary with a tag key, value and list of columns they must be assigned to |
| `lf_inherited_tags`       | None    | List of the Lake Formation tag keys that are to be inherited from the database level and shouldn't be removed during the assignment of those defined in `ls_tags_config`.                                                                                                                                                                                                                                  |
| `lf_grants`               | None    | Lake Formation grants config for `data_cell` filters.                                                                                                                                                                                                                                                                                                                                                      |

###### Configuration examples[​](#configuration-examples "Direct link to Configuration examples")

* schema.yml
* dbt\_project.yml
* Lake formation grants

Consider these limitations and recommendations:

* `lf_tags` and `lf_tags_columns` configs support only attaching lf tags to corresponding resources.
* We recommend managing LF Tags permissions somewhere outside dbt. For example, [terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lakeformation_permissions) or [aws cdk](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_lakeformation-readme.html).
* `data_cell_filters` management can't be automated outside dbt because the filter can't be attached to the table, which doesn't exist. Once you `enable` this config, dbt will set all filters and their permissions during every dbt run. Such an approach keeps the actual state of row-level security configuration after every dbt run and applies changes if they occur: drop, create, and update filters and their permissions.
* Any tags listed in `lf_inherited_tags` should be strictly inherited from the database level and never overridden at the table and column level.
* Currently, `dbt-athena` does not differentiate between an inherited tag association and an override it made previously.
  <!-- -->
  * For example, If a `lf_tags_config` value overrides an inherited tag in one run, and that override is removed before a subsequent run, the prior override will linger and no longer be encoded anywhere (for example, Terraform where the inherited value is configured nor in the dbt project where the override previously existed but now is gone).

##### Table location[​](#table-location "Direct link to Table location")

The saved location of a table is determined in precedence by the following conditions:

1. If `external_location` is defined, that value is used.
2. If `s3_data_dir` is defined, the path is determined by that and `s3_data_naming`.
3. If `s3_data_dir` is not defined, data is stored under `{s3_staging_dir}/tables/`.

The following options are available for `s3_data_naming`:

* `unique`: `{s3_data_dir}/{uuid4()}/`
* `table`: `{s3_data_dir}/{table}/`
* `table_unique`: `{s3_data_dir}/{table}/{uuid4()}/`
* `schema_table`: `{s3_data_dir}/{schema}/{table}/`
* `schema_table_unique`: `{s3_data_dir}/{schema}/{table}/{uuid4()}/`

To set the `s3_data_naming` globally in the target profile, overwrite the value in the table config, or set up the value for groups of the models in dbt\_project.yml.

Note: If you're using a workgroup with a default output location configured, `s3_data_naming` ignores any configured buckets and uses the location configured in the workgroup.

##### Incremental models[​](#incremental-models "Direct link to Incremental models")

The following [incremental models](https://docs.getdbt.com/docs/build/incremental-models.md) strategies are supported:

* `insert_overwrite` (default): The insert-overwrite strategy deletes the overlapping partitions from the destination table and then inserts the new records from the source. This strategy depends on the `partitioned_by` keyword! dbt will fall back to the `append` strategy if no partitions are defined.
* `append`: Insert new records without updating, deleting or overwriting any existing data. There might be duplicate data (great for log or historical data).
* `merge`: Conditionally updates, deletes, or inserts rows into an Iceberg table. Used in combination with `unique_key`.It is only available when using Iceberg.

Consider this limitation when using Iceberg models:

* Incremental Iceberg models — Sync all columns on schema change. You can't remove columns used for partitioning with an incremental refresh; you must fully refresh the model.

##### On schema change[​](#on-schema-change "Direct link to On schema change")

The `on_schema_change` option reflects changes of the schema in incremental models. The values you can set this to are:

* `ignore` (default)
* `fail`
* `append_new_columns`
* `sync_all_columns`

To learn more, refer to [What if the columns of my incremental model change](https://docs.getdbt.com/docs/build/incremental-models.md#what-if-the-columns-of-my-incremental-model-change).

##### Iceberg[​](#iceberg "Direct link to Iceberg")

The adapter supports table materialization for Iceberg.

Iceberg supports bucketing as hidden partitions. Use the `partitioned_by` config to add specific bucketing conditions.

Iceberg supports the `PARQUET`, `AVRO` and `ORC` table formats for data .

The following are the supported strategies for using Iceberg incrementally:

* `append`: New records are appended to the table (this can lead to duplicates).

* `merge`: Perform an update and insert (and optional delete) where new and existing records are added. This is only available with Athena engine version 3.

* `unique_key`(required): Columns that define a unique source and target table record.
  * `incremental_predicates` (optional): The SQL conditions that enable custom join clauses in the merge statement. This helps improve performance via predicate pushdown on target tables.
  * `delete_condition` (optional): SQL condition that identifies records that should be deleted.
  * `update_condition` (optional): SQL condition that identifies records that should be updated.
  * `insert_condition` (optional): SQL condition that identifies records that should be inserted.

`incremental_predicates`, `delete_condition`, `update_condition` and `insert_condition` can include any column of the incremental table (`src`) or the final table (`target`). Column names must be prefixed by either `src` or `target` to prevent a `Column is ambiguous` error.

* delete\_condition
* update\_condition
* insert\_condition

##### High availability (HA) table[​](#high-availability-ha-table "Direct link to High availability (HA) table")

The current implementation of table materialization can lead to downtime, as the target table is dropped and re-created. For less destructive behavior, you can use the `ha` config on your `table` materialized models. It leverages the table versions feature of the glue catalog, which creates a temporary table and swaps the target table to the location of the temporary table. This materialization is only available for `table_type=hive` and requires using unique locations. For Iceberg, high availability is the default.

By default, the materialization keeps the last 4 table versions,but you can change it by setting `versions_to_keep`.

##### HA known issues[​](#ha-known-issues "Direct link to HA known issues")

* There could be a little downtime when swapping from a table with partitions to a table without (and the other way around). If higher performance is needed, consider bucketing instead of partitions.
* By default, Glue "duplicates" the versions internally, so the last two versions of a table point to the same location.
* It's recommended to set `versions_to_keep` >= 4, as this will avoid having the older location removed.

##### Avoid deleting parquet files[​](#avoid-deleting-parquet-files "Direct link to Avoid deleting parquet files")

If a dbt model has the same name as an existing table in the AWS Glue catalog, the `dbt-athena` adapter deletes the files in that table’s S3 location before recreating the table using the SQL from the model.

The adapter may also delete data if a model is configured to use the same S3 location as an existing table. In this case, it clears the folder before creating the new table to avoid conflicts during setup.

When dropping a model, the `dbt-athena` adapter performs two cleanup steps for both Iceberg and Hive tables:

* It deletes the table from the AWS Glue catalog using Glue APIs.
* It removes the associated S3 data files using a delete operation.

However, for Iceberg tables, using standard SQL like [`DROP TABLE`](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-drop-table.html) may not remove all related S3 objects. To ensure proper cleanup in a dbt workflow, the adapter includes a workaround that explicitly deletes these S3 objects. Alternatively, users can enable [`native_drop`](https://docs.getdbt.com/reference/resource-configs/athena-configs.md#table-configuration) to let Iceberg handle the cleanup natively.

##### Update glue data catalog[​](#update-glue-data-catalog "Direct link to Update glue data catalog")

You can persist your column and model level descriptions to the Glue Data Catalog as [glue table properties](https://docs.aws.amazon.com/glue/latest/dg/tables-described.html#table-properties) and [column parameters](https://docs.aws.amazon.com/glue/latest/webapi/API_Column.html). To enable this, set the configuration to `true` as shown in the following example. By default, documentation persistence is disabled, but it can be enabled for specific resources or groups of resources as needed.

Refer to [persist\_docs](https://docs.getdbt.com/reference/resource-configs/persist_docs.md) for more details.

#### Snapshots[​](#snapshots "Direct link to Snapshots")

The adapter supports snapshot materialization. It supports both the timestamp and check strategies. To create a snapshot, create a snapshot file in the `snapshots` directory. You'll need to create this directory if it doesn't already exist.

##### Timestamp strategy[​](#timestamp-strategy "Direct link to Timestamp strategy")

Refer to [Timestamp strategy](https://docs.getdbt.com/docs/build/snapshots.md#timestamp-strategy-recommended) for details on how to use it.

##### Check strategy[​](#check-strategy "Direct link to Check strategy")

Refer to [Check strategy](https://docs.getdbt.com/docs/build/snapshots.md#check-strategy) for details on how to use it.

##### Hard deletes[​](#hard-deletes "Direct link to Hard deletes")

The materialization also supports invalidating hard deletes. For usage details, refer to [Hard deletes](https://docs.getdbt.com/docs/build/snapshots.md#hard-deletes-opt-in).

##### Snapshots known issues[​](#snapshots-known-issues "Direct link to Snapshots known issues")

* Tables, schemas, and database names should only be lowercase.
* To avoid potential conflicts, make sure [`dbt-athena-adapter`](https://github.com/Tomme/dbt-athena) is not installed in the target environment.
* Snapshot does not support dropping columns from the source table. If you drop a column, make sure to drop the column from the snapshot as well. Another workaround is to NULL the column in the snapshot definition to preserve the history.

#### AWS Lake Formation integration[​](#aws-lake-formation-integration "Direct link to AWS Lake Formation integration")

The following describes how the adapter implements the AWS Lake Formation tag management:

* [Enable](#table-configuration) LF tags management with the `lf_tags_config` parameter. By default, it's disabled.
* Once enabled, LF tags are updated on every dbt run.
* First, all lf-tags for columns are removed to avoid inheritance issues.
* Then, all redundant lf-tags are removed from tables and actual tags from table configs are applied.
* Finally, lf-tags for columns are applied.

It's important to understand the following points:

* dbt doesn't manage `lf-tags` for databases
* dbt doesn't manage Lake Formation permissions

That's why it's important to take care of this yourself or use an automation tool such as terraform and AWS CDK. For more details, refer to:

* [terraform aws\_lakeformation\_permissions](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lakeformation_permissions)
* [terraform aws\_lakeformation\_resource\_lf\_tags](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lakeformation_resource_lf_tags)

#### Python models[​](#python-models "Direct link to Python models")

The adapter supports Python models using [`spark`](https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark.html).

##### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* A Spark-enabled workgroup created in Athena.
* Spark execution role granted access to Athena, Glue and S3.
* The Spark workgroup is added to the `~/.dbt/profiles.yml` file and the profile to be used is referenced in `dbt_project.yml`.

##### Spark-specific table configuration[​](#spark-specific-table-configuration "Direct link to Spark-specific table configuration")

| Configuration                 | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `timeout`                     | 43200   | Time out in seconds for each Python model execution. Defaults to 12 hours/43200 seconds.                                                                                                                                                                                                                                                                                                                                                                                          |
| `spark_encryption`            | False   | When set to `true,` it encrypts data stored locally by Spark and in transit between Spark nodes.                                                                                                                                                                                                                                                                                                                                                                                  |
| `spark_cross_account_catalog` | False   | When using the Spark Athena workgroup, queries can only be made against catalogs on the same AWS account by default. Setting this parameter to true will enable querying external catalogs if you want to query another catalog on an external AWS account.<br />Use the syntax `external_catalog_id/database.table` to access the external table on the external catalog (For example, `999999999999/mydatabase.cloudfront_logs` where 999999999999 is the external catalog ID). |
| `spark_requester_pays`        | False   | When set to true, if an Amazon S3 bucket is configured as `requester pays`, the user account running the query is charged for data access and data transfer fees associated with the query.                                                                                                                                                                                                                                                                                       |

##### Spark notes[​](#spark-notes "Direct link to Spark notes")

* A session is created for each unique engine configuration defined in the models that are part of the invocation. A session's idle timeout is set to 10 minutes. Within the timeout period, if a new calculation (Spark Python model) is ready for execution and the engine configuration matches, the process will reuse the same session.
* The number of Python models running simultaneously depends on the `threads`. The number of sessions created for the entire run depends on the number of unique engine configurations and the availability of sessions to maintain thread concurrency.
* For Iceberg tables, it's recommended to use the `table_properties` configuration to set the `format_version` to `2`. This helps maintain compatibility between the Iceberg tables Trino created and those Spark created.

##### Example models[​](#example-models "Direct link to Example models")

* Simple pandas
* Simple Spark
* Spark incremental
* Config Spark model
* PySpark UDF

Using imported external python files:

##### Known issues in Python models[​](#known-issues-in-python-models "Direct link to Known issues in Python models")

* Python models can't [reference Athena SQL views](https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark.html).
* You can use third-party Python libraries; however, they must be [included in the pre-installed list](https://docs.aws.amazon.com/athena/latest/ug/notebooks-spark-preinstalled-python-libraries.html) or [imported manually](https://docs.aws.amazon.com/athena/latest/ug/notebooks-import-files-libraries.html).
* Python models can only reference or write to tables with names matching the regular expression: `^[0-9a-zA-Z_]+$`. Spark doesn't support dashes or special characters, even though Athena supports them.
* Incremental models don't fully utilize Spark capabilities. They depend partially on existing SQL-based logic that runs on Trino.
* Snapshot materializations are not supported.
* Spark can only reference tables within the same catalog.
* For tables created outside of the dbt tool, be sure to populate the location field, or dbt will throw an error when creating the table.

#### Contracts[​](#contracts "Direct link to Contracts")

The adapter partly supports contract definitions:

* `data_type` is supported but needs to be adjusted for complex types. Types must be specified entirely (for example, `array<int>`) even though they won't be checked. Indeed, as dbt recommends, we only compare the broader type (array, map, int, varchar). The complete definition is used to check that the data types defined in Athena are ok (pre-flight check).
* The adapter does not support the constraints since Athena has no constraint concept.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Amazon Redshift adapter behavior changes

#### The `restrict_direct_pg_catalog_access` flag[​](#the-restrict_direct_pg_catalog_access-flag "Direct link to the-restrict_direct_pg_catalog_access-flag")

Originally, the `dbt-redshift` adapter was built on top of the `dbt-postgres` adapter and used Postgres tables for metadata access. When this flag is enabled, the adapter uses the Redshift API (through the Python client) if available, or queries Redshift's `information_schema` tables instead of using the `pg_` tables.

While you shouldn't notice any behavior changes due to this change, however, to be cautious dbt Labs is gating it behind a behavior-change flag and encouraging you to test it before it becoming the default.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Analysis properties

We recommend you define analysis properties in your `analyses/` directory, which is illustrated in the [`analysis-paths`](https://docs.getdbt.com/reference/project-configs/analysis-paths.md) configuration. Analysis properties<!-- --> are "special properties" in that you can't configure them in the `dbt_project.yml` file or using `config()` blocks. Refer to [Configs and properties](https://docs.getdbt.com/reference/define-properties#which-properties-are-not-also-configs) for more info.<br />

You can name these files `whatever_you_want.yml`, and nest them arbitrarily deeply in subfolders within the `analyses/` or `models/` directory.

analyses/\<filename>.yml

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

#### Definition[​](#definition "Direct link to Definition")

Specify a custom list of directories where [analyses](https://docs.getdbt.com/docs/build/analyses.md) are located.

#### Default[​](#default "Direct link to Default")

Without specifying this config, dbt will not compile any `.sql` files as analyses.

However, the [`dbt init` command](https://docs.getdbt.com/reference/commands/init.md) populates this value as `analyses` ([source](https://github.com/dbt-labs/dbt-starter-project/blob/HEAD/dbt_project.yml#L15)).

Paths specified in `analysis-paths` must be relative to the location of your `dbt_project.yml` file. Avoid using absolute paths like `/Users/username/project/analyses`, as it will lead to unexpected behavior and outcomes.

* Avoid absolute paths:

#### Examples[​](#examples "Direct link to Examples")

##### Use a subdirectory named `analyses`[​](#use-a-subdirectory-named-analyses "Direct link to use-a-subdirectory-named-analyses")

This is the value populated by the [`dbt init` command](https://docs.getdbt.com/reference/commands/init.md).

##### Use a subdirectory named `custom_analyses`[​](#use-a-subdirectory-named-custom_analyses "Direct link to use-a-subdirectory-named-custom_analyses")

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

#### Definition[​](#definition "Direct link to Definition")

Anchors are a [YAML feature](https://yaml.org/spec/1.2.2/#692-node-anchors) that let you reuse configuration blocks inside a single YAML file. In dbt Core v1.10, the `anchors:` key was introduced to enclose configuration fragments that aren't valid on their own or that only exist as template data. Using the `anchors:` key ensures these fragments won't be rejected during file validation.

In dbt Core v1.10 and higher, invalid anchors trigger a warning. In the dbt Fusion engine, these invalid anchors will result in errors when Fusion leaves beta.

You can define anchors in dbt Core v1.9 and earlier, but there is no dedicated location for anchors in these versions. If you need to define a standalone anchor, you can put it at the top level of your YAML file.

#### YAML anchor syntax[​](#yaml-anchor-syntax "Direct link to YAML anchor syntax")

##### Anchors and aliases[​](#anchors-and-aliases "Direct link to Anchors and aliases")

To define a YAML anchor, add an `anchors:` block in your YAML file and use the `&` symbol in front of the anchor's name (for example, `&id_column_alias`). This creates an alias which you can reference elsewhere by prefixing the alias with a `*` character.

The following example creates an anchor whose alias is `*id_column_alias`. The `id` column, its description, data type, and data tests are all applied to `my_first_model`, `my_second_model`, and `my_third_model`.

[![Behind the scenes, the alias is replaced with the object defined by the anchor.](/img/reference/resource-properties/anchor_example_expansion.png?v=2 "Behind the scenes, the alias is replaced with the object defined by the anchor.")](#)Behind the scenes, the alias is replaced with the object defined by the anchor.

##### Merge syntax[​](#merge-syntax "Direct link to Merge syntax")

Sometimes, an anchor is mostly the same but one part needs to be overridden. When the anchor refers to a dictionary/mapping (not a list or a scalar value), you can use the `<<:` merge syntax to override an already-defined key, or add extra keys to the dictionary. For example:

#### Usage notes[​](#usage-notes "Direct link to Usage notes")

* Old versions of dbt Core (v1.9 and earlier) do not have a dedicated `anchors:` key. If you need to define a standalone anchor, you can leave it at the top level of your file.

* You can't merge additional elements into a list which was defined as an anchor. For example, if you define an anchor containing multiple columns, you can't attach extra columns to the end of the list. Instead, define each column as an individual anchor and add each one to the relevant tables.

* You do not need to move existing anchors to the `anchors:` key if they are already defined in a larger valid YAML object. For example, the following `&customer_id_tests` anchor does not need to be moved because it is a valid part of the existing `columns` block.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Anonymous usage stats

dbt Labs is on a mission to build the best version of dbt possible, and a crucial part of that is understanding how users work with dbt. To this end, we've added some simple event tracking (or telemetry) to dbt using Snowplow. Importantly, we do not track credentials, raw model contents, or model names: we consider these private, and frankly none of our business.

The data we collect is used for use cases such as industry identification, use-case research, improvements of sales, marketing, product features, and services. Telemetry allows users to seamlessly contribute to the continuous improvement of dbt, enabling us to better serve the data community.

Usage statistics are fired when dbt is invoked and when models are run. These events contain basic platform information (OS + Python version) and metadata such as:

* Whether the invocation succeeded.
* How long it took.
* An anonymized hash key representing the raw model content.
* Number of nodes that were run.

For full transparency, you can see all the event definitions in [`tracking.py`](https://github.com/dbt-labs/dbt-core/blob/HEAD/core/dbt/tracking.py).

* dbt has telemetry enabled by default to help us enhance the user experience and improve the product by using real user feedback and usage patterns. While it cannot be disabled, we ensure the data is [secure](https://www.getdbt.com/security) and used responsibly. Collecting this data enables us to provide a better product experience, including improvements to the performance of dbt.

* dbt Core users have telemetry enabled by default to help us understand usage patterns and improve the product. You can opt out of event tracking at any time by adding the following to your `dbt_project.yml` file:

dbt Core users can also use the `DO_NOT_TRACK` environment variable to enable or disable sending anonymous data. For more information, see [Environment variables](https://docs.getdbt.com/docs/build/environment-variables.md).

`DO_NOT_TRACK=1` is the same as `DBT_SEND_ANONYMOUS_USAGE_STATS=False`

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Apache Spark configurations

If you're using Databricks, use `dbt-databricks`

If you're using Databricks, the `dbt-databricks` adapter is recommended over `dbt-spark`. If you're still using dbt-spark with Databricks consider [migrating from the dbt-spark adapter to the dbt-databricks adapter](https://docs.getdbt.com/guides/migrate-from-spark-to-databricks.md).

For the Databricks version of this page, refer to [Databricks setup](#databricks-setup).

See [Databricks configuration](#databricks-configs) for the Databricks version of this page.

#### Configuring tables[​](#configuring-tables "Direct link to Configuring tables")

When materializing a model as `table`, you may include several optional configs that are specific to the dbt-spark plugin, in addition to the standard [model configs](https://docs.getdbt.com/reference/model-configs.md).

| Option                                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Required?                               | Example                                                                                            |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| file\_format                           | The file format to use when creating tables (`parquet`, `delta`, `iceberg`, `hudi`, `csv`, `json`, `text`, `jdbc`, `orc`, `hive` or `libsvm`).                                                                                                                                                                                                                                                                                                                     | Optional                                | `parquet`                                                                                          |
| location\_root [1](#user-content-fn-1) | The created table uses the specified directory to store its data. The table alias is appended to it.                                                                                                                                                                                                                                                                                                                                                               | Optional                                | `/mnt/root`                                                                                        |
| partition\_by                          | Partition the created table by the specified columns. A directory is created for each partition.                                                                                                                                                                                                                                                                                                                                                                   | Optional                                | `date_day`                                                                                         |
| clustered\_by                          | Each partition in the created table will be split into a fixed number of buckets by the specified columns.                                                                                                                                                                                                                                                                                                                                                         | Optional                                | `country_code`                                                                                     |
| buckets                                | The number of buckets to create while clustering                                                                                                                                                                                                                                                                                                                                                                                                                   | Required if `clustered_by` is specified | `8`                                                                                                |
| tblproperties                          | The table properties configure table behavior. Properties differ depending on the file format, see reference docs ([Iceberg](https://iceberg.apache.org/docs/latest/configuration/#table-properties), [Parquet](https://spark.apache.org/docs/3.5.4/sql-data-sources-parquet.html#data-source-option), [Delta](https://docs.databricks.com/aws/en/delta/table-properties#delta-table-properties), [Hudi](https://hudi.apache.org/docs/sql_ddl/#table-properties)). | Optional                                | `# Iceberg Example
tblproperties:
  read.split.target-size: 268435456
  commit.retry.num-retries: 10` |

#### Incremental models[​](#incremental-models "Direct link to Incremental models")

dbt seeks to offer useful, intuitive modeling abstractions by means of its built-in configurations and materializations. Because there is so much variance between Apache Spark clusters out in the world—not to mention the powerful features offered to Databricks users by the Delta file format and custom runtime—making sense of all the available options is an undertaking in its own right.

Alternatively, you can use Apache Iceberg or Apache Hudi file format with Apache Spark runtime for building incremental models.

For that reason, the dbt-spark plugin leans heavily on the [`incremental_strategy` config](https://docs.getdbt.com/docs/build/incremental-strategy.md). This config tells the incremental materialization how to build models in runs beyond their first. It can be set to one of three values:

* **`append`** (default): Insert new records without updating or overwriting any existing data.
* **`insert_overwrite`**: If `partition_by` is specified, overwrite partitions in the table with new data. If no `partition_by` is specified, overwrite the entire table with new data.
* **`merge`** (Delta, Iceberg and Hudi file format only): Match records based on a `unique_key`; update old records, insert new ones. (If no `unique_key` is specified, all new data is inserted, similar to `append`.)
* `microbatch` Implements the [microbatch strategy](https://docs.getdbt.com/docs/build/incremental-microbatch.md) using `event_time` to define time-based ranges for filtering data.

Each of these strategies has its pros and cons, which we'll discuss below. As with any model config, `incremental_strategy` may be specified in `dbt_project.yml` or within a model file's `config()` block.

##### The `append` strategy[​](#the-append-strategy "Direct link to the-append-strategy")

Following the `append` strategy, dbt will perform an `insert into` statement with all new data. The appeal of this strategy is that it is straightforward and functional across all platforms, file types, connection methods, and Apache Spark versions. However, this strategy *cannot* update, overwrite, or delete existing data, so it is likely to insert duplicate records for many data sources.

Specifying `append` as the incremental strategy is optional, since it's the default strategy used when none is specified.

* Source code
* Run code

spark\_incremental.sql

spark\_incremental.sql

##### The `insert_overwrite` strategy[​](#the-insert_overwrite-strategy "Direct link to the-insert_overwrite-strategy")

This strategy is most effective when specified alongside a `partition_by` clause in your model config. dbt will run an [atomic `insert overwrite` statement](https://downloads.apache.org/spark/docs/3.0.0/sql-ref-syntax-dml-insert-overwrite-table.html) that dynamically replaces all partitions included in your query. Be sure to re-select *all* of the relevant data for a partition when using this incremental strategy.

If no `partition_by` is specified, then the `insert_overwrite` strategy will atomically replace all contents of the table, overriding all existing data with only the new records. The column schema of the table remains the same, however. This can be desirable in some limited circumstances, since it minimizes downtime while the table contents are overwritten. The operation is comparable to running `truncate` + `insert` on other databases. For atomic replacement of Delta-formatted tables, use the `table` materialization (which runs `create or replace`) instead.

* This strategy is not supported for tables with `file_format: delta`.
* This strategy is not available when connecting via Databricks SQL endpoints (`method: odbc` + `endpoint`).
* If connecting via a Databricks cluster + ODBC driver (`method: odbc` + `cluster`), you **must** include `set spark.sql.sources.partitionOverwriteMode DYNAMIC` in the [cluster Spark Config](https://docs.databricks.com/clusters/configure.html#spark-config) in order for dynamic partition replacement to work (`incremental_strategy: insert_overwrite` + `partition_by`).

[![Databricks cluster: Spark Config](/img/reference/databricks-cluster-sparkconfig-partition-overwrite.png?v=2 "Databricks cluster: Spark Config")](#)Databricks cluster: Spark Config

* Source code
* Run code

spark\_incremental.sql

spark\_incremental.sql

##### The `merge` strategy[​](#the-merge-strategy "Direct link to the-merge-strategy")

**Usage notes:** The `merge` incremental strategy requires:

* `file_format: delta, iceberg or hudi`
* Databricks Runtime 5.1 and above for delta file format
* Apache Spark for Iceberg or Hudi file format

dbt will run an [atomic `merge` statement](https://docs.databricks.com/spark/latest/spark-sql/language-manual/merge-into.html) which looks nearly identical to the default merge behavior on Snowflake and BigQuery. If a `unique_key` is specified (recommended), dbt will update old records with values from new records that match on the key column. If a `unique_key` is not specified, dbt will forgo match criteria and simply insert all new records (similar to `append` strategy).

* Source code
* Run code

merge\_incremental.sql

target/run/merge\_incremental.sql

#### Persisting model descriptions[​](#persisting-model-descriptions "Direct link to Persisting model descriptions")

Relation-level docs persistence is supported in dbt. For more information on configuring docs persistence, see [the docs](https://docs.getdbt.com/reference/resource-configs/persist_docs.md).

When the `persist_docs` option is configured appropriately, you'll be able to see model descriptions in the `Comment` field of `describe [table] extended` or `show table extended in [database] like '*'`.

#### Always `schema`, never `database`[​](#always-schema-never-database "Direct link to always-schema-never-database")

Apache Spark uses the terms "schema" and "database" interchangeably. dbt understands `database` to exist at a higher level than `schema`. As such, you should *never* use or set `database` as a node config or in the target profile when running dbt-spark.

If you want to control the schema/database in which dbt will materialize models, use the `schema` config and `generate_schema_name` macro *only*.

#### Default file format configurations[​](#default-file-format-configurations "Direct link to Default file format configurations")

To access advanced incremental strategies features, such as [snapshots](https://docs.getdbt.com/docs/build/snapshots.md) and the `merge` incremental strategy, you will want to use the Delta, Iceberg or Hudi file format as the default file format when materializing models as tables.

It's quite convenient to do this by setting a top-level configuration in your project file:

#### Footnotes[​](#footnote-label "Direct link to Footnotes")

1. If you configure `location_root`, dbt specifies a location path in the `create table` statement. This changes the table from "managed" to "external" in Spark/Databricks. [↩](#user-content-fnref-1)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### arguments (for functions)

[dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md).

functions/\<filename>.yml

#### Definition[​](#definition "Direct link to Definition")

The `arguments` property is used to define the parameters that a resource can accept. Each argument can have a `name`, a type field, and an optional `description`.

For **functions**, you can add `arguments` to a [function property](https://docs.getdbt.com/reference/function-properties.md), which defines the parameters for user-defined functions (UDFs) in your warehouse. The `data_type` for function arguments is warehouse-specific (for example, `STRING`, `VARCHAR`, `INTEGER`) and should match the data types supported by your data platform.

#### Properties[​](#properties "Direct link to Properties")

##### name[​](#name "Direct link to name")

The name of the argument. This is a required field if `arguments` is specified.

##### data\_type[​](#data_type "Direct link to data_type")

The data type that the warehouse expects for this parameter. This is a required field if `arguments` is specified and must match the data types supported by your specific data platform.

Warehouse-specific data types

The `data_type` values are warehouse-specific. Use the data type syntax that your warehouse requires:

* **Snowflake**: `STRING`, `NUMBER`, `BOOLEAN`, `TIMESTAMP_NTZ`, etc.
* **BigQuery**: `STRING`, `INT64`, `BOOL`, `TIMESTAMP`, `ARRAY<STRING>`, etc.
* **Redshift**: `VARCHAR`, `INTEGER`, `BOOLEAN`, `TIMESTAMP`, etc.
* **Postgres**: `TEXT`, `INTEGER`, `BOOLEAN`, `TIMESTAMP`, etc.

Refer to your warehouse documentation for the complete list of supported data types.

##### description[​](#description "Direct link to description")

An optional markdown string describing the argument. This is helpful for documentation purposes.

#### Examples[​](#examples "Direct link to Examples")

##### Simple function arguments[​](#simple-function-arguments "Direct link to Simple function arguments")

##### Complex data types[​](#complex-data-types "Direct link to Complex data types")

##### Array data types (BigQuery example)[​](#array-data-types-bigquery-example "Direct link to Array data types (BigQuery example)")

#### Related documentation[​](#related-documentation "Direct link to Related documentation")

* [Function properties](https://docs.getdbt.com/reference/function-properties.md)
* [Function configurations](https://docs.getdbt.com/reference/function-configs.md)
* [Arguments (for macros)](https://docs.getdbt.com/reference/resource-properties/arguments.md)
* [Returns](https://docs.getdbt.com/reference/resource-properties/returns.md)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### arguments (for macros)

macros/\<filename>.yml

#### Definition[​](#definition "Direct link to Definition")

The `arguments` property is used to define the parameters that a resource can accept. Each argument can have a `name`, a type field, and an optional `description`.

For **macros**, you can add `arguments` to a [macro property](https://docs.getdbt.com/reference/macro-properties.md), which helps in documenting the macro and understanding what inputs it requires.

#### type[​](#type "Direct link to type")

From dbt Core v1.10, you can opt into validating the arguments you define in macro documentation using the `validate_macro_args` behavior change flag. When enabled, dbt will:

* Infer arguments from the macro and includes them in the [manifest.json](https://docs.getdbt.com/reference/artifacts/manifest-json.md) file if no arguments are documented.
* Raise a warning if documented argument names don't match the macro definition.
* Raise a warning if `type` fields don't follow [supported formats](https://docs.getdbt.com/reference/resource-properties/arguments.md#supported-types).

Learn more about [macro argument validation](https://docs.getdbt.com/reference/global-configs/behavior-changes.md#macro-argument-validation).

macros/\<filename>.yml

##### Supported types[​](#supported-types "Direct link to Supported types")

From dbt Core v1.10, when you use the [`validate_macro_args`](https://docs.getdbt.com/reference/global-configs/behavior-changes.md#macro-argument-validation) flag, dbt supports the following types for macro arguments:

* `string` or `str`
* `boolean` or `bool`
* `integer` or `int`
* `float`
* `any`
* `list[<Type>]`, for example, `list[string]`
* `dict[<Type>, <Type>]`, for example, `dict[str, list[int]]`
* `optional[<Type>]`, for example, `optional[integer]`
* [`relation`](https://docs.getdbt.com/reference/dbt-classes.md#relation)
* [`column`](https://docs.getdbt.com/reference/dbt-classes.md#column)

Note that the types follow a Python-like style but are used for documentation and validation only. They are not Python types.

#### Examples[​](#examples "Direct link to Examples")

macros/cents\_to\_dollars.sql

macros/cents\_to\_dollars.yml

#### Related documentation[​](#related-documentation "Direct link to Related documentation")

* [Macro properties](https://docs.getdbt.com/reference/macro-properties.md)
* [Arguments (for functions)](https://docs.getdbt.com/reference/resource-properties/function-arguments.md)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

#### Definition[​](#definition "Direct link to Definition")

Optionally specify a custom list of directories to copy to the `target` directory as part of the `docs generate` command. This is useful for rendering images in your repository in your project documentation.

#### Default[​](#default "Direct link to Default")

By default, dbt will not copy any additional files as part of docs generate. For example, `asset-paths: []`.

Paths specified in `asset-paths` must be relative to the location of your `dbt_project.yml` file. Avoid using absolute paths like `/Users/username/project/assets`, as it will lead to unexpected behavior and outcomes.

* Avoid absolute paths:

#### Examples[​](#examples "Direct link to Examples")

##### Compile files in the `assets` subdirectory as part of `docs generate`[​](#compile-files-in-the-assets-subdirectory-as-part-of-docs-generate "Direct link to compile-files-in-the-assets-subdirectory-as-part-of-docs-generate")

Any files included in this directory will be copied to the `target/` directory as part of `dbt docs generate`, making them accessible as images in your project documentation.

Check out the full writeup on including images in your descriptions [here](https://docs.getdbt.com/reference/resource-properties/description.md#include-an-image-from-your-repo-in-your-descriptions).

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### AWS Glue configurations

#### Configuring tables[​](#configuring-tables "Direct link to Configuring tables")

When materializing a model as `table`, you may include several optional configs that are specific to the dbt-glue plugin, in addition to the [Apache Spark model configuration](https://docs.getdbt.com/reference/resource-configs/spark-configs.md#configuring-tables).

| Option           | Description                                                                                                                                                                                                                  | Required? | Example                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------- |
| custom\_location | By default, the adapter will store your data in the following path: `location path`/`database`/`table`. If you don't want to follow that default behaviour, you can use this parameter to set your own custom location on S3 | No        | `s3://mycustombucket/mycustompath` |

#### Incremental models[​](#incremental-models "Direct link to Incremental models")

dbt seeks to offer useful, intuitive modeling abstractions by means of its built-in configurations and materializations.

For that reason, the dbt-glue plugin leans heavily on the [`incremental_strategy` config](https://docs.getdbt.com/docs/build/incremental-strategy.md). This config tells the incremental materialization how to build models in runs beyond their first. It can be set to one of three values:

* **`append`** (default): Insert new records without updating or overwriting any existing data.
* **`insert_overwrite`**: If `partition_by` is specified, overwrite partitions in the table with new data. If no `partition_by` is specified, overwrite the entire table with new data.
* **`merge`** (Apache Hudi only): Match records based on a `unique_key`; update old records, insert new ones. (If no `unique_key` is specified, all new data is inserted, similar to `append`.)

Each of these strategies has its pros and cons, which we'll discuss below. As with any model config, `incremental_strategy` may be specified in `dbt_project.yml` or within a model file's `config()` block.

**Notes:** The default strategie is **`insert_overwrite`**

##### The `append` strategy[​](#the-append-strategy "Direct link to the-append-strategy")

Following the `append` strategy, dbt will perform an `insert into` statement with all new data. The appeal of this strategy is that it is straightforward and functional across all platforms, file types, connection methods, and Apache Spark versions. However, this strategy *cannot* update, overwrite, or delete existing data, so it is likely to insert duplicate records for many data sources.

* Source code
* Run code

glue\_incremental.sql

glue\_incremental.sql

drop view spark\_incremental\_\_dbt\_tmp

##### The `insert_overwrite` strategy[​](#the-insert_overwrite-strategy "Direct link to the-insert_overwrite-strategy")

This strategy is most effective when specified alongside a `partition_by` clause in your model config. dbt will run an [atomic `insert overwrite` statement](https://spark.apache.org/docs/3.1.2/sql-ref-syntax-dml-insert-overwrite-table.html) that dynamically replaces all partitions included in your query. Be sure to re-select *all* of the relevant data for a partition when using this incremental strategy.

If no `partition_by` is specified, then the `insert_overwrite` strategy will atomically replace all contents of the table, overriding all existing data with only the new records. The column schema of the table remains the same, however. This can be desirable in some limited circumstances, since it minimizes downtime while the table contents are overwritten. The operation is comparable to running `truncate` + `insert` on other databases. For atomic replacement of Delta-formatted tables, use the `table` materialization (which runs `create or replace`) instead.

* Source code
* Run code

spark\_incremental.sql

spark\_incremental.sql

Specifying `insert_overwrite` as the incremental strategy is optional, since it's the default strategy used when none is specified.

##### The `merge` strategy[​](#the-merge-strategy "Direct link to the-merge-strategy")

**Usage notes:** The `merge` incremental strategy requires:

* `file_format: hudi`
* AWS Glue runtime 2 with hudi libraries as extra jars

You can add hudi libraries as extra jars in the classpath using extra\_jars options in your profiles.yml. Here is an example:

dbt will run an [atomic `merge` statement](https://hudi.apache.org/docs/writing_data#spark-datasource-writer) which looks nearly identical to the default merge behavior on Snowflake and BigQuery. If a `unique_key` is specified (recommended), dbt will update old records with values from new records that match on the key column. If a `unique_key` is not specified, dbt will forgo match criteria and simply insert all new records (similar to `append` strategy).

hudi\_incremental.sql

#### Persisting model descriptions[​](#persisting-model-descriptions "Direct link to Persisting model descriptions")

Relation-level docs persistence is inherited from dbt-spark, for more details, check [Apache Spark model configuration](https://docs.getdbt.com/reference/resource-configs/spark-configs.md#persisting-model-descriptions).

#### Always `schema`, never `database`[​](#always-schema-never-database "Direct link to always-schema-never-database")

This section is also inherited from dbt-spark, for more details, check [Apache Spark model configuration](https://docs.getdbt.com/reference/resource-configs/spark-configs.md#always-schema-never-database).

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

[dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md).

#### Definition[​](#definition "Direct link to Definition")

The `batch_size` config determines how large batches are when running a [microbatch incremental model](https://docs.getdbt.com/docs/build/incremental-microbatch.md). Accepted values are `hour`, `day`, `month`, or `year`. You can configure `batch_size` for a [model](https://docs.getdbt.com/docs/build/models.md) in your `dbt_project.yml` file, property YAML file, or config block.

#### Examples[​](#examples "Direct link to Examples")

The following examples set `day` as the `batch_size` for the `user_sessions` model.

Example of the `batch_size` config in the `dbt_project.yml` file:

Example in a properties YAML file:

models/properties.yml

Example in SQL model config block:

models/user\_sessions.sql

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

[dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md).

#### Definition[​](#definition "Direct link to Definition")

Set the `begin` config to the timestamp value at which your [microbatch incremental model](https://docs.getdbt.com/docs/build/incremental-microbatch.md) data should begin — at the point the data becomes relevant for the microbatch model.

You can configure `begin` for a [model](https://docs.getdbt.com/docs/build/models.md) in your `dbt_project.yml` file, property YAML file, or config block. The value for `begin` must be a string representing an ISO-formatted date, *or* date and time, *or* [relative dates](#set-begin-to-use-relative-dates). Check out the [examples](#examples) in the next section for more details.

#### Examples[​](#examples "Direct link to Examples")

The following examples set `2024-01-01 00:00:00` as the `begin` config for the `user_sessions` model.

###### Example in the `dbt_project.yml` file[​](#example-in-the-dbt_projectyml-file "Direct link to example-in-the-dbt_projectyml-file")

###### Example in a properties YAML file[​](#example-in-a-properties-yaml-file "Direct link to Example in a properties YAML file")

models/properties.yml

###### Example in SQL model config block[​](#example-in-sql-model-config-block "Direct link to Example in SQL model config block")

models/user\_sessions.sql

###### Set `begin` to use relative dates[​](#set-begin-to-use-relative-dates "Direct link to set-begin-to-use-relative-dates")

To configure `begin` to use relative dates, you can use modules variables [`modules.datetime`](https://docs.getdbt.com/reference/dbt-jinja-functions/modules.md#datetime) and [`modules.pytz`](https://docs.getdbt.com/reference/dbt-jinja-functions/modules.md#pytz) to dynamically specify relative timestamps, such as yesterday's date or the start of the current week.

For example, to set `begin` to yesterday's date:

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

Most flags exist to configure runtime behaviors with multiple valid choices. The right choice may vary based on the environment, user preference, or the specific invocation.

Another category of flags provides existing projects with a migration window for runtime behaviors that are changing in newer releases of dbt. These flags help us achieve a balance between these goals, which can otherwise be in tension, by:

* Providing a better, more sensible, and more consistent default behavior for new users/projects.
* Providing a migration window for existing users/projects — nothing changes overnight without warning.
* Providing maintainability of dbt software. Every fork in behavior requires additional testing & cognitive overhead that slows future development. These flags exist to facilitate migration from "current" to "better," not to stick around forever.

These flags go through three phases of development:

1. **Introduction (disabled by default):** dbt adds logic to support both 'old' and 'new' behaviors. The 'new' behavior is gated behind a flag, disabled by default, preserving the old behavior.
2. **Maturity (enabled by default):** The default value of the flag is switched, from `false` to `true`, enabling the new behavior by default. Users can preserve the 'old' behavior and opt out of the 'new' behavior by setting the flag to `false` in their projects. They may see deprecation warnings when they do so.
3. **Removal (generally enabled):** After marking the flag for deprecation, we remove it along with the 'old' behavior it supported from the dbt codebases. We aim to support most flags indefinitely, but we're not committed to supporting them forever. If we choose to remove a flag, we'll offer significant advance notice.

#### What is a behavior change?[​](#what-is-a-behavior-change "Direct link to What is a behavior change?")

The same dbt project code and the same dbt commands return one result before the behavior change, and they return a different result after the behavior change.

Examples of behavior changes:

* dbt begins raising a validation *error* that it didn't previously.
* dbt changes the signature of a built-in macro. Your project has a custom reimplementation of that macro. This could lead to errors, because your custom reimplementation will be passed arguments it cannot accept.
* A dbt adapter renames or removes a method that was previously available on the `{{ adapter }}` object in the dbt-Jinja context.
* dbt makes a breaking change to contracted metadata artifacts by deleting a required field, changing the name or type of an existing field, or removing the default value of an existing field ([README](https://github.com/dbt-labs/dbt-core/blob/37d382c8e768d1e72acd767e0afdcb1f0dc5e9c5/core/dbt/artifacts/README.md#breaking-changes)).
* dbt removes one of the fields from [structured logs](https://docs.getdbt.com/reference/events-logging.md#structured-logging).

The following are **not** behavior changes:

* Fixing a bug where the previous behavior was defective, undesirable, or undocumented.
* dbt begins raising a *warning* that it didn't previously.
* dbt updates the language of human-friendly messages in log events.
* dbt makes a non-breaking change to contracted metadata artifacts by adding a new field with a default, or deleting a field with a default ([README](https://github.com/dbt-labs/dbt-core/blob/37d382c8e768d1e72acd767e0afdcb1f0dc5e9c5/core/dbt/artifacts/README.md#non-breaking-changes)).

The vast majority of changes are not behavior changes. Because introducing these changes does not require any action on the part of users, they are included in continuous releases of dbt and patch releases of dbt Core.

By contrast, behavior change migrations happen slowly, over the course of months, facilitated by behavior change flags. The flags are loosely coupled to the specific dbt runtime version. By setting flags, users have control over opting in (and later opting out) of these changes.

#### Behavior change flags[​](#behavior-change-flags "Direct link to Behavior change flags")

These flags *must* be set in the `flags` dictionary in `dbt_project.yml`. They configure behaviors closely tied to project code, which means they should be defined in version control and modified through pull or merge requests, with the same testing and peer review.

The following example displays the current flags and their current default values in the latest dbt and dbt Core versions. To opt out of a specific behavior change, set the values of the flag to `False` in `dbt_project.yml`. You will continue to see warnings for legacy behaviors you've opted out of, until you either:

* Resolve the issue (by switching the flag to `True`)
* Silence the warnings using the `warn_error_options.silence` flag

Here's an example of the available behavior change flags with their default values:

###### dbt Core behavior changes[​](#dbt-core-behavior-changes "Direct link to dbt Core behavior changes")

This table outlines which month of the "Latest" release track in dbt and which version of dbt Core contains the behavior change's introduction (disabled by default) or maturity (enabled by default).

| Flag                                                                                                                    | dbt "Latest": Intro | dbt "Latest": Maturity | dbt Core: Intro | dbt Core: Maturity |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------- | ---------------------- | --------------- | ------------------ |
| [require\_explicit\_package\_overrides\_for\_builtin\_materializations](#package-override-for-built-in-materialization) | 2024.04             | 2024.06                | 1.6.14, 1.7.14  | 1.8.0              |
| [require\_resource\_names\_without\_spaces](#no-spaces-in-resource-names)                                               | 2024.05             | 2025.05                | 1.8.0           | 1.10.0             |
| [source\_freshness\_run\_project\_hooks](#project-hooks-with-source-freshness)                                          | 2024.03             | 2025.05                | 1.8.0           | 1.10.0             |
| [skip\_nodes\_if\_on\_run\_start\_fails](#failures-in-on-run-start-hooks)                                               | 2024.10             | TBD\*                  | 1.9.0           | TBD\*              |
| [state\_modified\_compare\_more\_unrendered\_values](#source-definitions-for-state)                                     | 2024.10             | TBD\*                  | 1.9.0           | TBD\*              |
| [require\_yaml\_configuration\_for\_mf\_time\_spines](#metricflow-time-spine-yaml)                                      | 2024.10             | TBD\*                  | 1.9.0           | TBD\*              |
| [require\_batched\_execution\_for\_custom\_microbatch\_strategy](#custom-microbatch-strategy)                           | 2024.11             | TBD\*                  | 1.9.0           | TBD\*              |
| [require\_nested\_cumulative\_type\_params](#cumulative-metrics)                                                        | 2024.11             | TBD\*                  | 1.9.0           | TBD\*              |
| [validate\_macro\_args](#macro-argument-validation)                                                                     | 2025.03             | TBD\*                  | 1.10.0          | TBD\*              |
| [require\_generic\_test\_arguments\_property](#generic-test-arguments-property)                                         | 2025.07             | 2025.08                | 1.10.5          | 1.10.8             |

###### dbt adapter behavior changes[​](#dbt-adapter-behavior-changes "Direct link to dbt adapter behavior changes")

This table outlines which version of the dbt adapter contains the behavior change's introduction (disabled by default) or maturity (enabled by default).

| Flag                                                                                                                                                     | dbt-ADAPTER: Intro | dbt-ADAPTER: Maturity |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | --------------------- |
| [use\_info\_schema\_for\_columns](https://docs.getdbt.com/reference/global-configs/databricks-changes.md#use-information-schema-for-columns)             | Databricks 1.9.0   | TBD                   |
| [use\_user\_folder\_for\_python](https://docs.getdbt.com/reference/global-configs/databricks-changes.md#use-users-folder-for-python-model-notebooks)     | Databricks 1.9.0   | TBD                   |
| [use\_materialization\_v2](https://docs.getdbt.com/reference/global-configs/databricks-changes.md#use-restructured-materializations)                     | Databricks 1.10.0  | TBD                   |
| [enable\_truthy\_nulls\_equals\_macro](https://docs.getdbt.com/reference/global-configs/snowflake-changes.md#the-enable_truthy_nulls_equals_macro-flag)  | Snowflake 1.9.0    | TBD                   |
| [restrict\_direct\_pg\_catalog\_access](https://docs.getdbt.com/reference/global-configs/redshift-changes.md#the-restrict_direct_pg_catalog_access-flag) | Redshift 1.9.0     | TBD                   |

When the dbt Maturity is "TBD," it means we have not yet determined the exact date when these flags' default values will change. Affected users will see deprecation warnings in the meantime, and they will receive emails providing advance warning ahead of the maturity date. In the meantime, if you are seeing a deprecation warning, you can either:

* Migrate your project to support the new behavior, and then set the flag to `True` to stop seeing the warnings.
* Set the flag to `False`. You will continue to see warnings, and you will retain the legacy behavior even after the maturity date (when the default value changes).

##### Failures in on-run-start hooks[​](#failures-in-on-run-start-hooks "Direct link to Failures in on-run-start hooks")

The flag is `False` by default.

Set the `skip_nodes_if_on_run_start_fails` flag to `True` to skip all selected resources from running if there is a failure on an `on-run-start` hook.

##### Source definitions for state<!-- -->:modified[​](#source-definitions-for-state "Direct link to source-definitions-for-state")

You need to build the state directory using dbt v1.9 or higher, or [the dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md), and you need to set `state_modified_compare_more_unrendered_values` to `true` within your dbt\_project.yml.

If the state directory was built with an older dbt version or if the `state_modified_compare_more_unrendered_values` behavior change flag was either not set or set to `false`, you need to rebuild the state directory to avoid false positives during state comparison with `state:modified`.

The flag is `False` by default.

Set `state_modified_compare_more_unrendered_values` to `True` to reduce false positives during `state:modified` checks (especially when configs differ by target environment like `prod` vs. `dev`).

Setting the flag to `True` changes the `state:modified` comparison from using rendered values to unrendered values instead. It accomplishes this by persisting `unrendered_config` during model parsing and `unrendered_database` and `unrendered_schema` configs during source parsing.

##### Package override for built-in materialization[​](#package-override-for-built-in-materialization "Direct link to Package override for built-in materialization")

Setting the `require_explicit_package_overrides_for_builtin_materializations` flag to `True` prevents this automatic override.

We have deprecated the behavior where installed packages could override built-in materializations without your explicit opt-in. When this flag is set to `True`, a materialization defined in a package that matches the name of a built-in materialization will no longer be included in the search and resolution order. Unlike macros, materializations don't use the `search_order` defined in the project `dispatch` config.

The built-in materializations are `'view'`, `'table'`, `'incremental'`, `'materialized_view'` for models as well as `'test'`, `'unit'`, `'snapshot'`, `'seed'`, and `'clone'`.

You can still explicitly override built-in materializations, in favor of a materialization defined in a package, by reimplementing the built-in materialization in your root project and wrapping the package implementation.

macros/materialization\_view.sql

In the future, we may extend the project-level [`dispatch` configuration](https://docs.getdbt.com/reference/project-configs/dispatch-config.md) to support a list of authorized packages for overriding built-in materialization.

##### No spaces in resource names[​](#no-spaces-in-resource-names "Direct link to No spaces in resource names")

The `require_resource_names_without_spaces` flag enforces using resource names without spaces.

The names of dbt resources (for example, models) should contain letters, numbers, and underscores. We highly discourage the use of other characters, especially spaces. To that end, we have deprecated support for spaces in resource names. When the `require_resource_names_without_spaces` flag is set to `True`, dbt will raise an exception (instead of a deprecation warning) if it detects a space in a resource name.

models/model name with spaces.sql

##### Project hooks with source freshness[​](#project-hooks-with-source-freshness "Direct link to Project hooks with source freshness")

Set the `source_freshness_run_project_hooks` flag to include/exclude "project hooks" ([`on-run-start` / `on-run-end`](https://docs.getdbt.com/reference/project-configs/on-run-start-on-run-end.md)) in the `dbt source freshness` command execution. The flag is set to `True` (include) by default.

If you have a specific project [`on-run-start` / `on-run-end`](https://docs.getdbt.com/reference/project-configs/on-run-start-on-run-end.md) hooks that should not run before/after `source freshness` command, you can add a conditional check to those hooks:

##### MetricFlow time spine YAML[​](#metricflow-time-spine-yaml "Direct link to MetricFlow time spine YAML")

The `require_yaml_configuration_for_mf_time_spines` flag is set to `False` by default.

In previous versions (dbt Core 1.8 and earlier), the MetricFlow time spine configuration was stored in a `metricflow_time_spine.sql` file.

When the flag is set to `True`, dbt will continue to support the SQL file configuration. When the flag is set to `False`, dbt will raise a deprecation warning if it detects a MetricFlow time spine configured in a SQL file.

The MetricFlow YAML file should have the `time_spine:` field. Refer to [MetricFlow timespine](https://docs.getdbt.com/docs/build/metricflow-time-spine.md) for more details.

##### Custom microbatch strategy[​](#custom-microbatch-strategy "Direct link to Custom microbatch strategy")

The `require_batched_execution_for_custom_microbatch_strategy` flag is set to `False` by default and is only relevant if you already have a custom microbatch macro in your project. If you don't have a custom microbatch macro, you don't need to set this flag as dbt will handle microbatching automatically for any model using the [microbatch strategy](https://docs.getdbt.com/docs/build/incremental-microbatch.md#how-microbatch-compares-to-other-incremental-strategies).

Set the flag is set to `True` if you have a custom microbatch macro set up in your project. When the flag is set to `True`, dbt will execute the custom microbatch strategy in batches.

If you have a custom microbatch macro and the flag is left as `False`, dbt will issue a deprecation warning.

Previously, users needed to set the `DBT_EXPERIMENTAL_MICROBATCH` environment variable to `True` to prevent unintended interactions with existing custom incremental strategies. But this is no longer necessary, as setting `DBT_EXPERMINENTAL_MICROBATCH` will no longer have an effect on runtime functionality.

##### Cumulative metrics[​](#cumulative-metrics "Direct link to Cumulative metrics")

[Cumulative-type metrics](https://docs.getdbt.com/docs/build/cumulative.md#parameters) are nested under the `cumulative_type_params` field in [the dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md), dbt Core v1.9 and newer. Currently, dbt will warn users if they have cumulative metrics improperly nested. To enforce the new format (resulting in an error instead of a warning), set the `require_nested_cumulative_type_params` to `True`.

Use the following metric configured with the syntax before v1.9 as an example:

If you run `dbt parse` with that syntax on Core v1.9 or [the dbt "Latest" release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md), you will receive a warning like:

If you set `require_nested_cumulative_type_params` to `True` and re-run `dbt parse` you will now receive an error like:

Once the metric is updated, it will work as expected:

##### Macro argument validation[​](#macro-argument-validation "Direct link to Macro argument validation")

dbt supports optional validation for macro arguments using the `validate_macro_args` flag. By default, the `validate_macro_args` flag is set to `False`, which means that dbt won't validate the names or types of documented macro arguments.

In the past, dbt didn't enforce a standard vocabulary for the [`type`](https://docs.getdbt.com/reference/resource-properties/arguments.md#type) field on macro arguments in YAML. Because of this, the `type` field was used for documentation only, and dbt didn't check that:

* the argument names matched those in your macro
* the argument types were valid or consistent with the macro's Jinja definition

Here's an example of a documented macro:

When you set the `validate_macro_args` flag to `True`, dbt will:

* Check that all argument names in your YAML match those in the macro definition
* Raise warnings if the names or types don't match
* Validate that the [`type` values follow the supported format](https://docs.getdbt.com/reference/resource-properties/arguments.md#supported-types).
* If no arguments are documented in the YAML, infer them from the macro and include them in the [`manifest.json` file](https://docs.getdbt.com/reference/artifacts/manifest-json.md)

##### Generic test arguments property[​](#generic-test-arguments-property "Direct link to Generic test arguments property")

dbt supports parsing key-value arguments that are inputs to generic tests when specified under the `arguments` property. In the past, dbt didn't support a way to clearly disambiguate between properties that were inputs to generic tests and framework configurations, and only accepted arguments as top-level properties.

In "Latest", the `require_generic_test_arguments_property` flag is set to `True` by default. In dbt Core versions prior to 1.10.8, the default value is `False`. Using the `arguments` property in test definitions is optional in either case.

If you do use `arguments` while the flag is `False`, dbt will recognize it but raise the `ArgumentsPropertyInGenericTestDeprecation` warning. This warning lets you know that the flag will eventually default to `True` across all releases and will be parsed as keyword arguments to the data test.

Here's an example using the new `arguments` property:

Here's an example using the alternative `test_name` format:

When you set the `require_generic_test_arguments_property` flag to `True`, dbt will:

* Parse any key-value pairs under `arguments` in generic tests as inputs to the generic test macro.
* Raise a `MissingArgumentsPropertyInGenericTestDeprecation` warning if additional non-config arguments are specified outside of the `arguments` property.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### BigQuery configurations

#### Use `project` and `dataset` in configurations[​](#use-project-and-dataset-in-configurations "Direct link to use-project-and-dataset-in-configurations")

* `schema` is interchangeable with the BigQuery concept `dataset`
* `database` is interchangeable with the BigQuery concept of `project`

For our reference documentation, you can declare `project` in place of `database.` This will allow you to read and write from multiple BigQuery projects. Same for `dataset`.

#### Using table partitioning and clustering[​](#using-table-partitioning-and-clustering "Direct link to Using table partitioning and clustering")

##### Partition clause[​](#partition-clause "Direct link to Partition clause")

BigQuery supports the use of a [partition by](https://cloud.google.com/bigquery/docs/data-definition-language#specifying_table_partitioning_options) clause to easily partition a table by a column or expression. This option can help decrease latency and cost when querying large tables. Note that partition pruning [only works](https://cloud.google.com/bigquery/docs/querying-partitioned-tables#use_a_constant_filter_expression) when partitions are filtered using literal values (so selecting partitions using a subquery won't improve performance).

The `partition_by` config can be supplied as a dictionary with the following format:

###### Partitioning by a date or timestamp[​](#partitioning-by-a-date-or-timestamp "Direct link to Partitioning by a date or timestamp")

When using a `datetime` or `timestamp` column to partition data, you can create partitions with a granularity of hour, day, month, or year. A `date` column supports granularity of day, month and year. Daily partitioning is the default for all column types.

If the `data_type` is specified as a `date` and the granularity is day, dbt will supply the field as-is when configuring table partitioning.

* Source code
* Compiled code

###### Partitioning by an "ingestion" date or timestamp[​](#partitioning-by-an-ingestion-date-or-timestamp "Direct link to Partitioning by an \"ingestion\" date or timestamp")

BigQuery supports an [older mechanism of partitioning](https://cloud.google.com/bigquery/docs/partitioned-tables#ingestion_time) based on the time when each row was ingested. While we recommend using the newer and more ergonomic approach to partitioning whenever possible, for very large datasets, there can be some performance improvements to using this older, more mechanistic approach. [Read more about the `insert_overwrite` incremental strategy below](#copying-ingestion-time-partitions).

dbt will always instruct BigQuery to partition your table by the values of the column specified in `partition_by.field`. By configuring your model with `partition_by.time_ingestion_partitioning` set to `True`, dbt will use that column as the input to a `_PARTITIONTIME` pseudocolumn. Unlike with newer column-based partitioning, you must ensure that the values of your partitioning column match exactly the time-based granularity of your partitions.

* Source code
* Compiled code

###### Partitioning with integer buckets[​](#partitioning-with-integer-buckets "Direct link to Partitioning with integer buckets")

If the `data_type` is specified as `int64`, then a `range` key must also be provided in the `partition_by` dict. dbt will use the values provided in the `range` dict to generate the partitioning clause for the table.

* Source code
* Compiled code

###### Additional partition configs[​](#additional-partition-configs "Direct link to Additional partition configs")

If your model has `partition_by` configured, you may optionally specify two additional configurations:

* `require_partition_filter` (boolean): If set to `true`, anyone querying this model *must* specify a partition filter, otherwise their query will fail. This is recommended for very large tables with obvious partitioning schemes, such as event streams grouped by day. Note that this will affect other dbt models or tests that try to select from this model, too.

* `partition_expiration_days` (integer): If set for date- or timestamp-type partitions, the partition will expire that many days after the date it represents. E.g. A partition representing `2021-01-01`, set to expire after 7 days, will no longer be queryable as of `2021-01-08`, its storage costs zeroed out, and its contents will eventually be deleted. Note that [table expiration](#controlling-table-expiration) will take precedence if specified.

##### Clustering clause[​](#clustering-clause "Direct link to Clustering clause")

BigQuery tables can be [clustered](https://cloud.google.com/bigquery/docs/clustered-tables) to colocate related data.

Clustering on a single column:

Clustering on multiple columns:

#### Managing KMS encryption[​](#managing-kms-encryption "Direct link to Managing KMS encryption")

[Customer managed encryption keys](https://cloud.google.com/bigquery/docs/customer-managed-encryption) can be configured for BigQuery tables using the `kms_key_name` model configuration.

##### Using KMS encryption[​](#using-kms-encryption "Direct link to Using KMS encryption")

To specify the KMS key name for a model (or a group of models), use the `kms_key_name` model configuration. The following example sets the `kms_key_name` for all of the models in the `encrypted/` directory of your dbt project.

#### Labels and tags[​](#labels-and-tags "Direct link to Labels and tags")

##### Specifying labels[​](#specifying-labels "Direct link to Specifying labels")

dbt supports the specification of BigQuery labels for the tables and views that it creates. These labels can be specified using the `labels` model config.

The `labels` config can be provided in a model config, or in the `dbt_project.yml` file, as shown below.

BigQuery key-value pair entries for labels larger than 63 characters are truncated.

**Configuring labels in a model file**

**Configuring labels in dbt\_project.yml**

[![Viewing labels in the BigQuery console](/img/docs/building-a-dbt-project/building-models/73eaa8a-Screen_Shot_2020-01-20_at_12.12.54_PM.png?v=2 "Viewing labels in the BigQuery console")](#)Viewing labels in the BigQuery console

##### Specifying tags[​](#specifying-tags "Direct link to Specifying tags")

BigQuery table and view *tags* can be created by supplying an empty string for the label value.

You can create a new label with no value or remove a value from an existing label key.

A label with a key that has an empty value can also be referred to as a [tag](https://cloud.google.com/bigquery/docs/adding-labels#adding_a_label_without_a_value) in BigQuery. However, this is different from a [BigQuery tag](https://cloud.google.com/bigquery/docs/tags), which conditionally applies IAM policies to BigQuery tables and datasets. For more information, see the [Tags documentation](https://cloud.google.com/resource-manager/docs/tags/tags-overview).

##### Resource tags[​](#resource-tags "Direct link to Resource tags")

[BigQuery tags](https://cloud.google.com/bigquery/docs/tags) enable conditional IAM access control for BigQuery tables and views. You can apply these BigQuery tags using the `resource_tags` configuration. This section contains guidelines for using the `resource_tags` configuration parameter.

Resource tags are key-value pairs that must follow BigQuery's tag format: `{google_cloud_project_id}/{key_name}: value`. Unlike labels, BigQuery tags are primarily designed for IAM access control using conditional policies, allowing organizations to:

* **Implement conditional access control**: Apply IAM policies conditionally based on BigQuery tags (for example, granting access only to tables tagged with `environment:production`).
* **Enforce data governance**: Use BigQuery tags with IAM policies to protect sensitive data.
* **Control access at scale**: Manage access patterns consistently across different projects and environments.

###### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* [Create tag keys and values](https://cloud.google.com/bigquery/docs/tags#create_tag_keys_and_values) in advance before using them in dbt.
* Grant the [required IAM permissions](https://cloud.google.com/bigquery/docs/tags#required_permissions) to apply tags to resources.

###### Configuring tags in a model file[​](#configuring-tags-in-a-model-file "Direct link to Configuring tags in a model file")

To configure tags in a model file, refer to the following example:

###### Configuring tags in `dbt_project.yml`[​](#configuring-tags-in-dbt_projectyml "Direct link to configuring-tags-in-dbt_projectyml")

To configure tags in a `dbt_project.yml` file, refer to the following example:

###### Using both dbt tags and BigQuery tags[​](#using-both-dbt-tags-and-bigquery-tags "Direct link to Using both dbt tags and BigQuery tags")

You can use dbt's existing `tags` configuration alongside BigQuery's `resource_tags`:

For more information on setting up IAM conditional policies with BigQuery tags, see BigQuery's documentation on [tags](https://cloud.google.com/bigquery/docs/tags).

##### Policy tags[​](#policy-tags "Direct link to Policy tags")

BigQuery enables [column-level security](https://cloud.google.com/bigquery/docs/column-level-security-intro) by setting [policy tags](https://cloud.google.com/bigquery/docs/best-practices-policy-tags) on specific columns.

dbt enables this feature as a column resource property, `policy_tags` (*not* a node config).

models/\<filename>.yml

Please note that in order for policy tags to take effect, [column-level `persist_docs`](https://docs.getdbt.com/reference/resource-configs/persist_docs.md) must be enabled for the model, seed, or snapshot. Consider using [variables](https://docs.getdbt.com/docs/build/project-variables.md) to manage taxonomies and make sure to add the required security [roles](https://cloud.google.com/bigquery/docs/column-level-security-intro#roles) to your BigQuery service account key.

#### Merge behavior (incremental models)[​](#merge-behavior-incremental-models "Direct link to Merge behavior (incremental models)")

The [`incremental_strategy` config](https://docs.getdbt.com/docs/build/incremental-strategy.md) controls how dbt builds incremental models. dbt uses a [merge statement](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax) on BigQuery to refresh incremental tables.

The `incremental_strategy` config can be set to one of the following values:

* `merge` (default)
* `insert_overwrite`
* [`microbatch`](https://docs.getdbt.com/docs/build/incremental-microbatch.md)

##### Performance and cost[​](#performance-and-cost "Direct link to Performance and cost")

The operations performed by dbt while building a BigQuery incremental model can be made cheaper and faster by using a [clustering clause](#clustering-clause) in your model configuration. See [this guide](https://discourse.getdbt.com/t/benchmarking-incremental-strategies-on-bigquery/981) for more information on performance tuning for BigQuery incremental models.

**Note:** These performance and cost benefits are applicable to incremental models built with either the `merge` or the `insert_overwrite` incremental strategy.

##### The `merge` strategy[​](#the-merge-strategy "Direct link to the-merge-strategy")

The `merge` incremental strategy will generate a `merge` statement that looks something like:

The 'merge' approach automatically updates new data in the destination incremental table but requires scanning all source tables referenced in the model SQL, as well as destination tables. This can be slow and expensive for large data volumes. [Partitioning and clustering](#using-table-partitioning-and-clustering) techniques mentioned earlier can help mitigate these issues.

**Note:** The `unique_key` configuration is required when the `merge` incremental strategy is selected.

##### The `insert_overwrite` strategy[​](#the-insert_overwrite-strategy "Direct link to the-insert_overwrite-strategy")

The `insert_overwrite` strategy generates a merge statement that replaces entire partitions in the destination table. **Note:** this configuration requires that the model is configured with a [Partition clause](#partition-clause). The `merge` statement that dbt generates when the `insert_overwrite` strategy is selected looks something like:

For a complete writeup on the mechanics of this approach, see [this explainer post](https://discourse.getdbt.com/t/bigquery-dbt-incremental-changes/982).

###### Determining partitions to overwrite[​](#determining-partitions-to-overwrite "Direct link to Determining partitions to overwrite")

dbt is able to determine the partitions to overwrite dynamically from the values present in the temporary table, or statically using a user-supplied configuration.

The "dynamic" approach is simplest (and the default), but the "static" approach will reduce costs by eliminating multiple queries in the model build script.

###### Static partitions[​](#static-partitions "Direct link to Static partitions")

To supply a static list of partitions to overwrite, use the `partitions` configuration.

This example model serves to replace the data in the destination table for both *today* and *yesterday* every day that it is run. It is the fastest and cheapest way to incrementally update a table using dbt. If we wanted this to run more dynamically— let’s say, always for the past 3 days—we could leverage dbt’s baked-in [datetime macros](https://github.com/dbt-labs/dbt-core/blob/dev/octavius-catto/core/dbt/include/global_project/macros/etc/datetime.sql) and write a few of our own.

Think of this as "full control" mode. You must ensure that expressions or literal values in the `partitions` config have proper quoting when templated, and that they match the `partition_by.data_type` (`timestamp`, `datetime`, `date`, or `int64`). Otherwise, the filter in the incremental `merge` statement will raise an error.

###### Dynamic partitions[​](#dynamic-partitions "Direct link to Dynamic partitions")

If no `partitions` configuration is provided, dbt will instead:

1. Create a temporary table for your model SQL
2. Query the temporary table to find the distinct partitions to be overwritten
3. Query the destination table to find the *max* partition in the database

When building your model SQL, you can take advantage of the introspection performed by dbt to filter for only *new* data. The maximum value in the partitioned field in the destination table will be available using the `_dbt_max_partition` BigQuery scripting variable. **Note:** this is a BigQuery SQL variable, not a dbt Jinja variable, so no Jinja brackets are required to access this variable.

**Example model SQL:**

###### Copying partitions[​](#copying-partitions "Direct link to Copying partitions")

If you are replacing entire partitions in your incremental runs, you can opt to do so with the [copy table API](https://cloud.google.com/bigquery/docs/managing-tables#copy-table) and partition decorators rather than a `merge` statement. While this mechanism doesn't offer the same visibility and ease of debugging as the SQL `merge` statement, it can yield significant savings in time and cost for large datasets because the copy table API does not incur any costs for inserting the data - it's equivalent to the `bq cp` gcloud command line interface (CLI) command.

You can enable this by switching on `copy_partitions: True` in the `partition_by` configuration. This approach works only in combination with "dynamic" partition replacement.

#### Controlling table expiration[​](#controlling-table-expiration "Direct link to Controlling table expiration")

By default, dbt-created tables never expire. You can configure certain model(s) to expire after a set number of hours by setting `hours_to_expiration`.

The `hours_to_expiration` only applies to initial creation of the underlying table. It doesn't reset for incremental models when they do another run.

models/\<modelname>.sql

#### Authorized views[​](#authorized-views "Direct link to Authorized views")

If the `grant_access_to` config is specified for a model materialized as a view, dbt will grant the view model access to select from the list of datasets provided. See [BQ docs on authorized views](https://cloud.google.com/bigquery/docs/share-access-views) for more details.

The `grants` config and the `grant_access_to` config are distinct.

* **`grant_access_to`:** Enables you to set up authorized views. When configured, dbt provides an authorized view access to show partial information from other datasets, without providing end users with full access to those underlying datasets. For more information, see ["BigQuery configurations: Authorized views"](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md#authorized-views)
* **`grants`:** Provides specific permissions to users, groups, or service accounts for managing access to datasets you're producing with dbt. For more information, see ["Resource configs: grants"](https://docs.getdbt.com/reference/resource-configs/grants.md)

You can use the two features together: "authorize" a view model with the `grants_access_to` configuration, and then add `grants` to that view model to share its query results (and *only* its query results) with other users, groups, or service accounts.

models/\<modelname>.sql

Views with this configuration will be able to select from objects in `project_1.dataset_1` and `project_2.dataset_2`, even when they are located elsewhere and queried by users who do not otherwise have access to `project_1.dataset_1` and `project_2.dataset_2`.

#### Materialized views[​](#materialized-views "Direct link to Materialized views")

The BigQuery adapter supports [materialized views](https://cloud.google.com/bigquery/docs/materialized-views-intro) with the following configuration parameters:

| Parameter                                                                                                  | Type                   | Required | Default | Change Monitoring Support |
| ---------------------------------------------------------------------------------------------------------- | ---------------------- | -------- | ------- | ------------------------- |
| [`on_configuration_change`](https://docs.getdbt.com/reference/resource-configs/on_configuration_change.md) | `<string>`             | no       | `apply` | n/a                       |
| [`cluster_by`](#clustering-clause)                                                                         | `[<string>]`           | no       | `none`  | drop/create               |
| [`partition_by`](#partition-clause)                                                                        | `{<dictionary>}`       | no       | `none`  | drop/create               |
| [`enable_refresh`](#auto-refresh)                                                                          | `<boolean>`            | no       | `true`  | alter                     |
| [`refresh_interval_minutes`](#auto-refresh)                                                                | `<float>`              | no       | `30`    | alter                     |
| [`max_staleness`](#auto-refresh) (in Preview)                                                              | `<interval>`           | no       | `none`  | alter                     |
| [`description`](https://docs.getdbt.com/reference/resource-properties/description.md)                      | `<string>`             | no       | `none`  | alter                     |
| [`labels`](#specifying-labels)                                                                             | `{<string>: <string>}` | no       | `none`  | alter                     |
| [`resource_tags`](#resource-tags)                                                                          | `{<string>: <string>}` | no       | `none`  | alter                     |
| [`hours_to_expiration`](#controlling-table-expiration)                                                     | `<integer>`            | no       | `none`  | alter                     |
| [`kms_key_name`](#using-kms-encryption)                                                                    | `<string>`             | no       | `none`  | alter                     |

* Project file
* Property file
* Config block

models/properties.yml

models/\<model\_name>.sql

Many of these parameters correspond to their table counterparts and have been linked above. The set of parameters unique to materialized views covers [auto-refresh functionality](#auto-refresh).

Learn more about these parameters in BigQuery's docs:

* [CREATE MATERIALIZED VIEW statement](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#create_materialized_view_statement)
* [materialized\_view\_option\_list](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#materialized_view_option_list)

##### Auto-refresh[​](#auto-refresh "Direct link to Auto-refresh")

| Parameter                    | Type         | Required | Default | Change Monitoring Support |
| ---------------------------- | ------------ | -------- | ------- | ------------------------- |
| `enable_refresh`             | `<boolean>`  | no       | `true`  | alter                     |
| `refresh_interval_minutes`   | `<float>`    | no       | `30`    | alter                     |
| `max_staleness` (in Preview) | `<interval>` | no       | `none`  | alter                     |

BigQuery supports [automatic refresh](https://cloud.google.com/bigquery/docs/materialized-views-manage#automatic_refresh) configuration for materialized views. By default, a materialized view will automatically refresh within 5 minutes of changes in the base table, but not more frequently than once every 30 minutes. BigQuery only officially supports the configuration of the frequency (the "once every 30 minutes" frequency); however, there is a feature in preview that allows for the configuration of the staleness (the "5 minutes" refresh). dbt will monitor these parameters for changes and apply them using an `ALTER` statement.

Learn more about these parameters in BigQuery's docs:

* [materialized\_view\_option\_list](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-definition-language#materialized_view_option_list)
* [max\_staleness](https://cloud.google.com/bigquery/docs/materialized-views-create#max_staleness)

##### Limitations[​](#limitations "Direct link to Limitations")

As with most data platforms, there are limitations associated with materialized views. Some worth noting include:

* Materialized view SQL has a [limited feature set](https://cloud.google.com/bigquery/docs/materialized-views-create#supported-mvs).
* Materialized view SQL cannot be updated; the materialized view must go through a `--full-refresh` (DROP/CREATE).
* The `partition_by` clause on a materialized view must match that of the underlying base table.
* While materialized views can have descriptions, materialized view *columns* cannot.
* Recreating/dropping the base table requires recreating/dropping the materialized view.

Find more information about materialized view limitations in Google's BigQuery [docs](https://cloud.google.com/bigquery/docs/materialized-views-intro#limitations).

#### Python model configuration[​](#python-model-configuration "Direct link to Python model configuration")

**Submission methods:** BigQuery supports a few different mechanisms to submit Python code, each with relative advantages. The `dbt-bigquery` adapter uses BigQuery DataFrames (BigFrames) or Dataproc. This process reads data from BigQuery, computes it either natively with BigQuery DataFrames or Dataproc, and writes the results back to BigQuery.

* BigQuery DataFrames
* Dataproc

BigQuery DataFrames can execute pandas and scikit-learn. There's no need to manage infrastructure and leverages BigQuery-distributed query engines. It's great for analysts, data scientists, and machine learning engineers who want to manipulate big data using a pandas-like syntax.

**Note:** BigQuery DataFrames run on Google Colab's default runtime. If no `default` runtime template is available, the adapter will automatically create one for you and mark it `default` for next time usage (assuming it has the right permissions).

**BigQuery DataFrames setup:**

**Examples:**

Example 1 (unknown):
```unknown
##### Variable default values[​](#variable-default-values "Direct link to Variable default values")

The `var()` function takes an optional second argument, `default`. If this argument is provided, then it will be the default value for the variable if one is not explicitly defined.

my\_model.sql
```

Example 2 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About zip context method

The `zip` context method can be used to return an iterator of tuples, where the i-th tuple contains the i-th element from each of the argument iterables. For more information, see [Python docs](https://docs.python.org/3/library/functions.html#zip).

**Args**:

* `*args`: Any number of iterables
* `default`: A default value to return if `*args` is not iterable

##### Usage[​](#usage "Direct link to Usage")
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
##### zip\_strict[​](#zip_strict "Direct link to zip_strict")

The `zip_strict` context method can be used to used to return an iterator of tuples, just like `zip`. The difference to the `zip` context method is that the `zip_strict` method will raise an exception on a `TypeError`, if one of the provided values is not a valid iterable.

**Args**:

* `value`: The iterable to convert (e.g. a list)
```

---

## clone all of my models from specified state to my target schema(s), running up to 50 clone statements in parallel

**URL:** llms-txt#clone-all-of-my-models-from-specified-state-to-my-target-schema(s),-running-up-to-50-clone-statements-in-parallel

**Contents:**
  - About dbt compile command
  - About dbt debug command
  - About dbt deps command

dbt clone --state path/to/artifacts --threads 50

dbt compile --select "stg_orders"                           
dbt compile --inline "select * from {{ ref('raw_orders') }}"

dbt compile --select "stg_orders"

21:17:09  Running with dbt=1.7.5
21:17:09  Registered adapter: postgres=1.7.5
21:17:09  Found 5 models, 3 seeds, 20 tests, 0 sources, 0 exposures, 0 metrics, 401 macros, 0 groups, 0 semantic models
21:17:09  
21:17:09 Concurrency: 24 threads (target='dev')
21:17:09  
21:17:09  Compiled node 'stg_orders' is:
with source as (
    select * from "jaffle_shop"."main"."raw_orders"

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

select * from renamed

dbt compile --inline "select * from {{ ref('raw_orders') }}"

18:15:49  Running with dbt=1.7.5
18:15:50  Registered adapter: postgres=1.7.5
18:15:50  Found 5 models, 3 seeds, 20 tests, 0 sources, 0 exposures, 0 metrics, 401 macros, 0 groups, 0 semantic models
18:15:50  
18:15:50  Concurrency: 5 threads (target='postgres')
18:15:50  
18:15:50  Compiled inline node is:
select * from "jaffle_shop"."main"."raw_orders"

Usage: dbt debug [OPTIONS]

Show information on the current dbt environment and check dependencies, then
 test the database connection. Not to be confused with the --debug option
 which increases verbosity.

Options:
 --cache-selected-only / --no-cache-selected-only
                At start of run, populate relational cache
                only for schemas containing selected nodes,
                or for all schemas of interest.

-d, --debug / --no-debug    
                Display debug logging during dbt execution.
                Useful for debugging and making bug reports.

--defer / --no-defer      
                If set, resolve unselected nodes by
                deferring to the manifest within the --state
                directory.

--defer-state DIRECTORY     
                Override the state directory for deferral
                only.

--deprecated-favor-state TEXT  
                Internal flag for deprecating old env var.

-x, --fail-fast / --no-fail-fast
                 Stop execution on first failure.

--favor-state / --no-favor-state
                If set, defer to the argument provided to
                the state flag for resolving unselected
                nodes, even if the node(s) exist as a
                database object in the current environment.

--indirect-selection [eager|cautious|buildable|empty]
                Choose which tests to select that are
                adjacent to selected resources. Eager is
                most inclusive, cautious is most exclusive,
                and buildable is in between. Empty includes
                no tests at all.

--log-cache-events / --no-log-cache-events
                Enable verbose logging for relational cache
                events to help when debugging.

--log-format [text|debug|json|default]
                Specify the format of logging to the console
                and the log file. Use --log-format-file to
                configure the format for the log file
                differently than the console.

--log-format-file [text|debug|json|default]
                Specify the format of logging to the log
                file by overriding the default value and the
                general --log-format setting.

--log-level [debug|info|warn|error|none]
                Specify the minimum severity of events that
                are logged to the console and the log file.
                Use --log-level-file to configure the
                severity for the log file differently than
                the console.

--log-level-file [debug|info|warn|error|none]
                Specify the minimum severity of events that
                are logged to the log file by overriding the
                default value and the general --log-level
                setting.

--log-path PATH         
                Configure the 'log-path'. Only applies this
                setting for the current run. Overrides the
                'DBT_LOG_PATH' if it is set.

--partial-parse / --no-partial-parse
                Allow for partial parsing by looking for and
                writing to a pickle file in the target
                directory. This overrides the user
                configuration file.

--populate-cache / --no-populate-cache
                At start of run, use `show` or
                `information_schema` queries to populate a
                relational cache, which can speed up
                subsequent materializations.

--print / --no-print      
                Output all {{ print() }} macro calls.

--printer-width INTEGER     
                Sets the width of terminal output

--profile TEXT         
                Which existing profile to load. Overrides
                setting in dbt_project.yml.

-q, --quiet / --no-quiet    
                Suppress all non-error logging to stdout.
                Does not affect {{ print() }} macro calls.

-r, --record-timing-info PATH  
                When this option is passed, dbt will output
                low-level timing stats to the specified
                file. Example: `--record-timing-info
                output.profile`

--send-anonymous-usage-stats / --no-send-anonymous-usage-stats
                Send anonymous usage stats to dbt Labs.

--state DIRECTORY        
                Unless overridden, use this state directory
                for both state comparison and deferral.

--static-parser / --no-static-parser
                Use the static parser.

-t, --target TEXT        
                Which target to load for the given profile

--use-colors / --no-use-colors 
                Specify whether log output is colorized in
                the console and the log file. Use --use-
                colors-file/--no-use-colors-file to colorize
                the log file differently than the console.

--use-colors-file / --no-use-colors-file
                Specify whether log file output is colorized
                by overriding the default value and the
                general --use-colors/--no-use-colors
                setting.

--use-experimental-parser / --no-use-experimental-parser
                Enable experimental parsing features.

-V, -v, --version        
                Show version information and exit

--version-check / --no-version-check
                If set, ensure the installed dbt version
                matches the require-dbt-version specified in
                the dbt_project.yml file (if any).
                Otherwise, allow them to differ.

--warn-error   
                If dbt would normally warn, instead raise an
                exception. Examples include --select that
                selects nothing, deprecations,
                configurations with no associated models,
                invalid test configurations, and missing
                sources/refs in tests.

--warn-error-options WARNERROROPTIONSTYPE
                If dbt would normally warn, instead raise an
                exception based on include/exclude
                configuration. Examples include --select
                that selects nothing, deprecations,
                configurations with no associated models,
                invalid test configurations, and missing
                sources/refs in tests. This argument should
                be a YAML string, with keys 'include' or
                'exclude'. eg. '{"include": "all",
                "exclude": ["NoNodesForSelectionCriteria"]}'

--write-json / --no-write-json 
                Whether or not to write the manifest.json
                and run_results.json files to the target
                directory

--connection          
                Test the connection to the target database
                independent of dependency checks.
                Available in Studio IDE and dbt Core CLI

--config-dir          
                Print a system-specific command to access
                the directory that the current dbt project
                is searching for a profiles.yml. Then, exit.
                This flag renders other debug step flags no-
                ops.

--profiles-dir PATH       
                Which directory to look in for the
                profiles.yml file. If not set, dbt will look
                in the current working directory first, then
                HOME/.dbt/

--project-dir PATH       
                Which directory to look in for the
                dbt_project.yml file. Default is the current
                working directory and its parents.

--vars YAML           
                Supply variables to the project. This
                argument overrides variables defined in your
                dbt_project.yml file. This argument should
                be a YAML string, eg. '{my_variable:
                my_value}'

-h, --help           
                Show this message and exit.

dbt debug --connection

dbt debug --config-dir
To view your profiles.yml file, run:

open /Users/alice/.dbt

dbt debug --connection

packages:
  - package: dbt-labs/dbt_utils
    version: 0.7.1
  - package: brooklyn-data/dbt_artifacts
    version: 1.2.0
    install-prerelease: true
  - package: dbt-labs/codegen
    version: 0.4.0
  - package: calogica/dbt_expectations
    version: 0.4.1
  - git: https://github.com/dbt-labs/dbt_audit_helper.git
    revision: 0.4.0
  - git: "https://github.com/dbt-labs/dbt_labs-experimental-features" # git URL
    subdirectory: "materialized-views" # name of subdirectory containing `dbt_project.yml`
    revision: 0.0.1
  - package: dbt-labs/snowplow
    version: 0.13.0

Installing dbt-labs/dbt_utils@0.7.1
  Installed from version 0.7.1
  Up to date!
Installing brooklyn-data/dbt_artifacts@1.2.0
  Installed from version 1.2.0
Installing dbt-labs/codegen@0.4.0
  Installed from version 0.4.0
  Up to date!
Installing calogica/dbt_expectations@0.4.1
  Installed from version 0.4.1
  Up to date!
Installing https://github.com/dbt-labs/dbt_audit_helper.git@0.4.0
  Installed from revision 0.4.0
Installing https://github.com/dbt-labs/dbt_labs-experimental-features@0.0.1
  Installed from revision 0.0.1
   and subdirectory materialized-views
Installing dbt-labs/snowplow@0.13.0
  Installed from version 0.13.0
  Updated version available: 0.13.1
Installing calogica/dbt_date@0.4.0
  Installed from version 0.4.0
  Up to date!

Updates available for packages: ['tailsdotcom/dbt_artifacts', 'dbt-labs/snowplow']
Update your versions in packages.yml, then run dbt deps

dbt deps --add-package dbt-labs/dbt_utils@1.0.0

**Examples:**

Example 1 (unknown):
```unknown
##### When to use `dbt clone` instead of [deferral](https://docs.getdbt.com/reference/node-selection/defer.md)?[​](#when-to-use-dbt-clone-instead-of-deferral "Direct link to when-to-use-dbt-clone-instead-of-deferral")

Unlike deferral, `dbt clone` requires some compute and creation of additional objects in your data warehouse. In many cases, deferral is a cheaper and simpler alternative to `dbt clone`. However, `dbt clone` covers additional use cases where deferral may not be possible.

For example, by creating actual data warehouse objects, `dbt clone` allows you to test out your code changes on downstream dependencies *outside of dbt* (such as a BI tool).

As another example, you could `clone` your modified incremental models as the first step of your dbt CI job to prevent costly `full-refresh` builds for warehouses that support zero-copy cloning.

#### Cloning in dbt[​](#cloning-in-dbt "Direct link to Cloning in dbt")

You can clone nodes between states in dbt using the `dbt clone` command. This is available in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md) and the [Cloud CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md) and relies on the [`--defer`](https://docs.getdbt.com/reference/node-selection/defer.md) feature. For more details on defer in dbt, read [Using defer in dbt](https://docs.getdbt.com/docs/cloud/about-cloud-develop-defer.md).

* **Using Cloud CLI** — The `dbt clone` command in the Cloud CLI automatically includes the `--defer` flag. This means you can use the `dbt clone` command without any additional setup.

* **Using Studio IDE** — To use the `dbt clone` command in the Studio IDE, follow these steps before running the `dbt clone` command:

  * Set up your **Production environment** and have a successful job run.

  * Enable **Defer to production** by toggling the switch in the lower-right corner of the command bar.

    [![Select the 'Defer to production' toggle on the bottom right of the command bar to enable defer in the Studio IDE.](/img/docs/dbt-cloud/defer-toggle.png?v=2 "Select the 'Defer to production' toggle on the bottom right of the command bar to enable defer in the Studio IDE.")](#)Select the 'Defer to production' toggle on the bottom right of the command bar to enable defer in the Studio IDE.

  * Run the `dbt clone` command from the command bar.

Check out [this Developer blog post](https://docs.getdbt.com/blog/to-defer-or-to-clone) for more details on best practices when to use `dbt clone` vs. deferral.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt compile command

`dbt compile` generates executable SQL from source `model`, `test`, and `analysis` files. You can find these compiled SQL files in the `target/` directory of your dbt project.

The `compile` command is useful for:

1. Visually inspecting the compiled output of model files. This is useful for validating complex Jinja logic or macro usage.
2. Manually running compiled SQL. While debugging a model or schema test, it's often useful to execute the underlying `select` statement to find the source of the bug.
3. Compiling `analysis` files. Read more about analysis files [here](https://docs.getdbt.com/docs/build/analyses.md).

Some common misconceptions:

* `dbt compile` is *not* a pre-requisite of `dbt run`, or other building commands. Those commands will handle compilation themselves.
* If you just want dbt to read and validate your project code, without connecting to the data warehouse, use `dbt parse` instead.

##### Interactive compile[​](#interactive-compile "Direct link to Interactive compile")

Starting in dbt v1.5, `compile` can be "interactive" in the CLI, by displaying the compiled code of a node or arbitrary dbt-SQL query:

* `--select` a specific node *by name*
* `--inline` an arbitrary dbt-SQL query

This will log the compiled SQL to the terminal, in addition to writing to the `target/` directory.

For example:
```

Example 2 (unknown):
```unknown
returns the following:
```

Example 3 (unknown):
```unknown

```

Example 4 (unknown):
```unknown
The command accesses the data platform to cache-related metadata, and to run introspective queries. Use the flags:

* `--no-populate-cache` to disable the initial cache population. If metadata is needed, it will be a cache miss, requiring dbt to run the metadata query. This is a `dbt` flag, which means you need to add `dbt` as a prefix. For example: `dbt --no-populate-cache`.
* `--no-introspect` to disable [introspective queries](https://docs.getdbt.com/faqs/Warehouse/db-connection-dbt-compile.md#introspective-queries). dbt will raise an error if a model's definition requires running one. This is a `dbt compile` flag, which means you need to add `dbt compile` as a prefix. For example:`dbt compile --no-introspect`.

##### FAQs[​](#faqs "Direct link to FAQs")

Why dbt compile needs a data platform connection

`dbt compile` needs a data platform connection in order to gather the info it needs (including from introspective queries) to prepare the SQL for every model in your project.

##### dbt compile[​](#dbt-compile "Direct link to dbt compile")

The [`dbt compile` command](https://docs.getdbt.com/reference/commands/compile.md) generates executable SQL from `source`, `model`, `test`, and `analysis` files. `dbt compile` is similar to `dbt run` except that it doesn't materialize the model's compiled SQL into an existing table. So, up until the point of materialization, `dbt compile` and `dbt run` are similar because they both require a data platform connection, run queries, and have an [`execute` variable](https://docs.getdbt.com/reference/dbt-jinja-functions/execute.md) set to `True`.

However, here are some things to consider:

* You don't need to execute `dbt compile` before `dbt run`
* In dbt, `compile` doesn't mean `parse`. This is because `parse` validates your written `YAML`, configured tags, and so on.

##### Introspective queries[​](#introspective-queries "Direct link to Introspective queries")

To generate the compiled SQL for many models, dbt needs to run introspective queries, (which is when dbt needs to run SQL in order to pull data back and do something with it) against the data platform.

These introspective queries include:

* Populating the relation cache. For more information, refer to the [Create new materializations](https://docs.getdbt.com/guides/create-new-materializations.md) guide. Caching speeds up the metadata checks, including whether an [incremental model](https://docs.getdbt.com/docs/build/incremental-models.md) already exists in the data platform.
* Resolving [macros](https://docs.getdbt.com/docs/build/jinja-macros.md#macros), such as `run_query` or `dbt_utils.get_column_values` that you're using to template out your SQL. This is because dbt needs to run those queries during model SQL compilation.

Without a data platform connection, dbt can't perform these introspective queries and won't be able to generate the compiled SQL needed for the next steps in the dbt workflow. You can [`parse`](https://docs.getdbt.com/reference/commands/parse.md) a project and use the [`list`](https://docs.getdbt.com/reference/commands/list.md) resources in the project, without an internet or data platform connection. Parsing a project is enough to produce a [manifest](https://docs.getdbt.com/reference/artifacts/manifest-json.md), however, keep in mind that the written-out manifest won't include compiled SQL.

To configure a project, you do need a [connection profile](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles.md) (`profiles.yml` if using the CLI). You need this file because the project's configuration depends on its contents. For example, you may need to use [`{{target}}`](https://docs.getdbt.com/reference/dbt-jinja-functions/target.md) for conditional configs or know what platform you're running against so that you can choose the right flavor of SQL.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt debug command

Use dbt debug to test database connections and check system setup.

`dbt debug` is a utility function to test the database connection and display information for debugging purposes, such as the validity of your project file, the [dbt version](https://docs.getdbt.com/reference/dbt-jinja-functions/dbt_version.md), and your installation of any requisite dependencies (like `git` when you run `dbt deps`).

It checks your database connection, local configuration, and system setup across multiple axes to help identify potential issues before running dbt commands.

By default, `dbt debug` validates:

* **Database connection** (for configured profiles)
* **dbt project setup** (like `dbt_project.yml` validity)
* **System environment** (OS, Python version, installed dbt version)
* **Required dependencies** (such as `git` for `dbt deps`)
* **Adapter details** (installed adapter versions and compatibility)

\*Note: Not to be confused with [debug-level logging](https://docs.getdbt.com/reference/global-configs/logs.md#debug-level-logging) through the `--debug` option which increases verbosity.

#### Flags[​](#flags "Direct link to Flags")

Most of the `dbt debug` flags apply to the dbt Core CLI. Some flags also work in Cloud CLI, but only `--connection` is supported in the Studio IDE.

* dbt Core CLI: Supports all flags.
* Studio IDE: Only supports dbt `debug` and `dbt debug --connection`.
* Cloud CLI: Only supports dbt `debug` and `dbt debug --connection`. You can also use the [`dbt environment`](https://docs.getdbt.com/reference/commands/dbt-environment.md) command to interact with your dbt environment.

`dbt debug` supports the following flags in your terminal when using the command line interface (CLI):
```

---

## dbt will supply a unique schema per test, so we do not specify 'schema' here

**URL:** llms-txt#dbt-will-supply-a-unique-schema-per-test,-so-we-do-not-specify-'schema'-here

@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        'type': '<myadapter>',
        'threads': 1,
        'host': os.getenv('HOST_ENV_VAR_NAME'),
        'user': os.getenv('USER_ENV_VAR_NAME'),
        ...
    }

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import BaseSingularTestsEphemeral
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod

class TestSimpleMaterializationsMyAdapter(BaseSimpleMaterializations):
    pass

class TestSingularTestsMyAdapter(BaseSingularTests):
    pass

class TestSingularTestsEphemeralMyAdapter(BaseSingularTestsEphemeral):
    pass

class TestEmptyMyAdapter(BaseEmpty):
    pass

class TestEphemeralMyAdapter(BaseEphemeral):
    pass

class TestIncrementalMyAdapter(BaseIncremental):
    pass

class TestGenericTestsMyAdapter(BaseGenericTests):
    pass

class TestSnapshotCheckColsMyAdapter(BaseSnapshotCheckCols):
    pass

class TestSnapshotTimestampMyAdapter(BaseSnapshotTimestamp):
    pass

class TestBaseAdapterMethod(BaseAdapterMethod):
    pass

python3 -m pytest tests/functional

import pytest
from dbt.tests.adapter.basic.files import seeds_base_csv, seeds_added_csv, seeds_newcolumns_csv
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols

**Examples:**

Example 1 (unknown):
```unknown
##### Define test cases[​](#define-test-cases "Direct link to Define test cases")

As in the example above, each test case is defined as a class, and has its own "project" setup. To get started, you can import all basic test cases and try running them without changes.

tests/functional/adapter/test\_basic.py
```

Example 2 (unknown):
```unknown
Finally, run pytest:
```

Example 3 (unknown):
```unknown
##### Modifying test cases[​](#modifying-test-cases "Direct link to Modifying test cases")

You may need to make slight modifications in a specific test case to get it passing on your adapter. The mechanism to do this is simple: rather than simply inheriting the "base" test with `pass`, you can redefine any of its fixtures or test methods.

For instance, on Redshift, we need to explicitly cast a column in the fixture input seed to use data type `varchar(64)`:

tests/functional/adapter/test\_basic.py
```

---

## Snowplow sessionization

**URL:** llms-txt#snowplow-sessionization

**Contents:**
  - About Hybrid projects Enterprise +
  - About Hybrid projects [Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - About Iceberg catalogs
  - About incremental models
  - About incremental strategy
  - About MetricFlow
  - About microbatch incremental models
  - About model governance
  - About state-aware orchestration Private previewEnterpriseEnterprise +
  - About state-aware orchestration [Private preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

Our organization uses this package of transformations to roll Snowplow events
up to page views and sessions.
{% enddocs %}

models:
  +incremental_strategy: "insert_overwrite"

{{
  config(
    materialized='incremental',
    unique_key='date_day',
    incremental_strategy='delete+insert',
    ...
  )
}}

{{
  config(
    materialized = 'incremental',
    unique_key = 'id',
    merge_update_columns = ['email', 'ip_address'],
    ...
  )
}}

{{
  config(
    materialized = 'incremental',
    unique_key = 'id',
    merge_exclude_columns = ['created_at'],
    ...
  )
}}

models:
  - name: my_incremental_model
    config:
      materialized: incremental
      unique_key: id
      # this will affect how the data is stored on disk, and indexed to limit scans
      cluster_by: ['session_start']  
      incremental_strategy: merge
      # this limits the scan of the existing table to the last 7 days of data
      incremental_predicates: ["DBT_INTERNAL_DEST.session_start > dateadd(day, -7, current_date)"]
      # `incremental_predicates` accepts a list of SQL statements. 
      # `DBT_INTERNAL_DEST` and `DBT_INTERNAL_SOURCE` are the standard aliases for the target table and temporary table, respectively, during an incremental run using the merge strategy.

-- in models/my_incremental_model.sql

{{
  config(
    materialized = 'incremental',
    unique_key = 'id',
    cluster_by = ['session_start'],  
    incremental_strategy = 'merge',
    incremental_predicates = [
      "DBT_INTERNAL_DEST.session_start > dateadd(day, -7, current_date)"
    ]
  )
}}

merge into <existing_table> DBT_INTERNAL_DEST
    from <temp_table_with_new_records> DBT_INTERNAL_SOURCE
    on
        -- unique key
        DBT_INTERNAL_DEST.id = DBT_INTERNAL_SOURCE.id
        and
        -- custom predicate: limits data scan in the "old" data / existing table
        DBT_INTERNAL_DEST.session_start > dateadd(day, -7, current_date)
    when matched then update ...
    when not matched then insert ...

with large_source_table as (

select * from {{ ref('large_source_table') }}
    {% if is_incremental() %}
        where session_start >= dateadd(day, -3, current_date)
    {% endif %}

{% macro get_incremental_append_sql(arg_dict) %}

{% do return(some_custom_macro_with_sql(arg_dict["target_relation"], arg_dict["temp_relation"], arg_dict["unique_key"], arg_dict["dest_columns"], arg_dict["incremental_predicates"])) %}

{% macro some_custom_macro_with_sql(target_relation, temp_relation, unique_key, dest_columns, incremental_predicates) %}

{%- set dest_cols_csv = get_quoted_csv(dest_columns | map(attribute="name")) -%}

insert into {{ target_relation }} ({{ dest_cols_csv }})
    (
        select {{ dest_cols_csv }}
        from {{ temp_relation }}
    )

{{ config(
    materialized="incremental",
    incremental_strategy="append",
) }}

select * from {{ ref("some_model") }}

{% macro get_incremental_insert_only_sql(arg_dict) %}

{% do return(some_custom_macro_with_sql(arg_dict["target_relation"], arg_dict["temp_relation"], arg_dict["unique_key"], arg_dict["dest_columns"], arg_dict["incremental_predicates"])) %}

{% macro some_custom_macro_with_sql(target_relation, temp_relation, unique_key, dest_columns, incremental_predicates) %}

{%- set dest_cols_csv = get_quoted_csv(dest_columns | map(attribute="name")) -%}

insert into {{ target_relation }} ({{ dest_cols_csv }})
    (
        select {{ dest_cols_csv }}
        from {{ temp_relation }}
    )

{{ config(
    materialized="incremental",
    incremental_strategy="insert_only",
    ...
) }}

{% macro get_incremental_merge_null_safe_sql(arg_dict) %}
    {% do return(example.get_incremental_merge_null_safe_sql(arg_dict)) %}
{% endmacro %}

select
    date_trunc('day',orders.ordered_at) as day, 
    case when customers.first_ordered_at is not null then true else false end as is_new_customer,
    sum(orders.order_total) as order_total
from
  orders
left join
  customers
on
  orders.customer_id = customers.customer_id
group by 1, 2

semantic_models:
  - name: orders    # The name of the semantic model
    description: |
      A model containing order data. The grain of the table is the order id.
    model: ref('orders') #The name of the dbt model and schema
    defaults:
      agg_time_dimension: metric_time
    entities: # Entities, which usually correspond to keys in the table. 
      - name: order_id
        type: primary
      - name: customer
        type: foreign
        expr: customer_id
    measures:   # Measures, which are the aggregations on the columns in the table.
      - name: order_total
        agg: sum
    dimensions: # Dimensions are either categorical or time. They add additional context to metrics and the typical querying pattern is Metric by Dimension.
      - name: metric_time
        expr: cast(ordered_at as date)
        type: time
        type_params:
          time_granularity: day
  - name: customers    # The name of the second semantic model
    description: >
      Customer dimension table. The grain of the table is one row per
        customer.
    model: ref('customers') #The name of the dbt model and schema
    defaults:
      agg_time_dimension: first_ordered_at
    entities: # Entities, which  usually correspond to keys in the table.
      - name: customer 
        type: primary
        expr: customer_id
    dimensions: # Dimensions are either categorical or time. They add additional context to metrics and the typical querying pattern is Metric by Dimension.
      - name: is_new_customer
        type: categorical
        expr: case when first_ordered_at is not null then true else false end
      - name: first_ordered_at
        type: time
        type_params:
          time_granularity: day

semantic_models:
  - name: orders
    description: |
      A model containing order data. The grain of the table is the order id.
    model: ref('orders')  #The name of the dbt model and schema
    defaults:
      agg_time_dimension: metric_time
    entities: # Entities, which usually correspond to keys in the table
      - name: order_id
        type: primary
      - name: customer
        type: foreign
        expr: customer_id
    measures: # Measures, which are the aggregations on the columns in the table.
      - name: order_total
        agg: sum
    dimensions: # Dimensions are either categorical or time. They add additional context to metrics and the typical querying pattern is Metric by Dimension.
      - name: metric_time
        expr: cast(ordered_at as date)
        type: time
        type_params:
          time_granularity: day
      - name: is_food_order
        type: categorical

select
    date_trunc('day',orders.ordered_at) as day, 
    sum(case when is_food_order = true then order_total else null end) as food_order,
    sum(orders.order_total) as sum_order_total,
    food_order/sum_order_total
from
  orders
left join
  customers
on
  orders.customer_id = customers.customer_id
where
  case when customers.first_ordered_at is not null then true else false end = true
group by 1

metrics:
  - name: food_order_pct_of_order_total_returning
    description: Revenue from food orders from returning customers
    label: "Food % of Order Total"
    type: ratio
    type_params:
      numerator: food_order
      denominator: order_total
    filter: |
      {{ Dimension('customer__is_new_customer') }} = false

models:
  - name: page_views
    config:
      event_time: page_view_start

{{ config(
    materialized='incremental',
    incremental_strategy='microbatch',
    event_time='session_start',
    begin='2020-01-01',
    batch_size='day'
) }}

-- this ref will be auto-filtered
    select * from {{ ref('page_views') }}

-- this ref won't
    select * from {{ ref('customers') }}

select
  page_views.id as session_id,
  page_views.page_view_start as session_start,
  customers.*
  from page_views
  left join customers
    on page_views.customer_id = customers.id

select * from (
        -- filtered on configured event_time
        select * from "analytics"."page_views"
        where page_view_start >= '2024-10-01 00:00:00'  -- Oct 1
        and page_view_start < '2024-10-02 00:00:00'
    )

select * from "analytics"."customers"

select * from (
        -- filtered on configured event_time
        select * from "analytics"."page_views"
        where page_view_start >= '2024-10-02 00:00:00'  -- Oct 2
        and page_view_start < '2024-10-03 00:00:00'
    )

select * from "analytics"."customers"

{{ config(
    materialized='incremental',
    incremental_strategy='microbatch',
    unique_key='sales_id', ## required for dbt-postgres
    event_time='transaction_date',
    begin='2023-01-01',
    batch_size='day'
) }}

select
    sales_id,
    transaction_date,
    customer_id,
    product_id,
    total_amount
from {{ source('sales', 'transactions') }}

dbt run --full-refresh --event-time-start "2024-01-01" --event-time-end "2024-02-01"

dbt run --full-refresh

dbt run --event-time-start "2024-09-01" --event-time-end "2024-09-04"

{{
    config(
        materialized='incremental',
        incremental_strategy='delete+insert',
        unique_key='date_day'
    )
}}

select * from {{ ref('stg_events') }}

{% if is_incremental() %}
        -- this filter will only be applied on an incremental run
        -- add a lookback window of 3 days to account for late-arriving records
        where date_day >= (select {{ dbt.dateadd("day", -3, "max(date_day)") }} from {{ this }})  
    {% endif %}

{{
    config(
        materialized='incremental',
        incremental_strategy='microbatch',
        event_time='event_occured_at',
        batch_size='day',
        lookback=3,
        begin='2020-01-01',
        full_refresh=false
    )
}}

select * from {{ ref('stg_events') }} -- this ref will be auto-filtered

models:
  - name: stg_events
    config:
      event_time: my_time_field

select * from (
    select * from "analytics"."stg_events"
    where my_time_field >= '2024-10-01 00:00:00'
      and my_time_field < '2024-10-02 00:00:00'
)

with
  orders as (select * from ref('orders')),
  customers as (select * from ref('customers')),
  joined as (
    select
      customers.customer_id as customer_id,
      orders.order_id as order_id
    from customers
    left join orders
      on orders.customer_id = customers.customer_id
  )
select * from joined

config:
    fail_calc: <string>
    limit: <integer>
    severity: error | warn
    error_if: <string>
    warn_if: <string>
    store_failures: true | false
    where: <string>
  
dbt run --empty

dbt run --select path/to/your_model --empty

dbt run --select path/to/stg_customers --sample="3 days"

dbt run --select path/to/stg_customers --sample="6 hours"

dbt run --sample="{'start': '2024-07-01', 'end': '2024-07-08 18:00:00'}"

select * from {{ ref('stg_customers').render() }}

orders as (
      select * from {{ ref('orders') }}
  ),

customers as (
      select * from {{ ref('customers') }}
  )

select 
      date_trunc('year', ordered_at) as order_year,
      count(distinct orders.customer_id) as unique_customers,
      count(distinct orders.location_id) as unique_cities,
      to_char(sum(orders.order_total), '999,999,999.00') as total_order_revenue
  from orders
  join customers
      on orders.customer_id = customers.customer_id
  group by 1
  order by 1
  
-- Refunds have a negative amount, so the total amount should always be >= 0.
-- Therefore return records where total_amount < 0 to make the test fail.
select
    order_id,
    sum(amount) as total_amount
from {{ ref('fct_payments') }}
group by 1
having total_amount < 0

data_tests:
  - name: assert_total_payment_amount_is_positive
    description: >
      Refunds have a negative amount, so the total amount should always be >= 0.
      Therefore return records where total amount < 0 to make the test fail.

{% test not_null(model, column_name) %}

select *
    from {{ model }}
    where {{ column_name }} is null

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: status
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ['placed', 'shipped', 'completed', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              arguments:
                to: ref('customers')
                field: id

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null

Found 3 models, 2 tests, 0 snapshots, 0 analyses, 130 macros, 0 operations, 0 seed files, 0 sources

17:31:05 | Concurrency: 1 threads (target='learn')
17:31:05 |
17:31:05 | 1 of 2 START test not_null_order_order_id..................... [RUN]
17:31:06 | 1 of 2 PASS not_null_order_order_id........................... [PASS in 0.99s]
17:31:06 | 2 of 2 START test unique_order_order_id....................... [RUN]
17:31:07 | 2 of 2 PASS unique_order_order_id............................. [PASS in 0.79s]
17:31:07 |
17:31:07 | Finished running 2 tests in 7.17s.

Completed successfully

Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2

select
        order_id

from analytics.orders
    where order_id is not null
    group by order_id
    having count(*) > 1

select
        {{ column_name }}

from {{ model }}
    where {{ column_name }} is not null
    group by {{ column_name }}
    having count(*) > 1

select *
from analytics.orders
where order_id is null

select *
from {{ model }}
where {{ column_name }} is null

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null

data_tests:
  +store_failures: true

dbt test --select customers

test-paths: ["my_cool_tests"]

dbt test --select "source:*"

$ dbt test --select source:jaffle_shop

$ dbt test --select source:jaffle_shop.orders

select
  country_code || '-' || order_id as surrogate_key,
  ...

models:
  - name: orders
    columns:
      - name: surrogate_key
        data_tests:
          - unique

models:
  - name: orders
    data_tests:
      - unique:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            column_name: "(country_code || '-' || order_id)"

models:
  - name: orders
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
            combination_of_columns:
              - country_code
              - order_id

- name: weekly_jaffle_metrics
    label: Jaffles by the Week
    type: dashboard
    maturity: high
    url: https://bi.tool/dashboards/1
    description: >
      Did someone say "exponential growth"?

depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
      - source('gsheets', 'goals')
      - metric('count_orders')

owner:
      name: Callum McData
      email: data@jaffleshop.com

dbt run -s +exposure:weekly_jaffle_report
dbt test -s +exposure:weekly_jaffle_report

model-paths: ["models", "groups"]
  
models:
  marts:
    finance:
      +group: finance

models:
  - name: model_name
    config:
      group: finance

{{ config(group = 'finance') }}

models:
  - name: finance_private_model
    config:
      access: private # changed to config in v1.10
      group: finance

# in a different group!
  - name: marketing_model
    config:
      group: marketing

select * from {{ ref('finance_private_model') }}

$ dbt run -s marketing_model
...
dbt.exceptions.DbtReferenceError: Parsing Error
  Node model.jaffle_shop.marketing_model attempted to reference node model.jaffle_shop.finance_private_model, 
  which is not allowed because the referenced node is private to the finance group.

country_code,country_name
US,United States
CA,Canada
GB,United Kingdom
...

Found 2 models, 3 tests, 0 archives, 0 analyses, 53 macros, 0 operations, 1 seed file

14:46:15 | Concurrency: 1 threads (target='dev')
14:46:15 |
14:46:15 | 1 of 1 START seed file analytics.country_codes........................... [RUN]
14:46:15 | 1 of 1 OK loaded seed file analytics.country_codes....................... [INSERT 3 in 0.01s]
14:46:16 |
14:46:16 | Finished running 1 seed in 0.14s.

Completed successfully

Done. PASS=1 ERROR=0 SKIP=0 TOTAL=1

-- This refers to the table created from seeds/country_codes.csv
select * from {{ ref('country_codes') }}

seed-paths: ["custom_seeds"]

$ dbt seed
Running with dbt=1.6.0-rc2
Found 0 models, 0 tests, 0 snapshots, 0 analyses, 130 macros, 0 operations, 1 seed file, 0 sources

12:12:27 | Concurrency: 8 threads (target='dev_snowflake')
12:12:27 |
12:12:27 | 1 of 1 START seed file dbt_claire.country_codes...................... [RUN]
12:12:30 | 1 of 1 ERROR loading seed file dbt_claire.country_codes.............. [ERROR in 2.78s]
12:12:31 |
12:12:31 | Finished running 1 seed in 10.05s.

Completed with 1 error and 0 warnings:

Database Error in seed country_codes (seeds/country_codes.csv)
  000904 (42000): SQL compilation error: error line 1 at position 62
  invalid identifier 'COUNTRY_NAME'

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

$ dbt seed
Running with dbt=1.6.0-rc2
Found 0 models, 0 tests, 0 snapshots, 0 analyses, 149 macros, 0 operations, 1 seed file, 0 sources

12:14:46 | Concurrency: 1 threads (target='dev_redshift')
12:14:46 |
12:14:46 | 1 of 1 START seed file dbt_claire.country_codes...................... [RUN]
12:14:46 | 1 of 1 ERROR loading seed file dbt_claire.country_codes.............. [ERROR in 0.23s]
12:14:46 |
12:14:46 | Finished running 1 seed in 1.75s.

Completed with 1 error and 0 warnings:

Database Error in seed country_codes (seeds/country_codes.csv)
  column "country_name" of relation "country_codes" does not exist

Done. PASS=0 WARN=0 ERROR=1 SKIP=0 TOTAL=1

dbt seed --full-refresh

seeds:
  - name: country_codes
    description: A mapping of two letter country codes to country names
    columns:
      - name: country_code
        data_tests:
          - unique
          - not_null
      - name: country_name
        data_tests:
          - unique
          - not_null

seeds:
  jaffle_shop: # you must include the project name
    warehouse_locations:
      +column_types:
        zipcode: varchar(5)

$ dbt run --select country_codes+

$ dbt seed --select country_codes

snapshots:
  - name: orders_snapshot
    relation: ref('stg_orders')
    config:
      schema: snapshots
      unique_key: order_id
      strategy: check
      check_cols:
        - status
        - is_cancelled
      updated_at: updated_at

$ dbt snapshot --select order_snapshot

snapshot-paths: ["snapshots"]

{% snapshot snappy %}
  {{ config(materialized = 'table', ...) }}
  ...
{% endsnapshot %}

A snapshot must have a materialized value of 'snapshot'

sources:
  - name: jaffle_shop
    database: raw  
    schema: jaffle_shop  
    tables:
      - name: orders
      - name: customers

- name: stripe
    tables:
      - name: payments

from {{ source('jaffle_shop', 'orders') }}

left join {{ source('jaffle_shop', 'customers') }} using (customer_id)

from raw.jaffle_shop.orders

left join raw.jaffle_shop.customers using (customer_id)

sources:
  - name: jaffle_shop
    description: This is a replica of the Postgres database used by our app
    tables:
      - name: orders
        database: raw
        description: >
          One record per order. Includes cancelled and deleted orders.
        columns:
          - name: id
            description: Primary key of the orders table
            data_tests:
              - unique
              - not_null
          - name: status
            description: Note that the status can change over time

sources:
  - name: jaffle_shop
    schema: postgres_backend_public_schema
    database: raw
    tables:
      - name: orders
        identifier: api_orders

select * from {{ source('jaffle_shop', 'orders') }}

select * from raw.postgres_backend_public_schema.api_orders

sources:
  - name: jaffle_shop
    database: raw
    tables:
      - name: orders
      - name: customers

sources:
  - name: jaffle_shop
    database: raw
    quoting:
      database: true
      schema: true
      identifier: true

tables:
      - name: order_items
      - name: orders
        # This overrides the `jaffle_shop` quoting config
        quoting:
          identifier: false

dbt test --select "source:*"

$ dbt test --select source:jaffle_shop

$ dbt test --select source:jaffle_shop.orders

$ dbt run --select source:jaffle_shop+

$ dbt run --select source:jaffle_shop.orders+

sources:
  - name: jaffle_shop
    database: raw
    config: 
      freshness: # default freshness
        # changed to config in v1.9
        warn_after: {count: 12, period: hour}
        error_after: {count: 24, period: hour}
      loaded_at_field: _etl_loaded_at # changed to config in v1.10

tables:
      - name: orders
        config:
          freshness: # make this a little more strict
            warn_after: {count: 6, period: hour}
            error_after: {count: 12, period: hour}

- name: customers # this inherits the default freshness defined in the jaffle_shop source block at the beginning

- name: product_skus
        config:
          freshness: null # do not check freshness for this table

$ dbt source freshness

select
  max(_etl_loaded_at) as max_loaded_at,
  convert_timezone('UTC', current_timestamp()) as calculated_at
from raw.jaffle_shop.orders

select
  max(_etl_loaded_at) as max_loaded_at,
  convert_timezone('UTC', current_timestamp()) as calculated_at
from raw.jaffle_shop.orders
where _etl_loaded_at >= date_sub(current_date(), interval 1 day)

sources:
  - name: jaffle_shop
    database: raw
    config: 
      freshness: # changed to config in v1.9
        warn_after: {count: 12, period: hour}
        error_after: {count: 24, period: hour}

loaded_at_field: _etl_loaded_at # changed to config in v1.10

tables:
      - name: orders
      - name: product_skus
        config:
          freshness: null # do not check freshness for this table

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About Hybrid projects Enterprise +

### About Hybrid projects [Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

With Hybrid projects, your organization can adopt complementary dbt Core and dbt workflows (where some teams deploy projects in dbt Core and others in dbt) and seamlessly integrate these workflows by automatically uploading dbt Core [artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts.md) into dbt.

Available in public preview

Hybrid projects is available in public preview to [dbt Enterprise accounts](https://www.getdbt.com/pricing).

dbt Core users can seamlessly upload [artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts.md) like [run results.json](https://docs.getdbt.com/reference/artifacts/run-results-json.md), [manifest.json](https://docs.getdbt.com/reference/artifacts/manifest-json.md), [catalog.json](https://docs.getdbt.com/reference/artifacts/catalog-json.md), [sources.json](https://docs.getdbt.com/reference/artifacts/sources-json.md), and so on — into dbt after executing a run in the dbt Core command line interface (CLI), which helps:

* Collaborate with dbt + dbt Core users by enabling them to visualize and perform [cross-project references](https://docs.getdbt.com/docs/mesh/govern/project-dependencies.md#how-to-write-cross-project-ref) to dbt models that live in Core projects.
* (Coming soon) New users interested in the [Canvas](https://docs.getdbt.com/docs/cloud/canvas.md) can build off of dbt models already created by a central data team in dbt Core rather than having to start from scratch.
* dbt Core and dbt users can navigate to [Catalog](https://docs.getdbt.com/docs/explore/explore-projects.md) and view their models and assets. To view Catalog, you must have a [read-only seat](https://docs.getdbt.com/docs/cloud/manage-access/seats-and-users.md).

#### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

To upload artifacts, make sure you meet these prerequisites:

* Your organization is on a [dbt Enterprise+ plan](https://www.getdbt.com/pricing)

* You're on [dbt's release tracks](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md) and your dbt Core project is on dbt v1.10 or higher

* [Configured](https://docs.getdbt.com/docs/deploy/hybrid-setup.md#connect-project-in-dbt-cloud) a hybrid project in dbt.

* Updated your existing dbt Core project with latest changes and [configured it with model access](https://docs.getdbt.com/docs/deploy/hybrid-setup.md#make-dbt-core-models-public):

  <!-- -->

  * Ensure models that you want to share with other dbt projects use `access: public` in their model configuration. This makes the models more discoverable and shareable
  * Learn more about [access modifier](https://docs.getdbt.com/docs/mesh/govern/model-access.md#access-modifiers) and how to set the [`access` config](https://docs.getdbt.com/reference/resource-configs/access.md)

* Update [dbt permissions](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions.md) to create a new project in dbt

**Note:** Uploading artifacts doesn't count against dbt run slots.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About Iceberg catalogs

Data catalogs have recently become at the top of the data industry's mind, especially given the excitement about Iceberg and data governance for AI. It has become an overused term that represents a broad set of tools. So, before we dive into Iceberg catalogs, let's start at the beginning:

#### About data catalogs[​](#about-data-catalogs "Direct link to About data catalogs")

The short answer is it’s **data about your data**.

A Data Catalog is a centralized metadata management layer that enables users and tools to discover, understand, and govern data effectively. At its core, it organizes metadata about datasets, including information about the schemas, lineage, access controls, and business context to help technical and non-technical users work with data more efficiently.

##### History of data catalogs[​](#history-of-data-catalogs "Direct link to History of data catalogs")

Data catalogs aren’t a new concept.

Data dictionaries were the earliest forms of catalogs, and they were part of relational databases. These dictionaries stored schema-level metadata (like table names). They weren’t made for business users and were very manual.

Fast forward to the early 2010s, and the industry began to delve deeply into [Hadoop](https://hadoop.apache.org/) and data lakes. [Hive Metastore](https://hive.apache.org/) became the standard for managing schema metadata in Hadoop ecosystems. However, it was still limited to structural metadata, as it lacked lineage, discovery, and business context metadata.

Next, there was the emergence of open source technical catalogs like [Iceberg](https://iceberg.apache.org/terms/), [Polaris](https://polaris.apache.org/), and [Unity Catalog](https://www.unitycatalog.io/), and business catalogs like [Atlan](https://atlan.com/what-is-a-data-catalog/). In the era of AI, it’s more important than ever to have catalogs that can support structural metadata and business logic.

For data teams, the catalogs can fall into two buckets:

* **Technical data catalogs:** Focus on structural metadata, including information about data like table and column names, data types, storage locations (particularly important for open table formats), and access controls. They usually come either “built-in” (no setup needed) or externally managed and integrated into your data platform. They are used by compute engines to locate and interact with data.

* **Business data catalogs:** Serve broader organizational users (BI analysts, product managers, etc.). They enrich technical metadata with business context in the form of metrics, business definitions, data quality indicators, usage patterns, and ownership.

##### Why data catalogs are important to dbt[​](#why-data-catalogs-are-important-to-dbt "Direct link to Why data catalogs are important to dbt")

For dbt users working in a lakehouse or multi-engine architecture, understanding and interacting with data catalogs is essential for several reasons, including:

* **Table Discovery:** dbt models are registered in catalogs. Understanding the catalog structure is critical for managing datasets and informing dbt about what has already been built and where it resides.

* **Cross-Engine Interoperability:** Iceberg catalogs allow datasets created by one compute engine to be read by another. This is what dbt Mesh’s cross-platform functionality is built on.

#### About Iceberg catalogs[​](#about-iceberg-catalogs "Direct link to About Iceberg catalogs")

Apache Iceberg is an open table format designed for petabyte-scale analytic datasets. It supports schema evolution, time travel, partition pruning, and transactional operations across distributed compute engines.

Iceberg catalogs are a critical abstraction layer that maps logical table names to their metadata locations and provides a namespace mechanism. They decouple compute engines from the physical layout of data, enabling multiple tools to interoperate consistently on the same dataset.

There are multiple types of Iceberg catalogs:

* Iceberg REST
* Iceberg REST compatible
* Delta/Iceberg Hybrid\*

Hybrid catalogs support storing duplicate table metadata in Iceberg and Delta Lake formats, enabling workflows like an Iceberg engine to read from Delta Lake or vice versa. There will be limitations specific to how the platform has implemented this.

##### How dbt works with Iceberg catalogs[​](#how-dbt-works-with-iceberg-catalogs "Direct link to How dbt works with Iceberg catalogs")

dbt interacts with Iceberg catalogs through the adapters in two ways:

* **Model Materialization:** When dbt materializes a model as a table or view, if the catalog integration is declared, the underlying adapter (Spark, Trino, Snowflake, etc.) creates an Iceberg table entry in the specified catalog, both built-in or external.

* **Catalog Integration**: With our initial release of the new catalog framework, users can declare which catalog the table's metadata is written to.

Why is this important? dbt uses and creates a significant amount of metadata. Before every run, dbt needs to know what already exists so it knows how to compile code (ex. resolving your `{{ref()}}` to the actual table name) and where to materialize the object. By supporting these two methods, dbt can cleverly adjust based on the environment, code logic, and use case defined in your dbt project.

##### Limitations[​](#limitations "Direct link to Limitations")

To ensure that your compute engine has access to the catalog, you must provide the networking and permissions are set up correctly. This means that if you are using X warehouse with Y catalog but want to read Y catalog from Z warehouse, you need to ensure that Z warehouse can connect to Y catalog. If IP restrictions are turned on, you must resolve this by removing restrictions on allowlisting (only possible if the warehouse supports static IP addresses) or setting something like Privatelink to support this.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About incremental models

This is an introduction on incremental models, when to use them, and how they work in dbt.

Incremental models in dbt is a [materialization](https://docs.getdbt.com/docs/build/materializations.md) strategy designed to efficiently update your data warehouse tables by only transforming and loading new or changed data since the last run. Instead of processing your entire dataset every time, incremental models append or update only the new rows, significantly reducing the time and resources required for your data transformations.

This page will provide you with a brief overview of incremental models, their importance in data transformations, and the core concepts of incremental materializations in dbt.

[![A visual representation of how incremental models work. Source: Materialization best practices guide (/best-practices/materializations/1-guide-overview)](/img/docs/building-a-dbt-project/incremental-diagram.jpg?v=2 "A visual representation of how incremental models work. Source: Materialization best practices guide (/best-practices/materializations/1-guide-overview)")](#)A visual representation of how incremental models work. Source: Materialization best practices guide (/best-practices/materializations/1-guide-overview)

<!-- -->

Learn by video!

For video tutorials on

<!-- -->

Incremental models

<!-- -->

, go to dbt Learn and check out the [Incremental models](https://learn.getdbt.com/courses/incremental-models)

<!-- -->

[ course](https://learn.getdbt.com/courses/incremental-models).

#### Understand incremental models[​](#understand-incremental-models "Direct link to Understand incremental models")

Incremental models enable you to significantly reduce the build time by just transforming new records. This is particularly useful for large datasets, where the cost of processing the entire dataset is high.

Incremental models [require extra configuration](https://docs.getdbt.com/docs/build/incremental-models.md) and are an advanced usage of dbt. We recommend using them when your dbt runs are becoming too slow.

##### When to use an incremental model[​](#when-to-use-an-incremental-model "Direct link to When to use an incremental model")

Building models as tables in your data warehouse is often preferred for better query performance. However, using `table` materialization can be computationally intensive, especially when:

* Source data has millions or billions of rows.
* Data transformations on the source data are computationally expensive (take a long time to execute) and complex, like when using Regex or UDFs.

Incremental models offer a balance between complexity and improved performance compared to `view` and `table` materializations and offer better performance of your dbt runs.

In addition to these considerations for incremental models, it's important to understand their limitations and challenges, particularly with large datasets. For more insights into efficient strategies, performance considerations, and the handling of late-arriving data in incremental models, refer to the [On the Limits of Incrementality](https://discourse.getdbt.com/t/on-the-limits-of-incrementality/303) discourse discussion or to our [Materialization best practices](https://docs.getdbt.com/best-practices/materializations/2-available-materializations.md) page.

##### How incremental models work in dbt[​](#how-incremental-models-work-in-dbt "Direct link to How incremental models work in dbt")

dbt's [incremental materialization strategy](https://docs.getdbt.com/docs/build/incremental-strategy.md) works differently on different databases. Where supported, a `merge` statement is used to insert new records and update existing records.

On warehouses that do not support `merge` statements, a merge is implemented by first using a `delete` statement to delete records in the target table that are to be updated, and then an `insert` statement.

Transaction management, a process used in certain data platforms, ensures that a set of actions is treated as a single unit of work (or task). If any part of the unit of work fails, dbt will roll back open transactions and restore the database to a good state.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Incremental models](https://docs.getdbt.com/docs/build/incremental-models.md) to learn how to configure incremental models in dbt.
* [Incremental strategies](https://docs.getdbt.com/docs/build/incremental-strategy.md) to understand how dbt implements incremental models on different databases.
* [Microbatch](https://docs.getdbt.com/docs/build/incremental-microbatch.md) to understand a new incremental strategy intended for efficient and resilient processing of very large time-series datasets.
* [Materializations best practices](https://docs.getdbt.com/best-practices/materializations/1-guide-overview.md) to learn about the best practices for using materializations in dbt.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About incremental strategy

Incremental strategies for materializations optimize performance by defining how to handle new and changed data.

There are various strategies to implement the concept of incremental materializations. The value of each strategy depends on:

* The volume of data.
* The reliability of your `unique_key`.
* The support of certain features in your data platform.

An optional `incremental_strategy` config is provided in some adapters that controls the code that dbt uses to build incremental models.

Microbatch

The [`microbatch` incremental strategy](https://docs.getdbt.com/docs/build/incremental-microbatch.md) is intended for large time-series datasets. dbt will process the incremental model in multiple queries (or "batches") based on a configured `event_time` column. Depending on the volume and nature of your data, this can be more efficient and resilient than using a single query for adding new data.

##### Supported incremental strategies by adapter[​](#supported-incremental-strategies-by-adapter "Direct link to Supported incremental strategies by adapter")

This table shows the support of each incremental strategy across adapters available on dbt's [Latest release track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md). Some strategies may be unavailable if you're not on "Latest" and the feature hasn't been released to the "Compatible" track.

If you're interested in an adapter available in dbt Core only, check out the [adapter's individual configuration page](https://docs.getdbt.com/reference/resource-configs/resource-configs.md) for more details.

Click the name of the adapter in the following table for more information about supported incremental strategies:

| Data platform adapter                                                                                                                     | `append` | `merge` | `delete+insert` | `insert_overwrite` | `microbatch` |
| ----------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------- | --------------- | ------------------ | ------------ |
| [dbt-postgres](https://docs.getdbt.com/reference/resource-configs/postgres-configs.md#incremental-materialization-strategies)             | ✅       | ✅      | ✅              |                    | ✅           |
| [dbt-redshift](https://docs.getdbt.com/reference/resource-configs/redshift-configs.md#incremental-materialization-strategies)             | ✅       | ✅      | ✅              |                    | ✅           |
| [dbt-bigquery](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md#merge-behavior-incremental-models)                  |          | ✅      |                 | ✅                 | ✅           |
| [dbt-spark](https://docs.getdbt.com/reference/resource-configs/spark-configs.md#incremental-models)                                       | ✅       | ✅      |                 | ✅                 | ✅           |
| [dbt-databricks](https://docs.getdbt.com/reference/resource-configs/databricks-configs.md#incremental-models)                             | ✅       | ✅      |                 | ✅                 | ✅           |
| [dbt-snowflake](https://docs.getdbt.com/reference/resource-configs/snowflake-configs.md#merge-behavior-incremental-models)                | ✅       | ✅      | ✅              | ✅                 | ✅           |
| [dbt-trino](https://docs.getdbt.com/reference/resource-configs/trino-configs.md#incremental)                                              | ✅       | ✅      | ✅              |                    | ✅           |
| [dbt-fabric](https://docs.getdbt.com/reference/resource-configs/fabric-configs.md#incremental)                                            | ✅       |         | ✅              |                    |              |
| [dbt-athena](https://docs.getdbt.com/reference/resource-configs/athena-configs.md#incremental-models)                                     | ✅       | ✅      |                 | ✅                 | ✅           |
| [dbt-teradata](https://docs.getdbt.com/reference/resource-configs/teradata-configs.md#valid_history-incremental-materialization-strategy) | ✅       | ✅      | ✅              |                    | ✅           |

##### Configuring incremental strategy[​](#configuring-incremental-strategy "Direct link to Configuring incremental strategy")

The `incremental_strategy` config can either be defined in specific models or for all models in your `dbt_project.yml` file:

dbt\_project.yml
```

Example 2 (unknown):
```unknown
or:

models/my\_model.sql
```

Example 3 (unknown):
```unknown
##### Strategy-specific configs[​](#strategy-specific-configs "Direct link to Strategy-specific configs")

If you use the `merge` strategy and specify a `unique_key`, by default, dbt will entirely overwrite matched rows with new values.

On adapters which support the `merge` strategy, you may optionally pass a list of column names to a `merge_update_columns` config. In that case, dbt will update *only* the columns specified by the config, and keep the previous values of other columns.

models/my\_model.sql
```

Example 4 (unknown):
```unknown
Alternatively, you can specify a list of columns to exclude from being updated by passing a list of column names to a `merge_exclude_columns` config.

models/my\_model.sql
```

---

## set this environment variable to 'True' (bash syntax)

**URL:** llms-txt#set-this-environment-variable-to-'true'-(bash-syntax)

**Contents:**
  - Project Parsing
  - Putting it together
  - query-comment
  - quote_columns
  - Record timing info
  - Redshift configurations
  - Redshift permissions
  - require-dbt-version

export DBT_FAIL_FAST=1
dbt run

dbt run --fail-fast # set to True for this specific invocation
dbt run --no-fail-fast # set to False

python -c "from yaml import CLoader"

dbt run --select "my_package.*+"      # select all models in my_package and their children
dbt run --select "+some_model+"       # select some_model and all parents and children

dbt run --select "tag:nightly+"      # select "nightly" models and all children
dbt run --select "+tag:nightly+"      # select "nightly" models and all parents and children

dbt run --select "@source:snowplow"   # build all models that select from snowplow sources, plus their parents

dbt test --select "config.incremental_strategy:insert_overwrite,test_name:unique"   # execute all `unique` tests that select from models using the `insert_overwrite` incremental strategy

dbt run --select "@source:snowplow,tag:nightly models/export" --exclude "package:snowplow,config.materialized:incremental export_performance_timing"

query-comment: string

models:
  my_dbt_project:
    +materialized: table

query-comment:
  comment: string
  append: true | false
  job-label: true | false  # BigQuery only

/* {"app": "dbt", "dbt_version": "1.10.0rc2", "profile_name": "debug",
      "target_name": "dev", "node_id": "model.dbt2.my_model"} */

create view analytics.analytics.orders as (
      select ...
    );
  
query-comment: "executed by dbt"

/* executed by dbt */

query-comment: "run by {{ target.user }} in dbt"

/* run by drew in dbt */

query-comment:
  append: True

select ...
/* {"app": "dbt", "dbt_version": "1.6.0rc2", "profile_name": "debug", "target_name": "dev", "node_id": "model.dbt2.my_model"} */
;

query-comment:
  job-label: True

query-comment:
  comment: "run by {{ target.user }} in dbt"
  append: True

select ...
/* run by drew in dbt */
;

{% macro query_comment() %}

dbt {{ dbt_version }}: running {{ node.unique_id }} for target {{ target.name }}

query-comment: "{{ query_comment() }}"

{% macro query_comment(node) %}
    {%- set comment_dict = {} -%}
    {%- do comment_dict.update(
        app='dbt',
        dbt_version=dbt_version,
        profile_name=target.get('profile_name'),
        target_name=target.get('target_name'),
    ) -%}
    {%- if node is not none -%}
      {%- do comment_dict.update(
        file=node.original_file_path,
        node_id=node.unique_id,
        node_name=node.name,
        resource_type=node.resource_type,
        package_name=node.package_name,
        relation={
            "database": node.database,
            "schema": node.schema,
            "identifier": node.identifier
        }
      ) -%}
    {% else %}
      {%- do comment_dict.update(node_id='internal') -%}
    {%- endif -%}
    {% do return(tojson(comment_dict)) %}
{% endmacro %}

query-comment: "{{ query_comment(node) }}"

seeds:
  +quote_columns: true

seeds:
  jaffle_shop:
    mappings:
      +quote_columns: true

seeds:
  - name: mappings
    config:
      quote_columns: true

$ dbt run -r timing.txt
...

$ snakeviz timing.txt

python -m pip install py-spy
sudo py-spy record -s -f speedscope -- dbt parse

-- Example with one sort key
{{ config(materialized='table', sort='reporting_day', dist='unique_id') }}

-- Example with multiple sort keys
{{ config(materialized='table', sort=['category', 'region', 'reporting_day'], dist='received_at') }}

-- Example with interleaved sort keys
{{ config(materialized='table',
          sort_type='interleaved'
          sort=['category', 'region', 'reporting_day'],
          dist='unique_id')
}}

{{ config(materialized='view', bind=False) }}

select *
from source.data

models:
  +bind: false # Materialize all views as late-binding
  project_name:
    ....

models:
  <resource-path>:
    +materialized: materialized_view
    +on_configuration_change: apply | continue | fail
    +dist: all | auto | even | <field-name>
    +sort: <field-name> | [<field-name>]
    +sort_type: auto | compound | interleaved
    +auto_refresh: true | false
    +backup: true | false

models:
  - name: [<model-name>]
    config:
      materialized: materialized_view
      on_configuration_change: apply | continue | fail
      dist: all | auto | even | <field-name>
      sort: <field-name> | [<field-name>]
      sort_type: auto | compound | interleaved
      auto_refresh: true | false
      backup: true | false

{{ config(
    materialized="materialized_view",
    on_configuration_change="apply" | "continue" | "fail",
    dist="all" | "auto" | "even" | "<field-name>",
    sort=["<field-name>"],
    sort_type="auto" | "compound" | "interleaved",
    auto_refresh=true | false,
    backup=true | false,
) }}

grant create schema on database database_name to user_name;
grant usage on schema database.schema_name to user_name;
grant create table on schema database.schema_name to user_name;
grant create view on schema database.schema_name to user_name;
grant usage for schemas in database database_name to role role_name;
grant select on all tables in database database_name to user_name;
grant select on all views in database database_name to user_name;

require-dbt-version: version-range | [version-range]

{% macro a_few_days_in_september() %}

{% if not dbt.get('date_spine') %}
      {{ exceptions.raise_compiler_error("Expected to find the dbt.date_spine macro, but it could not be found") }}
    {% endif %}

{{ date_spine("day", "cast('2020-01-01' as date)", "cast('2030-12-31' as date)") }}

**Examples:**

Example 1 (unknown):
```unknown

```

Example 2 (unknown):
```unknown
There are two categories of exceptions:

1. **Flags setting file paths:** Flags for file paths that are relevant to runtime execution (for example, `--log-path` or `--state`) cannot be set in `dbt_project.yml`. To override defaults, pass CLI options or set environment variables (`DBT_LOG_PATH`, `DBT_STATE`). Flags that tell dbt where to find project resources (for example, `model-paths`) are set in `dbt_project.yml`, but as a top-level key, outside the `flags` dictionary; these configs are expected to be fully static and never vary based on the command or execution environment.
2. **Opt-in flags:** Flags opting in or out of [behavior changes](https://docs.getdbt.com/reference/global-configs/behavior-changes.md) can *only* be defined in `dbt_project.yml`. These are intended to be set in version control and migrated via pull/merge request. Their values should not diverge indefinitely across invocations, environments, or users.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Project Parsing

#### Related documentation[​](#related-documentation "Direct link to Related documentation")

* The `dbt parse` [command](https://docs.getdbt.com/reference/commands/parse.md)
* Partial parsing [profile config](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml.md#partial_parse) and [CLI flags](https://docs.getdbt.com/reference/global-configs/parsing.md)
* Parsing [CLI flags](https://docs.getdbt.com/reference/global-configs/parsing.md)

#### What is parsing?[​](#what-is-parsing "Direct link to What is parsing?")

At the start of every dbt invocation, dbt reads all the files in your project, extracts information, and constructs a manifest containing every object (model, source, macro, etc). Among other things, dbt uses the `ref()`, `source()`, and `config()` macro calls within models to set properties, infer dependencies, and construct your project's DAG.

Parsing projects can be slow, especially as projects get bigger—hundreds of models, thousands of files—which is frustrating in development. There are a handful of ways to optimize dbt performance today:

* LibYAML bindings for PyYAML
* Partial parsing, which avoids re-parsing unchanged files between invocations
* A static parser, which extracts information from simple models much more quickly
* [RPC server](https://docs.getdbt.com/reference/commands/rpc.md), which keeps a manifest in memory, and re-parses the project at server startup/hangup

These optimizations can be used in combination to reduce parse time from minutes to seconds. At the same time, each has some known limitations, so they are disabled by default.

#### PyYAML + LibYAML[​](#pyyaml--libyaml "Direct link to PyYAML + LibYAML")

dbt uses [PyYAML](https://pyyaml.org/wiki/PyYAML) to read and validate YAML files in your project. PyYAML is written in pure Python, but it can leverage [LibYAML](https://pyyaml.org/wiki/LibYAML) (written in C, much faster) if it's available in your system. Whenever it parses your project, dbt will always check first to see if LibYAML is available.

You can test to see if LibYAML is installed by running this command in the environment where you've installed dbt:
```

Example 3 (unknown):
```unknown
#### Partial parsing[​](#partial-parsing "Direct link to Partial parsing")

After parsing your project, dbt stores an internal project manifest in a file called `partial_parse.msgpack`. When partial parsing is enabled, dbt will use that internal manifest to determine which files have been changed (if any) since it last parsed the project. Then, it will *only* parse the changed files, or files related to those changes.

Starting in v1.0, partial parsing is **on** by default. In development, partial parsing can significantly reduce the time spent waiting at the start of a run, which translates to faster dev cycles and iteration.

The [`PARTIAL_PARSE` global config](https://docs.getdbt.com/reference/global-configs/parsing.md) can be enabled or disabled via `profiles.yml`, environment variable, or CLI flag.

##### Known limitations[​](#known-limitations "Direct link to Known limitations")

Parse-time attributes (dependencies, configs, and resource properties) are resolved using the parse-time context. When partial parsing is enabled, and certain context variables change, those attributes will *not* be re-resolved, and are likely to become stale.

In particular, you may see incorrect results if these attributes depend on "volatile" context variables, such as [`run_started_at`](https://docs.getdbt.com/reference/dbt-jinja-functions/run_started_at.md), [`invocation_id`](https://docs.getdbt.com/reference/dbt-jinja-functions/invocation_id.md), or [flags](https://docs.getdbt.com/reference/dbt-jinja-functions/flags.md). These variables are likely (or even guaranteed!) to change in each invocation. dbt Labs *strongly discourages* you from using these variables to set parse-time attributes (dependencies, configs, and resource properties).

Starting in v1.0, dbt *will* detect changes in environment variables. It will selectively re-parse only the files that depend on that [`env_var`](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var.md) value. (If the env var is used in `profiles.yml` or `dbt_project.yml`, a full re-parse is needed.) However, dbt will *not* re-render **descriptions** that include env vars. If your descriptions include frequently changing env vars (this is highly uncommon), we recommend that you fully re-parse when generating documentation: `dbt docs generate --no-partial-parse`.

If certain inputs change between runs, dbt will trigger a full re-parse. The results will be correct, but the full re-parse may be quite slow. Today those inputs are:

* `--vars`
* `profiles.yml` content (or `env_var` values used within)
* `dbt_project.yml` content (or `env_var` values used within)
* installed packages
* dbt version
* certain widely-used macros (for example, [builtins](https://docs.getdbt.com/reference/dbt-jinja-functions/builtins.md), overrides, or `generate_x_name` for `database`/`schema`/`alias`)

If you're triggering [CI](https://docs.getdbt.com/docs/deploy/continuous-integration.md) job runs, the benefits of partial parsing are not applicable to new pull requests (PR) or new branches. However, they are applied on subsequent commits to the new PR or branch.

When partial parsing is enabled, dbt may occasionally fail or incorrectly parse the project causing:

* Nodes (for example, models, sources) to not be found.
* Configurations to be set incorrectly (for example, different from what is defined in a model's `schema.yml` file).

If you get into this state, you can trigger a full re-parse using any of the following options:

* Run the dbt command with `--no-partial-parse`.
* Delete the `target/partial_parse.msgpack` file by running `dbt clean`.

You can disable partial parsing entirely by setting the `PARTIAL_PARSE` global config to `false`.

#### Static parser[​](#static-parser "Direct link to Static parser")

At parse time, dbt needs to extract the contents of `ref()`, `source()`, and `config()` from all models in the project. Traditionally, dbt has extracted those values by rendering the Jinja in every model file, which can be slow. We statically analyze model files leveraging [`tree-sitter`](https://github.com/tree-sitter/tree-sitter). You can see the code for an initial Jinja2 grammar [here](https://github.com/dbt-labs/tree-sitter-jinja2).

The static parser is **on** by default. We believe it can offer *some* speed up to 95% of projects. You may optionally turn it off using the [`STATIC_PARSER` global config](https://docs.getdbt.com/reference/global-configs/parsing.md).

For now, the static parser only works with models, and models whose Jinja is limited to those three special macros (`ref`, `source`, `config`). The static parser is at least 3x faster than a full Jinja render. Based on testing with data from dbt, we believe the current grammar can statically parse 60% of models in the wild. So for the average project, we'd hope to see a 40% speedup in the model parser.

#### Experimental parser[​](#experimental-parser "Direct link to Experimental parser")

Not currently in use.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Putting it together
```

Example 4 (unknown):
```unknown
This can get complex! Let's say I want a nightly run of models that build off snowplow data and feed exports, while *excluding* the biggest incremental models (and one other model, to boot).
```

---

## clone all of my models from specified state to my target schema(s)

**URL:** llms-txt#clone-all-of-my-models-from-specified-state-to-my-target-schema(s)

dbt clone --state path/to/artifacts

---

## Define second query variables

**URL:** llms-txt#define-second-query-variables

variables_query_two = {
    "environmentId": *[ENVR_ID_HERE]*
    "lastRunCount": 10,
    "uniqueId": longest_running_model
}

---

## dbt Core users

**URL:** llms-txt#dbt-core-users

**Contents:**
  - Discover data with Catalog
  - Enhance your code
  - Enhance your models
  - Entities
  - Environment variables
  - Explore multiple projects
  - Explore your data
  - External metadata ingestion EnterpriseEnterprise + Preview
  - External metadata ingestion [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing") [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - Fill null values for metrics

mf query --metrics transactions --group-by metric_time__month,sales_person__tier --order-by metric_time__month,sales_person__tier

employee_id (primary key)
first_name
last_name

student_id (primary key)
email (unique key)
first_name
last_name

customer_id (primary key)
customer_name

order_id (primary key)
order_date
customer_id (foreign key)

entities:
  - name: brand_target_key # Entity name or identified.
    type: foreign # This can be any entity type key. 
    expr: date_key || '|' || brand_code # Defines the expression for linking fields to form the surrogate key.

date_id (primary key)
date_day (unique key)
fiscal_year_name

order_id (primary key)
ordered_at
delivered_at
order_total

semantic_models:
- name: date_categories
  description: A date dimension table providing fiscal time attributes for analysis.
  model: ref('date_categories')
  entities:
  - name: date_id
    type: primary

- name: ordered_at_entity
    type: unique
    expr: date_day

- name: delivered_at_entity
    type: unique
    expr: date_day

dimensions:
  - name: date_day
    type: time
    type_params:
      time_granularity: day

- name: fiscal_year_name
    description: Formatted fiscal year string (for example, 'FY2025')
    type: categorical

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: ordered_at
    description: |
      Order fact table. This table is at the order grain with one row per order.
    model: ref('orders')
    entities:
      - name: order_id
        type: primary

- name: ordered_at_entity
        type: foreign
        expr: ordered_at

- name: delivered_at_entity
        type: foreign
        expr: delivered_at

dimensions:
      - name: ordered_at
        expr: ordered_at
        type: time
        type_params:
          time_granularity: day

measures:
      - name: order_total
        description: Total amount for each order including taxes.
        agg: sum
        create_metric: True

{{ config(materialized='incremental', unique_key='user_id') }}

with users_aggregated as (

select
        user_id,
        min(event_time) as first_event_time,
        max(event_time) as last_event_time,
        count(*) as count_total_events

from {{ ref('users') }}
    group by 1

select *,
    -- Inject the run id if present, otherwise use "manual"
    '{{ env_var("DBT_CLOUD_RUN_ID", "manual") }}' as _audit_run_id

from users_aggregated

CREATE OR REPLACE ROLE dbt_metadata_role;

GRANT USAGE ON WAREHOUSE "<your-warehouse>" TO ROLE dbt_metadata_role;

CREATE USER dbt_metadata_user
  DISPLAY_NAME = 'dbt Metadata Integration'
  PASSWORD = 'our-password>'
  DEFAULT_ROLE = dbt_metadata_role
  TYPE = 'LEGACY_SERVICE'
  DEFAULT_WAREHOUSE = '<your-warehouse>';

GRANT ROLE dbt_metadata_role TO USER dbt_metadata_user;

SET db_var = '"<your-database>"';

-- Grant access to view the database and its schemas
GRANT USAGE ON DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT USAGE ON ALL SCHEMAS IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT USAGE ON FUTURE SCHEMAS IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;

-- Grant REFERENCES to enable lineage and dependency analysis
GRANT REFERENCES ON ALL TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT REFERENCES ON FUTURE TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT REFERENCES ON ALL EXTERNAL TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT REFERENCES ON FUTURE EXTERNAL TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT REFERENCES ON ALL VIEWS IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT REFERENCES ON FUTURE VIEWS IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;

-- Recommended grant SELECT for privileges to enable metadata introspection and profiling
GRANT SELECT ON ALL TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON FUTURE TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON ALL EXTERNAL TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON FUTURE EXTERNAL TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON ALL VIEWS IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON FUTURE VIEWS IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON ALL DYNAMIC TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT SELECT ON FUTURE DYNAMIC TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;

-- Grant MONITOR on dynamic tables (e.g., for freshness or status checks)
GRANT MONITOR ON ALL DYNAMIC TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;
GRANT MONITOR ON FUTURE DYNAMIC TABLES IN DATABASE IDENTIFIER($db_var) TO ROLE dbt_metadata_role;

GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE dbt_metadata_role;

metrics:
  - name: website_visits
    type: simple
    type_params:
      measure:
        name: bookings
  - name: leads
    type: simple
    type_params:
      measure:
        name: bookings
        fill_nulls_with: 0 # This fills null values with zero
  - name: leads_to_website_visit
    type: derived
    type_params:
      expr: leads/website_visits
      metrics:
        - name: leads
        - name: website_visits

- name: leads
  type: simple
  type_params:
    measure:
      name: bookings
      fill_nulls_with: 0
      join_to_timespine: true

{{ config(
    post_hook=[
      "alter table {{ this }} ..."
    ]
) }}

{{ config(
    pre_hook=[
      "{{ some_macro() }}"
    ]
) }}

models:
  - name: <model_name>
    config:
      pre_hook:
        - "{{ some_macro() }}"

models:
  <project_name>:
    +pre-hook:
      - "{{ some_macro() }}"

{% macro grant_select(role) %}
{% set sql %}
    grant usage on schema {{ target.schema }} to role {{ role }};
    grant select on all tables in schema {{ target.schema }} to role {{ role }};
    grant select on all views in schema {{ target.schema }} to role {{ role }};
{% endset %}

{% do run_query(sql) %}
{% do log("Privileges granted", info=True) %}
{% endmacro %}

$ dbt run-operation grant_select --args '{role: reporter}'
Running with dbt=1.6.0
Privileges granted

models:
     define_public_models: # This is my project name, remember it must be specified
       marts:
         +access: public
   
      Core:
      - installed: 1.10.0-b1
      - latest:    1.9.3     - Ahead of latest version!
   
   export DBT_CLOUD_ACCOUNT_ID=your_account_id
   export DBT_CLOUD_ENVIRONMENT_ID=your_environment_id
   export DBT_CLOUD_TOKEN=your_token
   export DBT_UPLOAD_TO_ARTIFACTS_INGEST_API=True
   
   name: "jaffle_shop"
   version: "3.0.0"
   require-dbt-version: ">=1.5.0"
   ....rest of dbt_project.yml configuration...

dbt-cloud:
     tenant_hostname: cloud.getdbt.com # Replace with your Tenant URL
   
    dbt run
   
    DBT_CLOUD_ACCOUNT_ID=1 DBT_CLOUD_ENVIRONMENT_ID=123 dbt run
   
dbt init --fusion-upgrade

mkdir ~/.dbt # macOS
mkdir %USERPROFILE%\.dbt # Windows

mv ~/Downloads/dbt_cloud.yml ~/.dbt/dbt_cloud.yml

move %USERPROFILE%\Downloads\dbt_cloud.yml %USERPROFILE%\.dbt\dbt_cloud.yml

dbt-cloud:
project-id: 12345 # Required

claude mcp add dbt -- uvx --env-file <path-to-.env-file> dbt-mcp

claude mcp add dbt -s project -- uvx --env-file <path-to-.env-file> dbt-mcp

{
     "mcpServers": {
       "dbt-mcp": {
        "command": "uvx",
        "args": [
          "--env-file",
           "<environment_variable_file.env",
           "dbt-mcp"
         ]
       }
     }
   }
   
   {
     "mcpServers": {
       "dbt": {
         "command": "uvx",
         "args": [
           "dbt-mcp"
         ],
         "env": {
           "DBT_HOST": "https://<your-dbt-host-with-custom-subdomain>",
           "DBT_PROJECT_DIR": "/path/to/project",
           "DBT_PATH": "path/to/dbt/executable"
         }
       }
     }
   }
   
   {
     "mcpServers": {
       "dbt": {
         "command": "uvx",
         "args": [
           "dbt-mcp"
         ],
         "env": {
           "DBT_HOST": "https://<your-dbt-host-with-custom-subdomain>",
           "DISABLE_DBT_CLI": "true"
         }
       }
     }
   }
   
   {
     "servers": {
       "dbt": {
       "command": "uvx",
         "args": [
           "--env-file",
           "<path-to-.env-file>",
           "dbt-mcp"
         ]
       }
     }
   }
   
   {
     "servers": {
       "dbt": {
         "url": "https://<host>/api/ai/v1/mcp/",
         "headers": {
           "Authorization": "token <token>",
           "x-dbt-prod-environment-id": "<prod-id>"
         }
       }
     }
   }
   
   {
     "mcpServers": {
       "dbt": {
         "command": "uvx",
         "args": [
           "dbt-mcp"
         ],
         "env": {
           "DBT_HOST": "https://<your-dbt-host-with-custom-subdomain>",
           "DBT_PROJECT_DIR": "/path/to/project",
           "DBT_PATH": "path/to/dbt/executable"
         }
       }
     }
   }
   
   {
     "mcpServers": {
       "dbt": {
         "command": "uvx",
         "args": [
           "dbt-mcp"
         ],
         "env": {
           "DBT_HOST": "https://<your-dbt-host-with-custom-subdomain>",
           "DISABLE_DBT_CLI": "true"
         }
       }
     }
   }
   
{% set payment_methods = ["bank_transfer", "credit_card", "gift_card"] %}

select
    order_id,
    {% for payment_method in payment_methods %}
    sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount,
    {% endfor %}
    sum(amount) as total_amount
from app_data.payments
group by 1

select
    order_id,
    sum(case when payment_method = 'bank_transfer' then amount end) as bank_transfer_amount,
    sum(case when payment_method = 'credit_card' then amount end) as credit_card_amount,
    sum(case when payment_method = 'gift_card' then amount end) as gift_card_amount,
    sum(amount) as total_amount
from app_data.payments
group by 1

{% macro cents_to_dollars(column_name, scale=2) %}
    ({{ column_name }} / 100)::numeric(16, {{ scale }})
{% endmacro %}

select
  id as payment_id,
  {{ cents_to_dollars('amount') }} as amount_usd,
  ...
from app_data.payments

select
  id as payment_id,
  (amount / 100)::numeric(16, 2) as amount_usd,
  ...
from app_data.payments

select
  field_1,
  field_2,
  field_3,
  field_4,
  field_5,
  count(*)
from my_table
{{ dbt_utils.dimensions(5) }}

{{ cents_to_dollars('amount') }} as amount_usd

macros:
  - name: cents_to_dollars
    description: A macro to convert cents to dollars
    arguments:
      - name: column_name
        type: column
        description: The name of the column you want to convert
      - name: precision
        type: integer
        description: Number of decimal places. Defaults to 2.

materialization_{materialization_name}_{adapter}

macros:
  - name: materialization_my_materialization_name_default
    description: A custom materialization to insert records into an append-only table and track when they were added.
  - name: materialization_my_materialization_name_xyz
    description: A custom materialization to insert records into an append-only table and track when they were added.

$ dbt run
Running with dbt=1.7.0
Found 1 model, 0 tests, 0 snapshots, 0 analyses, 138 macros, 0 operations, 0 seed files, 0 sources

-- 🙅 This works, but can be hard to maintain as your code grows
{% for payment_method in ["bank_transfer", "credit_card", "gift_card"] %}
...
{% endfor %}

-- ✅ This is our preferred method of setting variables
{% set payment_methods = ["bank_transfer", "credit_card", "gift_card"] %}

{% for payment_method in payment_methods %}
...
{% endfor %}

--select state:modified --exclude fct_orders
  
     --select state modified --exclude tag:tagname_a tag:tagname_b
  
  --select state:modified+1
  
semantic_models:
  - name: transactions
    entities:
      - name: id
        type: primary
      - name: user
        type: foreign
        expr: user_id
    measures:
      - name: average_purchase_price
        agg: avg
        expr: purchase_price
  - name: user_signup
    entities:
      - name: user
        type: primary
        expr: user_id
    dimensions:
      - name: type
        type: categorical

dbt sl query --metrics average_purchase_price --group-by metric_time,user_id__type # In <Constant name="cloud" />

mf query --metrics average_purchase_price --group-by metric_time,user_id__type # In <Constant name="core" />

select
  transactions.user_id,
  transactions.purchase_price,
  user_signup.type
from transactions
left outer join user_signup
  on transactions.user_id = user_signup.user_id
where transactions.purchase_price is not null
group by
  transactions.user_id,
  user_signup.type;

select
  sales.user_id,
  sales.total_sales,
  returns.total_returns
from sales
full outer join returns
  on sales.user_id = returns.user_id
where sales.user_id is not null or returns.user_id is not null;

semantic_models:
  - name: sales
    defaults:
      agg_time_dimension: first_ordered_at
    entities:
      - name: id
        type: primary
      - name: user_id
        type: foreign
    measures:
      - name: average_purchase_price
        agg: avg
        expr: purchase_price
    dimensions:
      - name: metric_time
        type: time
        type_params:
  - name: user_signup
    entities:
      - name: user_id
        type: primary
      - name: country_id
        type: unique
    dimensions:
      - name: signup_date
        type: time
      - name: country_dim

- name: country
    entities:
      - name: country_id
        type: primary
    dimensions:
      - name: country_name
        type: categorical

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Discover data with Catalog

With Catalog, you can view your project's [resources](https://docs.getdbt.com/docs/build/projects.md) (such as models, tests, and metrics), their lineage, and [model consumption](https://docs.getdbt.com/docs/explore/view-downstream-exposures.md) to gain a better understanding of its latest production state.

Use Catalog to navigate and manage your projects within dbt to help you and other data developers, analysts, and consumers discover and leverage your dbt resources. Catalog integrates with the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md), [dbt Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md), [Orchestrator](https://docs.getdbt.com/docs/deploy/deployments.md), and [Canvas](https://docs.getdbt.com/docs/cloud/canvas.md) to help you develop or view your dbt resources.

#### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* You have a dbt account on the [Starter, Enterprise, or Enterprise+ plan](https://www.getdbt.com/pricing/).
* You have set up a [production](https://docs.getdbt.com/docs/deploy/deploy-environments.md#set-as-production-environment) or [staging](https://docs.getdbt.com/docs/deploy/deploy-environments.md#create-a-staging-environment) deployment environment for each project you want to explore.
* You have at least one successful job run in the deployment environment. Note that [CI jobs](https://docs.getdbt.com/docs/deploy/ci-jobs.md) do not update Catalog.
* You are on the Catalog page. To do this, select **Explore** from the navigation in dbt.

<!-- -->

#### Generate metadata[​](#generate-metadata "Direct link to Generate metadata")

Catalog uses the metadata provided by the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) to display the details about [the state of your dbt project](https://docs.getdbt.com/docs/dbt-cloud-apis/project-state.md). The metadata that's available depends on the [deployment environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md) you've designated as *production* or *staging* in your dbt project.

Catalog also allows you to ingest external metadata from Snowflake, giving you visibility into tables, views, and other resources that aren't defined in dbt with Catalog.

#### dbt metadata[​](#dbt-metadata "Direct link to dbt metadata")

If you're using a [hybrid project setup](https://docs.getdbt.com/docs/deploy/hybrid-setup.md) and uploading artifacts from dbt Core, make sure to follow the [setup instructions](https://docs.getdbt.com/docs/deploy/hybrid-setup.md#connect-project-in-dbt-cloud) to connect your project in dbt. This enables Catalog to access and display your metadata correctly.

* To ensure all metadata is available in Catalog, run `dbt build` and `dbt docs generate` as part of your job in your production or staging environment. Running those two commands ensure all relevant metadata (like lineage, test results, documentation, and more) is available in Catalog.
* Catalog automatically retrieves the metadata updates after each job run in the production or staging deployment environment so it always has the latest results for your project. This includes deploy and merge jobs.
  <!-- -->
  * Note that CI jobs don't update Catalog. This is because they don't reflect the production state and don't provide the necessary metadata updates.
* To view a resource and its metadata, you must define the resource in your project and run a job in the production or staging environment.
* The resulting metadata depends on the [commands](https://docs.getdbt.com/docs/deploy/job-commands.md) executed by the jobs.

Note that Catalog automatically deletes stale metadata after 3 months if no jobs were run to refresh it. To avoid this, make sure you schedule jobs to run more frequently than 3 months with the necessary commands.

| To view in Catalog                                        | You must successfully run                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| All metadata                                              | [dbt build](https://docs.getdbt.com/reference/commands/build.md), [dbt docs generate](https://docs.getdbt.com/reference/commands/cmd-docs.md), and [dbt source freshness](https://docs.getdbt.com/reference/commands/source.md#dbt-source-freshness) together as part of the same job in the environment |
| Model lineage, details, or results                        | [dbt run](https://docs.getdbt.com/reference/commands/run.md) or [dbt build](https://docs.getdbt.com/reference/commands/build.md) on a given model within a job in the environment                                                                                                                        |
| Columns and statistics for models, sources, and snapshots | [dbt docs generate](https://docs.getdbt.com/reference/commands/cmd-docs.md) within [a job](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md) in the environment                                                                                                                          |
| Test results                                              | [dbt test](https://docs.getdbt.com/reference/commands/test.md) or [dbt build](https://docs.getdbt.com/reference/commands/build.md) within a job in the environment                                                                                                                                       |
| Source freshness results                                  | [dbt source freshness](https://docs.getdbt.com/reference/commands/source.md#dbt-source-freshness) within a job in the environment                                                                                                                                                                        |
| Snapshot details                                          | [dbt snapshot](https://docs.getdbt.com/reference/commands/snapshot.md) or [dbt build](https://docs.getdbt.com/reference/commands/build.md) within a job in the environment                                                                                                                               |
| Seed details                                              | [dbt seed](https://docs.getdbt.com/reference/commands/seed.md) or [dbt build](https://docs.getdbt.com/reference/commands/build.md) within a job in the environment                                                                                                                                       |

Richer and more timely metadata will become available as dbt evolves.

tip

If your organization works in both dbt Core and Cloud, you can unify these workflows by automatically uploading dbt Core artifacts into dbt Cloud and viewing them in Catalog for a more connected dbt experience. To learn more, visit [hybrid projects](https://docs.getdbt.com/docs/deploy/hybrid-projects.md).

##### External metadata ingestion [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")[​](#external-metadata-ingestion- "Direct link to external-metadata-ingestion-")

Connect directly to your data warehouse with [external metadata ingestion](https://docs.getdbt.com/docs/explore/external-metadata-ingestion.md), giving you visibility into tables, views, and other resources that aren't defined in dbt with Catalog.

We create dbt metadata and pull external metadata. Catalog uses the metadata provided by the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) to display details about the state of your project. The available metadata depends on which [deployment environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md) you’ve designated as production or staging in your dbt project.

#### Catalog overview[​](#catalog-overview "Direct link to Catalog overview")

[Global navigation](https://docs.getdbt.com/docs/explore/global-navigation.md) [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing") [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")

Catalog introduces the ability to widen your search by including dbt resources (models, seeds, snapshots, sources, exposures, and more) across your entire account. This broadens the results returned and gives you greater insight into all the assets across your dbt projects. Learn more in [Global navigation](https://docs.getdbt.com/docs/explore/global-navigation.md) or in our [video overview](https://www.loom.com/share/ae93b3d241cd439fbe5f98f5e6872113?).

Navigate the Catalog overview page to access your project's resources and metadata. The page includes the following sections:

* **Search bar** — [Search](#search-resources) for resources in your project by keyword. You can also use filters to refine your search results.
* **Sidebar** — Use the left sidebar to access model [performance](https://docs.getdbt.com/docs/explore/model-performance.md), [project recommendations](https://docs.getdbt.com/docs/explore/project-recommendations.md) in the **Project details** section. Browse your project's [resources, file tree, and database](#browse-with-the-sidebar) in the lower section of the sidebar.
  <!-- -->
  * Find your project recommendations within your project's landing page.\*
* **Lineage graph** — Explore your project's or account's [lineage graph](#project-lineage) to visualize the relationships between resources.
* **Latest updates** — View the latest changes or issues related to your project's resources, including the most recent job runs, changed properties, lineage, and issues.
* **Marts and public models** — View the [marts](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview.md#guide-structure-overview) and [public models](https://docs.getdbt.com/docs/mesh/govern/model-access.md#access-modifiers) in your project. You can also navigate to all public models in your account through this view.
* **Model query history** — Use [model query history](https://docs.getdbt.com/docs/explore/model-query-history.md) to track consumption queries on your models for deeper insights.
* **Visualize downstream exposures** — [Set up](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures-tableau.md) and [visualize downstream exposures](https://docs.getdbt.com/docs/explore/view-downstream-exposures.md) to automatically expose relevant data models from Tableau to enhance visibility.
* **Data health signals** — View the [data-health-signals](https://docs.getdbt.com/docs/explore/data-health-signals.md) for each resource to understand its health and performance.

##### Catalog permissions[​](#catalog-permissions "Direct link to Catalog permissions")

When using global navigation and searching across your projects, the following permissions apply.

* Your project access permissions determine which dbt projects appear in the left-hand menu of the global navigation.
* In Catalog searches, we use soft access controls, you'll see all matching resources in search results, with clear indicators for items you don't have access to.
* For external metadata, the global platform credential controls which resources metadata users can discover. See [External metadata ingestion](https://docs.getdbt.com/docs/explore/external-metadata-ingestion.md) for more details.

<!-- -->

On-demand learning

If you enjoy video courses, check out our [dbt Catalog on-demand course](https://learn.getdbt.com/courses/dbt-catalog) and learn how to best explore your dbt project(s)!

#### Explore your project's lineage graph[​](#project-lineage "Direct link to Explore your project's lineage graph")

Catalog provides a visualization of your project's DAG that you can interact with. To access the project's full lineage graph, select **Overview** in the left sidebar and click the **Explore Lineage** button on the main (center) section of the page.

If you don't see the project lineage graph immediately, click **Render Lineage**. It can take some time for the graph to render depending on the size of your project and your computer's available memory. The graph of very large projects might not render so you can select a subset of nodes by using selectors, instead.

The nodes in the lineage graph represent the project's resources and the edges represent the relationships between the nodes. Nodes are color-coded and include iconography according to their resource type.

By default, Catalog shows the project's [applied state](https://docs.getdbt.com/docs/dbt-cloud-apis/project-state.md#definition-logical-vs-applied-state-of-dbt-nodes) lineage. That is, it shows models that have been successfully built and are available to query, not just the models defined in the project.

To explore the lineage graphs of tests and macros, view [their resource details pages](#view-resource-details). By default, Catalog excludes these resources from the full lineage graph unless a search query returns them as results.

 How can I interact with the full lineage graph?

* Hover over any item in the graph to display the resource's name and type.

* Zoom in and out on the graph by mouse-scrolling.

* Grab and move the graph and the nodes.

* Right-click on a node (context menu) to:

  * Refocus on the node, including its upstream and downstream nodes
  * Refocus on the node and its downstream nodes only
  * Refocus on the node and it upstream nodes only
  * View the node's [resource details](#view-resource-details) page

* Select a resource to highlight its relationship with other resources in your project. A panel opens on the graph's right-hand side that displays a high-level summary of the resource's details. The side panel includes a **General** tab for information like description, materialized type, and other details. In the side panel's upper right corner:

  * Click the View Resource icon to [view the resource details](#view-resource-details).
  * Click the [Open in IDE](#open-in-ide) icon to examine the resource using the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md).
  * Click the Copy Link to Page icon to copy the page's link to your clipboard.

* Use [selectors](https://docs.getdbt.com/reference/node-selection/methods.md) (in the search bar) to select specific resources or a subset of the DAG. This can help narrow the focus on the resources that interest you. All selectors are available for use, except those requiring a state comparison (result, source status, and state). You can also use the `--exclude` and the `--select` flag (which is optional). Examples:

  * `resource_type:model [RESOURCE_NAME]` — Returns all models matching the name search
  * `resource_type:metric,tag:nightly` — Returns metrics with the tag `nightly`

* Use [graph operators](https://docs.getdbt.com/reference/node-selection/graph-operators.md) (in the search bar) to select specific resources or a subset of the DAG. This can help narrow the focus on the resources that interest you. Examples:

  * `+orders` — Returns all the upstream nodes of `orders`
  * `+dim_customers,resource_type:source` — Returns all sources that are upstream of `dim_customers`

* Use [set operators](https://docs.getdbt.com/reference/node-selection/set-operators.md) (in the search bar) to select specific resources or a subset of the DAG. This can help narrow the focus on the resources that interest you. For example:

  * `+snowplow_sessions +fct_orders` — Use space-delineated arguments for a union operation. Returns resources that are upstream nodes of either `snowplow_sessions` or `fct_orders`.

* [View resource details](#view-resource-details) by selecting a node (double-clicking) in the graph.

* Click **Lenses** (lower right corner of the graph) to use Catalog [lenses](#lenses) feature.

##### Example of full lineage graph[​](#example-of-full-lineage-graph "Direct link to Example of full lineage graph")

Example of exploring a model in the project's lineage graph:

[![Example of full lineage graph](/img/docs/collaborate/dbt-explorer/example-project-lineage-graph.png?v=2 "Example of full lineage graph")](#)Example of full lineage graph

#### Lenses[​](#lenses "Direct link to Lenses")

The **Lenses** feature is available from your [project's lineage graph](#project-lineage) (lower right corner). Lenses are like map layers for your DAG. Lenses make it easier to understand your project's contextual metadata at scale, especially to distinguish a particular model or a subset of models.

When you apply a lens, tags become visible on the nodes in the lineage graph, indicating the layer value along with coloration based on that value. If you're significantly zoomed out, only the tags and their colors are visible in the graph.

Lenses are helpful to analyze a subset of the DAG if you're zoomed in, or to find models/issues from a larger vantage point.

 List of available lenses

A resource in your project is characterized by resource type, materialization type, or model layer, as well as its latest run or latest test status. Lenses are available for the following metadata:

* **Resource type**: Organizes resources by resource type, such as models, tests, seeds, saved query, and [more](https://docs.getdbt.com/docs/build/projects.md). Resource type uses the `resource_type` selector.

* **Materialization type**: Identifies the strategy for building the dbt models in your data platform.

* **Latest status**: The status from the latest execution of the resource in the current environment. For example, diagnosing a failed DAG region.

* **Model layer**: The modeling layer that the model belongs to according to [best practices guide](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview.md#guide-structure-overview). For example, discovering marts models to analyze.

  <!-- -->

  * **Marts** — A model with the prefix `fct_` or `dim_` or a model that lives in the `/marts/` subdirectory.
  * **Intermediate** — A model with the prefix `int_`. Or, a model that lives in the `/int/` or `/intermediate/` subdirectory.
  * **Staging** — A model with the prefix `stg_`. Or, a model that lives in the `/staging/` subdirectory.

* **Test status**: The status from the latest execution of the tests that ran again this resource. In the case that a model has multiple tests with different results, the lens reflects the 'worst case' status.

* **Consumption query history**: The number of queries against this resource over a given time period.

##### Example of lenses[​](#example-of-lenses "Direct link to Example of lenses")

Example of applying the **Materialization type** *lens* with the lineage graph zoomed out. In this view, each model name has a color according to the materialization type legend at the bottom, which specifies the materialization type. This color-coding helps to quickly identify the materialization types of different models.

[![Example of the Materialization type lens](/img/docs/collaborate/dbt-explorer/example-materialization-type.jpg?v=2 "Example of the Materialization type lens")](#)Example of the Materialization type lens

Example of applying the **Tests Status** *lens*, where each model name displays the tests status according to the legend at the bottom, which specifies the test status.

[![Example of the Test Status lens](/img/docs/collaborate/dbt-explorer/example-test-status.jpg?v=2 "Example of the Test Status lens")](#)Example of the Test Status lens

#### Keyword search[​](#search-resources "Direct link to Keyword search")

With Catalog, global navigation provides a search experience allowing you to find dbt resources across all your projects, as well as non-dbt resources in Snowflake.

You can locate resources in your project by performing a keyword search in the search bar. All resource names, column names, resource descriptions, warehouse relations, and code matching your search criteria will be displayed as a list on the main (center) section of the page. When searching for an exact column name, the results show all relational nodes containing that column in their schemas. If there's a match, a notice in the search result indicates the resource contains the specified column. Also, you can apply filters to further refine your search results.

 Search features

* **Partial keyword search** — Also referred to as fuzzy search. Catalog uses a "contains" logic to improve your search results. This means you can search for partial terms without knowing the exact root word of your search term.
* **Exclude keywords** — Prepend a minus sign (-) to the keyword you want to exclude from search results. For example, `-user` will exclude all matches of that keyword from search results.
* **Boolean operators** — Use Boolean operators to enhance your keyword search. For example, the search results for `users OR github` will include matches for either keyword.
* **Phrase search** — Surround a string of keywords with double quotation marks to search for that exact phrase (for example, `"stg users"`). To learn more, refer to [Phrase search](https://en.wikipedia.org/wiki/Phrase_search) on Wikipedia.
* **SQL keyword search** — Use SQL keywords in your search. For example, the search results `int github users joined` will include matches that contain that specific string of keywords (similar to phrase searching).

 Filters side panel

The **Filters** side panel becomes available after you perform a keyword search. Use this panel to further refine the results from your keyword search. By default, Catalog searches across all resources in the project. You can filter on:

* [Resource type](https://docs.getdbt.com/docs/build/projects.md) (like models, sources, and so on)
* [Model access](https://docs.getdbt.com/docs/mesh/govern/model-access.md) (like public, private)
* [Model layer](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview.md) (like marts, staging)
* [Model materialization](https://docs.getdbt.com/docs/build/materializations.md) (like view, table)
* [Tags](https://docs.getdbt.com/reference/resource-configs/tags.md) (supports multi-select)

Under the **Models** option, you can filter on model properties (access or materialization type). Also available are **Advanced** options, where you can limit the search results to column name, model code, and more.

 Global navigation

Catalog builds on the functionality of the old navigation and introduces exciting new capabilities to enhance your experience. For more information, refer to [Global navigation](https://docs.getdbt.com/docs/explore/global-navigation.md).

##### Example of keyword search[​](#example-of-keyword-search "Direct link to Example of keyword search")

Example of results from searching on the keyword `customers` and applying the filters models, description, and code. [Data health signals](https://docs.getdbt.com/docs/explore/data-health-signals.md) are visible to the right of the model name in the search results.

#### Browse with the sidebar[​](#browse-with-the-sidebar "Direct link to Browse with the sidebar")

From the sidebar, you can browse your project's resources, its file tree, and the database.

* **Resources** tab — All resources in the project organized by type. Select any resource type in the list and all those resources in the project will display as a table in the main section of the page. For a description on the different resource types (like models, metrics, and so on), refer to [About dbt projects](https://docs.getdbt.com/docs/build/projects.md).
  <!-- -->
  * [Data health signals](https://docs.getdbt.com/docs/explore/data-health-signals.md) are visible to the right of the resource name under the **Health** column.
* **File Tree** tab — All resources in the project organized by the file in which they are defined. This mirrors the file tree in your dbt project repository.
* **Database** tab — All resources in the project organized by the database and schema in which they are built. This mirrors your data platform's structure that represents the [applied state](https://docs.getdbt.com/docs/dbt-cloud-apis/project-state.md) of your project.

#### Integrated tool access[​](#integrated-tool-access "Direct link to Integrated tool access")

Users with a [developer license](https://docs.getdbt.com/docs/cloud/manage-access/about-user-access.md#license-based-access-control) or an analyst seat can open a resource directly from the Catalog in the Studio IDE to view its model files, in Insights to query it, or in Canvas for visual editing.

#### View model versions[​](#view-model-versions "Direct link to View model versions")

If models in the project are versioned, you can see which [version of the model](https://docs.getdbt.com/docs/mesh/govern/model-versions.md) is being applied — `prerelease`, `latest`, and `old` — in the title of the model's details page and in the model list from the sidebar.

#### View resource details[​](#view-resource-details "Direct link to View resource details")

You can view the definition and latest run results of any resource in your project. To find a resource and view its details, you can interact with the lineage graph, use search, or browse the Catalog.

The details (metadata) available to you depends on the resource's type, its definition, and the [commands](https://docs.getdbt.com/docs/deploy/job-commands.md) that run within jobs in the production environment.

In the upper right corner of the resource details page, you can:

* Click the [Open in Studio IDE](#open-in-ide) icon to examine the resource using the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md).
* Click the Share icon to copy the page's link to your clipboard.

 What details are available for a model?

* **Data health signals** — [Data health signals](https://docs.getdbt.com/docs/explore/data-health-signals.md) offer a quick, at-a-glance view of data health. These icons indicate whether a model is Healthy, Caution, Degraded, or Unknown. Hover over an icon to view detailed information about the model's health.

* **Status bar** (below the page title) — Information on the last time the model ran, whether the run was successful, how the data is materialized, number of rows, and the size of the model.

* **General** tab includes:

  <!-- -->

  * **Lineage** graph — The model's lineage graph that you can interact with. The graph includes one upstream node and one downstream node from the model. Click the Expand icon in the graph's upper right corner to view the model in full lineage graph mode.
  * **Description** section — A [description of the model](https://docs.getdbt.com/docs/build/documentation.md#adding-descriptions-to-your-project).
  * **Recent** section — Information on the last time the model ran, how long it ran for, whether the run was successful, the job ID, and the run ID.
  * **Tests** section — [Data tests](https://docs.getdbt.com/docs/build/data-tests.md) for the model, including a status indicator for the latest test status. A
    <!-- -->
    ✅
    <!-- -->
    denotes a passing test.
  * **Details** section — Key properties like the model's relation name (for example, how it's represented and how you can query it in the data platform: `database.schema.identifier`); model governance attributes like access, group, and if contracted; and more.
  * **Relationships** section — The nodes the model **Depends On**, is **Referenced by**, and (if applicable) is **Used by** for projects that have declared the models' project as a dependency.

* **Code** tab — The source code and compiled code for the model.

* **Columns** tab — The available columns in the model. This tab also shows tests results (if any) that you can select to view the test's details page. A
  <!-- -->
  ✅
  <!-- -->
  denotes a passing test. To filter the columns in the resource, you can use the search bar that's located at the top of the columns view.

 What details are available for an exposure?

* **Status bar** (below the page title) — Information on the last time the exposure was updated.

* **Data health signals** — [Data health signals](https://docs.getdbt.com/docs/explore/data-health-signals.md) offer a quick, at-a-glance view of data health. These icons indicate whether a resource is Healthy, Caution, or Degraded. Hover over an icon to view detailed information about the exposure's health.

* **General** tab includes:

  <!-- -->

  * **Data health** — The status on data freshness and data quality.
  * **Status** section — The status on data freshness and data quality.
  * **Lineage** graph — The exposure's lineage graph. Click the **Expand** icon in the graph's upper right corner to view the exposure in full lineage graph mode. Integrates natively with Tableau and auto-generates downstream lineage.
  * **Description** section — A description of the exposure.
  * **Details** section — Details like exposure type, maturity, owner information, and more.
  * **Relationships** section — The nodes the exposure **Depends On**.

 What details are available for a test?

* **Status bar** (below the page title) — Information on the last time the test ran, whether the test passed, test name, test target, and column name. Defaults to all if not specified.
* **Test Type** (next to the Status bar) — Information on the different test types available: Unit test or Data test. Defaults to all if not specified.

When you select a test, the following details are available:

* **General** tab includes:

  <!-- -->

  * **Lineage** graph — The test's lineage graph that you can interact with. The graph includes one upstream node and one downstream node from the test resource. Click the Expand icon in the graph's upper right corner to view the test in full lineage graph mode.
  * **Description** section — A description of the test.
  * **Recent** section — Information on the last time the test ran, how long it ran for, whether the test passed, the job ID, and the run ID.
  * **Details** section — Details like schema, severity, package, and more.
  * **Relationships** section — The nodes the test **Depends On**.

* **Code** tab — The source code and compiled code for the test.

Example of the Tests view:

 What details are available for each source table within a source collection?

* **Status bar** (below the page title) — Information on the last time the source was updated and the number of tables the source uses.

* **Data health signals** — [Data health signals](https://docs.getdbt.com/docs/explore/data-health-signals.md) offer a quick, at-a-glance view of data health. These icons indicate whether a resource is Healthy, Caution, or Degraded. Hover over an icon to view detailed information about the source's health.

* **General** tab includes:

  <!-- -->

  * **Lineage** graph — The source's lineage graph that you can interact with. The graph includes one upstream node and one downstream node from the source. Click the Expand icon in the graph's upper right corner to view the source in full lineage graph mode.
  * **Description** section — A description of the source.
  * **Source freshness** section — Information on whether refreshing the data was successful, the last time the source was loaded, the timestamp of when a run generated data, and the run ID.
  * **Details** section — Details like database, schema, and more.
  * **Relationships** section — A table that lists all the sources used with their freshness status, the timestamp of when freshness was last checked, and the timestamp of when the source was last loaded.

* **Columns** tab — The available columns in the source. This tab also shows tests results (if any) that you can select to view the test's details page. A
  <!-- -->
  ✅
  <!-- -->
  denotes a passing test.

##### Example of model details[​](#example-of-model-details "Direct link to Example of model details")

Example of the details view for the model `customers`:<br />

[![Example of resource details](/img/docs/collaborate/dbt-explorer/example-model-details.png?v=2 "Example of resource details")](#)Example of resource details

[![Example of downstream exposure details for Tableau.](/img/docs/cloud-integrations/auto-exposures/explorer-lineage2.jpg?v=2 "Example of downstream exposure details for Tableau.")](#)Example of downstream exposure details for Tableau.

#### Staging environment[​](#staging-environment "Direct link to Staging environment")

Catalog supports views for [staging deployment environments](https://docs.getdbt.com/docs/deploy/deploy-environments.md#staging-environment), in addition to the production environment. This gives you a unique view into your pre-production data workflows, with the same tools available in production, while providing an extra layer of scrutiny.

You can explore the metadata from your production or staging environment to inform your data development lifecycle. Just [set a single environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md) per dbt project as "production" or "staging," and ensure the proper metadata has been generated then you'll be able to view it in Catalog. Refer to [Generating metadata](https://docs.getdbt.com/docs/explore/explore-projects.md#generate-metadata) for more details.

#### Related content[​](#related-content "Direct link to Related content")

* [Enterprise permissions](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions.md)
* [About model governance](https://docs.getdbt.com/docs/mesh/govern/about-model-governance.md)
* Blog on [What is data mesh?](https://www.getdbt.com/blog/what-is-data-mesh-the-definition-and-importance-of-data-mesh)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Enhance your code

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/build/environment-variables.md)

###### [Environment variables](https://docs.getdbt.com/docs/build/environment-variables.md)

[Learn how you can use environment variables to customize the behavior of a dbt project.](https://docs.getdbt.com/docs/build/environment-variables.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/build/hooks-operations.md)

###### [Hooks and operations](https://docs.getdbt.com/docs/build/hooks-operations.md)

[Learn how to use hooks to trigger actions and operations to invoke macros.](https://docs.getdbt.com/docs/build/hooks-operations.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/build/packages.md)

###### [Packages](https://docs.getdbt.com/docs/build/packages.md)

[Learn how you can leverage code reuse through packages (libraries).](https://docs.getdbt.com/docs/build/packages.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/build/project-variables.md)

###### [Project variables](https://docs.getdbt.com/docs/build/project-variables.md)

[Learn how to use project variables to provide data to models for compilation.](https://docs.getdbt.com/docs/build/project-variables.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Enhance your models

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/build/materializations.md)

###### [Materializations](https://docs.getdbt.com/docs/build/materializations.md)

[Learn how to use materializations to make dbt models persist in a data platform.](https://docs.getdbt.com/docs/build/materializations.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/build/incremental-models.md)

###### [Incremental models](https://docs.getdbt.com/docs/build/incremental-models.md)

[Learn how to use incremental models so you can limit the amount of data that needs to be transformed.](https://docs.getdbt.com/docs/build/incremental-models.md)

<br />

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Entities

Entities are real-world concepts in a business, such as customers, transactions, and ad campaigns. We often focus our analyses on specific entities, such as customer churn or annual recurring revenue modeling. In our Semantic Layer models, these entities serve as a join key across semantic models.

Within a semantic graph, the required parameters for an entity are `name` and `type`. The `name` refers to either the key column name from the underlying data table, or it may serve as an alias with the column name referenced in the `expr` parameter. The `name` for your entity must be unique to the semantic model and can not be the same as an existing `measure` or `dimension` within that same model.

Entities can be specified with a single column or multiple columns. Entities (join keys) in a semantic model are identified by their name. Each entity name must be unique within a semantic model, but it doesn't have to be unique across different semantic models.

There are four entity types:

* [Primary](#primary) — Has only one record for each row in the table and includes every record in the data platform. This key uniquely identifies each record in the table.
* [Unique](#unique) — Contains only one record per row in the table and allows for null values. May have a subset of records in the data warehouse.
* [Foreign](#foreign) — A field (or a set of fields) in one table that uniquely identifies a row in another table. This key establishes a link between tables.
* [Natural](#natural) — Columns or combinations of columns in a table that uniquely identify a record based on real-world data. This key is derived from actual data attributes.

Use entities as dimensions

You can also use entities as dimensions, which allows you to aggregate a metric to the granularity of that entity.

#### Entity types[​](#entity-types "Direct link to Entity types")

MetricFlow's join logic depends on the entity `type` you use and determines how to join semantic models. Refer to [Joins](https://docs.getdbt.com/docs/build/join-logic.md) for more info on how to construct joins.

##### Primary[​](#primary "Direct link to Primary")

A primary key has *only one* record for each row in the table and includes every record in the data platform. It must contain unique values and can't contain null values. Use the primary key to ensure that each record in the table is distinct and identifiable.

 Primary key example

For example, consider a table of employees with the following columns:
```

Example 2 (unknown):
```unknown
In this case, `employee_id` is the primary key. Each `employee_id` is unique and represents one specific employee. There can be no duplicate `employee_id` and can't be null.

##### Unique[​](#unique "Direct link to Unique")

A unique key contains *only one* record per row in the table but may have a subset of records in the data warehouse. However, unlike the primary key, a unique key allows for null values. The unique key ensures that the column's values are distinct, except for null values.

 Unique key example

For example, consider a table of students with the following columns:
```

Example 3 (unknown):
```unknown
In this example, `email` is defined as a unique key. Each email address must be unique; however, multiple students can have null email addresses. This is because the unique key constraint allows for one or more null values, but non-null values must be unique. This then creates a set of records with unique emails (non-null) that could be a subset of the entire table, which includes all students.

##### Foreign[​](#foreign "Direct link to Foreign")

A foreign key is a field (or a set of fields) in one table that uniquely identifies a row in another table. The foreign key establishes a link between the data in two tables. It can include zero, one, or multiple instances of the same record. It can also contain null values.

 Foreign key example

For example, consider you have two tables, `customers` and `orders`:

customers table:
```

Example 4 (unknown):
```unknown
orders table:
```

---

## tests on one source table

**URL:** llms-txt#tests-on-one-source-table

dbt test --select "source:jaffle_shop.customers"

---

## └── stg_event_sessions.sql

**URL:** llms-txt#└──-stg_event_sessions.sql

**Contents:**
  - Measures
  - Merge jobs in dbt StarterEnterprise
  - Merge jobs in dbt [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - MetricFlow commands

name: my_project
version: 1.0.0
config-version: 2

models:
  my_project:
    events:
      # materialize all models in models/events as tables
      +materialized: table
    csvs:
      # this is redundant, and does not need to be set
      +materialized: view

{{ config(materialized='table', sort='timestamp', dist='user_id') }}

models:
  - name: events
    config:
      materialized: table

import snowflake.snowpark.functions as F

def model(dbt, session):
    dbt.config(materialized = "incremental")
    df = dbt.ref("upstream_table")

if dbt.is_incremental:

# only new rows compared to max in current table
        max_from_this = f"select max(updated_at) from {dbt.this}"
        df = df.filter(df.updated_at >= session.sql(max_from_this).collect()[0][0])

# or only rows from the past 3 days
        df = df.filter(df.updated_at >= F.dateadd("day", F.lit(-3), F.current_timestamp()))

import pyspark.sql.functions as F

def model(dbt, session):
    dbt.config(materialized = "incremental")
    df = dbt.ref("upstream_table")

if dbt.is_incremental:

# only new rows compared to max in current table
        max_from_this = f"select max(updated_at) from {dbt.this}"
        df = df.filter(df.updated_at >= session.sql(max_from_this).collect()[0][0])

# or only rows from the past 3 days
        df = df.filter(df.updated_at >= F.date_add(F.current_timestamp(), F.lit(-3)))

name: p99_transaction_value
description: The 99th percentile transaction value
expr: transaction_amount_usd
agg: percentile
agg_params:
  percentile: .99
  use_discrete_percentile: False  # False calculates the continuous percentile, True calculates the discrete percentile.

semantic_models:
  - name: subscriptions
    description: A subscription table with one row per date for each active user and their subscription plans. 
    model: ref('your_schema.subscription_table')
    defaults:
      agg_time_dimension: subscription_date

entities:
      - name: user_id
        type: foreign
    primary_entity: subscription

dimensions:
      - name: subscription_date
        type: time
        expr: date_transaction
        type_params:
          time_granularity: day

measures: 
      - name: count_users
        description: Count of users at the end of the month 
        expr: user_id
        agg: count_distinct
        non_additive_dimension: 
          name: subscription_date
          window_choice: max 
      - name: mrr
        description: Aggregate by summing all users' active subscription plans
        expr: subscription_value
        agg: sum 
        non_additive_dimension: 
          name: subscription_date
          window_choice: max
      - name: user_mrr
        description: Group by user_id to achieve each user's MRR
        expr: subscription_value
        agg: sum  
        non_additive_dimension: 
          name: subscription_date
          window_choice: max
          window_groupings: 
            - user_id

metrics:
  - name: mrr_metrics
    type: simple
    type_params:
        measure: mrr

dbt sl query --metrics mrr_by_end_of_month --group-by subscription__subscription_date__month --order subscription__subscription_date__month 
dbt sl query --metrics mrr_by_end_of_month --group-by subscription__subscription_date__week --order subscription__subscription_date__week

mf query --metrics mrr_by_end_of_month --group-by subscription__subscription_date__month --order subscription__subscription_date__month 
mf query --metrics mrr_by_end_of_month --group-by subscription__subscription_date__week --order subscription__subscription_date__week

dbt sl list metrics <metric_name> # In the dbt platform

mf list metrics <metric_name> # In dbt Core

Options:
  --search TEXT          Filter available metrics by this search term
  --show-all-dimensions  Show all dimensions associated with a metric.
  --help                 Show this message and exit.

dbt sl list dimensions --metrics <metric_name> # In the dbt platform

mf list dimensions --metrics <metric_name> # In dbt Core

Options:
  --metrics SEQUENCE  List dimensions by given metrics (intersection). Ex. --metrics bookings,messages
  --help              Show this message and exit.

dbt sl list dimension-values --metrics <metric_name> --dimension <dimension_name> # In the dbt platform

mf list dimension-values --metrics <metric_name> --dimension <dimension_name> # In dbt Core

Options:
  --dimension TEXT    Dimension to query values from  [required]
  --metrics SEQUENCE  Metrics that are associated with the dimension
                      [required]
  --end-time TEXT     Optional iso8601 timestamp to constraint the end time of
                      the data (inclusive)
                      *Not available in the dbt platform yet
  --start-time TEXT   Optional iso8601 timestamp to constraint the start time
                      of the data (inclusive)
                      *Not available in in the dbt platform yet
  --help              Show this message and exit.

dbt sl list entities --metrics <metric_name> # In the dbt platform

mf list entities --metrics <metric_name> # In dbt Core

Options:
  --metrics SEQUENCE  List entities by given metrics (intersection). Ex. --metrics bookings,messages
  --help              Show this message and exit.

dbt sl list saved-queries

dbt sl list saved-queries --show-exports

dbt sl list saved-queries --show-exports

The list of available saved queries:
- new_customer_orders
  exports:
       - Export(new_customer_orders_table, exportAs=TABLE)
       - Export(new_customer_orders_view, exportAs=VIEW)
       - Export(new_customer_orders, alias=orders, schemas=customer_schema, exportAs=TABLE)

dbt sl validate # For dbt users
mf validate-configs # For dbt Core users

Options:
  --timeout                       # dbt platform only
                                  Optional timeout for data warehouse validation in the dbt platform.
  --dw-timeout INTEGER            # dbt Core only
                                  Optional timeout for data warehouse
                                  validation steps. Default None.
  --skip-dw                       # dbt Core only
                                  Skips the data warehouse validations.
  --show-all                      # dbt Core only
                                  Prints warnings and future errors.
  --verbose-issues                # dbt Core only
                                  Prints extra details about issues.
  --semantic-validation-workers INTEGER  # dbt Core only
                                  Uses specified number of workers for large configs.
  --help                          Show this message and exit.

mf health-checks # In dbt Core

mf tutorial # In dbt Core

dbt sl query --metrics <metric_name> --group-by <dimension_name> # In the dbt platform
dbt sl query --saved-query <name> # In the dbt platform

mf query --metrics <metric_name> --group-by <dimension_name> # In dbt Core

--metrics SEQUENCE       Syntax to query single metrics: --metrics metric_name
                           For example, --metrics bookings
                           To query multiple metrics, use --metrics followed by the metric names, separated by commas without spaces.
                           For example,  --metrics bookings,messages

--group-by SEQUENCE      Syntax to group by single dimension/entity: --group-by dimension_name
                           For example, --group-by ds
                           For multiple dimensions/entities, use --group-by followed by the dimension/entity names, separated by commas without spaces.
                           For example, --group-by ds,org

--end-time TEXT          Optional iso8601 timestamp to constraint the end
                           time of the data (inclusive).
                           *Not available in the dbt platform yet

--start-time TEXT        Optional iso8601 timestamp to constraint the start
                           time of the data (inclusive)
                           *Not available in the dbt platform yet

--where TEXT             SQL-like where statement provided as a string and wrapped in quotes.
                           All filter items must explicitly reference fields or dimensions that are part of your model.
                           To query a single statement: ---where "{{ Dimension('order_id__revenue') }} > 100"
                           To query multiple statements: --where "{{ Dimension('order_id__revenue') }} > 100" --where "{{ Dimension('user_count') }} < 1000" # make sure to wrap each statement in quotes
                           To add a dimension filter, use the `Dimension()` template wrapper to indicate that the filter item is part of your model. 
                           Refer to the FAQ for more info on how to do this using a template wrapper.

--limit TEXT             Limit the number of rows out using an int or leave
                           blank for no limit. For example: --limit 100

--order-by SEQUENCE     Specify metrics, dimension, or group bys to order by.
                          Add the `-` prefix to sort query in descending (DESC) order. 
                          Leave blank for ascending (ASC) order.
                          For example, to sort metric_time in DESC order: --order-by -metric_time 
                          To sort metric_time in ASC order and revenue in DESC order:  --order-by metric_time,-revenue

--csv FILENAME           Provide filepath for data frame output to csv

--compile (the dbt platform)          In the query output, show the query that was
 --explain (dbt Core)     executed against the data warehouse

--show-dataflow-plan     Display dataflow plan in explain output

--display-plans          Display plans (such as metric dataflow) in the browser

--decimals INTEGER       Choose the number of decimal places to round for
                           the numerical values

--show-sql-descriptions  Shows inline descriptions of nodes in displayed SQL

--help                   Show this message and exit.

dbt sl query --metrics order_total,users_active --group-by metric_time # In the dbt platform

mf query --metrics order_total,users_active --group-by metric_time # In dbt Core

✔ Success 🦄 - query completed after 1.24 seconds
| METRIC_TIME   |   ORDER_TOTAL |
|:--------------|---------------:|
| 2017-06-16    |         792.17 |
| 2017-06-17    |         458.35 |
| 2017-06-18    |         490.69 |
| 2017-06-19    |         749.09 |
| 2017-06-20    |         712.51 |
| 2017-06-21    |         541.65 |

dbt sl query --metrics order_total --group-by order_id__is_food_order # In the dbt platform

mf query --metrics order_total --group-by order_id__is_food_order # In dbt Core

Success 🦄 - query completed after 1.70 seconds
| METRIC_TIME   | IS_FOOD_ORDER   |   ORDER_TOTAL |
|:--------------|:----------------|---------------:|
| 2017-06-16    | True            |         499.27 |
| 2017-06-16    | False           |         292.90 |
| 2017-06-17    | True            |         431.24 |
| 2017-06-17    | False           |          27.11 |
| 2017-06-18    | True            |         466.45 |
| 2017-06-18    | False           |          24.24 |
| 2017-06-19    | False           |         300.98 |
| 2017-06-19    | True            |         448.11 |

**Examples:**

Example 1 (unknown):
```unknown
Alternatively, materializations can be configured directly inside of the model SQL files. This can be useful if you are also setting \[Performance Optimization] configs for specific models (for example, [Redshift specific configurations](https://docs.getdbt.com/reference/resource-configs/redshift-configs.md) or [BigQuery specific configurations](https://docs.getdbt.com/reference/resource-configs/bigquery-configs.md)).

models/events/stg\_event\_log.sql
```

Example 2 (unknown):
```unknown
Materializations can also be configured in the model's `properties.yml` file. The following example shows the `table` materialization type. For a complete list of materialization types, refer to [materializations](https://docs.getdbt.com/docs/build/materializations.md#materializations).

models/properties.yml
```

Example 3 (unknown):
```unknown
#### Materializations[​](#materializations "Direct link to Materializations")

##### View[​](#view "Direct link to View")

When using the `view` materialization, your model is rebuilt as a view on each run, via a `create view as` statement.

* **Pros:** No additional data is stored, views on top of source data will always have the latest records in them.

* **Cons:** Views that perform a significant transformation, or are stacked on top of other views, are slow to query.

* **Advice:**

  * Generally start with views for your models, and only change to another materialization when you notice performance problems.
  * Views are best suited for models that do not do significant transformation, for example, renaming, or recasting columns.

##### Table[​](#table "Direct link to Table")

When using the `table` materialization, your model is rebuilt as a table on each run, via a `create table as` statement.

* **Pros:** Tables are fast to query

* **Cons:**

  * Tables can take a long time to rebuild, especially for complex transformations
  * New records in underlying source data are not automatically added to the table

* **Advice:**

  * Use the table materialization for any models being queried by BI tools, to give your end user a faster experience
  * Also use the table materialization for any slower transformations that are used by many downstream models

##### Incremental[​](#incremental "Direct link to Incremental")

`incremental` models allow dbt to insert or update records into a table since the last time that model was run.

* **Pros:** You can significantly reduce the build time by just transforming new records

* **Cons:** Incremental models require extra configuration and are an advanced usage of dbt. Read more about using incremental models [here](https://docs.getdbt.com/docs/build/incremental-models.md).

* **Advice:**

  * Incremental models are best for event-style data
  * Use incremental models when your `dbt run`s are becoming too slow (i.e. don't start with incremental models)

##### Ephemeral[​](#ephemeral "Direct link to Ephemeral")

`ephemeral` models are not directly built into the database. Instead, dbt will interpolate the code from an ephemeral model into its dependent models using a common table expression (CTE). You can control the identifier for this CTE using a [model alias](https://docs.getdbt.com/docs/build/custom-aliases.md), but dbt will always prefix the model identifier with `__dbt__cte__`.

* **Pros:**

  * You can still write reusable logic
  * Ephemeral models can help keep your data warehouse clean by reducing clutter (also consider splitting your models across multiple schemas by [using custom schemas](https://docs.getdbt.com/docs/build/custom-schemas.md)).

* **Cons:**

  * You cannot select directly from this model.
  * [Operations](https://docs.getdbt.com/docs/build/hooks-operations.md#about-operations) (for example, macros called using [`dbt run-operation`](https://docs.getdbt.com/reference/commands/run-operation.md) cannot `ref()` ephemeral nodes)
  * Overuse of ephemeral materialization can also make queries harder to debug.
  * Ephemeral materialization doesn't support [model contracts](https://docs.getdbt.com/docs/mesh/govern/model-contracts.md#where-are-contracts-supported).

* **Advice:** Use the ephemeral materialization for:

  <!-- -->

  * Very light-weight transformations that are early on in your DAG
  * Are only used in one or two downstream models, and
  * Don't need to be queried directly

##### Materialized View[​](#materialized-view "Direct link to Materialized View")

The `materialized_view` materialization allows the creation and maintenance of materialized views in the target database. Materialized views are a combination of a view and a table, and serve use cases similar to incremental models.

* **Pros:**

  * Materialized views combine the query performance of a table with the data freshness of a view
  * Materialized views operate much like incremental materializations, however they are usually able to be refreshed without manual interference on a regular cadence (depending on the database), forgoing the regular dbt batch refresh required with incremental materializations
  * `dbt run` on materialized views corresponds to a code deployment, just like views

- **Cons:**

  * Due to the fact that materialized views are more complex database objects, database platforms tend to have fewer configuration options available; see your database platform's docs for more details
  * Materialized views may not be supported by every database platform

* **Advice:**
  * Consider materialized views for use cases where incremental models are sufficient, but you would like the data platform to manage the incremental logic and refresh.

###### Configuration Change Monitoring[​](#configuration-change-monitoring "Direct link to Configuration Change Monitoring")

This materialization makes use of the [`on_configuration_change`](https://docs.getdbt.com/reference/resource-configs/on_configuration_change.md) config, which aligns with the incremental nature of the namesake database object. This setting tells dbt to attempt to make configuration changes directly to the object when possible, as opposed to completely recreating the object to implement the updated configuration. Using `dbt-postgres` as an example, indexes can be dropped and created on the materialized view without the need to recreate the materialized view itself.

###### Scheduled Refreshes[​](#scheduled-refreshes "Direct link to Scheduled Refreshes")

In the context of a `dbt run` command, materialized views should be thought of as similar to views. For example, a `dbt run` command is only needed if there is the potential for a change in configuration or sql; it's effectively a deploy action. By contrast, a `dbt run` command is needed for a table in the same scenarios *AND when the data in the table needs to be updated*. This also holds true for incremental and snapshot models, whose underlying relations are tables. In the table cases, the scheduling mechanism is either dbt or your local scheduler; there is no built-in functionality to automatically refresh the data behind a table. However, most platforms (Postgres excluded) provide functionality to configure automatically refreshing a materialized view. Hence, materialized views work similarly to incremental models with the benefit of not needing to run dbt to refresh the data. This assumes, of course, that auto refresh is turned on and configured in the model.

info

`dbt-snowflake` *does not* support materialized views, it uses Dynamic Tables instead. For details, refer to [Snowflake specific configurations](https://docs.getdbt.com/reference/resource-configs/snowflake-configs.md#dynamic-tables).

#### Python materializations[​](#python-materializations "Direct link to Python materializations")

Python models support two materializations:

* `table`
* `incremental`

Incremental Python models support all the same [incremental strategies](https://docs.getdbt.com/docs/build/incremental-strategy.md) as their SQL counterparts. The specific strategies supported depend on your adapter.

Python models can't be materialized as `view` or `ephemeral`. Python isn't supported for non-model resource types (like tests and snapshots).

For incremental models, like SQL models, you will need to filter incoming tables to only new rows of data:

* Snowpark
* PySpark

models/my\_python\_model.py
```

Example 4 (unknown):
```unknown
models/my\_python\_model.py
```

---

## Run all resources tagged "order_metrics"

**URL:** llms-txt#run-all-resources-tagged-"order_metrics"

dbt run --select tag:order_metrics

saved_queries:
  - name: test_saved_query
    description: "{{ doc('saved_query_description') }}"
    label: Test saved query
    config:
      tags: 
        - order_metrics
        - hourly

**Examples:**

Example 1 (unknown):
```unknown
The second example shows how to apply multiple tags to a saved query in the `semantic_model.yml` file. The saved query is then tagged with `order_metrics` and `hourly`.

semantic\_model.yml
```

Example 2 (unknown):
```unknown
Run resources with multiple tags using the following commands:
```

---

## tests on two or more specific sources

**URL:** llms-txt#tests-on-two-or-more-specific-sources

dbt test --select "source:jaffle_shop source:raffle_bakery"

---

## my test_is_valid_email_address unit test will run on all versions EXCEPT 1 of my_model

**URL:** llms-txt#my-test_is_valid_email_address-unit-test-will-run-on-all-versions-except-1-of-my_model

**Contents:**
  - updated_at
  - Upsolver configurations
  - Using the + prefix
  - version
  - versions
  - Vertica configurations
  - Warnings
  - where
  - YAML Selectors
  - Yellowbrick configurations

unit_tests:
  - name: test_is_valid_email_address
    model: my_model 
    versions:
      exclude: 
        - 1
    ...

snapshots:
  <resource-path>:
    +strategy: timestamp
    +updated_at: column_name

{{ config(
        materialized='connection',
        connection_type={ 'S3' | 'GLUE_CATALOG' | 'KINESIS' | 'KAFKA'| 'SNOWFLAKE' },
        connection_options={}
        )
}}

{{ config(  materialized='incremental',
            sync=True|False,
            source = 'S3'| 'KAFKA' | ... ,
            options={
              'option_name': 'option_value'
            },
            partition_by=[{}]
          )
}}
SELECT * FROM {{ ref(<model>) }}

{{ config(  materialized='incremental',
            sync=True|False,
            map_columns_by_name=True|False,
            incremental_strategy='insert',
            options={
              'option_name': 'option_value'
            },
            primary_key=[{}]
          )
}}
SELECT ...
FROM {{ ref(<model>) }}
WHERE ...
GROUP BY ...
HAVING COUNT(DISTINCT orderid::string) ...

{{ config(  materialized='incremental',
            sync=True|False,
            map_columns_by_name=True|False,
            incremental_strategy='merge',
            options={
              'option_name': 'option_value'
            },
            primary_key=[{}]
          )
}}
SELECT ...
FROM {{ ref(<model>) }}
WHERE ...
GROUP BY ...
HAVING COUNT ...

{{ config(  materialized='materializedview',
            sync=True|False,
            options={'option_name': 'option_value'}
        )
}}
SELECT ...
FROM {{ ref(<model>) }}
WHERE ...
GROUP BY ...

WITH EXPECTATION <expectation_name> EXPECT <sql_predicate>
ON VIOLATION WARN

models:
  - name: <model name>
    # required
    config:
      contract:
        enforced: true
    # model-level constraints
    constraints:
      - type: check
        columns: ['<column1>', '<column2>']
        expression: "column1 <= column2"
        name: <constraint_name>
      - type: not_null
        columns: ['column1', 'column2']
        name: <constraint_name>

columns:
      - name: <column3>
        data_type: string

# column-level constraints
        constraints:
          - type: not_null
          - type: check
            expression: "REGEXP_LIKE(<column3>, '^[0-9]{4}[a-z]{5}$')"
            name: <constraint_name>

name: jaffle_shop
config-version: 2

models:
  +materialized: view
  jaffle_shop:
    marts:
      +materialized: table

name: jaffle_shop
config-version: 2

models:
  +persist_docs: # this config is a dictionary, so needs a + prefix
    relation: true
    columns: true

jaffle_shop:
    schema: my_schema # a plus prefix is optional here
    +tags: # this is the tag config
      - "hello"
    config:
      tags: # whereas this is the tag resource path
        # changed to config in v1.10
        # The below config applies to models in the
        # models/tags/ directory.
        # Note: you don't _need_ a leading + here,
        # but it wouldn't hurt.
        materialized: view

version: 2  # Only 2 is accepted by dbt versions up to 1.4.latest.

models:
  - name: model_name
    versions:
      - v: <version_identifier> # required
        defined_in: <file_name> # optional -- default is <model_name>_v<v>
        columns:
          # specify all columns, or include/exclude columns from the top-level model YAML definition
          - include: <include_value>
            exclude: <exclude_list>
          # specify additional columns
          - name: <column_name> # required
      - v: ...
    
    # optional
    latest_version: <version_identifier>

models:
  
  # top-level model properties
  - name: <model_name>
    columns:
      - name: <column_name> # required
    
    # versions of this model
    versions:
      - v: <version_identifier> # required
        columns:
          - include: '*' | 'all' | [<column_name>, ...]
            exclude:
              - <column_name>
              - ... # declare additional column names to exclude
          
          # declare more columns -- can be overrides from top-level, or in addition
          - name: <column_name>
            ...

models:
  - name: customers
    columns:
      - name: customer_id
        description: Unique identifier for this table
        data_type: text
        constraints:
          - type: not_null
        data_tests:
          - unique
      - name: customer_country
        data_type: text
        description: "Country where the customer currently lives"
      - name: first_purchase_date
        data_type: date
    
    versions:
      - v: 4
      
      - v: 3
        columns:
          - include: "*"
          - name: customer_country
            data_type: text
            description: "Country where the customer first lived at time of first purchase"
      
      - v: 2
        columns:
          - include: "*"
            exclude:
              - customer_country
      
      - v: 1
        columns:
          - include: []
          - name: id
            data_type: int

Breaking Change to Unversioned Contract for contracted_model (models/contracted_models/contracted_model.sql)
  While comparing to previous project state, dbt detected a breaking change to an unversioned model.
    - Contract enforcement was removed: Previously, this model's configuration included contract: {enforced: true}. It is no longer configured to enforce its contract, and this is a breaking change.
    - Columns were removed:
      - color
      - date_day
    - Enforced column level constraints were removed:
      - id (ConstraintType.not_null)
      - id (ConstraintType.primary_key)
    - Enforced model level constraints were removed:
      - ConstraintType.check -> ['id']
    - Materialization changed with enforced constraints:
      - table -> view

Breaking Change to Contract Error in model sometable (models/sometable.sql)
  While comparing to previous project state, dbt detected a breaking change to an enforced contract.

The contract's enforcement has been disabled.

Columns were removed:
   - order_name

Columns with data_type changes:
   - order_id (number -> int)

Consider making an additive (non-breaking) change instead, if possible.
  Otherwise, create a new model version: https://docs.getdbt.com/docs/mesh/govern/model-versions

{{config(materialized = 'incremental',on_schema_change='ignore')}} 
    
    select * from {{ ref('seed_added') }}

insert into "VMart"."public"."merge" ("id", "name", "some_date")
    (
        select "id", "name", "some_date"
        from "merge__dbt_tmp"
    )

{{config(materialized = 'incremental',on_schema_change='fail')}} 
      
      
      select * from {{ ref('seed_added') }}

The source and target schemas on this incremental model are out of sync!
              They can be reconciled in several ways:
                - set the `on_schema_change` config to either append_new_columns or sync_all_columns, depending on your situation.
                - Re-run the incremental model with `full_refresh: True` to update the target schema.
                - update the schema manually and re-run the process.

Additional troubleshooting context:
                 Source columns not in target: {{ schema_changes_dict['source_not_in_target'] }}
                 Target columns not in source: {{ schema_changes_dict['target_not_in_source'] }}
                 New column types: {{ schema_changes_dict['new_target_types'] }}

{{ config( materialized='incremental', on_schema_change='append_new_columns') }}

select * from  public.seed_added

insert into "VMart"."public"."over" ("id", "name", "some_date", "w", "w1", "t1", "t2", "t3")
          (
                select "id", "name", "some_date", "w", "w1", "t1", "t2", "t3"
                from "over__dbt_tmp"
          )

{{ config(  materialized='incremental',     incremental_strategy='append'  ) }}

select * from  public.product_dimension

{% if is_incremental() %} 
    
        where product_key > (select max(product_key) from {{this }}) 
    
    
    {% endif %}

insert into "VMart"."public"."samp" (

"product_key", "product_version", "product_description", "sku_number", "category_description", 
        "department_description", "package_type_description", "package_size", "fat_content", "diet_type",
        "weight", "weight_units_of_measure", "shelf_width", "shelf_height", "shelf_depth", "product_price",
        "product_cost", "lowest_competitor_price", "highest_competitor_price", "average_competitor_price", "discontinued_flag")
    (
          select "product_key", "product_version", "product_description", "sku_number", "category_description", "department_description", "package_type_description", "package_size", "fat_content", "diet_type", "weight", "weight_units_of_measure", "shelf_width", "shelf_height", "shelf_depth", "product_price", "product_cost", "lowest_competitor_price", "highest_competitor_price", "average_competitor_price", "discontinued_flag"

from "samp__dbt_tmp"
    )

{{ config( materialized = 'incremental', incremental_strategy = 'merge',  unique_key='promotion_key'   )  }}
      
      
          select * FROM  public.promotion_dimension

merge into "VMart"."public"."samp" as DBT_INTERNAL_DEST using "samp__dbt_tmp" as DBT_INTERNAL_SOURCE
          on DBT_INTERNAL_DEST."promotion_key" = DBT_INTERNAL_SOURCE."promotion_key"
  
        when matched then update set
        "promotion_key" = DBT_INTERNAL_SOURCE."promotion_key", "price_reduction_type" = DBT_INTERNAL_SOURCE."price_reduction_type", "promotion_media_type" = DBT_INTERNAL_SOURCE."promotion_media_type", "display_type" = DBT_INTERNAL_SOURCE."display_type", "coupon_type" = DBT_INTERNAL_SOURCE."coupon_type", "ad_media_name" = DBT_INTERNAL_SOURCE."ad_media_name", "display_provider" = DBT_INTERNAL_SOURCE."display_provider", "promotion_cost" = DBT_INTERNAL_SOURCE."promotion_cost", "promotion_begin_date" = DBT_INTERNAL_SOURCE."promotion_begin_date", "promotion_end_date" = DBT_INTERNAL_SOURCE."promotion_end_date"
        
        when not matched then insert
          ("promotion_key", "price_reduction_type", "promotion_media_type", "display_type", "coupon_type",
           "ad_media_name", "display_provider", "promotion_cost", "promotion_begin_date", "promotion_end_date")
        values
        (
          DBT_INTERNAL_SOURCE."promotion_key", DBT_INTERNAL_SOURCE."price_reduction_type", DBT_INTERNAL_SOURCE."promotion_media_type", DBT_INTERNAL_SOURCE."display_type", DBT_INTERNAL_SOURCE."coupon_type", DBT_INTERNAL_SOURCE."ad_media_name", DBT_INTERNAL_SOURCE."display_provider", DBT_INTERNAL_SOURCE."promotion_cost", DBT_INTERNAL_SOURCE."promotion_begin_date", DBT_INTERNAL_SOURCE."promotion_end_date"
        )

{{ config( materialized = 'incremental', incremental_strategy='merge', unique_key = 'id', merge_update_columns = ["names", "salary"] )}}
    
        select * from {{ref('seed_tc1')}}

merge into "VMart"."public"."test_merge" as DBT_INTERNAL_DEST using "test_merge__dbt_tmp" as DBT_INTERNAL_SOURCE on  DBT_INTERNAL_DEST."id" = DBT_INTERNAL_SOURCE."id"
        
        when matched then update set
          "names" = DBT_INTERNAL_SOURCE."names", "salary" = DBT_INTERNAL_SOURCE."salary"
        
        when not matched then insert
        ("id", "names", "salary")
        values
        (
          DBT_INTERNAL_SOURCE."id", DBT_INTERNAL_SOURCE."names", DBT_INTERNAL_SOURCE."salary"
        )

{{ config( materialized = 'incremental', incremental_strategy = 'delete+insert',  unique_key='date_key'   )  }}

select * FROM  public.date_dimension

delete from "VMart"."public"."samp"
            where (
                date_key) in (
                select (date_key)
                from "samp__dbt_tmp"
            );

insert into "VMart"."public"."samp" (
             "date_key", "date", "full_date_description", "day_of_week", "day_number_in_calendar_month", "day_number_in_calendar_year", "day_number_in_fiscal_month", "day_number_in_fiscal_year", "last_day_in_week_indicator", "last_day_in_month_indicator", "calendar_week_number_in_year", "calendar_month_name", "calendar_month_number_in_year", "calendar_year_month", "calendar_quarter", "calendar_year_quarter", "calendar_half_year", "calendar_year", "holiday_indicator", "weekday_indicator", "selling_season")
        (
            select "date_key", "date", "full_date_description", "day_of_week", "day_number_in_calendar_month", "day_number_in_calendar_year", "day_number_in_fiscal_month", "day_number_in_fiscal_year", "last_day_in_week_indicator", "last_day_in_month_indicator", "calendar_week_number_in_year", "calendar_month_name", "calendar_month_number_in_year", "calendar_year_month", "calendar_quarter", "calendar_year_quarter", "calendar_half_year", "calendar_year", "holiday_indicator", "weekday_indicator", "selling_season"
            from "samp__dbt_tmp"
        );

{{config(materialized = 'incremental',incremental_strategy = 'insert_overwrite',partition_by_string='YEAR(cc_open_date)',partitions=['2023'])}}

select * from online_sales.call_center_dimension

select PARTITION_TABLE('online_sales.update_call_center_dimension');

SELECT DROP_PARTITIONS('online_sales.update_call_center_dimension', '2023', '2023');
      
        SELECT PURGE_PARTITION('online_sales.update_call_center_dimension', '2023');
      
        insert into "VMart"."online_sales"."update_call_center_dimension"

("call_center_key", "cc_closed_date", "cc_open_date", "cc_name", "cc_class", "cc_employees",
       
        "cc_hours", "cc_manager", "cc_address", "cc_city", "cc_state", "cc_region")
      
        (

select "call_center_key", "cc_closed_date", "cc_open_date", "cc_name", "cc_class", "cc_employees",
        
            "cc_hours", "cc_manager", "cc_address", "cc_city", "cc_state", "cc_region"

from "update_call_center_dimension__dbt_tmp"
        );

{{ config(  materialized='table',  order_by='product_key') }} 
    
        select * from public.product_dimension

create  table  "VMart"."public"."order_s__dbt_tmp" as 
            
             ( select * from public.product_dimension)
              
                 order by product_key;

{{ config( materialized='table', segmented_by_string='product_key'  )  }}  
        
        
        select * from public.product_dimension

create  table
        
        "VMart"."public"."segmented_by__dbt_tmp"
        
        as (select * from public.product_dimension)
          
             segmented by product_key  ALL NODES;

{{ config( materialized='table', segmented_by_string='product_key' ,segmented_by_all_nodes='True' )  }}  
        
            select * from public.product_dimension

create  table   "VMart"."public"."segmented_by__dbt_tmp" as
              
          (select * from public.product_dimension)
                  
            segmented by product_key  ALL NODES;

{{config(materialized='table',no_segmentation='true')}}

select * from public.product_dimension

create  table
                      "VMart"."public"."ww__dbt_tmp"
    
                   INCLUDE SCHEMA PRIVILEGES as (
    
                select * from public.product_dimension )
                
                        UNSEGMENTED ALL NODES ;

{{ config( materialized='table', partition_by_string='employee_age' )}} 
    
      
        select * FROM public.employee_dimension

create table "VMart"."public"."test_partition__dbt_tmp" as 
        
        ( select * FROM public.employee_dimension); 
        
        alter table "VMart"."public"."test_partition__dbt_tmp"
         
        partition BY employee_age

{{ config( materialized='table', 
    partition_by_string='employee_age',    
    partition_by_group_by_string="""
                                  CASE WHEN employee_age < 5 THEN 1
                                  WHEN employee_age>50 THEN 2
                                  ELSE 3 END""",
    
    partition_by_active_count = 2) }}

select * FROM public.employee_dimension

create  table "VMart"."public"."test_partition__dbt_tmp" as
      
      ( select * FROM public.employee_dimension );
          
          alter table "VMart"."public"."test_partition__dbt_tmp" partition BY employee_ag  
          
            group by CASE WHEN employee_age < 5 THEN 1
        
        WHEN employee_age>50 THEN 2
        
        ELSE 3 END
        
        SET ACTIVEPARTITIONCOUNT 2  ;

{{config(materialized='table',
    partition_by_string='number_of_children', 
    partition_by_group_by_string="""
                                  CASE WHEN number_of_children <= 2 THEN 'small_family'
                                  ELSE 'big_family' END""")}}
select * from public.customer_dimension

create  table "VMart"."public"."test_partition__dbt_tmp"  INCLUDE SCHEMA PRIVILEGES as 
    
        ( select * from public.customer_dimension ) ; 
        
      alter table "VMart"."public"."test_partition__dbt_tmp" 
      partition BY number_of_children
      group by CASE WHEN number_of_children <= 2 THEN 'small_family'
                                             ELSE 'big_family' END  ;

{{  config(  materialized='table',    ksafe='1'   ) }} 
        
          select * from  public.product_dimension

create  table "VMart"."public"."segmented_by__dbt_tmp" as 
  
        (select * from  public.product_dimension ) 
            ksafe 1;

...
flags:
  warn_error_options:
    error: # Previously called "include"
    warn: # Previously called "exclude"
    silence: # To silence or ignore warnings
      - NoNodesForSelectionCriteria

dbt run --warn-error-options '{"error": "all", "warn": ["NoNodesForSelectionCriteria"]}'
  
  dbt run --warn-error-options '{"error": "all", "warn": ["Deprecations"]}'
  
  dbt run --warn-error-options '{"error": ["NoNodesForSelectionCriteria"]}'
  
  DBT_WARN_ERROR_OPTIONS='{"error": ["NoNodesForSelectionCriteria"]}' dbt run
  
...
flags:
  warn_error_options:
    error: all # Previously called "include"
    warn:      # Previously called "exclude"
      - NoNodesForSelectionCriteria
    silence:   # To silence or ignore warnings
      - NoNodesForSelectionCriteria

dbt run --warn-error
dbt run --warn-error-options '{"error": "all"}'
dbt run --warn-error-options '{"error": "*"}'

WARN_ERROR=true dbt run 
DBT_WARN_ERROR_OPTIONS='{"error": "all"}' dbt run 
DBT_WARN_ERROR_OPTIONS='{"error": "*"}' dbt run

select *
from my_model
where my_column is null

select *
from (select * from my_model where date_column = current_date) dbt_subquery
where my_column is null

models:
  - name: large_table
    columns:
      - name: my_column
        data_tests:
          - accepted_values:
              arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                values: ["a", "b", "c"]
              config:
                where: "date_column = current_date"
      - name: other_column
        data_tests:
          - not_null:
              config: 
                where: "date_column < current_date"

{% test <testname>(model, column_name) %}

{{ config(where = "date_column = current_date") }}

data_tests:
  +where: "date_column = current_date"
  
  <package_name>:
    +where: >
        date_column = current_date
        and another_column is not null

models:
  - name: my_model
    columns:
      - name: id
        data_tests:
          - unique:
              config:
                where: "date_column > __3_days_ago__"  # placeholder string for static config

{% macro get_where_subquery(relation) -%}
    {% set where = config.get('where') %}
    {% if where %}
        {% if "_days_ago__" in where %}
            {# replace placeholder string with result of custom macro #}
            {% set where = replace_days_ago(where) %}
        {% endif %}
        {%- set filtered -%}
            (select * from {{ relation }} where {{ where }}) dbt_subquery
        {%- endset -%}
        {% do return(filtered) %}
    {%- else -%}
        {% do return(relation) %}
    {%- endif -%}
{%- endmacro %}

{% macro replace_days_ago(where_string) %}
    {# Use regex to search the pattern for the number days #}
    {# Default to 3 days when no number found #}
    {% set re = modules.re %}
    {% set days = 3 %}
    {% set pattern = '__(\d+)_days_ago__' %}
    {% set match = re.search(pattern, where_string) %}
    {% if match %}
        {% set days = match.group(1) | int %}        
    {% endif %}
    {% set n_days_ago = dbt.dateadd('day', -days, current_timestamp()) %}
    {% set result = re.sub(pattern, n_days_ago, where_string) %}
    {{ return(result) }}
{% endmacro %}

selectors:
  - name: nodes_to_joy
    definition: ...
  - name: nodes_to_a_grecian_urn
    description: Attic shape with a fair attitude
    default: true
    definition: ...

definition:
  'tag:nightly'

definition:
  tag: nightly

definition:
  method: tag
  value: nightly

# Optional keywords map to the `+` and `@` graph operators:

children: true | false
  parents: true | false

children_depth: 1    # if children: true, degrees to include
  parents_depth: 1     # if parents: true, degrees to include

childrens_parents: true | false     # @ operator

indirect_selection: eager | cautious | buildable | empty # include all tests selected indirectly? eager by default

definition:
  method: fqn
  value: "*"

- method: tag
  value: nightly
  exclude:
    - "@tag:daily"

- union:
    - method: tag
      value: nightly
    - exclude:
       - method: tag
         value: daily

- union:
    - method: fqn
      value: model_a
      indirect_selection: eager  # default: will include all tests that touch model_a
    - method: fqn
      value: model_b
      indirect_selection: cautious  # will not include tests touching model_b
                        # if they have other unselected parents
    - method: fqn
      value: model_c
      indirect_selection: buildable  # will not include tests touching model_c
                        # if they have other unselected parents (unless they have an ancestor that is selected)
    - method: fqn
      value: model_d
      indirect_selection: empty  # will include tests for only the selected node and ignore all tests attached to model_d

$ dbt run --select @source:snowplow,tag:nightly models/export --exclude package:snowplow,config.materialized:incremental export_performance_timing

selectors:
  - name: nightly_diet_snowplow
    description: "Non-incremental Snowplow models that power nightly exports"
    definition:

# Optional `union` and `intersection` keywords map to the ` ` and `,` set operators:
      union:
        - intersection:
            - '@source:snowplow'
            - 'tag:nightly'
        - 'models/export'
        - exclude:
            - intersection:
                - 'package:snowplow'
                - 'config.materialized:incremental'
            - export_performance_timing

selectors:
  - name: nightly_diet_snowplow
    description: "Non-incremental Snowplow models that power nightly exports"
    definition:
      # Optional `union` and `intersection` keywords map to the ` ` and `,` set operators:
      union:
        - intersection:
            - method: source
              value: snowplow
              childrens_parents: true
            - method: tag
              value: nightly
        - method: path
          value: models/export
        - exclude:
            - intersection:
                - method: package
                  value: snowplow
                - method: config.materialized
                  value: incremental
            - method: fqn
              value: export_performance_timing

dbt run --selector nightly_diet_snowplow

selectors:
  - name: root_project_only
    description: >
        Only resources from the root project.
        Excludes resources defined in installed packages.
    default: true
    definition:
      method: package
      value: <my_root_project_name>

dbt build
dbt source freshness
dbt docs generate

dbt run --select  "model_a"
dbt run --exclude model_a

selectors:
  - name: default_for_dev
    default: "{{ target.name == 'dev' | as_bool }}"
    definition: ...
  - name: default_for_prod
    default: "{{ target.name == 'prod' | as_bool }}"
    definition: ...

selectors:
  - name: foo_and_bar
    definition:
      intersection:
        - tag: foo
        - tag: bar

- name: foo_bar_less_buzz
    definition:
      intersection:
        # reuse the definition from above
        - method: selector
          value: foo_and_bar
        # with a modification!
        - exclude:
            - method: tag
              value: buzz

{{
  config(
    materialized = "table",
    dist = "replicate",
    sort_col = "stadium_capacity"
  )
}}

select
    hash(stg.name) as team_key
    , stg.name as team_name
    , stg.nickname as team_nickname
    , stg.city as home_city
    , stg.stadium as stadium_name
    , stg.capacity as stadium_capacity
    , stg.avg_att as average_game_attendance
    , current_timestamp as md_create_timestamp
from
    {{ source('premdb_public','team') }} stg
where
    stg.name is not null

create table if not exists marts.dim_team as (
select
    hash(stg.name) as team_key
    , stg.name as team_name
    , stg.nickname as team_nickname
    , stg.city as home_city
    , stg.stadium as stadium_name
    , stg.capacity as stadium_capacity
    , stg.avg_att as average_game_attendance
    , current_timestamp as md_create_timestamp
from
    premdb.public.team stg
where
    stg.name is not null
)
distribute REPLICATE
sort on (stadium_capacity);

{{
  config(
    materialized = 'table',
    dist = 'match_key',
    cluster_cols = ['season_key', 'match_date_key', 'home_team_key', 'away_team_key']
  )
}}

select
	hash(concat_ws('||',
	    lower(trim(s.season_name)),
		translate(left(m.match_ts,10), '-', ''),
	    lower(trim(h."name")),
		lower(trim(a."name")))) as match_key
	, hash(lower(trim(s.season_name))) as season_key
	, cast(translate(left(m.match_ts,10), '-', '') as integer) as match_date_key
	, hash(lower(trim(h."name"))) as home_team_key
	, hash(lower(trim(a."name"))) as away_team_key
	, m.htscore
	, split_part(m.htscore, '-', 1)  as home_team_goals_half_time
	, split_part(m.htscore , '-', 2)  as away_team_goals_half_time
	, m.ftscore
	, split_part(m.ftscore, '-', 1)  as home_team_goals_full_time
	, split_part(m.ftscore, '-', 2)  as away_team_goals_full_time
from
	{{ source('premdb_public','match') }} m
		inner join {{ source('premdb_public','team') }} h on (m.htid = h.htid)
		inner join {{ source('premdb_public','team') }} a on (m.atid = a.atid)
		inner join {{ source('premdb_public','season') }} s on (m.seasonid = s.seasonid)

create  table if not exists marts.fact_match as (
select
    hash(concat_ws('||',
        lower(trim(s.season_name)),
        translate(left(m.match_ts,10), '-', ''),
        lower(trim(h."name")),
        lower(trim(a."name")))) as match_key
    , hash(lower(trim(s.season_name))) as season_key
    , cast(translate(left(m.match_ts,10), '-', '') as integer) as match_date_key
    , hash(lower(trim(h."name"))) as home_team_key
    , hash(lower(trim(a."name"))) as away_team_key
    , m.htscore
    , split_part(m.htscore, '-', 1)  as home_team_goals_half_time
    , split_part(m.htscore , '-', 2)  as away_team_goals_half_time
    , m.ftscore
    , split_part(m.ftscore, '-', 1)  as home_team_goals_full_time
    , split_part(m.ftscore, '-', 2)  as away_team_goals_full_time
from
    premdb.public.match m
        inner join premdb.public.team h on (m.htid = h.htid)
        inner join premdb.public.team a on (m.atid = a.atid)
        inner join premdb.public.season s on (m.seasonid = s.seasonid)
)
distribute on (match_key)
cluster on (season_key, match_date_key, home_team_key, away_team_key);

<profile-name>:
  target: <target-name> # this is the default target
  outputs:
    <target-name>:
      type: <bigquery | postgres | redshift | snowflake | other>
      schema: <schema_identifier>
      threads: <natural_number>

### database-specific connection details
      ...

<target-name>: # additional targets
      ...

<profile-name>: # additional profiles
  ...

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### updated_at

dbt\_project.yml
```

Example 2 (unknown):
```unknown
<!-- -->

#### Description[​](#description "Direct link to Description")

A column within the results of your snapshot query that represents when the record row was last updated.

This parameter is **required if using the `timestamp` [strategy](https://docs.getdbt.com/reference/resource-configs/strategy.md)**. The `updated_at` field may support ISO date strings and unix epoch integers, depending on the data platform you use.

#### Default[​](#default "Direct link to Default")

No default is provided.

#### Examples[​](#examples "Direct link to Examples")

##### Use a column name `updated_at`[​](#use-a-column-name-updated_at "Direct link to use-a-column-name-updated_at")

<!-- -->

##### Coalesce two columns to create a reliable `updated_at` column[​](#coalesce-two-columns-to-create-a-reliable-updated_at-column "Direct link to coalesce-two-columns-to-create-a-reliable-updated_at-column")

Consider a data source that only has an `updated_at` column filled in when a record is updated (so a `null` value indicates that the record hasn't been updated after it was created).

Since the `updated_at` configuration only takes a column name, rather than an expression, you should update your snapshot query to include the coalesced column.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Upsolver configurations

#### Supported Upsolver SQLake functionality[​](#supported-upsolver-sqlake-functionality "Direct link to Supported Upsolver SQLake functionality")

| COMMAND                | STATE         | MATERIALIZED     |
| ---------------------- | ------------- | ---------------- |
| SQL compute cluster    | not supported | -                |
| SQL connections        | supported     | connection       |
| SQL copy job           | supported     | incremental      |
| SQL merge job          | supported     | incremental      |
| SQL insert job         | supported     | incremental      |
| SQL materialized views | supported     | materializedview |
| Expectations           | supported     | incremental      |

#### Configs materialization[​](#configs-materialization "Direct link to Configs materialization")

| Config                 | Required | Materialization              | Description                                                                                    | Example                                                                                         |
| ---------------------- | -------- | ---------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| connection\_type       | Yes      | connection                   | Connection identifier: S3/GLUE\_CATALOG/KINESIS                                                | connection\_type='S3'                                                                           |
| connection\_options    | Yes      | connection                   | Dictionary of options supported by selected connection                                         | connection\_options={ 'aws\_role': 'aws\_role', 'external\_id': 'SAMPLES', 'read\_only': True } |
| incremental\_strategy  | No       | incremental                  | Define one of incremental strategies: merge/copy/insert. Default: copy                         | incremental\_strategy='merge'                                                                   |
| source                 | No       | incremental                  | Define source to copy from: S3/KAFKA/KINESIS                                                   | source = 'S3'                                                                                   |
| target\_type           | No       | incremental                  | Define target type REDSHIFT/ELASTICSEARCH/S3/SNOWFLAKE/POSTGRES. Default None for Data lake    | target\_type='Snowflake'                                                                        |
| target\_prefix         | False    | incremental                  | Define PREFIX for ELASTICSEARCH target type                                                    | target\_prefix = 'orders'                                                                       |
| target\_location       | False    | incremental                  | Define LOCATION for S3 target type                                                             | target\_location = 's3://your-bucket-name/path/to/folder/'                                      |
| schema                 | Yes/No   | incremental                  | Define target schema. Required if target\_type, no table created in a metastore connection     | schema = 'target\_schema'                                                                       |
| database               | Yes/No   | incremental                  | Define target connection. Required if target\_type, no table created in a metastore connection | database = 'target\_connection'                                                                 |
| alias                  | Yes/No   | incremental                  | Define target table. Required if target\_type, no table created in a metastore connection      | alias = 'target\_table'                                                                         |
| delete\_condition      | No       | incremental                  | Records that match the ON condition and a delete condition can be deleted                      | delete\_condition='nettotal > 1000'                                                             |
| partition\_by          | No       | incremental                  | List of dictionaries to define partition\_by for target metastore table                        | partition\_by=\[{'field':'$field\_name'}]                                                       |
| primary\_key           | No       | incremental                  | List of dictionaries to define partition\_by for target metastore table                        | primary\_key=\[{'field':'customer\_email', 'type':'string'}]                                    |
| map\_columns\_by\_name | No       | incremental                  | Maps columns from the SELECT statement to the table. Boolean. Default: False                   | map\_columns\_by\_name=True                                                                     |
| sync                   | No       | incremental/materializedview | Boolean option to define if job is synchronized or non-msynchronized. Default: False           | sync=True                                                                                       |
| options                | No       | incremental/materializedview | Dictionary of job options                                                                      | options={ 'START\_FROM': 'BEGINNING', 'ADD\_MISSING\_COLUMNS': True }                           |

#### SQL connection[​](#sql-connection "Direct link to SQL connection")

Connections are used to provide Upsolver with the proper credentials to bring your data into SQLake as well as to write out your transformed data to various services. More details on ["Upsolver SQL connections"](https://docs.upsolver.com/sqlake/sql-command-reference/sql-connections) As a dbt model connection is a model with materialized='connection'
```

Example 3 (unknown):
```unknown
Running this model will compile CREATE CONNECTION(or ALTER CONNECTION if exists) SQL and send it to Upsolver engine. Name of the connection will be name of the model.

#### SQL copy job[​](#sql-copy-job "Direct link to SQL copy job")

A COPY FROM job allows you to copy your data from a given source into a table created in a metastore connection. This table then serves as your staging table and can be used with SQLake transformation jobs to write to various target locations. More details on ["Upsolver SQL copy-from"](https://docs.upsolver.com/sqlake/sql-command-reference/sql-jobs/create-job/copy-from)

As a dbt model copy job is model with materialized='incremental'
```

Example 4 (unknown):
```unknown
Running this model will compile CREATE TABLE SQL for target type Data lake (or ALTER TABLE if exists) and CREATE COPY JOB(or ALTER COPY JOB if exists) SQL and send it to Upsolver engine. Name of the table will be name of the model. Name of the job will be name of the model plus '\_job'

#### SQL insert job[​](#sql-insert-job "Direct link to SQL insert job")

An INSERT job defines a query that pulls in a set of data based on the given SELECT statement and inserts it into the designated target. This query is then run periodically based on the RUN\_INTERVAL defined within the job. More details on ["Upsolver SQL insert"](https://docs.upsolver.com/sqlake/sql-command-reference/sql-jobs/create-job/sql-transformation-jobs/insert).

As a dbt model insert job is model with materialized='incremental' and incremental\_strategy='insert'
```

---

## Run all resources tagged "order_metrics" and "hourly"

**URL:** llms-txt#run-all-resources-tagged-"order_metrics"-and-"hourly"

**Contents:**
  - target_database
  - target_schema
  - Teradata configurations
  - Test selection examples

dbt build --select tag:order_metrics tag:hourly

sources:
  - name: ecom
    schema: raw
    description: E-commerce data for the Jaffle Shop
    config:
      tags:
        my_tag: "my_value". # invalid
    tables:
      - name: raw_customers
        config:
          tags:
            my_tag: "my_value". # invalid

Field config.tags: {'my_tag': 'my_value'} is not valid for source (ecom)

exposures:
  - name: my_exposure
    config:
      tags: ['exposure_tag'] # changed to config in v1.10
    ...

sources:
  - name: source_name
    config:
      tags: ['top_level'] # changed to config in v1.10

tables:
      - name: table_name
        config:
          tags: ['table_level'] # changed to config in v1.10

columns:
          - name: column_name
            config:
              tags: ['column_level'] # changed to config in v1.10 and backported to 1.9
            data_tests:
              - unique:
                config:
                  tags: ['test_level'] # changed to config in v1.10

dbt test --select tag:top_level
dbt test --select tag:table_level
dbt test --select tag:column_level
dbt test --select tag:test_level

snapshots:
  <resource-path>:
    +target_database: string

{{ config(
  target_database="string"
) }}

Encountered an error:
Runtime Error
  Cross-db references not allowed in redshift (raw vs analytics)

snapshots:
  +target_database: snapshots

snapshots:
  +target_database: "{% if target.name == 'dev' %}dev{% else %}{{ target.database }}{% endif %}"

{{
    config(
      target_database=generate_database_name('snapshots')
    )
}}

snapshots:
  <resource-path>:
    +target_schema: string

{{ config(
      target_schema="string"
) }}

snapshots:
  +target_schema: snapshots

seeds:
    +quote_columns: false  #or `true` if you have CSV column headers with spaces
  
    {{
      config(
          materialized="table",
          table_kind="SET"
      )
    }}
    
    seeds:
      <project-name>:
        table_kind: "SET"
    
  { MAP = map_name [COLOCATE USING colocation_name] |
    [NO] FALLBACK [PROTECTION] |
    WITH JOURNAL TABLE = table_specification |
    [NO] LOG |
    [ NO | DUAL ] [BEFORE] JOURNAL |
    [ NO | DUAL | LOCAL | NOT LOCAL ] AFTER JOURNAL |
    CHECKSUM = { DEFAULT | ON | OFF } |
    FREESPACE = integer [PERCENT] |
    mergeblockratio |
    datablocksize |
    blockcompression |
    isolated_loading
  }
  
    { DEFAULT MERGEBLOCKRATIO |
      MERGEBLOCKRATIO = integer [PERCENT] |
      NO MERGEBLOCKRATIO
    }
    
    DATABLOCKSIZE = {
      data_block_size [ BYTES | KBYTES | KILOBYTES ] |
      { MINIMUM | MAXIMUM | DEFAULT } DATABLOCKSIZE
    }
    
    BLOCKCOMPRESSION = { AUTOTEMP | MANUAL | ALWAYS | NEVER | DEFAULT }
      [, BLOCKCOMPRESSIONALGORITHM = { ZLIB | ELZS_H | DEFAULT } ]
      [, BLOCKCOMPRESSIONLEVEL = { value | DEFAULT } ]
    
    WITH [NO] [CONCURRENT] ISOLATED LOADING [ FOR { ALL | INSERT | NONE } ]
    
    {{
      config(
          materialized="table",
          table_option="NO FALLBACK"
      )
    }}
    
    {{
      config(
          materialized="table",
          table_option="NO FALLBACK, NO JOURNAL"
      )
    }}
    
    {{
      config(
          materialized="table",
          table_option="NO FALLBACK, NO JOURNAL, CHECKSUM = ON,
            NO MERGEBLOCKRATIO,
            WITH CONCURRENT ISOLATED LOADING FOR ALL"
      )
    }}
    
    seeds:
      <project-name>:
        table_option:"NO FALLBACK"
    
    seeds:
      <project-name>:
        table_option:"NO FALLBACK, NO JOURNAL"
    
    seeds:
      <project-name>:
        table_option: "NO FALLBACK, NO JOURNAL, CHECKSUM = ON,
          NO MERGEBLOCKRATIO,
          WITH CONCURRENT ISOLATED LOADING FOR ALL"
    
  {{
    config(
        materialized="table",
        with_statistics="true"
    )
  }}
  
  [UNIQUE] PRIMARY INDEX [index_name] ( index_column_name [,...] ) |
  NO PRIMARY INDEX |
  PRIMARY AMP [INDEX] [index_name] ( index_column_name [,...] ) |
  PARTITION BY { partitioning_level | ( partitioning_level [,...] ) } |
  UNIQUE INDEX [ index_name ] [ ( index_column_name [,...] ) ] [loading] |
  INDEX [index_name] [ALL] ( index_column_name [,...] ) [ordering] [loading]
  [,...]
  
    { partitioning_expression |
      COLUMN [ [NO] AUTO COMPRESS |
      COLUMN [ [NO] AUTO COMPRESS ] [ ALL BUT ] column_partition ]
    } [ ADD constant ]
    
    ORDER BY [ VALUES | HASH ] [ ( order_column_name ) ]
    
    WITH [NO] LOAD IDENTITY
    
    {{
      config(
          materialized="table",
          index="UNIQUE PRIMARY INDEX ( GlobalID )"
      )
    }}
    
    {{
      config(
          materialized="table",
          index="PRIMARY INDEX(id)
          PARTITION BY RANGE_N(create_date
                        BETWEEN DATE '2020-01-01'
                        AND     DATE '2021-01-01'
                        EACH INTERVAL '1' MONTH)"
      )
    }}
    
    {{
      config(
          materialized="table",
          index="PRIMARY INDEX(id)
          PARTITION BY RANGE_N(create_date
                        BETWEEN DATE '2020-01-01'
                        AND     DATE '2021-01-01'
                        EACH INTERVAL '1' MONTH)
          INDEX index_attrA (attrA) WITH LOAD IDENTITY"
      )
    }}
    
    seeds:
      <project-name>:
        index: "UNIQUE PRIMARY INDEX ( GlobalID )"
    
    seeds:
      <project-name>:
        index: "PRIMARY INDEX(id)
          PARTITION BY RANGE_N(create_date
                        BETWEEN DATE '2020-01-01'
                        AND     DATE '2021-01-01'
                        EACH INTERVAL '1' MONTH)"
    
    seeds:
      <project-name>:
        index: "PRIMARY INDEX(id)
          PARTITION BY RANGE_N(create_date
                        BETWEEN DATE '2020-01-01'
                        AND     DATE '2021-01-01'
                        EACH INTERVAL '1' MONTH)
          INDEX index_attrA (attrA) WITH LOAD IDENTITY"
    
  seeds:
    <project-name>:
      +use_fastload: true
  
{% snapshot snapshot_example %}
{{
  config(
    target_schema='snapshots',
    unique_key='id',
    strategy='check',
    check_cols=["c2"],
    snapshot_hash_udf='GLOBAL_FUNCTIONS.hash_md5'
  )
}}
select * from {{ ref('order_payments') }}
{% endsnapshot %}

models:
  - name: model_name
    config:
      grants:
        select: ['user_a', 'user_b']

models:
- name: model_name
  config:
    materialized: table
    grants:
      select: ["user_b"]
      insert: ["user_c"]

query_band: 'application=dbt;'
   
     models:
     Project_name:
        +query_band: "app=dbt;model={model};"
   
   {{ config( query_band='sql={model};' ) }}
   
models:
Project_name:
  +query_band: "app=dbt;model={model};"

{{
      config(
          materialized='incremental',
          unique_key='id',
          on_schema_change='fail',
          incremental_strategy='valid_history',
          valid_period='valid_period_col',
          use_valid_to_time='no',
  )
  }}

An illustration demonstrating the source sample data and its corresponding target data:

-- Source data
      pk |       valid_from          | value_txt1 | value_txt2
      ======================================================================
      1  | 2024-03-01 00:00:00.0000  | A          | x1
      1  | 2024-03-12 00:00:00.0000  | B          | x1
      1  | 2024-03-12 00:00:00.0000  | B          | x2
      1  | 2024-03-25 00:00:00.0000  | A          | x2
      2  | 2024-03-01 00:00:00.0000  | A          | x1
      2  | 2024-03-12 00:00:00.0000  | C          | x1
      2  | 2024-03-12 00:00:00.0000  | D          | x1
      2  | 2024-03-13 00:00:00.0000  | C          | x1
      2  | 2024-03-14 00:00:00.0000  | C          | x1
  
  -- Target data
      pk | valid_period                                                       | value_txt1 | value_txt2
      ===================================================================================================
      1  | PERIOD(TIMESTAMP)[2024-03-01 00:00:00.0, 2024-03-12 00:00:00.0]    | A          | x1
      1  | PERIOD(TIMESTAMP)[2024-03-12 00:00:00.0, 2024-03-25 00:00:00.0]    | B          | x1
      1  | PERIOD(TIMESTAMP)[2024-03-25 00:00:00.0, 9999-12-31 23:59:59.9999] | A          | x2
      2  | PERIOD(TIMESTAMP)[2024-03-01 00:00:00.0, 2024-03-12 00:00:00.0]    | A          | x1
      2  | PERIOD(TIMESTAMP)[2024-03-12 00:00:00.0, 9999-12-31 23:59:59.9999] | C          | x1

{{ config(
    post_hook=[
      "COLLECT STATISTICS ON  {{ this }} COLUMN (column_1,  column_2  ...);"
      ]
  )}}
  
packages:
  - package: dbt-labs/dbt_external_tables
    version: [">=0.9.0", "<1.0.0"]

dispatch:
  - macro_namespace: dbt_external_tables
    search_order: ['dbt', 'dbt_external_tables']

sources:
  - name: teradata_external
    schema: "{{ target.schema }}"
    loader: S3

tables:
      - name: people_csv_partitioned
        external: 
          location: "/s3/s3.amazonaws.com/dbt-external-tables-testing/csv/"
          file_format: "TEXTFILE"
          row_format: '{"field_delimiter":",","record_delimiter":"\n","character_set":"LATIN"}'
          using: |
            PATHPATTERN  ('$var1/$section/$var3')
          tbl_properties: |
            MAP = TD_MAP1
            ,EXTERNAL SECURITY  MyAuthObj
          partitions:
            - name: section
              data_type: CHAR(1)
        columns:
          - name: id
            data_type: int
          - name: first_name
            data_type: varchar(64)
          - name: last_name
            data_type: varchar(64)
          - name: email
            data_type: varchar(64)

sources:
  - name: teradata_external
    schema: "{{ target.schema }}"
    loader: S3

tables:
      - name: people_json_partitioned
        external:
          location: '/s3/s3.amazonaws.com/dbt-external-tables-testing/json/'
          using: |
            STOREDAS('TEXTFILE')
            ROWFORMAT('{"record_delimiter":"\n", "character_set":"cs_value"}')
            PATHPATTERN  ('$var1/$section/$var3')
          tbl_properties: |
            MAP = TD_MAP1
            ,EXTERNAL SECURITY  MyAuthObj
          partitions:
            - name: section
              data_type: CHAR(1)

vars:
  temporary_metadata_generation_schema: <schema-name>

dbt test --select "test_type:generic"

dbt test --select "test_type:singular"

dbt test --select "orders"
dbt build --select "orders"

dbt test --select "orders" --indirect-selection=buildable
dbt build --select "orders" --indirect-selection=buildable

dbt test --select "orders" --indirect-selection=cautious
dbt build --select "orders" --indirect-selection=cautious

dbt test --select "orders" --indirect-selection=empty
dbt build --select "orders" --indirect-selection=empty

**Examples:**

Example 1 (unknown):
```unknown
#### Usage notes[​](#usage-notes "Direct link to Usage notes")

##### Tags must be strings[​](#tags-must-be-strings "Direct link to Tags must be strings")

Each individual tag must be a string value (for example, `marketing` or `daily`).

In the following example, `my_tag: "my_value"` is invalid because it is a key-value pair.
```

Example 2 (unknown):
```unknown
A warning is raised when the `tags` value is not a string. For example:
```

Example 3 (unknown):
```unknown
##### Tags are additive[​](#tags-are-additive "Direct link to Tags are additive")

Tags accumulate hierarchically. The [earlier example](https://docs.getdbt.com/reference/resource-configs/tags.md#use-tags-to-run-parts-of-your-project) would result in:

| Model                             | Tags                                  |
| --------------------------------- | ------------------------------------- |
| models/staging/stg\_customers.sql | `contains_pii`, `hourly`              |
| models/staging/stg\_payments.sql  | `contains_pii`, `hourly`, `finance`   |
| models/marts/dim\_customers.sql   | `contains_pii`, `hourly`, `published` |
| models/metrics/daily\_metrics.sql | `contains_pii`, `daily`, `published`  |

##### Other resource types[​](#other-resource-types "Direct link to Other resource types")

Tags can also be applied to [sources](https://docs.getdbt.com/docs/build/sources.md), [exposures](https://docs.getdbt.com/docs/build/exposures.md), and even *specific columns* in a resource. These resources do not yet support the `config` property, so you'll need to specify the tags as a top-level key instead.

models/schema.yml
```

Example 4 (unknown):
```unknown
In the example above, the `unique` test would be selected by any of these four tags:
```

---
