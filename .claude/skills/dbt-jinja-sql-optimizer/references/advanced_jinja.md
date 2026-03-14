# Jinja-Sql-Optimizer - Advanced Jinja

**Pages:** 2

---

## dbt-adapters

**URL:** llms-txt#dbt-adapters

dbt-athena==1.9.4
dbt-bigquery==1.10.1
dbt-databricks==1.10.10
dbt-fabric==1.9.4
dbt-postgres==1.9.0
dbt-redshift==1.9.5
dbt-snowflake==1.10.0
dbt-spark==1.9.3
dbt-synapse==1.8.2
dbt-teradata==1.9.3
dbt-trino==1.9.3

**Examples:**

Example 1 (unknown):
```unknown
Changelogs:

* [dbt-core 1.10.8](https://github.com/dbt-labs/dbt-core/blob/1.10.latest/CHANGELOG.md#dbt-core-1108---august-12-2025)
* [dbt-adapters 1.16.3](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-adapters/CHANGELOG.md#dbt-adapters-1163---july-21-2025)
* [dbt-common 1.25.0](https://github.com/dbt-labs/dbt-common/blob/main/CHANGELOG.md#dbt-common-1271---july-21-2025)
* [dbt-athena 1.9.4](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-athena/CHANGELOG.md#dbt-athena-194---april-28-2025)
* [dbt-bigquery 1.10.1](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-bigquery/CHANGELOG.md#dbt-bigquery-1101---july-29-2025)
* [dbt-databricks 1.9.7](https://github.com/databricks/dbt-databricks/blob/main/CHANGELOG.md#dbt-databricks-1109-august-7-2025)
* [dbt-fabric 1.9.4](https://github.com/microsoft/dbt-fabric/releases/tag/v1.9.4)
* [dbt-postgres 1.9.0](https://github.com/dbt-labs/dbt-postgres/blob/main/CHANGELOG.md#dbt-postgres-190---december-09-2024)
* [dbt-redshift 1.9.5](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-redshift/CHANGELOG.md#dbt-redshift-195---may-13-2025)
* [dbt-snowflake 1.10.0](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-snowflake/CHANGELOG.md#dbt-snowflake-1100-rc3---june-24-2025)
* [dbt-spark 1.9.3](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-spark/CHANGELOG.md#dbt-spark-193---july-16-2025)
* [dbt-synapse 1.8.2](https://github.com/microsoft/dbt-synapse/blob/v1.8.latest/CHANGELOG.md)
* [dbt-teradata 1.9.3](https://github.com/Teradata/dbt-teradata/releases/tag/v1.9.3)
* [dbt-trino 1.9.3](https://github.com/starburstdata/dbt-trino/blob/master/CHANGELOG.md#dbt-trino-193---july-22-2025)

#### July 2025[​](#july-2025 "Direct link to July 2025")

The compatible release slated for July 2025 will be skipped in order to further stabilize the minor upgrade of `dbt-core==1.10.0` ([released June 16, 2025](https://pypi.org/project/dbt-core/1.10.0/)) across the dbt platform.

Compatible releases will resume in August 2025.

#### June 2025[​](#june-2025 "Direct link to June 2025")

Release date: June 12, 2025

This release includes functionality from the following versions of dbt Core OSS:
```

---

## adapters

**URL:** llms-txt#adapters

**Contents:**
  - dbt Product lifecycles
  - dbt release notes
  - dbt Semantic Layer architecture
  - dbt Semantic Layer FAQs
  - dbt Semantic Layer StarterEnterpriseEnterprise +
  - dbt Semantic Layer [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - dbt support
  - dbt tips and tricks
  - dbt VS Code extension features Preview
  - dbt VS Code extension features [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")

dbt-athena==1.9.0
dbt-bigquery==1.9.0
dbt-databricks==1.9.0
dbt-fabric==1.8.8
dbt-postgres==1.9.0
dbt-redshift==1.9.0
dbt-snowflake==1.9.0
dbt-spark==1.9.0
dbt-synapse==1.8.2
dbt-teradata==1.8.2
dbt-trino==1.8.5

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

sources:
  - name: sensitive_source
    database: "{{ env_var('SENSITIVE_SOURCE_DATABASE') }}"
    tables:
      - name: table_with_pii

metrics:
  - name: the metric name # Required
    description: the metric description # Optional
    type: derived # Required
    label: The value that will be displayed in downstream tools #Required
    type_params: # Required
      expr: the derived expression # Required
      metrics: # The list of metrics used in the derived metrics # Required
        - name: the name of the metrics. must reference a metric you have already defined # Required
          alias: optional alias for the metric that you can use in the expr # Optional
          filter: optional filter to apply to the metric # Optional
          offset_window: set the period for the offset window, such as 1 month. This will return the value of the metric one month from the metric time. # Optional

metrics:
  - name: order_gross_profit
    description: Gross profit from each order.
    type: derived
    label: Order gross profit
    type_params:
      expr: revenue - cost
      metrics:
        - name: order_total
          alias: revenue
        - name: order_cost
          alias: cost
  - name: food_order_gross_profit
    label: Food order gross profit
    description: "The gross profit for each food order."
    type: derived
    type_params:
      expr: revenue - cost
      metrics:
        - name: order_total
          alias: revenue
          filter: |
            {{ Dimension('order__is_food_order') }} = True
        - name: order_cost
          alias: cost
          filter: |
            {{ Dimension('order__is_food_order') }} = True
  - name: order_total_growth_mom
    description: "Percentage growth of orders total completed to 1 month ago"
    type: derived
    label: Order total growth % M/M
    type_params:
      expr: (order_total - order_total_prev_month)*100/order_total_prev_month
      metrics: 
        - name: order_total
        - name: order_total
          offset_window: 1 month
          alias: order_total_prev_month

- name: customer_retention
  description: Percentage of customers that are active now and those active 1 month ago
  label: customer_retention
  type_params:
    expr: (active_customers/ active_customers_prev_month)
    metrics:
      - name: active_customers
        alias: current_active_customers
      - name: active_customers
        offset_window: 1 month
        alias: active_customers_prev_month

- name: d7_booking_change
  description: Difference between bookings now and 7 days ago
  type: derived
  label: d7 bookings change
  type_params:
    expr: bookings - bookings_7_days_ago
    metrics:
      - name: bookings
        alias: current_bookings
      - name: bookings
        offset_window: 7 days
        alias: bookings_7_days_ago

bookings - bookings_7_days_ago would be compile as 7438 - 7252 = 186.

dimensions:
  - name: Name of the group that will be visible to the user in downstream tools # Required
    type: Categorical or Time # Required
    label: Recommended adding a string that defines the display value in downstream tools. # Optional
    type_params: Specific type params such as if the time is primary or used as a partition # Required
    description: Same as always # Optional
    expr: The column name or expression. If not provided the default is the dimension name # Optional

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

**Examples:**

Example 1 (unknown):
```unknown
Changelogs:

* [dbt Core 1.9.0](https://github.com/dbt-labs/dbt-core/blob/1.9.latest/CHANGELOG.md#dbt-core-190---december-09-2024)
* [dbt-adapters 1.10.4](https://github.com/dbt-labs/dbt-adapters/blob/main/dbt-adapters/CHANGELOG.md#dbt-adapters-1104---november-11-2024)
* [dbt-common 1.14.0](https://github.com/dbt-labs/dbt-common/blob/main/CHANGELOG.md)
* [dbt-bigquery 1.9.0](https://github.com/dbt-labs/dbt-bigquery/blob/1.9.latest/CHANGELOG.md#dbt-bigquery-190---december-09-2024)
* [dbt-databricks 1.9.0](https://github.com/databricks/dbt-databricks/blob/main/CHANGELOG.md#dbt-databricks-190-december-9-2024)
* [dbt-fabric 1.8.8](https://github.com/microsoft/dbt-fabric/blob/v1.8.latest/CHANGELOG.md)
* [dbt-postgres 1.9.0](https://github.com/dbt-labs/dbt-postgres/blob/main/CHANGELOG.md#dbt-postgres-190---december-09-2024)
* [dbt-redshift 1.9.0](https://github.com/dbt-labs/dbt-redshift/blob/1.9.latest/CHANGELOG.md#dbt-redshift-190---december-09-2024)
* [dbt-snowflake 1.9.0](https://github.com/dbt-labs/dbt-snowflake/blob/1.9.latest/CHANGELOG.md#dbt-snowflake-190---december-09-2024)
* [dbt-spark 1.9.0](https://github.com/dbt-labs/dbt-spark/blob/1.9.latest/CHANGELOG.md#dbt-spark-190---december-10-2024)
* [dbt-synapse 1.8.2](https://github.com/microsoft/dbt-synapse/blob/v1.8.latest/CHANGELOG.md)
* [dbt-teradata 1.8.2](https://github.com/Teradata/dbt-teradata/releases/tag/v1.8.2)
* [dbt-trino 1.8.5](https://github.com/starburstdata/dbt-trino/blob/master/CHANGELOG.md#dbt-trino-185---december-11-2024)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt Product lifecycles

dbt Labs is directly involved with the maintenance of three products:

* dbt Core: The [open-source](https://github.com/dbt-labs/dbt-core) software that’s freely available.
* dbt platform: The cloud-based [SaaS solution](https://www.getdbt.com/signup), originally built on top of dbt Core. We're now introducing dbt's new engine, the dbt Fusion Engine. For more information, refer to [the dbt Fusion engine](https://docs.getdbt.com/docs/fusion.md).
* dbt Fusion Engine: The next-generation dbt engine, substantially faster than dbt Core and has built in SQL comprehension technology to power the next generation of analytics engineering workflows. The dbt Fusion Engine is designed to deliver data teams a lightning-fast development experience, intelligent cost savings, and improved governance.

All dbt features fall into a lifecycle category determined by their availability in the following products:

##### The dbt platform[​](#the-dbt-platform "Direct link to The dbt platform")

dbt features all fall into one of the following categories:

* **Beta:** Beta features are in development and might not be entirely stable; they should be used at the customer’s risk, as breaking changes could occur. Beta features might not be fully documented, technical support is limited, and service level objectives (SLOs) might not be provided. Download the [Beta Features Terms and Conditions](https://docs.getdbt.com/assets/files/beta-tc-740ff696113c89c38a96bb70b968775e.pdf) for more details. If a beta feature is marked `Private`, it must be enabled by dbt Labs, and access is not self-service. If documentation is available, it will include instructions for requesting access.
* **Preview:** Preview features are stable and considered functionally ready for production deployments. Some planned additions and modifications to feature behaviors could occur before they become generally available. New functionality that is not backward compatible could also be introduced. Preview features include documentation, technical support, and service level objectives (SLOs). Features in preview are provided at no extra cost, although they might become paid features when they become generally available. If a preview feature is marked `Private`, it must be enabled by dbt Labs, and access is not self-service. Refer to the feature documentation for instructions on requesting access.
* **Generally available (GA):** Generally available features provide stable features introduced to all qualified dbt accounts. Service level agreements (SLAs) apply to GA features, including documentation and technical support. Certain GA feature availability is determined by the dbt version of the environment. To always receive the latest GA features, ensure your dbt [environments](https://docs.getdbt.com/docs/dbt-cloud-environments.md) are on a supported [Release Track](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md).
* **Deprecated:** Features in this state are no longer being developed or enhanced by dbt Labs. They will continue functioning as-is, and their documentation will persist until their removal date. However, they are no longer subject to technical support.
* **Removed:** Removed features are no longer available on the platform in any capacity.

##### dbt Core[​](#dbt-core "Direct link to dbt Core")

We release dbt Core in the following lifecycle states. Core releases follow semantic versioning, which you can read more about in [About Core versions](https://docs.getdbt.com/docs/dbt-versions/core.md).

* **Unreleased:** We will include this functionality in the next minor version prerelease. However, we make no commitments about its behavior or implementation. As maintainers, we reserve the right to change any part of it, or remove it entirely (with an accompanying explanation.)

* **Prerelease:**

  * **Beta:** The purpose of betas is to provide a first glimpse of the net-new features that will be arriving in this minor version, when it has its final release. The code included in beta should work, without regression from existing functionality, or negative interactions with other released features. Net-new features included in a beta *may be* incomplete or have known edge cases/limitations. Changes included in beta are not “locked,” and the maintainers reserve the right to change or remove (with an explanation).
  * **Release Candidate:** The purpose of a release candidate is to offer a 2-week window for more extensive production-level testing, with the goal of catching regressions before they go live in a final release. Users can believe that features in a Release Candidate will work the same on release day. However, if we do find a significant bug, we do still reserve the right to change or remove the underlying behavior, with a clear explanation.

* **Released:** Ready for use in production.

* **Experimental:** Features we release for general availability, which we believe are usable in their current form, but for which we may document additional caveats.

* **Undocumented:** These are subsets of dbt Core functionality that are internal, not contracted, or intentionally left undocumented. Do not consider this functionality part of that release’s product surface area.

* **Deprecated:** Features in this state are not actively worked on or enhanced by dbt Labs and will continue to function as-is until their removal date.

* **Removed:** Removed features no longer have any level of product functionality or platform support.

##### dbt Fusion engine[​](#dbt-fusion-engine "Direct link to dbt Fusion engine")

The dbt Fusion Engine and [VS Code extension](https://docs.getdbt.com/docs/about-dbt-extension.md) are currently in preview for local installations and beta in dbt.

* **Beta:** Beta features are still in development and are only available to select customers. Beta features are incomplete and might not be entirely stable; they should be used at the customer’s risk, as breaking changes could occur. Beta features might not be fully documented, technical support is limited, and service level objectives (SLOs) might not be provided. Download the [Beta Features Terms and Conditions](https://docs.getdbt.com/assets/files/beta-tc-740ff696113c89c38a96bb70b968775e.pdf) for more details.
* **Preview:** Preview features are stable and considered functionally ready for production deployments that are using supported features and do not depend on deprecated functionality. For more about the status of features and functionality, the [Fusion Diaries](https://github.com/dbt-labs/dbt-fusion/discussions/categories/announcements) contain the most recent updates.
* **Path to Generally available (GA):** Learn what's required for the dbt Fusion engine to reach GA in our [Path to GA](https://docs.getdbt.com/blog/dbt-fusion-engine-path-to-ga) blog post.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt release notes

dbt release notes for recent and historical changes. Release notes fall into one of the following categories:

* **New:** New products and features
* **Enhancement:** Performance improvements and feature enhancements
* **Fix:** Bug and security fixes
* **Behavior change:** A change to existing behavior that doesn't fit into the other categories, such as feature deprecations or changes to default settings

Release notes are grouped by month for both multi-tenant and virtual private cloud (VPC) environments.

#### October 2025[​](#october-2025 "Direct link to October 2025")

* **New**: The [docs.getdbt.com](http://docs.getdbt.com/) documentation site has introduced an LLM Context menu on all product documentation and guide pages. This menu provides users with quick options to interact with the current page using LLMs. You can can now:

  <!-- -->

  * Copy the page as raw Markdown — This makes it easier to reference or reuse documentation content.
  * Open the page directly in ChatGPT or Claude — This redirects you to a chat with the LLM and automatically loads a message asking it to read the page, helping you start a conversation with context from the page.

  [![LLM Context menu on documentation pages](/img/llm-menu.png?v=2 "LLM Context menu on documentation pages")](#)LLM Context menu on documentation pages

* **Enhancement**: The CodeGenCodeLen feature has been re-introduced to the Studio IDE. This feature was [temporarily](#pre-coalesce) removed in the previous release due to compatibility issues.

##### Coalesce 2025 announcements[​](#coalesce-2025-announcements "Direct link to Coalesce 2025 announcements")

The following features are new or enhanced as part of [dbt's Coalesce analytics engineering conference](https://coalesce.getdbt.com/event/21662b38-2c17-4c10-9dd7-964fd652ab44/summary) from October 13-16, 2025:

* **New**: The [dbt MCP server](https://docs.getdbt.com/docs/dbt-ai/about-mcp.md) is now generally available (GA). For more information on the dbt MCP server and dbt Agents, refer to the [Announcing dbt Agents and the remote dbt MCP Server: Trusted AI for analytics](https://www.getdbt.com/blog/dbt-agents-remote-dbt-mcp-server-trusted-ai-for-analytics) blog post.

* **Private preview**: The [dbt platform (powered by Fusion)](https://docs.getdbt.com/docs/dbt-versions/upgrade-dbt-version-in-cloud.md#dbt-fusion-engine) is now in private preview. If you have any questions, please reach out to your account manager.
  <!-- -->
  * [About data platform connections](https://docs.getdbt.com/docs/cloud/connect-data-platform/about-connections.md) lists all available dbt platform connections on Fusion and the supported authentication methods per connection.

* **New**: Fusion‑specific configuration is now available for BigQuery, Databricks, Redshift, and Snowflake. For more information, see [Connect Fusion to your data platform](https://docs.getdbt.com/docs/fusion/connect-data-platform-fusion/profiles.yml.md).

* **Alpha**: The `dbt-salesforce` adapter is available via the dbt Fusion Engine CLI. Note that this connection is in the Alpha product stage and is not production-ready. For more information, see [Salesforce Data Cloud setup](https://docs.getdbt.com/docs/fusion/connect-data-platform-fusion/salesforce-data-cloud-setup.md).

* **Private preview**: [State-aware orchestration](https://docs.getdbt.com/docs/deploy/state-aware-about.md) is now in private preview!

  <!-- -->

  * **New**: You can now [enable state-aware orchestration](https://docs.getdbt.com/docs/deploy/state-aware-setup.md) by selecting **Enable Fusion cost optimization features** in your job settings. Previously, you had to disable **Force node selection** to enable state-aware orchestration.

  * **Private beta**: The [Efficient Testing feature](https://docs.getdbt.com/docs/deploy/state-aware-about.md#efficient-testing-in-state-aware-orchestration) is now available in private beta. This feature reduces warehouse costs by avoiding redundant data tests and combining multiple tests in a single query.

  * **New**: To improve visibility into state‑aware orchestration and provide better control when you need to reset cached state, the following [UI enhancements](https://docs.getdbt.com/docs/deploy/state-aware-interface.md) are introduced:

    <!-- -->

    * **Models built and reused chart** on your **Account home**
    * New charts in the **Overview** section of your job that display **Recent runs**, **Total run duration**, **Models built**, and **Models reused**
    * A new structure to view logs grouped by models, with a **Reused** tab to quickly find reused models
    * **Reused** tag in **Latest status** lineage lens to see reused models in your DAG
    * **Clear cache** button on the **Environments** page to reset cached state when needed

* **New**: [dbt Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md) is now generally available (GA)!

  <!-- -->

  * **Private beta**: The [Analyst agent](https://docs.getdbt.com/docs/explore/navigate-dbt-insights.md#dbt-copilot) is now available in dbt Insights. The Analyst agent is a conversational AI feature where you can ask natural language prompts and receive analysis in real-time. For more information, see [Analyze data with the Analyst agent](https://docs.getdbt.com/docs/cloud/use-dbt-copilot.md#analyze-data-with-the-analyst-agent).
  * **Beta**: dbt Insights now has a [Query Builder](https://docs.getdbt.com/docs/explore/navigate-dbt-insights.md#query-builder), where you can build SQL queries against the Semantic Layer without writing SQL code. It guides you in creating queries based on available metrics, dimensions, and entities.
  * **Enhancement**: In [dbt Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md), projects upgraded to the [dbt Fusion Engine](https://docs.getdbt.com/docs/fusion.md) get [Language Server Protocol (LSP) features](https://docs.getdbt.com/docs/explore/navigate-dbt-insights.md#lsp-features) and their compilation running on Fusion.

* **New**: [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md) is now developed and maintained as part of the [Open Semantic Interchange (OSI)](https://www.snowflake.com/en/blog/open-semantic-interchange-ai-standard/) initiative, and is distributed under the [Apache 2.0 license](https://github.com/dbt-labs/metricflow/blob/main/LICENSE). For more information, see the blog post about [Open sourcing MetricFlow](https://www.getdbt.com/blog/open-source-metricflow-governed-metrics).

##### Pre-Coalesce[​](#pre-coalesce "Direct link to Pre-Coalesce")

* **Behavior change**: dbt platform [access URLs](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses.md) for accounts in the US multi-tenant (US MT) region are transitioning from `cloud.getdbt.com` to dedicated domains on `dbt.com` (for example, `us1.dbt.com`). Users will be automatically redirected, which means no action is required. EMEA and APAC MT accounts are not impacted by this change and will be updated by the end of November 2025.

  Organizations that use network allow-listing should add `YOUR_ACCESS_URL.dbt.com` to their allow list (for example, if your access URL is `ab123.us1.dbt.com`, add the entire domain `ab123.us1.dbt.com` to your allow list).

  All OAuth, Git, and public API integrations will continue to work with the previous domain. View the updated access URL in dbt platform's **Account settings** page.

  For questions, contact <support@getdbt.com>.

* **Enhancement**:

  * **Fusion MCP tools** — Added Fusion tools that support `compile_sql` and `get_column_lineage` (Fusion-exclusive) for both [Remote](https://docs.getdbt.com/docs/dbt-ai/about-mcp.md#fusion-tools-remote) and [Local](https://docs.getdbt.com/docs/dbt-ai/about-mcp.md#fusion-tools-local) usage. Remote Fusion tools defer to your prod environment by default (set with `x-dbt-prod-environment-id`); you can disable deferral with `x-dbt-fusion-disable-defer=true`. Refer to [set up remote MCP](https://docs.getdbt.com/docs/dbt-ai/setup-remote-mcp.md) for more info.
  * **Local MCP OAuth** — You can now authenticate the local dbt MCP server to the dbt platform with OAuth (supported docs for [Claude](https://docs.getdbt.com/docs/dbt-ai/integrate-mcp-claude.md), [Cursor](https://docs.getdbt.com/docs/dbt-ai/integrate-mcp-cursor.md), and [VS Code](https://docs.getdbt.com/docs/dbt-ai/integrate-mcp-vscode.md)), reducing local secret management and standardizing setup. Refer to [dbt platform authentication](https://docs.getdbt.com/docs/dbt-ai/setup-local-mcp.md#dbt-platform-authentication) for more information.

* **Behavior change**: The CodeGenCodeLens feature for creating models from your sources with a click of a button has been temporarily removed from the Studio IDE due to compatibility issues. We plan to reintroduce this feature in the near future for both the IDE and the VS Code extension.

#### September 2025[​](#september-2025 "Direct link to September 2025")

* **Fix**: Improved how [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md) handles [offset metrics](https://docs.getdbt.com/docs/build/derived.md) for more accurate results when querying time-based data. MetricFlow now joins data *after* aggregation when the query grain matches the offset grain. Previously, when querying offset metrics, the offset join was applied *before* aggregation, which could exclude some values from the total time period.

#### August 2025[​](#august-2025 "Direct link to August 2025")

* **Fix**: Resolved a bug that caused [saved query](https://docs.getdbt.com/docs/build/saved-queries.md) exports to fail during `dbt build` with `Unable to get saved_query` errors.
* **New**: The Semantic Layer GraphQL API now has a [`queryRecords`](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md#query-records) endpoint. With this endpoint, you can view the query history both for Insights and Semantic Layer queries.
* **Fix**: Resolved a bug that caused Semantic Layer queries with a trailing whitespace to produce an error. This issue mostly affected [Push.ai](https://docs.push.ai/data-sources/semantic-layers/dbt) users and is fixed now.
* **New**: You can now use [personal access tokens (PATs)](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md) to authenticate in the Semantic Layer. This enables user-level authentication and reduces the need for sharing tokens between users. When you authenticate using PATs, queries are run using your personal development credentials. For more information, see [Set up the dbt Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md).

#### July 2025[​](#july-2025 "Direct link to July 2025")

* **New**: The [Tableau Cloud](https://www.tableau.com/products/cloud-bi) integration with Semantic Layer is now available. For more information, see [Tableau](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/tableau.md).
* **Preview**: The [Semantic Layer Power BI integration](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/power-bi.md) is now available in Preview.
* **Enhancement:** You can now use `limit` and `order_by` parameters when creating [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md).
* **Enhancement:** Users assigned IT [licenses](https://docs.getdbt.com/docs/cloud/manage-access/seats-and-users.md) can now edit and manage [global connections settings](https://docs.getdbt.com/docs/cloud/connect-data-platform/about-connections.md#connection-management).
* **New**: Paginated [GraphQL](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md) endpoints for metadata queries in Semantic Layer are now available. This improves integration load times for large manifests. For more information, see [Metadata calls](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md#metadata-calls).

#### June 2025[​](#june-2025 "Direct link to June 2025")

* **New**: [System for Cross-Domain Identity Management](https://docs.getdbt.com/docs/cloud/manage-access/scim.md#scim-configuration-for-entra-id) (SCIM) through Microsoft Entra ID is now GA. Also available on legacy Enterprise plans.
* **Enhancement:** You can now set the [compilation environment](https://docs.getdbt.com/docs/explore/access-dbt-insights.md#set-jinja-environment) to control how Jinja functions are rendered in dbt Insights.
* **Beta**: The dbt Fusion engine supports the BigQuery adapter in beta.
* **New:** You can now view the history of settings changes for [projects](https://docs.getdbt.com/docs/cloud/account-settings.md), [environments](https://docs.getdbt.com/docs/dbt-cloud-environments.md), and [jobs](https://docs.getdbt.com/docs/deploy/deploy-jobs.md).
* **New:** Added support for the latest version of BigQuery credentials in Semantic Layer and MetricFlow.
* **New:** Snowflake External OAuth is now supported for Semantic Layer queries. Snowflake connections that use External OAuth for user credentials can now emit queries for Insights, Cloud CLI, and Studio IDE through the Semantic Layer Gateway. This enables secure, identity-aware access via providers like Okta or Microsoft Entra ID.
* **New:** You can now [download your managed Git repo](https://docs.getdbt.com/docs/cloud/git/managed-repository.md#download-managed-repository) from the dbt platform.
* **New**: The Semantic Layer now supports Trino as a data platform. For more details, see [Set up the Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md).
* **New**: The dbt Fusion engine supports Databricks in beta.
* **Enhancement**: Group owners can now specify multiple email addresses for model-level notifications, enabling broader team alerts. Previously, only a single email address was supported. Check out the [Configure groups](https://docs.getdbt.com/docs/deploy/model-notifications.md#configure-groups) section to learn more.
* **New**: The Semantic Layer GraphQL API now has a [`List a saved query`](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md#list-a-saved-query) endpoint.

#### May 2025[​](#may-2025 "Direct link to May 2025")

##### 2025 dbt Launch Showcase[​](#2025-dbt-launch-showcase "Direct link to 2025 dbt Launch Showcase")

The following features are new or enhanced as part of our [dbt Launch Showcase](https://www.getdbt.com/resources/webinars/2025-dbt-cloud-launch-showcase) on May 28th, 2025:

* **New**: The dbt Fusion engine is the brand new dbt engine re-written from the ground up to provide incredible speed, cost-savings tools, and comprehensive SQL language tools. The dbt Fusion engine is now available in beta for Snowflake users.

  <!-- -->

  * Read more [about Fusion](https://docs.getdbt.com/docs/fusion.md).
  * Understand what actions you need to take to get your projects Fusion-ready with the [upgrade guide](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-fusion.md).
  * Begin testing today with the [quickstart guide](https://docs.getdbt.com/guides/fusion.md).
  * Know [where we're headed with the dbt Fusion engine](https://getdbt.com/blog/where-we-re-headed-with-the-dbt-fusion-engine).

* **New**: The dbt VS Code extension is a powerful new tool that brings the speed and productivity of the dbt Fusion engine into your Visual Studio Code editor. This is a free download that will forever change your dbt development workflows. The dbt VS Code extension is now available as beta [alongside Fusion](https://getdbt.com/blog/get-to-know-the-new-dbt-fusion-engine-and-vs-code-extension). Check out the [installation instructions](https://docs.getdbt.com/docs/install-dbt-extension.md) and read more [about the features](https://docs.getdbt.com/docs/about-dbt-extension.md) to get started enhancing your dbt workflows today!

* **New**: dbt Explorer is now Catalog! Learn more about the change [here](https://getdbt.com/blog/updated-names-for-dbt-platform-and-features).

  <!-- -->

  * dbt's Catalog, global navigation provides a search experience that lets you find dbt resources across all your projects, as well as non-dbt resources in Snowflake.
  * External metadata ingestion allows you to connect directly to your data warehouse, giving you visibility into tables, views, and other resources that aren't defined in dbt.

* **New**: [dbt Canvas is now generally available](https://getdbt.com/blog/dbt-canvas-is-ga) (GA). Canvas is the intuitive visual editing tool that enables anyone to create dbt models with an easy to understand drag-and-drop interface. Read more [about Canvas](https://docs.getdbt.com/docs/cloud/canvas.md) to begin empowering your teams to build more, faster!

* **New**: [State-aware orchestration](https://docs.getdbt.com/docs/deploy/state-aware-about.md) is now in beta! Every time a new job in Fusion runs, state-aware orchestration automatically determines which models to build by detecting changes in code or data.

* **New**: With Hybrid Projects, your organization can adopt complementary dbt Core and dbt Cloud workflows and seamlessly integrate these workflows by automatically uploading dbt Core artifacts into dbt Cloud. [Hybrid Projects](https://docs.getdbt.com/docs/deploy/hybrid-projects.md) is now available as a preview to [dbt Enterprise accounts](https://www.getdbt.com/pricing).

* **New**: [System for Cross-Domain Identity Management (SCIM)](https://docs.getdbt.com/docs/cloud/manage-access/scim.md) through Okta is now GA.

* **New**: dbt now acts as a [Model Context Protocol](https://docs.getdbt.com/docs/dbt-ai/about-mcp.md) (MCP) server, allowing seamless integration of AI tools with data warehouses through a standardized framework.

* **New**: The [quickstart guide for data analysts](https://docs.getdbt.com/guides/analyze-your-data.md) is now available. With dbt, data analysts can use built-in, AI-powered tools to build governed data models, explore how they’re built, and run their own analysis.

* **New**: You can view your [usage metering and limiting in dbt Copilot](https://docs.getdbt.com/docs/cloud/billing.md#dbt-copilot-usage-metering-and-limiting) on the billing page of your dbt Cloud account.

* **New**: You can use Copilot to create a `dbt-styleguide.md` for dbt projects. The generated style guide template includes SQL style guidelines, model organization and naming conventions, model configurations and testing practices, and recommendations to enforce style rules. For more information, see [Copilot style guide](https://docs.getdbt.com/docs/cloud/copilot-styleguide.md).

* **New**: Copilot chat is an interactive interface within the Studio IDE where you can generate SQL code from natural language prompts and ask analytics-related questions. It integrates contextual understanding of your dbt project and assists in streamlining SQL development. For more information, see [Copilot chat](https://docs.getdbt.com/docs/cloud/copilot-chat-in-studio.md).

* **New**: Leverage dbt Copilot to generate SQL queries in [Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md) from natural language prompts, enabling efficient data exploration within a context-aware interface.

* **New**: The dbt platform Cost management dashboard is now available as a preview for Snowflake users on Enterprise and Enteprise Plus plans. Gain valuable insights into your warehouse spend with the comprehensive and interactive dashboard. Read more [about it](https://docs.getdbt.com/docs/cloud/cost-management.md) to get started with your cost savings analysis today!

* **New**: Apache Iceberg catalog integration support is now available on Snowflake and BigQuery! This is essential to making your dbt Mesh interoperable across platforms, built on Iceberg. Read more about [Iceberg](https://docs.getdbt.com/docs/mesh/iceberg/apache-iceberg-support.md) to begin creating Iceberg tables.

* **Update**: Product renaming and other changes. For more information, refer to [Updated names for dbt platform and features](https://getdbt.com/blog/updated-names-for-dbt-platform-and-features).

  <!-- -->

   Product names key

  * Canvas (previously Visual Editor)
  * Catalog (previously Explorer)
  * Copilot
  * Cost Management
  * dbt Fusion engine
  * Insights
  * Mesh
  * Orchestrator
  * Studio IDE (previously Cloud IDE)
  * Semantic Layer
  * Pricing plan changes. For more information, refer to [One dbt](https://www.getdbt.com/product/one-dbt).

#### April 2025[​](#april-2025 "Direct link to April 2025")

* **Enhancement**: The [Python SDK](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-python.md) now supports lazy loading for large fields for `dimensions`, `entities`, and `measures` on `Metric` objects. For more information, see [Lazy loading for large fields](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-python.md#lazy-loading-for-large-fields).
* **Enhancement**: The Semantic Layer now supports SSH tunneling for [Postgres](https://docs.getdbt.com/docs/cloud/connect-data-platform/connect-postgresql-alloydb.md) or [Redshift](https://docs.getdbt.com/docs/cloud/connect-data-platform/connect-redshift.md) connections. Refer to [Set up the Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md) for more information.
* **Behavior change**: Users assigned the [`job admin` permission set](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions.md#job-admin) now have access to set up integrations for projects, including the [Tableau](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures-tableau.md) integration to populate downstream exposures.

#### March 2025[​](#march-2025 "Direct link to March 2025")

* **Behavior change**: As of March 31st, 2025, dbt Core versions 1.0, 1.1, and 1.2 have been deprecated from dbt. They are no longer available to select as versions for dbt projects. Workloads currently on these versions will be automatically upgraded to v1.3, which may cause new failures.
* **Enhancement**: [Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md) users on single-tenant configurations no longer need to contact their account representative to enable this feature. Setup is now self-service and available across all tenant configurations.
* **New**: The Semantic Layer now supports Postgres as a data platform. For more details on how to set up the Semantic Layer for Postgres, see [Set up the Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md).
* **New**: New [environment variable default](https://docs.getdbt.com/docs/build/environment-variables.md#dbt-cloud-context) `DBT_CLOUD_INVOCATION_CONTEXT`.
* **Enhancement**: Users assigned [read-only licenses](https://docs.getdbt.com/docs/cloud/manage-access/about-user-access.md#licenses) are now able to view the [Deploy](https://docs.getdbt.com/docs/deploy/deployments.md) section of their dbt account and click into the individual sections but not edit or otherwise make any changes.

###### dbt Developer day[​](#dbt-developer-day "Direct link to dbt Developer day")

The following features are new or enhanced as part of our [dbt Developer day](https://www.getdbt.com/resources/webinars/dbt-developer-day) on March 19th and 20th, 2025:

* **New**: The [`--sample` flag](https://docs.getdbt.com/docs/build/sample-flag.md), now available for the `run` and `build` commands, helps reduce build times and warehouse costs by running dbt in sample mode. It generates filtered refs and sources using time-based sampling, allowing developers to validate outputs without building entire models.
* **New**: Copilot, an AI-powered assistant, is now generally available in the Cloud IDE for all dbt Enterprise accounts. Check out [Copilot](https://docs.getdbt.com/docs/cloud/dbt-copilot.md) for more information.

###### Also available this month[​](#also-available-this-month "Direct link to Also available this month")

* **New**: Bringing your own [Azure OpenAI key](https://docs.getdbt.com/docs/cloud/enable-dbt-copilot.md#bringing-your-own-openai-api-key-byok) for [Copilot](https://docs.getdbt.com/docs/cloud/dbt-copilot.md) is now generally available. Your organization can configure Copilot to use your own Azure OpenAI keys, giving you more control over data governance and billing.
* **New**: The Semantic Layer supports Power BI as a [partner integration](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md), available in private beta. To join the private beta, please reach out to your account representative. Check out the [Power BI](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/power-bi.md) integration for more information.
* **New**: [dbt release tracks](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md) are Generally Available. Depending on their plan, customers may select among the Latest, Compatible, or Extended tracks to manage the update cadences for development and deployment environments.
* **New:** The dbt-native integration with Azure DevOps now supports [Entra ID service principals](https://docs.getdbt.com/docs/cloud/git/setup-service-principal.md). Unlike a services user, which represents a real user object in Entra ID, the service principal is a secure identity associated with your dbt app to access resources in Azure unattended. Please [migrate your service user](https://docs.getdbt.com/docs/cloud/git/setup-service-principal.md#migrate-to-service-principal) to a service principal for Azure DevOps as soon as possible.

#### February 2025[​](#february-2025 "Direct link to February 2025")

* **Enhancement**: The [Python SDK](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-python.md) added a new timeout parameter to Semantic Layer client and to underlying GraphQL clients to specify timeouts. Set a timeout number or use the `total_timeout` parameter in the global `TimeoutOptions` to control connect, execute, and close timeouts granularly. `ExponentialBackoff.timeout_ms` is now deprecated.

* **New**: The [Azure DevOps](https://docs.getdbt.com/docs/cloud/git/connect-azure-devops.md) integration for Git now supports [Entra service principal apps](https://docs.getdbt.com/docs/cloud/git/setup-service-principal.md) on dbt Enterprise accounts. Microsoft is enforcing MFA across user accounts, including service users, which will impact existing app integrations. This is a phased rollout, and dbt Labs recommends [migrating to a service principal](https://docs.getdbt.com/docs/cloud/git/setup-service-principal.md#migrate-to-service-principal) on existing integrations once the option becomes available in your account.

* **New**: Added the `dbt invocation` command to the [dbt CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md). This command allows you to view and manage active invocations, which are long-running sessions in the dbt CLI. For more information, see [dbt invocation](https://docs.getdbt.com/reference/commands/invocation.md).

* **New**: Users can now switch themes directly from the user menu, available [in Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles.md#dbt-cloud). We have added support for **Light mode** (default), **Dark mode**, and automatic theme switching based on system preferences. The selected theme is stored in the user profile and will follow users across all devices.
  <!-- -->
  * Dark mode is currently available on the Developer plan and will be available for all [plans](https://www.getdbt.com/pricing) in the future. We’ll be rolling it out gradually, so stay tuned for updates. For more information, refer to [Change your dbt theme](https://docs.getdbt.com/docs/cloud/about-cloud/change-your-dbt-cloud-theme.md).

* **Fix**: Semantic Layer errors in the Cloud IDE are now displayed with proper formatting, fixing an issue where newlines appeared broken or difficult to read. This fix ensures error messages are more user-friendly and easier to parse.

* **Fix**: Fixed an issue where [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md) with no [exports](https://docs.getdbt.com/docs/build/saved-queries.md#configure-exports) would fail with an `UnboundLocalError`. Previously, attempting to process a saved query without any exports would cause an error due to an undefined relation variable. Exports are optional, and this fix ensures saved queries without exports don't fail.

* **New**: You can now query metric alias in Semantic Layer [GraphQL](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md) and [JDBC](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md) APIs.

  <!-- -->

  * For the JDBC API, refer to [Query metric alias](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md#query-metric-alias) for more information.
  * For the GraphQL API, refer to [Query metric alias](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql.md#query-metric-alias) for more information.

* **Enhancement**: Added support to automatically refresh access tokens when Snowflake's SSO connection expires. Previously, users would get the following error: `Connection is not available, request timed out after 30000ms` and would have to wait 10 minutes to try again.

* **Enhancement**: The [`dbt_version` format](https://docs.getdbt.com/reference/commands/version.md#versioning) in dbt Cloud now better aligns with [semantic versioning rules](https://semver.org/). Leading zeroes have been removed from the month and day (`YYYY.M.D+<suffix>`). For example:

  <!-- -->

  * New format: `2024.10.8+996c6a8`
  * Previous format: `2024.10.08+996c6a8`

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt Semantic Layer architecture

The Semantic Layer allows you to define metrics and use various interfaces to query them. The Semantic Layer does the heavy lifting to find where the queried data exists in your data platform and generates the SQL to make the request (including performing joins).

[![This diagram shows how the dbt Semantic Layer works with your data stack.](/img/docs/dbt-cloud/semantic-layer/sl-concept.png?v=2 "This diagram shows how the dbt Semantic Layer works with your data stack.")](#)This diagram shows how the dbt Semantic Layer works with your data stack.

[![The diagram displays how your data flows using the dbt Semantic Layer and the variety of integration tools it supports.](/img/docs/dbt-cloud/semantic-layer/sl-architecture.jpg?v=2 "The diagram displays how your data flows using the dbt Semantic Layer and the variety of integration tools it supports.")](#)The diagram displays how your data flows using the dbt Semantic Layer and the variety of integration tools it supports.

#### Components[​](#components "Direct link to Components")

The Semantic Layer includes the following components:

| Components                                                                                | Information                                                                                                                                                                                                                                                                        | dbt Core users | Developer plans | Starter plans | Enterprise-tier plans | License                                                                        |
| ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- | --------------- | ------------- | --------------------- | ------------------------------------------------------------------------------ |
| **[MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md)**                  | MetricFlow in dbt allows users to centrally define their semantic models and metrics with YAML specifications.                                                                                                                                                                     | ✅             | ✅              | ✅            | ✅                    | [Apache 2.0 license](https://github.com/dbt-labs/metricflow/blob/main/LICENSE) |
| **dbt Semantic interfaces**                                                               | A configuration spec for defining metrics, dimensions, how they link to each other, and how to query them. The [dbt-semantic-interfaces](https://github.com/dbt-labs/dbt-semantic-interfaces) is available under Apache 2.0.                                                       | ❌             | ❌              | ✅            | ✅                    | Proprietary, Cloud (Starter & Enterprise)                                      |
| **Service layer**                                                                         | Coordinates query requests and dispatching the relevant metric query to the target query engine. This is provided through dbt and is available to all users on dbt version 1.6 or later. The service layer includes a Gateway service for executing SQL against the data platform. | ❌             | ❌              | ✅            | ✅                    | Proprietary, Cloud (Starter, Enterprise, Enterprise+)                          |
| **[Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md)** | The interfaces allow users to submit metric queries using GraphQL and JDBC APIs. They also serve as the foundation for building first-class integrations with various tools.                                                                                                       | ❌             | ❌              | ✅            | ✅                    | Proprietary, Cloud (Starter, Enterprise, Enterprise+)                          |

#### Feature comparison[​](#feature-comparison "Direct link to Feature comparison")

The following table compares the features available in dbt and source available in dbt Core:

| Feature                                                                            | MetricFlow Source available | Semantic Layer with dbt |
| ---------------------------------------------------------------------------------- | --------------------------- | ----------------------- |
| Define metrics and semantic models in dbt using the MetricFlow spec                | ✅                          | ✅                      |
| Generate SQL from a set of config files                                            | ✅                          | ✅                      |
| Query metrics and dimensions through the command line interface (CLI)              | ✅                          | ✅                      |
| Query dimension, entity, and metric metadata through the CLI                       | ✅                          | ✅                      |
| Query metrics and dimensions through semantic APIs (ADBC, GQL)                     | ❌                          | ✅                      |
| Connect to downstream integrations (Tableau, Hex, Mode, Google Sheets, and so on.) | ❌                          | ✅                      |
| Create and run Exports to save metrics queries as tables in your data platform.    | ❌                          | ✅                      |

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Semantic Layer FAQs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-faqs.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt Semantic Layer FAQs

The [Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md) is a dbt offering that allows users to centrally define their metrics within their dbt project using [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md).

The Semantic Layer offers:

* Dynamic SQL generation to compute metrics
* APIs to query metrics and dimensions
* First-class [integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md) to query those centralized metrics in downstream tools

The Semantic Layer is powered by MetricFlow, which is a source-available component.

#### Overview of the dbt Semantic Layer[​](#overview-of-the-dbt-semantic-layer "Direct link to Overview of the dbt Semantic Layer")

 What are the main benefits of using the dbt Semantic Layer?

The primary value of the dbt Semantic Layer is to centralize and bring consistency to your metrics across your organization. Additionally, it allows you to:

* **Meet your users where they are** by being agnostic to where your end users consume data through the supporting of different APIs for integrations.
* **Optimize costs** by spending less time preparing data for consumption.
* **Simplify your code** by not duplicating metric logic and allowing MetricFlow to perform complex calculations for you.
* **Empower stakeholders** with rich context and flexible, yet governed experiences.

[![This diagram shows how the dbt Semantic Layer works with your data stack.](/img/docs/dbt-cloud/semantic-layer/sl-concept.png?v=2 "This diagram shows how the dbt Semantic Layer works with your data stack.")](#)This diagram shows how the dbt Semantic Layer works with your data stack.

 What's the main difference between the dbt Semantic Layer and dbt Metrics?

dbt Metrics is the now-deprecated dbt package that was used to define metrics within dbt. dbt Metrics has been replaced with [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md), a more flexible and powerful engine, which powers the foundation of the dbt Semantic Layer today.

MetricFlow introduces SQL generation to the dbt Semantic Layer and offers more advanced capabilities than dbt Metrics, for example:

* **Query construction** — MetricFlow iteratively constructs queries using a dataflow plan, our internal DAG for generating SQL. By comparison, dbt Metrics relied on templated Jinja to construct SQL.
* **Joins** — MetricFlow also has a sophisticated way of handling joins, which dbt Metrics did not support. With MetricFlow you can effortlessly access all valid dimensions for your metrics on the fly, even when they are defined in different semantic models.

 Is there a dbt Semantic Layer discussion hub?

Yes, absolutely! Join the [dbt Slack community](https://app.slack.com/client/T0VLPD22H) and [#dbt-cloud-semantic-layer](https://getdbt.slack.com/archives/C046L0VTVR6) slack channel for all things related to the dbt Semantic Layer.

 How does the dbt Semantic Layer fit with different modeling approaches (Medallion, Data Vault, Dimensional modeling)?

The dbt Semantic Layer is flexible enough to work with many common modeling approaches. It references dbt models, which means how you configure your Semantic Layer will mirror the modeling approach you've taken with the underlying data.

The primary consideration is the flexibility and performance of the underlying queries. For example:

* A star schema data model offers more flexibility for dimensions that are available for a given metric, but will require more joins.
* A fully denormalized data model is simpler, will be materialized to a specific grain, but won’t be able to join to other tables.

While the dbt Semantic Layer will work for both cases, it's best to allow MetricFlow do handle some level of denormalization for you in order to provide more flexibility to metric consumers.

 How is the dbt Semantic Layer priced?

The dbt Semantic Layer measures usage in distinct 'Queried Metrics'. Refer to the [Billing](https://docs.getdbt.com/docs/cloud/billing.md#what-counts-as-a-queried-metric) to learn more about pricing.

#### Availability[​](#availability "Direct link to Availability")

 What data platforms are supported by the dbt Semantic Layer?

The dbt Semantic Layer supports the following data platforms:

* Snowflake
* BigQuery
* Databricks
* Redshift
* Postgres
* Trino

Support for other data platforms, such as Fabric, isn't available at this time. If you're interested in using the dbt Semantic Layer with a data platform not on the list, please [contact us](https://www.getdbt.com/get-started).

 Do I need to be on a specific version of dbt to use dbt Semantic Layer?

Yes, the dbt Semantic Layer is compatible with [dbt v1.6 or higher](https://docs.getdbt.com/docs/dbt-versions/upgrade-dbt-version-in-cloud.md).

 Does dbt Semantic Layer require a specific dbt plan?

Yes, dbt [Starter, Enterprise, or Enterprise+](https://www.getdbt.com/pricing) plan customers can access the dbt Semantic Layer. Certain features like caching and using multiple credentials are available for Enterprise and Enterprise+ plans.

 Is there a way to leverage dbt Semantic Layer capabilities in dbt Core?

The dbt Semantic Layer is proprietary to dbt, however some components of it are open-source. dbt Core users can use MetricFlow features, like defining metrics in their projects, without a dbt plan.

dbt Core users can also query their semantic layer locally using the command line. However, they won't be able to use the [APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) or [available integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md) to access metrics dynamically.

 Is there a solution or licensing path for an organization that doesn't use dbt for pipelining, but might like to implement the dbt Semantic Layer?

If you're interested in the this type of implementation, please reach out to us [here](https://www.getdbt.com/get-started).

#### How does the dbt Semantic Layer work?[​](#how-does-the-dbt-semantic-layer-work "Direct link to How does the dbt Semantic Layer work?")

 Why is the dbt Semantic Layer better than using tables or dbt models to calculate metrics?

You can use tables and dbt models to calculate metrics as an option, but it's a static approach that is rigid and cumbersome to maintain. That’s because metrics are seldom useful on their own: they usually need dimensions, grains, and attributes for business users to analyze (or slice and dice) data effectively.

If you create a table with a metric, you’ll need to create numerous other tables derived from that table to show the desired metric cut by the desired dimension or time grain. Mature data models have thousands of dimensions, so you can see how this will quickly result in unnecessary duplication, maintenance, and costs. It's also incredibly hard to predict all the slices of data that a user is going to need ahead of time.

With the dbt Semantic Layer, you don’t need to pre-join or build any tables; rather, you can simply add a few lines of code to your semantic model, and that data will only be computed upon request.

[![This diagram shows how the dbt Semantic Layer works with your data stack.](/img/docs/dbt-cloud/semantic-layer/sl-concept.png?v=2 "This diagram shows how the dbt Semantic Layer works with your data stack.")](#)This diagram shows how the dbt Semantic Layer works with your data stack.

 Do I materialize anything when I define a semantic model?

No, you don't. When querying the dbt Semantic Layer through the [Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md), you're not materializing any data by default.

The dbt Semantic Layer dynamically computes the metric using the underlying data tables. Then it returns the output to the end user.

 Is the dbt Semantic Layer a physical copy of your data stored on your data warehouse?

The dbt Semantic Layer does not store a physical copy of your data. It uses underlying tables to construct or compute the requested output.

 How does the Semantic Layer handle data?

The dbt Semantic Layer is part of the dbt platform. It allows data teams to define metrics once, centrally, and access them from any integrated analytics tool, ensuring consistent answers across diverse datasets. In providing this service, dbt Labs permits clients to access Semantic Layer metrics. Client data passes through the Semantic Layer on the way back from the data warehouse.

dbt Labs handles this in a secure way using encryption and authentication from the client’s data warehouse. In certain cases, such data may be cached on dbt Labs system ephemerally (data is not persistently stored).

dbt Labs employees cannot access cached data during normal business operations and must have a business need and/or direct manager approval for access to the underlying infrastructure. Access would only be when necessary for providing a client services and never with the purpose of enriching dbt Labs.

No client warehouse data is retained on dbt Labs's systems. We offer a caching solution to optimize query performance. The caching feature uses client data warehouse storage rather than being stored on dbt Labs’s systems. In addition, this feature is activated only through a client opt-in. Therefore, caching is always in client hands and at client discretion

 Does our agreement, the Terms of Service (ToS) for dbt, apply to the Semantic Layer?

Yes it does.

 Where is MetricFlow hosted? How do queries pass through MetricFlow and dbt and back to the end user?

MetricFlow is hosted in dbt. Requests from the [Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) are routed from our API gateway to MetricFlow, which generates the SQL to compute what's requested by the user. MetricFlow hands the SQL back to our gateway, which then executes it against the data platform.

 How do I configure the dbt Semantic Layer?

1. You define [semantic models](https://docs.getdbt.com/docs/build/semantic-models.md) in YAML files that describe your data, including entities (for joins), measures (with aggregation types as a building block to your metrics), and dimensions (to slice and dice your metrics).

2. Then you build your metrics on top of these semantic models. This is all done in `.yml` configurations alongside your dbt models in your projects.

3. Once you've defined your metrics and semantic models, you can [configure the dbt Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md) in dbt.

Read our [dbt Semantic Layer quickstart](https://docs.getdbt.com/guides/sl-snowflake-qs.md) guide for more information.

 How does caching work in the dbt Semantic Layer?

Beginning in March 2024, the dbt Semantic Layer will offer two layers of caching:

* The result cache, which caches query results in the data platform so that subsequent runs of the same query are faster.
* A declarative cache which also lives in your data platform.

 Does the dbt Semantic Layer expect all models to be in normalized format?

No, the dbt Semantic Layer is flexible enough to work with many data modeling approaches including Snowflake, Star schemas, Data vaults, or other normalized tables.

 How are queries optimized to not scan more data than they should?

MetricFlow always tries to generate SQL in the most performant way, while ensuring the metric value is correct. It generates SQL in a way that allows us to add optimizations, like predicate pushdown, to ensure we don’t perform full table scans.

 What are the latency considerations of using the dbt Semantic Layer?

The latency of query runtimes is low, in the order of milliseconds.

 What if different teams have different definitions?

If the underlying metric aggregation is different, then these would be different metrics. However, if teams have different definitions because they're using specific filters or dimensions, it's still the same metric. They're just using it in different ways.

This can be managed by adjusting how the metric is viewed in downstream tools or setting up [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md) to handle the various permutations of it.

#### Build metrics and semantic models[​](#build-metrics-and-semantic-models "Direct link to Build metrics and semantic models")

 Can I define my own aggregations?

MetricFlow does not currently support custom aggregations on measures. You can find supported aggregation types [here](https://docs.getdbt.com/docs/build/measures.md#aggregation).

 How are joins identified in the semantic model?

[Joins](https://docs.getdbt.com/docs/build/join-logic.md) are identified through [entities](https://docs.getdbt.com/docs/build/entities.md) defined in a [semantic model](https://docs.getdbt.com/docs/build/semantic-models.md). These are the keys in your dataset. You can specify `foreign`, `unique`, `primary`, or `natural` joins.

With multiple semantic models and the entities within them, MetricFlow creates a graph using the semantic models as nodes and the join paths as edges to perform joins automatically. MetricFlow chooses the appropriate join type and avoids fan-out or chasm joins with other tables based on the entity types. You can find supported join types [here](https://docs.getdbt.com/docs/build/join-logic.md#types-of-joins).

 What is the benefit of “expr” used in semantic models and metric configurations?

Expr (short for “expression”) allows you to put any arbitrary SQL supported by your data platform in any definition of a measure, entity, or dimension.

This is useful if you want the object name in the semantic model to be different than what it’s called in the database. Or if you want to include logic in the definition of the component you're creating.

The MetricFlow spec is deliberately opinionated, and we offer “expr” as an escape hatch to allow developers to be more expressive.

 Do you support semi-additive metrics?

Yes, we approach this by specifying a [dimension](https://docs.getdbt.com/docs/build/dimensions.md) that a metric cannot be aggregated across (such as `time`). You can learn how to configure semi-additive dimensions [here](https://docs.getdbt.com/docs/build/measures.md#non-additive-dimensions).

 Can I use an entity as a dimension?

Yes, while [entities](https://docs.getdbt.com/docs/build/entities.md) must be defined under “entities,” they can be queried like dimensions in downstream tools. Additionally, if the entity isn't used to perform joins across your semantic models, you may optionally define it as a dimension.

 Can I test my semantic models and metrics?

Yes! You can validate your semantic nodes (semantic models, metrics, saved queries) in a few ways:

* [Query and validate you metrics](https://docs.getdbt.com/docs/build/metricflow-commands.md) in your development tool before submitting your code changes.
* [Validate semantic nodes in CI](https://docs.getdbt.com/docs/deploy/ci-jobs.md#semantic-validations-in-ci) to ensure code changes made to dbt models don't break these metrics.

#### Available integrations[​](#available-integrations "Direct link to Available integrations")

 What integrations are supported today?

There are a number of data applications that have integrations with the dbt Semantic Layer, including Tableau, Google Sheets, Hex, and Mode, among others.

Refer to [Available integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md) for more information.

 How can I benefit from using the dbt Semantic Layer if my visualization tool is not currently supported?

You can use [exports](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md) to materialize your metrics into a table or view in your data platform. From there, you can connect your visualization tool to your data platform.

Although this approach doesn't provide the dynamic benefits of the dbt Semantic Layer, you still benefit from centralized metrics and from using MetricFlow configurations to define, generate, and compute SQL for your metrics.

 Why should I use exports as opposed to defining a view within my data platform?

Creating an [export](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md) allows you to bring your governed metric definitions into your data platform as a table or view. This means your metric logic is managed centrally in dbt, instead of as a view in your data platform and ensures that metric values remain consistent across all interfaces.

 Can metric descriptions be viewed from third-party tools?

Yes, all of our interfaces or APIs expose metric descriptions, which you can surface in downstream tools.

#### Permissions and access[​](#permissions-and-access "Direct link to Permissions and access")

 How do fine-grained access controls work with the dbt Semantic Layer?

The dbt Semantic Layer uses service or personal tokens for authentication.

[Service tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md) are mapped to underlying data platform credentials. These credentials control physical access to the raw data. The credential configuration allows admins to create a credential and map it to service tokens, which can then be shared to relevant teams for BI connection setup. You can configure credentials and service tokens to reflect your teams and their roles.

Personal access tokens [(PATs)](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md) enable user-level authentication. When you use PATs to authenticate, your personal development credentials are used when running queries against the Semantic Layer.

Currently, the credentials you configure when setting up the dbt Semantic Layer are used for every request. Any physical access policies you have tied to your credentials will be respected.

#### Implementation[​](#implementation "Direct link to Implementation")

 How can I implement dbt Mesh with the dbt Semantic Layer

When using the dbt Semantic Layer in a [dbt Mesh](https://docs.getdbt.com/best-practices/how-we-mesh/mesh-1-intro.md) setting, we recommend the following:

* You have one standalone project that contains your semantic models and metrics.
* Then as you build your Semantic Layer, you can [cross-reference dbt models](https://docs.getdbt.com/docs/mesh/govern/project-dependencies.md) across your various projects or packages to create your semantic models using the [two-argument `ref` function](https://docs.getdbt.com/reference/dbt-jinja-functions/ref.md#ref-project-specific-models)( `ref('project_name', 'model_name')`).
* Your dbt Semantic Layer project serves as a global source of truth across the rest of your projects.

###### Usage example[​](#usage-example "Direct link to Usage example")

For example, let's say you have a public model (`fct_orders`) that lives in the `jaffle_finance` project. As you build your semantic model, use the following syntax to ref the model:

models/metrics/semantic\_model\_name.yml
```

Example 2 (unknown):
```unknown
Notice that in the `model` parameter, we're using the `ref` function with two arguments to reference the public model `fct_orders` defined in the `jaffle_finance` project.

<br />

 Which ‘staging layer’ should the dbt Semantic Layer talk to? Raw, staging, or marts?

We recommend to build your semantic layer on top of the [marts layer](https://docs.getdbt.com/best-practices/how-we-structure/4-marts.md), which represents the clean and transformed data from your dbt models.

 Should semantic layer credentials mirror those for production environments? Or should they be different?

Semantic layer credentials are different than the credentials you use to run dbt models. Specifically, we recommend a less privileged set of credentials since consumers are only reading data.

 How does the dbt Semantic Layer support a dbt Mesh architecture design?

Currently, semantic models can be created from dbt models that live across projects ([dbt Mesh](https://docs.getdbt.com/best-practices/how-we-mesh/mesh-1-intro.md)). In the future, users will also be able to use mesh concepts on semantic objects and define metrics across dbt projects.

 How do I migrate from the legacy Semantic Layer?

If you're using the legacy Semantic Layer, we highly recommend you [upgrade your dbt version](https://docs.getdbt.com/docs/dbt-versions/upgrade-dbt-version-in-cloud.md) to dbt v1.6 or higher to use the latest dbt Semantic Layer. Refer to the dedicated [migration guide](https://docs.getdbt.com/guides/sl-migration.md) for more info.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt Semantic Layer StarterEnterpriseEnterprise +

### dbt Semantic Layer [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

The dbt Semantic Layer eliminates duplicate coding by allowing data teams to define metrics on top of existing models and automatically handling data joins.

The dbt Semantic Layer, powered by [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow.md), simplifies the process of defining and using critical business metrics, like `revenue` in the modeling layer (your dbt project). By centralizing metric definitions, data teams can ensure consistent self-service access to these metrics in downstream data tools and applications.

Moving metric definitions out of the BI layer and into the modeling layer allows data teams to feel confident that different business units are working from the same metric definitions, regardless of their tool of choice. If a metric definition changes in dbt, it’s refreshed everywhere it’s invoked and creates consistency across all applications. To ensure secure access control, the Semantic Layer implements robust [access permissions](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md#set-up-dbt-semantic-layer) mechanisms.

Refer to the [Semantic Layer FAQs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-faqs.md) or [Why we need a universal semantic layer](https://www.getdbt.com/blog/universal-semantic-layer/) blog post to learn more.

[YouTube video player](https://www.youtube.com/embed/DS7Ub_CmBR0?si=m92hLmxw1VuE6KKO)

#### Get started with the dbt Semantic Layer[​](#get-started-with-the-dbt-semantic-layer "Direct link to Get started with the dbt Semantic Layer")

<!-- -->

To define and query metrics with the

<!-- -->

dbt Semantic Layer

<!-- -->

, you must be on a [dbt Starter or Enterprise-tier](https://www.getdbt.com/pricing/) account. [](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses)Suitable for both Multi-tenant and Single-tenant accounts. Note: Single-tenant accounts should contact their account representative for necessary setup and enablement.

<br />

<br />

Not yet supported in the dbt Fusion engine

Semantic Layer is currently supported in the dbt platform for environments running versions of dbt Core. Support for environments on the dbt Fusion engine is coming soon.

This page points to various resources available to help you understand, configure, deploy, and integrate the Semantic Layer. The following sections contain links to specific pages that explain each aspect in detail. Use these links to navigate directly to the information you need, whether you're setting up the Semantic Layer for the first time, deploying metrics, or integrating with downstream tools.

Refer to the following resources to get started with the Semantic Layer:

* [Quickstart with the Semantic Layer](https://docs.getdbt.com/guides/sl-snowflake-qs.md) — Build and define metrics, set up the Semantic Layer, and query them using our first-class integrations.
* [Build your metrics](https://docs.getdbt.com/docs/build/build-metrics-intro.md) — Use MetricFlow in dbt to centrally define your metrics.
* [Semantic Layer FAQs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-faqs.md) — Discover answers to frequently asked questions about the Semantic Layer, such as availability, integrations, and more.

#### Configure the dbt Semantic Layer[​](#configure-the-dbt-semantic-layer "Direct link to Configure the dbt Semantic Layer")

The following resources provide information on how to configure the Semantic Layer:

* [Administer the Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md) — Seamlessly set up the credentials and tokens to start querying the Semantic Layer.
* [Architecture](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-architecture.md) — Explore the powerful components that make up the Semantic Layer.

#### Deploy metrics[​](#deploy-metrics "Direct link to Deploy metrics")

This section provides information on how to deploy the Semantic Layer and materialize your metrics:

* [Deploy your Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/deploy-sl.md) — Run a dbt job to deploy the Semantic Layer and materialize your metrics.
* [Write queries with exports](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md) — Use exports to write commonly used queries directly within your data platform, on a schedule.
* [Cache common queries](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-cache.md) — Leverage result caching and declarative caching for common queries to speed up performance and reduce query computation.

#### Consume metrics and integrate[​](#consume-metrics-and-integrate "Direct link to Consume metrics and integrate")

Consume metrics and integrate the Semantic Layer with downstream tools and applications:

* [Consume metrics](https://docs.getdbt.com/docs/use-dbt-semantic-layer/consume-metrics.md) — Query and consume metrics in downstream tools and applications using the Semantic Layer.
* [Available integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md) — Review a wide range of partners you can integrate and query with the Semantic Layer.
* [Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) — Use the Semantic Layer APIs to query metrics in downstream tools for consistent, reliable data metrics.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt support

Support for dbt is available to all users through the following channels:

* Dedicated dbt Support team (dbt users).
* [The Community Forum](https://discourse.getdbt.com/).
* [dbt Community slack](https://www.getdbt.com/community/join-the-community/).

#### dbt Core support[​](#dbt-core-support "Direct link to dbt Core support")

If you're developing on the command line (CLI) and have questions or need some help — reach out to the helpful dbt community through [the Community Forum](https://discourse.getdbt.com/) or [dbt Community slack](https://www.getdbt.com/community/join-the-community/).

#### dbt platform support[​](#dbt-platform-support "Direct link to dbt platform support")

The global dbt Support team is available to dbt customers by [email](mailto:support@getdbt.com) or by clicking **Create a support ticket** through the dbt navigation.

##### Create a support ticket[​](#create-a-support-ticket "Direct link to Create a support ticket")

To create a support ticket in dbt:

1. In the dbt navigation, click on **Help & Guides**.
2. Click **Create a support ticket**.
3. Fill out the form and click **Create Ticket**.
4. A dbt Support team member will respond to your ticket through email.

[![Create a support ticket in dbt](/img/create-support-ticket.gif?v=2 "Create a support ticket in dbt")](#)Create a support ticket in dbt

##### Ask dbt Support Assistant[​](#ask-dbt-support-assistant "Direct link to Ask dbt Support Assistant")

dbt Support Assistant is an AI widget that provides instant, AI-generated responses to common questions. This feature is available to dbt users and can help answer troubleshooting questions, give a synopsis of features and functionality, or link to relevant documentation.

The dbt Support Assistant AI widget is separate from [Copilot](https://docs.getdbt.com/docs/cloud/dbt-copilot.md), a powerful AI engine that helps with code generation to accelerate your analytics workflows. The dbt Support Assistant focuses on answering documentation and troubleshooting-related questions. Enabling or disabling AI features in dbt won't affect the dbt Support Assistant's availability.

info

We recommend validating information received in AI responses for any scenario using our documentation. Please [contact support](mailto:support@getdbt.com) to report incorrect information provided by the Support Assistant.

##### Support plans and resources[​](#support-plans-and-resources "Direct link to Support plans and resources")

We want to help you work through implementing and utilizing dbt platform at your organization. Have a question you can't find an answer to in [our docs](https://docs.getdbt.com/) or [the Community Forum](https://discourse.getdbt.com/)? Our Support team is here to `dbt help` you!

* **Enterprise and Enterprise+ plans** — Priority [support](#severity-level-for-enterprise-support), optional premium plans, enhanced SLAs, implementation assistance, dedicated management, and dbt Labs security reviews depending on price point.
* **Developer and Starter plans** — 24x5 support (no service level agreement (SLA); [contact Sales](https://www.getdbt.com/pricing/) for Enterprise plan inquiries).
* **Support team help** — Assistance with [common dbt questions](https://docs.getdbt.com/category/troubleshooting.md), like project setup, login issues, error understanding, setup private packages, link to a new GitHub account, [how to generate a har file](https://docs.getdbt.com/faqs/Troubleshooting/generate-har-file.md), and so on.
* **Resource guide** — Check the [guide](https://docs.getdbt.com/community/resources/getting-help.md) for effective help-seeking strategies.

Example of common support questions

Types of dbt cloud-based platform related questions our Support team can assist you with, regardless of your dbt plan:<br /><br />**How do I...**<br />

* set up a dbt project? <br />
* set up a private package in dbt? <br />
* configure custom branches on git repos? <br />
* link dbt to a new GitHub account? <br /> <br />
  **Help! I can't...** <br />
* log in. <br />
* access logs. <br />
* update user groups. <br /> <br />
  **I need help understanding...** <br />
* why this run failed. <br />
* why I am getting this error message in dbt? <br />
* why my CI jobs are not kicking off as expected. <br />

#### dbt Enterprise accounts[​](#dbt-enterprise-accounts "Direct link to dbt Enterprise accounts")

Basic assistance with dbt project troubleshooting. Help with errors and issues in macros, models, and dbt Labs' packages. For strategic advice, best practices, or expansion conversations, consult your Account team.

For customers on a dbt Enterprise-tier plan, we **also** offer basic assistance in troubleshooting issues with your dbt project:

* **Something isn't working the way I would expect it to...**

  * in a macro I created...
  * in an incremental model I'm building...
  * in one of dbt Labs' packages like dbt\_utils or audit\_helper...

* **I need help understanding and troubleshooting this error...**

  * `Server error: Compilation Error in rpc request (from remote system) 'dbt_utils' is undefined`
  * `SQL compilation error: syntax error line 1 at position 38 unexpected '<EOF>'.`
  * `Compilation Error Error reading name_of_folder/name_of_file.yml - Runtime Error Syntax error near line 9`

Types of questions you should ask your Account team:

* How should we think about setting up our dbt projects, environments, and jobs based on our company structure and needs?
* I want to expand my account! How do I add more people and train them?
* Here is our data road map for the next year - can we talk through how dbt fits into it and what features we may not be utilizing that can help us achieve our goals?
* It is time for our contract renewal, what options do I have?

##### Severity level for Enterprise support[​](#severity-level-for-enterprise-support "Direct link to Severity level for Enterprise support")

Support tickets are assigned a severity level based on the impact of the issue on your business. The severity level is assigned by dbt Labs, and the level assigned determines the priority level of support you will receive. For specific ticket response time or other questions that relate to your Enterprise or Enterprise+ account’s SLA, please refer to your Enterprise contract.

| Severity Level   | Description                                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Severity Level 1 | Any Error which makes the use or continued use of the Subscription or material features impossible; Subscription is not operational, with no alternative available. |
| Severity Level 2 | Feature failure, without a workaround, but Subscription is operational.                                                                                             |
| Severity Level 3 | Feature failure, but a workaround exists.                                                                                                                           |
| Severity Level 4 | Error with low-to-no impact on Client’s access to or use of the Subscription, or Client has a general question or feature enhancement request.                      |

#### Leave feedback[​](#leave-feedback "Direct link to Leave feedback")

Leave feedback or submit a feature request for dbt or dbt Core.

###### Share feedback or feature request for the dbt platform[​](#share-feedback-or-feature-request-for-the-dbt-platform "Direct link to Share feedback or feature request for the dbt platform")

1. In the dbt navigation, click **Leave feedback**.
2. In the **Leave feedback** pop up, fill out the form.
3. Upload any relevant files to the feedback form (optional).
4. Confirm if you'd like dbt Labs to contact you about the feedback (optional).
5. Click **Send Feedback**.

[![Leave feedback in dbt](/img/docs/leave-feedback.gif?v=2 "Leave feedback in dbt")](#)Leave feedback in dbt

###### Share feedback or feature request for dbt Core[​](#share-feedback-or-feature-request-for-dbt-core "Direct link to Share feedback or feature request for dbt Core")

* [Create a GitHub issue here](https://github.com/dbt-labs/dbt-core/issues).

#### External help[​](#external-help "Direct link to External help")

For SQL writing, project performance review, or project building, refer to dbt Preferred Consulting Providers and dbt Labs' Services. For help writing SQL, reviewing the overall performance of your project, or want someone to actually help build your dbt project, refer to the following pages:

* List of [dbt Consulting Partners](https://www.getdbt.com/partner-directory).
* dbt Labs' [Services](https://www.getdbt.com/dbt-labs/services/).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt tips and tricks

Use this page for valuable insights and practical advice to enhance your dbt experience. Whether you're new to dbt or an experienced user, these tips are designed to help you work more efficiently and effectively.

The following tips are organized into the following categories:

* [Package tips](#package-tips) to help you streamline your workflow.
* [Advanced tips and techniques](#advanced-tips-and-techniques) to help you get the most out of dbt.

If you're developing with the Studio IDE, you can refer to the [keyboard shortcuts](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/keyboard-shortcuts.md) page to help make development more productive and easier for everyone.

#### YAML tips[​](#yaml-tips "Direct link to YAML tips")

This section clarifies where you can use [Jinja](https://docs.getdbt.com/docs/build/jinja-macros.md), nest [vars](https://docs.getdbt.com/reference/dbt-jinja-functions/var.md) and [`env_var`](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var.md) in your YAML files.

* You can use Jinja in almost every YAML file in dbt *except* the [`dependencies.yml` file](https://docs.getdbt.com/docs/build/packages.md#use-cases). This is because the `dependencies.yml` file doesn't support Jinja.
* Use `vars` in any YAML file that supports Jinja (like `schema.yml`, `snapshots.yml`). However, note that:
  <!-- -->
  * In `dbt_project.yml`, `packages.yml`, and `profiles.yml` files, you must pass `vars` through the CLI using `--vars`, not defined inside the `vars:` block in the YAML file. This is because these files are parsed before Jinja is rendered.
* You can use `env_var()` in all YAML files that support Jinja. Only `profiles.yml` and `packages.yml` support environment variables for secure values (using the `DBT_ENV_SECRET_` prefix). These are masked in logs and intended for credentials or secrets.

For additional information, check out [dbt Core's context docs](https://github.com/dbt-labs/dbt-core/blob/main/core/dbt/context/README.md).

#### Package tips[​](#package-tips "Direct link to Package tips")

Leverage these dbt packages to streamline your workflow:

| Package                                                                                 | Description                                                                                                                                                   |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`dbt_codegen`](https://hub.getdbt.com/dbt-labs/codegen/latest/)                        | Use the package to help you generate YML files for your models and sources and SQL files for your staging models.                                             |
| [`dbt_utils`](https://hub.getdbt.com/dbt-labs/dbt_utils/latest/)                        | The package contains macros useful for daily development. For example, `date_spine` generates a table with all dates between the ones provided as parameters. |
| [`dbt_project_evaluator`](https://hub.getdbt.com/dbt-labs/dbt_project_evaluator/latest) | The package compares your dbt project against a list of our best practices and provides suggestions and guidelines on how to update your models.              |
| [`dbt_expectations`](https://hub.getdbt.com/metaplane/dbt_expectations/latest/)         | The package contains many tests beyond those built into dbt.                                                                                                  |
| [`dbt_audit_helper`](https://hub.getdbt.com/#:~:text=adwords-,audit_helper,-codegen)    | The package lets you compare the output of 2 queries. Use it when refactoring existing logic to ensure that the new results are identical.                    |
| [`dbt_artifacts`](https://hub.getdbt.com/brooklyn-data/dbt_artifacts/latest)            | The package saves information about your dbt runs directly to your data platform so that you can track the performance of models over time.                   |
| [`dbt_meta_testing`](https://hub.getdbt.com/tnightengale/dbt_meta_testing/latest)       | This package checks that your dbt project is sufficiently tested and documented.                                                                              |

#### Advanced tips and techniques[​](#advanced-tips-and-techniques "Direct link to Advanced tips and techniques")

* Use your folder structure as your primary selector method. `dbt build --select marts.marketing` is simpler and more resilient than relying on tagging every model.
* Think about jobs in terms of build cadences and SLAs. Run models that have hourly, daily, or weekly build cadences together.
* Use the [where config](https://docs.getdbt.com/reference/resource-configs/where.md) for tests to test an assertion on a subset of records.
* [store\_failures](https://docs.getdbt.com/reference/resource-configs/store_failures.md) lets you examine records that cause tests to fail, so you can either repair the data or change the test as needed.
* Use [severity](https://docs.getdbt.com/reference/resource-configs/severity.md) thresholds to set an acceptable number of failures for a test.
* Use [incremental\_strategy](https://docs.getdbt.com/docs/build/incremental-strategy.md) in your incremental model config to implement the most effective behavior depending on the volume of your data and reliability of your unique keys.
* Set `vars` in your `dbt_project.yml` to define global defaults for certain conditions, which you can then override using the `--vars` flag in your commands.
* Use [for loops](https://docs.getdbt.com/guides/using-jinja.md?step=3) in Jinja to DRY up repetitive logic, such as selecting a series of columns that all require the same transformations and naming patterns to be applied.
* Instead of relying on post-hooks, use the [grants config](https://docs.getdbt.com/reference/resource-configs/grants.md) to apply permission grants in the warehouse resiliently.
* Define [source-freshness](https://docs.getdbt.com/docs/build/sources.md#source-data-freshness) thresholds on your sources to avoid running transformations on data that has already been processed.
* Use the `+` operator on the left of a model `dbt build --select +model_name` to run a model and all of its upstream dependencies. Use the `+` operator on the right of the model `dbt build --select model_name+` to run a model and everything downstream that depends on it.
* Use `dir_name` to run all models in a package or directory.
* Use the `@` operator on the left of a model in a non-state-aware CI setup to test it. This operator runs all of a selection’s parents and children, and also runs the parents of its children, which in a fresh CI schema will likely not exist yet.
* Use the [--exclude flag](https://docs.getdbt.com/reference/node-selection/exclude.md) to remove a subset of models out of a selection.
* Use the [--full-refresh](https://docs.getdbt.com/reference/commands/run.md#refresh-incremental-models) flag to rebuild an incremental model from scratch.
* Use [seeds](https://docs.getdbt.com/docs/build/seeds.md) to create manual lookup tables, like zip codes to states or marketing UTMs to campaigns. `dbt seed` will build these from CSVs into your warehouse and make them `ref` able in your models.
* Use [target.name](https://docs.getdbt.com/docs/build/custom-schemas.md#an-alternative-pattern-for-generating-schema-names) to pivot logic based on what environment you’re using. For example, to build into a single development schema while developing, but use multiple schemas in production.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Quickstart guide](https://docs.getdbt.com/guides.md)
* [About dbt](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features.md)
* [Develop in the Cloud](https://docs.getdbt.com/docs/cloud/about-develop-dbt.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### dbt VS Code extension features Preview

### dbt VS Code extension features [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")

The dbt VS Code extension is backed by the speed and power of the dbt Fusion engine and a dynamic Language Server Protocol (LSP) that enables enhanced workflows, faster development, and easy navigation.

The following extension features help you get more done, fast:

* **[Live error detection](#live-error-detection):** Automatically validate your SQL code to detect errors and surface warnings, without hitting the warehouse. This includes both dbt errors (like invalid `ref`) and SQL errors (like invalid column name or SQL syntax).
* **[Lightning-fast parse times](#lightning-fast-parse-times):** Parse even the largest projects up to 30x faster than dbt Core.
* **[Powerful IntelliSense](#powerful-intellisense):** Autocomplete SQL functions, model names, macros, and more.
* **[Instant refactoring](#instant-refactoring):** Rename models or columns and see references update project-wide.
* **[Go-to-definition](#go-to-definition-and-reference):** Jump to the definition of any `ref`, macro, model, or column with a single click. Particularly useful in large projects with many models and macros. Excludes definitions from installed packages.
* **[Hover insights](#hover-insights):** See context on tables, columns, and functions without leaving your code. Simply hover over any SQL element to see details like column names and data types.
* **[Live CTE previews](#live-preview-for-models-and-ctes):** Preview a CTE’s output directly from inside your dbt model for faster validation and debugging.
* **[Rich lineage in context](#rich-lineage-in-context):** See lineage at the column or table level as you develop with no context switching or breaking the flow.
* **[View compiled code](#view-compiled-code):** Get a live view of the SQL code your models will build alongside your dbt code.
* **[Build flexibly](#build-flexibly):** Use the command palette to build models with complex selectors.

##### Live error detection[​](#live-error-detection "Direct link to Live error detection")

Automatically validate your SQL code to detect errors and surface warnings without hitting the warehouse.

* Displays diagnostics (red squiggles) for:

  <!-- -->

  * Syntax errors (missing commas, misspelled keywords, etc).
  * Invalid / missing column names (for example, `select not_a_column from {{ ref('real_model') }}`).
  * Missing `group by` clauses, or columns that are neither grouped nor aggregated.
  * Invalid function names or arguments

* Hover over red squiggles to display errors.

* Full diagnostic information is available in the “Problems”.

[](/img/docs/extension/live-error-detection.mp4)

##### Lightning-fast parse times[​](#lightning-fast-parse-times "Direct link to Lightning-fast parse times")

Parse even the largest projects up to 30x faster than with dbt Core.

[](/img/docs/extension/zoomzoom.mp4)

##### Powerful IntelliSense[​](#powerful-intellisense "Direct link to Powerful IntelliSense")

Autocomplete SQL functions, model names, macros and more.

Usage:

* Autocomplete `ref`s and `source` calls. For example, type `{{ ref(` or `{{ source(` and you will see a list of available resources and their type complete the function call.
* Autocomplete dialect-specific function names.

[![Example of the VS Code extension IntelliSense](/img/docs/extension/vsce-intellisense.gif?v=2 "Example of the VS Code extension IntelliSense")](#)Example of the VS Code extension IntelliSense

##### Instant refactoring[​](#instant-refactoring "Direct link to Instant refactoring")

Renaming models:

* Right-click on a file in the file tree and select **Rename**.
* After renaming the file, you'll get a prompt asking if you want to make refactoring changes.
* Select **OK** to apply the changes, or **Show Preview** to display a preview of refactorings.
* After applying your changes, `ref`s should be updated to use the updated model name.

Renaming columns:

* Right-click on a column alias and select **Rename Symbol**.
* After renaming the column, you'll get a prompt asking if you want to make refactoring changes.
  <!-- -->
  * Select **OK** to apply the changes, or **Show Preview** to show a preview of refactorings.
* After applying your changes, downstream references to the column should be updated to use the new column name.

Note: Renaming models and columns is not yet supported for snapshots, or any resources defined in a .yml file.

[](/img/docs/extension/refactor.mp4)

##### Go-to-definition and reference[​](#go-to-definition-and-reference "Direct link to Go-to-definition and reference")

Jump to the definition of any `ref`, macro, model, or column with a single click. Particularly useful in large projects with many models and macros. Excludes definitions from installed packages.

Usage:

* Command or Ctrl-click to go to the definition for an identifier.
* You can also right-click an identifier or and select **Go to Definition** or **Go to References**.
* Supports CTE names, column names, `*`, macro names, and dbt `ref()` and `source()` call.

[](/img/docs/extension/go-to-definition.mp4)

##### Hover insights[​](#hover-insights "Direct link to Hover insights")

See context on tables, columns, and functions without leaving your code. Simply hover over any SQL element to see details like column names and data types.

Usage:

* Hover over `*` to see expanded list of columns and their types.
* Hover over column name or alias to see its type.

[](/img/docs/extension/hover-insights.mp4)

##### Live preview for models and CTEs[​](#live-preview-for-models-and-ctes "Direct link to Live preview for models and CTEs")

Preview a CTE’s output, or an entire model, directly from inside your editor for faster validation and debugging.

Usage:

* Click the **table icon** or use keyboard shortcut `cmd+enter` (macOS) / `ctrl+enter` (Windows/Linux) to preview query results.
* Click the **Preview CTE** codelens to preview CTE results.
* Results will be displayed in the **Query Results** tab in the bottom panel.
* The preview table is sortable and results are stored until the tab is closed.
* You can also select a range of SQL to preview the results of a specific SQL snippet.

[](/img/docs/extension/preview-cte.mp4)

##### Rich lineage in context[​](#rich-lineage-in-context "Direct link to Rich lineage in context")

See lineage at the column or table level as you develop — no context switching or breaking flow.

View table lineage:

* Open the **Lineage** tab in your editor. It will reflect table lineage focused on the currently-open file.
* Double-click nodes to open the files in your editor.
* The lineage pane updates as you navigate the files in your dbt project.
* Right-click on a node to update the DAG, or view column lineage for a node.

View column lineage:

* Right-click on a filename, or in the SQL contents of a model file.
* Select **dbt: View Lineage** --> **Show column lineage**.
* Select the column to view lineage for.
* Double-click on a node to update the DAG selector.
* You can also use column selectors in the lineage window by adding the `column:` prefix and appending the column name.
  <!-- -->
  * For example, if you want the lineage for the `AMOUNT` column of your `stg_payments` model, edit the `+model.jaffle_shop.stg_payments+` to `+column:model.jaffle_shop.stg_payments.AMOUNT+`.

[](/img/docs/extension/lineage.mp4)

##### View compiled code[​](#view-compiled-code "Direct link to View compiled code")

Get a live view of the SQL code your models will build — right alongside your dbt code.

Usage:

* Click the **code icon** to view compiled code side-by-side with source code.
* Compiled code will update as you save your source code.
* Clicking on a dbt macro will focus the corresponding compiled code.
* Clicking on a compiled code block will focus the corresponding source code.

[](/img/docs/extension/compiled-code.mp4)

##### Build flexibly[​](#build-flexibly "Direct link to Build flexibly")

Use the command palette to quickly build models using complex selectors.

Usage:

* Click the **dbt icon** or use keyboard shortcut `cmd+shift+enter` (macOS) / `ctrl+shift+enter` (Windows/Linux) to launch a quickpick menu.
* Select a command to run.

[](/img/docs/extension/build-flexibly.mp4)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Deploy dbt

Use dbt's capabilities to seamlessly run a dbt job in production or staging environments. Rather than run dbt commands manually from the command line, you can leverage the [dbt's in-app scheduling](https://docs.getdbt.com/docs/deploy/job-scheduler.md) to automate how and when you execute dbt.

The dbt platform offers the easiest and most reliable way to run your dbt project in production. Effortlessly promote high quality code from development to production and build fresh data assets that your business intelligence tools and end users query to make business decisions. Deploying with dbt lets you:

* Keep production data fresh on a timely basis
* Ensure CI and production pipelines are efficient
* Identify the root cause of failures in deployment environments
* Maintain high-quality code and data in production
* Gain visibility into the [health](https://docs.getdbt.com/docs/explore/data-tile.md) of deployment jobs, models, and tests
* Uses [exports](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md) to write [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md) in your data platform for reliable and fast metric reporting
* [Visualize](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures-tableau.md) and [orchestrate](https://docs.getdbt.com/docs/cloud-integrations/orchestrate-exposures.md) downstream exposures to understand how models are used in downstream tools and proactively refresh the underlying data sources during scheduled dbt jobs. [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
* Use [dbt's Git repository caching](https://docs.getdbt.com/docs/cloud/account-settings.md#git-repository-caching) to protect against third-party outages and improve job run reliability. [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
* Use [Hybrid projects](https://docs.getdbt.com/docs/deploy/hybrid-projects.md) to upload dbt artifacts into the dbt platform for central visibility, cross-project referencing, and easier collaboration. [Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing") Preview

Before continuing, make sure you understand dbt's approach to [deployment environments](https://docs.getdbt.com/docs/deploy/deploy-environments.md).

Learn how to use dbt's features to help your team ship timely and quality production data more easily.

#### Deploy with dbt[​](#deploy-with-dbt "Direct link to Deploy with dbt")

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/job-scheduler.md)

###### [Job scheduler](https://docs.getdbt.com/docs/deploy/job-scheduler.md)

[The job scheduler is the backbone of running jobs in the dbt platform, bringing power and simplicity to building data pipelines in both continuous integration and production environments.](https://docs.getdbt.com/docs/deploy/job-scheduler.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/deploy-jobs.md)

###### [Deploy jobs](https://docs.getdbt.com/docs/deploy/deploy-jobs.md)

[Create and schedule jobs for the job scheduler to run.](https://docs.getdbt.com/docs/deploy/deploy-jobs.md)

<br />

<br />

[Runs on a schedule, by API, or after another job completes.](https://docs.getdbt.com/docs/deploy/deploy-jobs.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/state-aware-about.md)

###### [State-aware orchestration](https://docs.getdbt.com/docs/deploy/state-aware-about.md)

[Intelligently determines which models to build by detecting changes in code or data at each job run.](https://docs.getdbt.com/docs/deploy/state-aware-about.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/continuous-integration.md)

###### [Continuous integration](https://docs.getdbt.com/docs/deploy/continuous-integration.md)

[Set up CI checks so you can build and test any modified code in a staging environment when you open PRs and push new commits to your dbt repository.](https://docs.getdbt.com/docs/deploy/continuous-integration.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/continuous-deployment.md)

###### [Continuous deployment](https://docs.getdbt.com/docs/deploy/continuous-deployment.md)

[Set up merge jobs to ensure the latest code changes are always in production when pull requests are merged to your Git repository.](https://docs.getdbt.com/docs/deploy/continuous-deployment.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/job-commands.md)

###### [Job commands](https://docs.getdbt.com/docs/deploy/job-commands.md)

[Configure which dbt commands to execute when running a dbt job.](https://docs.getdbt.com/docs/deploy/job-commands.md)

<br />

#### Monitor jobs and alerts[​](#monitor-jobs-and-alerts "Direct link to Monitor jobs and alerts")

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/orchestrate-exposures.md)

###### [Visualize and orchestrate exposures](https://docs.getdbt.com/docs/deploy/orchestrate-exposures.md)

[Learn how to use dbt to automatically generate downstream exposures from dashboards and proactively refresh the underlying data sources during scheduled dbt jobs.](https://docs.getdbt.com/docs/deploy/orchestrate-exposures.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/artifacts.md)

###### [Artifacts](https://docs.getdbt.com/docs/deploy/artifacts.md)

[dbt generates and saves artifacts for your project, which it uses to power features like creating docs for your project and reporting the freshness of your sources.](https://docs.getdbt.com/docs/deploy/artifacts.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/job-notifications.md)

###### [Job notifications](https://docs.getdbt.com/docs/deploy/job-notifications.md)

[Receive email or Slack channel notifications when a job run succeeds, fails, or is canceled so you can respond quickly and begin remediation if necessary.](https://docs.getdbt.com/docs/deploy/job-notifications.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/model-notifications.md)

###### [Model notifications](https://docs.getdbt.com/docs/deploy/model-notifications.md)

[Receive email notifications in real time about issues encountered by your models and tests while a job is running.](https://docs.getdbt.com/docs/deploy/model-notifications.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/run-visibility.md)

###### [Run visibility](https://docs.getdbt.com/docs/deploy/run-visibility.md)

[View the history of your runs and the model timing dashboard to help identify where improvements can be made to the scheduled jobs.](https://docs.getdbt.com/docs/deploy/run-visibility.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/retry-jobs.md)

###### [Retry jobs](https://docs.getdbt.com/docs/deploy/retry-jobs.md)

[Rerun your errored jobs from start or the failure point.](https://docs.getdbt.com/docs/deploy/retry-jobs.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/source-freshness.md)

###### [Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness.md)

[Enable snapshots to capture the freshness of your data sources and configure how frequent these snapshots should be taken. This can help you determine whether your source data freshness is meeting your SLAs.](https://docs.getdbt.com/docs/deploy/source-freshness.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/webhooks.md)

###### [Webhooks](https://docs.getdbt.com/docs/deploy/webhooks.md)

[Create outbound webhooks to send events about your dbt jobs' statuses to other systems in your organization.](https://docs.getdbt.com/docs/deploy/webhooks.md)

<br />

#### Hybrid projects [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing") Preview[​](#hybrid-projects-- "Direct link to hybrid-projects--")

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/hybrid-projects.md)

###### [Hybrid projects](https://docs.getdbt.com/docs/deploy/hybrid-projects.md)

[Use Hybrid projects to upload dbt Core artifacts into the dbt platform for central visibility, cross-project referencing, and easier collaboration.](https://docs.getdbt.com/docs/deploy/hybrid-projects.md)

<br />

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Use exports to materialize saved queries](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md)
* [Integrate with other orchestration tools](https://docs.getdbt.com/docs/deploy/deployment-tools.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Deploy jobs

You can use deploy jobs to build production data assets. Deploy jobs make it easy to run dbt commands against a project in your cloud data platform, triggered either by schedule or events. Each job run in dbt will have an entry in the job's run history and a detailed run overview, which provides you with:

* Job trigger type
* Commit SHA
* Environment name
* Sources and documentation info, if applicable
* Job run details, including run timing, [model timing data](https://docs.getdbt.com/docs/deploy/run-visibility.md#model-timing), and [artifacts](https://docs.getdbt.com/docs/deploy/artifacts.md)
* Detailed run steps with logs and their run step statuses

You can create a deploy job and configure it to run on [scheduled days and times](#schedule-days), enter a [custom cron schedule](#cron-schedule), or [trigger the job after another job completes](#trigger-on-job-completion).

#### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* You must have a [dbt account](https://www.getdbt.com/signup/) and [Developer seat license](https://docs.getdbt.com/docs/cloud/manage-access/seats-and-users.md).
  <!-- -->
  * For the [Trigger on job completion](#trigger-on-job-completion) feature, your dbt account must be on the [Starter or an Enterprise-tier](https://www.getdbt.com/pricing/) plan.
* You must have a dbt project connected to a [data platform](https://docs.getdbt.com/docs/cloud/connect-data-platform/about-connections.md).
* You must have [access permission](https://docs.getdbt.com/docs/cloud/manage-access/about-user-access.md) to view, create, modify, or run jobs.
* You must set up a [deployment environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md).

#### Create and schedule jobs[​](#create-and-schedule-jobs "Direct link to Create and schedule jobs")

1. On your deployment environment page, click **Create job** > **Deploy job** to create a new deploy job.

2. Options in the **Job settings** section:

   <!-- -->

   * **Job name** — Specify the name for the deploy job. For example, `Daily build`.
   * (Optional) **Description** — Provide a description of what the job does (for example, what the job consumes and what the job produces).
   * **Environment** — By default, it’s set to the deployment environment you created the deploy job from.

3. Options in the **Execution settings** section:

   <!-- -->

   * [**Commands**](https://docs.getdbt.com/docs/deploy/job-commands.md#built-in-commands) — By default, it includes the `dbt build` command. Click **Add command** to add more [commands](https://docs.getdbt.com/docs/deploy/job-commands.md) that you want to be invoked when the job runs. During a job run, [built-in commands](https://docs.getdbt.com/docs/deploy/job-commands.md#built-in-commands) are "chained" together and if one run step fails, the entire job fails with an "Error" status.
   * [**Generate docs on run**](https://docs.getdbt.com/docs/deploy/job-commands.md#checkbox-commands) — Enable this option if you want to [generate project docs](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md) when this deploy job runs. If the step fails, the job can succeed if subsequent steps pass.
   * [**Run source freshness**](https://docs.getdbt.com/docs/deploy/job-commands.md#checkbox-commands) — Enable this option to invoke the `dbt source freshness` command before running the deploy job. If the step fails, the job can succeed if subsequent steps pass. Refer to [Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness.md) for more details.

4. Options in the **Triggers** section:

   <!-- -->

   * **Run on schedule** — Run the deploy job on a set schedule.

     <!-- -->

     * **Timing** — Specify whether to [schedule](#schedule-days) the deploy job using **Intervals** that run the job every specified number of hours, **Specific hours** that run the job at specific times of day, or **Cron schedule** that run the job specified using [cron syntax](#cron-schedule).
     * **Days of the week** — By default, it’s set to every day when **Intervals** or **Specific hours** is chosen for **Timing**.

   * **Run when another job finishes** — Run the deploy job when another *upstream* deploy [job completes](#trigger-on-job-completion).

     <!-- -->

     * **Project** — Specify the parent project that has that upstream deploy job.
     * **Job** — Specify the upstream deploy job.
     * **Completes on** — Select the job run status(es) that will [enqueue](https://docs.getdbt.com/docs/deploy/job-scheduler.md#scheduler-queue) the deploy job.

[![Example of Triggers on the Deploy Job page](/img/docs/dbt-cloud/using-dbt-cloud/example-triggers-section.png?v=2 "Example of Triggers on the Deploy Job page")](#)Example of Triggers on the Deploy Job page

5. (Optional) Options in the **Advanced settings** section:

   * **Environment variables** — Define [environment variables](https://docs.getdbt.com/docs/build/environment-variables.md) to customize the behavior of your project when the deploy job runs.
   * **Target name** — Define the [target name](https://docs.getdbt.com/docs/build/custom-target-names.md) to customize the behavior of your project when the deploy job runs. Environment variables and target names are often used interchangeably.
   * **Run timeout** — Cancel the deploy job if the run time exceeds the timeout value.
   * **Compare changes against** — By default, it’s set to **No deferral**. Select either **Environment** or **This Job** to let dbt know what it should compare the changes against.

   info

   Older versions of dbt only allow you to defer to a specific job instead of an environment. Deferral to a job compares state against the project code that was run in the deferred job's last successful run. While deferral to an environment is more efficient as dbt will compare against the project representation (which is stored in the `manifest.json`) of the last successful deploy job run that executed in the deferred environment. By considering *all* deploy jobs that run in the deferred environment, dbt will get a more accurate, latest project representation state.

   * **dbt version** — By default, it’s set to inherit the [dbt version](https://docs.getdbt.com/docs/dbt-versions/core.md) from the environment. dbt Labs strongly recommends that you don't change the default setting. This option to change the version at the job level is useful only when you upgrade a project to the next dbt version; otherwise, mismatched versions between the environment and job can lead to confusing behavior.
   * **Threads** — By default, it’s set to 4 [threads](https://docs.getdbt.com/docs/core/connect-data-platform/connection-profiles.md#understanding-threads). Increase the thread count to increase model execution concurrency.

   [![Example of Advanced Settings on the Deploy Job page](/img/docs/dbt-cloud/using-dbt-cloud/deploy-job-adv-settings.png?v=2 "Example of Advanced Settings on the Deploy Job page")](#)Example of Advanced Settings on the Deploy Job page

##### Schedule days[​](#schedule-days "Direct link to Schedule days")

To set your job's schedule, use the **Run on schedule** option to choose specific days of the week, and select customized hours or intervals.

Under **Timing**, you can either use regular intervals for jobs that need to run frequently throughout the day or customizable hours for jobs that need to run at specific times:

* **Intervals** — Use this option to set how often your job runs, in hours. For example, if you choose **Every 2 hours**, the job will run every 2 hours from midnight UTC. This doesn't mean that it will run at exactly midnight UTC. However, subsequent runs will always be run with the same amount of time between them. For example, if the previous scheduled pipeline ran at 00:04 UTC, the next run will be at 02:04 UTC. This option is useful if you need to run jobs multiple times per day at regular intervals.

* **Specific hours** — Use this option to set specific times when your job should run. You can enter a comma-separated list of hours (in UTC) when you want the job to run. For example, if you set it to `0,12,23,` the job will run at midnight, noon, and 11 PM UTC. Job runs will always be consistent between both hours and days, so if your job runs at 00:05, 12:05, and 23:05 UTC, it will run at these same hours each day. This option is useful if you want your jobs to run at specific times of day and don't need them to run more frequently than once a day.

info

dbt uses [Coordinated Universal Time](https://en.wikipedia.org/wiki/Coordinated_Universal_Time) (UTC) and does not account for translations to your specific timezone or take into consideration daylight savings time. For example:

* 0 means 12am (midnight) UTC
* 12 means 12pm (afternoon) UTC
* 23 means 11pm UTC

##### Cron schedule[​](#cron-schedule "Direct link to Cron schedule")

To fully customize the scheduling of your job, choose the **Cron schedule** option and use cron syntax. With this syntax, you can specify the minute, hour, day of the month, month, and day of the week, allowing you to set up complex schedules like running a job on the first Monday of each month.

**Cron frequency**

To enhance performance, job scheduling frequencies vary by dbt plan:

* Developer plans: dbt sets a minimum interval of every 10 minutes for scheduling jobs. This means scheduling jobs to run more frequently, or at less than 10 minute intervals, is not supported.
* Starter, Enterprise, and Enterprise+ plans: No restrictions on job execution frequency.

**Examples**

Use tools such as [crontab.guru](https://crontab.guru/) to generate the correct cron syntax. This tool allows you to input cron snippets and return their plain English translations. The dbt job scheduler supports using `L` to schedule jobs on the last day of the month.

Examples of cron job schedules:

* `0 * * * *`: Every hour, at minute 0.
* `*/5 * * * *`: Every 5 minutes. (Not available on Developer plans)
* `5 4 * * *`: At exactly 4:05 AM UTC.
* `30 */4 * * *`: At minute 30 past every 4th hour (such as 4:30 AM, 8:30 AM, 12:30 PM, and so on, all UTC).
* `0 0 */2 * *`: At 12:00 AM (midnight) UTC every other day.
* `0 0 * * 1`: At midnight UTC every Monday.
* `0 0 L * *`: At 12:00 AM (midnight), on the last day of the month.
* `0 0 L 1,2,3,4,5,6,8,9,10,11,12 *`: At 12:00 AM, on the last day of the month, only in January, February, March, April, May, June, August, September, October, November, and December.
* `0 0 L 7 *`: At 12:00 AM, on the last day of the month, only in July.
* `0 0 L * FRI,SAT`: At 12:00 AM, on the last day of the month, and on Friday and Saturday.
* `0 12 L * *`: At 12:00 PM (afternoon), on the last day of the month.
* `0 7 L * 5`: At 07:00 AM, on the last day of the month, and on Friday.
* `30 14 L * *`: At 02:30 PM, on the last day of the month.

##### Trigger on job completion [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[​](#trigger-on-job-completion-- "Direct link to trigger-on-job-completion--")

To *chain* deploy jobs together:

1. In the **Triggers** section, enable the **Run when another job finishes** option.
2. Select the project that has the deploy job you want to run after completion.
3. Specify the upstream (parent) job that, when completed, will trigger your job.
   <!-- -->
   * You can also use the [Create Job API](https://docs.getdbt.com/dbt-cloud/api-v2#/operations/Create%20Job) to do this.
4. In the **Completes on** option, select the job run status(es) that will [enqueue](https://docs.getdbt.com/docs/deploy/job-scheduler.md#scheduler-queue) the deploy job.

[![Example of Trigger on job completion on the Deploy job page](/img/docs/deploy/deploy-job-completion.jpg?v=2 "Example of Trigger on job completion on the Deploy job page")](#)Example of Trigger on job completion on the Deploy job page

5. You can set up a configuration where an upstream job triggers multiple downstream (child) jobs and jobs in other projects. You must have proper [permissions](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions.md#project-role-permissions) to the project and job to configure the trigger.

If another job triggers your job to run, you can find a link to the upstream job in the [run details section](https://docs.getdbt.com/docs/deploy/run-visibility.md#job-run-details).

#### Delete a job[​](#delete-a-job "Direct link to Delete a job")

<!-- -->

To delete a job or multiple jobs in dbt:

1. Click **Deploy** on the navigation header.
2. Click **Jobs** and select the job you want to delete.
3. Click **Settings** on the top right of the page and then click **Edit**.
4. Scroll to the bottom of the page and click **Delete job** to delete the job. <br />

[![Delete a job](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/delete-job.png?v=2 "Delete a job")](#)Delete a job

5. Confirm your action in the pop-up by clicking **Confirm delete** in the bottom right to delete the job immediately. This action cannot be undone. However, you can create a new job with the same information if the deletion was made in error.
6. Refresh the page, and the deleted job should now be gone. If you want to delete multiple jobs, you'll need to perform these steps for each job.

If you're having any issues, feel free to [contact us](mailto:support@getdbt.com) for additional help.

<!-- -->

#### Job monitoring[​](#job-monitoring "Direct link to Job monitoring")

On the **Environments** page, there are two sections that provide an overview of the jobs for that environment:

* **In progress** — Lists the currently in progress jobs with information on when the run started
* **Top jobs by models built** — Ranks jobs by the number of models built over a specific time

[![In progress jobs and Top jobs by models built](/img/docs/deploy/in-progress-top-jobs.png?v=2 "In progress jobs and Top jobs by models built")](#)In progress jobs and Top jobs by models built

#### Job settings history[​](#job-settings-history "Direct link to Job settings history")

You can view historical job settings changes over the last 90 days.

To view the change history:

1. Navigate to **Orchestration** from the main menu and click **Jobs**.
2. Click a **job name**.
3. Click **Settings**.
4. Click **History**.

[![Example of the job settings history.](/img/docs/deploy/job-history.png?v=2 "Example of the job settings history.")](#)Example of the job settings history.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Artifacts](https://docs.getdbt.com/docs/deploy/artifacts.md)
* [Continuous integration (CI) jobs](https://docs.getdbt.com/docs/deploy/ci-jobs.md)
* [Webhooks](https://docs.getdbt.com/docs/deploy/webhooks.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Deploy your metrics StarterEnterpriseEnterprise +

### Deploy your metrics [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

<!-- -->

This section explains how you can perform a job run in your deployment environment in dbt to materialize and deploy your metrics. Currently, the deployment environment is only supported.

1. Once you’ve [defined your semantic models and metrics](https://docs.getdbt.com/guides/sl-snowflake-qs.md?step=10), commit and merge your metric changes in your dbt project.

2. In dbt, create a new [deployment environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md#create-a-deployment-environment) or use an existing environment on dbt 1.6 or higher.

   * Note — Deployment environment is currently supported (*development experience coming soon*)

3. To create a new environment, navigate to **Deploy** in the navigation menu, select **Environments**, and then select **Create new environment**.

4. Fill in your deployment credentials with your Snowflake username and password. You can name the schema anything you want. Click **Save** to create your new production environment.

5. [Create a new deploy job](https://docs.getdbt.com/docs/deploy/deploy-jobs.md#create-and-schedule-jobs) that runs in the environment you just created. Go back to the **Deploy** menu, select **Jobs**, select **Create job**, and click **Deploy job**.

6. Set the job to run a `dbt parse` job to parse your projects and generate a [`semantic_manifest.json` artifact](https://docs.getdbt.com/reference/artifacts/sl-manifest.md) file. Although running `dbt build` isn't required, you can choose to do so if needed.

   note

   If you are on the dbt Fusion engine, add the `dbt docs generate` command to your job to successfully deploy your metrics.

7. Run the job by clicking the **Run now** button. Monitor the job's progress in real-time through the **Run summary** tab.

   Once the job completes successfully, your dbt project, including the generated documentation, will be fully deployed and available for use in your production environment. If any issues arise, review the logs to diagnose and address any errors.

What’s happening internally?

* Merging the code into your main branch allows dbt to pull those changes and build the definition in the manifest produced by the run. <br />
* Re-running the job in the deployment environment helps materialize the models, which the metrics depend on, in the data platform. It also makes sure that the manifest is up to date. <br />
* The Semantic Layer APIs pull in the most recent manifest and enables your integration to extract metadata from it.

#### Next steps[​](#next-steps "Direct link to Next steps")

After you've executed a job and deployed your Semantic Layer:

* [Set up your Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md) in dbt.
* Discover the [available integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md), such as Tableau, Google Sheets, Microsoft Excel, and more.
* Start querying your metrics with the [API query syntax](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-jdbc.md#querying-the-api-for-metric-metadata).

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Optimize querying performance](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-cache.md) using declarative caching.
* [Validate semantic nodes in CI](https://docs.getdbt.com/docs/deploy/ci-jobs.md#semantic-validations-in-ci) to ensure code changes made to dbt models don't break these metrics.
* If you haven't already, learn how to [build your metrics and semantic models](https://docs.getdbt.com/docs/build/build-metrics-intro.md) in your development tool of choice.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Deployment environments

Deployment environments in dbt are crucial for deploying dbt jobs in production and using features or integrations that depend on dbt metadata or results. To execute dbt, environments determine the settings used during job runs, including:

* The version of dbt Core that will be used to run your project
* The warehouse connection information (including the target database/schema settings)
* The version of your code to execute

A dbt project can have multiple deployment environments, providing you the flexibility and customization to tailor the execution of dbt jobs. You can use deployment environments to [create and schedule jobs](https://docs.getdbt.com/docs/deploy/deploy-jobs.md#create-and-schedule-jobs), [enable continuous integration](https://docs.getdbt.com/docs/deploy/continuous-integration.md), or more based on your specific needs or requirements.

Learn how to manage dbt environments

To learn different approaches to managing dbt environments and recommendations for your organization's unique needs, read [dbt environment best practices](https://docs.getdbt.com/guides/set-up-ci.md).

Learn more about development vs. deployment environments in [dbt Environments](https://docs.getdbt.com/docs/dbt-cloud-environments.md).

There are three types of deployment environments:

* **Production**: Environment for transforming data and building pipelines for production use.
* **Staging**: Environment for working with production tools while limiting access to production data.
* **General**: General use environment for deployment development.

We highly recommend using the `Production` environment type for the final, source of truth deployment data. There can be only one environment marked for final production workflows and we don't recommend using a `General` environment for this purpose.

#### Create a deployment environment[​](#create-a-deployment-environment "Direct link to Create a deployment environment")

To create a new dbt deployment environment, navigate to **Deploy** -> **Environments** and then click **Create Environment**. Select **Deployment** as the environment type. The option will be greyed out if you already have a development environment.

[![Navigate to Deploy ->  Environments to create a deployment environment](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/create-deploy-env.png?v=2 "Navigate to Deploy ->  Environments to create a deployment environment")](#)Navigate to Deploy -> Environments to create a deployment environment

##### Set as production environment[​](#set-as-production-environment "Direct link to Set as production environment")

In dbt, each project can have one designated deployment environment, which serves as its production environment. This production environment is *essential* for using features like Catalog and cross-project references. It acts as the source of truth for the project's production state in dbt.

[![Set your production environment as the default environment in your Environment Settings](/img/docs/dbt-cloud/using-dbt-cloud/prod-settings-1.png?v=2 "Set your production environment as the default environment in your Environment Settings")](#)Set your production environment as the default environment in your Environment Settings

##### Semantic Layer[​](#semantic-layer "Direct link to Semantic Layer")

For customers using the Semantic Layer, the next section of environment settings is the Semantic Layer configurations. [The Semantic Layer setup guide](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md) has the most up-to-date setup instructions.

You can also leverage the dbt Job scheduler to [validate your semantic nodes in a CI job](https://docs.getdbt.com/docs/deploy/ci-jobs.md#semantic-validations-in-ci) to ensure code changes made to dbt models don't break these metrics.

#### Staging environment[​](#staging-environment "Direct link to Staging environment")

Use a Staging environment to grant developers access to deployment workflows and tools while controlling access to production data. Staging environments enable you to achieve more granular control over permissions, data warehouse connections, and data isolation — within the purview of a single project in dbt.

##### Git workflow[​](#git-workflow "Direct link to Git workflow")

You can approach this in a couple of ways, but the most straightforward is configuring Staging with a long-living branch (for example, `staging`) similar to but separate from the primary branch (for example, `main`).

In this scenario, the workflows would ideally move upstream from the Development environment -> Staging environment -> Production environment with developer branches feeding into the `staging` branch, then ultimately merging into `main`. In many cases, the `main` and `staging` branches will be identical after a merge and remain until the next batch of changes from the `development` branches are ready to be elevated. We recommend setting branch protection rules on `staging` similar to `main`.

Some customers prefer to connect Development and Staging to their `main` branch and then cut release branches on a regular cadence (daily or weekly), which feeds into Production.

##### Why use a staging environment[​](#why-use-a-staging-environment "Direct link to Why use a staging environment")

These are the primary motivations for using a Staging environment:

1. An additional validation layer before changes are deployed into Production. You can deploy, test, and explore your dbt models in Staging.
2. Clear isolation between development workflows and production data. It enables developers to work in metadata-powered ways, using features like deferral and cross-project references, without accessing data in production deployments.
3. Provide developers with the ability to create, edit, and trigger ad hoc jobs in the Staging environment, while keeping the Production environment locked down using [environment-level permissions](https://docs.getdbt.com/docs/cloud/manage-access/environment-permissions.md).

**Conditional configuration of sources** enables you to point to "prod" or "non-prod" source data, depending on the environment you're running in. For example, this source will point to `<DATABASE>.sensitive_source.table_with_pii`, where `<DATABASE>` is dynamically resolved based on an environment variable.

models/sources.yml
```

Example 3 (unknown):
```unknown
There is exactly one source (`sensitive_source`), and all downstream dbt models select from it as `{{ source('sensitive_source', 'table_with_pii') }}`. The code in your project and the shape of the DAG remain consistent across environments. By setting it up in this way, rather than duplicating sources, you get some important benefits.

**Cross-project references in dbt Mesh:** Let's say you have `Project B` downstream of `Project A` with cross-project refs configured in the models. When developers work in the IDE for `Project B`, cross-project refs will resolve to the Staging environment of `Project A`, rather than production. You'll get the same results with those refs when jobs are run in the Staging environment. Only the Production environment will reference the Production data, keeping the data and access isolated without needing separate projects.

**Faster development enabled by deferral:** If `Project B` also has a Staging deployment, then references to unbuilt upstream models within `Project B` will resolve to that environment, using [deferral](https://docs.getdbt.com/docs/cloud/about-cloud-develop-defer.md), rather than resolving to the models in Production. This saves developers time and warehouse spend, while preserving clear separation of environments.

Finally, the Staging environment has its own view in [Catalog](https://docs.getdbt.com/docs/explore/explore-projects.md), giving you a full view of your prod and pre-prod data.

[![Explore in a staging environment](/img/docs/collaborate/dbt-explorer/explore-staging-env.png?v=2 "Explore in a staging environment")](#)Explore in a staging environment

##### Create a Staging environment[​](#create-a-staging-environment "Direct link to Create a Staging environment")

In the dbt, navigate to **Deploy** -> **Environments** and then click **Create Environment**. Select **Deployment** as the environment type. The option will be greyed out if you already have a development environment.

[![Create a staging environment](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/create-staging-environment.png?v=2 "Create a staging environment")](#)Create a staging environment

Follow the steps outlined in [deployment credentials](#deployment-connection) to complete the remainder of the environment setup.

We recommend that the data warehouse credentials be for a dedicated user or service principal.

#### Deployment connection[​](#deployment-connection "Direct link to Deployment connection")

Warehouse Connections

Warehouse connections are created and managed at the account-level for dbt accounts and assigned to an environment. To change warehouse type, we recommend creating a new environment.

Each project can have multiple connections (Snowflake account, Redshift host, Bigquery project, Databricks host, and so on.) of the same warehouse type. Some details of that connection (databases/schemas/and so on.) can be overridden within this section of the dbt environment settings.

This section determines the exact location in your warehouse dbt should target when building warehouse objects! This section will look a bit different depending on your warehouse provider.

For all warehouses, use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override missing or inactive (grayed-out) settings.

* Postgres
* Redshift
* Snowflake
* Bigquery
* Spark
* Databricks

This section will not appear if you are using Postgres, as all values are inferred from the project's connection. Use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override these values.

This section will not appear if you are using Redshift, as all values are inferred from the project's connection. Use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override these values.

[![Snowflake Deployment Connection Settings](/img/docs/collaborate/snowflake-deploy-env-deploy-connection.png?v=2 "Snowflake Deployment Connection Settings")](#)Snowflake Deployment Connection Settings

###### Editable fields[​](#editable-fields "Direct link to Editable fields")

* **Role**: Snowflake role
* **Database**: Target database
* **Warehouse**: Snowflake warehouse

This section will not appear if you are using Bigquery, as all values are inferred from the project's connection. Use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override these values.

This section will not appear if you are using Spark, as all values are inferred from the project's connection. Use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override these values.

[![Databricks Deployment Connection Settings](/img/docs/collaborate/databricks-deploy-env-deploy-connection.png?v=2 "Databricks Deployment Connection Settings")](#)Databricks Deployment Connection Settings

###### Editable fields[​](#editable-fields-1 "Direct link to Editable fields")

* **Catalog** (optional): [Unity Catalog namespace](https://docs.getdbt.com/docs/core/connect-data-platform/databricks-setup.md)

##### Deployment credentials[​](#deployment-credentials "Direct link to Deployment credentials")

This section allows you to determine the credentials that should be used when connecting to your warehouse. The authentication methods may differ depending on the warehouse and dbt tier you are on.

For all warehouses, use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override missing or inactive (grayed-out) settings. For credentials, we recommend wrapping extended attributes in [environment variables](https://docs.getdbt.com/docs/build/environment-variables.md) (`password: '{{ env_var(''DBT_ENV_SECRET_PASSWORD'') }}'`) to avoid displaying the secret value in the text box and the logs.

* Postgres
* Redshift
* Snowflake
* Bigquery
* Spark
* Databricks

[![Postgres Deployment Credentials Settings](/img/docs/collaborate/postgres-deploy-env-deploy-credentials.png?v=2 "Postgres Deployment Credentials Settings")](#)Postgres Deployment Credentials Settings

###### Editable fields[​](#editable-fields-2 "Direct link to Editable fields")

* **Username**: Postgres username to use (most likely a service account)
* **Password**: Postgres password for the listed user
* **Schema**: Target schema

[![Redshift Deployment Credentials Settings](/img/docs/collaborate/postgres-deploy-env-deploy-credentials.png?v=2 "Redshift Deployment Credentials Settings")](#)Redshift Deployment Credentials Settings

###### Editable fields[​](#editable-fields-3 "Direct link to Editable fields")

* **Username**: Redshift username to use (most likely a service account)
* **Password**: Redshift password for the listed user
* **Schema**: Target schema

[![Snowflake Deployment Credentials Settings](/img/docs/collaborate/snowflake-deploy-env-deploy-credentials.png?v=2 "Snowflake Deployment Credentials Settings")](#)Snowflake Deployment Credentials Settings

###### Editable fields[​](#editable-fields-4 "Direct link to Editable fields")

* **Auth Method**: This determines the way dbt connects to your warehouse
  <!-- -->
  * One of: \[**Username & Password**, **Key Pair**]

* If **Username & Password**:

  <!-- -->

  * **Username**: username to use (most likely a service account)
  * **Password**: password for the listed user

* If **Key Pair**:

  <!-- -->

  * **Username**: username to use (most likely a service account)
  * **Private Key**: value of the Private SSH Key (optional)
  * **Private Key Passphrase**: value of the Private SSH Key Passphrase (optional, only if required)

* **Schema**: Target Schema for this environment

[![Bigquery Deployment Credentials Settings](/img/docs/collaborate/bigquery-deploy-env-deploy-credentials.png?v=2 "Bigquery Deployment Credentials Settings")](#)Bigquery Deployment Credentials Settings

###### Editable fields[​](#editable-fields-5 "Direct link to Editable fields")

* **Dataset**: Target dataset

Use [extended attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) to override missing or inactive (grayed-out) settings. For credentials, we recommend wrapping extended attributes in [environment variables](https://docs.getdbt.com/docs/build/environment-variables.md) (`password: '{{ env_var(''DBT_ENV_SECRET_PASSWORD'') }}'`) to avoid displaying the secret value in the text box and the logs.

[![Spark Deployment Credentials Settings](/img/docs/collaborate/spark-deploy-env-deploy-credentials.png?v=2 "Spark Deployment Credentials Settings")](#)Spark Deployment Credentials Settings

###### Editable fields[​](#editable-fields-6 "Direct link to Editable fields")

* **Token**: Access token
* **Schema**: Target schema

[![Databricks Deployment Credentials Settings](/img/docs/collaborate/spark-deploy-env-deploy-credentials.png?v=2 "Databricks Deployment Credentials Settings")](#)Databricks Deployment Credentials Settings

###### Editable fields[​](#editable-fields-7 "Direct link to Editable fields")

* **Token**: Access token
* **Schema**: Target schema

#### Delete an environment[​](#delete-an-environment "Direct link to Delete an environment")

<!-- -->

Deleting an environment automatically deletes its associated job(s). If you want to keep those jobs, move them to a different environment first.

Follow these steps to delete an environment in dbt:

1. Click **Deploy** on the navigation header and then click **Environments**
2. Select the environment you want to delete.
3. Click **Settings** on the top right of the page and then click **Edit**.
4. Scroll to the bottom of the page and click **Delete** to delete the environment.

[![Delete an environment](/img/docs/dbt-cloud/cloud-configuring-dbt-cloud/delete-environment.png?v=2 "Delete an environment")](#)Delete an environment

5. Confirm your action in the pop-up by clicking **Confirm delete** in the bottom right to delete the environment immediately. This action cannot be undone. However, you can create a new environment with the same information if the deletion was made in error.
6. Refresh your page and the deleted environment should now be gone. To delete multiple environments, you'll need to perform these steps to delete each one.

If you're having any issues, feel free to [contact us](mailto:support@getdbt.com) for additional help.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [dbt environment best practices](https://docs.getdbt.com/guides/set-up-ci.md)
* [Deploy jobs](https://docs.getdbt.com/docs/deploy/deploy-jobs.md)
* [CI jobs](https://docs.getdbt.com/docs/deploy/continuous-integration.md)
* [Delete a job or environment in dbt](https://docs.getdbt.com/faqs/Environments/delete-environment-job.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Derived metrics

In MetricFlow, derived metrics are metrics created by defining an expression using other metrics. They enable you to perform calculations with existing metrics. This is helpful for combining metrics and doing math functions on aggregated columns, like creating a profit metric.

The parameters, description, and type for derived metrics are:

| Parameter       | Description                                                                                                                                           | Required | Type   |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------ |
| `name`          | The name of the metric.                                                                                                                               | Required | String |
| `description`   | The description of the metric.                                                                                                                        | Optional | String |
| `type`          | The type of the metric (cumulative, derived, ratio, or simple).                                                                                       | Required | String |
| `label`         | Defines the display value in downstream tools. Accepts plain text, spaces, and quotes (such as `orders_total` or `"orders_total"`).                   | Required | String |
| `type_params`   | The type parameters of the metric.                                                                                                                    | Required | Dict   |
| `expr`          | The derived expression. You'll see validation warnings when the derived metric is missing an `expr` or the `expr` does not use all the input metrics. | Required | String |
| `metrics`       | The list of metrics used in the derived metrics. Each entry can include optional fields like `alias`, `filter`, or `offset_window`.                   | Required | List   |
| `alias`         | Optional alias for the metric that you can use in the `expr`.                                                                                         | Optional | String |
| `filter`        | Optional filter to apply to the metric.                                                                                                               | Optional | String |
| `offset_window` | Set the period for the offset window, such as 1 month. This will return the value of the metric one month from the metric time.                       | Optional | String |

The following displays the complete specification for derived metrics, along with an example.
```

Example 4 (unknown):
```unknown
For advanced data modeling, you can use `fill_nulls_with` and `join_to_timespine` to [set null metric values to zero](https://docs.getdbt.com/docs/build/fill-nulls-advanced.md), ensuring numeric values for every data row.

#### Derived metrics example[​](#derived-metrics-example "Direct link to Derived metrics example")
```

---
