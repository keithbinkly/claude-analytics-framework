# Jinja-Sql-Optimizer - Other

**Pages:** 125

---

## .

**URL:** llms-txt#.

---

## my test_is_valid_email_address unit test will run on all versions of my_model

**URL:** llms-txt#my-test_is_valid_email_address-unit-test-will-run-on-all-versions-of-my_model

unit_tests:
  - name: test_is_valid_email_address
    model: my_model
    ...

---

## run all tests that failed on the prior invocation of dbt test

**URL:** llms-txt#run-all-tests-that-failed-on-the-prior-invocation-of-dbt-test

dbt test --select "result:fail" --state path/to/artifacts

---

## │   └── goals.sql

**URL:** llms-txt#│  -└──-goals.sql

---

## Unnest the executionInfo column

**URL:** llms-txt#unnest-the-executioninfo-column

models_df = pd.concat([models_df.drop(['executionInfo'], axis=1), models_df['executionInfo'].apply(pd.Series)], axis=1)

---

## run unit tests limited to one_specific_model

**URL:** llms-txt#run-unit-tests-limited-to-one_specific_model

**Contents:**
  - About dbt_project.yml context

dbt test --select "one_specific_model,test_type:unit"

name: my_project
version: 1.0.0

**Examples:**

Example 1 (unknown):
```unknown
For more information on writing tests, read the [data testing](https://docs.getdbt.com/docs/build/data-tests.md) and [unit testing](https://docs.getdbt.com/docs/build/unit-tests.md) documentation.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About dbt_project.yml context

The following context methods and variables are available when configuring resources in the `dbt_project.yml` file. This applies to the `models:`, `seeds:`, and `snapshots:` keys in the `dbt_project.yml` file.

**Available context methods:**

* [env\_var](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var.md)
* [var](https://docs.getdbt.com/reference/dbt-jinja-functions/var.md) (*Note: only variables defined with `--vars` are available*)

**Available context variables:**

* [target](https://docs.getdbt.com/reference/dbt-jinja-functions/target.md)
* [builtins](https://docs.getdbt.com/reference/dbt-jinja-functions/builtins.md)
* [dbt\_version](https://docs.getdbt.com/reference/dbt-jinja-functions/dbt_version.md)

##### Example configuration[​](#example-configuration "Direct link to Example configuration")

dbt\_project.yml
```

---

## query the first metric by `metric_time`

**URL:** llms-txt#query-the-first-metric-by-`metric_time`

def main():
    with client.session():
        metrics = client.metrics()
        table = client.query(
            metrics=[metrics[0].name],
            group_by=["metric_time"],
        )
        print(table)

import asyncio
from dbtsl.asyncio import AsyncSemanticLayerClient

client = AsyncSemanticLayerClient(
    environment_id=123,
    auth_token="<your-semantic-layer-api-token>",
    host="semantic-layer.cloud.getdbt.com",
)

async def main():
    async with client.session():
        metrics = await client.metrics()
        table = await client.query(
            metrics=[metrics[0].name],
            group_by=["metric_time"],
        )
        print(table)

"""Fetch all available metrics from the metadata API and display only the dimensions of certain metrics."""

from argparse import ArgumentParser

from dbtsl import SemanticLayerClient

def get_arg_parser() -> ArgumentParser:
    p = ArgumentParser()

p.add_argument("--env-id", required=True, help="The dbt environment ID", type=int)
    p.add_argument("--token", required=True, help="The API auth token")
    p.add_argument("--host", required=True, help="The API host")

def main() -> None:
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

client = SemanticLayerClient(
        environment_id=args.env_id,
        auth_token=args.token,
        host=args.host,
        lazy=True,
    )

with client.session():
        metrics = client.metrics()
        for i, m in enumerate(metrics):
            print(f"📈 {m.name}")
            print(f"     type={m.type}")
            print(f"     description={m.description}")

assert len(m.dimensions) == 0

# skip if index is odd
            if i & 1:
                print("     dimensions=skipped")
                continue

# load dimensions only if index is even
            m.load_dimensions()

print("     dimensions=[")
            for dim in m.dimensions:
                print(f"        {dim.name},")
            print("     ]")

if __name__ == "__main__":
    main()

**Examples:**

Example 1 (unknown):
```unknown
**Note**: All method calls that reach out to the APIs need to be within a `client.session()` context manager. This allows the client to establish a connection to the APIs only once and reuse the same connection between API calls.

We recommend creating an application-wide session and reusing the same session throughout the application for optimal performance. Creating a session per request is discouraged and inefficient.

##### asyncio usage[​](#asyncio-usage "Direct link to asyncio usage")

If you're using asyncio, import `AsyncSemanticLayerClient` from `dbtsl.asyncio`. The `SemanticLayerClient` and `AsyncSemanticLayerClient` APIs are identical, but the async version has async methods that you need to `await`.
```

Example 2 (unknown):
```unknown
##### Lazy loading for large fields[​](#lazy-loading-for-large-fields "Direct link to Lazy loading for large fields")

By default, the Python SDK eagerly loads nested lists of objects such as `dimensions`, `entities`, and `measures` for each `Metric` — even if you don't need them. This is generally convenient, but in large projects, it can lead to slower responses due to the amount of data returned.

To improve performance, you can opt into lazy loading by passing `lazy=True` when creating the client. With lazy loading enabled, the SDK skips fetching large nested fields until you explicitly request them on a per-model basis.

Lazy loading is currently only supported for `dimensions`, `entities`, and `measures` on `Metric` objects.

For example, the following code fetches all available metrics from the metadata API and displays only the dimensions of certain metrics:

list\_metrics\_lazy\_sync.py
```

Example 3 (unknown):
```unknown
Refer to the [lazy loading example](https://github.com/dbt-labs/semantic-layer-sdk-python/blob/main/examples/list_metrics_lazy_sync.py) for more details.

#### Integrate with dataframe libraries[​](#integrate-with-dataframe-libraries "Direct link to Integrate with dataframe libraries")

The Python SDK returns all query data as [pyarrow](https://arrow.apache.org/docs/python/index.html) tables.

The Python SDK library doesn't come bundled with [Polars](https://pola.rs/) or [Pandas](https://pandas.pydata.org/). If you use these libraries, add them as dependencies in your project.

To use the data with libraries like Polars or Pandas, manually convert the data into the desired format. For example:

###### If you're using pandas[​](#if-youre-using-pandas "Direct link to If you're using pandas")
```

---

## run only data tests

**URL:** llms-txt#run-only-data-tests

dbt test --select test_type:data

---

## models/my_model.yml

**URL:** llms-txt#models/my_model.yml

my_model_yml = """
version: 2
models:
  - name: my_model
    columns:
      - name: id
        data_tests:
          - unique
          - not_null  # this test will fail
"""

import pytest
from dbt.tests.util import run_dbt

**Examples:**

Example 1 (unknown):
```unknown
2. Use the "fixtures" to define the project for your test case. These fixtures are always scoped to the **class**, where the class represents one test case—that is, one dbt project or scenario. (The same test case can be used for one or more actual tests, which we'll see in step 3.) Following the default pytest configurations, the file name must begin with `test_`, and the class name must begin with `Test`.

tests/functional/example/test\_example\_failing\_test.py
```

---

## Run tests on two or more specific models (indirect selection)

**URL:** llms-txt#run-tests-on-two-or-more-specific-models-(indirect-selection)

dbt test --select "customers orders"

---

## Snapshot freshness for all Jaffle Shop tables:

**URL:** llms-txt#snapshot-freshness-for-all-jaffle-shop-tables:

$ dbt source freshness --select source:jaffle_shop

---

## The account_id is 16173 and the job_id is 65767

**URL:** llms-txt#the-account_id-is-16173-and-the-job_id-is-65767

---

## create CLI args as a list of strings

**URL:** llms-txt#create-cli-args-as-a-list-of-strings

cli_args = ["run", "--select", "tag:my_tag"]

---

## Run tests on a model (indirect selection)

**URL:** llms-txt#run-tests-on-a-model-(indirect-selection)

dbt test --select "customers"

---

## snapshot

**URL:** llms-txt#snapshot

**Contents:**
  - Exit codes
  - Exposure properties

dbt snapshot --exclude "snap_order_statuses"    # execute all snapshots except snap_order_statuses

exposures:
  - name: <string_with_underscores>
    description: <markdown_string>
    type: {dashboard, notebook, analysis, ml, application}
    url: <string>
    maturity: {high, medium, low}  # Indicates level of confidence or stability in the exposure
    enabled: true | false
    config: # 'tags' and 'meta' changed to config in v1.10
      tags: [<string>] 
      meta: {<dictionary>}
      enabled: true | false
    owner: # supports 'name' and 'email' only
      name: <string>
      email: <string>
    
    depends_on:
      - ref('model')
      - ref('seed')
      - source('name', 'table')
      - metric('metric_name')
      
    label: "Human-Friendly Name for this Exposure!"

- name: ... # declare properties of additional exposures

- name: weekly_jaffle_metrics
    label: Jaffles by the Week              # optional
    type: dashboard                         # required
    maturity: high                          # optional
    url: https://bi.tool/dashboards/1       # optional
    description: >                          # optional
      Did someone say "exponential growth"?

depends_on:                             # expected
      - ref('fct_orders')
      - ref('dim_customers')
      - source('gsheets', 'goals')
      - metric('count_orders')

owner:
      name: Callum McData
      email: data@jaffleshop.com

- name: jaffle_recommender
    maturity: medium
    type: ml
    url: https://jupyter.org/mycoolalg
    description: >
      Deep learning to power personalized "Discover Sandwiches Weekly"
    
    depends_on:
      - ref('fct_orders')
      
    owner:
      name: Data Science Drew
      email: data@jaffleshop.com

- name: jaffle_wrapped
    type: application
    description: Tell users about their favorite jaffles of the year
    depends_on: [ ref('fct_orders') ]
    owner: { email: summer-intern@jaffleshop.com }

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Exit codes

When dbt exits, it will return an exit code of either 0, 1, or 2.

| Exit Code | Condition                                                                                                                                                                  |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0         | The dbt invocation completed without error.                                                                                                                                |
| 1         | The dbt invocation completed with at least one handled error (eg. model syntax error, bad permissions, etc). The run was completed, but some models may have been skipped. |
| 2         | The dbt invocation completed with an unhandled error (eg. ctrl-c, network interruption, etc).                                                                              |

While these exit codes may change in the future, a zero exit code will always imply success whereas a nonzero exit code will always imply failure.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Exposure properties

#### Related documentation[​](#related-documentation "Direct link to Related documentation")

* [Using exposures](https://docs.getdbt.com/docs/build/exposures.md)
* [Declaring resource properties](https://docs.getdbt.com/reference/configs-and-properties.md)

#### Overview[​](#overview "Direct link to Overview")

<!-- -->

Exposures are defined in `properties.yml` files nested under an `exposures:` key. You may define `exposures` in YAML files that also define `sources` or `models`. Exposure properties<!-- --> are "special properties" in that you can't configure them in the `dbt_project.yml` file or using `config()` blocks. Refer to [Configs and properties](https://docs.getdbt.com/reference/define-properties#which-properties-are-not-also-configs) for more info.<br />

Note that while most exposure properties must be configured directly in these YAML files, you can set the [`enabled`](https://docs.getdbt.com/reference/resource-configs/enabled.md) config at the [project level](#project-level-configs) in the`dbt_project.yml` file.

You can name these files `whatever_you_want.yml`, and nest them arbitrarily deeply in subfolders within the `models/` directory.

Exposure names must contain only letters, numbers, and underscores (no spaces or special characters). For a short human-friendly name with title casing, spaces, and special characters, use the `label` property.

models/\<filename>.yml
```

Example 2 (unknown):
```unknown
#### Example[​](#example "Direct link to Example")

models/jaffle/exposures.yml
```

Example 3 (unknown):
```unknown
###### Project-level configs[​](#project-level-configs "Direct link to Project-level configs")

You can define project-level configs for exposures in the `dbt_project.yml` file under the `exposures:` key using the `+` prefix. Currently, only the [`enabled` config](https://docs.getdbt.com/reference/resource-configs/enabled.md) is supported:

dbt\_project.yml
```

---

## Run tests upstream of a model (indirect selection)

**URL:** llms-txt#run-tests-upstream-of-a-model-(indirect-selection)

dbt test --select "+stg_customers"

---

## our file contents

**URL:** llms-txt#our-file-contents

from tests.functional.example.fixtures import (
    my_seed_csv,
    my_model_sql,
    my_model_yml,
)

---

## │   ├── employees.sql

**URL:** llms-txt#│  -├──-employees.sql

---

## in models/__groups.yml

**URL:** llms-txt#in-models/__groups.yml

groups: 
  - name: marketing
    owner:
        name: Ben Jaffleck 
        email: ben.jaffleck@jaffleshop.com

**Examples:**

Example 1 (unknown):
```unknown
* Then, we can add models to that group using the `group:` key in the model's YAML entry.
```

---

## ✅ These will work

**URL:** llms-txt#✅-these-will-work

require-dbt-version: ">=1.0.0" # Double quotes are OK
require-dbt-version: '>=1.0.0' # So are single quotes

---

## Git package

**URL:** llms-txt#git-package

dbt deps --add-package https://github.com/fivetran/dbt_amplitude@v0.3.0 --source git

---

## In the dbt platform

**URL:** llms-txt#in-the-dbt-platform

dbt sl query --metrics order_total --group-by metric_time,is_food_order --limit 10 --order-by -metric_time --where "is_food_order = True" --start-time '2017-08-22' --end-time '2017-08-27' --compile

---

## run only unit tests

**URL:** llms-txt#run-only-unit-tests

dbt test --select test_type:unit

---

## Zapier looks for the `output` dictionary for use in subsequent steps

**URL:** llms-txt#zapier-looks-for-the-`output`-dictionary-for-use-in-subsequent-steps

output = {'step_summary_post': step_summary_post, 'send_error_thread': send_error_thread, 'threaded_errors_post': threaded_errors_post}

store = StoreClient('abc123') #replace with your UUID secret
store.set('DBT_CLOUD_SERVICE_TOKEN', 'abc123') #replace with your <Constant name="cloud" /> API token
`
import re

**Examples:**

Example 1 (unknown):
```unknown
#### Add Slack actions in Zapier[​](#add-slack-actions-in-zapier "Direct link to Add Slack actions in Zapier")

Select **Slack** as the App, and **Send Channel Message** as the Action.

In the **Action** section, choose which **Channel** to post to. Set the **Message Text** field to **2. Step Summary Post** from the Run Python in Code by Zapier output.

Configure the other options as you prefer (for example, **Bot Name** and **Bot Icon**).

![Screenshot of the Zapier UI, showing the mappings of prior steps to a Slack message](/assets/images/parent-slack-config-39e85487efcfb04136c351992ed08cb9.png)

Add another step, **Filter**. In the **Filter setup and testing** section, set the **Field** to **2. Send Error Thread** and the **condition** to **(Boolean) Is true**. This prevents the Zap from failing if the job succeeded and you try to send an empty Slack message in the next step.

![Screenshot of the Zapier UI, showing the correctly configured Filter step](/assets/images/filter-config-5a7f7eca78c49d24fd5b8674f23337e3.png)

Add another **Send Channel Message in Slack** action. In the **Action** section, choose the same channel as last time, but set the **Message Text** to **2. Threaded Errors Post** from the same Run Python step. Set the **Thread** value to **3. Message Ts**, which is the timestamp of the post created by the first Slack action. This tells Zapier to add this post as a threaded reply to the main message, which prevents the full (potentially long) output from cluttering your channel.

![Screenshot of the Zapier UI, showing the mappings of prior steps to a Slack message](/assets/images/thread-slack-config-9ebe2df87964d97e82c18d80d9ff9ac2.png)

#### Test and deploy[​](#test-and-deploy "Direct link to Test and deploy")

When you're done testing your Zap, make sure that your `run_id` and `account_id` are no longer hardcoded in the Code step, then publish your Zap.

#### Alternately, use a dbt app Slack message to trigger Zapier[​](#alternately-use-a-dbt-app-slack-message-to-trigger-zapier "Direct link to Alternately, use a dbt app Slack message to trigger Zapier")

Instead of using a webhook as your trigger, you can keep the existing dbt app installed in your Slack workspace and use its messages being posted to your channel as the trigger. In this case, you can skip validating the webhook and only need to load the context from the thread.

##### 1. Create a new Zap in Zapier[​](#1-create-a-new-zap-in-zapier "Direct link to 1. Create a new Zap in Zapier")

Use **Slack** as the initiating app, and **New Message Posted to Channel** as the Trigger. In the **Trigger** section, select the channel where your Slack alerts are being posted, and set **Trigger for Bot Messages?** to **Yes**.

![Screenshot of the Zapier UI, showing the correctly configured Message trigger step](/assets/images/message-trigger-config-432c82983008423e7914d0c59eab38cd.png)

Test your Zap to find an example record. You might need to load additional samples until you get one that relates to a failed job, depending on whether you post all job events to Slack or not.

##### 2. Add a Filter step[​](#2-add-a-filter-step "Direct link to 2. Add a Filter step")

Add a **Filter** step with the following conditions:

* **1. Text contains failed on Job**
* **1. User Is Bot Is true**
* **1. User Name Exactly matches dbt**

![Screenshot of the Zapier UI, showing the correctly configured Filter step](/assets/images/message-trigger-filter-57c4f8c530e21a72704481619b040a51.png)

##### 3. Extract the run ID[​](#3-extract-the-run-id "Direct link to 3. Extract the run ID")

Add a **Format** step with the **Event** of **Text**, and the Action **Extract Number**. For the **Input**, select **1. Text**.

![Screenshot of the Zapier UI, showing the Transform step configured to extract a number from the Slack message\&#39;s Text property](/assets/images/extract-number-e9674c26f01614ccfd93b7fdefaab3ed.png)

Test your step and validate that the run ID has been correctly extracted.

##### 4. Add a Delay[​](#4-add-a-delay "Direct link to 4. Add a Delay")

Sometimes dbt posts the message about the run failing before the run's artifacts are available through the API. For this reason, it's recommended to add a brief delay to increase the likelihood that the data is available. On certain plans, Zapier will automatically retry a job that fails from to a 404 error, but its standdown period is longer than is normally necessary so the context will be missing from your thread for longer.

A one-minute delay is generally sufficient.

##### 5. Store secrets[​](#5-store-secrets "Direct link to 5. Store secrets")

In the next step, you will need either a dbt [personal access token](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md) or [service account token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md).

Zapier allows you to [store secrets](https://help.zapier.com/hc/en-us/articles/8496293271053-Save-and-retrieve-data-from-Zaps). This prevents your keys from being displayed as plaintext in the Zap code. You can access them with the [StoreClient utility](https://help.zapier.com/hc/en-us/articles/8496293969549-Store-data-from-code-steps-with-StoreClient).

This guide assumes the name for the secret key is `DBT_CLOUD_SERVICE_TOKEN`. If you're using a different name, make sure you update all references to it in the sample code.

This guide uses a short-lived code action to store the secrets, but you can also use a tool like Postman to interact with the [REST API](https://store.zapier.com/) or create a separate Zap and call the [Set Value Action](https://help.zapier.com/hc/en-us/articles/8496293271053-Save-and-retrieve-data-from-Zaps#3-set-a-value-in-your-store-0-3).

###### a. Create a Storage by Zapier connection[​](#a-create-a-storage-by-zapier-connection "Direct link to a. Create a Storage by Zapier connection")

If you haven't already got one, go to <https://zapier.com/app/connections/storage> and create a new connection. Remember the UUID secret you generate for later.

###### b. Add a temporary code step[​](#b-add-a-temporary-code-step "Direct link to b. Add a temporary code step")

Choose **Run Python** as the Event. Run the following code:
```

Example 2 (unknown):
```unknown
Test the step. You can delete this Action when the test succeeds. The key will remain stored as long as it is accessed at least once every three months.

##### 6. Add a Code action[​](#6-add-a-code-action "Direct link to 6. Add a Code action")

Select **Code by Zapier** as the App, and **Run Python** as the Event.

This step is very similar to the one described in the main example, but you can skip a lot of the initial validation work.

In the **Action** section, add two items to **Input Data**: `run_id` and `account_id`. Map those to the `3. Output` property and your hardcoded dbt Account ID, respectively.

![Screenshot of the Zapier UI, showing the mappings of raw\_body and auth\_header](/assets/images/code-example-alternate-bbb2b5028df008f1b6832e8453215ff4.png)

In the **Code** field, paste the following code, replacing `YOUR_SECRET_HERE` with the secret you created when setting up the Storage by Zapier integration. Remember that this is not your dbt secret.

This example code extracts the run logs for the completed job from the Admin API, and then builds a message displaying any error messages extracted from the end-of-invocation logs created by dbt Core (which will be posted in a thread).
```

---

## works

**URL:** llms-txt#works

host: "{{ env_var('DBT_ENV_SECRET_HOST') }}"

---

## Get the uniqueId of the longest running model

**URL:** llms-txt#get-the-uniqueid-of-the-longest-running-model

longest_running_model = models_df_sorted.iloc[0]['uniqueId']

---

## Import libraries

**URL:** llms-txt#import-libraries

import os
import matplotlib.pyplot as plt
import pandas as pd
import requests

---

## ignore all folders in a directory

**URL:** llms-txt#ignore-all-folders-in-a-directory

---

## Run tests on all models in the models/staging/jaffle_shop directory (indirect selection)

**URL:** llms-txt#run-tests-on-all-models-in-the-models/staging/jaffle_shop-directory-(indirect-selection)

dbt test --select "staging.jaffle_shop"

---

## Using @pytest.mark.skip_profile('apache_spark') uses the 'skip_by_profile_type'

**URL:** llms-txt#using-@pytest.mark.skip_profile('apache_spark')-uses-the-'skip_by_profile_type'

---

## dbt_project.yml

**URL:** llms-txt#dbt_project.yml

flags:
  # set default for running this project -- anywhere, anytime, by anyone
  fail_fast: true

**Examples:**

Example 1 (unknown):
```unknown

```

---

## run tests for one_specific_model

**URL:** llms-txt#run-tests-for-one_specific_model

dbt test --select "one_specific_model"

---

## run data tests limited to one_specific_model

**URL:** llms-txt#run-data-tests-limited-to-one_specific_model

dbt test --select "one_specific_model,test_type:data"

---

## Validate the webhook came from dbt

**URL:** llms-txt#validate-the-webhook-came-from-dbt

**Contents:**
  - Refresh Tableau workbook with extracts after a job finishes

signature = hmac.new(hook_secret.encode('utf-8'), raw_body.encode('utf-8'), hashlib.sha256).hexdigest()

if signature != auth_header:
  raise Exception("Calculated signature doesn't match contents of the Authorization header. This webhook may not have been sent from <Constant name="cloud" />.")

full_body = json.loads(raw_body)
hook_data = full_body['data']

if hook_data['runStatus'] == "Success":

# Create a report run with the Mode API
  url = f'https://app.mode.com/api/{account_username}/reports/{report_token}/run'

params = {
    'parameters': {
      "user_id": 123, 
      "location": "San Francisco"
    } 
  }
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/hal+json'
  }
  response = requests.post(
    url, 
    json=params, 
    headers=headers, 
    auth=HTTPBasicAuth(username, password)
  )
  response.raise_for_status()

store = StoreClient('abc123') #replace with your UUID secret
store.set('DBT_WEBHOOK_KEY', 'abc123') #replace with your <Constant name="cloud" /> Webhook key
store.set('TABLEAU_SITE_URL', 'abc123') #replace with your Tableau Site URL, inclusive of https:// and .com
store.set('TABLEAU_SITE_NAME', 'abc123') #replace with your Tableau Site/Server Name
store.set('TABLEAU_API_TOKEN_NAME', 'abc123') #replace with your Tableau API Token Name
store.set('TABLEAU_API_TOKEN_SECRET', 'abc123') #replace with your Tableau API Secret

import requests
import hashlib
import json
import hmac

**Examples:**

Example 1 (unknown):
```unknown
#### Test and deploy[​](#test-and-deploy "Direct link to Test and deploy")

You can iterate on the Code step by modifying the code and then running the test again. When you're happy with it, you can publish your Zap.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Refresh Tableau workbook with extracts after a job finishes

[Back to guides](https://docs.getdbt.com/guides.md)

Webhooks

Advanced

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

This guide will teach you how to refresh a Tableau workbook that leverages [extracts](https://help.tableau.com/current/pro/desktop/en-us/extracting_data.htm) when a dbt job has completed successfully and there is fresh data available. The integration will:

* Receive a webhook notification in Zapier
* Trigger a refresh of a Tableau workbook

##### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

To set up the integration, you need to be familiar with:

* [dbt Webhooks](https://docs.getdbt.com/docs/deploy/webhooks.md)
* Zapier
* The [Tableau API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm)
* The [version](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_versions.htm#rest_api_versioning) of Tableau's REST API that is compatible with your server

#### Obtain authentication credentials from Tableau[​](#obtain-authentication-credentials-from-tableau "Direct link to Obtain authentication credentials from Tableau")

To authenticate with the Tableau API, obtain a [Personal Access Token](https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm) from your Tableau Server/Cloud instance. In addition, make sure your Tableau workbook uses data sources that allow refresh access, which is usually set when publishing.

#### Create a new Zap in Zapier[​](#create-a-new-zap-in-zapier "Direct link to Create a new Zap in Zapier")

To trigger an action with the delivery of a webhook in Zapier, you'll want to create a new Zap with **Webhooks by Zapier** as the Trigger and **Catch Raw Hook** as the Event. However, if you choose not to [validate the authenticity of your webhook](https://docs.getdbt.com/docs/deploy/webhooks.md#validate-a-webhook), which isn't recommended, you can choose **Catch Hook** instead.

Press **Continue**, then copy the webhook URL.

![Screenshot of the Zapier UI, showing the webhook URL ready to be copied](/assets/images/catch-raw-hook-16dd72d8a6bc26284c5fad897f3da646.png)

#### Configure a new webhook in dbt[​](#configure-a-new-webhook-in-dbt "Direct link to Configure a new webhook in dbt")

To set up a webhook subscription for dbt, follow the instructions in [Create a webhook subscription](https://docs.getdbt.com/docs/deploy/webhooks.md#create-a-webhook-subscription). For the event, choose **Run completed** and modify the **Jobs** list to include only the jobs that should trigger a report refresh.

Remember to save the Webhook Secret Key for later. Paste in the webhook URL obtained from Zapier in step 2 into the **Endpoint** field and test the endpoint.

Once you've tested the endpoint in dbt, go back to Zapier and click **Test Trigger**, which will create a sample webhook body based on the test event dbt sent.

The sample body's values are hard-coded and not reflective of your project, but they give Zapier a correctly-shaped object during development.

#### Store secrets[​](#store-secrets "Direct link to Store secrets")

In the next step, you will need the Webhook Secret Key from the prior step, and your Tableau authentication credentials and details. Specifically, you'll need your Tableau server/site URL, server/site name, PAT name, and PAT secret.

Zapier allows you to [store secrets](https://help.zapier.com/hc/en-us/articles/8496293271053-Save-and-retrieve-data-from-Zaps), which prevents your keys from being displayed in plaintext in the Zap code. You will be able to access them via the [StoreClient utility](https://help.zapier.com/hc/en-us/articles/8496293969549-Store-data-from-code-steps-with-StoreClient).

This guide assumes the names for the secret keys are: `DBT_WEBHOOK_KEY`, `TABLEAU_SITE_URL`, `TABLEAU_SITE_NAME`, `TABLEAU_API_TOKEN_NAME`, and `TABLEAU_API_TOKEN_SECRET`. If you are using different names, make sure you update all references to them in the sample code.

This guide uses a short-lived code action to store the secrets, but you can also use a tool like Postman to interact with the [REST API](https://store.zapier.com/) or create a separate Zap and call the [Set Value Action](https://help.zapier.com/hc/en-us/articles/8496293271053-Save-and-retrieve-data-from-Zaps#3-set-a-value-in-your-store-0-3).

##### a. Create a Storage by Zapier connection[​](#a-create-a-storage-by-zapier-connection "Direct link to a. Create a Storage by Zapier connection")

Create a new connection at <https://zapier.com/app/connections/storage> if you don't already have one and remember the UUID secret you generate for later.

##### b. Add a temporary code step[​](#b-add-a-temporary-code-step "Direct link to b. Add a temporary code step")

Choose **Run Python** as the Event and input the following code:
```

Example 2 (unknown):
```unknown
Test the step to run the code. You can delete this action when the test succeeds. The keys will remain stored as long as it is accessed at least once every three months.

#### Add a code action[​](#add-a-code-action "Direct link to Add a code action")

Select **Code by Zapier** as the App, and **Run Python** as the Event.

In the **Set up action** area, add two items to **Input Data**: `raw_body` and `auth_header`. Map those to the `1. Raw Body` and `1. Headers Http Authorization` fields from the **Catch Raw Hook** step above.

![Screenshot of the Zapier UI, showing the mappings of raw\_body and auth\_header](/assets/images/run-python-40333883c6a20727c02d25224d0e40a4.png)

In the **Code** field, paste the following code, replacing `YOUR_STORAGE_SECRET_HERE` in the StoreClient constructor with the UUID secret you created when setting up the Storage by Zapier integration, and replacing the `workbook_name` and `api_version` variables to actual values.

The following code validates the authenticity of the request and obtains the workbook ID for the specified workbook name. Next, the code will send a [`update workbook` command to the Tableau API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_now) for the given workbook ID.
```

---

## job 1

**URL:** llms-txt#job-1

dbt source freshness # must be run to get previous state

**Examples:**

Example 1 (unknown):
```unknown
Test all my sources that are fresher than the previous run, and run and test all models downstream of them:
```

---

## Note: fixtures with session scope need to be local

**URL:** llms-txt#note:-fixtures-with-session-scope-need-to-be-local

pytest_plugins = ["dbt.tests.fixtures.project"]

---

## Snapshot freshness for all Snowplow tables:

**URL:** llms-txt#snapshot-freshness-for-all-snowplow-tables:

$ dbt source freshness --select "source:snowplow"

---

## run data and unit tests

**URL:** llms-txt#run-data-and-unit-tests

---

## Construct a lineage graph with freshness info

**URL:** llms-txt#construct-a-lineage-graph-with-freshness-info

**Contents:**
- Best Practices
  - Available materializations
  - Best practice guides
  - Best practices
  - Best practices for dbt and Unity Catalog
  - Best practices for materializations
  - Best practices for workflows

def create_freshness_graph(models_df, sources_df):
    G = nx.DiGraph()
    current_time = datetime.now(timezone.utc)
    for _, model in models_df.iterrows():
        max_freshness = pd.Timedelta.min
        if "meta" in models_df.columns:
          freshness_sla = model["meta"]["freshness_sla"]
        else:
          freshness_sla = None
        if model["executionInfo"]["executeCompletedAt"] is not None:
          model_freshness = current_time - pd.Timestamp(model["executionInfo"]["executeCompletedAt"])
          for ancestor in model["ancestors"]:
              if ancestor["resourceType"] == "SourceAppliedStateNestedNode":
                  ancestor_freshness = current_time - pd.Timestamp(ancestor["freshness"]['maxLoadedAt'])
              elif ancestor["resourceType"] == "ModelAppliedStateNestedNode":
                  ancestor_freshness = current_time - pd.Timestamp(ancestor["executionInfo"]["executeCompletedAt"])

if ancestor_freshness > max_freshness:
                  max_freshness = ancestor_freshness

G.add_node(model["uniqueId"], name=model["name"], type="model", max_ancestor_freshness = max_freshness, freshness = model_freshness, freshness_sla=freshness_sla)
    for _, source in sources_df.iterrows():
        if source["maxLoadedAt"] is not None:
          G.add_node(source["uniqueId"], name=source["name"], type="source", freshness=current_time - pd.Timestamp(source["maxLoadedAt"]))
    for _, model in models_df.iterrows():
        for parent in model["parents"]:
            G.add_edge(parent["uniqueId"], model["uniqueId"])

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      sources(
        first: $first
        filter: { freshnessChecked: true, database: "production" }
      ) {
        edges {
          node {
            sourceName
            name
            identifier
            loader
            freshness {
              freshnessJobDefinitionId
              freshnessRunId
              freshnessRunGeneratedAt
              freshnessStatus
              freshnessChecked
              maxLoadedAt
              maxLoadedAtTimeAgoInS
              snapshottedAt
              criteria {
                errorAfter {
                  count
                  period
                }
                warnAfter {
                  count
                  period
                }
              }
            }
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      tests(first: $first) {
        edges {
          node {
            name
            columnName
            parents {
              name
              resourceType
            }
            executionInfo {
              lastRunStatus
              lastRunError
              executeCompletedAt
              executionTime
            }
          }
        }
      }
    }
  }
}

query {
  environment(id: 123) {
    applied {
      models(first: 100, filter: { access: public }) {
        edges {
          node {
            name
            latestVersion
            contractEnforced
            constraints {
              name
              type
              expression
              columns
            }
            catalog {
              columns {
                name
                type
              }
            }
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(
        first: $first
        filter: {
          database: "analytics"
          schema: "prod"
          identifier: "customers"
        }
      ) {
        edges {
          node {
            name
            description
            tags
            meta
            catalog {
              columns {
                name
                description
                type
              }
            }
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first) {
        edges {
          node {
            name
            ancestors(types: [Model, Source, Seed, Snapshot]) {
              ... on ModelAppliedStateNestedNode {
                name
                resourceType
              }
              ... on SourceAppliedStateNestedNode {
                sourceName
                name
                resourceType
              }
            }
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    definition {
      metrics(first: $first) {
        edges {
          node {
            name
            description
            type
            formula
            filter
            tags
            parents {
              name
              resourceType
            }
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first, filter: { uniqueIds: ["MODEL.PROJECT.NAME"] }) {
        edges {
          node {
            name
            description
            resourceType
            access
            group
          }
        }
      }
    }
    definition {
      groups(first: $first) {
        edges {
          node {
            name
            resourceType
            models {
              name
            }
            ownerName
            ownerEmail
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    definition {
      models(first: $first) {
        edges {
          node {
            name
            access
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    definition {
      models(first: $first, filter: { access: public }) {
        edges {
          node {
            name
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      exposures(first: $first) {
        edges {
          node {
            name
            description
            ownerName
            url
            parents {
              name
              resourceType
              ... on ModelAppliedStateNestedNode {
                executionInfo {
                  executeCompletedAt
                  lastRunStatus
                }
              }
            }
          }
        }
      }
    }
  }
}

query (
  $environmentId: BigInt!
  $uniqueId: String!
  $lastRunCount: Int!
  $withCatalog: Boolean!
) {
  environment(id: $environmentId) {
    applied {
      modelHistoricalRuns(
        uniqueId: $uniqueId
        lastRunCount: $lastRunCount
        withCatalog: $withCatalog
      ) {
        name
        compiledCode
        columns {
          name
        }
        stats {
          label
          value
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      sources(
        first: $first
        filter: { uniqueIds: ["SOURCE_NAME.TABLE_NAME"] }
      ) {
        edges {
          node {
            loader
            children {
              uniqueId
              resourceType
              ... on ModelAppliedStateNestedNode {
                database
                schema
                alias
              }
            }
          }
        }
      }
    }
  }
}

models:
  jaffle_shop:
    marketing:
      +materialized: view
      paid_ads:
        google:
          +materialized: table

models:
  jaffle_shop:
    staging:
      +materialized: view

dbt run -s state:modified+ --defer --state path/to/prod/artifacts
dbt test -s state:modified+ --defer --state path/to/prod/artifacts

dbt run --select state:modified+ result:error+ --defer --state path/to/prod/artifacts

dbt build --select state:modified+ result:error+ --defer --state path/to/prod/artifacts

dbt build --select state:modified+ result:error+ result:fail+ --defer --state path/to/prod/artifacts

dbt test --select result:fail --exclude <example test> --defer --state path/to/prod/artifacts

**Examples:**

Example 1 (unknown):
```unknown
Graph example:

[![A lineage graph with source freshness information](/img/docs/dbt-cloud/discovery-api/lineage-graph-with-freshness-info.png?v=2 "A lineage graph with source freshness information")](#)A lineage graph with source freshness information

##### Are my data sources fresh?[​](#are-my-data-sources-fresh "Direct link to Are my data sources fresh?")

Checking [source freshness](https://docs.getdbt.com/docs/build/sources.md#source-data-freshness) allows you to ensure that sources loaded and used in your dbt project are compliant with expectations. The API provides the latest metadata about source loading and information about the freshness check criteria.

[![Source freshness page in dbt](/img/docs/dbt-cloud/discovery-api/source-freshness-page.png?v=2 "Source freshness page in dbt")](#)Source freshness page in dbt

Example query
```

Example 2 (unknown):
```unknown
##### What’s the test coverage and status?[​](#whats-the-test-coverage-and-status "Direct link to What’s the test coverage and status?")

[Data tests](https://docs.getdbt.com/docs/build/data-tests.md) are an important way to ensure that your stakeholders are reviewing high-quality data. You can execute tests during a dbt run. The Discovery API provides complete test results for a given environment or job, which it represents as the `children` of a given node that’s been tested (for example, a `model`).

Example query

For the following example, the `parents` are the nodes (code) that's being tested and `executionInfo` describes the latest test results:
```

Example 3 (unknown):
```unknown
##### How is this model contracted and versioned?[​](#how-is-this-model-contracted-and-versioned "Direct link to How is this model contracted and versioned?")

To enforce the shape of a model's definition, you can define contracts on models and their columns. You can also specify model versions to keep track of discrete stages in its evolution and use the appropriate one.

Example query
```

Example 4 (unknown):
```unknown
#### Discovery[​](#discovery "Direct link to Discovery")

You can use the Discovery API to find and understand relevant datasets and semantic nodes with rich context and metadata. Below are example questions and queries you can run.

For discovery use cases, people typically query the latest applied or definition state, often in the downstream part of the DAG (for example, mart models or metrics), using the `environment` endpoint.

##### What does this dataset and its columns mean?[​](#what-does-this-dataset-and-its-columns-mean "Direct link to What does this dataset and its columns mean?")

Query the Discovery API to map a table/view in the data platform to the model in the dbt project; then, retrieve metadata about its meaning, including descriptive metadata from its YAML file and catalog information from its YAML file and the schema.

Example query
```

---

## optional

**URL:** llms-txt#optional

config.get('optional_config_name', default="the default")

---

## Perform whatever functionality is available, like convert to a pandas table.

**URL:** llms-txt#perform-whatever-functionality-is-available,-like-convert-to-a-pandas-table.

**Contents:**
  - JDBC API StarterEnterpriseEnterprise +
  - JDBC API [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Job object schema
  - Fetching data...
  - Fetching data...
  - Lineage object schema
  - Fetching data...
  - Fetching data...
  - Model Historical Runs object schema
  - Fetching data...

print(arrow_table.to_pandas())
"""
order_total  ordered_at
          3  2023-08-07
        112  2023-08-08
         12  2023-08-09
       5123  2023-08-10
"""

mutation {
  createQuery(
    environmentId: "123"
    metrics: [{name: "metric_name", alias: "metric_alias"}]
  ) {
    ...
  }
}

mutation {
  createQuery(
    environmentId: "123"
    metrics: [{name: "order_total"}]
    groupBy: [{name: "metric_time", grain: MONTH}] 
  ) {
    queryId
  }
}

mutation {
  createQuery(
    environmentId: "123"
    metrics: [{name: "food_order_amount"}, {name: "order_gross_profit"}]
    groupBy: [{name: "metric_time", grain: MONTH}, {name: "customer__customer_type"}]
  ) {
    queryId
  }
}

mutation {
  createQuery(
    environmentId: "123"
    groupBy: [{name: "customer__customer_type"}]
  ) {
    queryId
  }
}

mutation {
  createQuery(
    environmentId: "123"
    metrics:[{name: "order_total"}]
    groupBy:[{name: "customer__customer_type"}, {name: "metric_time", grain: month}]
    where:[{sql: "{{ Dimension('customer__customer_type') }} = 'new'"}, {sql:"{{ Dimension('metric_time').grain('month') }} > '2022-10-01'"}]
    ) {
     queryId
    }
}

semantic_model:
  name: my_model_source

defaults:
  agg_time_dimension: created_month
  measures:
    - name: measure_0
      agg: sum
    - name: measure_1
      agg: sum
      agg_time_dimension: order_year
  dimensions:
    - name: created_month
      type: time
      type_params:
        time_granularity: month
    - name: order_year
      type: time
      type_params:
        time_granularity: year

metrics:
  - name: metric_0
    description: A metric with a month grain.
    type: simple
    type_params:
      measure: measure_0
  - name: metric_1
    description: A metric with a year grain.
    type: simple
    type_params:
      measure: measure_1

{{Dimension('location__location_name', entity_path=['order_id'])}}
  
  {{ Dimension('salesforce_account_owner__region',['salesforce_account']) }}
  
mutation {
  createQuery(
    environmentId: "123"
    metrics: [{name: "order_total"}]
    groupBy: [{name: "metric_time", grain: MONTH}] 
    orderBy: [{metric: {name: "order_total"}}, {groupBy: {name: "metric_time", grain: MONTH}, descending:true}]
  ) {
    queryId
  }
}

mutation {
  createQuery(
    environmentId: "123"
    metrics: [{name:"food_order_amount"}, {name: "order_gross_profit"}]
    groupBy: [{name:"metric_time", grain: MONTH}, {name: "customer__customer_type"}]
    limit: 10 
  ) {
    queryId
  }
}

mutation {
  createQuery(
    environmentId: "123"
    savedQuery: "new_customer_orders"
  ) {
    queryId
  }
}

mutation {
  compileSql(
    environmentId: "123"
    metrics: [{name:"food_order_amount"} {name:"order_gross_profit"}]
    groupBy: [{name:"metric_time", grain: MONTH}, {name:"customer__customer_type"}]
  ) {
    sql
  }
}

{
  queryRecords(
    environmentId:123
  ) {
    items {
      queryId
      status
      startTime
      endTime
      connectionDetails
      sqlDialect
      connectionSchema
      error
      queryDetails {
        ... on SemanticLayerQueryDetails {
          params {
            type
            metrics {
              name
            }
            groupBy {
              name
              grain
            }
            limit
            where {
              sql
            }
            orderBy {
              groupBy {
                name
                grain
              }
              metric {
                name
              }
              descending
            }
            savedQuery
          }
        }
        ... on RawSqlQueryDetails {
          queryStr
          compiledSql
          numCols
          queryDescription
          queryTitle
        }
      }
    }
    totalItems
    pageNum
    pageSize
  }
}

jdbc:arrow-flight-sql://semantic-layer.cloud.getdbt.com:443?&environmentId=202339&token=AUTHENTICATION_TOKEN

select * from {{ 
	semantic_layer.metrics() 
}}

select * from {{ 
    semantic_layer.dimensions(metrics=['food_order_amount'])}}

select * from {{
    semantic_layer.queryable_granularities(metrics=['food_order_amount', 'order_gross_profit'])}}

select * from {{
    semantic_layer.metrics_for_dimensions(group_by=['customer__customer_type'])
}}

select NAME, QUERYABLE_GRANULARITIES from {{
    semantic_layer.dimensions(
        metrics=["order_total"]
    )
}}

select * from {{
    semantic_layer.measures(metrics=['orders'])
}}

select * from {{ semantic_layer.metrics(search='order') }}

-- Retrieves the 5th page with a page size of 10 metrics
select * from {{ semantic_layer.metrics(page_size=10, page_number=5) }}

-- Retrieves the 1st page with a page size of 10 metrics
select * from {{ semantic_layer.metrics(page_size=10) }}

-- Retrieves all metrics without pagination
select * from {{ semantic_layer.metrics() }}

select * from semantic_layer.saved_queries()

| NAME | DESCRIPTION | LABEL | METRICS | GROUP_BY | WHERE_FILTER |

select * from {{
    semantic_layer.query(metrics=[Metric("metric_name", alias="metric_alias")])
}}

select name, dimensions from {{ 
	semantic_layer.metrics() 
	}}
	WHERE name='food_order_amount'

select * from {{ 
	semantic_layer.dimensions(metrics=['food_order_amount', 'order_gross_profit'])
	}}

select * from {{
	semantic_layer.query(metrics=['food_order_amount','order_gross_profit'], 
	group_by=['metric_time'])
	}}

select * from {{
	semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'], 
	group_by=[Dimension('metric_time').grain('month')])
	}}

select * from {{
	semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'], 
	group_by=[Dimension('metric_time').grain('month'), 'customer__customer_type'])
	}}

select * from {{
    semantic_layer.query(group_by=['customer__customer_type'])
                  }}

select * from {{
    semantic_layer.query_with_all_group_bys(metrics =['revenue','orders','food_orders'],
    compile= True)
}}

semantic_model:
  name: my_model_source

defaults:
  agg_time_dimension: created_month
  measures:
    - name: measure_0
      agg: sum
    - name: measure_1
      agg: sum
      agg_time_dimension: order_year
  dimensions:
    - name: created_month
      type: time
      type_params:
        time_granularity: month
    - name: order_year
      type: time
      type_params:
        time_granularity: year

metrics:
  - name: metric_0
    description: A metric with a month grain.
    type: simple
    type_params:
      measure: measure_0
  - name: metric_1
    description: A metric with a year grain.
    type: simple
    type_params:
      measure: measure_1

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
group_by=[Dimension('metric_time').grain('month'),'customer__customer_type'],
where="{{ Dimension('metric_time').grain('month')  }} >= '2017-03-09' AND {{ Dimension('customer__customer_type' }} in ('new') AND {{ Entity('order_id') }} = 10")
}}

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
group_by=[Dimension('metric_time').grain('month'),'customer__customer_type'],
where=["{{ Dimension('metric_time').grain('month') }} >= '2017-03-09'", "{{ Dimension('customer__customer_type') }} in ('new')", "{{ Entity('order_id') }} = 10"])
}}

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
  group_by=[Dimension('metric_time')],
  limit=10)
  }}

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
  group_by=[Dimension('metric_time')],
  limit=10,
  order_by=['order_gross_profit'])
  }}

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
  group_by=[Dimension('metric_time')],
  limit=10,
  order_by=['-order_gross_profit'])
  }}

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
  group_by=[Dimension('metric_time').grain('week')],
  limit=10,
  order_by=[Metric('order_gross_profit').descending(True), Dimension('metric_time').grain('week').descending(True) ])
  }}

select * from {{
semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
  group_by=[Dimension('metric_time').grain('week')],
  limit=10,
  order_by=[Metric('order_gross_profit'), Dimension('metric_time').grain('week')])
  }}

select * from {{
  semantic_layer.query(metrics=['food_order_amount', 'order_gross_profit'],
      group_by=[Dimension('metric_time').grain('month'),'customer__customer_type'],
      compile=True)
      }}
  
  select * from {{ semantic_layer.query(saved_query="new_customer_orders", limit=5, compile=True}}
  
select * from {{ semantic_layer.query(saved_query="new_customer_orders", limit=5}}

select * from {{
    semantic_layer.query(metrics=[Metric("revenue", alias="metric_alias")])
}}

select * from {{
    semantic_layer.query(metrics=[Metric("order_total", alias="total_revenue_global")], group_by=['metric_time'])
}}

| METRIC_TIME   | TOTAL_REVENUE_GLOBAL |
|:-------------:|:------------------:  |
| 2023-12-01    |              1500.75 |
| 2023-12-02    |              1725.50 |
| 2023-12-03    |              1850.00 |

semantic_layer.query(metrics=[Metric("revenue", alias="banana")], where="{{ Metric('revenue') }} > 0")

{{Dimension('location__location_name', entity_path=['order_id'])}}
  
  {{ Dimension('salesforce_account_owner__region',['salesforce_account']) }}
  
query JobQueryExample {
  # Provide runId for looking at specific run, otherwise it defaults to latest run
  job(id: 940) {
    # Get all models from this job's latest run
    models(schema: "analytics") {
      uniqueId
      executionTime
    }

# Or query a single node
    source(uniqueId: "source.jaffle_shop.snowplow.event") {
      uniqueId
      sourceName
      name
      state
      maxLoadedAt
      criteria {
        warnAfter {
          period
          count
        }
        errorAfter {
          period
          count
        }
      }
      maxLoadedAtTimeAgoInS
    }
  }
}

query {
  environment(id: 834) {
    applied {
      lineage(
        filter: {"types": ["Model"]} # Return results for the Model type
      ) {
        name
        resourceType
        filePath
        projectId
        materializationType
        parentIds
        tags
        uniqueId
      }
    }
  }
}

query {
  environment(id: 834) {
    applied {
      modelHistoricalRuns(
        uniqueId: "model.marketing.customers" # Use this format for unique ID: RESOURCE_TYPE.PACKAGE_NAME.RESOURCE_NAME
        lastRunCount: 20
      ) {
        runId # Get historical results for a particular model
        runGeneratedAt
        executionTime # View build time across runs
        status
        tests {
          name
          status
          executeCompletedAt
        } # View test results across runs
      }
    }
  }
}

{
  job(id: 123) {
    model(uniqueId: "model.jaffle_shop.dim_user") {
      parentsModels {
        runId
        uniqueId
        executionTime
      }
      parentsSources {
        runId
        uniqueId
        state
      }
    }
  }
}

{
  job(id: 123) {
    model(uniqueId: "model.jaffle_shop.dim_user") {
      runId
      projectId
      name
      uniqueId
      resourceType
      executeStartedAt
      executeCompletedAt
      executionTime
    }
  }
}

{
  job(id: 123) {
    model(uniqueId: "model.jaffle_shop.dim_user") {
      columns {
        name
        index
        type
        comment
        description
        tags
        meta
      }
    }
  }
}

query {
  environment(id: 834) {
    applied {
      models (first: 100) {
        edges {
          node {
            name
            description
            access
            accountId
            catalog {
              owner
            }
            config
            environmentId
            tests {
              name
              description
            }
          }
        }
      }
    }
  }
}

{
  job(id: 123) {
    models(database:"analytics", schema: "analytics", identifier:"dim_customers") {
      uniqueId
    }
  }
}

{
  job(id: 123) {
    models(schema: "analytics") {
      uniqueId
      executionTime
    }
  }
}

query {
  environment(id: 834) {
    applied {
      owners(resource: exposure) {
        email
        name
      }
    }
  }
}

query {
  environment(id: 834) {
    applied {
      packages(resource: "model")
    }
  }
}

query Compare($environmentId: Int!, $first: Int!) {
	environment(id: $environmentId) {
		definition {
			models(first: $first) {
				edges {
					node {
						name
						rawCode
					}
				}
			}
		}
		applied {
			models(first: $first) {
				edges {
					node {
						name
						rawCode 
						executionInfo {
							executeCompletedAt
						}
					}
				}
			}
		}
	}
}

pip install "dbt-sl-sdk[sync]"

pip install "dbt-sl-sdk[sync]"

from dbtsl import SemanticLayerClient

client = SemanticLayerClient(
    environment_id=123,
    auth_token="<your-semantic-layer-api-token>",
    host="semantic-layer.cloud.getdbt.com",
)

**Examples:**

Example 1 (unknown):
```unknown
##### Additional create query examples[​](#additional-create-query-examples "Direct link to Additional create query examples")

The following section provides query examples for the GraphQL API, such as how to query metrics, dimensions, where filters, and more:

* [Query metric alias](#query-metric-alias) — Query with metric alias, which allows you to use simpler or more intuitive names for metrics instead of their full definitions.
* [Query with a time grain](#query-with-a-time-grain) — Fetch multiple metrics with a change in time dimension granularities.
* [Query multiple metrics and multiple dimensions](#query-multiple-metrics-and-multiple-dimensions) — Select common dimensions for multiple metrics.
* [Query a categorical dimension on its own](#query-a-categorical-dimension-on-its-own) — Group by a categorical dimension.
* [Query with a where filter](#query-with-a-where-filter) — Use the `where` parameter to filter on dimensions and entities using parameters.
* [Query with order](#query-with-order) — Query with `orderBy`, accepts basic string that's a Dimension, Metric, or Entity. Defaults to ascending order.
* [Query with limit](#query-with-limit) — Query using a `limit` clause.
* [Query saved queries](#query-saved-queries) — Query using a saved query using the `savedQuery` parameter for frequently used queries.
* [Query with just compiling SQL](#query-with-just-compiling-sql) — Query using a compile keyword using the `compileSql` mutation.
* [Query records](#query-records) — View all the queries made in your project.

###### Query metric alias[​](#query-metric-alias "Direct link to Query metric alias")
```

Example 2 (unknown):
```unknown
###### Query with a time grain[​](#query-with-a-time-grain "Direct link to Query with a time grain")
```

Example 3 (unknown):
```unknown
Note that when using granularity in the query, the output of a time dimension with a time grain applied to it always takes the form of a dimension name appended with a double underscore and the granularity level - `{time_dimension_name}__{DAY|WEEK|MONTH|QUARTER|YEAR}`. Even if no granularity is specified, it will also always have a granularity appended to it and will default to the lowest available (usually daily for most data sources). It is encouraged to specify a granularity when using time dimensions so that there won't be any unexpected results with the output data.

###### Query multiple metrics and multiple dimensions[​](#query-multiple-metrics-and-multiple-dimensions "Direct link to Query multiple metrics and multiple dimensions")
```

Example 4 (unknown):
```unknown
###### Query a categorical dimension on its own[​](#query-a-categorical-dimension-on-its-own "Direct link to Query a categorical dimension on its own")
```

---

## Get the latest run metadata for all models

**URL:** llms-txt#get-the-latest-run-metadata-for-all-models

models_latest_metadata = query_discovery_api(auth_token, query_one, variables_query_one)['environment']

---

## Run all models tagged "daily", except those that are tagged hourly

**URL:** llms-txt#run-all-models-tagged-"daily",-except-those-that-are-tagged-hourly

dbt run --select tag:daily --exclude tag:hourly

seeds:
  jaffle_shop:
    utm_mappings:
      +tags: marketing

seeds:
  jaffle_shop:
    utm_mappings:
      +tags:
        - marketing
        - hourly

saved-queries:
  jaffle_shop:
    customer_order_metrics:
      +tags: order_metrics

**Examples:**

Example 1 (unknown):
```unknown
##### Apply tags to seeds[​](#apply-tags-to-seeds "Direct link to Apply tags to seeds")

dbt\_project.yml
```

Example 2 (unknown):
```unknown
dbt\_project.yml
```

Example 3 (unknown):
```unknown
##### Apply tags to saved queries[​](#apply-tags-to-saved-queries "Direct link to Apply tags to saved queries")

This following example shows how to apply a tag to a saved query in the `dbt_project.yml` file. The saved query is then tagged with `order_metrics`.

dbt\_project.yml
```

Example 4 (unknown):
```unknown
Then run resources with a specific tag using the following commands:
```

---

## For the dbt Job URL https://YOUR_ACCESS_URL/#/accounts/16173/projects/36467/jobs/65767/

**URL:** llms-txt#for-the-dbt-job-url-https://your_access_url/#/accounts/16173/projects/36467/jobs/65767/

---

## Filter dataframe to only successful runs

**URL:** llms-txt#filter-dataframe-to-only-successful-runs

model_df = model_df[model_df['status'] == 'success']

---

## ignore individual .py files

**URL:** llms-txt#ignore-individual-.py-files

not-a-dbt-model.py
another-non-dbt-model.py

---

## These three selectors are equivalent

**URL:** llms-txt#these-three-selectors-are-equivalent

dbt run --select "package:snowplow"
dbt run --select "snowplow"
dbt run --select "snowplow.*"

**Examples:**

Example 1 (unknown):
```unknown
Use the `this` package to select nodes from the current project. From the example, running `dbt run --select "package:this"` from the `snowplow` project runs the exact same set of models as the other three selectors.

Since `this` always refers to the current project, using `package:this` ensures that you're only selecting models from the project you're working in.

##### path[​](#path "Direct link to path")

<!-- -->

<!-- -->

##### resource\_type[​](#resource_type "Direct link to resource_type")

<!-- -->

<!-- -->

##### result[​](#result "Direct link to result")

The `result` method is related to the [`state` method](https://docs.getdbt.com/reference/node-selection/methods.md#state) and can be used to select resources based on their result status from a prior run. Note that one of the dbt commands \[`run`, `test`, `build`, `seed`] must have been performed in order to create the result on which a result selector operates.

You can use `result` selectors in conjunction with the `+` operator.
```

---

## e.g. assert every public model has a description

**URL:** llms-txt#e.g.-assert-every-public-model-has-a-description

for node in manifest.nodes.values():
    if node.resource_type == "model" and node.access == "public":
        assert node.description != "", f"{node.name} is missing a description"

---

## Overall run summary

**URL:** llms-txt#overall-run-summary

step_summary_post = f"""
*<{run_data_results['href']}|{hook_data['runStatus']} for Run #{run_id} on Job \"{hook_data['jobName']}\">*

*Environment:* {hook_data['environmentName']} | *Trigger:* {hook_data['runReason']} | *Duration:* {run_data_results['duration_humanized']}

threaded_errors_post = ""

---

## Update the name to match the name of your default branch

**URL:** llms-txt#update-the-name-to-match-the-name-of-your-default-branch

on:
  push:
    branches:
      - 'main'

# the job calls the dbt API to run a job
  run_dbt_cloud_job:
    name: Run dbt Job
    runs-on: ubuntu-latest

# Set the environment variables needed for the run
    env:
      DBT_ACCOUNT_ID: 00000 # enter your account id
      DBT_PROJECT_ID: 00000 # enter your project id
      DBT_PR_JOB_ID:  00000 # enter your job id
      DBT_API_KEY: ${{ secrets.DBT_API_KEY }}
      DBT_URL: https://cloud.getdbt.com # enter a URL that matches your job
      DBT_JOB_CAUSE: 'GitHub Pipeline CI Job' 
      DBT_JOB_BRANCH: ${{ github.head_ref }} # Resolves to the head_ref or source branch of the pull request in a workflow run.

steps:
      - uses: "actions/checkout@v4"
      - uses: "actions/setup-python@v5"
        with:
          python-version: "3.9"
      - name: Run dbt job
        run: "python python/run_and_monitor_dbt_job.py"

variables:
  DBT_ACCOUNT_ID: 00000 # enter your account id
  DBT_PROJECT_ID: 00000 # enter your project id
  DBT_PR_JOB_ID:  00000 # enter your job id
  DBT_API_KEY: $DBT_API_KEY # secret variable in gitlab account
  DBT_URL: https://cloud.getdbt.com 
  DBT_JOB_CAUSE: 'GitLab Pipeline CI Job' 
  DBT_JOB_BRANCH: $CI_COMMIT_BRANCH

**Examples:**

Example 1 (unknown):
```unknown
For this job, we'll set it up using the `gitlab-ci.yml` file as in the prior step (see Step 1 of the linting setup for more info). The YAML file will look pretty similar to our earlier job, but there is a new section called `variables` that we’ll use to pass in the required variables to the Python script. Update this section to match your setup based on the comments in the file.

Please note that the `rules:` section now says to run **only** when there are pushes to a branch named `main`, such as a PR being merged. Have a look through [GitLab’s docs](https://docs.gitlab.com/ee/ci/yaml/#rules) on these filters for additional use cases.

* Only dbt job
* Lint and dbt job
```

---

## does not work

**URL:** llms-txt#does-not-work

**Contents:**
  - About exceptions namespace
  - About execute variable
  - About flags (global configs)

host: "www.{{ env_var('DBT_ENV_SECRET_HOST_DOMAIN') }}.com/{{ env_var('DBT_ENV_SECRET_HOST_PATH') }}"

-- {{ dbt_metadata_envs }}

$ DBT_ENV_CUSTOM_ENV_MY_FAVORITE_COLOR=indigo DBT_ENV_CUSTOM_ENV_MY_FAVORITE_NUMBER=6 dbt compile

-- {'MY_FAVORITE_COLOR': 'indigo', 'MY_FAVORITE_NUMBER': '6'}

{% if number < 0 or number > 100 %}
  {{ exceptions.raise_compiler_error("Invalid `number`. Got: " ~ number) }}
{% endif %}

{% if number < 0 or number > 100 %}
  {% do exceptions.warn("Invalid `number`. Got: " ~ number) %}
{% endif %}

1   {% set payment_method_query %}
2   select distinct
3   payment_method
4   from {{ ref('raw_payments') }}
5   order by 1
6   {% endset %}
7
8   {% set results = run_query(payment_method_query) %}
9
10  {# Return the first column #}
11  {% set payment_methods = results.columns[0].values() %}

Encountered an error:
Compilation Error in model order_payment_methods (models/order_payment_methods.sql)
  'None' has no attribute 'table'

{% set payment_method_query %}
select distinct
payment_method
from {{ ref('raw_payments') }}
order by 1
{% endset %}

{% set results = run_query(payment_method_query) %}
{% if execute %}
{# Return the first column #}
{% set payment_methods = results.columns[0].values() %}
{% else %}
{% set payment_methods = [] %}
{% endif %}

$ dbt run
15:42:01  Running with dbt=1.10.2
15:42:01  I'm running a query now.  <------ this one is misleading!!!! no query is actually being run
15:42:01  Found 1 model, 0 tests, 0 snapshots, 0 macros, 0 operations, 0 seed files, 0 sources, 0 exposures, 0 metrics
15:42:01
15:42:01  Concurrency: 8 threads (target='dev')
15:42:01
15:42:01  1 of 1 START table model analytics.my_model .................................. [RUN]
15:42:01  I'm running a query now
15:42:02  1 of 1 OK created table model analytics.my_model ............................. [OK in 0.36s]

{%- if load_relation(relation) is none -%}
    {{ log("Relation is missing: " ~ relation, True) }}
{% endif %}

{%- if execute and load_relation(relation) is none -%}
    {% do exceptions.warn("Relation is missing: " ~ relation) %}
    {{ log("Relation is missing: " ~ relation, info=True) }}
{%- endif -%}

**Examples:**

Example 1 (unknown):
```unknown
##### Custom metadata[​](#custom-metadata "Direct link to Custom metadata")

Any env var named with the prefix `DBT_ENV_CUSTOM_ENV_` will be included in two places, with its prefix-stripped name as the key:

* [dbt artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts.md#common-metadata): `metadata` -> `env`
* [events and structured logs](https://docs.getdbt.com/reference/events-logging.md#info-fields): `info` -> `extra`

A dictionary of these prefixed env vars will also be available in a `dbt_metadata_envs` context variable:
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
Compiles to:
```

Example 4 (unknown):
```unknown
##### dbt platform usage[​](#dbt-platform-usage "Direct link to dbt platform usage")

If you are using dbt, you must adhere to the naming conventions for environment variables. Environment variables in dbt must be prefixed with `DBT_` (including `DBT_ENV_CUSTOM_ENV_` or `DBT_ENV_SECRET`). Environment variables keys are uppercased and case sensitive. When referencing `{{env_var('DBT_KEY')}}` in your project's code, the key must match exactly the variable defined in dbt's UI.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### About exceptions namespace

The `exceptions` namespace can be used to raise warnings and errors in dbt userspace.

#### raise\_compiler\_error[​](#raise_compiler_error "Direct link to raise_compiler_error")

The `exceptions.raise_compiler_error` method will raise a compiler error with the provided message. This is typically only useful in macros or materializations when invalid arguments are provided by the calling model. Note that throwing an exception will cause a model to fail, so please use this variable with care!

**Example usage**:

exceptions.sql
```

---

## The profile dictionary, used to write out profiles.yml

**URL:** llms-txt#the-profile-dictionary,-used-to-write-out-profiles.yml

---

## dbt Developer Hub

**URL:** llms-txt#dbt-developer-hub

**Contents:**
- API Reference
  - About the Discovery API schema
  - About the Discovery API StarterEnterpriseEnterprise +
  - About the Discovery API [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Account-scoped personal access tokens
  - APIs overview StarterEnterpriseEnterprise +
  - APIs overview [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Applied object schema
  - Fetching data...
  - Authentication tokens

> End user documentation, guides and technical reference for dbt

### About the Discovery API schema

With the Discovery API, you can query the metadata in dbt to learn more about your dbt deployments and the data they generate. You can analyze the data to make improvements. If you are new to the API, refer to [About the Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) for an introduction. You might also find the [use cases and examples](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md) helpful.

The Discovery API *schema* provides all the pieces necessary to query and interact with the Discovery API. The most common queries use the `environment` endpoint:

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment.md)

###### [Environment schema](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment.md)

[Query and compare a model’s definition (intended) and its applied (actual) state.](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied.md)

###### [Applied schema](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied.md)

[Query the actual state of objects and metadata in the warehouse after a \`dbt run\` or \`dbt build\`.](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-definition.md)

###### [Definition schema](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-definition.md)

[Query intended state in project code and configuration defined in your dbt project.](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-definition.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied-modelHistoricalRuns.md)

###### [Model Historical Runs schema](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied-modelHistoricalRuns.md)

[Query information about a model's run history.](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied-modelHistoricalRuns.md)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### About the Discovery API StarterEnterpriseEnterprise +

### About the Discovery API [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

Every time dbt runs a project, it generates and stores information about the project. The metadata includes details about your project’s models, sources, and other nodes along with their execution results. With the dbt Discovery API, you can query this comprehensive information to gain a better understanding of your DAG and the data it produces.

By leveraging the metadata in dbt, you can create systems for data monitoring and alerting, lineage exploration, and automated reporting. This can help you improve data discovery, data quality, and pipeline operations within your organization.

You can access the Discovery API through [ad hoc queries](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-querying.md), custom applications, a wide range of [partner ecosystem integrations](https://www.getdbt.com/product/integrations/) (like BI/analytics, catalog and governance, and quality and observability), and by using dbt features like [model timing](https://docs.getdbt.com/docs/deploy/run-visibility.md#model-timing) and [data health tiles](https://docs.getdbt.com/docs/explore/data-tile.md).

[![A rich ecosystem for integration ](/img/docs/dbt-cloud/discovery-api/discovery-api-figure.png?v=2 "A rich ecosystem for integration ")](#)A rich ecosystem for integration

You can query the dbt metadata:

* At the [environment](https://docs.getdbt.com/docs/environments-in-dbt.md) level for both the latest state (use the `environment` endpoint) and historical run results (use `modelHistoricalRuns`) of a dbt project in production.
* At the job level for results on a specific dbt job run for a given resource type, like `models` or `test`.

#### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* dbt [multi-tenant](https://docs.getdbt.com/docs/cloud/about-cloud/tenancy.md#multi-tenant) or [single tenant](https://docs.getdbt.com/docs/cloud/about-cloud/tenancy.md#single-tenant) account
* You must be on an [Enterprise or Enterprise+ plan](https://www.getdbt.com/pricing/)
* Your projects must be on a dbt [release tracks](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md) or dbt version 1.0 or later. Refer to [Upgrade dbt version in Cloud](https://docs.getdbt.com/docs/dbt-versions/upgrade-dbt-version-in-cloud.md) to upgrade.

#### What you can use the Discovery API for[​](#what-you-can-use-the-discovery-api-for "Direct link to What you can use the Discovery API for")

Click the following tabs to learn more about the API's use cases, the analysis you can do, and the results you can achieve by integrating with it.

To use the API directly or integrate your tool with it, refer to [Uses case and examples](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md) for detailed information.

* Performance
* Quality
* Discovery
* Governance
* Development

Use the API to look at historical information like model build time to determine the health of your dbt projects. Finding inefficiencies in orchestration configurations can help decrease infrastructure costs and improve timeliness. To learn more about how to do this, refer to [Performance](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md#performance).

You can use, for example, the [model timing](https://docs.getdbt.com/docs/deploy/run-visibility.md#model-timing) tab to help identify and optimize bottlenecks in model builds:

[![Model timing visualization in dbt](/img/docs/dbt-cloud/discovery-api/model-timing.png?v=2 "Model timing visualization in dbt")](#)Model timing visualization in dbt

Use the API to determine if the data is accurate and up-to-date by monitoring test failures, source freshness, and run status. Accurate and reliable information is valuable for analytics, decisions, and monitoring to help prevent your organization from making bad decisions. To learn more about this, refer to [Quality](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md#quality).

When used with [webhooks](https://docs.getdbt.com/docs/deploy/webhooks.md), it can also help with detecting, investigating, and alerting issues.

Use the API to find and understand dbt assets in integrated tools using information like model and metric definitions, and column information. For more details, refer to [Discovery](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md#discovery).

Data producers must manage and organize data for stakeholders, while data consumers need to quickly and confidently analyze data on a large scale to make informed decisions that improve business outcomes and reduce organizational overhead. The API is useful for discovery data experiences in catalogs, analytics, apps, and machine learning (ML) tools. It can help you understand the origin and meaning of datasets for your analysis.

[![Data lineage produced by dbt](/img/docs/collaborate/dbt-explorer/example-model-details.png?v=2 "Data lineage produced by dbt")](#)Data lineage produced by dbt

Use the API to review who developed the models and who uses them to help establish standard practices for better governance. For more details, refer to [Governance](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md#governance).

Use the API to review dataset changes and uses by examining exposures, lineage, and dependencies. From the investigation, you can learn how to define and build more effective dbt projects. For more details, refer to [Development](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md#development).

[![Use exposures to embed data health tiles in your dashboards to distill trust signals for data consumers.](/img/docs/collaborate/dbt-explorer/data-tile-pass.jpg?v=2 "Use exposures to embed data health tiles in your dashboards to distill trust signals for data consumers.")](#)Use exposures to embed data health tiles in your dashboards to distill trust signals for data consumers.

#### Types of project state[​](#types-of-project-state "Direct link to Types of project state")

You can query these two types of [project state](https://docs.getdbt.com/docs/dbt-cloud-apis/project-state.md) at the environment level:

* **Definition** — The logical state of a dbt project’s [resources](https://docs.getdbt.com/docs/build/projects.md) that update when the project is changed.
* **Applied** — The output of successful dbt DAG execution that creates or describes the state of the database (for example: `dbt run`, `dbt test`, source freshness, and so on)

These states allow you to easily examine the difference between a model’s definition and its applied state so you can get answers to questions like, did the model run? or did the run fail? Applied models exist as a table/view in the data platform given their most recent successful run.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Use cases and examples for the Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md)
* [Query the Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-querying.md)
* [Schema](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-job.md)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Account-scoped personal access tokens

User API tokens have been deprecated and will no longer work. [Migrate](#migrate-deprecated-user-api-keys-to-personal-access-tokens) to personal access tokens to resume services.

Each dbt user with a [Developer license](https://docs.getdbt.com/docs/cloud/manage-access/seats-and-users.md) can create a new personal access token (PAT) to access the dbt API and dbt CLI. This token can execute queries against the dbt API on the user's behalf. To access dbt APIs and resources on behalf of the *account*, we recommend using service tokens instead. Learn more about [which token type you should use](https://docs.getdbt.com/docs/dbt-cloud-apis/authentication.md#which-token-type-should-you-use) to understand the token differences.

PATs inherit the permissions of the user that created them. For example, if a developer-licensed user with Project Admin role access to specific projects creates a PAT, the token will get the Project Admin role with access to the same projects as the user. These tokens are also account-specific, so if a user has access to more than one dbt account with the same email address, they need to create a unique PAT for each one of these accounts.

#### Create a personal access token[​](#create-a-personal-access-token "Direct link to Create a personal access token")

Creating an account-scoped PAT requires only a few steps.

1. Navigate to your **Account Settings**, expand **API tokens** and click **Personal tokens**.

2. Click **Create personal access token**.

3. Give the token a descriptive name and click **Save**.

4. Copy the token before closing the window. *It will not be available after, and you will have to create a new token if you lose it.*

To maintain best security practices, it's recommended that you regularly rotate your PATs. To do so, create a new token and delete the old one once it's in place.

#### Delete a personal access token[​](#delete-a-personal-access-token "Direct link to Delete a personal access token")

To permanently delete a PAT:

1. Navigate to your **Account Settings**, expand **API tokens** and click **Personal tokens**.
2. Find the token you want to delete and click "X" to the right of the token description fields.
3. **Confirm delete** and the token will no longer be valid.

#### Migrate deprecated user API keys to personal access tokens[​](#migrate-deprecated-user-api-keys-to-personal-access-tokens "Direct link to Migrate deprecated user API keys to personal access tokens")

The migration to PATs is critical if you are using user API keys today. The current API key is located under **Personal Settings → API Key**.

There are a few things to understand if you are using a user API key today:

* PATs are more secure.
  <!-- -->
  * To promote the least privilege and high-security assurance for your dbt accounts, we highly recommend moving to the new account-scoped PATs.

* You must create and use unique tokens in each one of your dbt accounts that share the same email address.

* For example, if <paul.atreides@example.com> belongs to two dbt accounts: Spice Harvesting Account and Guild Navigator Account. Before this release, the same API key was used to access both of these accounts.
  * After this release, Paul has to individually go into these accounts and create a unique PAT for each account he wants to access the API for. These PATs are account-specific and not user specific.

* Cross-Account API endpoints will change in behavior when using PATs.

* These are namely /v2/accounts and /v3/accounts. Since all PATs are now account specific, getting all accounts associated with a username cannot work. /v3/accounts will only return account metadata that’s relevant to the PAT that’s being used.
  * User account metadata will only contain information about the specific account under which the request is being made.
  * Any other accounts that belong to that user account will need to be requested through the PAT that belongs to that account.

If you’re using any undocumented and unsupported API endpoints, please note that these can be deprecated without any notice. If you are using any undocumented endpoints and have use-cases that are not satisfied by the current API, please reach out to <support@getdbt.com>.

##### Using the personal access tokens[​](#using-the-personal-access-tokens "Direct link to Using the personal access tokens")

Are you using a user API key today to access dbt APIs in any of your workflows? If not, you don’t have any action to take. If you are using a user API key, please follow the instructions below.

1. Make a list of all the places where you’re making a call to the dbt API using the dbt user API key.

2. Create a new PAT under **Account Settings → API Tokens → Personal Tokens.** For instructions, see [Create a personal access token](#create-a-personal-access-token).

3. Replace the API key in your APIs with the PAT you created. You can use a PAT wherever you previously used an API key.

To replace the API key with a PAT, include the PAT in the Authorization header of your API requests. For example: `Authorization: Bearer <your-token>`.

Make sure to replace `<your-token>` with the new PAT you created.

The option to rotate API keys is used for existing API keys, not for replacing them with PATs. You do not need to replace your API key with a PAT in the dbt UI.

4. Ensure that you’re using a PAT only where it's needed. For flows that require a service account, please use a service token.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### APIs overview StarterEnterpriseEnterprise +

### APIs overview [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

Accounts on the Enterprise and Enterprise+ plans can query the dbt APIs.

dbt provides the following APIs:

* The [dbt Administrative API](https://docs.getdbt.com/docs/dbt-cloud-apis/admin-cloud-api.md) can be used to administrate a dbt account. It can be called manually or with [the dbt Terraform provider](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest).
* The [dbt Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) can be used to fetch metadata related to the state and health of your dbt project.
* The [Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) provides multiple API options which allow you to query your metrics defined in the Semantic Layer.

If you want to learn more about webhooks, refer to [Webhooks for your jobs](https://docs.getdbt.com/docs/deploy/webhooks.md).

#### How to Access the APIs[​](#how-to-access-the-apis "Direct link to How to Access the APIs")

dbt supports two types of API Tokens: [personal access tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md) and [service account tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md). Requests to the dbt APIs can be authorized using these tokens.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Applied object schema

The applied object allows you to query information about a particular model based on `environmentId`.

The [Example queries](#example-queries) illustrate a few fields you can query with this `environment` object. Refer to [Fields](#fields) to view the entire schema, which provides all possible fields you can query.

##### Example queries[​](#example-queries "Direct link to Example queries")

You can use your production environment's `id`:

##### Fields[​](#fields "Direct link to Fields")

When querying the `applied` field of `environment`, you can use the following fields.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Authentication tokens

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md)

###### [Personal access tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md)

[Learn about user tokens and how to use them to execute queries against the dbt API.](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md)

###### [Service account tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md)

[Learn how to use service account tokens to securely authenticate with dbt APIs for system-level integrations.](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md)

#### Types of API access tokens[​](#types-of-api-access-tokens "Direct link to Types of API access tokens")

**Personal access tokens:** Preferred and secure way of accessing dbt APIs on behalf of a user. PATs are scoped to an account and can be enhanced with more granularity and control.

**Service tokens:** Service tokens are similar to service accounts and are the preferred method to enable access on behalf of the dbt account.

##### Which token type should you use[​](#which-token-type-should-you-use "Direct link to Which token type should you use")

You should use service tokens broadly for any production workflow where you need a service account. You should use PATs only for developmental workflows *or* dbt client workflows that require user context. The following examples show you when to use a personal access token (PAT) or a service token:

* **Connecting a partner integration to dbt** — Some examples include the [Semantic Layer Google Sheets integration](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md), Hightouch, Datafold, a custom app you’ve created, etc. These types of integrations should use a service token instead of a PAT because service tokens give you visibility, and you can scope them to only what the integration needs and ensure the least privilege. We highly recommend switching to a service token if you’re using a personal access token for these integrations today.
* **Production Terraform** — Use a service token since this is a production workflow and is acting as a service account and not a user account.
* **Cloud CLI** — Use a PAT since the Cloud CLI works within the context of a user (the user is making the requests and has to operate within the context of their user account).
* **Testing a custom script and staging Terraform or Postman** — We recommend using a PAT as this is a developmental workflow and is scoped to the user making the changes. When you push this script or Terraform into production, use a service token instead.
* **API endpoints requiring user context** — Use PATs to authenticate to any API endpoint that requires user context (for example, endpoints to create and update user credentials).

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### dbt Administrative API StarterEnterpriseEnterprise +

### dbt Administrative API [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

The dbt Administrative API is enabled by default for [Enterprise and Enterprise+ plans](https://www.getdbt.com/pricing/). It can be used to:

* Download artifacts after a job has completed
* Kick off a job run from an orchestration tool
* Manage your dbt account
* and more

dbt currently supports two versions of the Administrative API: v2 and v3. In general, v3 is the recommended version to use, but we don't yet have all our v2 routes upgraded to v3. We're currently working on this. If you can't find something in our v3 docs, check out the shorter list of v2 endpoints because you might find it there.

Many endpoints of the Administrative API can also be called through the [dbt Terraform provider](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest). The built-in documentation on the Terraform registry contains [a guide on how to get started with the provider](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest/docs/guides/1_getting_started) as well as [a page showing all the Terraform resources available](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest/docs/guides/99_list_resources) to configure.

[![](/img/icons/pencil-paper.svg)](https://docs.getdbt.com/dbt-cloud/api-v2)

###### [API v2](https://docs.getdbt.com/dbt-cloud/api-v2)

[Our legacy API version, with limited endpoints and features. Contains information not available in v3.](https://docs.getdbt.com/dbt-cloud/api-v2)

[![](/img/icons/pencil-paper.svg)](https://docs.getdbt.com/dbt-cloud/api-v3)

###### [API v3](https://docs.getdbt.com/dbt-cloud/api-v3)

[Our latest API version, with new endpoints and features.](https://docs.getdbt.com/dbt-cloud/api-v3)

[![](/img/icons/pencil-paper.svg)](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest)

###### [dbt Terraform provider](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest)

[The Terraform provider maintained by dbt Labs which can be used to manage a dbt account.](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest)

[](https://registry.terraform.io/providers/dbt-labs/dbtcloud/latest)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Definition object schema

The definition object allows you to query the logical state of a given project node given its most recent manifest generated models.

The [Example queries](#example-queries) illustrate a few fields you can query with this `definition` object. Refer to [Fields](#fields) to view the entire schema, which provides all possible fields you can query.

##### Example queries[​](#example-queries "Direct link to Example queries")

You can use your production environment's `id`:

##### Fields[​](#fields "Direct link to Fields")

When querying the `definition` field of `environment`, you can use the following fields.

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Environment object schema

You can use the environment object to query and compare definition (intended) and applied (actual) states for nodes (models, seeds, snapshots, models, and more) in your dbt project. For example, you specify an `environmentId` to learn more about a particular model (or other node type) in that environment.

The [Example queries](#example-queries) illustrate a few fields you can query with this `environment` object. Refer to [Fields](#fields) to view the entire schema, which provides all possible fields you can query.

##### Arguments[​](#arguments "Direct link to Arguments")

When querying for `environment`, you can use the following arguments.

##### Example queries[​](#example-queries "Direct link to Example queries")

You can use your production environment's `id`:

With the deprecation of the data type `Int` for `id`, below is an example of replacing it with `BigInt`:

With the deprecation of `modelByEnvironment`, below is an example of replacing it with `environment`:

##### Fields[​](#fields "Direct link to Fields")

When querying an `environment`, you can use the following fields.

For details on querying the `applied` field of `environment`, you can visit: [Applied](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-applied.md)

For details querying the `definition` field of `environment`, you can visit: [Definition](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-environment-definition.md)

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Exposure object schema

The exposure object allows you to query information about a particular exposure. To learn more, refer to [Add Exposures to your DAG](https://docs.getdbt.com/docs/build/exposures.md).

##### Arguments[​](#arguments "Direct link to Arguments")

When querying for an `exposure`, the following arguments are available.

Below we show some illustrative example queries and outline the schema of the exposure object.

##### Example query[​](#example-query "Direct link to Example query")

The example below queries information about an exposure including the owner's name and email, the URL, and information about parent sources and parent models.

##### Fields[​](#fields "Direct link to Fields")

When querying for an `exposure`, the following fields are available:

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Exposure Tile object schema

[Exposure health tiles](https://docs.getdbt.com/docs/explore/data-tile.md) distill data health signals for data consumers and can be embedded in downstream tools. You can query information on these tiles from the Discovery API.

The [Example query](#example-query) illustrates a few fields you can query with the `exposureTile` object. Refer to [Fields](#fields) to view the entire schema, which provides all possible fields you can query.

##### Arguments[​](#arguments "Direct link to Arguments")

When querying for `exposureTile`, you can use the following arguments:

##### Example query[​](#example-query "Direct link to Example query")

You can specify the `environmentId` and filter by a model's `uniqueId` to understand the data quality and metadata information for the exposure tile associated with the `customers` model in the `marketing` package:

##### Fields[​](#fields "Direct link to Fields")

When querying for `exposureTile`, you can use the following fields:

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Exposures object schema

[Exposures](https://docs.getdbt.com/docs/build/exposures.md) are dbt resources that represent downstream uses of your project, such as dashboards, applications, or data science pipelines. You can query exposures through the Discovery API to understand which assets depend on your models.

The [Example query](#example-query) illustrates a few fields you can query with the `exposures` object. Refer to [Fields](#fields) to view the entire schema, which provides all possible fields you can query.

##### Arguments[​](#arguments "Direct link to Arguments")

When querying for `exposures`, you can use the following arguments:

##### Example query[​](#example-query "Direct link to Example query")

You can specify the `environmentId`, `first: 100`, and filter by model `uniqueIds` to return all the downstream exposures (dashboards, applications, etc.) that depend on the `customers` model in the `marketing` package, limited to the first 100 results:

##### Fields[​](#fields "Direct link to Fields")

When querying for `exposures`, you can use the following fields:

##### Key fields from nodes[​](#key-fields-from-nodes "Direct link to Key fields from nodes")

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### Exposures object schema

The exposures object allows you to query information about all exposures in a given job. To learn more, refer to [Add Exposures to your DAG](https://docs.getdbt.com/docs/build/exposures.md).

##### Arguments[​](#arguments "Direct link to Arguments")

When querying for `exposures`, the following arguments are available.

Below we show some illustrative example queries and outline the schema of the exposures object.

##### Example query[​](#example-query "Direct link to Example query")

The example below queries information about all exposures in a given job including the owner's name and email, the URL, and information about parent sources and parent models for each exposure.

##### Fields[​](#fields "Direct link to Fields")

When querying for `exposures`, the following fields are available:

#### Was this page helpful?

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.

### GraphQL StarterEnterpriseEnterprise +

### GraphQL [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

[GraphQL](https://graphql.org/) (GQL) is an open-source query language for APIs. It offers a more efficient and flexible approach compared to traditional RESTful APIs.

With GraphQL, users can request specific data using a single query, reducing the need for many server round trips. This improves performance and minimizes network overhead.

GraphQL has several advantages, such as self-documenting, having a strong typing system, supporting versioning and evolution, enabling rapid development, and having a robust ecosystem. These features make GraphQL a powerful choice for APIs prioritizing flexibility, performance, and developer productivity.

#### dbt Semantic Layer GraphQL API[​](#dbt-semantic-layer-graphql-api "Direct link to dbt Semantic Layer GraphQL API")

The Semantic Layer GraphQL API allows you to explore and query metrics and dimensions. Due to its self-documenting nature, you can explore the calls conveniently through a schema explorer.

The schema explorer URLs vary depending on your [deployment region](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses.md). Use the following table to find the right link for your region:

| Deployment type            | Schema explorer URL                                                                                                                                                                                                   |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| North America multi-tenant | <https://semantic-layer.cloud.getdbt.com/api/graphql>                                                                                                                                                                 |
| EMEA multi-tenant          | <https://semantic-layer.emea.dbt.com/api/graphql>                                                                                                                                                                     |
| APAC multi-tenant          | <https://semantic-layer.au.dbt.com/api/graphql>                                                                                                                                                                       |
| Single tenant              | `https://semantic-layer.YOUR_ACCESS_URL/api/graphql`<br /><br />Replace `YOUR_ACCESS_URL` with your specific account prefix followed by the appropriate Access URL for your region and plan.                          |
| Multi-cell                 | `https://YOUR_ACCOUNT_PREFIX.semantic-layer.REGION.dbt.com/api/graphql`<br /><br />Replace `YOUR_ACCOUNT_PREFIX` with your specific account identifier and `REGION` with your location, which could be `us1.dbt.com`. |

* If your Single tenant access URL is `ABC123.getdbt.com`, your schema explorer URL will be `https://semantic-layer.ABC123.getdbt.com/api/graphql`.

dbt Partners can use the Semantic Layer GraphQL API to build an integration with the Semantic Layer.

Note that the Semantic Layer GraphQL API doesn't support `ref` to call dbt objects. Instead, use the complete qualified table name. If you're using dbt macros at query time to calculate your metrics, you should move those calculations into your Semantic Layer metric definitions as code.

#### Requirements to use the GraphQL API[​](#requirements-to-use-the-graphql-api "Direct link to Requirements to use the GraphQL API")

* A dbt project on dbt v1.6 or higher
* Metrics are defined and configured
* A dbt [service token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md) with "Semantic Layer Only” and "Metadata Only" permissions or a [personal access token](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md)

#### Using the GraphQL API[​](#using-the-graphql-api "Direct link to Using the GraphQL API")

If you're a dbt user or partner with access to dbt and the [Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md), you can [set up](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md) and test this API with data from your own instance by configuring the Semantic Layer and obtaining the right GQL connection parameters described in this document.

Refer to [Get started with the Semantic Layer](https://docs.getdbt.com/guides/sl-snowflake-qs.md) for more info.

Authentication uses either a dbt [service account token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md) or a [personal access token](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md) passed through a header as follows. To explore the schema, you can enter this information in the "header" section.

Each GQL request also requires a dbt `environmentId`. The API uses both the service or personal token in the header and `environmentId` for authentication.

##### Metadata calls[​](#metadata-calls "Direct link to Metadata calls")

###### Fetch data platform dialect[​](#fetch-data-platform-dialect "Direct link to Fetch data platform dialect")

In some cases in your application, it may be useful to know the dialect or data platform that's internally used for the Semantic Layer connection (such as if you are building `where` filters from a user interface rather than user-inputted SQL).

The GraphQL API has an easy way to fetch this with the following query:

###### Fetch available metrics[​](#fetch-available-metrics "Direct link to Fetch available metrics")

###### Fetch available dimensions for metrics[​](#fetch-available-dimensions-for-metrics "Direct link to Fetch available dimensions for metrics")

###### Fetch available granularities given metrics[​](#fetch-available-granularities-given-metrics "Direct link to Fetch available granularities given metrics")

Note: This call for `queryableGranularities` returns only queryable granularities for metric time - the primary time dimension across all metrics selected.

You can also get queryable granularities for all other dimensions using the `dimensions` call:

You can also optionally access it from the metrics endpoint:

###### Fetch measures[​](#fetch-measures "Direct link to Fetch measures")

`aggTimeDimension` tells you the name of the dimension that maps to `metric_time` for a given measure. You can also query `measures` from the `metrics` endpoint, which allows you to see what dimensions map to `metric_time` for a given metric:

###### Fetch entities[​](#fetch-entities "Direct link to Fetch entities")

###### Fetch entities and dimensions to group metrics[​](#fetch-entities-and-dimensions-to-group-metrics "Direct link to Fetch entities and dimensions to group metrics")

###### Metric types[​](#metric-types "Direct link to Metric types")

###### Metric type parameters[​](#metric-type-parameters "Direct link to Metric type parameters")

###### Dimension types[​](#dimension-types "Direct link to Dimension types")

###### List saved queries[​](#list-saved-queries "Direct link to List saved queries")

List all saved queries for the specified environment:

###### List a saved query[​](#list-a-saved-query "Direct link to List a saved query")

List a single saved query using environment ID and query name:

##### Querying[​](#querying "Direct link to Querying")

When querying for data, *either* a `groupBy` *or* a `metrics` selection is required. The following section provides examples of how to query metrics:

* [Create query](#create-metric-query)
* [Fetch query result](#fetch-query-result)

###### Create query[​](#create-query "Direct link to Create query")

###### Fetch query result[​](#fetch-query-result "Direct link to Fetch query result")

The GraphQL API uses a polling process for querying since queries can be long-running in some cases. It works by first creating a query with a mutation, \`createQuery, which returns a query ID. This ID is then used to continuously check (poll) for the results and status of your query. The typical flow would look as follows:

3. Keep querying 2. at an appropriate interval until status is `FAILED` or `SUCCESSFUL`

##### Output format and pagination[​](#output-format-and-pagination "Direct link to Output format and pagination")

###### Output format[​](#output-format "Direct link to Output format")

By default, the output is in Arrow format. You can switch to JSON format using the following parameter. However, due to performance limitations, we recommend using the JSON parameter for testing and validation. The JSON received is a base64 encoded string. To access it, you can decode it using a base64 decoder. The JSON is created from pandas, which means you can change it back to a dataframe using `pandas.read_json(json, orient="table")`. Or you can work with the data directly using `json["data"]`, and find the table schema using `json["schema"]["fields"]`. Alternatively, you can pass `encoded:false` to the jsonResult field to get a raw JSON string directly.

The results default to the table but you can change it to any [pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html) supported value.

###### Pagination[​](#pagination "Direct link to Pagination")

By default, we return 1024 rows per page. If your result set exceeds this, you need to increase the page number using the `pageNum` option.

##### Run a Python query[​](#run-a-python-query "Direct link to Run a Python query")

The `arrowResult` in the GraphQL query response is a byte dump, which isn't visually useful. You can convert this byte data into an Arrow table using any Arrow-supported language. Refer to the following Python example explaining how to query and decode the arrow result:

```
import base64
import pyarrow as pa
import time

headers = {"Authorization":"Bearer <token>"}
query_result_request = """
{
  query(environmentId: 70, queryId: "12345678") {
    sql
    status
    error
    arrowResult
  }
}
"""

while True:
  gql_response = requests.post(
    "https://semantic-layer.cloud.getdbt.com/api/graphql",
    json={"query": query_result_request},
    headers=headers,
  )
  if gql_response.json()["data"]["status"] in ["FAILED", "SUCCESSFUL"]:
    break
  # Set an appropriate interval between polling requests
  time.sleep(1)

"""
gql_response.json() => 
{
  "data": {
    "query": {
      "sql": "SELECT\n  ordered_at AS metric_time__day\n  , SUM(order_total) AS order_total\nFROM semantic_layer.orders orders_src_1\nGROUP BY\n  ordered_at",
      "status": "SUCCESSFUL",
      "error": null,
      "arrowResult": "arrow-byte-data"
    }
  }
}
"""

def to_arrow_table(byte_string: str) -> pa.Table:
  """Get a raw base64 string and convert to an Arrow Table."""
  with pa.ipc.open_stream(base64.b64decode(byte_string)) as reader:
    return pa.Table.from_batches(reader, reader.schema)

arrow_table = to_arrow_table(gql_response.json()["data"]["query"]["arrowResult"])

**Examples:**

Example 1 (unknown):
```unknown
query Example {
	environment(id: 834){ # Get the latest state of the production environment
		applied { # The state of an executed node as it exists as an object in the database
			models(first: 100){ # Pagination to ensure manageable response for large projects
				edges { node {
					uniqueId, name, description, rawCode, compiledCode, # Basic properties
					database, schema, alias, # Table/view identifier (can also filter by)
					executionInfo {executeCompletedAt, executionTime}, # Metadata from when the model was built
					tests {name, executionInfo{lastRunStatus, lastRunError}}, # Latest test results
					catalog {columns {name, description, type}, stats {label, value}}, # Catalog info
					ancestors(types:[Source]) {name, ...on SourceAppliedStateNestedNode {freshness{maxLoadedAt, freshnessStatus}}}, # Source freshness }
					children {name, resourceType}}} # Immediate dependencies in lineage
				totalCount } # Number of models in the project
		}
	}
}
```

Example 2 (unknown):
```unknown
query Example {
	environment(id: 834){ # Get the latest state of the production environment
		definition { # The logical state of a given project node given its most recent manifest generated
			models(first: 100, filter:{access:public}){ # Filter on model access (or other properties)
				edges { node {
					rawCode, # Compare to see if/how the model has changed since the last build
					jobDefinitionId, runGeneratedAt,	# When the code was last compiled or run
					contractEnforced, group, version}}} # Model governance
		}
	}
}
```

Example 3 (unknown):
```unknown
query Example {
	environment(id: 834){ # Get the latest state of the production environment
		applied { # The state of an executed node as it exists as an object in the database
			models(first: 100){ # Pagination to ensure manageable response for large projects
				edges { node {
					uniqueId, name, description, rawCode, compiledCode, # Basic properties
					database, schema, alias, # Table/view identifier (can also filter by)
					executionInfo {executeCompletedAt, executionTime}, # Metadata from when the model was built
					tests {name, executionInfo{lastRunStatus, lastRunError}}, # Latest test results
					catalog {columns {name, description, type}, stats {label, value}}, # Catalog info
					ancestors(types:[Source]) {name, ...on SourceAppliedStateNode {freshness{maxLoadedAt, freshnessStatus}}}, # Source freshness }
					children {name, resourceType}}} # Immediate dependencies in lineage
				totalCount } # Number of models in the project
		}
		definition { # The logical state of a given project node given its most recent manifest generated
			models(first: 100, filter:{access:public}){ # Filter on model access (or other properties)
				edges { node {
					rawCode, # Compare to see if/how the model has changed since the last build
					jobDefinitionId, runGeneratedAt,	# When the code was last compiled or run
					contractEnforced, group, version}}} # Model governance
		}
	}
```

Example 4 (unknown):
```unknown
query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first) {
        edges {
          node {
            uniqueId
            executionInfo {
              lastRunId
            }
          }
        }
      }
    }
  }
}
```

---

## These are documented on the dbt API docs

**URL:** llms-txt#these-are-documented-on-the-dbt-api-docs

**Contents:**
  - Use Jinja to improve your SQL code
  - Using BigQuery DataFrames with dbt Python models
- Navigation Options
  - navigation-options
- Platform
  - About Canvas EnterpriseEnterprise +
  - About Canvas [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - About cost management Private previewEnterpriseEnterprise +
  - About cost management [Private preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - About dbt Copilot StarterEnterpriseEnterprise +

class DbtJobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30

def _trigger_job() -> int:
    res = requests.post(
        url=f"https://{base_url}/api/v2/accounts/{account_id}/jobs/{job_id}/run/",
        headers={'Authorization': f"Token {api_key}"},
        json={
            # Optionally pass a description that can be viewed within the <Constant name="cloud" /> API.
            # See the API docs for additional parameters that can be passed in,
            # including `schema_override` 
            'cause': f"Triggered by Databricks Workflows.",
        }
    )

try:
        res.raise_for_status()
    except:
        print(f"API token (last four): ...{api_key[-4:]}")
        raise

response_payload = res.json()
    return response_payload['data']['id']

def _get_job_run_status(job_run_id):
    res = requests.get(
        url=f"https://{base_url}/api/v2/accounts/{account_id}/runs/{job_run_id}/",
        headers={'Authorization': f"Token {api_key}"},
    )

res.raise_for_status()
    response_payload = res.json()
    return response_payload['data']['status']

def run():
    job_run_id = _trigger_job()
    print(f"job_run_id = {job_run_id}")   
    while True:
        time.sleep(5)
        status = _get_job_run_status(job_run_id)
        print(DbtJobRunStatus(status))
        if status == DbtJobRunStatus.SUCCESS:
            break
        elif status == DbtJobRunStatus.ERROR or status == DbtJobRunStatus.CANCELLED:
            raise Exception("Failure!")

if __name__ == '__main__':
    run()

job_run_id = 123456
DbtJobRunStatus.QUEUED
DbtJobRunStatus.QUEUED
DbtJobRunStatus.QUEUED
DbtJobRunStatus.STARTING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.RUNNING
DbtJobRunStatus.SUCCESS

select
order_id,
sum(case when payment_method = 'bank_transfer' then amount end) as bank_transfer_amount,
sum(case when payment_method = 'credit_card' then amount end) as credit_card_amount,
sum(case when payment_method = 'gift_card' then amount end) as gift_card_amount,
sum(amount) as total_amount
from {{ ref('raw_payments') }}
group by 1

select
order_id,
{% for payment_method in ["bank_transfer", "credit_card", "gift_card"] %}
sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount,
{% endfor %}
sum(amount) as total_amount
from {{ ref('raw_payments') }}
group by 1

{% set payment_methods = ["bank_transfer", "credit_card", "gift_card"] %}

select
order_id,
{% for payment_method in payment_methods %}
sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount,
{% endfor %}
sum(amount) as total_amount
from {{ ref('raw_payments') }}
group by 1

{% set payment_methods = ["bank_transfer", "credit_card", "gift_card"] %}

select
order_id,
{% for payment_method in payment_methods %}
sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount
{% if not loop.last %},{% endif %}
{% endfor %}
from {{ ref('raw_payments') }}
group by 1

sum(case when payment_method = 'bank_transfer' then amount end) as bank_transfer_amount
,

sum(case when payment_method = 'credit_card' then amount end) as credit_card_amount
,

sum(case when payment_method = 'gift_card' then amount end) as gift_card_amount

from raw_jaffle_shop.payments
group by 1

{%- set payment_methods = ["bank_transfer", "credit_card", "gift_card"] -%}

select
order_id,
{%- for payment_method in payment_methods %}
sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount
{%- if not loop.last %},{% endif -%}
{% endfor %}
from {{ ref('raw_payments') }}
group by 1

{% macro get_payment_methods() %}
{{ return(["bank_transfer", "credit_card", "gift_card"]) }}
{% endmacro %}

{%- set payment_methods = get_payment_methods() -%}

select
order_id,
{%- for payment_method in payment_methods %}
sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount
{%- if not loop.last %},{% endif -%}
{% endfor %}
from {{ ref('raw_payments') }}
group by 1

select distinct
payment_method
from {{ ref('raw_payments') }}
order by 1

{% macro get_payment_methods() %}

{% set payment_methods_query %}
select distinct
payment_method
from {{ ref('raw_payments') }}
order by 1
{% endset %}

{% set results = run_query(payment_methods_query) %}

{{ log(results, info=True) }}

| column         | data_type |
| -------------- | --------- |
| payment_method | Text      |

{% macro get_payment_methods() %}

{% set payment_methods_query %}
select distinct
payment_method
from {{ ref('raw_payments') }}
order by 1
{% endset %}

{% set results = run_query(payment_methods_query) %}

{% if execute %}
{# Return the first column #}
{% set results_list = results.columns[0].values() %}
{% else %}
{% set results_list = [] %}
{% endif %}

{{ return(results_list) }}

{% macro get_column_values(column_name, relation) %}

{% set relation_query %}
select distinct
{{ column_name }}
from {{ relation }}
order by 1
{% endset %}

{% set results = run_query(relation_query) %}

{% if execute %}
{# Return the first column #}
{% set results_list = results.columns[0].values() %}
{% else %}
{% set results_list = [] %}
{% endif %}

{{ return(results_list) }}

{% macro get_payment_methods() %}

{{ return(get_column_values('payment_method', ref('raw_payments'))) }}

{%- set payment_methods = dbt_utils.get_column_values(
    table=ref('raw_payments'),
    column='payment_method'
) -%}

select
order_id,
{%- for payment_method in payment_methods %}
sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount
{%- if not loop.last %},{% endif -%}
{% endfor %}
from {{ ref('raw_payments') }}
group by 1

#Create Service Account
   gcloud iam service-accounts create dbt-bigframes-sa
   #Grant BigQuery User Role
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/bigquery.user
   #Grant BigQuery Data Editor role. This can be restricted at dataset level
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/bigquery.dataEditor
   #Grant Service Account user 
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/iam.serviceAccountUser
   #Grant Colab Entperprise User
   gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/aiplatform.colabEnterpriseUser
   
   #Create BQ dataset 
   bq mk --location=${REGION} echo "${GOOGLE_CLOUD_PROJECT}" | tr '-' '_'_dataset
   
   #Create GCS bucket
   gcloud storage buckets create gs://${GOOGLE_CLOUD_PROJECT}-bucket --location=${REGION}
   #Grant Storage Admin over the bucket to your SA

gcloud storage buckets add-iam-policy-binding gs://${GOOGLE_CLOUD_PROJECT}-bucket --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/storage.admin
   
      select 
      1 as foo,
      2 as bar
   
   def model(dbt, session):
      dbt.config(submission_method="bigframes")
      bdf = dbt.ref("my_sql_model") #loading from prev step
      return bdf
   
   models:
   my_dbt_project:
      submission_method: bigframes
      python_models:
         +materialized: view
   
   def model(dbt, session):
      dbt.config(submission_method="bigframes")
      # rest of the python code...

CREATE USER dbt_cost_user
  PASSWORD = 'A_SECURE_PASSWORD'
  DEFAULT_ROLE = dbt_cost_management
  MUST_CHANGE_PASSWORD = FALSE;

CREATE ROLE dbt_cost_management;

GRANT ROLE dbt_cost_management TO USER dbt_cost_user;

GRANT USAGE ON DATABASE SNOWFLAKE TO ROLE dbt_cost_management;
GRANT USAGE ON SCHEMA SNOWFLAKE.ACCOUNT_USAGE TO ROLE dbt_cost_management;
GRANT USAGE ON WAREHOUSE YOUR_WAREHOUSE TO ROLE dbt_cost_management;
ALTER USER dbt_cost_user SET DEFAULT_WAREHOUSE = 'YOUR_WAREHOUSE';

GRANT SELECT ON VIEW SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY TO ROLE dbt_cost_management;
GRANT SELECT ON VIEW SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY TO ROLE dbt_cost_management;
GRANT SELECT ON VIEW SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY TO ROLE dbt_cost_management;
GRANT SELECT ON VIEW SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY TO ROLE dbt_cost_management;

GRANT USAGE ON SCHEMA SNOWFLAKE.ORGANIZATION_USAGE TO ROLE dbt_cost_management;
GRANT SELECT ON VIEW SNOWFLAKE.ORGANIZATION_USAGE.USAGE_IN_CURRENCY_DAILY TO ROLE dbt_cost_management;

CREATE USER dbt_cost_user
  PASSWORD = 'A_SECURE_PASSWORD'
  DEFAULT_ROLE = dbt_cost_management
  MUST_CHANGE_PASSWORD = FALSE;

CREATE ROLE dbt_cost_management;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE dbt_cost_management;
GRANT ROLE dbt_cost_management TO USER dbt_cost_user;

dbt sl query --metrics revenue --group-by metric_time
  
  dbt sl query --metrics revenue --group-by metric_time,user__country
  
  dbt sl query --metrics revenue,gross_sales --group-by metric_time,user__country
  
  dbt sl query --metrics revenue --group-by metric_time --compile
  
  dbt sl query --metrics revenue,gross_sales --group-by metric_time --compile
  
    selectors:
      - name: skip_views_but_test_views
        description: >
          A default selector that will exclude materializing views
          without skipping tests on views.
        default: true
        definition:
          union:
            - union: 
              - method: path
                value: "*"
              - exclude: 
                - method: config.materialized
                  value: view
            - method: resource_type
              value: test
   
   version: "1"
   context:
     active-project: "<project id from the list below>"
     active-host: "<active host from the list>"
     defer-env-id: "<optional defer environment id>"
   projects:
     - project-name: "<project-name>"
       project-id: "<project-id>"
       account-name: "<account-name>"
       account-id: "<account-id>"
       account-host: "<account-host>" # for example, "cloud.getdbt.com"
       token-name: "<pat-name>"
       token-value: "<pat-value>"

- project-name: "<project-name>"
       project-id: "<project-id>"
       account-name: "<account-name>"
       account-id: "<account-id>"
       account-host: "<account-host>" # for example, "cloud.getdbt.com"
       token-name: "<pat-name>"
       token-value: "<pat-value>"  
   
   cd ~/dbt-projects/jaffle_shop
   
   # dbt_project.yml
   name:
   version:
   # Your project configs...

dbt-cloud: 
       project-id: PROJECT_ID
   
dbt sqlfluff lint [PATHS]... [flags]

**Examples:**

Example 1 (unknown):
```unknown
3. Replace **`<YOUR_SECRET_SCOPE>`** and **`<YOUR_SECRET_KEY>`** with the values you used [previously](#set-up-a-databricks-secret-scope)

4. Replace **`<YOUR_BASE_URL>`** and **`<YOUR_ACCOUNT_ID>`** with the correct values of your environment and [Access URL](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses.md) for your region and plan.

   * To find these values, navigate to dbt, select **Deploy -> Jobs**. Select the Job you want to run and copy the URL. For example: `https://YOUR_ACCESS_URL/deploy/000000/projects/111111/jobs/222222` and therefore valid code would be:

Your URL is structured `https://<YOUR_BASE_URL>/deploy/<YOUR_ACCOUNT_ID>/projects/<YOUR_PROJECT_ID>/jobs/<YOUR_JOB_ID>` account\_id = 000000 job\_id = 222222 base\_url = "cloud.getdbt.com"

5. Run the Notebook. It will fail, but you should see **a `job_id` widget** at the top of your notebook.

6. In the widget, **enter your `job_id`** from step 4.

7. **Run the Notebook again** to trigger the dbt job. Your results should look similar to the following:
```

Example 2 (unknown):
```unknown
You can cancel the job from dbt if necessary.

#### Configure the workflows to run the dbt jobs[​](#configure-the-workflows-to-run-the-dbt-jobs "Direct link to Configure the workflows to run the dbt jobs")

You can set up workflows directly from the notebook OR by adding this notebook to one of your existing workflows:

* Create a workflow from existing Notebook
* Add the Notebook to existing workflow

1. Click **Schedule** on the upper right side of the page
2. Click **Add a schedule**
3. Configure Job name, Schedule, Cluster
4. Add a new parameter called: `job_id` and fill in your job ID. Refer to [step 4 in previous section](#create-a-databricks-python-notebook) to find your job ID.
5. Click **Create**
6. Click **Run Now** to test the job

1) Open Existing **Workflow**
2) Click **Tasks**
3) Press **“+” icon** to add a new task
4) Enter the **following**:

| Field      | Value                         |
| ---------- | ----------------------------- |
| Task name  | `<unique_task_name>`          |
| Type       | Notebook                      |
| Source     | Workspace                     |
| Path       | `</path/to/notebook>`         |
| Cluster    | `<your_compute_cluster>`      |
| Parameters | `job_id`: `<your_dbt_job_id>` |

5. Select **Save Task**
6. Click **Run Now** to test the workflow

Multiple Workflow tasks can be set up using the same notebook by configuring the `job_id` parameter to point to different dbt jobs.

Using Databricks workflows to access the dbt job API can improve integration of your data pipeline processes and enable scheduling of more complex workflows.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Use Jinja to improve your SQL code

[Back to guides](https://docs.getdbt.com/guides.md)

Jinja

dbt Core

Advanced

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

In this guide, we're going to take a common pattern used in SQL, and then use Jinja to improve our code.

If you'd like to work through this query, add [this CSV](https://github.com/dbt-labs/jaffle_shop/blob/core-v1.0.0/seeds/raw_payments.csv) to the `seeds/` folder of your dbt project, and then execute `dbt seed`.

While working through the steps of this model, we recommend that you have your compiled SQL open as well, to check what your Jinja compiles to. To do this:

* **Using dbt:** Click the compile button to see the compiled SQL in the right hand pane
* **Using dbt Core:** Run `dbt compile` from the command line. Then open the compiled SQL file in the `target/compiled/{project name}/` directory. Use a split screen in your code editor to keep both files open at once.

#### Write the SQL without Jinja[​](#write-the-sql-without-jinja "Direct link to Write the SQL without Jinja")

Consider a data model in which an `order` can have many `payments`. Each `payment` may have a `payment_method` of `bank_transfer`, `credit_card` or `gift_card`, and therefore each `order` can have multiple `payment_methods`

From an analytics perspective, it's important to know how much of each `order` was paid for with each `payment_method`. In your dbt project, you can create a model, named `order_payment_method_amounts`, with the following SQL:

models/order\_payment\_method\_amounts.sql
```

Example 3 (unknown):
```unknown
The SQL for each payment method amount is repetitive, which can be difficult to maintain for a number of reasons:

* If the logic or field name were to change, the code would need to be updated in three places.
* Often this code is created by copying and pasting, which may lead to mistakes.
* Other analysts that review the code are less likely to notice errors as it's common to only scan through repeated code.

So we're going to use Jinja to help us clean it up, or to make our code more "DRY" ("Don't Repeat Yourself").

#### Use a for loop in models for repeated SQL[​](#use-a-for-loop-in-models-for-repeated-sql "Direct link to Use a for loop in models for repeated SQL")

Here, the repeated code can be replaced with a `for` loop. The following will be compiled to the same query, but is significantly easier to maintain.

/models/order\_payment\_method\_amounts.sql
```

Example 4 (unknown):
```unknown
#### Set variables at the top of a model[​](#set-variables-at-the-top-of-a-model "Direct link to Set variables at the top of a model")

We recommend setting variables at the top of a model, as it helps with readability, and enables you to reference the list in multiple places if required. This is a practice we've borrowed from many other programming languages.

/models/order\_payment\_method\_amounts.sql
```

---

## seed

**URL:** llms-txt#seed

dbt seed --exclude "account_parent_mappings"    # load all seeds except account_parent_mappings

---

## Cumulative metrics aggregate a measure over a given window. The window is considered infinite if no window parameter is passed (accumulate the measure over all of time)

**URL:** llms-txt#cumulative-metrics-aggregate-a-measure-over-a-given-window.-the-window-is-considered-infinite-if-no-window-parameter-is-passed-(accumulate-the-measure-over-all-of-time)

**Contents:**
  - Cumulative metrics
  - Custom aliases
  - Custom databases
  - Custom schemas

metrics:
  - name: wau_rolling_7
    type: cumulative
    label: Weekly active users
    type_params:
      measure:
        name: active_users
        fill_nulls_with: 0
        join_to_timespine: true
      cumulative_type_params:
        window: 7 days

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

metrics:
  - name: cancellation_rate
    type: ratio
    label: Cancellation rate
    type_params:
      numerator: cancellations
      denominator: transaction_amount
    filter: |   
      {{ Dimension('customer__country') }} = 'MX'
  - name: enterprise_cancellation_rate
    type: ratio
    type_params:
      numerator:
        name: cancellations
        filter: {{ Dimension('company__tier') }} = 'enterprise'  
      denominator: transaction_amount
    filter: | 
      {{ Dimension('customer__country') }} = 'MX'

metrics:
  - name: cancellations
    description: The number of cancellations
    type: simple
    label: Cancellations
    type_params:
      measure:
        name: cancellations_usd  # Specify the measure you are creating a proxy for.
        fill_nulls_with: 0
        join_to_timespine: true
    filter: |
      {{ Dimension('order__value')}} > 100 and {{Dimension('user__acquisition')}} is not null

filter: | 
  {{ Entity('entity_name') }}

filter: |  
  {{ Dimension('primary_entity__dimension_name') }}

filter: |  
  {{ TimeDimension('time_dimension', 'granularity') }}

filter: |  
 {{ Metric('metric_name', group_by=['entity_name']) }}

filter: |  
  {{ TimeDimension('order_date', 'month') }}

type_params:
    measure: revenue
  
  type_params:
    measure:
      name: order_total
      fill_nulls_with: 0
      join_to_timespine: true
  
measures:
  - name: customers
    expr: customer_id
    agg: count_distinct

measures:
  - name: revenue
    description: Total revenue
    agg: sum
    expr: revenue
  - name: subscription_count
    description: Count of active subscriptions
    agg: sum
    expr: event_type
metrics:
  - name: current_revenue
    description: Current revenue
    label: Current Revenue
    type: cumulative
    type_params:
      measure: revenue
  - name: active_subscriptions
    description: Count of active subscriptions
    label: Active Subscriptions
    type: cumulative
    type_params:
      measure: subscription_count

measures:
      - name: order_total
        agg: sum

select
  count(distinct distinct_users) as weekly_active_users,
  metric_time
from (
  select
    subq_3.distinct_users as distinct_users,
    subq_3.metric_time as metric_time
  from (
    select
      subq_2.distinct_users as distinct_users,
      subq_1.metric_time as metric_time
    from (
      select
        metric_time
      from transform_prod_schema.mf_time_spine subq_1356
      where (
        metric_time >= cast('2000-01-01' as timestamp)
      ) and (
        metric_time <= cast('2040-12-31' as timestamp)
      )
    ) subq_1
    inner join (
      select
        distinct_users as distinct_users,
        date_trunc('day', ds) as metric_time
      from demo_schema.transactions transactions_src_426
      where (
        (date_trunc('day', ds)) >= cast('1999-12-26' as timestamp)
      ) AND (
        (date_trunc('day', ds)) <= cast('2040-12-31' as timestamp)
      )
    ) subq_2
    on
      (
        subq_2.metric_time <= subq_1.metric_time
      ) and (
        subq_2.metric_time > dateadd(day, -7, subq_1.metric_time)
      )
  ) subq_3
)
group by
  metric_time,
limit 100;

select
  count(distinct subq_3.distinct_users) as weekly_active_users,
  subq_3.metric_time
from (
  select
    subq_2.distinct_users as distinct_users,
    subq_1.metric_time as metric_time
group by
  subq_3.metric_time

-- This model will be created in the database with the identifier `sessions`
-- Note that in this example, `alias` is used along with a custom schema
{{ config(alias='sessions', schema='google_analytics') }}

models:
  - name: ga_sessions
    config:
      alias: sessions

-- Use the model's filename in ref's, regardless of any aliasing configs

select * from {{ ref('ga_sessions') }}
union all
select * from {{ ref('snowplow_sessions') }}

{% macro generate_alias_name(custom_alias_name=none, node=none) -%}

{%- if custom_alias_name -%}

{{ custom_alias_name | trim }}

{%- elif node.version -%}

{{ return(node.name ~ "_v" ~ (node.version | replace(".", "_"))) }}

{{ config(alias='sessions') }}

$ dbt compile
Encountered an error:
Compilation Error
  dbt found two resources with the database representation "analytics.sessions".
  dbt cannot create two resources with identical database representations. To fix this,
  change the "schema" or "alias" configuration of one of these resources:
  - model.my_project.snowplow_sessions (models/snowplow_sessions.sql)
  - model.my_project.sessions (models/sessions.sql)

models:
  jaffle_shop:
    +database: jaffle_shop

# For BigQuery users:
    # project: jaffle_shop

{{ config(database="jaffle_shop") }}

{% macro generate_database_name(custom_database_name=none, node=none) -%}

{%- set default_database = target.database -%}
    {%- if custom_database_name is none -%}

{{ default_database }}

{{ custom_database_name | trim }}

{{ config(schema='marketing') }}

**Examples:**

Example 1 (unknown):
```unknown
#### Derived metrics[​](#derived-metrics "Direct link to Derived metrics")

[Derived metrics](https://docs.getdbt.com/docs/build/derived.md) are defined as an expression of other metrics. Derived metrics allow you to do calculations on top of metrics.

models/metrics/file\_name.yml
```

Example 2 (unknown):
```unknown
#### Ratio metrics[​](#ratio-metrics "Direct link to Ratio metrics")

[Ratio metrics](https://docs.getdbt.com/docs/build/ratio.md) involve a numerator metric and a denominator metric. A `filter` string can be applied to both the numerator and denominator or separately to the numerator or denominator.

models/metrics/file\_name.yml
```

Example 3 (unknown):
```unknown
#### Simple metrics[​](#simple-metrics "Direct link to Simple metrics")

[Simple metrics](https://docs.getdbt.com/docs/build/simple.md) point directly to a measure. You may think of it as a function that takes only one measure as the input.

* `name` — Use this parameter to define the reference name of the metric. The name must be unique amongst metrics and can include lowercase letters, numbers, and underscores. You can use this name to call the metric from the Semantic Layer API.

**Note:** If you've already defined the measure using the `create_metric: True` parameter, you don't need to create simple metrics. However, if you would like to include a constraint on top of the measure, you will need to create a simple type metric.

models/metrics/file\_name.yml
```

Example 4 (unknown):
```unknown
#### Filters[​](#filters "Direct link to Filters")

A filter is configured using Jinja templating. Use the following syntax to reference entities, dimensions, time dimensions, or metrics in filters.

Refer to [Metrics as dimensions](https://docs.getdbt.com/docs/build/ref-metrics-in-filters.md) for details on how to use metrics as dimensions with metric filters:

models/metrics/file\_name.yml
```

---

## Step-specific summaries

**URL:** llms-txt#step-specific-summaries

for step in run_data_results['run_steps']:
  if step['status_humanized'] == 'Success':
    step_summary_post += f"""
✅ {step['name']} ({step['status_humanized']} in {step['duration_humanized']})
"""
  else:
    step_summary_post += f"""
❌ {step['name']} ({step['status_humanized']} in {step['duration_humanized']})
"""

# Don't try to extract info from steps that don't have well-formed logs
    show_logs = not any(cmd in step['name'] for cmd in commands_to_skip_logs)
    if show_logs:
      full_log = step['logs']
      # Remove timestamp and any colour tags
      full_log = re.sub('\x1b?\[[0-9]+m[0-9:]*', '', full_log)
    
      summary_start = re.search('(?:Completed with \d+ error.* and \d+ warnings?:|Database Error|Compilation Error|Runtime Error)', full_log)
    
      line_items = re.findall('(^.*(?:Failure|Error) in .*\n.*\n.*)', full_log, re.MULTILINE)

if not summary_start:
        continue
      
      threaded_errors_post += f"""
*{step['name']}*
"""    
      # If there are no line items, the failure wasn't related to dbt nodes, and we want the whole rest of the message. 
      # If there are, then we just want the summary line and then to log out each individual node's error.
      if len(line_items) == 0:
        relevant_log = f''
      else:
        relevant_log = summary_start[0]
        for item in line_items:
          relevant_log += f'\n\n'
      threaded_errors_post += f"""
{relevant_log}
"""

send_error_thread = len(threaded_errors_post) > 0

---

## Run tests on all snapshots, which use the 'snapshot' materialization

**URL:** llms-txt#run-tests-on-all-snapshots,-which-use-the-'snapshot'-materialization

**Contents:**
  - test-paths
  - type
  - unique_key
  - Unit test overrides
  - Unit testing versioned SQL models

dbt test --select "config.materialized:snapshot"

models:
  - name: orders
    columns:
      - name: order_id
        config:
          tags: [my_column_tag] # changed to config in v1.10 and backported to 1.9
        data_tests:
          - unique

dbt test --select "tag:my_column_tag"

models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique:
            config:
              tags: [my_test_tag] # changed to config in v1.10

dbt test --select "tag:my_test_tag"

test-paths: [directorypath]

test-paths: ["test"]
    
    test-paths: ["/Users/username/project/test"]
    
test-paths: ["custom_tests"]

functions:
  - name: <function name>
    type: scalar | aggregate | table  # aggregate and table coming soon

functions:
  - name: is_positive_int
    description: Determines if a string represents a positive integer
    type: scalar
    arguments:
      - name: input_string
        data_type: STRING
    returns:
      data_type: BOOLEAN

functions:
  - name: double_total
    description: Sums values and doubles the result
    type: aggregate
    arguments:
      - name: values
        data_type: FLOAT
        description: A sequence of numbers to aggregate
    returns:
      data_type: FLOAT

{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

models:
  - name: my_incremental_model
    description: "An incremental model example with a unique key."
    config:
      materialized: incremental
      unique_key: id

models:
  jaffle_shop:
    staging:
      +unique_key: id

snapshots:
  <resource-path>:
    +unique_key: column_name_or_expression

{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

snapshots:
  <resource-path>:
    +unique_key: id

- name: test_my_model_overrides
    model: my_model
    given:
      - input: ref('my_model_a')
        rows:
          - {id: 1, a: 1}
      - input: ref('my_model_b')
        rows:
          - {id: 1, b: 2}
          - {id: 2, b: 2}
    overrides:
      macros:
        type_numeric: override
        invocation_id: 123
      vars:
        my_test: var_override
      env_vars:
        MY_TEST: env_var_override
    expect:
      rows:
        - {macro_call: override, var_call: var_override, env_var_call: env_var_override, invocation_id: 123}

unit_tests:
  - name: my_unit_test
    model: my_incremental_model
    overrides:
      macros:
        # unit test this model in "full refresh" mode
        is_incremental: false 
    ...

unit_tests:
  - name: my_other_unit_test
    model: my_model_that_uses_star
    overrides:
      macros:
        # explicity set star to relevant list of columns
        dbt_utils.star: col_a,col_b,col_c 
    ...

**Examples:**

Example 1 (unknown):
```unknown
Note that this functionality may change in future versions of dbt.

##### Run tests on tagged columns[​](#run-tests-on-tagged-columns "Direct link to Run tests on tagged columns")

Because the column `order_id` is tagged `my_column_tag`, the test itself also receives the tag `my_column_tag`. Because of that, this is an example of direct selection.

models/\<filename>.yml
```

Example 2 (unknown):
```unknown

```

Example 3 (unknown):
```unknown
Currently, tests "inherit" tags applied to columns, sources, and source tables. They do *not* inherit tags applied to models, seeds, or snapshots. In all likelihood, those tests would still be selected indirectly, because the tag selects its parent. This is a subtle distinction, and it may change in future versions of dbt.

##### Run tagged tests only[​](#run-tagged-tests-only "Direct link to Run tagged tests only")

This is an even clearer example of direct selection: the test itself is tagged `my_test_tag`, and selected accordingly.

models/\<filename>.yml
```

Example 4 (unknown):
```unknown

```

---

## run all seeds that generated errors on the prior invocation of dbt seed

**URL:** llms-txt#run-all-seeds-that-generated-errors-on-the-prior-invocation-of-dbt-seed

dbt seed --select "result:error" --state path/to/artifacts

# reruns all the models associated with failed tests from the prior invocation of dbt build
  dbt build --select "1+result:fail" --state path/to/artifacts

# reruns the models associated with failed tests and all downstream dependencies - especially useful in deferred state workflows
  dbt build --select "1+result:fail+" --state path/to/artifacts
  
dbt list --select "saved_query:*"                    # list all saved queries 
dbt list --select "+saved_query:orders_saved_query"  # list your saved query named "orders_saved_query" and all upstream resources

dbt list --select "semantic_model:*"        # list all semantic models 
dbt list --select "+semantic_model:orders"  # list your semantic model named "orders" and all upstream resources

dbt run --select "source:snowplow+"    # run all models that select from Snowplow sources

**Examples:**

Example 1 (unknown):
```unknown
* Only use `result:fail` when you want to re-run tests that failed during the last invocation. This selector is specific to test nodes. Tests don't have downstream nodes in the DAG, so using the `result:fail+` selector will only return the failed test itself and not the model or anything built on top of it.

* On the other hand, `result:error` selects any resource (models, tests, snapshots, and more) that returned an error.

* As an example, to re-run upstream and downstream resources associated with failed tests, you can use one of the following selectors:

  <!-- -->
```

Example 2 (unknown):
```unknown
##### saved\_query[​](#saved_query "Direct link to saved_query")

The `saved_query` method selects [saved queries](https://docs.getdbt.com/docs/build/saved-queries.md).
```

Example 3 (unknown):
```unknown
##### semantic\_model[​](#semantic_model "Direct link to semantic_model")

The `semantic_model` method selects [semantic models](https://docs.getdbt.com/docs/build/semantic-models.md).
```

Example 4 (unknown):
```unknown
##### source[​](#source "Direct link to source")

The `source` method is used to select models that select from a specified [source](https://docs.getdbt.com/docs/build/sources.md#using-sources). Use in conjunction with the `+` operator.
```

---

## Get the historical run metadata for the longest running model

**URL:** llms-txt#get-the-historical-run-metadata-for-the-longest-running-model

model_historical_metadata = query_discovery_api(auth_token, query_two, variables_query_two)['environment']['applied']['modelHistoricalRuns']

---

## set the datatype of the name column in the 'added' seed so it

**URL:** llms-txt#set-the-datatype-of-the-name-column-in-the-'added'-seed-so-it

---

## Extract graph nodes from response

**URL:** llms-txt#extract-graph-nodes-from-response

def extract_nodes(data):
    models = []
    sources = []
    groups = []
    for model_edge in data["applied"]["models"]["edges"]:
        models.append(model_edge["node"])
    for source_edge in data["applied"]["sources"]["edges"]:
        sources.append(source_edge["node"])
    for group_edge in data["definition"]["groups"]["edges"]:
        groups.append(group_edge["node"])
    models_df = pd.DataFrame(models)
    sources_df = pd.DataFrame(sources)
    groups_df = pd.DataFrame(groups)

return models_df, sources_df, groups_df

---

## ... initialize client

**URL:** llms-txt#...-initialize-client

**Contents:**
  - Query the Discovery API
  - Resources object schema
  - Fetching data...
  - Fetching data...
  - Fetching data...
  - Seed object schema
  - Fetching data...
  - Fetching data...
  - Seeds object schema
  - Fetching data...

curl 'YOUR_API_URL' \
    -H 'authorization: Bearer YOUR_TOKEN' \
    -H 'content-type: application/json'
    -X POST
    --data QUERY_BODY
  
response = requests.post(
    'YOUR_API_URL',
    headers={"authorization": "Bearer "+YOUR_TOKEN, "content-type": "application/json"},
    json={"query": QUERY_BODY, "variables": VARIABLES}
)

metadata = response.json()['data'][ENDPOINT]

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first, filter: { uniqueIds: "MODEL.PROJECT.MODEL_NAME" }) {
        edges {
          node {
            name
            ancestors(types: [Model, Source, Seed, Snapshot]) {
              ... on ModelAppliedStateNestedNode {
                name
                resourceType
                materializedType
                executionInfo {
                  executeCompletedAt
                }
              }
              ... on SourceAppliedStateNestedNode {
                sourceName
                name
                resourceType
                freshness {
                  maxLoadedAt
                }
              }
              ... on SnapshotAppliedStateNestedNode {
                name
                resourceType
                executionInfo {
                  executeCompletedAt
                }
              }
              ... on SeedAppliedStateNestedNode {
                name
                resourceType
                executionInfo {
                  executeCompletedAt
                }
              }
            }
          }
        }
      }
    }
  }
}

pageInfo {
  startCursor
  endCursor
  hasNextPage
}
totalCount # Total number of records across all pages

query ModelsAndTests($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first, filter: { lastRunStatus: error }) {
        edges {
          node {
            name
            executionInfo {
              lastRunId
            }
          }
        }
      }
      tests(first: $first, filter: { status: "fail" }) {
        edges {
          node {
            name
            executionInfo {
              lastRunId
            }
          }
        }
      }
    }
  }
}

query {
  environment(id: 834) {
    applied {
      resources(
        filter: {
          types: [
            Model
          ]
        }, 
        first: 100
      ) {
        edges {
          node {
            accountId
            description
            environmentId
            filePath
            meta
            name
            projectId
            resourceType
            uniqueId
            tags
          }
        }
      }
    }
  }
}

{
  job(id: 123) {
    seed(uniqueId: "seed.jaffle_shop.raw_customers") {
      database
      schema
      uniqueId
      name
      status
      error
    }
  }
}

query ($environmentId: BigInt!, $first: Int!, $filter: GenericMaterializedFilter) {
  environment(id: $environmentId) {
    applied {
      seeds(
        first: 100,
        filter: {
          database: "analytics"
        }
      ) {
        edges {
          node {
            description
            name
            filePath
            projectId
            fqn
            tags
            uniqueId
            resourceType
          }
        }
      }
    }
  }
}

{
  job(id: 123) {
    seeds {
      uniqueId
      name
      executionTime
      status
    }
  }
}

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

query {
  environment(id: 834) {
    applied {
      snapshots(
        filter: {
          database: "analytics"
        }, 
        first: 100
      ) {
        edges {
          node {
            executionInfo {
              compileCompletedAt
              compileStartedAt
              executeCompletedAt
              executeStartedAt
              executionTime
              lastRunStatus
              lastRunId
            }
            fqn
            name
          }
        }
      }
    }
  }
}

{
  job(id: 123) {
    snapshots {
      uniqueId
      name
      executionTime
      environmentId
      executeStartedAt
      executeCompletedAt
    }
  }
}

{
  job(id: 123) {
    source(uniqueId: "source.jaffle_shop.snowplow.event") {
      uniqueId
      sourceName
      name
      state
      maxLoadedAt
      criteria {
        warnAfter {
          period
          count
        }
        errorAfter {
          period
          count
        }
      }
      maxLoadedAtTimeAgoInS
    }
  }
}

query {
  environment(id: 834) {
    applied {
      sources(
        filter: {
          database: "analytics"
        }, 
        first: 100
      ) {
        edges {
          node {
            name
            fqn
            description
            filePath
            freshness {
              freshnessChecked
              freshnessStatus
            }
            sourceName
            sourceDescription
            tests {
              name
              description
              testType
              executionInfo {
                lastRunStatus
              }
            }
          }
        }
      }
    }
  }
}

{
  job(id: 123) {
    sources(
      database: "analytics"
      schema: "analytics"
      identifier: "dim_customers"
    ) {
      uniqueId
    }
  }
}

{
  job(id: 123) {
    sources(schema: "analytics") {
      uniqueId
      state
    }
  }
}

query {
  environment(id: 834) {
    applied {
      tags {
        name
      }
    }
  }
}

{
  job(id: 123) {
    test(uniqueId: "test.internal_analytics.not_null_metrics_id") {
      runId
      accountId
      projectId
      uniqueId
      name
      columnName
      state
    }
  }
}

query {
  environment(id: 834) {
    applied {
      tests(
        filter: {
          testTypes: [
            GENERIC_DATA_TEST,
            SINGULAR_DATA_TEST,
            UNIT_TEST
          ]
        }, 
        first: 100
      ) {
        edges {
          node {
            name
            model
            description
            expect
            resourceType
            testType
            given
          }
        }
      }
    }
  }
}

{
  job(id: 123) {
    tests {
      runId
      accountId
      projectId
      uniqueId
      name
      columnName
      state
    }
  }
}

query AppliedModels($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first) {
        edges {
          node {
            name
            uniqueId
            materializedType
            executionInfo {
              lastSuccessRunId
              executionTime
              executeStartedAt
            }
          }
        }
      }
    }
  }
}

query ModelHistoricalRuns(
  $environmentId: BigInt!
  $uniqueId: String
  $lastRunCount: Int
) {
  environment(id: $environmentId) {
    applied {
      modelHistoricalRuns(
        uniqueId: $uniqueId
        lastRunCount: $lastRunCount
      ) {
        name
        runId
        runElapsedTime
        runGeneratedAt
        executionTime
        executeStartedAt
        executeCompletedAt
        status
      }
    }
  }
}

**Examples:**

Example 1 (unknown):
```unknown
#### Contribute[​](#contribute "Direct link to Contribute")

To contribute to this project, check out our [contribution guidelines](https://github.com/dbt-labs/semantic-layer-sdk-python/blob/main/CONTRIBUTING.md) and open a GitHub [issue](https://github.com/dbt-labs/semantic-layer-sdk-python/issues) or [pull request](https://github.com/dbt-labs/semantic-layer-sdk-python/pulls).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Query the Discovery API

The Discovery API supports ad-hoc queries and integrations. If you are new to the API, refer to [About the Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md) for an introduction.

Use the Discovery API to evaluate data pipeline health and project state across runs or at a moment in time. dbt Labs provide a default [GraphQL explorer](https://metadata.cloud.getdbt.com/graphql) for this API, enabling you to run queries and browse the schema. However, you can also use any GraphQL client of your choice to query the API.

Since GraphQL describes the data in the API, the schema displayed in the GraphQL explorer accurately represents the graph and fields available to query.

#### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

* dbt [multi-tenant](https://docs.getdbt.com/docs/cloud/about-cloud/tenancy.md#multi-tenant) or [single tenant](https://docs.getdbt.com/docs/cloud/about-cloud/tenancy.md#single-tenant) account
* You must be on an [Enterprise or Enterprise+ plan](https://www.getdbt.com/pricing/)
* Your projects must be on a dbt [release tracks](https://docs.getdbt.com/docs/dbt-versions/cloud-release-tracks.md) or dbt version 1.0 or later. Refer to [Upgrade dbt version in Cloud](https://docs.getdbt.com/docs/dbt-versions/upgrade-dbt-version-in-cloud.md) to upgrade.

#### Authorization[​](#authorization "Direct link to Authorization")

Currently, authorization of requests takes place [using a service token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md). dbt admin users can generate a Metadata Only service token that is authorized to execute a specific query against the Discovery API.

Once you've created a token, you can use it in the Authorization header of requests to the dbt Discovery API. Be sure to include the Token prefix in the Authorization header, or the request will fail with a `401 Unauthorized` error. Note that `Bearer` can be used instead of `Token` in the Authorization header. Both syntaxes are equivalent.

#### Access the Discovery API[​](#access-the-discovery-api "Direct link to Access the Discovery API")

1. Create a [service account token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md) to authorize requests. dbt Admin users can generate a *Metadata Only* service token, which can be used to execute a specific query against the Discovery API to authorize requests.

2. Find the API URL to use from the [Discovery API endpoints](#discovery-api-endpoints) table.

3. For specific query points, refer to the [schema documentation](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-schema-job.md).

#### Run queries using HTTP requests[​](#run-queries-using-http-requests "Direct link to Run queries using HTTP requests")

You can run queries by sending a `POST` request to the Discovery API, making sure to replace:

* `YOUR_API_URL` with the appropriate [Discovery API endpoint](#discovery-api-endpoints) for your region and plan.

* `YOUR_TOKEN` in the Authorization header with your actual API token. Be sure to include the Token prefix.

* `QUERY_BODY` with a GraphQL query, for example `{ "query": "<query text>", "variables": "<variables in json>" }`

* `VARIABLES` with a dictionary of your GraphQL query variables, such as a job ID or a filter.

* `ENDPOINT` with the endpoint you're querying, such as environment.
```

Example 2 (unknown):
```unknown
Python example:
```

Example 3 (unknown):
```unknown
Every query will require an environment ID or job ID. You can get the ID from a dbt URL or using the Admin API.

There are several illustrative example queries on this page. For more examples, refer to [Use cases and examples for the Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-use-cases-and-examples.md).

#### Discovery API endpoints[​](#discovery-api-endpoints "Direct link to Discovery API endpoints")

The following are the endpoints for accessing the Discovery API. Use the one that's appropriate for your region and plan.

| Deployment type            | Discovery API URL                                                                                                                                                                                                                                            |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| North America multi-tenant | <https://metadata.cloud.getdbt.com/graphql>                                                                                                                                                                                                                  |
| EMEA multi-tenant          | <https://metadata.emea.dbt.com/graphql>                                                                                                                                                                                                                      |
| APAC multi-tenant          | <https://metadata.au.dbt.com/graphql>                                                                                                                                                                                                                        |
| Multi-cell                 | `https://YOUR_ACCOUNT_PREFIX.metadata.REGION.dbt.com/graphql`<br /><br />Replace `YOUR_ACCOUNT_PREFIX` with your specific account identifier and `REGION` with your location, which could be `us1.dbt.com`.                                                  |
| Single-tenant              | `https://metadata.YOUR_ACCESS_URL/graphql`<br /><br />Replace `YOUR_ACCESS_URL` with your specific account prefix with the appropriate [Access URL](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses.md) for your region and plan. |

#### Reasonable use[​](#reasonable-use "Direct link to Reasonable use")

Discovery (GraphQL) API usage is subject to request rate and response size limits to maintain the performance and stability of the metadata platform and prevent abuse.

Job-level endpoints are subject to query complexity limits. Nested nodes (like parents), code (like rawCode), and catalog columns are considered as most complex. Overly complex queries should be broken up into separate queries with only necessary fields included. dbt Labs recommends using the environment endpoint instead for most use cases to get the latest descriptive and result metadata for a dbt project.

#### Retention limits[​](#retention-limits "Direct link to Retention limits")

You can use the Discovery API to query data from the previous two months. For example, if today was April 1st, you could query data back to February 1st.

#### Run queries with the GraphQL explorer[​](#run-queries-with-the-graphql-explorer "Direct link to Run queries with the GraphQL explorer")

You can run ad-hoc queries directly in the [GraphQL API explorer](https://metadata.cloud.getdbt.com/graphql) and use the document explorer on the left-hand side to see all possible nodes and fields.

Refer to the [Apollo explorer documentation](https://www.apollographql.com/docs/graphos/explorer/explorer) for setup and authorization information for GraphQL.

1. Access the [GraphQL API explorer](https://metadata.cloud.getdbt.com/graphql) and select fields you want to query.

2. Select **Variables** at the bottom of the explorer and replace any `null` fields with your unique values.

3. [Authenticate](https://www.apollographql.com/docs/graphos/explorer/connecting-authenticating#authentication) using Bearer auth with `YOUR_TOKEN`. Select **Headers** at the bottom of the explorer and select **+New header**.

4. Select **Authorization** in the **header key** dropdown list and enter your Bearer auth token in the **value** field. Remember to include the Token prefix. Your header key should be in this format: `{"Authorization": "Bearer <YOUR_TOKEN>}`.

<br />

[![Enter the header key and Bearer auth token values](/img/docs/dbt-cloud/discovery-api/graphql_header.jpg?v=2 "Enter the header key and Bearer auth token values")](#)Enter the header key and Bearer auth token values

1. Run your query by clicking the blue query button in the top right of the **Operation** editor (to the right of the query). You should see a successful query response on the right side of the explorer.

[![Run queries using the Apollo Server GraphQL explorer](/img/docs/dbt-cloud/discovery-api/graphql.jpg?v=2 "Run queries using the Apollo Server GraphQL explorer")](#)Run queries using the Apollo Server GraphQL explorer

##### Fragments[​](#fragments "Direct link to Fragments")

Use the [`... on`](https://www.apollographql.com/docs/react/data/fragments/) notation to query across lineage and retrieve results from specific node types.
```

Example 4 (unknown):
```unknown
##### Pagination[​](#pagination "Direct link to Pagination")

Querying large datasets can impact performance on multiple functions in the API pipeline. Pagination eases the burden by returning smaller data sets one page at a time. This is useful for returning a particular portion of the dataset or the entire dataset piece-by-piece to enhance performance. dbt utilizes cursor-based pagination, which makes it easy to return pages of constantly changing data.

Use the `PageInfo` object to return information about the page. The available fields are:

* `startCursor` string type — Corresponds to the first `node` in the `edge`.
* `endCursor` string type — Corresponds to the last `node` in the `edge`.
* `hasNextPage` boolean type — Whether or not there are more `nodes` after the returned results.

There are connection variables available when making the query:

* `first` integer type — Returns the first n `nodes` for each page, up to 500.
* `after` string type — Sets the cursor to retrieve `nodes` after. It's best practice to set the `after` variable with the object ID defined in the `endCursor` of the previous page.

Below is an example that returns the `first` 500 models `after` the specified Object ID in the variables. The `PageInfo` object returns where the object ID where the cursor starts, where it ends, and whether there is a next page.

[![Example of pagination](/img/Paginate.png?v=2 "Example of pagination")](#)Example of pagination

Below is a code example of the `PageInfo` object:
```

---

## Run tests on all models with a particular materialization

**URL:** llms-txt#run-tests-on-all-models-with-a-particular-materialization

dbt test --select "config.materialized:table"

---

## odbc connections

**URL:** llms-txt#odbc-connections

$ python -m pip install "dbt-spark[ODBC]"

---

## these are equivalent

**URL:** llms-txt#these-are-equivalent

**Contents:**
  - Project flags

dbt.invoke(["--fail-fast", "run", "--select", "tag:my_tag"])
dbt.invoke(["run"], select=["tag:my_tag"], fail_fast=True)

flags:
  <global_config>: <value>

**Examples:**

Example 1 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Project flags

dbt\_project.yml
```

Example 2 (unknown):
```unknown
Reference the [table of all flags](https://docs.getdbt.com/reference/global-configs/about-global-configs.md#available-flags) to see which global configs are available for setting in [`dbt_project.yml`](https://docs.getdbt.com/reference/dbt_project.yml.md).

The `flags` dictionary is the *only* place you can opt out of [behavior changes](https://docs.getdbt.com/reference/global-configs/behavior-changes.md), while the legacy behavior is still supported.

#### Config precedence[​](#config-precedence "Direct link to Config precedence")

<!-- -->

There are multiple ways of setting flags, which depend on the use case:

* **[Project-level `flags` in `dbt_project.yml`](https://docs.getdbt.com/reference/global-configs/project-flags.md):** Define version-controlled defaults for everyone running this project. Also, opt in or opt out of [behavior changes](https://docs.getdbt.com/reference/global-configs/behavior-changes.md) to manage your migration off legacy functionality.
* **[Environment variables](https://docs.getdbt.com/reference/global-configs/environment-variable-configs.md):** Define different behavior in different runtime environments (development vs. production vs. [continuous integration](https://docs.getdbt.com/docs/deploy/continuous-integration.md), or different behavior for different users in development (based on personal preferences).
* **[CLI options](https://docs.getdbt.com/reference/global-configs/command-line-options.md):** Define behavior specific to *this invocation*. Supported for all dbt commands.

The most specific setting "wins." If you set the same flag in all three places, the CLI option will take precedence, followed by the environment variable, and finally, the value in `dbt_project.yml`. If you set the flag in none of those places, it will use the default value defined within dbt.

Most flags can be set in all three places:
```

---

## with semantic version range

**URL:** llms-txt#with-semantic-version-range

dbt deps --add-package dbt-labs/snowplow@">=0.7.0,<0.8.0"

**Examples:**

Example 1 (unknown):
```unknown
###### Non-Hub packages[​](#non-hub-packages "Direct link to Non-Hub packages")

Use the `--source` flag to specify the type of package to be installed:
```

---

## dbt platform users

**URL:** llms-txt#dbt-platform-users

dbt sl query --metrics transactions --group-by metric_time__month,sales_person__tier --order-by metric_time__month,sales_person__tier

---

## initialize

**URL:** llms-txt#initialize

---

## ❌ These will not work

**URL:** llms-txt#❌-these-will-not-work

**Contents:**
  - Resource path
  - Resource type
  - resource-configs
  - returns
  - Run results JSON file
  - Salesforce Data Cloud configurations
  - schema
  - Seed configurations
  - Seed properties
  - seed-paths

require-dbt-version: >=1.0.0 # No quotes? No good
require-dbt-version: ">= 1.0.0" # Don't put whitespace after the equality signs

require-dbt-version: ">=1.0.0"

require-dbt-version: [">=1.0.0", "<2.0.0"]

require-dbt-version: ">=1.0.0,<2.0.0"

require-dbt-version: "1.5.0"

$ dbt compile
Running with dbt=1.5.0
Encountered an error while reading the project:
Runtime Error
  This version of dbt is not supported with the 'my_project' package.
    Installed version of dbt: =1.5.0
    Required version of dbt for 'my_project': ['>=1.6.0', '<2.0.0']
  Check the requirements for the 'my_project' package, or run dbt again with --no-version-check

$ dbt run --no-version-check
Running with dbt=1.5.0
Found 13 models, 2 tests, 1 archives, 0 analyses, 204 macros, 2 operations....

resource_type:
  project_name:
    directory_name:
      subdirectory_name:
        instance_of_resource_type (by name):
          ...

models:
  +enabled: false # this will disable all models (not a thing you probably want to do)

models:
  jaffle_shop:
    +enabled: false # this will apply to all models in your project, but not any installed packages

models:
  jaffle_shop:
    staging:
      +enabled: false # this will apply to all models in the `staging/` directory of your project

.
├── dbt_project.yml
└── models
    ├── marts
    └── staging

models:
  jaffle_shop:
    staging:
      stripe:
        payments:
          +enabled: false # this will apply to only one model

.
├── dbt_project.yml
└── models
    ├── marts
    │   └── core
    │       ├── dim_customers.sql
    │       └── fct_orders.sql
    └── staging
        ├── jaffle_shop
        │   ├── customers.sql
        │   └── orders.sql
        └── stripe
            └── payments.sql

sources:
  your_project_name:
    subdirectory_name:
      source_name:
        source_table_name:
          +enabled: false

dbt build --resource-type model test snapshot --exclude-resource-type snapshot

dbt build --resource-type test model

dbt build --resource-type snapshot

dbt build --resource-type saved_query

dbt build --resource-type test

dbt build --exclude-resource-type test model

dbt build --exclude-resource-type unit_test

functions:
  - name: <function name>
    returns:
      data_type: <string> # required, warehouse-specific
      description: <markdown_string> # optional

functions:
  - name: is_valid_email
    description: Validates if a string is a properly formatted email address
    arguments:
      - name: email_string
        data_type: STRING
        description: The email address to validate
    returns:
      data_type: BOOLEAN
      description: Returns true if the string is a valid email format, false otherwise

functions:
  - name: calculate_metrics
    description: Calculates revenue and profit metrics
    arguments:
      - name: revenue
        data_type: DECIMAL(18,2)
      - name: cost
        data_type: DECIMAL(18,2)
    returns:
      data_type: DECIMAL(18,2)
      description: The calculated profit margin as a percentage

functions:
  - name: split_tags
    description: Splits a comma-separated string into an array of tags
    arguments:
      - name: tag_string
        data_type: STRING
    returns:
      data_type: ARRAY<STRING>
      description: An array of individual tag strings

select {{ dbt.current_timestamp() }} as created_at

dbt compile -s my_model

{
      "status": "success",
      "timing": [
        {
          "name": "compile",
          "started_at": "2023-10-12T16:35:28.510434Z",
          "completed_at": "2023-10-12T16:35:28.519086Z"
        },
        {
          "name": "execute",
          "started_at": "2023-10-12T16:35:28.521633Z",
          "completed_at": "2023-10-12T16:35:28.521641Z"
        }
      ],
      "thread_id": "Thread-2",
      "execution_time": 0.0408780574798584,
      "adapter_response": {},
      "message": null,
      "failures": null,
      "unique_id": "model.my_project.my_model",
      "compiled": true,
      "compiled_code": "select now() as created_at",
      "relation_name": "\"postgres\".\"dbt_dbeatty\".\"my_model\""
    }

models:
  - name: my_model
    columns:
      - name: created_at
        data_tests:
          - not_null:
              config:
                store_failures_as: view
          - unique:
              config:
                store_failures_as: ephemeral

"results": [
    {
      "status": "pass",
      "timing": [
        {
          "name": "compile",
          "started_at": "2023-10-12T17:20:51.279437Z",
          "completed_at": "2023-10-12T17:20:51.317312Z"
        },
        {
          "name": "execute",
          "started_at": "2023-10-12T17:20:51.319812Z",
          "completed_at": "2023-10-12T17:20:51.441967Z"
        }
      ],
      "thread_id": "Thread-2",
      "execution_time": 0.1807551383972168,
      "adapter_response": {
        "_message": "SELECT 1",
        "code": "SELECT",
        "rows_affected": 1
      },
      "message": null,
      "failures": 0,
      "unique_id": "test.my_project.unique_my_model_created_at.a9276afbbb",
      "compiled": true,
      "compiled_code": "\n    \n    \n\nselect\n    created_at as unique_field,\n    count(*) as n_records\n\nfrom \"postgres\".\"dbt_dbeatty\".\"my_model\"\nwhere created_at is not null\ngroup by created_at\nhaving count(*) > 1\n\n\n",
      "relation_name": null
    },
    {
      "status": "pass",
      "timing": [
        {
          "name": "compile",
          "started_at": "2023-10-12T17:20:51.274049Z",
          "completed_at": "2023-10-12T17:20:51.295237Z"
        },
        {
          "name": "execute",
          "started_at": "2023-10-12T17:20:51.296361Z",
          "completed_at": "2023-10-12T17:20:51.491327Z"
        }
      ],
      "thread_id": "Thread-1",
      "execution_time": 0.22345590591430664,
      "adapter_response": {
        "_message": "SELECT 1",
        "code": "SELECT",
        "rows_affected": 1
      },
      "message": null,
      "failures": 0,
      "unique_id": "test.my_project.not_null_my_model_created_at.9b412fbcc7",
      "compiled": true,
      "compiled_code": "\n    \n    \n\n\n\nselect *\nfrom \"postgres\".\"dbt_dbeatty\".\"my_model\"\nwhere created_at is null\n\n\n",
      "relation_name": "\"postgres\".\"dbt_dbeatty_dbt_test__audit\".\"not_null_my_model_created_at\""
    }
  ],

sources:
  - name: default
    tables:
      - name: raw_customers__dll
        description: "Customers raw table stored in default dataspace"   
        columns:
          - name: id__c 
            description: "Customer ID"
            data_tests:
              - not_null
              - unique
          - name: first_name__c
            description: "Customer first name"
          - name: last_name__c
            description: "Customer last name"
          - name: email__c
            description: "Customer email address"
            data_tests:
              - not_null
              - unique

{{ config(
    materialized='table',
    primary_key='customer_id__c',
    category='Profile'
) }}

id__c as customer_id__c,
        first_name__c,
        last_name__c,
        email__c as customer_email__c

from {{ source('default', 'raw_customers__dll') }}

models:
  your_project:
    marketing: #  Grouping or folder for set of models
      +schema: marketing

seeds:
  your_project:
    product_mappings:
      +schema: mappings

saved-queries:
  +schema: metrics

data_tests:
  +store_failures: true
  +schema: test_results

models:
  jaffle_shop: # the name of a project
    marketing:
      +schema: marketing

{{ config(
    schema='marketing'
) }}

seeds:
  +schema: mappings

data_tests:
  +store_failures: true
  +schema: _sad_test_failures  # Will write tables to my_database.my_schema__sad_test_failures

create schema if not exists dev_username_dbt_test__audit authorization username;

seeds:
  <resource-path>:
    +quote_columns: true | false
    +column_types: {column_name: datatype}
    +delimiter: <string>

seeds:
  - name: [<seed-name>]
    config:
      quote_columns: true | false
      column_types: {column_name: datatype}
      delimiter: <string>

seeds:
  +schema: seed_data

seeds:
  jaffle_shop:
    +schema: seed_data

seeds:
  - name: utm_parameters
    config:
      schema: seed_data

seeds:
  jaffle_shop:
    marketing:
      utm_parameters:
        +schema: seed_data

name: jaffle_shop
...
seeds:
  jaffle_shop:
    +enabled: true
    +schema: seed_data
    # This configures seeds/country_codes.csv
    country_codes:
      # Override column types
      +column_types:
        country_code: varchar(2)
        country_name: varchar(32)
    marketing:
      +schema: marketing # this will take precedence

seeds:
  - name: <string>
    description: <markdown_string>
    config:
      <seed_config>: <config_value>
      docs:
        show: true | false
        node_color: <color_id> # Use name (such as node_color: purple) or hex code with quotes (such as node_color: "#cd7f32")
    data_tests:
      - <test>
      - ... # declare additional tests
    columns:
      - name: <column name>
        description: <markdown_string>
        quote: true | false
        data_tests:
          - <test>
          - ... # declare additional tests
        config:
          meta: {<dictionary>}
          tags: [<string>]

- name: ... # declare properties of additional columns

- name: ... # declare properties of additional seeds

seed-paths: [directorypath]

seed-paths: ["seed"]
    
    seed-paths: ["/Users/username/project/seed"]
    
seed-paths: ["custom_seeds"]

seed-paths: ["models"]
model-paths: ["models"]

seed-paths: ["seeds", "custom_seeds"]

{
    "semantic_models": [
        {
            "name": "semantic model name",
            "defaults": null,
            "description": "semantic model description",
            "node_relation": {
                "alias": "model alias",
                "schema_name": "model schema",
                "database": "model db",
                "relation_name": "Fully qualified relation name"
            },
            "entities": ["entities in the semantic model"],
            "measures": ["measures in the semantic model"],
            "dimensions": ["dimensions in the semantic model" ],
        }
    ],
    "metrics": [
        {
            "name": "name of the metric",
            "description": "metric description",
            "type": "metric type",
            "type_params": {
                "measure": {
                    "name": "name for measure",
                    "filter": "filter for measure",
                    "alias": "alias for measure"
                },
                "numerator": null,
                "denominator": null,
                "expr": null,
                "window": null,
                "grain_to_date": null,
                "metrics": ["metrics used in defining the metric. this is used in derived metrics"],
                "input_measures": []
            },
            "filter": null,
            "metadata": null
        }
    ],
    "project_configuration": {
        "time_spine_table_configurations": [
            {
                "location": "fully qualified table name for timespine",
                "column_name": "date column",
                "grain": "day"
            }
        ],
        "metadata": null,
        "dsi_package_version": {}
    },
    "saved_queries": [
        {
            "name": "name of the saved query",
            "query_params": {
                "metrics": [
                    "metrics used in the saved query"
                ],
                "group_by": [
                    "TimeDimension('model_primary_key__date_column', 'day')",
                    "Dimension('model_primary_key__metric_one')",
                    "Dimension('model__dimension')"
                ],
                "where": null
            },
            "description": "Description of the saved query",
            "metadata": null,
            "label": null,
            "exports": [
                {
                    "name": "saved_query_name",
                    "config": {
                        "export_as": "view",
                        "schema_name": null,
                        "alias": null
                    }
                }
            ]
        }
    ]
}

dbt run --select "+snowplow_sessions +fct_orders"

dbt run --select "+snowplow_sessions,+fct_orders"

dbt run --select "stg_invoices+,stg_accounts+"

dbt run --select "marts.finance,tag:nightly"

models:
  - name: large_table
    columns:
      - name: slightly_unreliable_column
        data_tests:
          - unique:
              config:
                severity: error
                error_if: ">1000"
                warn_if: ">10"

{{ config(error_if = '>50') }}

{% test <testname>(model, column_name) %}

{{ config(severity = 'warn') }}

data_tests:
  +severity: warn  # all tests

<package_name>:
    +warn_if: >10 # tests in <package_name>

{{ config(materialized='table', storage_type='rowstore') }}

{{
    config(
        primary_key=['id', 'user_id'],
        shard_key=['id']
    )
}}

{{
    config(
        materialized='table',
        unique_table_key=['id'],
        sort_key=['status'],
    )
}}

{{
    config(
        materialized='table',
        shard_key=['id'],
        indexes=[{'columns': ['order_date', 'id']}, {'columns': ['status'], 'type': 'hash'}]
    )
}}

{{
    config(
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
}}

models:
  - name: dim_customers
    config:
      materialized: table
      contract:
        enforced: true
    columns:
      - name: customer_id
        data_type: int
        constraints:
          - type: not_null
      - name: customer_name
        data_type: text

select
  'abc123' as customer_id,
  'My Best Customer' as customer_name

select
  ('abc123' :> int) as customer_id,
  ('My Best Customer' :> text) as customer_name

select
  'abc123' as customer_id,
  ('My Best Customer' :> text) as customer_name

Please ensure the name, data_type, and number of columns in your contract match the columns in your model's definition.
| column_name | definition_type | contract_type | mismatch_reason       |
| customer_id | LONGBLOB        | LONG          | data type mismatch    |

create table my_snapshot_table_backup as
   select * from my_snapshot_table;
   
   alter table my_snapshot_table
   add column dbt_valid_from timestamp,
   add column dbt_valid_to timestamp;
   
   snapshots:
     - name: orders_snapshot
       relation: source('something','orders')
       config:
         strategy: timestamp
         updated_at: updated_at
         unique_key: id
         dbt_valid_to_current: "to_date('9999-12-31')"
         snapshot_meta_column_names:
           dbt_valid_from: start_date
           dbt_valid_to: end_date
   
  snapshots:
    +unique_key: id
  
  snapshots:
    jaffle_shop:
      +unique_key: id
  
  snapshots:
    jaffle_shop:
      postgres_app:
        orders_snapshot:
          +unique_key: id
          +strategy: timestamp
          +updated_at: updated_at

snapshots:
    - name: orders_snapshot
      +persist_docs:
        relation: true
        columns: true
  
snapshots:
  - name: <snapshot_name>
    config:
      snapshot_meta_column_names:
        dbt_valid_from: <string>
        dbt_valid_to: <string>
        dbt_scd_id: <string>
        dbt_updated_at: <string>
        dbt_is_deleted: <string>

{{
    config(
      snapshot_meta_column_names={
        "dbt_valid_from": "<string>",
        "dbt_valid_to": "<string>",
        "dbt_scd_id": "<string>",
        "dbt_updated_at": "<string>",
        "dbt_is_deleted": "<string>",
      }
    )
}}

snapshots:
  <resource-path>:
    +snapshot_meta_column_names:
      dbt_valid_from: <string>
      dbt_valid_to: <string>
      dbt_scd_id: <string>
      dbt_updated_at: <string>
      dbt_is_deleted: <string>

md5(
 coalesce(cast(unique_key1 as string), '') || '|' ||
 coalesce(cast(unique_key2 as string), '') || '|' ||
 coalesce(cast(updated_at as string), '')
)

snapshots:
  - name: orders_snapshot
    relation: ref("orders")
    config:
      unique_key: id
      strategy: check
      check_cols: all
      hard_deletes: new_record
      snapshot_meta_column_names:
        dbt_valid_from: start_date
        dbt_valid_to: end_date
        dbt_scd_id: scd_id
        dbt_updated_at: modified_date
        dbt_is_deleted: is_deleted

select * from {{ ref('orders_snapshot') }}

snapshot-paths: [directorypath]

snapshot-paths: ["snapshots"]
    
    snapshot-paths: ["/Users/username/project/snapshots"]
    
snapshot-paths: ["archives"]

SnowflakeDynamicTableConfig.__init__() missing 6 required positional arguments: 'name', 'schema_name', 'database_name', 'query', 'target_lag', and 'snowflake_warehouse'

models:
  <resource-path>:
    +tmp_relation_type: table | view ## If not defined, view is the default.

{{ config(
    tmp_relation_type="table | view", ## If not defined, view is the default.
) }}

models:
  +transient: false
  my_project:
    ...

{{ config(materialized='table', transient=true) }}

models:
  <resource-path>:
    +query_tag: dbt_special

{{ config(
    query_tag = 'dbt_special'
) }}

{% macro set_query_tag() -%}
  {% set new_query_tag = model.name %} 
  {% if new_query_tag %}
    {% set original_query_tag = get_current_query_tag() %}
    {{ log("Setting query_tag to '" ~ new_query_tag ~ "'. Will reset to '" ~ original_query_tag ~ "' after materialization.") }}
    {% do run_query("alter session set query_tag = '{}'".format(new_query_tag)) %}
    {{ return(original_query_tag)}}
  {% endif %}
  {{ return(none)}}
{% endmacro %}

{{
  config(
    materialized='table',
    cluster_by=['session_start']
  )
}}

select
  session_id,
  min(event_time) as session_start,
  max(event_time) as session_end,
  count(*) as count_pageviews

from {{ source('snowplow', 'event') }}
group by 1

create or replace table my_database.my_schema.my_table as (

select * from (
    select
      session_id,
      min(event_time) as session_start,
      max(event_time) as session_end,
      count(*) as count_pageviews

from {{ source('snowplow', 'event') }}
    group by 1
  )

-- this order by is added by dbt in order to create the
  -- table in an already-clustered manner.
  order by session_start

alter table my_database.my_schema.my_table cluster by (session_start);

models:
  +automatic_clustering: true

def model(dbt, session):
    dbt.config(
        materialized = "table",
        python_version="3.11"
    )

import pandas
import snowflake.snowpark as snowpark

def model(dbt, session: snowpark.Session):
    dbt.config(
        materialized="table",
        secrets={"secret_variable_name": "test_secret"},
        external_access_integrations=["test_external_access_integration"],
    )
    import _snowflake
    return session.create_dataframe(
        pandas.DataFrame(
            [{"secret_value": _snowflake.get_generic_secret_string('secret_variable_name')}]
        )
    )

def model(dbt, session):
    # Configure the model
    dbt.config(
        materialized="table",
        imports=["@mystage/mycustompackage.zip"],  # Specify the external package location
    )
    
    # Example data transformation using the imported package
    # (Assuming `some_external_package` has a function we can call)
    data = {
        "name": ["Alice", "Bob", "Charlie"],
        "score": [85, 90, 88]
    }
    df = pd.DataFrame(data)

# Process data with the external package
    df["adjusted_score"] = df["score"].apply(lambda x: some_external_package.adjust_score(x))
    
    # Return the DataFrame as the model output
    return df

name: my_project
version: 1.0.0

models:
  +snowflake_warehouse: "EXTRA_SMALL"    # default Snowflake virtual warehouse for all models in the project.
  my_project:
    clickstream:
      +snowflake_warehouse: "EXTRA_LARGE"    # override the default Snowflake virtual warehouse for all models under the `clickstream` directory.
snapshots:
  +snowflake_warehouse: "EXTRA_LARGE"    # all Snapshot models are configured to use the `EXTRA_LARGE` warehouse.

models:
  - name: my_model
    config:
      snowflake_warehouse: "EXTRA_LARGE"    # override the Snowflake virtual warehouse just for this model

**Examples:**

Example 1 (unknown):
```unknown
#### Examples[​](#examples "Direct link to Examples")

##### Specify a minimum dbt version[​](#specify-a-minimum-dbt-version "Direct link to Specify a minimum dbt version")

Use a `>=` operator for a minimum boundary. In the following example, this project will run with any version of dbt greater than or equal to 1.0.0.

dbt\_project.yml
```

Example 2 (unknown):
```unknown
##### Pin to a range[​](#pin-to-a-range "Direct link to Pin to a range")

Use a comma separated list for an upper and lower bound. In the following example, this project will run with dbt 1.x.x.

dbt\_project.yml
```

Example 3 (unknown):
```unknown
OR

dbt\_project.yml
```

Example 4 (unknown):
```unknown
##### Require a specific dbt version[​](#require-a-specific-dbt-version "Direct link to Require a specific dbt version")

Not recommended

Pinning to a specific dbt version is discouraged because it limits project flexibility and can cause compatibility issues, especially with dbt packages. It's recommended to [pin to a major release](#pin-to-a-range), using a version range (for example, `">=1.0.0", "<2.0.0"`) for broader compatibility and to benefit from updates.

While you can restrict your project to run only with an exact version of dbt Core, we do not recommend this for dbt Core v1.0.0 and higher.

In the following example, the project will only run with dbt v1.5:

dbt\_project.yml
```

---

## multiple arguments can be provided to --select

**URL:** llms-txt#multiple-arguments-can-be-provided-to---select

dbt run --select "my_first_model my_second_model"

---

## introspect manifest

**URL:** llms-txt#introspect-manifest

---

## select my_model and all of its children

**URL:** llms-txt#select-my_model-and-all-of-its-children

dbt run --select "my_model+"

---

## run tests for all models in package

**URL:** llms-txt#run-tests-for-all-models-in-package

dbt test --select "some_package.*"

---

## Plot the runElapsedTime over time

**URL:** llms-txt#plot-the-runelapsedtime-over-time

plt.plot(model_df['runGeneratedAt'], model_df['runElapsedTime'])
plt.title('Run Elapsed Time')
plt.show()

---

## seeds/my_seed.csv

**URL:** llms-txt#seeds/my_seed.csv

my_seed_csv = """
id,name,some_date
1,Easton,1981-05-20T06:46:51
2,Lillian,1978-09-03T18:10:33
3,Jeremiah,1982-03-11T03:59:51
4,Nolan,1976-05-06T20:21:35
""".lstrip()

---

## thrift or http connections

**URL:** llms-txt#thrift-or-http-connections

$ python -m pip install "dbt-spark[PyHive]"

**Examples:**

Example 1 (unknown):
```unknown

```

---

## Plot the executionTime over time

**URL:** llms-txt#plot-the-executiontime-over-time

plt.plot(model_df['executeStartedAt'], model_df['executionTime'])
plt.title(model_df['name'].iloc[0]+" Execution Time")
plt.show()

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first) {
        edges {
          node {
            uniqueId
            compiledCode
            database
            schema
            alias
            materializedType
            executionInfo {
              executeCompletedAt
              lastJobDefinitionId
              lastRunGeneratedAt
              lastRunId
              lastRunStatus
              lastRunError
              lastSuccessJobDefinitionId
              runGeneratedAt
              lastSuccessRunId
            }
          }
        }
      }
    }
  }
}

query ($jobId: Int!, $runId: Int!) {
  models(jobId: $jobId, runId: $runId) {
    name
    status
    tests {
      name
      status
    }
  }
}

query ($jobId: BigInt!, $runId: BigInt!) {
  job(id: $jobId, runId: $runId) {
    models {
      name
      status
      tests {
        name
        status
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(
        first: $first
        filter: { uniqueIds: "MODEL.PROJECT.MODEL_NAME" }
      ) {
        edges {
          node {
            rawCode
            ancestors(types: [Source]) {
              ... on SourceAppliedStateNestedNode {
                freshness {
                  maxLoadedAt
                }
              }
            }
            executionInfo {
              runGeneratedAt
              executeCompletedAt
            }
            materializedType
          }
        }
      }
    }
    definition {
      models(
        first: $first
        filter: { uniqueIds: "MODEL.PROJECT.MODEL_NAME" }
      ) {
        edges {
          node {
            rawCode
            runGeneratedAt
            materializedType
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(first: $first, filter: { lastRunStatus: error }) {
        edges {
          node {
            name
            executionInfo {
              lastRunId
            }
          }
        }
      }
      tests(first: $first, filter: { status: "fail" }) {
        edges {
          node {
            name
            executionInfo {
              lastRunId
            }
          }
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $uniqueId: String!, $lastRunCount: Int) {
  environment(id: $environmentId) {
    applied {
      modelHistoricalRuns(uniqueId: $uniqueId, lastRunCount: $lastRunCount) {
        name
        executeStartedAt
        status
        tests {
          name
          status
        }
      }
    }
  }
}

query ($environmentId: BigInt!, $first: Int!) {
  environment(id: $environmentId) {
    applied {
      models(
        first: $first
        filter: { uniqueIds: "MODEL.PROJECT.MODEL_NAME" }
      ) {
        edges {
          node {
            name
            ancestors(types: [Model, Source, Seed, Snapshot]) {
              ... on ModelAppliedStateNestedNode {
                name
                resourceType
                materializedType
                executionInfo {
                  executeCompletedAt
                }
              }
              ... on SourceAppliedStateNestedNode {
                sourceName
                name
                resourceType
                freshness {
                  maxLoadedAt
                }
              }
              ... on SnapshotAppliedStateNestedNode {
                name
                resourceType
                executionInfo {
                  executeCompletedAt
                }
              }
              ... on SeedAppliedStateNestedNode {
                name
                resourceType
                executionInfo {
                  executeCompletedAt
                }
              }
            }
          }
        }
      }
    }
  }
}

**Examples:**

Example 1 (unknown):
```unknown
Plotting examples:

[![The plot of runElapsedTime over time](/img/docs/dbt-cloud/discovery-api/plot-of-runelapsedtime.png?v=2 "The plot of runElapsedTime over time")](#)The plot of runElapsedTime over time

[![The plot of executionTime over time](/img/docs/dbt-cloud/discovery-api/plot-of-executiontime.png?v=2 "The plot of executionTime over time")](#)The plot of executionTime over time

##### What’s the latest state of each model?[​](#whats-the-latest-state-of-each-model "Direct link to What’s the latest state of each model?")

The Discovery API provides information about the applied state of models and how they arrived in that state. You can retrieve the status information from the most recent run and most recent successful run (execution) from the `environment` endpoint and dive into historical runs using job-based and `modelByEnvironment` endpoints.

Example query

The API returns full identifier information (`database.schema.alias`) and the `executionInfo` for both the most recent run and most recent successful run from the database:
```

Example 2 (unknown):
```unknown
##### What happened with my job run?[​](#what-happened-with-my-job-run "Direct link to What happened with my job run?")

You can query the metadata at the job level to review results for specific runs. This is helpful for historical analysis of deployment performance or optimizing particular jobs.

Example query

Deprecated example:
```

Example 3 (unknown):
```unknown
New example:
```

Example 4 (unknown):
```unknown
##### What’s changed since the last run?[​](#whats-changed-since-the-last-run "Direct link to What’s changed since the last run?")

Unnecessary runs incur higher infrastructure costs and load on the data team and their systems. A model doesn’t need to be run if it’s a view and there's no code change since the last run, or if it’s a table/incremental with no code change since last run and source data has not been updated since the last run.

Example query

With the API, you can compare the `rawCode` between the definition and applied state, and review when the sources were last loaded (source `maxLoadedAt` relative to model `executeCompletedAt`) given the `materializedType` of the model:
```

---

## run the command

**URL:** llms-txt#run-the-command

res: dbtRunnerResult = dbt.invoke(cli_args)

---

## Convert to dataframe

**URL:** llms-txt#convert-to-dataframe

model_df = pd.DataFrame(model_historical_metadata)

---

## When testing, you will want to hardcode run_id and account_id to IDs that exist; the sample webhook won't work.

**URL:** llms-txt#when-testing,-you-will-want-to-hardcode-run_id-and-account_id-to-ids-that-exist;-the-sample-webhook-won't-work.

run_id = hook_data['runId']
account_id = full_body['accountId']

---

## Import the standard functional fixtures as a plugin

**URL:** llms-txt#import-the-standard-functional-fixtures-as-a-plugin

---

## note the dialect is set to Snowflake, so make that specific to your setup

**URL:** llms-txt#note-the-dialect-is-set-to-snowflake,-so-make-that-specific-to-your-setup

---

## ✅ Correct

**URL:** llms-txt#✅-correct

target/
dbt_packages/
logs/

---

## ├── csvs

**URL:** llms-txt#├──-csvs

---

## Monthly Recurring Revenue (MRR) playbook.

**URL:** llms-txt#monthly-recurring-revenue-(mrr)-playbook.

This dbt project is a worked example to demonstrate how to model subscription
revenue. **Check out the full write-up [here](https://blog.getdbt.com/modeling-subscription-revenue/),
as well as the repo for this project [here](https://github.com/dbt-labs/mrr-playbook/).**
...

{% docs __dbt_utils__ %}

**Examples:**

Example 1 (unknown):
```unknown
##### Custom project-level overviews[​](#custom-project-level-overviews "Direct link to Custom project-level overviews")

*Currently available for dbt Docs only.*

You can set different overviews for each dbt project/package included in your documentation site by creating a docs block named `__[project_name]__`.

For example, in order to define custom overview pages that appear when a viewer navigates inside the `dbt_utils` or `snowplow` package:

models/overview.md
```

---

## run only data tests defined generically

**URL:** llms-txt#run-only-data-tests-defined-generically

dbt test --select "test_type:generic"

---

## └── models

**URL:** llms-txt#└──-models

---

## Fetch run info from the dbt Admin API

**URL:** llms-txt#fetch-run-info-from-the-dbt-admin-api

url = f'https://YOUR_ACCESS_URL/api/v2/accounts/{account_id}/runs/{run_id}/?include_related=["run_steps"]'
headers = {'Authorization': f'Token {api_token}'}
run_data_response = requests.get(url, headers=headers)
run_data_response.raise_for_status()
run_data_results = run_data_response.json()['data']

---

## Set API key

**URL:** llms-txt#set-api-key

auth_token = *[SERVICE_TOKEN_HERE]*

---

## In dbt Core

**URL:** llms-txt#in-dbt-core

**Contents:**
  - MetricFlow time spine
  - Metrics as dimensions with metric filters
  - Microsoft Excel StarterEnterpriseEnterprise +
  - Microsoft Excel [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Model access

mf query --metrics order_total --group-by metric_time,is_food_order --limit 10 --order-by -metric_time --where "is_food_order = True" --start-time '2017-08-22' --end-time '2017-08-27' --csv query_example.csv

✔ Success 🦄 - query completed after 0.83 seconds
🖨 Successfully written query output to query_example.csv

dbt sl query --metrics revenue --group-by metric_time__month # In the dbt platform

mf query --metrics revenue --group-by metric_time__month # In dbt Core

{{ Metric('metric_name', group_by=['entity_name']) }}

with data_models_per_user as (
    select
        account_id as account,
        count(model_runs) as data_model_runs
    from 
        {{ ref('fct_model_runs') }}
    group by 
        account_id
),

activated_accounts as (
    select
        count(distinct account_id) as activated_accounts
    from 
        {{ ref('dim_accounts') }}
    left join 
        data_models_per_user 
    on 
        {{ ref('dim_accounts') }}.account_id = data_models_per_user.account
    where 
        data_models_per_user.data_model_runs > 5
)

select
    *
from 
    activated_accounts

semantic_models:
    - name: model_runs
      ... # Placeholder for other configurations
      entities:
        - name: model_run
          type: primary
        - name: account
          type: foreign
      measures:
        - name: data_model_runs
          agg: sum
          expr: 1
          create_metric: true # The 'create_metric: true' attribute automatically creates the 'data_model_runs' metric.

- name: accounts
      ... # Placeholder for other configurations
      entities:
        - name: account
          type: primary
      measures:
        - name: accounts
          agg: sum
          expr: 1
          create_metric: true
  metrics:
    - name: activated_accounts
      label: Activated Accounts
      type: simple
      type_params:
        measure: accounts
      filter: |
        {{ Metric('data_model_runs', group_by=['account']) }} > 5
  
  select
  	sum(1) as data_model_runs,
  	account
  from 
  	data_model_runs
  group by
  	account
  
  select
    sum(1) as activated_accounts
  from accounts
  left join (
    select
        sum(1) as data_model_runs, 
  	      account
      from data_model_runs
      group by 
  	      account
  ) as subq on accounts.account = subq.account
  where data_model_runs > 5
  
models:
  my_project_name:
    marts:
      customers:
        +group: customer_success
      finance:
        +group: finance

dbt run -s marketing_model
...
dbt.exceptions.DbtReferenceError: Parsing Error
  Node model.jaffle_shop.marketing_model attempted to reference node model.jaffle_shop.finance_model, 
  which is not allowed because the referenced node is private to the finance group.

**Examples:**

Example 1 (unknown):
```unknown
**Result**
```

Example 2 (unknown):
```unknown
#### Time granularity[​](#time-granularity "Direct link to Time granularity")

Optionally, you can specify the time granularity you want your data to be aggregated at by appending two underscores and the unit of granularity you want to `metric_time`, the global time dimension. You can group the granularity by: `day`, `week`, `month`, `quarter`, and `year`.

Below is an example for querying metric data at a monthly grain:
```

Example 3 (unknown):
```unknown
#### Export[​](#export "Direct link to Export")

Run [exports for a specific saved query](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md#exports-for-single-saved-query). Use this command to test and generate exports in your development environment. You can also use the `--select` flag to specify particular exports from a saved query. Refer to [exports in development](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md#exports-in-development) for more info.

Export is available in dbt.
```

Example 4 (unknown):
```unknown
#### Export-all[​](#export-all "Direct link to Export-all")

Run [exports for multiple saved queries](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md#exports-for-multiple-saved-queries) at once. This command provides a convenient way to manage and execute exports for several queries simultaneously, saving time and effort. Refer to [exports in development](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md#exports-in-development) for more info.

Export is available in dbt.
```

---

## shared interfaces

**URL:** llms-txt#shared-interfaces

dbt-adapters==1.10.4
dbt-common==1.14.0
dbt-semantic-interfaces==0.7.4

---

## ├── stg_event_log.sql

**URL:** llms-txt#├──-stg_event_log.sql

---

## so let's skip on Apache Spark

**URL:** llms-txt#so-let's-skip-on-apache-spark

**Contents:**
  - Building dbt packages
  - Coalesce dbt Fusion Engine in platform Quickstart Guide
  - Create Datadog events from dbt results
  - Create new materializations

@pytest.mark.skip_profile('apache_spark')
class TestSnapshotCheckColsSpark(BaseSnapshotCheckCols):
    @pytest.fixture(scope="class")
    def project_config_update(self):
        return {
            "seeds": {
                "+file_format": "delta",
            },
            "snapshots": {
                "+file_format": "delta",
            }
        }

python3 -m pytest tests/functional --profile apache_spark
python3 -m pytest tests/functional --profile databricks_sql_endpoint

---
title: "Documenting a new adapter"
id: "documenting-a-new-adapter"
---

import SetUpPages from '/snippets/_setup-pages-intro.md';

<SetUpPages meta={frontMatter.meta} />

$ dbt init [package_name]

packages:
  - package: dbt-labs/dbt_utils
    version: [">0.6.5", "0.7.0"]

packages:
    - local: ../ # this means "one directory above the current directory"

#example: replace with your actual path
cd ~/Documents/GitHub/dbt-cloud-webhooks-datadog

flyctl secrets set DBT_CLOUD_SERVICE_TOKEN=abc123 DBT_CLOUD_AUTH_TOKEN=def456 DD_API_KEY=ghi789 DD_SITE=datadoghq.com

{% materialization [materialization name], ["specified adapter" | default] %}
...
{% endmaterialization %}

{% materialization my_materialization_name, default %}
 -- cross-adapter materialization... assume Redshift is not supported
{% endmaterialization %}

{% materialization my_materialization_name, adapter='redshift' %}
-- override the materialization for Redshift
{% endmaterialization %}

-- Refer to the table materialization (linked above) for an example of real syntax
-- This code will not work and is only intended for demonstration purposes
{% set existing = adapter.get_relation(this) %}
{% if existing and existing.is_view  %}
  {% do adapter.drop_relation(existing) %}
{% endif %}

...
{{ run_hooks(pre_hooks) }}
....

{{ drop_relation_if_exists(backup_relation) }}

{%- materialization my_view, default -%}

{%- set target_relation = api.Relation.create(
        identifier=this.identifier, schema=this.schema, database=this.database,
        type='view') -%}

-- ... setup database ...
  -- ... run pre-hooks...

-- build model
  {% call statement('main') -%}
    {{ create_view_as(target_relation, sql) }}
  {%- endcall %}
  
  -- ... run post-hooks ...
  -- ... clean up the database...

-- Return the relations created in this materialization
  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization -%}

**Examples:**

Example 1 (unknown):
```unknown
Finally:
```

Example 2 (unknown):
```unknown
#### Document a new adapter[​](#document-a-new-adapter "Direct link to Document a new adapter")

If you've already built, and tested your adapter, it's time to document it so the dbt community will know that it exists and how to use it.

##### Making your adapter available[​](#making-your-adapter-available "Direct link to Making your adapter available")

Many community members maintain their adapter plugins under open source licenses. If you're interested in doing this, we recommend:

* Hosting on a public git provider (for example, GitHub or Gitlab)
* Publishing to [PyPI](https://pypi.org/)
* Adding to the list of ["Supported Data Platforms"](https://docs.getdbt.com/docs/supported-data-platforms.md#community-supported) (more info below)

##### General Guidelines[​](#general-guidelines "Direct link to General Guidelines")

To best inform the dbt community of the new adapter, you should contribute to the dbt's open-source documentation site, which uses the [Docusaurus project](https://docusaurus.io/). This is the site you're currently on!

##### Conventions[​](#conventions "Direct link to Conventions")

Each `.md` file you create needs a header as shown below. The document id will also need to be added to the config file: `website/sidebars.js`.
```

Example 3 (unknown):
```unknown
##### Single Source of Truth[​](#single-source-of-truth "Direct link to Single Source of Truth")

We ask our adapter maintainers to use the [docs.getdbt.com repo](https://github.com/dbt-labs/docs.getdbt.com) (i.e. this site) as the single-source-of-truth for documentation rather than having to maintain the same set of information in three different places. The adapter repo's `README.md` and the data platform's documentation pages should simply link to the corresponding page on this docs site. Keep reading for more information on what should and shouldn't be included on the dbt docs site.

##### Assumed Knowledge[​](#assumed-knowledge "Direct link to Assumed Knowledge")

To simplify things, assume the reader of this documentation already knows how both dbt and your data platform works. There's already great material for how to learn dbt and the data platform out there. The documentation we're asking you to add should be what a user who is already profiecient in both dbt and your data platform would need to know in order to use both. Effectively that boils down to two things: how to connect, and how to configure.

##### Topics and Pages to Cover[​](#topics-and-pages-to-cover "Direct link to Topics and Pages to Cover")

The following subjects need to be addressed across three pages of this docs site to have your data platform be listed on our documentation. After the corresponding pull request is merged, we ask that you link to these pages from your adapter repo's `README` as well as from your product documentation.

To contribute, all you will have to do make the changes listed in the table below.

| How To...            | File to change within `/website/docs/`                         | Action | Info to include                                                                                                                                                                                       |
| -------------------- | -------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Connect              | `/docs/core/connect-data-platform/{MY-DATA-PLATFORM}-setup.md` | Create | Give all information needed to define a target in `~/.dbt/profiles.yml` and get `dbt debug` to connect to the database successfully. All possible configurations should be mentioned.                 |
| Configure            | `reference/resource-configs/{MY-DATA-PLATFORM}-configs.md`     | Create | What options and configuration specific to your data platform do users need to know? e.g. table distribution and indexing options, column\_quoting policy, which incremental strategies are supported |
| Discover and Install | `docs/supported-data-platforms.md`                             | Modify | Is it a vendor- or community- supported adapter? How to install Python adapter package? Ideally with pip and PyPI hosted package, but can also use `git+` link to GitHub Repo                         |
| Add link to sidebar  | `website/sidebars.js`                                          | Modify | Add the document id to the correct location in the sidebar menu                                                                                                                                       |

For example say I want to document my new adapter: `dbt-ders`. For the "Connect" page, I will make a new Markdown file, `ders-setup.md` and add it to the `/website/docs/core/connect-data-platform/` directory.

##### Example PRs to add new adapter documentation[​](#example-prs-to-add-new-adapter-documentation "Direct link to Example PRs to add new adapter documentation")

Below are some recent pull requests made by partners to document their data platform's adapter:

* [TiDB](https://github.com/dbt-labs/docs.getdbt.com/pull/1309)
* [SingleStore](https://github.com/dbt-labs/docs.getdbt.com/pull/1044)
* [Firebolt](https://github.com/dbt-labs/docs.getdbt.com/pull/941)

Note — Use the following re-usable component to auto-fill the frontmatter content on your new page:
```

Example 4 (unknown):
```unknown
#### Promote a new adapter[​](#promote-a-new-adapter "Direct link to Promote a new adapter")

The most important thing here is recognizing that people are successful in the community when they join, first and foremost, to engage authentically.

What does authentic engagement look like? It’s challenging to define explicit rules. One good rule of thumb is to treat people with dignity and respect.

Contributors to the community should think of contribution *as the end itself,* not a means toward other business KPIs (leads, community members, etc.). [We are a mission-driven company.](https://www.getdbt.com/dbt-labs/values/) Some ways to know if you’re authentically engaging:

* Is an engagement’s *primary* purpose of sharing knowledge and resources or building brand engagement?
* Imagine you didn’t work at the org you do — can you imagine yourself still writing this?
* Is it written in formal / marketing language, or does it sound like you, the human?

##### Who should join the dbt community slack?[​](#who-should-join-the-dbt-community-slack "Direct link to Who should join the dbt community slack?")

* People who have insight into what it means to do hands-on [analytics engineering](https://www.getdbt.com/analytics-engineering/) work The dbt Community Slack workspace is fundamentally a place for analytics practitioners to interact with each other — the closer the users are in the community to actual data/analytics engineering work, the more natural their engagement will be (leading to better outcomes for partners and the community).

* DevRel practitioners with strong focus DevRel practitioners often have a strong analytics background and a good understanding of the community. It’s essential to be sure they are focused on *contributing,* not on driving community metrics for partner org (such as signing people up for their slack or events). The metrics will rise naturally through authentic engagement.

* Founder and executives who are interested in directly engaging with the community This is either incredibly successful or not at all depending on the profile of the founder. Typically, this works best when the founder has a practitioner-level of technical understanding and is interested in joining not to promote, but to learn and hear from users.

* Software Engineers at partner products that are building and supporting integrations with either - Software Engineers at partner products that are building and supporting integrations with either dbt Core or the dbt Core or the dbt platform This is successful when the engineers are familiar with dbt as a product or at least have taken our training course. The Slack is often a place where end-user questions and feedback is initially shared, so it is recommended that someone technical from the team be present. There are also a handful of channels aimed at those building integrations, which tend to be a font of knowledge.

##### Who might struggle in the dbt community[​](#who-might-struggle-in-the-dbt-community "Direct link to Who might struggle in the dbt community")

* People in marketing roles dbt Slack is not a marketing channel. Attempts to use it as such invariably fall flat and can even lead to people having a negative view of a product. This doesn’t mean that dbt can’t serve marketing objectives, but a long-term commitment to engagement is the only proven method to do this sustainably.

* People in product roles The dbt Community can be an invaluable source of feedback on a product. There are two primary ways this can happen — organically (community members proactively suggesting a new feature) and via direct calls for feedback and user research. Immediate calls for engagement must be done in your dedicated #tools channel. Direct calls should be used sparingly, as they can overwhelm more organic discussions and feedback.

##### Who is the audience for an adapter release?[​](#who-is-the-audience-for-an-adapter-release "Direct link to Who is the audience for an adapter release?")

A new adapter is likely to drive huge community interest from several groups of people:

* People who are currently using the database that the adapter is supporting
* People who may be adopting the database in the near future.
* People who are interested in dbt development in general.

The database users will be your primary audience and the most helpful in achieving success. Engage them directly in the adapter’s dedicated Slack channel. If one does not exist already, reach out in #channel-requests, and we will get one made for you and include it in an announcement about new channels.

The final group is where non-slack community engagement becomes important. Twitter and LinkedIn are both great places to interact with a broad audience. A well-orchestrated adapter release can generate impactful and authentic engagement.

##### How to message the initial rollout and follow-up content[​](#how-to-message-the-initial-rollout-and-follow-up-content "Direct link to How to message the initial rollout and follow-up content")

Tell a story that engages dbt users and the community. Highlight new use cases and functionality unlocked by the adapter in a way that will resonate with each segment.

* Existing users of your technology who are new to dbt

  * Provide a general overview of the value dbt will deliver to your users. This can lean on dbt's messaging and talking points which are laid out in the [dbt viewpoint.](https://docs.getdbt.com/community/resources/viewpoint.md)
  * Give examples of a rollout that speaks to the overall value of dbt and your product.

* Users who are already familiar with dbt and the community

  * Consider unique use cases or advantages your adapter provide over existing adapters. Who will be excited for this?
  * Contribute to the dbt Community and ensure that dbt users on your adapter are well supported (tutorial content, packages, documentation, etc).
  * Example of a rollout that is compelling for those familiar with dbt: [Firebolt](https://www.linkedin.com/feed/update/urn:li:activity:6879090752459182080/)

##### Tactically manage distribution of content about new or existing adapters[​](#tactically-manage-distribution-of-content-about-new-or-existing-adapters "Direct link to Tactically manage distribution of content about new or existing adapters")

There are tactical pieces on how and where to share that help ensure success.

* On slack:

  * \#i-made-this channel — this channel has a policy against “marketing” and “content marketing” posts, but it should be successful if you write your content with the above guidelines in mind. Even with that, it’s important to post here sparingly.
  * Your own database / tool channel — this is where the people who have opted in to receive communications from you and always a great place to share things that are relevant to them.

* On social media:

  * Twitter

  * LinkedIn

  * Social media posts *from the author* or an individual connected to the project tend to have better engagement than posts from a company or organization account.

  * Ask your partner representative about:

    <!-- -->

    * Retweets and shares from the official dbt Labs accounts.
    * Flagging posts internally at dbt Labs to get individual employees to share.

###### Measuring engagement[​](#measuring-engagement "Direct link to Measuring engagement")

You don’t need 1000 people in a channel to succeed, but you need at least a few active participants who can make it feel lived in. If you’re comfortable working in public, this could be members of your team, or it can be a few people who you know that are highly engaged and would be interested in participating. Having even 2 or 3 regulars hanging out in a channel is all that’s needed for a successful start and is, in fact, much more impactful than 250 people that never post.

##### How to announce a new adapter[​](#how-to-announce-a-new-adapter "Direct link to How to announce a new adapter")

We’d recommend *against* boilerplate announcements and encourage finding a unique voice. That being said, there are a couple of things that we’d want to include:

* A summary of the value prop of your database / technology for users who aren’t familiar.

* The personas that might be interested in this news.

* A description of what the adapter *is*. For example:

  <!-- -->

  > With the release of our new dbt adapter, you’ll be able to to use dbt to model and transform your data in \[name-of-your-org]

* Particular or unique use cases or functionality unlocked by the adapter.

* Plans for future / ongoing support / development.

* The link to the documentation for using the adapter on the dbt Labs docs site.

* An announcement blog.

###### Announcing new release versions of existing adapters[​](#announcing-new-release-versions-of-existing-adapters "Direct link to Announcing new release versions of existing adapters")

This can vary substantially depending on the nature of the release but a good baseline is the types of release messages that [we put out in the #dbt-releases](https://getdbt.slack.com/archives/C37J8BQEL/p1651242161526509) channel.

![Full Release Post](/assets/images/0-full-release-notes-1cc8cb263cb178df48deda1f69875c99.png)

Breaking this down:

* Visually distinctive announcement - make it clear this is a release
  <!-- -->
  [![title](/img/adapter-guide/1-announcement.png?v=2 "title")](#)title
* Short written description of what is in the release
  <!-- -->
  [![description](/img/adapter-guide/2-short-description.png?v=2 "description")](#)description
* Links to additional resources
  <!-- -->
  [![more resources](/img/adapter-guide/3-additional-resources.png?v=2 "more resources")](#)more resources
* Implementation instructions:
  <!-- -->
  [![more installation](/img/adapter-guide/4-installation.png?v=2 "more installation")](#)more installation
* Contributor recognition (if applicable)
  <!-- -->
  [![thank yous](/img/adapter-guide/6-thank-contribs.png?v=2 "thank yous")](#)thank yous

#### Build a trusted adapter[​](#build-a-trusted-adapter "Direct link to Build a trusted adapter")

The Trusted Adapter Program exists to allow adapter maintainers to demonstrate to the dbt community that your adapter is trusted to be used in production.

The very first data platform dbt supported was Redshift followed quickly by Postgres ([dbt-core#174](https://github.com/dbt-labs/dbt-core/pull/174)). In 2017, back when dbt Labs (née Fishtown Analytics) was still a data consultancy, we added support for Snowflake and BigQuery. We also turned dbt's database support into an adapter framework ([dbt-core#259](https://github.com/dbt-labs/dbt-core/pull/259/)), and a plugin system a few years later. For years, dbt Labs specialized in those four data platforms and became experts in them. However, the surface area of all possible databases, their respective nuances, and keeping them up-to-date and bug-free is a Herculean and/or Sisyphean task that couldn't be done by a single person or even a single team! Enter the dbt community which enables dbt Core to work on more than 30 different databases (32 as of Sep '22)!

Free and open-source tools for the data professional are increasingly abundant. This is by-and-large a *good thing*, however it requires due dilligence that wasn't required in a paid-license, closed-source software world. Before taking a dependency on an open-source projet is is important to determine the answer to the following questions:

1. Does it work?
2. Does it meet my team's specific use case?
3. Does anyone "own" the code, or is anyone liable for ensuring it works?
4. Do bugs get fixed quickly?
5. Does it stay up-to-date with new Core features?
6. Is the usage substantial enough to self-sustain?
7. What risks do I take on by taking a dependency on this library?

These are valid, important questions to answer—especially given that `dbt-core` itself only put out its first stable release (major version v1.0) in December 2021! Indeed, up until now, the majority of new user questions in database-specific channels are some form of:

* "How mature is `dbt-<ADAPTER>`? Any gotchas I should be aware of before I start exploring?"
* "has anyone here used `dbt-<ADAPTER>` for production models?"
* "I've been playing with `dbt-<ADAPTER>` -- I was able to install and run my initial experiments. I noticed that there are certain features mentioned on the documentation that are marked as 'not ok' or 'not tested'. What are the risks? I'd love to make a statement on my team to adopt dbt, but I'm pretty sure questions will be asked around the possible limitations of the adapter or if there are other companies out there using dbt with Oracle DB in production, etc."

There has been a tendency to trust the dbt Labs-maintained adapters over community- and vendor-supported adapters, but repo ownership is only one among many indicators of software quality. We aim to help our users feel well-informed as to the caliber of an adapter with a new program.

##### What it means to be trusted[​](#what-it-means-to-be-trusted "Direct link to What it means to be trusted")

By opting into the below, you agree to this, and we take you at your word. dbt Labs reserves the right to remove an adapter from the trusted adapter list at any time, should any of the below guidelines not be met.

##### Feature Completeness[​](#feature-completeness "Direct link to Feature Completeness")

To be considered for the Trusted Adapter Program, the adapter must cover the essential functionality of dbt Core given below, with best effort given to support the entire feature set.

Essential functionality includes (but is not limited to the following features):

* table, view, and seed materializations
* dbt tests

The adapter should have the required documentation for connecting and configuring the adapter. The dbt docs site should be the single source of truth for this information. These docs should be kept up-to-date.

Proceed to the "Document a new adapter" step for more information.

##### Release cadence[​](#release-cadence "Direct link to Release cadence")

Keeping an adapter up-to-date with the latest features of dbt, as defined in [dbt-adapters](https://github.com/dbt-labs/dbt-adapters), is an integral part of being a trusted adapter. We encourage adapter maintainers to keep track of new dbt-adapter releases and support new features relevant to their platform, ensuring users have the best version of dbt.

Before [dbt Core version 1.8](https://docs.getdbt.com/docs/dbt-versions/core-upgrade/upgrading-to-v1.8.md#new-dbt-core-adapter-installation-procedure), adapter versions needed to match the semantic versioning of dbt Core. After v1.8, this is no longer required. This means users can use an adapter on v1.8+ with a different version of dbt Core v1.8+. For example, a user could use dbt-core v1.9 with dbt-postgres v1.8.

##### Community responsiveness[​](#community-responsiveness "Direct link to Community responsiveness")

On a best effort basis, active participation and engagement with the dbt Community across the following forums:

* Being responsive to feedback and supporting user enablement in dbt Community’s Slack workspace
* Responding with comments to issues raised in public dbt adapter code repository
* Merging in code contributions from community members as deemed appropriate

##### Security Practices[​](#security-practices "Direct link to Security Practices")

Trusted adapters will not do any of the following:

* Output to logs or file either access credentials information to or data from the underlying data platform itself.
* Make API calls other than those expressly required for using dbt features (adapters may not add additional logging)
* Obfuscate code and/or functionality so as to avoid detection

Additionally, to avoid supply-chain attacks:

* Use an automated service to keep Python dependencies up-to-date (such as Dependabot or similar),
* Publish directly to PyPI from the dbt adapter code repository by using trusted CI/CD process (such as GitHub actions)
* Restrict admin access to both the respective code (GitHub) and package (PyPI) repositories
* Identify and mitigate security vulnerabilities by use of a static code analyzing tool (such as Snyk) as part of a CI/CD process

##### Other considerations[​](#other-considerations "Direct link to Other considerations")

The adapter repository is:

* open-souce licensed,
* published to PyPI, and
* automatically tests the codebase against dbt Lab's provided adapter test suite

##### How to get an adapter on the trusted list[​](#how-to-get-an-adapter-on-the-trusted-list "Direct link to How to get an adapter on the trusted list")

Open an issue on the [docs.getdbt.com GitHub repository](https://github.com/dbt-labs/docs.getdbt.com) using the "Add adapter to Trusted list" template. In addition to contact information, it will ask confirm that you agree to the following.

1. my adapter meet the guidelines given above
2. I will make best reasonable effort that this continues to be so
3. checkbox: I acknowledge that dbt Labs reserves the right to remove an adapter from the trusted adapter list at any time, should any of the above guidelines not be met.

The approval workflow is as follows:

1. create and populate the template-created issue
2. dbt Labs will respond as quickly as possible (maximally four weeks, though likely faster)
3. If approved, dbt Labs will create and merge a Pull request to formally add the adapter to the list.

##### Getting help for my trusted adapter[​](#getting-help-for-my-trusted-adapter "Direct link to Getting help for my trusted adapter")

Ask your question in #adapter-ecosystem channel of the dbt community Slack.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Building dbt packages

[Back to guides](https://docs.getdbt.com/guides.md)

dbt Core

Advanced

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

Creating packages is an **advanced use of dbt**. If you're new to the tool, we recommend that you first use the product for your own analytics before attempting to create a package for others.

##### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

A strong understanding of:

* [packages](https://docs.getdbt.com/docs/build/packages.md)
* administering a repository on GitHub
* [semantic versioning](https://semver.org/)

##### Assess whether a package is the right solution[​](#assess-whether-a-package-is-the-right-solution "Direct link to Assess whether a package is the right solution")

Packages typically contain either:

* macros that solve a particular analytics engineering problem — for example, [auditing the results of a query](https://hub.getdbt.com/dbt-labs/audit_helper/latest/), [generating code](https://hub.getdbt.com/dbt-labs/codegen/latest/), or [adding additional schema tests to a dbt project](https://hub.getdbt.com/calogica/dbt_expectations/latest/).
* models for a common dataset — for example a dataset for software products like [MailChimp](https://hub.getdbt.com/fivetran/mailchimp/latest/) or [Snowplow](https://hub.getdbt.com/dbt-labs/snowplow/latest/), or even models for metadata about your data stack like [Snowflake query spend](https://hub.getdbt.com/gitlabhq/snowflake_spend/latest/) and [the artifacts produced by `dbt run`](https://hub.getdbt.com/tailsdotcom/dbt_artifacts/latest/). In general, there should be a shared set of industry-standard metrics that you can model (e.g. email open rate).

Packages are *not* a good fit for sharing models that contain business-specific logic, for example, writing code for marketing attribution, or monthly recurring revenue. Instead, consider sharing a blog post and a link to a sample repo, rather than bundling this code as a package (here's our blog post on [marketing attribution](https://blog.getdbt.com/modeling-marketing-attribution/) as an example).

#### Create your new project[​](#create-your-new-project "Direct link to Create your new project")

Using the command line for package development

We tend to use the command line interface for package development. The development workflow often involves installing a local copy of your package in another dbt project — at present dbt is not designed for this workflow.

1. Use the [dbt init](https://docs.getdbt.com/reference/commands/init.md) command to create a new dbt project, which will be your package:
```

---

## select my_model, its children, and the parents of its children

**URL:** llms-txt#select-my_model,-its-children,-and-the-parents-of-its-children

dbt run --select @my_model

---

## Run tests on all seeds, which use the 'seed' materialization

**URL:** llms-txt#run-tests-on-all-seeds,-which-use-the-'seed'-materialization

dbt test --select "config.materialized:seed"

---

## Run all models tagged "daily"

**URL:** llms-txt#run-all-models-tagged-"daily"

dbt run --select tag:daily

---

## Steps derived from these commands won't have their error details shown inline, as they're messy

**URL:** llms-txt#steps-derived-from-these-commands-won't-have-their-error-details-shown-inline,-as-they're-messy

**Contents:**
  - Productionize your dbt Databricks project
  - Quickstart for dbt and Amazon Athena
  - Quickstart for dbt and Azure Synapse Analytics
  - Quickstart for dbt and BigQuery
  - Quickstart for dbt and Databricks
  - Quickstart for dbt and Microsoft Fabric
  - Quickstart for dbt and Redshift
  - Quickstart for dbt and Snowflake
  - Quickstart for dbt and Starburst Galaxy
  - Quickstart for dbt and Teradata

commands_to_skip_logs = ['dbt source', 'dbt docs']
run_id = input_data['run_id']
account_id = input_data['account_id']
url = f'https://YOUR_ACCESS_URL/api/v2/accounts/{account_id}/runs/{run_id}/?include_related=["run_steps"]'
headers = {'Authorization': f'Token {api_token}'}

response = requests.get(url, headers=headers)
response.raise_for_status()
results = response.json()['data']

threaded_errors_post = ""
for step in results['run_steps']:
  show_logs = not any(cmd in step['name'] for cmd in commands_to_skip_logs)
  if not show_logs:
    continue
  if step['status_humanized'] != 'Success':
    full_log = step['logs']
    # Remove timestamp and any colour tags
    full_log = re.sub('\x1b?\[[0-9]+m[0-9:]*', '', full_log)
    
    summary_start = re.search('(?:Completed with \d+ error.* and \d+ warnings?:|Database Error|Compilation Error|Runtime Error)', full_log)
    
    line_items = re.findall('(^.*(?:Failure|Error) in .*\n.*\n.*)', full_log, re.MULTILINE)
    if not summary_start:
      continue
      
    threaded_errors_post += f"""
*{step['name']}*
"""    
    # If there are no line items, the failure wasn't related to dbt nodes, and we want the whole rest of the message. 
    # If there are, then we just want the summary line and then to log out each individual node's error.
    if len(line_items) == 0:
      relevant_log = f''
    else:
      relevant_log = summary_start[0]
      for item in line_items:
        relevant_log += f'\n\n'
    threaded_errors_post += f"""
{relevant_log}
"""

output = {'threaded_errors_post': threaded_errors_post}

CASE
WHEN is_account_group_member('auditors') THEN email
ELSE regexp_extract(email, '^.*@(.*)$', 1)
END

select * from jaffle_shop.customers
     
with customers as (

select
        id as customer_id,
        first_name,
        last_name

from jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       id as customer_id,
       first_name,
       last_name

from jaffle_shop.customers
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from jaffle_shop.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select * from final
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

CREATE TABLE dbo.customers
   (
       [ID] [bigint],
       [FIRST_NAME] [varchar](8000),
       [LAST_NAME] [varchar](8000)
   );

COPY INTO [dbo].[customers]
   FROM 'https://dbtlabsynapsedatalake.blob.core.windows.net/dbt-quickstart-public/jaffle_shop_customers.parquet'
   WITH (
       FILE_TYPE = 'PARQUET'
   );

CREATE TABLE dbo.orders
   (
       [ID] [bigint],
       [USER_ID] [bigint],
       [ORDER_DATE] [date],
       [STATUS] [varchar](8000)
   );

COPY INTO [dbo].[orders]
   FROM 'https://dbtlabsynapsedatalake.blob.core.windows.net/dbt-quickstart-public/jaffle_shop_orders.parquet'
   WITH (
       FILE_TYPE = 'PARQUET'
   );

CREATE TABLE dbo.payments
   (
       [ID] [bigint],
       [ORDERID] [bigint],
       [PAYMENTMETHOD] [varchar](8000),
       [STATUS] [varchar](8000),
       [AMOUNT] [bigint],
       [CREATED] [date]
   );

COPY INTO [dbo].[payments]
   FROM 'https://dbtlabsynapsedatalake.blob.core.windows.net/dbt-quickstart-public/stripe_payments.parquet'
   WITH (
       FILE_TYPE = 'PARQUET'
   );
   
   with customers as (

select
       ID as customer_id,
       FIRST_NAME as first_name,
       LAST_NAME as last_name

from dbo.customers
   ),

select
           ID as order_id,
           USER_ID as customer_id,
           ORDER_DATE as order_date,
           STATUS as status

from dbo.orders
   ),

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

group by customer_id
   ),

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id
   )

select * from final
   
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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       ID as customer_id,
       FIRST_NAME as first_name,
       LAST_NAME as last_name

from dbo.customers
   
   select
       ID as order_id,
       USER_ID as customer_id,
       ORDER_DATE as order_date,
       STATUS as status

from dbo.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id

select * from final
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

select * from `dbt-tutorial.jaffle_shop.customers`;
   select * from `dbt-tutorial.jaffle_shop.orders`;
   select * from `dbt-tutorial.stripe.payment`;
   
     select * from `dbt-tutorial.jaffle_shop.customers`
     
with customers as (

select
        id as customer_id,
        first_name,
        last_name

from `dbt-tutorial`.jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from `dbt-tutorial`.jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       id as customer_id,
       first_name,
       last_name

from `dbt-tutorial`.jaffle_shop.customers
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from `dbt-tutorial`.jaffle_shop.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

sources:
       - name: jaffle_shop
         description: This is a replica of the Postgres database used by our app
         database: dbt-tutorial
         schema: jaffle_shop
         tables:
             - name: customers
               description: One record per customer.
             - name: orders
               description: One record per order. Includes cancelled and deleted orders.
   
   select
       id as customer_id,
       first_name,
       last_name

from {{ source('jaffle_shop', 'customers') }}
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from {{ source('jaffle_shop', 'orders') }}
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

select * from default.jaffle_shop_customers
    select * from default.jaffle_shop_orders
    select * from default.stripe_payments
    
    grant all privileges on schema default to users;
    
     select * from default.jaffle_shop_customers
     
with customers as (

select
        id as customer_id,
        first_name,
        last_name

from jaffle_shop_customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from jaffle_shop_orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       id as customer_id,
       first_name,
       last_name

from jaffle_shop_customers
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from jaffle_shop_orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select * from final
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

DROP TABLE dbo.customers;

CREATE TABLE dbo.customers
   (
       [ID] [int],
       [FIRST_NAME] [varchar](8000),
       [LAST_NAME] [varchar](8000)
   );

COPY INTO [dbo].[customers]
   FROM 'https://dbtlabsynapsedatalake.blob.core.windows.net/dbt-quickstart-public/jaffle_shop_customers.parquet'
   WITH (
       FILE_TYPE = 'PARQUET'
   );

DROP TABLE dbo.orders;

CREATE TABLE dbo.orders
   (
       [ID] [int],
       [USER_ID] [int],
       -- [ORDER_DATE] [int],
       [ORDER_DATE] [date],
       [STATUS] [varchar](8000)
   );

COPY INTO [dbo].[orders]
   FROM 'https://dbtlabsynapsedatalake.blob.core.windows.net/dbt-quickstart-public/jaffle_shop_orders.parquet'
   WITH (
       FILE_TYPE = 'PARQUET'
   );

DROP TABLE dbo.payments;

CREATE TABLE dbo.payments
   (
       [ID] [int],
       [ORDERID] [int],
       [PAYMENTMETHOD] [varchar](8000),
       [STATUS] [varchar](8000),
       [AMOUNT] [int],
       [CREATED] [date]
   );

COPY INTO [dbo].[payments]
   FROM 'https://dbtlabsynapsedatalake.blob.core.windows.net/dbt-quickstart-public/stripe_payments.parquet'
   WITH (
       FILE_TYPE = 'PARQUET'
   );
   
   with customers as (

select
       ID as customer_id,
       FIRST_NAME as first_name,
       LAST_NAME as last_name

from dbo.customers
   ),

select
           ID as order_id,
           USER_ID as customer_id,
           ORDER_DATE as order_date,
           STATUS as status

from dbo.orders
   ),

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

group by customer_id
   ),

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id
   )

select * from final
   
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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       ID as customer_id,
       FIRST_NAME as first_name,
       LAST_NAME as last_name

from dbo.customers
   
   select
       ID as order_id,
       USER_ID as customer_id,
       ORDER_DATE as order_date,
       STATUS as status

from dbo.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id

select * from final
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

create schema if not exists jaffle_shop;
   create schema if not exists stripe;
   
   create table jaffle_shop.customers(
       id integer,
       first_name varchar(50),
       last_name varchar(50)
   );

create table jaffle_shop.orders(
       id integer,
       user_id integer,
       order_date date,
       status varchar(50)
   );

create table stripe.payment(
       id integer,
       orderid integer,
       paymentmethod varchar(50),
       status varchar(50),
       amount integer,
       created date
   );
   
   copy jaffle_shop.customers( id, first_name, last_name)
   from 's3://dbt-data-lake-xxxx/jaffle_shop_customers.csv'
   iam_role 'arn:aws:iam::XXXXXXXXXX:role/RoleName'
   region 'us-east-1'
   delimiter ','
   ignoreheader 1
   acceptinvchars;
      
   copy jaffle_shop.orders(id, user_id, order_date, status)
   from 's3://dbt-data-lake-xxxx/jaffle_shop_orders.csv'
   iam_role 'arn:aws:iam::XXXXXXXXXX:role/RoleName'
   region 'us-east-1'
   delimiter ','
   ignoreheader 1
   acceptinvchars;

copy stripe.payment(id, orderid, paymentmethod, status, amount, created)
   from 's3://dbt-data-lake-xxxx/stripe_payments.csv'
   iam_role 'arn:aws:iam::XXXXXXXXXX:role/RoleName'
   region 'us-east-1'
   delimiter ','
   ignoreheader 1
   Acceptinvchars;
   
   select * from jaffle_shop.customers;
   select * from jaffle_shop.orders;
   select * from stripe.payment;
   
     select * from jaffle_shop.customers
     
with customers as (

select
        id as customer_id,
        first_name,
        last_name

from jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       id as customer_id,
       first_name,
       last_name

from jaffle_shop.customers
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from jaffle_shop.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select * from final
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

create warehouse transforming;
   create database raw;
   create database analytics;
   create schema raw.jaffle_shop;
   create schema raw.stripe;
   
     create table raw.jaffle_shop.customers 
     ( id integer,
       first_name varchar,
       last_name varchar
     );
     
     copy into raw.jaffle_shop.customers (id, first_name, last_name)
     from 's3://dbt-tutorial-public/jaffle_shop_customers.csv'
     file_format = (
         type = 'CSV'
         field_delimiter = ','
         skip_header = 1
         ); 
     
     create table raw.jaffle_shop.orders
     ( id integer,
       user_id integer,
       order_date date,
       status varchar,
       _etl_loaded_at timestamp default current_timestamp
     );
     
     copy into raw.jaffle_shop.orders (id, user_id, order_date, status)
     from 's3://dbt-tutorial-public/jaffle_shop_orders.csv'
     file_format = (
         type = 'CSV'
         field_delimiter = ','
         skip_header = 1
         );
     
     create table raw.stripe.payment 
     ( id integer,
       orderid integer,
       paymentmethod varchar,
       status varchar,
       amount integer,
       created date,
       _batched_at timestamp default current_timestamp
     );
     
     copy into raw.stripe.payment (id, orderid, paymentmethod, status, amount, created)
     from 's3://dbt-tutorial-public/stripe_payments.csv'
     file_format = (
         type = 'CSV'
         field_delimiter = ','
         skip_header = 1
         );
     
   select * from raw.jaffle_shop.customers;
   select * from raw.jaffle_shop.orders;
   select * from raw.stripe.payment;   
   
     select * from raw.jaffle_shop.customers
     
grant all on database raw to role snowflake_role_name;
grant all on database analytics to role snowflake_role_name;

grant all on schema raw.jaffle_shop to role snowflake_role_name;
grant all on schema raw.stripe to role snowflake_role_name;

grant all on all tables in database raw to role snowflake_role_name;
grant all on future tables in database raw to role snowflake_role_name;

select
        id as customer_id,
        first_name,
        last_name

from raw.jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from raw.jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       id as customer_id,
       first_name,
       last_name

from raw.jaffle_shop.customers
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from raw.jaffle_shop.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select * from final
   
$ dbt run --select customers

sources:
       - name: jaffle_shop
         description: This is a replica of the Postgres database used by our app
         database: raw
         schema: jaffle_shop
         tables:
             - name: customers
               description: One record per customer.
             - name: orders
               description: One record per order. Includes cancelled and deleted orders.
   
   select
       id as customer_id,
       first_name,
       last_name

from {{ source('jaffle_shop', 'customers') }}
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from {{ source('jaffle_shop', 'orders') }}
   
   version: 2

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

<bucket/blob>
       dbt-quickstart (folder)
           jaffle-shop-customers (folder)
               jaffle_shop_customers.csv (file)
           jaffle-shop-orders (folder)
               jaffle_shop_orders.csv (file)
           stripe-payments (folder)
               stripe-payments.csv (file)
   
   CREATE SCHEMA jaffle_shop WITH (location='s3://YOUR_S3_BUCKET_NAME/dbt-quickstart/');

CREATE TABLE jaffle_shop.jaffle_shop_customers (
       id VARCHAR,
       first_name VARCHAR,
       last_name VARCHAR
   )

WITH (
       external_location = 's3://YOUR_S3_BUCKET_NAME/dbt-quickstart/jaffle-shop-customers/',
       format = 'csv',
       type = 'hive',
       skip_header_line_count=1

CREATE TABLE jaffle_shop.jaffle_shop_orders (

id VARCHAR,
       user_id VARCHAR,
       order_date VARCHAR,
       status VARCHAR

WITH (
       external_location = 's3://YOUR_S3_BUCKET_NAME/dbt-quickstart/jaffle-shop-orders/',
       format = 'csv',
       type = 'hive',
       skip_header_line_count=1
   );

CREATE TABLE jaffle_shop.stripe_payments (

id VARCHAR,
       order_id VARCHAR,
       paymentmethod VARCHAR,
       status VARCHAR,
       amount VARCHAR,
       created VARCHAR
   )

external_location = 's3://YOUR_S3_BUCKET_NAME/dbt-quickstart/stripe-payments/',
       format = 'csv',
       type = 'hive',
       skip_header_line_count=1

);
   
   select * from jaffle_shop.jaffle_shop_customers;
   select * from jaffle_shop.jaffle_shop_orders;
   select * from jaffle_shop.stripe_payments;
   
         select * from dbt_quickstart.jaffle_shop.jaffle_shop_customers
     
with customers as (

select
        id as customer_id,
        first_name,
        last_name

from dbt_quickstart.jaffle_shop.jaffle_shop_customers
),

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from dbt_quickstart.jaffle_shop.jaffle_shop_orders
),

select
        customer_id,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

from orders
    group by 1
),

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

from customers
    left join customer_orders on customers.customer_id = customer_orders.customer_id
)
select * from final

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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
   select
       id as customer_id,
       first_name,
       last_name

from dbt_quickstart.jaffle_shop.jaffle_shop_customers
   
   select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from dbt_quickstart.jaffle_shop.jaffle_shop_orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
           customer_id,

min(order_date) as first_order_date,
           max(order_date) as most_recent_order_date,
           count(order_id) as number_of_orders

select
           customers.customer_id,
           customers.first_name,
           customers.last_name,
           customer_orders.first_order_date,
           customer_orders.most_recent_order_date,
           coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id

select * from final
   
$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

%connect local
   
   CREATE DATABASE jaffle_shop AS PERM = 1e9;
   
   CREATE FOREIGN TABLE jaffle_shop.customers (
       id integer,
       first_name varchar (100),
       last_name varchar (100),
       email varchar (100)
   )
   USING (
       LOCATION ('/gs/storage.googleapis.com/clearscape_analytics_demo_data/dbt/raw_customers.csv')
   )
   NO PRIMARY INDEX;

CREATE FOREIGN TABLE jaffle_shop.orders (
       id integer,
       user_id integer,
       order_date date,
       status varchar(100)
   )
   USING (
       LOCATION ('/gs/storage.googleapis.com/clearscape_analytics_demo_data/dbt/raw_orders.csv')
   )
   NO PRIMARY INDEX;

CREATE FOREIGN TABLE jaffle_shop.payments (
       id integer,
       orderid integer,
       paymentmethod varchar (100),
       amount integer
   )
   USING (
       LOCATION ('/gs/storage.googleapis.com/clearscape_analytics_demo_data/dbt/raw_payments.csv')
   )
   NO PRIMARY INDEX;
   
   # before
   models:
     my_new_project:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     my_new_project:
       +materialized: table

select
       id as customer_id,
       first_name,
       last_name

from jaffle_shop.customers

select
       id as order_id,
       user_id as customer_id,
       order_date,
       status

from jaffle_shop.orders

select
       customer_id,

min(order_date) as first_order_date,
       max(order_date) as most_recent_order_date,
       count(order_id) as number_of_orders

select
       customers.customer_id,
       customers.first_name,
       customers.last_name,
       customer_orders.first_order_date,
       customer_orders.most_recent_order_date,
       coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   select
      id as customer_id,
      first_name,
      last_name

from jaffle_shop.customers
   
   select
      id as order_id,
      user_id as customer_id,
      order_date,
      status

from jaffle_shop.orders
   
   with customers as (

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
          customer_id,

min(order_date) as first_order_date,
          max(order_date) as most_recent_order_date,
          count(order_id) as number_of_orders

select
          customers.customer_id,
          customers.first_name,
          customers.last_name,
          customer_orders.first_order_date,
          customer_orders.most_recent_order_date,
          coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders on customers.customer_id = customer_orders.customer_id

select * from final
   
$ dbt run --select customers

sources:
      - name: jaffle_shop
        description: This is a replica of the Postgres database used by the app
        database: raw
        schema: jaffle_shop
        tables:
            - name: customers
              description: One record per customer.
            - name: orders
              description: One record per order. Includes canceled and deleted orders.
   
   select
      id as customer_id,
      first_name,
      last_name

from {{ source('jaffle_shop', 'customers') }}
   
   select
      id as order_id,
      user_id as customer_id,
      order_date,
      status

from {{ source('jaffle_shop', 'orders') }}
   
   version: 2

models:
     - name: bi_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: bi_customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

$ pwd
> Users/BBaggins/dbt-tutorial/jaffle_shop

name: jaffle_shop # Change from the default, `my_new_project`

profile: jaffle_shop # Change from the default profile name, `default`

models:
    jaffle_shop: # Change from `my_new_project` to match the previous value for `name:`
    ...

jaffle_shop: # this needs to match the profile in your dbt_project.yml file
    target: dev
    outputs:
        dev:
            type: bigquery
            method: service-account
            keyfile: /Users/BBaggins/.dbt/dbt-tutorial-project-331118.json # replace this with the full path to your keyfile
            project: grand-highway-265418 # Replace this with your project id
            dataset: dbt_bbagins # Replace this with dbt_your_name, e.g. dbt_bilbo
            threads: 1
            timeout_seconds: 300
            location: US
            priority: interactive

$ dbt debug
> Connection test: OK connection ok

git init
git branch -M main
git add .
git commit -m "Create a dbt project"
git remote add origin https://github.com/USERNAME/dbt-tutorial.git
git push -u origin main

$ git checkout -b add-customers-model
>  Switched to a new branch `add-customer-model`

select
        id as customer_id,
        first_name,
        last_name

from `dbt-tutorial`.jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from `dbt-tutorial`.jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select
        id as customer_id,
        first_name,
        last_name

from jaffle_shop_customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from jaffle_shop_orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select
        id as customer_id,
        first_name,
        last_name

from jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

select
        id as customer_id,
        first_name,
        last_name

from raw.jaffle_shop.customers

select
        id as order_id,
        user_id as customer_id,
        order_date,
        status

from raw.jaffle_shop.orders

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

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

name: 'jaffle_shop'
     
     models:
       jaffle_shop:
         +materialized: table
         example:
           +materialized: view
     
   {{
     config(
       materialized='view'
     )
   }}

select
           id as customer_id
           ...

)
   
   # before
   models:
     jaffle_shop:
       +materialized: table
       example:
         +materialized: view
   
   # after
   models:
     jaffle_shop:
       +materialized: table
   
select
    id as customer_id,
    first_name,
    last_name

from `dbt-tutorial`.jaffle_shop.customers

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from `dbt-tutorial`.jaffle_shop.orders

select
    id as customer_id,
    first_name,
    last_name

from jaffle_shop_customers

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from jaffle_shop_orders

select
    id as customer_id,
    first_name,
    last_name

from jaffle_shop.customers

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from jaffle_shop.orders

select
    id as customer_id,
    first_name,
    last_name

from raw.jaffle_shop.customers

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from raw.jaffle_shop.orders

select * from {{ ref('stg_customers') }}

select * from {{ ref('stg_orders') }}

select
        customer_id,

min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        count(order_id) as number_of_orders

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order_date,
        customer_orders.most_recent_order_date,
        coalesce(customer_orders.number_of_orders, 0) as number_of_orders

left join customer_orders using (customer_id)

$ dbt run --select customers

models:
     - name: customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_customers
       columns:
         - name: customer_id
           data_tests:
             - unique
             - not_null

- name: stg_orders
       columns:
         - name: order_id
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
dbt test --select customers

models:
     - name: customers
       description: One record per customer
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: first_order_date
           description: NULL when a customer has not yet placed an order.

- name: stg_customers
       description: This model cleans up customer data
       columns:
         - name: customer_id
           description: Primary key
           data_tests:
             - unique
             - not_null

- name: stg_orders
       description: This model cleans up order data
       columns:
         - name: order_id
           description: Primary key
           data_tests:
             - unique
             - not_null
         - name: status
           data_tests:
             - accepted_values:
                 arguments: # available in v1.10.5 and higher. Older versions can set the <argument_name> as the top-level property.
                   values: ['placed', 'shipped', 'completed', 'return_pending', 'returned']
         - name: customer_id
           data_tests:
             - not_null
             - relationships:
                 arguments:
                   to: ref('stg_customers')
                   field: customer_id
   
  version: 2

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

/my_dbt_project/
├── dbt_project.yml
├── models/
│   ├── my_model.sql
├── tests/
│   ├── my_test.sql
└── requirements.txt

git clone https://github.com/dbt-labs/jaffle_shop_duckdb.git

cd jaffle_shop_duckdb

python3 -m venv venv
   source venv/bin/activate
   python3 -m pip install --upgrade pip
   python3 -m pip install -r requirements.txt
   source venv/bin/activate

python -m venv venv
   venv\Scripts\activate.bat
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   venv\Scripts\activate.bat

python -m venv venv
   venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   venv\Scripts\Activate.ps1

(venv) ➜  jaffle_shop_duckdb git:(duckdb) dbt build
15:10:12  Running with dbt=1.8.1
15:10:13  Registered adapter: duckdb=1.8.1
15:10:13  Found 5 models, 3 seeds, 20 data tests, 416 macros
15:10:13  
15:10:14  Concurrency: 24 threads (target='dev')
15:10:14  
15:10:14  1 of 28 START seed file main.raw_customers ..................................... [RUN]
15:10:14  2 of 28 START seed file main.raw_orders ........................................ [RUN]
15:10:14  3 of 28 START seed file main.raw_payments ...................................... [RUN]
....

15:10:15  27 of 28 PASS relationships_orders_customer_id__customer_id__ref_customers_ .... [PASS in 0.32s]
15:10:15  
15:10:15  Finished running 3 seeds, 3 view models, 20 data tests, 2 table models in 0 hours 0 minutes and 1.52 seconds (1.52s).
15:10:15  
15:10:15  Completed successfully
15:10:15  
15:10:15  Done. PASS=28 WARN=0 ERROR=0 SKIP=0 TOTAL=28

IO Error: Could not set lock on file "jaffle_shop.duckdb": Resource temporarily unavailable

/workspaces/test (main) $ dbt build
   
   python -m pip install jafgen
   
   jafgen [number of years to generate] # e.g. jafgen 6
   
git add 
git commit -m "Your commit message"
git push

curl -fsSL https://public.cdn.getdbt.com/fs/install/install.sh | sh -s -- --update
   
   exec $SHELL
   
   irm https://public.cdn.getdbt.com/fs/install/install.ps1 | iex
   
   Start-Process powershell
   
   dbtf --version
   
   dbt-fusion 2.0.0-preview.45
   
     dbtf init --skip-profile-setup
     
   cd jaffle_shop
   
   dbtf build
   
       models/marts/orders.sql
   
mkdir ~/.dbt # macOS
mkdir %USERPROFILE%\.dbt # Windows

mv ~/Downloads/dbt_cloud.yml ~/.dbt/dbt_cloud.yml

move %USERPROFILE%\Downloads\dbt_cloud.yml %USERPROFILE%\.dbt\dbt_cloud.yml

dbt-cloud:
project-id: 12345 # Required

create warehouse transforming;
   create database raw;
   create database analytics;
   create schema raw.jaffle_shop;
   create schema raw.stripe;
   
     create table raw.jaffle_shop.customers 
     ( id integer,
       first_name varchar,
       last_name varchar
     );
     
     copy into raw.jaffle_shop.customers (id, first_name, last_name)
     from 's3://dbt-tutorial-public/jaffle_shop_customers.csv'
     file_format = (
         type = 'CSV'
         field_delimiter = ','
         skip_header = 1
         ); 
     
     create table raw.jaffle_shop.orders
     ( id integer,
       user_id integer,
       order_date date,
       status varchar,
       _etl_loaded_at timestamp default current_timestamp
     );
     
     copy into raw.jaffle_shop.orders (id, user_id, order_date, status)
     from 's3://dbt-tutorial-public/jaffle_shop_orders.csv'
     file_format = (
         type = 'CSV'
         field_delimiter = ','
         skip_header = 1
         );
     
     create table raw.stripe.payment 
     ( id integer,
       orderid integer,
       paymentmethod varchar,
       status varchar,
       amount integer,
       created date,
       _batched_at timestamp default current_timestamp
     );
     
     copy into raw.stripe.payment (id, orderid, paymentmethod, status, amount, created)
     from 's3://dbt-tutorial-public/stripe_payments.csv'
     file_format = (
         type = 'CSV'
         field_delimiter = ','
         skip_header = 1
         );
     
   select * from raw.jaffle_shop.customers;
   select * from raw.jaffle_shop.orders;
   select * from raw.stripe.payment;   
   
     select * from raw.jaffle_shop.customers

sources:
 - name: jaffle_shop
   database: raw
   schema: jaffle_shop
   tables:
     - name: customers
     - name: orders

sources:
 - name: stripe
   database: raw
   schema: stripe
   tables:
     - name: payment

select
   id as customer_id,
   first_name,
   last_name
from {{ source('jaffle_shop', 'customers') }}

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status
  from {{ source('jaffle_shop', 'orders') }}

select
   id as payment_id,
   orderid as order_id,
   paymentmethod as payment_method,
   status,
   -- amount is stored in cents, convert it to dollars
   amount / 100 as amount,
   created as created_at

from {{ source('stripe', 'payment') }}

with orders as  (
   select * from {{ ref('stg_orders' )}}
),

payments as (
   select * from {{ ref('stg_payments') }}
),

order_payments as (
   select
       order_id,
       sum(case when status = 'success' then amount end) as amount

from payments
   group by 1
),

select
       orders.order_id,
       orders.customer_id,
       orders.order_date,
       coalesce(order_payments.amount, 0) as amount

from orders
   left join order_payments using (order_id)
)

with customers as (
   select * from {{ ref('stg_customers')}}
),
orders as (
   select * from {{ ref('fct_orders')}}
),
customer_orders as (
   select
       customer_id,
       min(order_date) as first_order_date,
       max(order_date) as most_recent_order_date,
       count(order_id) as number_of_orders,
       sum(amount) as lifetime_value
   from orders
   group by 1
),
final as (
   select
       customers.customer_id,
       customers.first_name,
       customers.last_name,
       customer_orders.first_order_date,
       customer_orders.most_recent_order_date,
       coalesce(customer_orders.number_of_orders, 0) as number_of_orders,
       customer_orders.lifetime_value
   from customers
   left join customer_orders using (customer_id)
)
select * from final

packages:
 - package: dbt-labs/dbt_utils
   version: 1.1.1

{{
   config(
       materialized = 'table',
   )
}}
with days as (
   {{
       dbt_utils.date_spine(
           'day',
           "to_date('01/01/2000','mm/dd/yyyy')",
           "to_date('01/01/2027','mm/dd/yyyy')"
       )
   }}
),
final as (
   select cast(date_day as date) as date_day
   from days
)
select * from final

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    description: |
      Order fact table. This table’s grain is one row per order.
    model: ref('fct_orders')

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    description: |
      Order fact table. This table’s grain is one row per order.
    model: ref('fct_orders')
    # Newly added
    entities: 
      - name: order_id
        type: primary
      - name: customer
        expr: customer_id
        type: foreign

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    description: |
      Order fact table. This table’s grain is one row per order.
    model: ref('fct_orders')
    entities:
      - name: order_id
        type: primary
      - name: customer
        expr: customer_id
        type: foreign
    # Newly added
    dimensions:   
      - name: order_date
        type: time
        type_params:
          time_granularity: day

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    description: |
      Order fact table. This table’s grain is one row per order.
    model: ref('fct_orders')
    entities:
      - name: order_id
        type: primary
      - name: customer
        expr: customer_id
        type: foreign
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
    # Newly added      
    measures:   
      - name: order_total
        description: The total amount for each order including taxes.
        agg: sum
        expr: amount
      - name: order_count
        expr: 1
        agg: sum
      - name: customers_with_orders
        description: Distinct count of customers placing orders
        agg: count_distinct
        expr: customer_id
      - name: order_value_p99 ## The 99th percentile order value
        expr: amount
        agg: percentile
        agg_params:
          percentile: 0.99
          use_discrete_percentile: True
          use_approximate_percentile: False

semantic_models:
  - name: orders
    defaults:
      agg_time_dimension: order_date
    description: |
      Order fact table. This table’s grain is one row per order
    model: ref('fct_orders')
    entities:
      - name: order_id
        type: primary
      - name: customer
        expr: customer_id
        type: foreign
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: order_total
        description: The total amount for each order including taxes.
        agg: sum
        expr: amount
      - name: order_count
        expr: 1
        agg: sum
      - name: customers_with_orders
        description: Distinct count of customers placing orders
        agg: count_distinct
        expr: customer_id
      - name: order_value_p99
        expr: amount
        agg: percentile
        agg_params:
          percentile: 0.99
          use_discrete_percentile: True
          use_approximate_percentile: False

**Examples:**

Example 1 (unknown):
```unknown
##### 7. Add Slack action in Zapier[​](#7-add-slack-action-in-zapier "Direct link to 7. Add Slack action in Zapier")

Add a **Send Channel Message in Slack** action. In the **Action** section, set the channel to **1. Channel Id**, which is the channel that the triggering message was posted in.

Set the **Message Text** to **5. Threaded Errors Post** from the Run Python step. Set the **Thread** value to **1. Ts**, which is the timestamp of the triggering Slack post. This tells Zapier to add this post as a threaded reply to the main message, which prevents the full (potentially long) output from cluttering your channel.

![Screenshot of the Zapier UI, showing the mappings of prior steps to a Slack message](/assets/images/thread-slack-config-alternate-36df7dedc6e8e5688edd5bfe1439ef2c.png)

##### 8. Test and deploy[​](#8-test-and-deploy "Direct link to 8. Test and deploy")

When you're done testing your Zap, publish it.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Productionize your dbt Databricks project

[Back to guides](https://docs.getdbt.com/guides.md)

Databricks

dbt Core

dbt platform

Intermediate

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

Welcome to the third installment of our comprehensive series on optimizing and deploying your data pipelines using Databricks and dbt. In this guide, we'll dive into delivering these models to end users while incorporating best practices to ensure that your production data remains reliable and timely.

##### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

If you don't have any of the following requirements, refer to the instructions in the [Set up your dbt project with Databricks](https://docs.getdbt.com/guides/set-up-your-databricks-dbt-project.md) for help meeting these requirements:

* You have [Set up your dbt project with Databricks](https://docs.getdbt.com/guides/set-up-your-databricks-dbt-project.md).
* You have [optimized your dbt models for peak performance](https://docs.getdbt.com/guides/optimize-dbt-models-on-databricks.md).
* You have created two catalogs in Databricks: *dev* and *prod*.
* You have created Databricks Service Principal to run your production jobs.
* You have at least one [deployment environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md) in dbt.

To get started, let's revisit the deployment environment created for your production data.

##### Deployment environments[​](#deployment-environments "Direct link to Deployment environments")

In software engineering, environments play a crucial role in allowing engineers to develop and test code without affecting the end users of their software. Similarly, you can design [data lakehouses](https://www.databricks.com/product/data-lakehouse) with separate environments. The *production* environment includes the relations (schemas, tables, and views) that end users query or use, typically in a BI tool or ML model.

In dbt, [environments](https://docs.getdbt.com/docs/dbt-cloud-environments.md) come in two flavors:

* Deployment — Defines the settings used for executing jobs created within that environment.
* Development — Determine the settings used in the Studio IDE for a particular dbt project.

Each dbt project can have multiple deployment environments, but only one development environment per user.

#### Create and schedule a production job[​](#create-and-schedule-a-production-job "Direct link to Create and schedule a production job")

With your deployment environment set up, it's time to create a production job to run in your *prod* environment.

To deploy our data transformation workflows, we will utilize [dbt’s built-in job scheduler](https://docs.getdbt.com/docs/deploy/deploy-jobs.md). The job scheduler is designed specifically to streamline your dbt project deployments and runs, ensuring that your data pipelines are easy to create, monitor, and modify efficiently.

Leveraging dbt's job scheduler allows data teams to own the entire transformation workflow. You don't need to learn and maintain additional tools for orchestration or rely on another team to schedule code written by your team. This end-to-end ownership simplifies the deployment process and accelerates the delivery of new data products.

Let’s [create a job](https://docs.getdbt.com/docs/deploy/deploy-jobs.md#create-and-schedule-jobs) in dbt that will transform data in our Databricks *prod* catalog.

1. Create a new job by clicking **Deploy** in the header, click **Jobs** and then **Create job**.

2. **Name** the job “Daily refresh”.

3. Set the **Environment** to your *production* environment.
   <!-- -->
   * This will allow the job to inherit the catalog, schema, credentials, and environment variables defined in [Set up your dbt project with Databricks](https://docs.getdbt.com/guides/set-up-your-databricks-dbt-project.md).

4. Under **Execution Settings**

   * Check the **Generate docs on run** checkbox to configure the job to automatically generate project docs each time this job runs. This will ensure your documentation stays evergreen as models are added and modified.
   * Select the **Run on source freshness** checkbox to configure dbt [source freshness](https://docs.getdbt.com/docs/deploy/source-freshness.md) as the first step of this job. Your sources will need to be configured to [snapshot freshness information](https://docs.getdbt.com/docs/build/sources.md#source-data-freshness) for this to drive meaningful insights.

   <!-- -->

   Add the following three **Commands:**

   * `dbt source freshness`
     * This will check if any sources are stale. We don’t want to recompute models with data that hasn’t changed since our last run.

   * `dbt test --models source:*`
     * This will test the data quality our source data, such as checking making sure ID fields are unique and not null. We don’t want bad data getting into production models.

   * `dbt build --exclude source:* --fail-fast`

     * dbt build is more efficient than issuing separate commands for dbt run and dbt test separately because it will run then test each model before continuing.
     * We are excluding source data because we already tested it in step 2.
     * The fail-fast flag will make dbt exit immediately if a single resource fails to build. If other models are in-progress when the first model fails, then dbt will terminate the connections for these still-running models.

5. Under **Triggers**, use the toggle to configure your job to [run on a schedule](https://docs.getdbt.com/docs/deploy/deploy-jobs.md#schedule-days). You can enter specific days and timing or create a custom cron schedule.
   <!-- -->
   * If you want your dbt job scheduled by another orchestrator, like Databricks Workflows, see the [Advanced Considerations](#advanced-considerations) section below.

This is just one example of an all-or-nothing command list designed to minimize wasted computing. The [job command list](https://docs.getdbt.com/docs/deploy/job-commands.md) and [selectors](https://docs.getdbt.com/reference/node-selection/syntax.md) provide a lot of flexibility on how your DAG will execute. You may want to design yours to continue running certain models if others fail. You may want to set up multiple jobs to refresh models at different frequencies. See our [Job Creation Best Practices discourse](https://discourse.getdbt.com/t/job-creation-best-practices-in-dbt-cloud-feat-my-moms-lasagna/2980) for more job design suggestions.

After your job is set up and runs successfully, configure your **[project artifacts](https://docs.getdbt.com/docs/deploy/artifacts.md)** to make this job inform your production docs site and data sources dashboard that can be reached from the UI.

This will be our main production job to refresh data that will be used by end users. Another job everyone should include in their dbt project is a continuous integration job.

#### Add a CI job[​](#add-a-ci-job "Direct link to Add a CI job")

CI/CD, or Continuous Integration and Continuous Deployment/Delivery, has become a standard practice in software development for rapidly delivering new features and bug fixes while maintaining high quality and stability. dbt enables you to apply these practices to your data transformations.

The steps below show how to create a CI test for your dbt project. CD in dbt requires no additional steps, as your jobs will automatically pick up the latest changes from the branch assigned to the environment your job is running in. You may choose to add steps depending on your deployment strategy. If you want to dive deeper into CD options, check out [this blog on adopting CI/CD with dbt](https://www.getdbt.com/blog/adopting-ci-cd-with-dbt-cloud/).

dbt allows you to write [data tests](https://docs.getdbt.com/docs/build/data-tests.md) for your data pipeline, which can be run at every step of the process to ensure the stability and correctness of your data transformations. The main places you’ll use your dbt tests are:

1. **Daily runs:** Regularly running tests on your data pipeline helps catch issues caused by bad source data, ensuring the quality of data that reaches your users.
2. **Development**: Running tests during development ensures that your code changes do not break existing assumptions, enabling developers to iterate faster by catching problems immediately after writing code.
3. **CI checks**: Automated CI jobs run and test your pipeline end-to end when a pull request is created, providing confidence to developers, code reviewers, and end users that the proposed changes are reliable and will not cause disruptions or data quality issues

Your CI job will ensure that the models build properly and pass any tests applied to them. We recommend creating a separate *test* environment and having a dedicated service principal. This will ensure the temporary schemas created during CI tests are in their own catalog and cannot unintentionally expose data to other users. Repeat the steps in [Set up your dbt project with Databricks](https://docs.getdbt.com/guides/set-up-your-databricks-dbt-project.md) to create your *prod* environment to create a *test* environment. After setup, you should have:

* A catalog called *test*
* A service principal called *dbt\_test\_sp*
* A new dbt environment called *test* that defaults to the *test* catalog and uses the *dbt\_test\_sp* token in the deployment credentials

We recommend setting up a dbt CI job. This will decrease the job’s runtime by running and testing only modified models, which also reduces compute spend on the lakehouse. To create a CI job, refer to [Set up CI jobs](https://docs.getdbt.com/docs/deploy/ci-jobs.md) for details.

With dbt tests and SlimCI, you can feel confident that your production data will be timely and accurate even while delivering at high velocity.

#### Monitor your jobs[​](#monitor-your-jobs "Direct link to Monitor your jobs")

Keeping a close eye on your dbt jobs is crucial for maintaining a robust and efficient data pipeline. By monitoring job performance and quickly identifying potential issues, you can ensure that your data transformations run smoothly. dbt provides three entry points to monitor the health of your project: run history, deployment monitor, and status tiles.

The [run history](https://docs.getdbt.com/docs/deploy/run-visibility.md#run-history) dashboard in dbt provides a detailed view of all your project's job runs, offering various filters to help you focus on specific aspects. This is an excellent tool for developers who want to check recent runs, verify overnight results, or track the progress of running jobs. To access it, select **Run History** from the **Deploy** menu.

The deployment monitor in dbt offers a higher-level view of your run history, enabling you to gauge the health of your data pipeline over an extended period of time. This feature includes information on run durations and success rates, allowing you to identify trends in job performance, such as increasing run times or more frequent failures. The deployment monitor also highlights jobs in progress, queued, and recent failures. To access the deployment monitor click on the dbt logo in the top left corner of the dbt UI.

[![The Deployment Monitor Shows Job Status Over Time Across Environments](/img/guides/databricks-guides/deployment_monitor_dbx.png?v=2 "The Deployment Monitor Shows Job Status Over Time Across Environments")](#)The Deployment Monitor Shows Job Status Over Time Across Environments

By adding [data health tiles](https://docs.getdbt.com/docs/explore/data-tile.md) to your BI dashboards, you can give stakeholders visibility into the health of your data pipeline without leaving their preferred interface. Data tiles instill confidence in your data and help prevent unnecessary inquiries or context switching. To implement dashboard status tiles, you'll need to have dbt docs with [exposures](https://docs.getdbt.com/docs/build/exposures.md) defined.

#### Set up notifications[​](#set-up-notifications "Direct link to Set up notifications")

Setting up [notifications](https://docs.getdbt.com/docs/deploy/job-notifications.md) in dbt allows you to receive alerts via email or a Slack channel whenever a run ends. This ensures that the appropriate teams are notified and can take action promptly when jobs fail or are canceled. To set up notifications:

1. Navigate to your dbt project settings.
2. Select the **Notifications** tab.
3. Choose the desired notification type (Email or Slack) and configure the relevant settings.

If you require notifications through other means than email or Slack, you can use dbt's outbound [webhooks](https://docs.getdbt.com/docs/deploy/webhooks.md) feature to relay job events to other tools. Webhooks enable you to integrate dbt with a wide range of SaaS applications, extending your pipeline’s automation into other systems.

#### Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

When a disruption occurs in your production pipeline, it's essential to know how to troubleshoot issues effectively to minimize downtime and maintain a high degree of trust with your stakeholders.

The five key steps for troubleshooting dbt issues are:

1. Read the error message: dbt error messages usually indicate the error type and the file where the issue occurred.
2. Inspect the problematic file and look for an immediate fix.
3. Isolate the problem by running one model at a time in the Studio IDE or undoing the code that caused the issue.
4. Check for problems in compiled files and logs.

Consult the [Debugging errors documentation](https://docs.getdbt.com/guides/debug-errors.md) for a comprehensive list of error types and diagnostic methods.

To troubleshoot issues with a dbt job, navigate to the "Deploy > Run History" tab in your dbt project and select the failed run. Then, expand the run steps to view [console and debug logs](https://docs.getdbt.com/docs/deploy/run-visibility.md#access-logs) to review the detailed log messages. To obtain additional information, open the Artifacts tab and download the compiled files associated with the run.

If your jobs are taking longer than expected, use the [model timing](https://docs.getdbt.com/docs/deploy/run-visibility.md#model-timing) dashboard to identify bottlenecks in your pipeline. Analyzing the time taken for each model execution helps you pinpoint the slowest components and optimize them for better performance. The Databricks [Query History](https://docs.databricks.com/sql/admin/query-history.html) lets you inspect granular details such as time spent in each task, rows returned, I/O performance, and execution plan.

For more on performance tuning, see our guide on [How to Optimize and Troubleshoot dbt Models on Databricks](https://docs.getdbt.com/guides/optimize-dbt-models-on-databricks.md).

#### Advanced considerations[​](#advanced-considerations "Direct link to Advanced considerations")

As you become more experienced with dbt and Databricks, you might want to explore advanced techniques to further enhance your data pipeline and improve the way you manage your data transformations. The topics in this section are not requirements but will help you harden your production environment for greater security, efficiency, and accessibility.

##### Refreshing your data with Databricks Workflows[​](#refreshing-your-data-with-databricks-workflows "Direct link to Refreshing your data with Databricks Workflows")

The dbt job scheduler offers several ways to trigger your jobs. If your dbt transformations are just one step of a larger orchestration workflow, use the dbt API to trigger your job from Databricks Workflows.

This is a common pattern for analytics use cases that want to minimize latency between ingesting bronze data into the lakehouse with a notebook, transforming that data into gold tables with dbt, and refreshing a dashboard. It is also useful for data science teams who use dbt for feature extraction before using the updated feature store to train and register machine learning models with MLflow.

The API enables integration between your dbt jobs and the Databricks workflow, ensuring that your data transformations are effectively managed within the broader context of your data processing pipeline.

Inserting dbt jobs into a Databricks Workflows allows you to chain together external tasks while still leveraging these benefits of dbt:

* UI Context: The dbt UI enables you to define the job within the context of your dbt environments, making it easier to create and manage relevant configs.
* Logs and Run History: Accessing logs and run history becomes more convenient when using dbt.
* Monitoring and Notification Features: dbt comes equipped with monitoring and notification features like the ones described above that can help you stay informed about the status and performance of your jobs.

To trigger your dbt job from Databricks, follow the instructions in our [Databricks Workflows to run dbt jobs guide](https://docs.getdbt.com/guides/how-to-use-databricks-workflows-to-run-dbt-cloud-jobs.md).

#### Data masking[​](#data-masking "Direct link to Data masking")

Our [Best Practices for dbt and Unity Catalog](https://docs.getdbt.com/best-practices/dbt-unity-catalog-best-practices.md) guide recommends using separate catalogs *dev* and *prod* for development and deployment environments, with Unity Catalog and dbt handling configurations and permissions for environment isolation. Ensuring security while maintaining efficiency in your development and deployment environments is crucial. Additional security measures may be necessary to protect sensitive data, such as personally identifiable information (PII).

Databricks leverages [Dynamic Views](https://docs.databricks.com/data-governance/unity-catalog/create-views.html#create-a-dynamic-view) to enable data masking based on group membership. Because views in Unity Catalog use Spark SQL, you can implement advanced data masking by using more complex SQL expressions and regular expressions. You can now also apply fine grained access controls like row filters in preview and column masks in preview on tables in Databricks Unity Catalog, which will be the recommended approach to protect sensitive data once this goes GA. Additionally, in the near term, Databricks Unity Catalog will also enable Attribute Based Access Control natively, which will make protecting sensitive data at scale simpler.

To implement data masking in a dbt model, ensure the model materialization configuration is set to view. Next, add a case statement using the is\_account\_group\_member function to identify groups permitted to view plain text values. Then, use regex to mask data for all other users. For example:
```

Example 2 (unknown):
```unknown
It is recommended not to grant users the ability to read tables and views referenced in the dynamic view. Instead, assign your dbt sources to dynamic views rather than raw data, allowing developers to run end-to-end builds and source freshness commands securely.

Using the same sources for development and deployment environments enables testing with the same volumes and frequency you will see in production. However, this may cause development runs to take longer than necessary. To address this issue, consider using the Jinja variable target.name to [limit data when working in the development environment](https://docs.getdbt.com/reference/dbt-jinja-functions/target.md#use-targetname-to-limit-data-in-dev).

#### Pairing dbt Docs and Unity Catalog[​](#pairing-dbt-docs-and-unity-catalog "Direct link to Pairing dbt Docs and Unity Catalog")

Though there are similarities between dbt docs and Databricks Unity Catalog, they are ultimately used for different purposes and complement each other well. By combining their strengths, you can provide your organization with a robust and user-friendly data management ecosystem.

dbt docs is a documentation site generated from your dbt project that provides an interface for developers and non-technical stakeholders to understand the data lineage and business logic applied to transformations without requiring full access to dbt or Databricks. It gives you additional options on how you can organize and search for your data. You can automatically [build and view your dbt docs using dbt](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md) to keep the documentation evergreen.

Unity Catalog is a unified governance solution for your lakehouse. It provides a data explorer that can be used for discovery of datasets that have not been defined in dbt. The data explorer also captures [column-level lineage](https://docs.databricks.com/data-governance/unity-catalog/data-lineage.html#capture-and-explore-lineage),  when you need to trace the lineage of a specific column.

To get the most out of both tools, you can use the [persist docs config](https://docs.getdbt.com/reference/resource-configs/persist_docs.md) to push table and column descriptions written in dbt into Unity Catalog, making the information easily accessible to both tools' users. Keeping the descriptions in dbt ensures they are version controlled and can be reproduced after a table is dropped.

##### Related docs[​](#related-docs "Direct link to Related docs")

* [Advanced Deployment course](https://learn.getdbt.com/courses/advanced-deployment) if you want a deeper dive into these topics
* [Autoscaling CI: The intelligent Slim CI](https://docs.getdbt.com/docs/deploy/continuous-integration.md)
* [Trigger a dbt Job in your automated workflow with Python](https://discourse.getdbt.com/t/triggering-a-dbt-cloud-job-in-your-automated-workflow-with-python/2573)
* [Databricks + dbt Quickstart Guide](https://docs.getdbt.com/guides/databricks.md)
* Reach out to your Databricks account team to get access to preview features on Databricks.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Quickstart for dbt and Amazon Athena

[Back to guides](https://docs.getdbt.com/guides.md)

Amazon

Athena

dbt platform

Quickstart

Beginner

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

In this quickstart guide, you'll learn how to use dbt with Amazon Athena. It will show you how to:

* Create an S3 bucket for Athena query results.
* Create an Athena database.
* Access sample data in a public dataset.
* Connect dbt to Amazon Athena.
* Take a sample query and turn it into a model in your dbt project. A model in dbt is a select statement.
* Add tests to your models.
* Document your models.
* Schedule a job to run.

Videos for you

You can check out [dbt Fundamentals](https://learn.getdbt.com/courses/dbt-fundamentals) for free if you're interested in course learning with videos.

##### Prerequisites​[​](#prerequisites "Direct link to Prerequisites​")

* You have a [dbt account](https://www.getdbt.com/signup/).
* You have an [AWS account](https://aws.amazon.com/).
* You have set up [Amazon Athena](https://docs.aws.amazon.com/athena/latest/ug/getting-started.html).

##### Related content[​](#related-content "Direct link to Related content")

* Learn more with [dbt Learn courses](https://learn.getdbt.com)
* [CI jobs](https://docs.getdbt.com/docs/deploy/continuous-integration.md)
* [Deploy jobs](https://docs.getdbt.com/docs/deploy/deploy-jobs.md)
* [Job notifications](https://docs.getdbt.com/docs/deploy/job-notifications.md)
* [Source freshness](https://docs.getdbt.com/docs/deploy/source-freshness.md)

#### Getting started[​](#getting-started "Direct link to Getting started")

For the following guide you can use an existing S3 bucket or [create a new one](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).

Download the following CSV files (the Jaffle Shop sample data) and upload them to your S3 bucket:

* [jaffle\_shop\_customers.csv](https://dbt-tutorial-public.s3-us-west-2.amazonaws.com/jaffle_shop_customers.csv)
* [jaffle\_shop\_orders.csv](https://dbt-tutorial-public.s3-us-west-2.amazonaws.com/jaffle_shop_orders.csv)
* [stripe\_payments.csv](https://dbt-tutorial-public.s3-us-west-2.amazonaws.com/stripe_payments.csv)

#### Configure Amazon Athena[​](#configure-amazon-athena "Direct link to Configure Amazon Athena")

1. Log into your AWS account and navigate to the **Athena console**.
   <!-- -->
   * If this is your first time in the Athena console (in your current AWS Region), click **Explore the query editor** to open the query editor. Otherwise, Athena opens automatically in the query editor.

2. Open **Settings** and find the **Location of query result box** field.

   <!-- -->

   1. Enter the path of the S3 bucket (prefix it with `s3://`).
   2. Navigate to **Browse S3**, select the S3 bucket you created, and click **Choose**.

3. **Save** these settings.

4. In the **query editor**, create a database by running `create database YOUR_DATABASE_NAME`.

5. To make the database you created the one you `write` into, select it from the **Database** list on the left side menu.

6. Access the Jaffle Shop data in the S3 bucket using one of these options:

   <!-- -->

   1. Manually create the tables.
   2. Create a glue crawler to recreate the data as external tables (recommended).

7. Once the tables have been created, you will able to `SELECT` from them.

#### Set up security access to Athena[​](#set-up-security-access-to-athena "Direct link to Set up security access to Athena")

To setup the security access for Athena, determine which access method you want to use:

* Obtain `aws_access_key_id` and `aws_secret_access_key` (recommended)
* Obtain an **AWS credentials** file.

##### AWS access key (recommended)[​](#aws-access-key-recommended "Direct link to AWS access key (recommended)")

To obtain your `aws_access_key_id` and `aws_secret_access_key`:

1. Open the **AWS Console**.
2. Click on your **username** near the top right and click **Security Credentials**.
3. Click on **Users** in the sidebar.
4. Click on your **username** (or the name of the user for whom to create the key).
5. Click on the **Security Credentials** tab.
6. Click **Create Access Key**.
7. Click **Show User Security Credentials** and

Save the `aws_access_key_id` and `aws_secret_access_key` for a future step.

##### AWS credentials file[​](#aws-credentials-file "Direct link to AWS credentials file")

To obtain your AWS credentials file:

1. Follow the instructions for [configuring the credentials file](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html) usin the AWS CLI

2. Locate the `~/.aws/credentials` file on your computer

   <!-- -->

   1. Windows: `%USERPROFILE%\.aws\credentials`
   2. Mac/Linux: `~/.aws/credentials`

Retrieve the `aws_access_key_id` and `aws_secret_access_key` from the `~/.aws/credentials` file for a future step.

#### Configure the connection in dbt[​](#configure-the-connection-in-dbt "Direct link to Configure the connection in dbt")

To configure the Athena connection in dbt:

1. Click your **account name** on the left-side menu and click **Account settings**.

2. Click **Connections** and click **New connection**.

3. Click **Athena** and fill out the required fields (and any optional fields).

   <!-- -->

   1. **AWS region name** — The AWS region of your environment.
   2. **Database (catalog)** — Enter the database name created in earlier steps (lowercase only).
   3. **AWS S3 staging directory** — Enter the S3 bucket created in earlier steps.

4. Click **Save**

##### Configure your environment[​](#configure-your-environment "Direct link to Configure your environment")

To configure the Athena credentials in your environment:

1. Click **Deploy** on the left-side menu and click **Environments**.
2. Click **Create environment** and fill out the **General settings**.
   <!-- -->
   * Your **dbt version** must be set to `Versionless` to use the Athena connection.
3. Select the Athena connection from the **Connection** dropdown.
4. Fill out the `aws_access_key` and `aws_access_id` recorded in previous steps, as well as the `Schema` to write to.
5. Click **Test connection** and once it succeeds, **Save** the environment.

Repeat the process to create a [development environment](https://docs.getdbt.com/docs/dbt-cloud-environments.md#types-of-environments).

#### Set up a dbt managed repository[​](#set-up-a-dbt-managed-repository "Direct link to Set up a dbt managed repository")

When you develop in dbt, you can leverage [Git](https://docs.getdbt.com/docs/cloud/git/git-version-control.md) to version control your code.

To connect to a repository, you can either set up a dbt-hosted [managed repository](https://docs.getdbt.com/docs/cloud/git/managed-repository.md) or directly connect to a [supported git provider](https://docs.getdbt.com/docs/cloud/git/connect-github.md). Managed repositories are a great way to trial dbt without needing to create a new repository. In the long run, it's better to connect to a supported git provider to use features like automation and [continuous integration](https://docs.getdbt.com/docs/deploy/continuous-integration.md).

To set up a managed repository:

1. Under "Setup a repository", select **Managed**.
2. Type a name for your repo such as `bbaggins-dbt-quickstart`
3. Click **Create**. It will take a few seconds for your repository to be created and imported.
4. Once you see the "Successfully imported repository," click **Continue**.

#### Initialize your dbt project​ and start developing[​](#initialize-your-dbt-project-and-start-developing "Direct link to Initialize your dbt project​ and start developing")

Now that you have a repository configured, you can initialize your project and start development in dbt:

1. Click **Start developing in the Studio IDE**. It might take a few minutes for your project to spin up for the first time as it establishes your git connection, clones your repo, and tests the connection to the warehouse.

2. Above the file tree to the left, click **Initialize dbt project**. This builds out your folder structure with example models.

3. Make your initial commit by clicking **Commit and sync**. Use the commit message `initial commit` and click **Commit**. This creates the first commit to your managed repo and allows you to open a branch where you can add new dbt code.

4. You can now directly query data from your warehouse and execute `dbt run`. You can try this out now:

   <!-- -->

   * Click **+ Create new file**, add this query to the new file, and click **Save as** to save the new file:

     <!-- -->
```

Example 3 (unknown):
```unknown
* In the command line bar at the bottom, enter `dbt run` and click **Enter**. You should see a `dbt run succeeded` message.

#### Build your first model[​](#build-your-first-model "Direct link to Build your first model")

You have two options for working with files in the Studio IDE:

* Create a new branch (recommended) — Create a new branch to edit and commit your changes. Navigate to **Version Control** on the left sidebar and click **Create branch**.
* Edit in the protected primary branch — If you prefer to edit, format, or lint files and execute dbt commands directly in your primary git branch. The Studio IDE prevents commits to the protected branch, so you will be prompted to commit your changes to a new branch.

Name the new branch `add-customers-model`.

1. Click the **...** next to the `models` directory, then select **Create file**.
2. Name the file `customers.sql`, then click **Create**.
3. Copy the following query into the file and click **Save**.
```

Example 4 (unknown):
```unknown
4. Enter `dbt run` in the command prompt at the bottom of the screen. You should get a successful run and see the three models.

Later, you can connect your business intelligence (BI) tools to these views and tables so they only read cleaned up data rather than raw data in your BI tool.

###### FAQs[​](#faqs "Direct link to FAQs")

How can I see the SQL that dbt is running?

To check out the SQL that dbt is running, you can look in:

* dbt:
  <!-- -->
  * Within the run output, click on a model name, and then select "Details"

* dbt Core:

  <!-- -->

  * The `target/compiled/` directory for compiled `select` statements
  * The `target/run/` directory for compiled `create` statements
  * The `logs/dbt.log` file for verbose logging.

How did dbt choose which schema to build my models in?

By default, dbt builds models in your target schema. To change your target schema:

* If you're developing in **dbt**, these are set for each user when you first use a development environment.
* If you're developing with **dbt Core**, this is the `schema:` parameter in your `profiles.yml` file.

If you wish to split your models across multiple schemas, check out the docs on [using custom schemas](https://docs.getdbt.com/docs/build/custom-schemas.md).

Note: on BigQuery, `dataset` is used interchangeably with `schema`.

Do I need to create my target schema before running dbt?

Nope! dbt will check if the schema exists when it runs. If the schema does not exist, dbt will create it for you.

If I rerun dbt, will there be any downtime as models are rebuilt?

Nope! The SQL that dbt generates behind the scenes ensures that any relations are replaced atomically (i.e. your business users won't experience any downtime).

The implementation of this varies on each warehouse, check out the [logs](https://docs.getdbt.com/faqs/Runs/checking-logs.md) to see the SQL dbt is executing.

What happens if the SQL in my query is bad or I get a database error?

If there's a mistake in your SQL, dbt will return the error that your database returns.
```

---

## session connections

**URL:** llms-txt#session-connections

$ python -m pip install "dbt-spark[session]"

your_profile_name:
  target: dev
  outputs:
    dev:
      type: spark
      method: odbc
      driver: [path/to/driver]
      schema: [database/schema name]
      host: [yourorg.sparkhost.com]
      organization: [org id]    # Azure Databricks only
      token: [abc123]
      
      # one of:
      endpoint: [endpoint id]
      cluster: [cluster id]
      
      # optional
      port: [port]              # default 443
      user: [user]
      server_side_parameters:
        "spark.driver.memory": "4g"

your_profile_name:
  target: dev
  outputs:
    dev:
      type: spark
      method: thrift
      schema: [database/schema name]
      host: [hostname]
      
      # optional
      port: [port]              # default 10001
      user: [user]
      auth: [for example, KERBEROS]
      kerberos_service_name: [for example, hive]
      use_ssl: [true|false]   # value of hive.server2.use.SSL, default false
      server_side_parameters:
        "spark.driver.memory": "4g"

your_profile_name:
  target: dev
  outputs:
    dev:
      type: spark
      method: http
      schema: [database/schema name]
      host: [yourorg.sparkhost.com]
      organization: [org id]    # Azure Databricks only
      token: [abc123]
      cluster: [cluster id]
      
      # optional
      port: [port]              # default: 443
      user: [user]
      connect_timeout: 60       # default 10
      connect_retries: 5        # default 0
      server_side_parameters:
        "spark.driver.memory": "4g"

your_profile_name:
  target: dev
  outputs:
    dev:
      type: spark
      method: session
      schema: [database/schema name]
      host: NA                           # not used, but required by `dbt-core`
      server_side_parameters:
        "spark.driver.memory": "4g"

retry_all: true
connect_timeout: 5
connect_retries: 3

default:
  outputs:
    dev:
      type: athena
      s3_staging_dir: [s3_staging_dir]
      s3_data_dir: [s3_data_dir]
      s3_data_naming: [table_unique] # the type of naming convention used when writing to S3
      region_name: [region_name]
      database: [database name]
      schema: [dev_schema]
      aws_profile_name: [optional profile to use from your AWS shared credentials file.]
      threads: [1 or more]
      num_retries: [0 or more] # number of retries performed by the adapter. Defaults to 5
  target: dev

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Read_and_write_databases",
            "Action": [
                "glue:SearchTables",
                "glue:BatchCreatePartition",
                "glue:CreatePartitionIndex",
                "glue:DeleteDatabase",
                "glue:GetTableVersions",
                "glue:GetPartitions",
                "glue:DeleteTableVersion",
                "glue:UpdateTable",
                "glue:DeleteTable",
                "glue:DeletePartitionIndex",
                "glue:GetTableVersion",
                "glue:UpdateColumnStatisticsForTable",
                "glue:CreatePartition",
                "glue:UpdateDatabase",
                "glue:CreateTable",
                "glue:GetTables",
                "glue:GetDatabases",
                "glue:GetTable",
                "glue:GetDatabase",
                "glue:GetPartition",
                "glue:UpdateColumnStatisticsForPartition",
                "glue:CreateDatabase",
                "glue:BatchDeleteTableVersion",
                "glue:BatchDeleteTable",
                "glue:DeletePartition",
                "glue:GetUserDefinedFunctions",
                "lakeformation:ListResources",
                "lakeformation:BatchGrantPermissions",
                "lakeformation:ListPermissions", 
                "lakeformation:GetDataAccess",
                "lakeformation:GrantPermissions",
                "lakeformation:RevokePermissions",
                "lakeformation:BatchRevokePermissions",
                "lakeformation:AddLFTagsToResource",
                "lakeformation:RemoveLFTagsFromResource",
                "lakeformation:GetResourceLFTags",
                "lakeformation:ListLFTags",
                "lakeformation:GetLFTag",
            ],
            "Resource": [
                "arn:aws:glue:<region>:<AWS Account>:catalog",
                "arn:aws:glue:<region>:<AWS Account>:table/<dbt output database>/*",
                "arn:aws:glue:<region>:<AWS Account>:database/<dbt output database>"
            ],
            "Effect": "Allow"
        },
        {
            "Sid": "Read_only_databases",
            "Action": [
                "glue:SearchTables",
                "glue:GetTableVersions",
                "glue:GetPartitions",
                "glue:GetTableVersion",
                "glue:GetTables",
                "glue:GetDatabases",
                "glue:GetTable",
                "glue:GetDatabase",
                "glue:GetPartition",
                "lakeformation:ListResources",
                "lakeformation:ListPermissions"
            ],
            "Resource": [
                "arn:aws:glue:<region>:<AWS Account>:table/<dbt source database>/*",
                "arn:aws:glue:<region>:<AWS Account>:database/<dbt source database>",
                "arn:aws:glue:<region>:<AWS Account>:database/default",
                "arn:aws:glue:<region>:<AWS Account>:database/global_temp"
            ],
            "Effect": "Allow"
        },
        {
            "Sid": "Storage_all_buckets",
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::<dbt output bucket>",
                "arn:aws:s3:::<dbt source bucket>"
            ],
            "Effect": "Allow"
        },
        {
            "Sid": "Read_and_write_buckets",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::<dbt output bucket>"
            ],
            "Effect": "Allow"
        },
        {
            "Sid": "Read_only_buckets",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::<dbt source bucket>"
            ],
            "Effect": "Allow"
        }
    ]
}

$ sudo yum install git
$ python3 -m venv dbt_venv
$ source dbt_venv/bin/activate
$ python3 -m pip install --upgrade pip

$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install

$ sudo yum install gcc krb5-devel.x86_64 python3-devel.x86_64 -y
$ pip3 install —upgrade boto3

$ pip3 install dbt-glue

type: glue
query-comment: This is a glue dbt example
role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
region: us-east-1
workers: 2
worker_type: G.1X
idle_timeout: 10
schema: "dbt_demo"
session_provisioning_timeout_in_seconds: 120
location: "s3://dbt_demo_bucket/dbt_demo_data"

{{ config(
    materialized='incremental',
    incremental_strategy='append',
) }}

--  All rows returned by this query will be appended to the existing table

select * from {{ ref('events') }}
{% if is_incremental() %}
  where event_ts > (select max(event_ts) from {{ this }})
{% endif %}

create temporary view spark_incremental__dbt_tmp as

select * from analytics.events

where event_ts >= (select max(event_ts) from {{ this }})

insert into table analytics.spark_incremental
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

create temporary view spark_incremental__dbt_tmp as

select * from analytics.events

where date_day >= date_add(current_date, -1)

select
        date_day,
        count(*) as users

from events
    group by 1

insert overwrite table analytics.spark_incremental
    partition (date_day)
    select `date_day`, `users` from spark_incremental__dbt_tmp

{
    "Sid": "access_to_connections",
    "Action": [
        "glue:GetConnection",
        "glue:GetConnections"
    ],
    "Resource": [
        "arn:aws:glue:<region>:<AWS Account>:catalog",
        "arn:aws:glue:<region>:<AWS Account>:connection/*"
    ],
    "Effect": "Allow"
}

test_project:
  target: dev
  outputs:
    dev:
      type: glue
      query-comment: my comment
      role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
      region: eu-west-1
      glue_version: "4.0"
      workers: 2
      worker_type: G.1X
      schema: "dbt_test_project"
      session_provisioning_timeout_in_seconds: 120
      location: "s3://aws-dbt-glue-datalake-1234567890-eu-west-1/"
      conf: spark.serializer=org.apache.spark.serializer.KryoSerializer --conf spark.sql.hive.convertMetastoreParquet=false
      datalake_formats: hudi

{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='user_id',
    file_format='hudi',
    hudi_options={
        'hoodie.datasource.write.precombine.field': 'eventtime',
    }
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

test_project:
  target: dev
  outputs:
    dev:
      type: glue
      query-comment: my comment
      role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
      region: eu-west-1
      glue_version: "4.0"
      workers: 2
      worker_type: G.1X
      schema: "dbt_test_project"
      session_provisioning_timeout_in_seconds: 120
      location: "s3://aws-dbt-glue-datalake-1234567890-eu-west-1/"
      datalake_formats: delta
      conf: "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
      extra_py_files: "/opt/aws_glue_connectors/selected/datalake/delta-core_2.12-2.1.0.jar"
      delta_athena_prefix: "delta"

{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key='user_id',
    partition_by=['dt'],
    file_format='delta'
) }}

select * from {{ ref('events') }}

{% if is_incremental() %}
    where date_day >= date_add(current_date, -1)
    {% endif %}

select
    user_id,
    max(date_day) as last_seen,
    current_date() as dt

from events
group by 1

iceberg_glue_commit_lock_table: "MyDynamoDbTable"

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CommitLockTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:CreateTable",
                "dynamodb:BatchGetItem",
                "dynamodb:BatchWriteItem",
                "dynamodb:ConditionCheckItem",
                "dynamodb:PutItem",
                "dynamodb:DescribeTable",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:UpdateItem"
            ],
            "Resource": "arn:aws:dynamodb:<AWS_REGION>:<AWS_ACCOUNT_ID>:table/myGlueLockTable"
        }
    ]
}

--conf spark.serializer=org.apache.spark.serializer.KryoSerializer
    --conf spark.sql.warehouse=s3://<your-bucket-name>
    --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog 
    --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog 
    --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO 
    --conf spark.sql.catalog.glue_catalog.lock-impl=org.apache.iceberg.aws.dynamodb.DynamoDbLockManager
    --conf spark.sql.catalog.glue_catalog.lock.table=myGlueLockTable  
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions

--conf spark.sql.catalog.RandomCatalogName=org.apache.iceberg.spark.SparkCatalog

--conf spark.sql.catalog.AnotherRandomCatalogName=org.apache.iceberg.spark.SparkCatalog

--conf spark.sql.catalog.RandomCatalogName=org.apache.iceberg.spark.SparkCatalog 
 --conf spark.sql.catalog.RandomCatalogName.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog 
 ...
 --conf spark.sql.catalog.RandomCatalogName.lock-impl=org.apache.iceberg.aws.glue.DynamoLockManager

test_project:
  target: dev
  outputs:
    dev:
      type: glue
      query-comment: my comment
      role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
      region: eu-west-1
      glue_version: "4.0"
      workers: 2
      worker_type: G.1X
      schema: "dbt_test_project"
      session_provisioning_timeout_in_seconds: 120
      location: "s3://aws-dbt-glue-datalake-1234567890-eu-west-1/"
      datalake_formats: iceberg
      conf: --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions --conf spark.serializer=org.apache.spark.serializer.KryoSerializer --conf spark.sql.warehouse=s3://aws-dbt-glue-datalake-1234567890-eu-west-1/dbt_test_project --conf spark.sql.catalog.glue_catalog=org.apache.iceberg.spark.SparkCatalog --conf spark.sql.catalog.glue_catalog.catalog-impl=org.apache.iceberg.aws.glue.GlueCatalog --conf spark.sql.catalog.glue_catalog.io-impl=org.apache.iceberg.aws.s3.S3FileIO --conf spark.sql.catalog.glue_catalog.lock-impl=org.apache.iceberg.aws.dynamodb.DynamoDbLockManager --conf spark.sql.catalog.glue_catalog.lock.table=myGlueLockTable  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions

{{ config(
    materialized='incremental',
    incremental_strategy='merge',
    unique_key=['user_id'],
    file_format='iceberg',
    iceberg_expire_snapshots='False', 
    partition_by=['status']
    table_properties={'write.target-file-size-bytes': '268435456'}
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

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudwatchMetrics",
            "Effect": "Allow",
            "Action": "cloudwatch:PutMetricData",
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "cloudwatch:namespace": "Glue"
                }
            }
        },
        {
            "Sid": "CloudwatchLogs",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:*:*:/aws-glue/*",
                "arn:aws:s3:::bucket-to-write-sparkui-logs/*"
            ]
        }
    ]
}

test_project:
  target: dev
  outputs:
    dev:
      type: glue
      query-comment: my comment
      role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
      region: eu-west-1
      glue_version: "4.0"
      workers: 2
      worker_type: G.1X
      schema: "dbt_test_project"
      session_provisioning_timeout_in_seconds: 120
      location: "s3://aws-dbt-glue-datalake-1234567890-eu-west-1/"
      default_arguments: "--enable-metrics=true, --enable-continuous-cloudwatch-log=true, --enable-continuous-log-filter=true, --enable-spark-ui=true, --spark-event-logs-path=s3://bucket-to-write-sparkui-logs/dbt/"

test_project:
  target: dev
  outputs:
    dev:
      type: glue
      query-comment: my comment
      role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
      region: eu-west-1
      glue_version: "3.0"
      workers: 2
      worker_type: G.1X
      schema: "dbt_test_project"
      session_provisioning_timeout_in_seconds: 120
      location: "s3://aws-dbt-glue-datalake-1234567890-eu-west-1/"
      default_arguments: "--enable-auto-scaling=true"

test_project:
  target: dev
  outputsAccountB:
    dev:
      type: glue
      query-comment: my comment
      role_arn: arn:aws:iam::1234567890:role/GlueInteractiveSessionRole
      region: eu-west-1
      glue_version: "3.0"
      workers: 2
      worker_type: G.1X
      schema: "dbt_test_project"
      session_provisioning_timeout_in_seconds: 120
      location: "s3://aws-dbt-glue-datalake-1234567890-eu-west-1/"
      conf: "--conf hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory 
             --conf spark.hadoop.hive.metastore.glue.catalogid=<TARGET-AWS-ACCOUNT-ID-B>"

lf_grants={
        'data_cell_filters': {
            'enabled': True,
            'drop_existing' : True,
            'filters': {
                'the_name_of_my_filter': {
                    'row_filter': 'customer_lifetime_value>15',
                    'principals': ['arn:aws:iam::123456789:user/lf-data-scientist'], 
                    'column_names': ['customer_id', 'first_order', 'most_recent_order', 'number_of_orders']
                }
            }, 
        }
    }

lf_grants={
        'data_cell_filters': {
            'enabled': True,
            'drop_existing' : True,
            'filters': {
                'the_name_of_my_filter': {
                    'row_filter': 'customer_lifetime_value>15',
                    'principals': ['arn:aws:iam::123456789:user/lf-data-scientist'], 
                    'excluded_column_names': ['first_name']
                }
            }, 
        }
    }

{{ config(
    materialized='incremental',
    unique_key="customer_id",
    incremental_strategy='append',
    lf_tags_config={
          'enabled': true,
          'drop_existing' : False,
          'tags_database': 
          {
            'name_of_my_db_tag': 'value_of_my_db_tag'          
            }, 
          'tags_table': 
          {
            'name_of_my_table_tag': 'value_of_my_table_tag'          
            }, 
          'tags_columns': {
            'name_of_my_lf_tag': {
              'value_of_my_tag': ['customer_id', 'customer_lifetime_value', 'dt']
            }}},
    lf_grants={
        'data_cell_filters': {
            'enabled': True,
            'drop_existing' : True,
            'filters': {
                'the_name_of_my_filter': {
                    'row_filter': 'customer_lifetime_value>15',
                    'principals': ['arn:aws:iam::123456789:user/lf-data-scientist'], 
                    'excluded_column_names': ['first_name']
                }
            }, 
        }
    }
) }}

select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customer_orders.first_order,
        customer_orders.most_recent_order,
        customer_orders.number_of_orders,
        customer_payments.total_amount as customer_lifetime_value,
        current_date() as dt
        
    from customers

left join customer_orders using (customer_id)

left join customer_payments using (customer_id)

seeds:
  +lf_tags_config:
    enabled: true
    tags_table: 
      name_of_my_table_tag: 'value_of_my_table_tag'  
    tags_database: 
      name_of_my_database_tag: 'value_of_my_database_tag'
models:
  +lf_tags_config:
    enabled: true
    drop_existing: True
    tags_database: 
      name_of_my_database_tag: 'value_of_my_database_tag'
    tags_table: 
      name_of_my_table_tag: 'value_of_my_table_tag'

$ pip3 install -r dev-requirements.txt

$ python3 setup.py build && python3 setup.py install_lib

$ export DBT_S3_LOCATION=s3://mybucket/myprefix
$ export DBT_ROLE_ARN=arn:aws:iam::1234567890:role/GlueInteractiveSessionRole

$ python3 -m pytest tests/functional

**Examples:**

Example 1 (unknown):
```unknown
#### Configuring <!-- -->dbt-spark<!-- -->

For <!-- -->Spark<!-- -->-specific configuration please refer to [Spark<!-- --> Configuration](https://docs.getdbt.com/reference/resource-configs/spark-configs.md)

For further info, refer to the GitHub repository: [dbt-labs/dbt-adapters](https://github.com/dbt-labs/dbt-adapters)

#### Connection methods[​](#connection-methods "Direct link to Connection methods")

dbt-spark can connect to Spark clusters by four different methods:

* [`odbc`](#odbc) is the preferred method when connecting to Databricks. It supports connecting to a SQL Endpoint or an all-purpose interactive cluster.

* [`thrift`](#thrift) connects directly to the lead node of a cluster, either locally hosted / on premise or in the cloud (for example, Amazon EMR).

* [`http`](#http) is a more generic method for connecting to a managed service that provides an HTTP endpoint. Currently, this includes connections to a Databricks interactive cluster.

* [`session`](#session) connects to a pySpark session, running locally or on a remote machine.

Advanced functionality

The `session` connection method is intended for advanced users and experimental dbt development. This connection method is not supported by dbt.

##### ODBC[​](#odbc "Direct link to ODBC")

Use the `odbc` connection method if you are connecting to a Databricks SQL endpoint or interactive cluster via ODBC driver. (Download the latest version of the official driver [here](https://databricks.com/spark/odbc-driver-download).)

\~/.dbt/profiles.yml
```

Example 2 (unknown):
```unknown
##### Thrift[​](#thrift "Direct link to Thrift")

Use the `thrift` connection method if you are connecting to a Thrift server sitting in front of a Spark cluster, for example, a cluster running locally or on Amazon EMR.

\~/.dbt/profiles.yml
```

Example 3 (unknown):
```unknown
##### HTTP[​](#http "Direct link to HTTP")

Use the `http` method if your Spark provider supports generic connections over HTTP (for example, Databricks interactive cluster).

\~/.dbt/profiles.yml
```

Example 4 (unknown):
```unknown
Databricks interactive clusters can take several minutes to start up. You may include the optional profile configs `connect_timeout` and `connect_retries`, and dbt will periodically retry the connection.

##### Session[​](#session "Direct link to Session")

Use the `session` method if you want to run `dbt` against a pySpark session.

\~/.dbt/profiles.yml
```

---

## models/my_model.sql

**URL:** llms-txt#models/my_model.sql

my_model_sql = """
select * from {{ ref('my_seed') }}
union all
select null as id, null as name, null as some_date
"""

---

## Sort the models by execution time

**URL:** llms-txt#sort-the-models-by-execution-time

models_df_sorted = models_df.sort_values('executionTime', ascending=False)

print(models_df_sorted)

---

## Run tests on all models with a particular materialization (indirect selection)

**URL:** llms-txt#run-tests-on-all-models-with-a-particular-materialization-(indirect-selection)

dbt test --select "config.materialized:table"

**Examples:**

Example 1 (unknown):
```unknown
The same principle can be extended to tests defined on other resource types. In these cases, we will execute all tests defined on certain sources via the `source:` selection method:
```

---

## dbt users

**URL:** llms-txt#dbt-users

dbt sl query --metrics users_created,users_deleted --group-by metric_time__year --order-by metric_time__year

---

## because linting will first compile dbt code into data warehouse code.

**URL:** llms-txt#because-linting-will-first-compile-dbt-code-into-data-warehouse-code.

**Contents:**
  - Navigate the interface EnterpriseEnterprise +
  - Navigate the interface [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Studio IDE keyboard shortcuts
  - Supported browsers
  - Tenancy
  - The dbt platform features
  - Use dbt Copilot StarterEnterpriseEnterprise +
  - Use dbt Copilot [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Using defer in dbt
- Reference

runaway_limit = 10
max_line_length = 80
indent_unit = space

[sqlfluff:indentation]
tab_space_size = 4

[sqlfluff:layout:type:comma]
spacing_before = touch
line_position = trailing

[sqlfluff:rules:capitalisation.keywords] 
capitalisation_policy = lower

[sqlfluff:rules:aliasing.table]
aliasing = explicit

[sqlfluff:rules:aliasing.column]
aliasing = explicit

[sqlfluff:rules:aliasing.expression]
allow_scalar = False

[sqlfluff:rules:capitalisation.identifiers]
extended_capitalisation_policy = lower

[sqlfluff:rules:capitalisation.functions]
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.literals]
capitalisation_policy = lower

[sqlfluff:rules:ambiguous.column_references]  # Number in group by
group_by_and_order_by_style = implicit

context:
  active-host: ...
  active-project: ...
  defer-env-id: '123456'

dbt-cloud:
  defer-env-id: '123456'

**Examples:**

Example 1 (unknown):
```unknown
For more info on styling best practices, refer to [How we style our SQL](https://docs.getdbt.com/best-practices/how-we-style/2-how-we-style-our-sql.md).

[![Customize linting by configuring your own linting code rules, including dbtonic linting/styling.](/img/docs/dbt-cloud/cloud-ide/ide-sqlfluff-config.png?v=2 "Customize linting by configuring your own linting code rules, including dbtonic linting/styling.")](#)Customize linting by configuring your own linting code rules, including dbtonic linting/styling.

#### Format[​](#format "Direct link to Format")

In the Studio IDE, you can format your code to match style guides with a click of a button. The Studio IDE integrates with formatters like sqlfmt, Prettier, and Black to automatically format code on five different file types — SQL, YAML, Markdown, Python, and JSON:

* SQL — Format with [sqlfmt](http://sqlfmt.com/), which provides one way to format your dbt SQL and Jinja.
  <!-- -->
  * **Note**: Custom sqlfmt configuration in the Studio IDE is not supported.
* YAML, Markdown, and JSON — Format with [Prettier](https://prettier.io/).
* Python — Format with [Black](https://black.readthedocs.io/en/latest/).

The Cloud Studio IDE formatting integrations take care of manual tasks like code formatting, enabling you to focus on creating quality data models, collaborating, and driving impactful results.

##### Format SQL[​](#format-sql "Direct link to Format SQL")

To format your SQL code, dbt integrates with [sqlfmt](http://sqlfmt.com/), which is an uncompromising SQL query formatter that provides one way to format the SQL query and Jinja.

By default, the Studio IDE uses sqlfmt rules to format your code, making the **Format** button available and convenient to use immediately. However, if you have a file named .sqlfluff in the root directory of your dbt project, the Studio IDE will default to SQLFluff rules instead.

Formatting is available on all branches, including your protected primary git branch. Since the Studio IDE prevents commits to the protected branch, it prompts you to commit those changes to a new branch.

1. Open a `.sql` file and click on the **Code Quality** tab.
2. Click on the **`</> Config`** button on the right side of the console.
3. In the code quality tool config pop-up, you have the option to select sqlfluff or sqlfmt.
4. To format your code, select the **sqlfmt** radio button. (Use sqlfluff to [lint](#linting) your code).
5. Once you've selected the **sqlfmt** radio button, go to the console section (located below the **File editor**) to select the **Format** button.
6. The **Format** button auto-formats your code in the **File editor**. Once you've auto-formatted, you'll see a message confirming the outcome.

[![Use sqlfmt to format your SQL code.](/img/docs/dbt-cloud/cloud-ide/sqlfmt.gif?v=2 "Use sqlfmt to format your SQL code.")](#)Use sqlfmt to format your SQL code.

##### Format YAML, Markdown, JSON[​](#format-yaml-markdown-json "Direct link to Format YAML, Markdown, JSON")

To format your YAML, Markdown, or JSON code, dbt integrates with [Prettier](https://prettier.io/), which is an opinionated code formatter. Formatting is available on all branches, including your protected primary git branch. Since the Studio IDE prevents commits to the protected branch, it prompts you to commit those changes to a new branch.

1. Open a `.yml`, `.md`, or `.json` file.
2. In the console section (located below the **File editor**), select the **Format** button to auto-format your code in the **File editor**. Use the **Code Quality** tab to view code errors.
3. Once you've auto-formatted, you'll see a message confirming the outcome.

[![Format YAML, Markdown, and JSON files using Prettier.](/img/docs/dbt-cloud/cloud-ide/prettier.gif?v=2 "Format YAML, Markdown, and JSON files using Prettier.")](#)Format YAML, Markdown, and JSON files using Prettier.

You can add a configuration file to customize formatting rules for YAML, Markdown, or JSON files using Prettier. The IDE looks for the configuration file based on an order of precedence. For example, it first checks for a "prettier" key in your `package.json` file.

For more info on the order of precedence and how to configure files, refer to [Prettier's documentation](https://prettier.io/docs/en/configuration.html). Please note, `.prettierrc.json5`, `.prettierrc.js`, and `.prettierrc.toml` files aren't currently supported.

##### Format Python[​](#format-python "Direct link to Format Python")

To format your Python code, dbt integrates with [Black](https://black.readthedocs.io/en/latest/), which is an uncompromising Python code formatter. Formatting is available on all branches, including your protected primary git branch. Since the Studio IDE prevents commits to the protected branch, it prompts you to commit those changes to a new branch.

1. Open a `.py` file.
2. In the console section (located below the **File editor**), select the **Format** button to auto-format your code in the **File editor**.
3. Once you've auto-formatted, you'll see a message confirming the outcome.

[![Format Python files using Black.](/img/docs/dbt-cloud/cloud-ide/python-black.gif?v=2 "Format Python files using Black.")](#)Format Python files using Black.

#### FAQs[​](#faqs "Direct link to FAQs")

 When should I use SQLFluff and when should I use sqlfmt?

SQLFluff and sqlfmt are both tools used for formatting SQL code, but some differences may make one preferable to the other depending on your use case.<br />

SQLFluff is a SQL code linter and formatter. This means that it analyzes your code to identify potential issues and bugs, and follows coding standards. It also formats your code according to a set of rules, which are [customizable](#customize-linting), to ensure consistent coding practices. You can also use SQLFluff to keep your SQL code well-formatted and follow styling best practices.<br />

sqlfmt is a SQL code formatter. This means it automatically formats your SQL code according to a set of formatting rules that aren't customizable. It focuses solely on the appearance and layout of the code, which helps ensure consistent indentation, line breaks, and spacing. sqlfmt doesn't analyze your code for errors or bugs and doesn't look at coding issues beyond code formatting.<br />

You can use either SQLFluff or sqlfmt depending on your preference and what works best for you:

* Use SQLFluff to have your code linted and formatted (meaning analyze fix your code for errors/bugs, and format your styling). It allows you the flexibility to customize your own rules.

* Use sqlfmt to only have your code well-formatted without analyzing it for errors and bugs. You can use sqlfmt out of the box, making it convenient to use right away without having to configure it.

 Can I nest \`.sqlfluff\` files?

To ensure optimal code quality, consistent code, and styles — it's highly recommended you have one main `.sqlfluff` configuration file in the root folder of your project. Having multiple files can result in various different SQL styles in your project.<br /><br />

However, you can customize and include an additional child `.sqlfluff` configuration file within specific subfolders of your dbt project.<br /><br />By nesting a `.sqlfluff` file in a subfolder, SQLFluff will apply the rules defined in that subfolder's configuration file to any files located within it. The rules specified in the parent `.sqlfluff` file will be used for all other files and folders outside of the subfolder. This hierarchical approach allows for tailored linting rules while maintaining consistency throughout your project. Refer to [SQLFluff documentation](https://docs.sqlfluff.com/en/stable/configuration.html#configuration-files) for more info.

 Can I run SQLFluff commands from the terminal?

Currently, running SQLFluff commands from the terminal isn't supported.

 What are some considerations when using dbt linting?

Currently, the Studio IDE can lint or fix files up to a certain size and complexity. If you attempt to lint or fix files that are too large, taking more than 60 seconds for the dbt backend to process, you will see an 'Unable to complete linting this file' error.

To avoid this, break up your model into smaller models (files) so that they are less complex to lint or fix. Note that linting is simpler than fixing so there may be cases where a file can be linted but not fixed.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [User interface](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/ide-user-interface.md)
* [Keyboard shortcuts](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/keyboard-shortcuts.md)
* [SQL linting in CI jobs](https://docs.getdbt.com/docs/deploy/continuous-integration.md#sql-linting)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Navigate the interface EnterpriseEnterprise +

### Navigate the interface [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

The Canvas interface contains an operator toolbar, operators, canvas, built-in AI, and more to help you access and transform data through a seamless drag-and-drop dbt model creation experience in dbt.

This page offers comprehensive definitions and terminology of user interface elements, allowing you to navigate the Canvas landscape with ease.

The Canvas interface is composed of:

* **Navigation bars** — The top and ledft-side navigation bars contain options for switching between models in the workspace, opening existing or creating new models, uploading CSV data, previewing data and runs, and viewing helpful shortcuts.

* **Operator toolbar** — Located at the top of the canvas area, the toolbar displays all the node categories available, as well as tools to help you develop:

  <!-- -->

  * **Input:** Source models and data
  * **Transform:** Data transformation tools
  * **Output:** Output model configurations
  * **[Copilot](https://docs.getdbt.com/docs/cloud/build-canvas-copilot.md):** AI tools to help you build fast and efficiently
  * **SQL:** View your completed model's compiled SQL

* **Operators** — Tiles that provide source data, perform specific transformations, and layer configurations (such as model, join, aggregate, filter, and so on). Use connectors to link the operators and build a complete data transformation pipeline.

* **Canvas** — The main whiteboard space below the node toolbar. The canvas allows you to create or modify models through a sleek drag-and-drop experience.

* **Configuration panel** — Each operator has a configuration panel that opens when you click on it. The configuration panel allows you to configure the operator, review the current model, preview changes to the table, view the SQL code for the node, and delete the operator.

#### Operators[​](#operators "Direct link to Operators")

The operator toolbar above the canvas contains the different transformation operators available to use. Use each operator to configure or perform specific tasks, like adding filters or joining models by dragging an operator onto the canvas. You can connect operators using the connector line, which allows you to form a complete model for your data transformation.

[![Use the operator toolbar to perform different transformation operations.](/img/docs/dbt-cloud/canvas/operators.png?v=2 "Use the operator toolbar to perform different transformation operations.")](#)Use the operator toolbar to perform different transformation operations.

Here the following operators are available:

###### Input[​](#input "Direct link to Input")

Input operators configure source data:

* **Model explorer**: Select the model and columns you want to use.

###### Transform[​](#transform "Direct link to Transform")

Transform operators shape your data:

* **Join**: Define the join conditions and choose columns from both tables.
* **Union:** Perform a `UNION` to remove duplicates or `UNION ALL` to prevent deduplicaation.
* **Formula**: Add the formula to create a new column. Use the built-AI code generator to help
* **Aggregate**: Specify the aggregation functions and the columns they apply to generate SQL code by clicking on the question mark (?) icon. Enter your prompt and wait to see the results.
* **Pivot:** Select the column and values to create a pivot.
* **Limit**: Set the maximum number of rows you want to return.
* **Order**: Select the columns to sort by and the sort order.
* **Filter**: Set the conditions to filter data.
* **Rename:** Provide custom alias' for your columns.

###### Output model[​](#output-model "Direct link to Output model")

Output operators configure the names and location of your transformed data:

* **Output model**: The final transformed dataset generated by a dbt model. You can only have one output model.

When you click on each operator, it opens a configuration panel. The configuration panel allows you to configure the operator, review the current model, preview changes to the model, view the SQL code for the node, and delete the operator.

[![The Canvas interface that contains a node toolbar and canvas.](/img/docs/dbt-cloud/canvas/canvas.png?v=2 "The Canvas interface that contains a node toolbar and canvas.")](#)The Canvas interface that contains a node toolbar and canvas.

If you have any feedback on additional operators that you might need, we'd love to hear it! Please contact your dbt Labs account team and share your thoughts.

#### Canvas[​](#canvas "Direct link to Canvas")

Canvas has a sleek drag-and-drop interface for creating and modifying dbt SQL models. It's like a digital whiteboard space for easily viewing and delivering trustworthy data. Use the canvas to:

* Drag-and-drop operators to create and configure your model(s)
* Generate SQL code using the built-in AI generator
* Zoom in or out for better visualization
* Version-control your dbt models
* \[Coming soon] Test and document your created models

[![The operator toolbar allows you to select different nodes to configure or perform specific tasks, like adding filters or joining models.](/img/docs/dbt-cloud/canvas/operators.png?v=2 "The operator toolbar allows you to select different nodes to configure or perform specific tasks, like adding filters or joining models.")](#)The operator toolbar allows you to select different nodes to configure or perform specific tasks, like adding filters or joining models.

##### Connector[​](#connector "Direct link to Connector")

Connectors allow you to connect your operators to create dbt models. Once you've added operators to the canvas:

* Hover over the "+" sign next to the operator and click.
* Drag your cursor between the operator's "+" start point to the other node you want to connect to. This should create a connector line.
* As an example, to create a join, connect one operator to the "L" (Left) and the other to the "R" (Right). The endpoints are located to the left of the operator so you can easily drag the connectors to the endpoint.

[![Click and drag your cursor to connect operators.](/img/docs/dbt-cloud/canvas/connector.png?v=2 "Click and drag your cursor to connect operators.")](#)Click and drag your cursor to connect operators.

#### Configuration panel[​](#configuration-panel "Direct link to Configuration panel")

Each operator has a configuration side panel that opens when you click on it. The configuration panel allows you to configure the operator, review the current model, preview changes, view the SQL code for the operator, and delete the operator.

The configuration side panel has the following:

* Configure tab — This section allows you to configure the operator to your specified requirements, such as using the built-in AI code generator to generate SQL.
* Input tab — This section allows you to view the data for the current source table. Not available for model operators.
* Output tab — This section allows you to preview the data for the modified source model.
* Code — This section allows you to view the underlying SQL code for the data transformation.

[![A sleek drag-and-drop canvas interface that allows you to create or modify dbt SQL models.](/img/docs/dbt-cloud/canvas/config-panel.png?v=2 "A sleek drag-and-drop canvas interface that allows you to create or modify dbt SQL models.")](#)A sleek drag-and-drop canvas interface that allows you to create or modify dbt SQL models.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Studio IDE keyboard shortcuts

The Studio IDE provides keyboard shortcuts, features, and development tips to help you work faster and be more productive.

Use this Studio IDE page to help you quickly reference some common operations.

| Shortcut description                                                                                                                                                                      | macOS                                                    | Windows                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------- |
| View the full list of editor shortcuts to help your development, such as adding a line comment, changing tab display size, building modified models, changing editor font size, and more. | Fn-F1                                                    | Fn-F1                           |
| Select a file to open.                                                                                                                                                                    | Command-O                                                | Control-O                       |
| Close the currently active editor tab.                                                                                                                                                    | Option-W                                                 | Alt-W                           |
| Preview code.                                                                                                                                                                             | Command-Enter                                            | Control-Enter                   |
| Compile code.                                                                                                                                                                             | Command-Shift-Enter                                      | Control-Shift-Enter             |
| Reveal a list of dbt functions in the editor.                                                                                                                                             | Enter two underscores `__`                               | Enter two underscores `__`      |
| Open the command palette to invoke dbt commands and actions.                                                                                                                              | Command-P / Command-Shift-P                              | Control-P / Control-Shift-P     |
| Multi-edit in the editor by selecting multiple lines.                                                                                                                                     | Option-Click / Shift-Option-Command / Shift-Option-Click | Hold Alt and Click              |
| Open the [**Invocation History Drawer**](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/ide-user-interface.md#invocation-history) located at the bottom of the IDE.                     | Control-backtick (or Control + \`)                       | Control-backtick (or Ctrl + \`) |
| Add a block comment to the selected code. SQL files will use the Jinja syntax `({# #})` rather than the SQL one `(/* */)`.                                                                | Shift-Option-A                                           | Shift-Alt-A                     |

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Quickstart guide](https://docs.getdbt.com/guides.md)
* [About dbt](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features.md)
* [Develop in the Cloud](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Supported browsers

To have the best experience with dbt, we recommend using the latest versions of the following browsers:

* [Google Chrome](https://www.google.com/chrome/) — Latest version is fully supported in dbt
* [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/) — Latest version is fully supported in dbt
* [Apple Safari](https://www.apple.com/safari/) — Latest version support provided on a best-effort basis
* [Microsoft Edge](https://www.microsoft.com/en-us/edge?form=MA13FJ\&exp=e00) — Latest version support provided on a best-effort basis

dbt provides two types of browser support:

* Fully supported — dbt is fully tested and supported on these browsers. Features display and work as intended.
* Best effort — You can access dbt on these browsers. Features may not display or work as intended.

You may still be able to access and use dbt even without using the latest recommended browser or an unlisted browser. However, some features might not display as intended.

note

To improve your experience using dbt, we suggest that you turn off ad blockers.

##### Browser sessions[​](#browser-sessions "Direct link to Browser sessions")

A session is a period of time during which you’re signed in to a dbt account from a browser. If you close your browser, it will end your session and log you out. You'll need to log in again the next time you try to access dbt.

If you've logged in using [SSO](https://docs.getdbt.com/docs/cloud/manage-access/sso-overview.md), you can customize your maximum session duration, which might vary depending on your identity provider (IdP).

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Tenancy

dbt is available in both single (virtual private) and multi-tenant configurations.

##### Multi-tenant[​](#multi-tenant "Direct link to Multi-tenant")

The Multi Tenant (SaaS) deployment environment refers to the SaaS dbt application hosted by dbt Labs. This is the most commonly used deployment and is completely managed and maintained by dbt Labs, the makers of dbt. As a SaaS product, a user can quickly [create an account](https://www.getdbt.com/signup/) on our North American servers and get started using the dbt and related services immediately. *If your organization requires cloud services hosted on EMEA or APAC regions*, please [contact us](https://www.getdbt.com/contact/). The deployments are hosted on AWS or Azure and are always kept up to date with the currently supported dbt versions, software updates, and bug fixes.

##### Single tenant[​](#single-tenant "Direct link to Single tenant")

The single tenant deployment environment provides a hosted alternative to the multi-tenant (SaaS) dbt environment. While still managed and maintained by dbt Labs, single tenant dbt instances provide dedicated infrastructure in a virtual private cloud (VPC) environment. This is accomplished by spinning up all the necessary infrastructure with a re-usable Infrastructure as Code (IaC) deployment built with [Terraform](https://www.terraform.io/). The single tenant infrastructure lives in a dedicated AWS or Azure account and can be customized with certain configurations, such as firewall rules, to limit inbound traffic or hosting in a specific regions.

A few common reasons for choosing a single tenant deployment over the Production SaaS product include:

* A requirement that the dbt application be hosted in a dedicated VPC that is logically separated from other customer infrastructure
* A desire for multiple isolated dbt instances for testing, development, etc

*To learn more about setting up a dbt single tenant deployment, [please contact our sales team](mailto:sales@getdbt.com).*

##### Available features[​](#available-features "Direct link to Available features")

The following table outlines which dbt features are supported on the different SaaS options available today. For more information about feature availability, please [contact us](https://www.getdbt.com/contact/).

| Feature                     | AWS Multi-tenant | AWS single tenant | Azure multi-tenant | Azure single tenant | GCP multi-tenant |
| --------------------------- | ---------------- | ----------------- | ------------------ | ------------------- | ---------------- |
| Audit logs                  | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Continuous integration jobs | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Cloud CLI                   | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Studio IDE                  | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Copilot                     | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Catalog                     | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Mesh                        | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Semantic Layer              | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Discovery API               | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| IP restrictions             | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| Orchestrator                | ✅               | ✅                | ✅                 | ✅                  | ✅               |
| PrivateLink egress          | ✅ (AWS only)    | ✅                | ✅                 | ✅                  | ✅               |
| PrivateLink ingress         | ❌               | ✅                | ❌                 | ✅                  | ✅               |
| Webhooks (Outbound)         | ✅               | ✅                | ✅                 | ❌                  | ❌               |

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### The dbt platform features

dbt platform (formerly dbt Cloud) is the fastest and most reliable way to deploy dbt. Develop, test, schedule, document, and investigate data models all in one browser-based UI.

In addition to providing a hosted architecture for running dbt across your organization, dbt comes equipped with turnkey support for scheduling jobs, CI/CD, hosting documentation, monitoring and alerting, an integrated development environment (Studio IDE), and allows you to develop and run dbt commands from your local command line interface (CLI) or code editor.

dbt's [flexible plans](https://www.getdbt.com/pricing/) and features make it well-suited for data teams of any size — sign up for your [free 14-day trial](https://www.getdbt.com/signup/)!

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md)

###### [dbt CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md)

[Use the CLI for the dbt platform to develop, test, run, and version control dbt projects and commands, directly from the command line.](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md)

###### [dbt Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md)

[The IDE is the easiest and most efficient way to develop dbt models, allowing you to build, test, run, and version control your dbt projects directly from your browser.](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/cloud/canvas.md)

###### [dbt Canvas](https://docs.getdbt.com/docs/cloud/canvas.md)

[Develop with Canvas, a seamless drag-and-drop experience that helps analysts quickly create and visualize dbt models in dbt.](https://docs.getdbt.com/docs/cloud/canvas.md)

[![](/img/icons/copilot.svg)](https://docs.getdbt.com/docs/cloud/dbt-copilot.md)

###### [dbt Copilot\*](https://docs.getdbt.com/docs/cloud/dbt-copilot.md)

[Use dbt Copilot to generate documentation, tests, semantic models, metrics, and SQL code from scratch, giving you the flexibility to modify or fix generated code.](https://docs.getdbt.com/docs/cloud/dbt-copilot.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/environments-in-dbt.md)

###### [Manage environments](https://docs.getdbt.com/docs/environments-in-dbt.md)

[Set up and manage separate production and development environments in dbt to help engineers develop and test code more efficiently, without impacting users or data.](https://docs.getdbt.com/docs/environments-in-dbt.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/job-scheduler.md)

###### [Schedule and run dbt jobs](https://docs.getdbt.com/docs/deploy/job-scheduler.md)

[Create custom schedules to run your production jobs. Schedule jobs by day of the week, time of day, or a recurring interval. Decrease operating costs by using webhooks to trigger CI jobs and the API to start jobs.](https://docs.getdbt.com/docs/deploy/job-scheduler.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/job-notifications.md)

###### [Notifications](https://docs.getdbt.com/docs/deploy/job-notifications.md)

[Set up and customize job notifications in dbt to receive email or slack alerts when a job run succeeds, fails, or is cancelled. Notifications alert the right people when something goes wrong instead of waiting for a user to report it.](https://docs.getdbt.com/docs/deploy/job-notifications.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/run-visibility.md)

###### [Run visibility](https://docs.getdbt.com/docs/deploy/run-visibility.md)

[View the history of your runs and the model timing dashboard to help identify where improvements can be made to the scheduled jobs.](https://docs.getdbt.com/docs/deploy/run-visibility.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md)

###### [Host & share documentation](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md)

[dbt hosts and authorizes access to dbt project documentation, allowing you to generate data documentation on a schedule for your project. Invite teammates to the dbt platform to collaborate and share your project's documentation.](https://docs.getdbt.com/docs/explore/build-and-view-your-docs.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/cloud/git/connect-github.md)

###### [Supports GitHub, GitLab, AzureDevOps](https://docs.getdbt.com/docs/cloud/git/connect-github.md)

[Seamlessly connect your git account to the dbt platform and provide another layer of security to dbt. Import new repositories, trigger continuous integration, clone repos using HTTPS, and more!](https://docs.getdbt.com/docs/cloud/git/connect-github.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/deploy/continuous-integration.md)

###### [Enable Continuous Integration](https://docs.getdbt.com/docs/deploy/continuous-integration.md)

[Configure dbt to run your dbt projects in a temporary schema when new commits are pushed to open pull requests. This build-on-PR functionality is a great way to catch bugs before deploying to production, and an essential tool in any analyst's belt.](https://docs.getdbt.com/docs/deploy/continuous-integration.md)

[![](/img/icons/dbt-bit.svg)](https://www.getdbt.com/security/)

###### [Security](https://www.getdbt.com/security/)

[Manage risk with SOC-2 compliance, CI/CD deployment, RBAC, and ELT architecture.](https://www.getdbt.com/security/)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures.md)

###### [Visualize and orchestrate exposures\*](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures.md)

[Configure downstream exposures automatically from dashboards and understand how models are used in downstream tools. Proactively refresh the underlying data sources during scheduled dbt jobs.](https://docs.getdbt.com/docs/cloud-integrations/downstream-exposures.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md)

###### [dbt Semantic Layer\*](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md)

[Use the dbt Semantic Layer to define metrics alongside your dbt models and query them from any integrated analytics tool. Get the same answers everywhere, every time.](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md)

###### [Discovery API\*](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md)

[Enhance your workflow and run ad-hoc queries, browse schema, or query the dbt Semantic Layer. dbt serves a GraphQL API, which supports arbitrary queries.](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/explore/explore-projects.md)

###### [dbt Catalog\*](https://docs.getdbt.com/docs/explore/explore-projects.md)

[Learn about dbt Catalog and how to interact with it to understand, improve, and leverage your data pipelines.](https://docs.getdbt.com/docs/explore/explore-projects.md)

[![](/img/icons/dbt-bit.svg)](https://docs.getdbt.com/docs/explore/dbt-insights.md)

###### [dbt Insights\*](https://docs.getdbt.com/docs/explore/dbt-insights.md)

[Learn how to query data and perform exploratory data analysis using dbt Insights.](https://docs.getdbt.com/docs/explore/dbt-insights.md)

<br />

\*These features are available on [selected plans](https://www.getdbt.com/pricing/).

#### Related docs[​](#related-docs "Direct link to Related docs")

* [dbt plans and pricing](https://www.getdbt.com/pricing/)
* [Quickstart guides](https://docs.getdbt.com/docs/get-started-dbt.md)
* [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Use dbt Copilot StarterEnterpriseEnterprise +

### Use dbt Copilot [Starter](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

Use Copilot to generate documentation, tests, semantic models, and code from scratch, giving you the flexibility to modify or fix generated code.

This page explains how to use Copilot to:

* [Generate resources](#generate-resources) — Save time by using Copilot’s generation button to generate documentation, tests, and semantic model files during your development in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md).
* [Generate and edit SQL inline](#generate-and-edit-sql-inline) — Use natural language prompts to generate SQL code from scratch or to edit existing SQL file by using keyboard shortcuts or highlighting code in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md).
* [Build visual models](#build-visual-models) — Use Copilot to generate models in [Canvas](https://docs.getdbt.com/docs/cloud/use-canvas.md) with natural language prompts.
* [Build queries](#build-queries) — Use Copilot to generate queries in [Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md) for exploratory data analysis using natural language prompts.
* [Analyze data with the Analyst agent](#analyze-data-with-the-analyst-agent) — Use Copilot to analyze your data and get contextualized results in real time by asking a natural language question to the Analyst agent.

tip

Check out our [dbt Copilot on-demand course](https://learn.getdbt.com/learn/course/dbt-copilot/welcome-to-dbt-copilot/welcome-5-mins) to learn how to use Copilot to generate resources, and more!

#### Generate resources[​](#generate-resources "Direct link to Generate resources")

Generate documentation, tests, metrics, and semantic models [resources](https://docs.getdbt.com/docs/build/projects.md) with the click-of-a-button in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md) using dbt Copilot, saving you time. To access and use this AI feature:

1. Navigate to the Studio IDE and select a SQL model file under the **File Explorer**.

2. In the **Console** section (under the **File Editor**), click **dbt Copilot** to view the available AI options.

3. Select the available options to generate the YAML config: **Generate Documentation**, **Generate Tests**, **Generate Semantic Model**, or **Generate Metrics**. To generate multiple YAML configs for the same model, click each option separately. dbt Copilot intelligently saves the YAML config in the same file.

   <!-- -->

   * To generate metrics, you need to first have semantic models defined.
   * Once defined, click **dbt Copilot** and select **Generate Metrics**.
   * Write a prompt describing the metrics you want to generate and press enter.
   * **Accept** or **Reject** the generated code.

4. Verify the AI-generated code. You can update or fix the code as needed.

5. Click **Save As**. You should see the file changes under the **Version control** section.

[![Example of using dbt Copilot to generate documentation in the IDE](/img/docs/dbt-cloud/cloud-ide/dbt-copilot-doc.gif?v=2 "Example of using dbt Copilot to generate documentation in the IDE")](#)Example of using dbt Copilot to generate documentation in the IDE

#### Generate and edit SQL inline[​](#generate-and-edit-sql-inline "Direct link to Generate and edit SQL inline")

Copilot also allows you to generate SQL code directly within the SQL file in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md), using natural language prompts. This means you can rewrite or add specific portions of the SQL file without needing to edit the entire file.

This intelligent AI tool streamlines SQL development by reducing errors, scaling effortlessly with complexity, and saving valuable time. Copilot's [prompt window](#use-the-prompt-window), accessible by keyboard shortcut, handles repetitive or complex SQL generation effortlessly so you can focus on high-level tasks.

Use Copilot's prompt window for use cases like:

* Writing advanced transformations
* Performing bulk edits efficiently
* Crafting complex patterns like regex

##### Use the prompt window[​](#use-the-prompt-window "Direct link to Use the prompt window")

Access Copilot's AI prompt window using the keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows) to:

###### 1. Generate SQL from scratch[​](#1-generate-sql-from-scratch "Direct link to 1. Generate SQL from scratch")

* Use the keyboard shortcuts Cmd+B (Mac) or Ctrl+B (Windows) to generate SQL from scratch.
* Enter your instructions to generate SQL code tailored to your needs using natural language.
* Ask Copilot to fix the code or add a specific portion of the SQL file.

[![dbt Copilot's prompt window accessible by keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows)](/img/docs/dbt-cloud/cloud-ide/copilot-sql-generation-prompt.png?v=2 "dbt Copilot's prompt window accessible by keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows)")](#)dbt Copilot's prompt window accessible by keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows)

###### 2. Edit existing SQL code[​](#2-edit-existing-sql-code "Direct link to 2. Edit existing SQL code")

* Highlight a section of SQL code and press Cmd+B (Mac) or Ctrl+B (Windows) to open the prompt window for editing.
* Use this to refine or modify specific code snippets based on your needs.
* Ask Copilot to fix the code or add a specific portion of the SQL file.

###### 3. Review changes with the diff view to quickly assess the impact of the changes before making changes[​](#3-review-changes-with-the-diff-view-to-quickly-assess-the-impact-of-the-changes-before-making-changes "Direct link to 3. Review changes with the diff view to quickly assess the impact of the changes before making changes")

* When a suggestion is generated, Copilot displays a visual "diff" view to help you compare the proposed changes with your existing code:

  <!-- -->

  * **Green**: Means new code that will be added if you accept the suggestion.
  * **Red**: Highlights existing code that will be removed or replaced by the suggested changes.

###### 4. Accept or reject suggestions[​](#4-accept-or-reject-suggestions "Direct link to 4. Accept or reject suggestions")

* **Accept**: If the generated SQL meets your requirements, click the **Accept** button to apply the changes directly to your `.sql` file directly in the IDE.
* **Reject**: If the suggestion don’t align with your request/prompt, click **Reject** to discard the generated SQL without making changes and start again.

###### 5. Regenerate code[​](#5-regenerate-code "Direct link to 5. Regenerate code")

* To regenerate, press the **Escape** button on your keyboard (or click the Reject button in the popup). This will remove the generated code and puts your cursor back into the prompt text area.
* Update your prompt and press **Enter** to try another generation. Press **Escape** again to close the popover entirely.

Once you've accepted a suggestion, you can continue to use the prompt window to generate additional SQL code and commit your changes to the branch.

[![Edit existing SQL code using dbt Copilot's prompt window accessible by keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows)](/img/docs/dbt-cloud/cloud-ide/copilot-sql-generation.gif?v=2 "Edit existing SQL code using dbt Copilot's prompt window accessible by keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows)")](#)Edit existing SQL code using dbt Copilot's prompt window accessible by keyboard shortcut Cmd+B (Mac) or Ctrl+B (Windows)

#### Build visual models[​](#build-visual-models "Direct link to Build visual models")

Copilot seamlessly integrates with the [Canvas](https://docs.getdbt.com/docs/cloud/canvas.md), a drag-and-drop experience that helps you build your visual models using natural language prompts. Before you begin, make sure you can [access the Canvas](https://docs.getdbt.com/docs/cloud/use-canvas.md#access-canvas).

To begin building models with natural language prompts in the Canvas:

1. Click on the **dbt Copilot** icon in Canvas menu.

2. In the dbt Copilot prompt box, enter your prompt in natural language for Copilot to build the model(s) you want. You can also reference existing models using the `@` symbol. For example, to build a model that calculates the total price of orders, you can enter `@orders` in the prompt and it'll pull in and reference the `orders` model.

3. Click **Generate** and dbt Copilot generates a summary of the model(s) you want to build.

   <!-- -->

   * To start over, click on the **+** icon. To close the prompt box, click **X**.

   [![Enter a prompt in the dbt Copilot prompt box to build models using natural language](/img/docs/dbt-cloud/copilot-generate.jpg?v=2 "Enter a prompt in the dbt Copilot prompt box to build models using natural language")](#)Enter a prompt in the dbt Copilot prompt box to build models using natural language

4. Click **Apply** to generate the model(s) in the Canvas.

5. dbt Copilot displays a visual "diff" view to help you compare the proposed changes with your existing code. Review the diff view in the canvas to see the generated operators built byCopilot:

   <!-- -->

   * White: Located in the top of the canvas and means existing set up or blank canvas that will be removed or replaced by the suggested changes.
   * Green: Located in the bottom of the canvas and means new code that will be added if you accept the suggestion. <br />

   [![Visual diff view of proposed changes](/img/docs/dbt-cloud/copilot-diff.jpg?v=2 "Visual diff view of proposed changes")](#)Visual diff view of proposed changes

6. Reject or accept the suggestions

7. In the **generated** operator box, click the play icon to preview the data

8. Confirm the results or continue building your model.
   <!-- -->
   [![Use the generated operator with play icon to preview the data](/img/docs/dbt-cloud/copilot-output.jpg?v=2 "Use the generated operator with play icon to preview the data")](#)Use the generated operator with play icon to preview the data

9. To edit the generated model, open **Copilot** prompt box and type your edits.

10. Click **Submit** and Copilot will generate the revised model. Repeat steps 5-8 until you're happy with the model.

#### Build queries[​](#build-queries "Direct link to Build queries")

Use Copilot to build queries in [Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md) with natural language prompts to seamlessly explore and query data with an intuitive, context-rich interface. Before you begin, make sure you can [access Insights](https://docs.getdbt.com/docs/explore/access-dbt-insights.md).

To begin building SQL queries with natural language prompts in Insights:

1. Click the **Copilot** icon in the Query console sidebar menu.

2. Click **Generate SQL**.

3. In the dbt Copilot prompt box, enter your prompt in natural language for dbt Copilot to build the SQL query you want.

4. Click **↑** to submit your prompt. Copilot generates a summary of the SQL query you want to build. To clear the prompt, click on the **Clear** button. To close the prompt box, click the Copilot icon again.

5. Copilot will automatically generate the SQL with an explanation of the query.

   <!-- -->

   * Click **Add** to add the generated SQL to the existing query.
   * Click **Replace** to replace the existing query with the generated SQL.

6. In the **Query console menu**, click the **Run** button to preview the data.

7. Confirm the results or continue building your model.

[![dbt Copilot in dbt Insights](/img/docs/dbt-insights/insights-copilot.gif?v=2 "dbt Copilot in dbt Insights")](#)dbt Copilot in dbt Insights

#### Analyze data with the Analyst agent [Private beta](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")[​](#analyze-data-with-the-analyst-agent- "Direct link to analyze-data-with-the-analyst-agent-")

Use dbt Copilot to analyze your data and get contextualized results in real time by asking natural language questions to the [Insights](https://docs.getdbt.com/docs/explore/dbt-insights.md) Analyst agent. To request access to the Analyst agent, [join the waitlist](https://www.getdbt.com/product/dbt-agents#dbt-Agents-signup).

Before you begin, make sure you can [access Insights](https://docs.getdbt.com/docs/explore/access-dbt-insights.md).

1. Click the **Copilot** icon in the Query console sidebar menu.

2. Click **Agent**.

3. In the dbt Copilot prompt box, enter your question.

4. Click **↑** to submit your question.

   The agent then translates natural language questions into structured queries, executes queries against governed dbt models and metrics, and returns results with references, assumptions, and possible next steps.

   The agent can loop through these steps multiple times if it hasn't reached a complete answer, allowing for complex, multi-step analysis.⁠

5. Confirm the results or continue asking the agent for more insights about your data.

Your conversation with the agent remains even if you switch tabs within dbt Insights. However, they disappear when you navigate out of Insights or when you close your browser.

[![Using the Analyst agent in Insights](/img/docs/dbt-insights/insights-copilot-agent.png?v=2 "Using the Analyst agent in Insights")](#)Using the Analyst agent in Insights

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Using defer in dbt

[Defer](https://docs.getdbt.com/reference/node-selection/defer.md) is a powerful feature that allows developers to only build and run and test models they've edited without having to first run and build all the models that come before them (upstream parents). dbt powers this by using a production manifest for comparison, and resolves the `{{ ref() }}` function with upstream production artifacts.

Both the Studio IDE and the dbt CLI enable users to natively defer to production metadata directly in their development workflows.

[![Use 'defer' to modify end-of-pipeline models by pointing to production models, instead of running everything upstream.](/img/docs/reference/defer-diagram.png?v=2 "Use 'defer' to modify end-of-pipeline models by pointing to production models, instead of running everything upstream.")](#)Use 'defer' to modify end-of-pipeline models by pointing to production models, instead of running everything upstream.

When using `--defer`, dbt will follow this order of execution for resolving the `{{ ref() }}` functions.

1. If a development version of a deferred relation exists, dbt preferentially uses the development database location when resolving the reference.
2. If a development version doesn't exist, dbt uses the staging locations of parent relations based on metadata from the staging environment.
3. If no development version and no staging environment exist, dbt uses the production locations of parent relations based on metadata from the production environment. Note that dbt only defers to one environment per invocation — either staging or production.

**Note:** Passing the `--favor-state` flag will always resolve refs using staging metadata if available; otherwise, it defaults to production metadata regardless of the presence of a development relation, skipping step #1.

For a clean slate, it's a good practice to drop the development schema at the start and end of your development cycle.

If you require additional controls over production data, create a [Staging environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md#staging-environment) and dbt will use that, rather than the Production environment, to resolve `{{ ref() }}` functions.

#### Required setup[​](#required-setup "Direct link to Required setup")

* You must select the **[Production environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md#set-as-production-environment)** checkbox in the **Environment Settings** page.
  <!-- -->
  * This can be set for one deployment environment per dbt project.
* You must have a successful job run first.

When using defer, it compares artifacts from the most recent successful production job, excluding CI jobs.

##### Defer in the dbt IDE[​](#defer-in-the-dbt-ide "Direct link to Defer in the dbt IDE")

To use deferral in the Studio IDE, you must have production artifacts generated by a deploy job. dbt will first check for these artifacts in your Staging environment (if available), or else in the Production environment.

The defer feature in the Studio IDE won't work if a Staging environment exists but no deploy job has run. This is because the necessary metadata to power defer won't exist until a deploy job has run successfully in the Staging environment.

To enable defer in the Studio IDE, toggle the **Defer to staging/production** button on the command bar. Once enabled, dbt will:

1. Pull down the most recent manifest from the Staging or Production environment for comparison
2. Pass the `--defer` flag to the command (for any command that accepts the flag)

For example, if you were to start developing on a new branch with [nothing in your development schema](https://docs.getdbt.com/reference/node-selection/defer.md#usage), edit a single model, and run `dbt build -s state:modified` — only the edited model would run. Any `{{ ref() }}` functions will point to the staging or production location of the referenced models.

[![Select the 'Defer to production' toggle on the bottom right of the command bar to enable defer in the Studio IDE.](/img/docs/dbt-cloud/defer-toggle.png?v=2 "Select the 'Defer to production' toggle on the bottom right of the command bar to enable defer in the Studio IDE.")](#)Select the 'Defer to production' toggle on the bottom right of the command bar to enable defer in the Studio IDE.

##### Defer in dbt CLI[​](#defer-in-dbt-cli "Direct link to Defer in dbt CLI")

One key difference between using `--defer` in the Cloud CLI and the Studio IDE is that `--defer` is *automatically* enabled in the Cloud CLI for all invocations, compared with production artifacts. You can disable it with the `--no-defer` flag.

The Cloud CLI offers additional flexibility by letting you choose the source environment for deferral artifacts. You can manually set a `defer-env-id` key in either your `dbt_project.yml` or `dbt_cloud.yml` file. By default, the Cloud CLI will prefer metadata from the project's "Staging" environment (if defined), otherwise "Production."

dbt\_cloud.yml
```

Example 2 (unknown):
```unknown
dbt\_project.yml
```

Example 3 (unknown):
```unknown
#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

## Reference

### .dbtignore

You can create a `.dbtignore` file in the root of your [dbt project](https://docs.getdbt.com/docs/build/projects.md) to specify files that should be **entirely** ignored by dbt. The file behaves like a [`.gitignore` file, using the same syntax](https://git-scm.com/docs/gitignore). Files and subdirectories matching the pattern will not be read, parsed, or otherwise detected by dbt—as if they didn't exist.

**Examples**

.dbtignore
```

---

## Update lines 34 and 35

**URL:** llms-txt#update-lines-34-and-35

**Contents:**
  - Analyze your data in dbt
  - Browse our guides
  - Browse our guides
  - Build a data lakehouse with dbt Core and Dremio Cloud
  - Build, test, document, and promote adapters

ACCOUNT_ID = "16173"
JOB_ID = "65767"

$ astrocloud dev stop

[+] Running 3/3
 ⠿ Container airflow-dbt-cloud_e3fe3c-webserver-1  Stopped    7.5s
 ⠿ Container airflow-dbt-cloud_e3fe3c-scheduler-1  Stopped    3.3s
 ⠿ Container airflow-dbt-cloud_e3fe3c-postgres-1   Stopped    0.3s

Name                                    State   Ports
airflow-dbt-cloud_e3fe3c-webserver-1    exited
airflow-dbt-cloud_e3fe3c-scheduler-1    exited
airflow-dbt-cloud_e3fe3c-postgres-1     exited

select 
    date_trunc('month', first_ordered_at) as month,
    count(customer_id) as new_customers
from {{ ref('customers') }}
where 
    date_part('year', first_ordered_at) = date_part('year', current_date) - 1
    and customer_type = 'new'
group by 1
order by 1;

select 
    date_trunc('month', first_ordered_at) as month,
    count(customer_id) as new_customers
from {{ ref('customers') }}
where 
    date_part('year', first_ordered_at) = 2024
    and customer_type = 'new'
group by 1
order by 1;

$ python3 --version
Python 3.11.4 # Must be Python 3

$ dbt --version
Core:
  - installed: 1.5.0 # Must be 1.5 or newer
  - latest:    1.6.3 - Update available!

Your version of dbt-core is out of date!
  You can find instructions for upgrading here:
  https://docs.getdbt.com/docs/installation

Plugins:
  - dremio: 1.5.0 - Up to date! # Must be 1.5 or newer

PATTERN = re.compile(r"""((?:[^."']|"[^"]*"|'[^']*')+)""")
return ".".join(PATTERN.split(identifier)[1::2])

def quoted_by_component(self, identifier, componentName):
        if componentName == ComponentName.Schema:
            PATTERN = re.compile(r"""((?:[^."']|"[^"]*"|'[^']*')+)""")
            return ".".join(PATTERN.split(identifier)[1::2])
        else:
            return self.quoted(identifier)

dremioSamples:
  outputs:
    cloud_dev:
      dremio_space: dev
      dremio_space_folder: no_schema
      object_storage_path: dev
      object_storage_source: $scratch
      pat: <this_is_the_personal_access_token>
      cloud_host: api.dremio.cloud
      cloud_project_id: <id_of_project_you_belong_to>
      threads: 1
      type: dremio
      use_ssl: true
      user: <your_username>
  target: dev

$ dbt run -t cloud_dev

17:24:16  Running with dbt=1.5.0
17:24:17  Found 5 models, 0 tests, 0 snapshots, 0 analyses, 348 macros, 0 operations, 0 seed files, 2 sources, 0 exposures, 0 metrics, 0 groups
17:24:17
17:24:29  Concurrency: 1 threads (target='cloud_dev')
17:24:29
17:24:29  1 of 5 START sql view model Preparation.trips .................................. [RUN]
17:24:31  1 of 5 OK created sql view model Preparation. trips ............................. [OK in 2.61s]
17:24:31  2 of 5 START sql view model Preparation.weather ................................ [RUN]
17:24:34  2 of 5 OK created sql view model Preparation.weather ........................... [OK in 2.15s]
17:24:34  3 of 5 START sql view model Business.Transportation.nyc_trips .................. [RUN]
17:24:36  3 of 5 OK created sql view model Business.Transportation.nyc_trips ............. [OK in 2.18s]
17:24:36  4 of 5 START sql view model Business.Weather.nyc_weather ....................... [RUN]
17:24:38  4 of 5 OK created sql view model Business.Weather.nyc_weather .................. [OK in 2.09s]
17:24:38  5 of 5 START sql view model Application.nyc_trips_with_weather ................. [RUN]
17:24:41  5 of 5 OK created sql view model Application.nyc_trips_with_weather ............ [OK in 2.74s]
17:24:41
17:24:41  Finished running 5 view models in 0 hours 0 minutes and 24.03 seconds (24.03s).
17:24:41
17:24:41  Completed successfully
17:24:41
17:24:41  Done. PASS=5 WARN=0 ERROR=0 SKIP=0 TOTAL=5

SELECT vendor_id,
       AVG(tip_amount)
FROM dev.application."nyc_treips_with_weather"
GROUP BY vendor_id

$ cookiecutter gh:dbt-labs/dbt-database-adapter-scaffold

from dataclasses import dataclass
from typing import Optional

from dbt.adapters.base import Credentials

@dataclass
class MyAdapterCredentials(Credentials):
    host: str
    port: int = 1337
    username: Optional[str] = None
    password: Optional[str] = None

@property
    def type(self):
        return 'myadapter'

@property
    def unique_field(self):
        """
        Hashed and included in anonymous telemetry to track adapter adoption.
        Pick a field that can uniquely identify one team/organization building with this adapter
        """
        return self.host

def _connection_keys(self):
        """
        List of keys to display in the `dbt debug` output.
        """
        return ('host', 'port', 'database', 'username')

@dataclass
class MyAdapterCredentials(Credentials):
    host: str
    port: int = 1337
    username: Optional[str] = None
    password: Optional[str] = None

ALIASES = {
        'collection': 'database',
    }

@classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection

credentials = connection.credentials

try:
            handle = myadapter_library.connect(
                host=credentials.host,
                port=credentials.port,
                username=credentials.username,
                password=credentials.password,
                catalog=credentials.database
            )
            connection.state = 'open'
            connection.handle = handle
        return connection

@classmethod
    def get_response(cls, cursor) -> AdapterResponse:
        code = cursor.sqlstate or "OK"
        rows = cursor.rowcount
        status_message = f"{code} {rows}"
        return AdapterResponse(
            _message=status_message,
            code=code,
            rows_affected=rows
        )

def cancel(self, connection):
        tid = connection.handle.transaction_id()
        sql = 'select cancel_transaction({})'.format(tid)
        logger.debug("Cancelling query '{}' ({})".format(connection_name, pid))
        _, cursor = self.add_query(sql, 'master')
        res = cursor.fetchone()
        logger.debug("Canceled query '{}': {}".format(connection_name, res))

@contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except myadapter_library.DatabaseError as exc:
            self.release(connection_name)

logger.debug('myadapter error: {}'.format(str(e)))
            raise dbt.exceptions.DatabaseException(str(exc))
        except Exception as exc:
            logger.debug("Error running SQL: {}".format(sql))
            logger.debug("Rolling back transaction.")
            self.release(connection_name)
            raise dbt.exceptions.RuntimeException(str(exc))

@available
    def standardize_grants_dict(self, grants_table: agate.Table) -> dict:
        """
        :param grants_table: An agate table containing the query result of
            the SQL returned by get_show_grant_sql
        :return: A standardized dictionary matching the `grants` config
        :rtype: dict
        """
        grants_dict: Dict[str, List[str]] = {}
        for row in grants_table:
            grantee = row["grantee"]
            privilege = row["privilege_type"]
            if privilege in grants_dict.keys():
                grants_dict[privilege].append(grantee)
            else:
                grants_dict.update({privilege: [grantee]})
        return grants_dict

@classmethod
    def date_function(cls):
        return 'datenow()'

{# dbt will call this macro by name, providing any arguments #}
{% macro create_table_as(temporary, relation, sql) -%}

{# dbt will dispatch the macro call to the relevant macro #}
  {{ return(
      adapter.dispatch('create_table_as')(temporary, relation, sql)
     ) }}
{%- endmacro %}

{# If no macro matches the specified adapter, "default" will be used #}
{% macro default__create_table_as(temporary, relation, sql) -%}
   ...
{%- endmacro %}

{# Example which defines special logic for Redshift #}
{% macro redshift__create_table_as(temporary, relation, sql) -%}
   ...
{%- endmacro %}

{# Example which defines special logic for BigQuery #}
{% macro bigquery__create_table_as(temporary, relation, sql) -%}
   ...
{%- endmacro %}

def drop_schema(self, relation: BaseRelation):
        relations = self.list_relations(
            database=relation.database,
            schema=relation.schema
        )
        for relation in relations:
            self.drop_relation(relation)
        super().drop_schema(relation)

class ABCAdapter(BaseAdapter):
    ...
    @property
    def _behavior_flags(self) -> List[BehaviorFlag]:
        return [
            {
                "name": "enable_new_functionality_requiring_higher_permissions",
                "default": False,
                "source": "dbt-abc",
                "description": (
                    "The dbt-abc adapter is implementing a new method for sourcing metadata. "
                    "This is a more performant way for dbt to source metadata but requires higher permissions on the platform. "
                    "Enabling this without granting the requisite permissions will result in an error. "
                    "This feature is expected to be required by Spring 2025."
                ),
                "docs_url": "https://docs.getdbt.com/reference/global-configs/behavior-changes#abc-enable_new_functionality_requiring_higher_permissions",
            }
        ]

class ABCAdapter(BaseAdapter):
    ...
    def some_method(self, *args, **kwargs):
        if self.behavior.enable_new_functionality_requiring_higher_permissions:
            # do the new thing
        else:
            # do the old thing

{% macro some_macro(**kwargs) %}
    {% if adapter.behavior.enable_new_functionality_requiring_higher_permissions %}
        {# do the new thing #}
    {% else %}
        {# do the old thing #}
    {% endif %}
{% endmacro %}

class ABCAdapter(BaseAdapter):
        ...
        def some_method(self, *args, **kwargs):
            if self.behavior.enable_new_functionality_requiring_higher_permissions.no_warn:
                # do the new thing
            else:
                # do the old thing

{% macro some_macro(**kwargs) %}
    {% if adapter.behavior.enable_new_functionality_requiring_higher_permissions.no_warn %}
        {# do the new thing #}
    {% else %}
        {# do the old thing #}
    {% endif %}
{% endmacro %}

**Examples:**

Example 1 (unknown):
```unknown
#### Run the Airflow DAG[​](#run-the-airflow-dag "Direct link to Run the Airflow DAG")

Turn on the DAG and trigger it to run. Verify the job succeeded after running.

![Airflow DAG](/assets/images/airflow-dag-d7d6a6fe556ac6e8a7970ae7305a5bc3.png)

Click **Monitor Job Run** to open the run details in dbt. ![Task run instance](/assets/images/task-run-instance-936ac2e4ef47727b434363656900a99d.png)

#### Cleaning up[​](#cleaning-up "Direct link to Cleaning up")

At the end of this guide, make sure you shut down your docker container. When you’re done using Airflow, use the following command to stop the container:
```

Example 2 (unknown):
```unknown
To verify that the deployment has stopped, use the following command:
```

Example 3 (unknown):
```unknown
This should give you an output like this:
```

Example 4 (unknown):
```unknown
#### Frequently asked questions[​](#frequently-asked-questions "Direct link to Frequently asked questions")

##### How can we run specific subsections of the dbt DAG in Airflow?[​](#how-can-we-run-specific-subsections-of-the-dbt-dag-in-airflow "Direct link to How can we run specific subsections of the dbt DAG in Airflow?")

Because the Airflow DAG references dbt jobs, your analytics engineers can take responsibility for configuring the jobs in dbt.

For example, to run some models hourly and others daily, there will be jobs like `Hourly Run` or `Daily Run` using the commands `dbt run --select tag:hourly` and `dbt run --select tag:daily` respectively. Once configured in dbt, these can be added as steps in an Airflow DAG as shown in this guide. Refer to our full [node selection syntax docs here](https://docs.getdbt.com/reference/node-selection/syntax.md).

##### How can I re-run models from the point of failure?[​](#how-can-i-re-run-models-from-the-point-of-failure "Direct link to How can I re-run models from the point of failure?")

You can trigger re-run from point of failure with the `rerun` API endpoint. See the docs on [retrying jobs](https://docs.getdbt.com/docs/deploy/retry-jobs.md) for more information.

##### Should Airflow run one big dbt job or many dbt jobs?[​](#should-airflow-run-one-big-dbt-job-or-many-dbt-jobs "Direct link to Should Airflow run one big dbt job or many dbt jobs?")

dbt jobs are most effective when a build command contains as many models at once as is practical. This is because dbt manages the dependencies between models and coordinates running them in order, which ensures that your jobs can run in a highly parallelized fashion. It also streamlines the debugging process when a model fails and enables re-run from point of failure.

As an explicit example, it's not recommended to have a dbt job for every single node in your DAG. Try combining your steps according to desired run frequency, or grouping by department (finance, marketing, customer success...) instead.

##### We want to kick off our dbt jobs after our ingestion tool (such as Fivetran) / data pipelines are done loading data. Any best practices around that?[​](#we-want-to-kick-off-our-dbt-jobs-after-our-ingestion-tool-such-as-fivetran--data-pipelines-are-done-loading-data-any-best-practices-around-that "Direct link to We want to kick off our dbt jobs after our ingestion tool (such as Fivetran) / data pipelines are done loading data. Any best practices around that?")

Astronomer's DAG registry has a sample workflow combining Fivetran, dbt and Census [here](https://registry.astronomer.io/dags/fivetran-dbt_cloud-census/versions/3.0.0).

##### How do you set up a CI/CD workflow with Airflow?[​](#how-do-you-set-up-a-cicd-workflow-with-airflow "Direct link to How do you set up a CI/CD workflow with Airflow?")

Check out these two resources for accomplishing your own CI/CD pipeline:

* [Continuous Integration with dbt](https://docs.getdbt.com/docs/deploy/continuous-integration.md)
* [Astronomer's CI/CD Example](https://docs.astronomer.io/software/ci-cd/#example-cicd-workflow)

##### Can dbt dynamically create tasks in the DAG like Airflow can?[​](#can-dbt-dynamically-create-tasks-in-the-dag-like-airflow-can "Direct link to Can dbt dynamically create tasks in the DAG like Airflow can?")

As discussed above, we prefer to keep jobs bundled together and containing as many nodes as are necessary. If you must run nodes one at a time for some reason, then review [this article](https://www.astronomer.io/blog/airflow-dbt-1/) for some pointers.

##### Can you trigger notifications if a dbt job fails with Airflow?[​](#can-you-trigger-notifications-if-a-dbt-job-fails-with-airflow "Direct link to Can you trigger notifications if a dbt job fails with Airflow?")

Yes, either through [Airflow's email/slack](https://www.astronomer.io/guides/error-notifications-in-airflow/) functionality, or [dbt's notifications](https://docs.getdbt.com/docs/deploy/job-notifications.md), which support email and Slack notifications. You could also create a [webhook](https://docs.getdbt.com/docs/deploy/webhooks.md).

##### How should I plan my dbt + Airflow implementation?[​](#how-should-i-plan-my-dbt--airflow-implementation "Direct link to How should I plan my dbt + Airflow implementation?")

Check out [this recording](https://www.youtube.com/watch?v=n7IIThR8hGk) of a dbt meetup for some tips.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Analyze your data in dbt

Start with a stakeholder question and analyze the data to answer that question without writing any SQL

[Back to guides](https://docs.getdbt.com/guides.md)

analyst

dbt platform

Quickstart

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

As a data analyst, you play a key role in transforming complex data into trusted, actionable insights for your team. With dbt, you can use built-in, AI-powered tools to build governed data models, explore how they’re built, and even run your own analysis.

In this quickstart, you’ll learn how to:

* Use Catalog to browse and understand data models across both dbt and Snowflake data assets
* Use Insights to run queries for exploring and validating your data
* Use Canvas to visually build your own data models
* Build confidence using dbt as your workspace enhanced with AI

Here's more about the tools you will use on your journey:

* Catalog: View your project's resources (such as models, tests, and metrics), their lineage, and query patterns to gain a better understanding of its latest production state.
* Insights: Explore, validate, and query data with an intuitive, context-rich interface that bridges technical and business users by combining metadata, documentation, AI-assisted tools, and powerful querying capabilities.
* Canvas: Quickly access and transform data through a visual, drag-and-drop experience and with a built-in AI for custom code generation.

#### Prerequisites[​](#prerequisites "Direct link to Prerequisites")

Before you begin, make sure:

* You have access to and credentials configured for a dbt project
* Your team has already run a successful dbt job, so models are built and ready
* You have a a git provider connected and authenticated

#### Analyst workflows[​](#analyst-workflows "Direct link to Analyst workflows")

Kimiko, an analyst at the Jaffle Shop, notices they've been doing a lot of new sales and wants to investigate the most critical data they have in their warehouse.

**Question: A stakeholder is curious how many customers you've acquired month by month, in the last 12 months.**

Kimiko wonders, "How do I find data in our project that will help me answer their question?"

##### Explore a stakeholder question[​](#explore-a-stakeholder-question "Direct link to Explore a stakeholder question")

She navigates to the data catalog, Catalog, by signing into dbt and clicking Catalog in the left panel. Because the question was about customers, Kimiko begins by searching for "customers" in Catalog:

[![Catalog search for customers](/img/guides/analyst-qs/catalog-search.png?v=2 "Catalog search for customers")](#)Catalog search for customers

She finds a "customers" model, which might be what she needs. She clicks **customers** to open the model. The description reads, “Customer overview data Mart offering key details for each unique customer, one row per customer.”

Next, Kimiko selects **Columns** to see which columns this model uses.

[![Columns in customers table](/img/guides/analyst-qs/columns.png?v=2 "Columns in customers table")](#)Columns in customers table

She notices these columns: `customer_ID`, `customer_names`, and `first_ordered_at`.

The `first_ordered_at` column stands out to Kimiko, and she wonders if she might use it to see how many customers they've acquired based on when they placed their first order.

But first, she decides to interact with the data to learn more.

##### Query data in Insights[​](#query-data-in-insights "Direct link to Query data in Insights")

From the **Customer model page** in Catalog, Kimiko selects **Analyze data** from the **Open in...** dropdown. This enables her to query data for the Customer model. Once opened, Insights contains a query poised and ready to run.

[![Open query](/img/guides/analyst-qs/query.png?v=2 "Open query")](#)Open query

When Kimiko runs the query, she can look at the data underyling it. The same context she saw in Catalog she now sees in her SQL editing experience.

As she looks through the data, she sees information about each customer. She also notices the `first_ordered_at` column. Kimiko wants to code the query but her SQL is a little rusty so she uses natural language in dbt Copilot:

*How many new customers did we get in each month last year? I'd like to use my customer model and the first ordered at field to do this analysis.*

dbt Copilot writes SQL that Kimiko decides to use:
```

---

## ignore all .py files

**URL:** llms-txt#ignore-all-.py-files

---

## Access secret credentials

**URL:** llms-txt#access-secret-credentials

secret_store = StoreClient('YOUR_STORAGE_SECRET_HERE')
hook_secret = secret_store.get('DBT_WEBHOOK_KEY')
server_url = secret_store.get('TABLEAU_SITE_URL')
server_name = secret_store.get('TABLEAU_SITE_NAME')
pat_name = secret_store.get('TABLEAU_API_TOKEN_NAME')
pat_secret = secret_store.get('TABLEAU_API_TOKEN_SECRET')

#Enter the name of the workbook to refresh
workbook_name = "YOUR_WORKBOOK_NAME"
api_version = "ENTER_COMPATIBLE_VERSION"

#Validate authenticity of webhook coming from <Constant name="cloud" />
auth_header = input_data['auth_header']
raw_body = input_data['raw_body']

signature = hmac.new(hook_secret.encode('utf-8'), raw_body.encode('utf-8'), hashlib.sha256).hexdigest()

if signature != auth_header:
raise Exception("Calculated signature doesn't match contents of the Authorization header. This webhook may not have been sent from <Constant name="cloud" />.")

full_body = json.loads(raw_body)
hook_data = full_body['data']

if hook_data['runStatus'] == "Success":

#Authenticate with Tableau Server to get an authentication token
auth_url = f"{server_url}/api/{api_version}/auth/signin"
auth_data = {
    "credentials": {
        "personalAccessTokenName": pat_name,
        "personalAccessTokenSecret": pat_secret,
        "site": {
            "contentUrl": server_name
        }
    }
}
auth_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
auth_response = requests.post(auth_url, data=json.dumps(auth_data), headers=auth_headers)

#Extract token to use for subsequent calls
auth_token = auth_response.json()["credentials"]["token"]
site_id = auth_response.json()["credentials"]["site"]["id"]

#Extract the workbook ID
workbooks_url = f"{server_url}/api/{api_version}/sites/{site_id}/workbooks"
workbooks_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Tableau-Auth": auth_token
}
workbooks_params = {
    "filter": f"name:eq:{workbook_name}"
}
workbooks_response = requests.get(workbooks_url, headers=workbooks_headers, params=workbooks_params)

#Assign workbook ID
workbooks_data = workbooks_response.json()
workbook_id = workbooks_data["workbooks"]["workbook"][0]["id"]

---

## my test_is_valid_email_address unit test will run on ONLY version 2 of my_model

**URL:** llms-txt#my-test_is_valid_email_address-unit-test-will-run-on-only-version-2-of-my_model

unit_tests:
  - name: test_is_valid_email_address 
    model: my_model 
    versions:
      include: 
        - 2
    ...

---

## Query the API

**URL:** llms-txt#query-the-api

def query_discovery_api(auth_token, gql_query, variables):
    response = requests.post('https://metadata.cloud.getdbt.com/graphql',
        headers={"authorization": "Bearer "+auth_token, "content-type": "application/json"},
        json={"query": gql_query, "variables": variables})
    data = response.json()['data']

---

## Snapshots require access to the Delta file format, available on our Databricks connection,

**URL:** llms-txt#snapshots-require-access-to-the-delta-file-format,-available-on-our-databricks-connection,

---

## └── events

**URL:** llms-txt#└──-events

---

## run all models that generated errors on the prior invocation of dbt run

**URL:** llms-txt#run-all-models-that-generated-errors-on-the-prior-invocation-of-dbt-run

dbt run --select "result:error" --state path/to/artifacts

---

## inspect the results

**URL:** llms-txt#inspect-the-results

for r in res.result:
    print(f"{r.node.name}: {r.status}")

from dbt.cli.main import dbtRunner, dbtRunnerResult
from dbt.contracts.graph.manifest import Manifest

**Examples:**

Example 1 (unknown):
```unknown
#### Parallel execution not supported[​](#parallel-execution-not-supported "Direct link to Parallel execution not supported")

[`dbt-core`](https://pypi.org/project/dbt-core/) doesn't support [safe parallel execution](https://docs.getdbt.com/reference/dbt-commands.md#parallel-execution) for multiple invocations in the same process. This means it's not safe to run multiple dbt commands concurrently. It's officially discouraged and requires a wrapping process to handle sub-processes. This is because:

* Running concurrent commands can unexpectedly interact with the data platform. For example, running `dbt run` and `dbt build` for the same models simultaneously could lead to unpredictable results.
* Each `dbt-core` command interacts with global Python variables. To ensure safe operation, commands need to be executed in separate processes, which can be achieved using methods like spawning processes or using tools like Celery.

To run [safe parallel execution](https://docs.getdbt.com/reference/dbt-commands.md#available-commands), you can use the [dbt CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md) or [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md), both of which does that additional work to manage concurrency (multiple processes) on your behalf.

#### `dbtRunnerResult`[​](#dbtrunnerresult "Direct link to dbtrunnerresult")

Each command returns a `dbtRunnerResult` object, which has three attributes:

* `success` (bool): Whether the command succeeded.
* `result`: If the command completed (successfully or with handled errors), its result(s). Return type varies by command.
* `exception`: If the dbt invocation encountered an unhandled error and did not complete, the exception it encountered.

There is a 1:1 correspondence between [CLI exit codes](https://docs.getdbt.com/reference/exit-codes.md) and the `dbtRunnerResult` returned by a programmatic invocation:

| Scenario                                                                                    | CLI Exit Code | `success` | `result`          | `exception` |
| ------------------------------------------------------------------------------------------- | ------------- | --------- | ----------------- | ----------- |
| Invocation completed without error                                                          | 0             | `True`    | varies by command | `None`      |
| Invocation completed with at least one handled error (e.g. test failure, model build error) | 1             | `False`   | varies by command | `None`      |
| Unhandled error. Invocation did not complete, and returns no results.                       | 2             | `False`   | `None`            | Exception   |

#### Commitments & Caveats[​](#commitments--caveats "Direct link to Commitments & Caveats")

From dbt Core v1.5 onward, we making an ongoing commitment to providing a Python entry point at functional parity with dbt Core's CLI. We reserve the right to change the underlying implementation used to achieve that goal. We expect that the current implementation will unlock real use cases, in the short & medium term, while we work on a set of stable, long-term interfaces that will ultimately replace it.

In particular, the objects returned by each command in `dbtRunnerResult.result` are not fully contracted, and therefore liable to change. Some of the returned objects are partially documented, because they overlap in part with the contents of [dbt artifacts](https://docs.getdbt.com/reference/artifacts/dbt-artifacts.md). As Python objects, they contain many more fields and methods than what's available in the serialized JSON artifacts. These additional fields and methods should be considered **internal and liable to change in future versions of dbt-core.**

#### Advanced usage patterns[​](#advanced-usage-patterns "Direct link to Advanced usage patterns")

caution

The syntax and support for these patterns are liable to change in future versions of `dbt-core`.

The goal of `dbtRunner` is to offer parity with CLI workflows, within a programmatic environment. There are a few advanced usage patterns that extend what's possible with the CLI.

##### Reusing objects[​](#reusing-objects "Direct link to Reusing objects")

Pass pre-constructed objects into `dbtRunner`, to avoid recreating those objects by reading files from disk. Currently, the only object supported is the `Manifest` (project contents).
```

---

## test

**URL:** llms-txt#test

dbt test --exclude "not_null_orders_order_id"   # test all models except the not_null_orders_order_id test
dbt test --exclude "orders"                     # test all models except tests associated with the orders model

---

## in models/marketing/__models.yml

**URL:** llms-txt#in-models/marketing/__models.yml

models: 
  - name: fct_marketing_model
    config: 
      group: marketing # changed to config in v1.10
      access: protected # changed to config in v1.10
  - name: stg_marketing_model
    config: 
      group: marketing # changed to config in v1.10
      access: private # changed to config in v1.10

**Examples:**

Example 1 (unknown):
```unknown
* **Validate these groups by incrementally migrating your jobs** to execute these groups specifically via selection syntax. We would recommend doing this in parallel to your production jobs until you’re sure about them. This will help you feel out if you’ve drawn the lines in the right place.
* If you find yourself **consistently making changes across multiple groups** when you update logic, that’s a sign that **you may want to rethink your groups**.

#### Split your projects[​](#split-your-projects "Direct link to Split your projects")

1. **Move your grouped models into a subfolder**. This will include any model in the selected group, it's associated YAML entry, as well as its parent or child resources as appropriate depending on where this group sits in your DAG.
   <!-- -->
   1. Note that just like in your dbt project, circular references are not allowed! Project B cannot have parents and children in Project A, for example.

2. **Create a new `dbt_project.yml` file** in the subdirectory.

3. **Copy any macros** used by the resources you moved.

4. **Create a new `packages.yml` file** in your subdirectory with the packages that are used by the resources you moved.

5. **Update `{{ ref }}` functions** — For any model that has a cross-project dependency (this may be in the files you moved, or in the files that remain in your project):

   <!-- -->

   1. Update the `{{ ref() }}` function to have two arguments, where the first is the name of the source project and the second is the name of the model: e.g. `{{ ref('jaffle_shop', 'my_upstream_model') }}`
   2. Update the upstream, cross-project parents’ `access` configs to `public` , ensuring any project can safely `{{ ref() }}` those models.
   3. We *highly* recommend adding a [model contract](https://docs.getdbt.com/docs/mesh/govern/model-contracts.md) to the upstream models to ensure the data shape is consistent and reliable for your downstream consumers.

6. **Create a `dependencies.yml` file** ([docs](https://docs.getdbt.com/docs/mesh/govern/project-dependencies.md)) for the downstream project, declaring the upstream project as a dependency.
```

---

## id_column is not a valid name for a top-level key in the dbt authoring spec, and will raise an error

**URL:** llms-txt#id_column-is-not-a-valid-name-for-a-top-level-key-in-the-dbt-authoring-spec,-and-will-raise-an-error

**Contents:**
  - Upgrading to v1.0
  - Upgrading to v1.1
  - Upgrading to v1.1 Beta
  - Upgrading to v1.1 [Beta](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - Upgrading to v1.10
  - Upgrading to v1.2
  - Upgrading to v1.3
  - Upgrading to v1.4
  - Upgrading to v1.5

id_column: &id_column_alias
  name: id
  description: This is a unique identifier.
  data_type: int
  data_tests:
    - not_null
    - unique

models:
  - name: my_first_model
    columns: 
      - *id_column_alias
      - name: unrelated_column_a
        description: This column is not repeated in other models.
  - name: my_second_model
    columns: 
      - *id_column_alias

anchors: 
  - &id_column_alias
      name: id
      description: This is a unique identifier.
      data_type: int
      data_tests:
        - not_null
        - unique

models:
  - name: my_first_model
    columns: 
      - *id_column_alias
      - name: unrelated_column_a
        description: This column is not repeated in other models
  - name: my_second_model
    columns: 
      - *id_column_alias

{% macro my_macro() %}

return('xyz') + 'abc'

error: dbt1501: Failed to add template invalid operation: return() is called in a non-block context

{% macro my_macro() %}

Expected a schema version of "https://schemas.getdbt.com/dbt/manifest/v5.json" in <state-path>/manifest.json, but found "https://schemas.getdbt.com/dbt/manifest/v4.json". Are you running with a different version of dbt?

python3 -m pip install dbt-core dbt-snowflake

python3 -m pip install dbt-core dbt-snowflake

id_column: &id_column_alias
  name: id
  description: This is a unique identifier.
  data_type: int
  data_tests:
    - not_null
    - unique

models:
  - name: my_first_model
    columns: 
      - *id_column_alias
      - name: unrelated_column_a
        description: This column is not repeated in other models.
  - name: my_second_model
    columns: 
      - *id_column_alias

anchors: 
  - &id_column_alias
      name: id
      description: This is a unique identifier.
      data_type: int
      data_tests:
        - not_null
        - unique

models:
  - name: my_first_model
    columns: 
      - *id_column_alias
      - name: unrelated_column_a
        description: This column is not repeated in other models
  - name: my_second_model
    columns: 
      - *id_column_alias

catalogs:
  - name: catalog_dave
    # materializing the data to an external location, and metadata to that data catalog
    write_integrations: 
      - name: databricks_glue_write_integration
          external_volume: databricks_external_volume_prod
          table_format: iceberg
          catalog_type: unity

models:
  - name: my_second_public_model
    config:
      catalog_name: catalog_dave

models:
  - name: my_model
    description: A model in my project.
    dbt_is_awesome: true # a custom property

models:
  - name: my_model
    description: A model in my project.
    config:
      meta:
        dbt_is_awesome: true

models:
  - name: my_model
    config:
      meta:
        custom_config_key: value
    columns:
      - name: my_column
        config:
          meta:
            some_key: some_value

my_profile:
  target: my_target
  outputs:
...

my_profile: # dbt would use only this profile key
  target: my_other_target
  outputs:
...

{% endmacro %} # orphaned endmacro jinja block

{% macro hello() %}
hello!
{% endmacro %}

sources: 
  - name: ecom
    schema: raw
    description: E-commerce data for the Jaffle Shop
    freshness:
      warn_after:
        count: 24
        period: hour

sources: 
  - name: ecom
    schema: raw
    description: E-commerce data for the Jaffle Shop
    config:
      freshness:
        warn_after:
          count: 24
          period: hour

...
flags:
  warn_error_options:
    error: # Previously called "include"
    warn: # Previously called "exclude"
    silence: # To silence or ignore warnings
      - NoNodesForSelectionCriteria

**Examples:**

Example 1 (unknown):
```unknown
Move the anchor under the `anchors:` key instead:

models/\_models.yml
```

Example 2 (unknown):
```unknown
This move is only necessary for fragments defined outside of the main YAML structure. For more information about this new key, see [anchors](https://docs.getdbt.com/reference/resource-properties/anchors.md).

###### Algebraic operations in Jinja macros[​](#algebraic-operations-in-jinja-macros "Direct link to Algebraic operations in Jinja macros")

In dbt Core, you can set algebraic functions in the return function of a Jinja macro:
```

Example 3 (unknown):
```unknown
This is no longer supported in Fusion and will return an error:
```

Example 4 (unknown):
```unknown
This is not a common use case and there is no deprecation warning for this behavior in dbt Core. The supported format is:
```

---

## .dbtignore

**URL:** llms-txt#.dbtignore

---

## IAM permission if using service account

**URL:** llms-txt#iam-permission-if-using-service-account

**Contents:**
  - Cache
  - Catalog JSON file
  - Caveats to state comparison
  - check_cols
  - Checking version compatibility
  - clean-targets
  - ClickHouse configurations
  - Cloudera Hive configurations
  - Cloudera Impala configurations
  - column_types

#Create Service Account
gcloud iam service-accounts create dbt-bigframes-sa
#Grant BigQuery User Role
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/bigquery.user
#Grant BigQuery Data Editor role. This can be restricted at dataset level
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/bigquery.dataEditor
#Grant Service Account user 
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/iam.serviceAccountUser
#Grant Colab Entperprise User
gcloud projects add-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} --member=serviceAccount:dbt-bigframes-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com --role=roles/aiplatform.colabEnterpriseUser

models:
  my_dbt_project:
    submission_method: bigframes

my_dbt_project_sa:
  outputs:
    dev:
      compute_region: us-central1
      dataset: <BIGQUERY_DATESET>
      gcs_bucket: <GCS BUCKET USED FOR BIGFRAME LOGS>
      job_execution_timeout_seconds: 300
      job_retries: 1
      keyfile: <SERVICE ACCOUNT KEY FILE>
      location: US
      method: service-account
      priority: interactive
      project: <BIGQUERY_PROJECT>
      threads: 1
      type: bigquery
  target: dev

def model(dbt, session):
    dbt.config(
        submission_method="cluster",
        dataproc_cluster_name="my-favorite-cluster"
    )
    ...

models:
  - name: my_python_model
    config:
      submission_method: serverless

dataproc.batches.create
dataproc.clusters.use
dataproc.jobs.create
dataproc.jobs.get
dataproc.operations.get
dataproc.operations.list
storage.buckets.get
storage.objects.create
storage.objects.delete

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
              runtime_config:
                  container_image: {HOSTNAME}/{PROJECT_ID}/{IMAGE}:{TAG}
  
dbt compile --no-populate-cache --select my_model_name

dbt run --cache-selected-only --select salesforce

dbt compile --log-cache-events

dbt run -s "state:modified"
dbt test -s "state:modified"

dbt run -s "state:modified"
dbt test -s "state:modified" --exclude "test_name:relationships"

snapshots:
  <resource-path>:
    +strategy: check
    +check_cols: [column_name] | all

$ dbt run --no-version-check
Running with dbt=1.0.0
Found 13 models, 2 tests, 1 archives, 0 analyses, 204 macros, 2 operations....

{% macro a_few_days_in_september() %}

{% if not dbt.get('date_spine') %}
      {{ exceptions.raise_compiler_error("Expected to find the dbt.date_spine macro, but it could not be found") }}
    {% endif %}

{{ date_spine("day", "cast('2020-01-01' as date)", "cast('2030-12-31' as date)") }}

clean-targets: [directorypath]

clean-targets:
    - target
    - dbt_packages

clean-targets: [target, dbt_packages, logs]

models:
  <resource-path>:
    +materialized: view

{{ config(materialized = "view") }}

models:
  <resource-path>:
    +materialized: table
    +order_by: [ <column-name>, ... ]
    +engine: <engine-type>
    +partition_by: [ <column-name>, ... ]

{{ config(
    materialized = "table",
    engine = "<engine-type>",
    order_by = [ "<column-name>", ... ],
    partition_by = [ "<column-name>", ... ],
      ...
    ]
) }}

models:
  <resource-path>:
    +materialized: incremental
    +order_by: [ <column-name>, ... ]
    +engine: <engine-type>
    +partition_by: [ <column-name>, ... ]
    +unique_key: [ <column-name>, ... ]
    +inserts_only: [ True|False ]

{{ config(
    materialized = "incremental",
    engine = "<engine-type>",
    order_by = [ "<column-name>", ... ],
    partition_by = [ "<column-name>", ... ],
    unique_key = [ "<column-name>", ... ],
    inserts_only = [ True|False ],
      ...
    ]
) }}

{{
    config(
        materialized='table',
        unique_key='id',
        partition_by=['city'],
    )
}}

with source_data as (
     select 1 as id, "Name 1" as name, "City 1" as city,
     union all
     select 2 as id, "Name 2" as name, "City 2" as city,
     union all
     select 3 as id, "Name 3" as name, "City 2" as city,
     union all
     select 4 as id, "Name 4" as name, "City 1" as city,
)

select * from source_data

{{
    config(
        materialized='table',
        unique_key='id',
        partition_by=['city'],
    )
}}

with source_data as (
     select 1 as id, "Name 1" as name, "City 1" as city,
     union all
     select 2 as id, "Name 2" as name, "City 2" as city,
     union all
     select 3 as id, "Name 3" as name, "City 2" as city,
     union all
     select 4 as id, "Name 4" as name, "City 1" as city,
)

select * from source_data

seeds:
  jaffle_shop:
    country_codes:
      +column_types:
        country_code: varchar(2)
        country_name: varchar(32)

seeds:
  - name: country_codes
    config:
      column_types:
        country_code: varchar(2)
        country_name: varchar(32)

seeds:
  jaffle_shop:
    marketing:
      utm_mappings:
        +column_types:
          ...

seeds:
  jaffle_shop: # you must include the project name
    warehouse_locations:
      +column_types:
        zipcode: varchar(5)

models:
  - name: <model_name>
    columns:
      - name: <column_name>
        data_type: <string>
        description: <markdown_string>
        quote: true | false
        data_tests: ...
        config:
          tags: ...
          meta: ...
      - name: <another_column>
        ...

sources:
  - name: <source_name>
    tables:
    - name: <table_name>
      columns:
        - name: <column_name>
          description: <markdown_string>
          data_type: <string>
          quote: true | false
          data_tests: ...
          config:
            tags: ...
            meta: ...
        - name: <another_column>
          ...

seeds:
  - name: <seed_name>
    columns:
      - name: <column_name>
        description: <markdown_string>
        data_type: <string>
        quote: true | false
        data_tests: ...
        config:
          tags: ...
          meta: ...
      - name: <another_column>
            ...

snapshots:
  - name: <snapshot_name>
    columns:
      - name: <column_name>
        description: <markdown_string>
        data_type: <string>
        quote: true | false
        data_tests: ...
        config:
          tags: ...
          meta: ...
      - name: <another_column>

analyses:
  - name: <analysis_name>
    columns:
      - name: <column_name>
        description: <markdown_string>
        data_type: <string>
      - name: <another_column>

models:
  - name: model_name
    columns:
      - name: column_name
        quote: true | false

sources:
  - name: source_name
    tables:
      - name: table_name
        columns:
          - name: column_name
            quote: true | false

seeds:
  - name: seed_name
    columns:
      - name: column_name
        quote: true | false

snapshots:
  - name: snapshot_name
    columns:
      - name: column_name
        quote: true | false

analyses:
  - name: analysis_name
    columns:
      - name: column_name
        quote: true | false

select user_group as "group"

sources:
  - name: stripe
    tables:
      - name: payment
        columns:
          - name: orderID
            quote: true
            data_tests:
              - not_null

$ dbt test -s source:stripe.*
Running with dbt=0.16.1
Found 7 models, 22 tests, 0 snapshots, 0 analyses, 130 macros, 0 operations, 0 seed files, 4 sources

13:33:37 | Concurrency: 4 threads (target='learn')
13:33:37 |
13:33:37 | 1 of 1 START test source_not_null_stripe_payment_order_id............ [RUN]
13:33:39 | 1 of 1 ERROR source_not_null_stripe_payment_order_id................. [ERROR in 1.89s]
13:33:39 |
13:33:39 | Finished running 1 tests in 6.43s.

Completed with 1 error and 0 warnings:

Database Error in test source_not_null_stripe_payment_order_id (models/staging/stripe/src_stripe.yml)
  000904 (42000): SQL compilation error: error line 3 at position 6
  invalid identifier 'ORDERID'
  compiled SQL at target/compiled/jaffle_shop/schema_test/source_not_null_stripe_payment_orderID.sql

select count(*)
from raw.stripe.payment
where orderID is null

select count(*)
from raw.stripe.payment
where "orderID" is null

dbt --no-populate-cache run

dbt run --no-populate-cache

<SUBCOMMAND> --<THIS-CONFIG>=<SETTING>

dbt run --printer-width=80 
dbt test --indirect-selection=eager

dbt <SUBCOMMAND> --<THIS-CONFIG> 
dbt <SUBCOMMAND> --no-<THIS-CONFIG>

dbt run --version-check
dbt run --no-version-check

**Examples:**

Example 1 (unknown):
```unknown
dbt\_project.yml
```

Example 2 (unknown):
```unknown
profiles.yml
```

Example 3 (unknown):
```unknown
Dataproc (`serverless` or pre-configured `cluster`) can execute Python models as PySpark jobs, reading from and writing to BigQuery. `serverless` is simpler but slower with limited configuration and pre-installed packages (`pandas`, `numpy`, `scikit-learn`), while `cluster` offers full control and faster runtimes. Good for complex, long-running batch pipelines and legacy Hadoop/Spark workflows but often slower for ad-hoc or interactive workloads.

**Dataproc setup:**

* Create or use an existing [Cloud Storage bucket](https://cloud.google.com/storage/docs/creating-buckets).
* Enable Dataproc APIs for your project and region.
* If using the `cluster` submission method: Create or use an existing [Dataproc cluster](https://cloud.google.com/dataproc/docs/guides/create-cluster) with the [Spark BigQuery connector initialization action](https://github.com/GoogleCloudDataproc/initialization-actions/tree/master/connectors#bigquery-connectors). (Google recommends copying the action into your own Cloud Storage bucket, rather than using the example version shown in the screenshot.)

[![Add the Spark BigQuery connector as an initialization action](/img/docs/building-a-dbt-project/building-models/python-models/dataproc-connector-initialization.png?v=2 "Add the Spark BigQuery connector as an initialization action")](#)Add the Spark BigQuery connector as an initialization action

The following configurations are needed to run Python models on Dataproc. You can add these to your [BigQuery profile](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup.md#running-python-models-on-dataproc) or configure them on specific Python models:

* `gcs_bucket`: Storage bucket to which dbt will upload your model's compiled PySpark code.
* `dataproc_region`: GCP region in which you have enabled Dataproc (for example `us-central1`).
* `dataproc_cluster_name`: Name of Dataproc cluster to use for running Python model (executing PySpark job). Only required if `submission_method: cluster`.
```

Example 4 (unknown):
```unknown

```

---

## Newly added

**URL:** llms-txt#newly-added

**Contents:**
  - Quickstart with dbt Mesh
  - Quickstart with MetricFlow time spine
  - Refactoring legacy SQL to dbt
  - Refresh a Mode dashboard when a job completes

metrics: 
  # Simple type metrics
  - name: "order_total"
    description: "Sum of orders value"
    type: simple
    label: "order_total"
    type_params:
      measure:
        name: order_total
  - name: "order_count"
    description: "number of orders"
    type: simple
    label: "order_count"
    type_params:
      measure:
        name: order_count
  - name: large_orders
    description: "Count of orders with order total over 20."
    type: simple
    label: "Large Orders"
    type_params:
      measure:
        name: order_count
    filter: |
      {{ Metric('order_total', group_by=['order_id']) }} >=  20
  # Ratio type metric
  - name: "avg_order_value"
    label: "avg_order_value"
    description: "average value of each order"
    type: ratio
    type_params:
      numerator: 
        name: order_total
      denominator: 
        name: order_count
  # Cumulative type metrics
  - name: "cumulative_order_amount_mtd"
    label: "cumulative_order_amount_mtd"
    description: "The month to date value of all orders"
    type: cumulative
    type_params:
      measure:
        name: order_total
      grain_to_date: month
  # Derived metric
  - name: "pct_of_orders_that_are_large"
    label: "pct_of_orders_that_are_large"
    description: "percent of orders that are large"
    type: derived
    type_params:
      expr: large_orders/order_count
      metrics:
        - name: large_orders
        - name: order_count

semantic_models:
  - name: customers
    defaults:
      agg_time_dimension: most_recent_order_date
    description: |
      semantic model for dim_customers
    model: ref('dim_customers')
    entities:
      - name: customer
        expr: customer_id
        type: primary
    dimensions:
      - name: customer_name
        type: categorical
        expr: first_name
      - name: first_order_date
        type: time
        type_params:
          time_granularity: day
      - name: most_recent_order_date
        type: time
        type_params:
          time_granularity: day
    measures:
      - name: count_lifetime_orders
        description: Total count of orders per customer.
        agg: sum
        expr: number_of_orders
      - name: lifetime_spend
        agg: sum
        expr: lifetime_value
        description: Gross customer lifetime spend inclusive of taxes.
      - name: customers
        expr: customer_id
        agg: count_distinct

metrics:
  - name: "customers_with_orders"
    label: "customers_with_orders"
    description: "Unique count of customers placing orders"
    type: simple
    type_params:
      measure:
        name: customers

dbt sl query --metrics order_total,order_count --group-by order_date
   
select * from
  {{ semantic_layer.query (
    metrics = ['order_total', 'order_count', 'large_orders', 'customers_with_orders', 'avg_order_value', pct_of_orders_that_are_large'],
    group_by = 
    [Dimension('metric_time').grain('day') ]
) }}

sources:
  - name: jaffle_shop
    description: This is a replica of the Postgres database used by our app
    database: raw
    schema: jaffle_shop
    tables:
      - name: customers
        description: One record per customer.
      - name: orders
        description: One record per order. Includes cancelled and deleted orders.

select
    id as customer_id,
    first_name,
    last_name

from {{ source('jaffle_shop', 'customers') }}

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

from {{ source('jaffle_shop', 'orders') }}

with customers as (
    select * 
    from {{ ref('stg_customers') }}
),

orders as (
    select * 
    from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_id,
        min(order_date) as first_order_date
    from orders
    group by customer_id
),

final as (
    select
        o.order_id,
        o.order_date,
        o.status,
        c.customer_id,
        c.first_name,
        c.last_name,
        co.first_order_date,
        -- Note that we've used a macro for this so that the appropriate DATEDIFF syntax is used for each respective data platform
        {{ datediff('first_order_date', 'order_date', 'day') }} as days_as_customer_at_purchase
    from orders o
    left join customers c using (customer_id)
    left join customer_orders co using (customer_id)
)

models:
  - name: fct_orders
    config:
      access: public # changed to config in v1.10
    description: "Customer and order details"
    columns:
      - name: order_id
        data_type: number
        description: ""

- name: order_date
        data_type: date
        description: ""

- name: status
        data_type: varchar
        description: "Indicates the status of the order"

- name: customer_id
        data_type: number
        description: ""

- name: first_name
        data_type: varchar
        description: ""

- name: last_name
        data_type: varchar
        description: ""

- name: first_order_date
        data_type: date
        description: ""

- name: days_as_customer_at_purchase
        data_type: number
        description: "Days between this purchase and customer's first purchase"

packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1

projects:
  - name: analytics

sources:
     - name: stripe
       database: raw
       schema: stripe 
       tables:
         - name: payment

with payments as (
       select * from {{ source('stripe', 'payment') }}
   ),

final as (
       select 
           id as payment_id,
           orderID as order_id,
           paymentMethod as payment_method,
           amount,
           created as payment_date 
       from payments
   )

with stg_payments as (
       select * from {{ ref('stg_payments') }}
   ),

fct_orders as (
       select * from {{ ref('analytics', 'fct_orders') }}
   ),

final as (
       select 
           days_as_customer_at_purchase,
           -- we use the pivot macro in the dbt_utils package to create columns that total payments for each method
           {{ dbt_utils.pivot(
               'payment_method',
               dbt_utils.get_column_values(ref('stg_payments'), 'payment_method'),
               agg='sum',
               then_value='amount',
               prefix='total_',
               suffix='_amount'
           ) }}, 
           sum(amount) as total_amount
       from fct_orders
       left join stg_payments using (order_id)
       group by 1
   )

select * from final
   
models:
  - name: fct_orders
    description: “Customer and order details”
    config:
      access: public # changed to config in v1.10
      contract:
        enforced: true
    columns:
      - name: order_id
        .....

models:
  - name: fct_orders
    description: "Customer and order details"
    latest_version: 2
    config:
      access: public # changed to config in v1.10
      contract:
        enforced: true
    columns:
      - name: order_id
        data_type: number
        description: ""

- name: order_date
        data_type: date
        description: ""

- name: status
        data_type: varchar
        description: "Indicates the status of the order"

- name: is_return
        data_type: boolean
        description: "Indicates if an order was returned"

- name: customer_id
        data_type: number
        description: ""

- name: first_name
        data_type: varchar
        description: ""

- name: last_name
        data_type: varchar
        description: ""

- name: first_order_date
        data_type: date
        description: ""

- name: days_as_customer_at_purchase
        data_type: number
        description: "Days between this purchase and customer's first purchase"

# Declare the versions, and highlight the diffs
    versions:
    
      - v: 1
        deprecation_date: 2024-06-30 00:00:00.00+00:00
        columns:
          # This means: use the 'columns' list from above, but exclude is_return
          - include: all
            exclude: [is_return]
        
      - v: 2
        columns:
          # This means: use the 'columns' list from above, but exclude status
          - include: all
            exclude: [status]

select * from {{ ref('fct_orders', v=1) }}
select * from {{ ref('fct_orders', v=2) }}
select * from {{ ref('fct_orders') }}

with stg_payments as (
    select * from {{ ref('stg_payments') }}
),

fct_orders as (
    select * from {{ ref('analytics', 'fct_orders', v=1) }}
),

final as (
    select 
        days_as_customer_at_purchase,
        -- we use the pivot macro in the dbt_utils package to create columns that total payments for each method
        {{ dbt_utils.pivot(
            'payment_method',
            dbt_utils.get_column_values(ref('stg_payments'), 'payment_method'),
            agg='sum',
            then_value='amount',
            prefix='total_',
            suffix='_amount'
        ) }}, 
        sum(amount) as total_amount
    from fct_orders
    left join stg_payments using (order_id)
    group by 1
)

{{
       config(
           materialized = 'table',
       )
   }}

base_dates as (
       {{
           dbt.date_spine(
               'day',
               "DATE('2000-01-01')",
               "DATE('2030-01-01')"
           )
       }}
   ),

final as (
       select
           cast(date_day as date) as date_day
       from base_dates
   )

select *
   from final
   where date_day > dateadd(year, -5, current_date())  -- Keep recent dates only
     and date_day < dateadd(day, 30, current_date())
   
   dbt run --select time_spine_daily 
   dbt show --select time_spine_daily # Use this command to preview the model if developing locally
   
   models:
     - name: time_spine_daily
       description: A time spine with one row per day, ranging from 5 years in the past to 30 days into the future.
       time_spine:
         standard_granularity_column: date_day  # The base column used for time joins
       columns:
         - name: date_day
           description: The base date column for daily granularity
           granularity: day
   
   models:
     - name: dim_date
       description: An existing date dimension model used as a time spine.
       time_spine:
         standard_granularity_column: date_day
       columns:
         - name: date_day
           granularity: day
         - name: day_of_week
           granularity: day
         - name: full_date
           granularity: day
   
   dbt run --select time_spine_daily
   dbt show --select time_spine_daily # Use this command to preview the model if developing locally
   
   dbt sl query --metrics revenue --group-by metric_time
   
   {{
       config(
           materialized = 'table',
       )
   }}

{{
           dbt.date_spine(
               'year',
               "to_date('01/01/2000','mm/dd/yyyy')",
               "to_date('01/01/2025','mm/dd/yyyy')"
           )
       }}

final as (
       select cast(date_year as date) as date_year
       from years
   )

select * from final
   -- filter the time spine to a specific range
   where date_year >= date_trunc('year', dateadd(year, -4, current_timestamp())) 
     and date_year < date_trunc('year', dateadd(year, 1, current_timestamp()))
   
   models:
     - name: time_spine_daily
       ... rest of the daily time spine config ...

- name: time_spine_yearly
       description: time spine one row per house
       time_spine:
         standard_granularity_column: date_year
       columns:
         - name: date_year
           granularity: year
   
   dbt run --select time_spine_yearly
   dbt show --select time_spine_yearly # Use this command to preview the model if developing locally
   
   dbt sl query --metrics orders --group-by metric_time__year
   
       with date_spine as (

select 
           date_day,
           extract(year from date_day) as calendar_year,
           extract(week from date_day) as calendar_week

from {{ ref('time_spine_daily') }}

select
           date_day,
           -- Define custom fiscal year starting in October
           case 
               when extract(month from date_day) >= 10 
                   then extract(year from date_day) + 1
               else extract(year from date_day) 
           end as fiscal_year,

-- Define fiscal weeks (e.g., shift by 1 week)
           extract(week from date_day) + 1 as fiscal_week

select * from fiscal_calendar
   
   models:
     - name: time_spine_yearly
       ... rest of the yearly time spine config ...  
       
     - name: fiscal_calendar
       description: A custom fiscal calendar with fiscal year and fiscal week granularities.
       time_spine:
         standard_granularity_column: date_day
         custom_granularities:
           - name: fiscal_year
             column_name: fiscal_year
           - name: fiscal_week
             column_name: fiscal_week
       columns:
         - name: date_day
           granularity: day
         - name: fiscal_year
           description: "Custom fiscal year starting in October"
         - name: fiscal_week
           description: "Fiscal week, shifted by 1 week from standard calendar"
   
   dbt run --select fiscal_calendar
   dbt show --select fiscal_calendar # Use this command to preview the model if developing locally
   
   dbt sl query --metrics orders --group-by metric_time__fiscal_year
   
sources:
  - name: jaffle_shop
    tables:
      - name: orders
      - name: customers

-- query only non-test orders
    select * from {{ source('jaffle_shop', 'orders') }}
    where amount > 0
),

import_customers as (
    select * from {{ source('jaffle_shop', 'customers') }}
),

-- perform some math on import_orders

-- perform some math on import_customers
),

-- join together logical_cte_1 and logical_cte_2
)

select * from final_cte

store = StoreClient('abc123') #replace with your UUID secret
store.set('DBT_WEBHOOK_KEY', 'abc123') #replace with your <Constant name="cloud" /> API token
store.set('MODE_API_TOKEN', 'abc123') #replace with your Mode API Token
store.set('MODE_API_SECRET', 'abc123') #replace with your Mode API Secret

import hashlib
import hmac
import json

#replace with the report token you want to run
account_username = 'YOUR_MODE_ACCOUNT_USERNAME_HERE'
report_token = 'YOUR_REPORT_TOKEN_HERE'

auth_header = input_data['auth_header']
raw_body = input_data['raw_body']

**Examples:**

Example 1 (unknown):
```unknown
##### Add second semantic model to your project[​](#add-second-semantic-model-to-your-project "Direct link to Add second semantic model to your project")

Great job, you've successfully built your first semantic model! It has all the required elements: entities, dimensions, measures, and metrics.

Let’s expand your project's analytical capabilities by adding another semantic model in your other marts model, such as: `dim_customers.yml`.

After setting up your orders model:

1. In the `metrics` sub-directory, create the file `dim_customers.yml`.
2. Copy the following query into the file and click **Save**.

models/metrics/dim\_customers.yml
```

Example 2 (unknown):
```unknown
This semantic model uses simple metrics to focus on customer metrics and emphasizes customer dimensions like name, type, and order dates. It uniquely analyzes customer behavior, lifetime value, and order patterns.

#### Test and query metrics[​](#test-and-query-metrics "Direct link to Test and query metrics")

To work with metrics in dbt, you have several tools to validate or run commands. Here's how you can test and query metrics depending on your setup:

* [**Studio IDE users**](#dbt-cloud-ide-users) — Run [MetricFlow commands](https://docs.getdbt.com/docs/build/metricflow-commands.md#metricflow-commands) directly in the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md) to query/preview metrics. View metrics visually in the **Lineage** tab.
* [**Cloud CLI users**](#dbt-cloud-cli-users) — The [Cloud CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md) enables you to run [MetricFlow commands](https://docs.getdbt.com/docs/build/metricflow-commands.md#metricflow-commands) to query and preview metrics directly in your command line interface.
* **dbt Core users** — Use the MetricFlow CLI for command execution. While this guide focuses on dbt users, dbt Core users can find detailed MetricFlow CLI setup instructions in the [MetricFlow commands](https://docs.getdbt.com/docs/build/metricflow-commands.md#metricflow-commands) page. Note that to use the Semantic Layer, you need to have a [Starter or Enterprise-tier account](https://www.getdbt.com/).

Alternatively, you can run commands with SQL client tools like DataGrip, DBeaver, or RazorSQL.

##### Studio IDE users[​](#studio-ide-users "Direct link to Studio IDE users")

You can use the `dbt sl` prefix before the command name to execute them in dbt. For example, to list all metrics, run `dbt sl list metrics`. For a complete list of the MetricFlow commands available in the Studio IDE, refer to the [MetricFlow commands](https://docs.getdbt.com/docs/build/metricflow-commands.md#metricflow-commandss) page.

The Studio IDE **Status button** (located in the bottom right of the editor) displays an **Error** status if there's an error in your metric or semantic model definition. You can click the button to see the specific issue and resolve it.

Once viewed, make sure you commit and merge your changes in your project.

[![Validate your metrics using the Lineage tab in the IDE.](/img/docs/dbt-cloud/semantic-layer/sl-ide-dag.png?v=2 "Validate your metrics using the Lineage tab in the IDE.")](#)Validate your metrics using the Lineage tab in the IDE.

##### Cloud CLI users[​](#cloud-cli-users "Direct link to Cloud CLI users")

This section is for Cloud CLI users. MetricFlow commands are integrated with dbt, which means you can run MetricFlow commands as soon as you install the Cloud CLI. Your account will automatically manage version control for you.

Refer to the following steps to get started:

1. Install the [Cloud CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md) (if you haven't already). Then, navigate to your dbt project directory.
2. Run a dbt command, such as `dbt parse`, `dbt run`, `dbt compile`, or `dbt build`. If you don't, you'll receive an error message that begins with: "ensure that you've ran an artifacts....".
3. MetricFlow builds a semantic graph and generates a `semantic_manifest.json` file in dbt, which is stored in the `/target` directory. If using the Jaffle Shop example, run `dbt seed && dbt run` to ensure the required data is in your data platform before proceeding.

Run dbt parse to reflect metric changes

When you make changes to metrics, make sure to run `dbt parse` at a minimum to update the Semantic Layer. This updates the `semantic_manifest.json` file, reflecting your changes when querying metrics. By running `dbt parse`, you won't need to rebuild all the models.

4. Run `dbt sl --help` to confirm you have MetricFlow installed and that you can view the available commands.

5. Run `dbt sl query --metrics <metric_name> --group-by <dimension_name>` to query the metrics and dimensions. For example, to query the `order_total` and `order_count` (both metrics), and then group them by the `order_date` (dimension), you would run:
```

Example 3 (unknown):
```unknown
6. Verify that the metric values are what you expect. To further understand how the metric is being generated, you can view the generated SQL if you type `--compile` in the command line.

7. Commit and merge the code changes that contain the metric definitions.

#### Run a production job[​](#run-a-production-job "Direct link to Run a production job")

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

#### Administer the Semantic Layer[​](#administer-the-semantic-layer "Direct link to Administer the Semantic Layer")

In this section, you will learn how to add credentials and create service tokens to start querying the dbt Semantic Layer. This section goes over the following topics:

* [Select environment](#1-select-environment)
* [Configure credentials and create tokens](#2-configure-credentials-and-create-tokens)
* [View connection detail](#3-view-connection-detail)
* [Add more credentials](#4-add-more-credentials)
* [Delete configuration](#delete-configuration)

You must be part of the Owner group and have the correct [license](https://docs.getdbt.com/docs/cloud/manage-access/seats-and-users.md) and [permissions](https://docs.getdbt.com/docs/cloud/manage-access/enterprise-permissions.md) to administer the Semantic Layer at the environment and project level.

* Enterprise+ and Enterprise plan:

  <!-- -->

  * Developer license with Account Admin permissions, or
  * Owner with a Developer license, assigned Project Creator, Database Admin, or Admin permissions.

* Starter plan: Owner with a Developer license.

* Free trial: You are on a free trial of the Starter plan as an Owner, which means you have access to the dbt Semantic Layer.

##### 1. Select environment[​](#1-select-environment "Direct link to 1. Select environment")

Select the environment where you want to enable the Semantic Layer:

1. Navigate to **Account settings** in the navigation menu.
2. Under **Settings**, click **Projects** and select the specific project you want to enable the Semantic Layer for.
3. In the **Project details** page, navigate to the **Semantic Layer** section. Select **Configure Semantic Layer**.

[![Semantic Layer section in the 'Project details' page](/img/docs/dbt-cloud/semantic-layer/new-sl-configure.png?v=2 "Semantic Layer section in the 'Project details' page")](#)Semantic Layer section in the 'Project details' page

4. In the **Set Up Semantic Layer Configuration** page, select the deployment environment you want for the Semantic Layer and click **Save**. This provides administrators with the flexibility to choose the environment where the Semantic Layer will be enabled.

[![Select the deployment environment to run your Semantic Layer against.](/img/docs/dbt-cloud/semantic-layer/sl-select-env.png?v=2 "Select the deployment environment to run your Semantic Layer against.")](#)Select the deployment environment to run your Semantic Layer against.

##### 2. Configure credentials and create tokens[​](#2-configure-credentials-and-create-tokens "Direct link to 2. Configure credentials and create tokens")

There are two options for setting up Semantic Layer using API tokens:

* [Add a credential and create service tokens](#add-a-credential-and-create-service-tokens)
* [Configure development credentials and create personal tokens](#configure-development-credentials-and-create-a-personal-token)

###### Add a credential and create service tokens[​](#add-a-credential-and-create-service-tokens "Direct link to Add a credential and create service tokens")

The first option is to use [service tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md) for authentication which are tied to an underlying data platform credential that you configure. The credential configured is used to execute queries that the Semantic Layer issues against your data platform.

This credential controls the physical access to underlying data accessed by the Semantic Layer, and all access policies set in the data platform for this credential will be respected.

| Feature                                             | Starter plan                                                 | Enterprise+ and Enterprise plan                                                                                                                                 |
| --------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Service tokens                                      | Can create multiple service tokens linked to one credential. | Can use multiple credentials and link multiple service tokens to each credential. Note that you cannot link a single service token to more than one credential. |
| Credentials per project                             | One credential per project.                                  | Can [add multiple](#4-add-more-credentials) credentials per project.                                                                                            |
| Link multiple service tokens to a single credential | ✅                                                           | ✅                                                                                                                                                              |

*If you're on a Starter plan and need to add more credentials, consider upgrading to our [Enterprise+ or Enterprise plan](https://www.getdbt.com/contact). All Enterprise users can refer to [Add more credentials](#4-add-more-credentials) for detailed steps on adding multiple credentials.*

###### 1. Select deployment environment[​](#1--select-deployment-environment "Direct link to 1.  Select deployment environment")

* After selecting the deployment environment, you should see the **Credentials & service tokens** page.
* Click the **Add Semantic Layer credential** button.

###### 2. Configure credential[​](#2-configure-credential "Direct link to 2. Configure credential")

* In the **1. Add credentials** section, enter the credentials specific to your data platform that you want the Semantic Layer to use.

* Use credentials with minimal privileges. The Semantic Layer requires read access to the schema(s) containing the dbt models used in your semantic models for downstream applications

* Use [Extended Attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) and [Environment Variables](https://docs.getdbt.com/docs/build/environment-variables.md) when connecting to the Semantic Layer. If you set a value directly in the Semantic Layer Credentials, it will have a higher priority than Extended Attributes. When using environment variables, the default value for the environment will be used.

  For example, set the warehouse by using `{{env_var('DBT_WAREHOUSE')}}` in your Semantic Layer credentials.

  Similarly, if you set the account value using `{{env_var('DBT_ACCOUNT')}}` in Extended Attributes, dbt will check both the Extended Attributes and the environment variable.

[![Add credentials and map them to a service token. ](/img/docs/dbt-cloud/semantic-layer/sl-add-credential.png?v=2 "Add credentials and map them to a service token. ")](#)Add credentials and map them to a service token.

###### 3. Create or link service tokens[​](#3-create-or-link-service-tokens "Direct link to 3. Create or link service tokens")

* If you have permission to create service tokens, you’ll see the [**Map new service token** option](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md#map-service-tokens-to-credentials) after adding the credential. Name the token, set permissions to 'Semantic Layer Only' and 'Metadata Only', and click **Save**.
* Once the token is generated, you won't be able to view this token again, so make sure to record it somewhere safe.
* If you don’t have access to create service tokens, you’ll see a message prompting you to contact your admin to create one for you. Admins can create and link tokens as needed.

[![If you don’t have access to create service tokens, you can create a credential and contact your admin to create one for you.](/img/docs/dbt-cloud/semantic-layer/sl-credential-no-service-token.png?v=2 "If you don’t have access to create service tokens, you can create a credential and contact your admin to create one for you.")](#)If you don’t have access to create service tokens, you can create a credential and contact your admin to create one for you.

info

* Starter plans can create multiple service tokens that link to a single underlying credential, but each project can only have one credential.
* All Enterprise plans can [add multiple credentials](#4-add-more-credentials) and map those to service tokens for tailored access.

[Book a free live demo](https://www.getdbt.com/contact) to discover the full potential of dbt Enterprise and higher plans.

###### Configure development credentials and create a personal token[​](#configure-development-credentials-and-create-a-personal-token "Direct link to Configure development credentials and create a personal token")

Using [personal access tokens (PATs)](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md) is also a supported authentication method for the dbt Semantic Layer. This enables user-level authentication, reducing the need for sharing tokens between users. When you authenticate using PATs, queries are run using your personal development credentials.

To use PATs in Semantic Layer:

1. Configure your development credentials.

   <!-- -->

   1. Click your account name at the bottom left-hand menu and go to **Account settings** > **Credentials**.
   2. Select your project.
   3. Click **Edit**.
   4. Go to **Development credentials** and enter your details.
   5. Click **Save**.

2. [Create a personal access token](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md). Make sure to copy the token.

You can use the generated PAT as the authentication method for Semantic Layer [APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md) and [integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md).

##### 3. View connection detail[​](#3-view-connection-detail "Direct link to 3. View connection detail")

1. Go back to the **Project details** page for connection details to connect to downstream tools.

2. Copy and share the Environment ID, service or personal token, Host, as well as the service or personal token name to the relevant teams for BI connection setup. If your tool uses the GraphQL API, save the GraphQL API host information instead of the JDBC URL.

   For info on how to connect to other integrations, refer to [Available integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md).

[![After configuring, you'll be provided with the connection details to connect to you downstream tools.](/img/docs/dbt-cloud/semantic-layer/sl-configure-example.png?v=2 "After configuring, you'll be provided with the connection details to connect to you downstream tools.")](#)After configuring, you'll be provided with the connection details to connect to you downstream tools.

##### 4. Add more credentials [Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[​](#4-add-more-credentials- "Direct link to 4-add-more-credentials-")

All dbt Enterprise plans can optionally add multiple credentials and map them to service tokens, offering more granular control and tailored access for different teams, which can then be shared to relevant teams for BI connection setup. These credentials control the physical access to underlying data accessed by the Semantic Layer.

We recommend configuring credentials and service tokens to reflect your teams and their roles. For example, create tokens or credentials that align with your team's needs, such as providing access to finance-related schemas to the Finance team.

 Considerations for linking credentials

* Admins can link multiple service tokens to a single credential within a project, but each service token can only be linked to one credential per project.

* When you send a request through the APIs, the service token of the linked credential will follow access policies of the underlying view and tables used to build your semantic layer requests.

* Use [Extended Attributes](https://docs.getdbt.com/docs/dbt-cloud-environments.md#extended-attributes) and [Environment Variables](https://docs.getdbt.com/docs/build/environment-variables.md) when connecting to the Semantic Layer. If you set a value directly in the Semantic Layer Credentials, it will have a higher priority than Extended Attributes. When using environment variables, the default value for the environment will be used.

  For example, set the warehouse by using `{{env_var('DBT_WAREHOUSE')}}` in your Semantic Layer credentials.

  Similarly, if you set the account value using `{{env_var('DBT_ACCOUNT')}}` in Extended Attributes, dbt will check both the Extended Attributes and the environment variable.

###### 1. Add more credentials[​](#1-add-more-credentials "Direct link to 1. Add more credentials")

* After configuring your environment, on the **Credentials & service tokens** page, click the **Add Semantic Layer credential** button to create multiple credentials and map them to a service token. <br />
* In the **1. Add credentials** section, fill in the data platform's credential fields. We recommend using “read-only” credentials.
  <!-- -->
  [![Add credentials and map them to a service token. ](/img/docs/dbt-cloud/semantic-layer/sl-add-credential.png?v=2 "Add credentials and map them to a service token. ")](#)Add credentials and map them to a service token.

###### 2. Map service tokens to credentials[​](#2-map-service-tokens-to-credentials "Direct link to 2. Map service tokens to credentials")

* In the **2. Map new service token** section, [map a service token to the credential](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl.md#map-service-tokens-to-credentials) you configured in the previous step. dbt automatically selects the service token permission set you need (Semantic Layer Only and Metadata Only).
* To add another service token during configuration, click **Add Service Token**.
* You can link more service tokens to the same credential later on in the **Semantic Layer Configuration Details** page. To add another service token to an existing Semantic Layer configuration, click **Add service token** under the **Linked service tokens** section.
* Click **Save** to link the service token to the credential. Remember to copy and save the service token securely, as it won't be viewable again after generation.

[![Use the configuration page to manage multiple credentials or link or unlink service tokens for more granular control.](/img/docs/dbt-cloud/semantic-layer/sl-credentials-service-token.png?v=2 "Use the configuration page to manage multiple credentials or link or unlink service tokens for more granular control.")](#)Use the configuration page to manage multiple credentials or link or unlink service tokens for more granular control.

###### 3. Delete credentials[​](#3-delete-credentials "Direct link to 3. Delete credentials")

* To delete a credential, go back to the **Credentials & service tokens** page.

* Under **Linked Service Tokens**, click **Edit** and, select **Delete Credential** to remove a credential.

  When you delete a credential, any service tokens mapped to that credential in the project will no longer work and will break for any end users.

##### Delete configuration[​](#delete-configuration "Direct link to Delete configuration")

You can delete the entire Semantic Layer configuration for a project. Note that deleting the Semantic Layer configuration will remove all credentials and unlink all service tokens to the project. It will also cause all queries to the Semantic Layer to fail.

Follow these steps to delete the Semantic Layer configuration for a project:

1. Navigate to the **Project details** page.
2. In the **Semantic Layer** section, select **Delete Semantic Layer**.
3. Confirm the deletion by clicking **Yes, delete semantic layer** in the confirmation pop up.

To re-enable the dbt Semantic Layer setup in the future, you will need to recreate your setup configurations by following the [previous steps](#set-up-dbt-semantic-layer). If your semantic models and metrics are still in your project, no changes are needed. If you've removed them, you'll need to set up the YAML configs again.

[![Delete the Semantic Layer configuration for a project.](/img/docs/dbt-cloud/semantic-layer/sl-delete-config.png?v=2 "Delete the Semantic Layer configuration for a project.")](#)Delete the Semantic Layer configuration for a project.

#### Additional configuration[​](#additional-configuration "Direct link to Additional configuration")

The following are the additional flexible configurations for Semantic Layer credentials.

##### Map service tokens to credentials[​](#map-service-tokens-to-credentials "Direct link to Map service tokens to credentials")

* After configuring your environment, you can map additional service tokens to the same credential if you have the required [permissions](https://docs.getdbt.com/docs/cloud/manage-access/about-user-access.md#permission-sets).
* Go to the **Credentials & service tokens** page and click the **+Add Service Token** button in the **Linked Service Tokens** section.
* Type the service token name and select the permission set you need (Semantic Layer Only and Metadata Only).
* Click **Save** to link the service token to the credential.
* Remember to copy and save the service token securely, as it won't be viewable again after generation.

[![Map additional service tokens to a credential.](/img/docs/dbt-cloud/semantic-layer/sl-add-service-token.gif?v=2 "Map additional service tokens to a credential.")](#)Map additional service tokens to a credential.

##### Unlink service tokens[​](#unlink-service-tokens "Direct link to Unlink service tokens")

* Unlink a service token from the credential by clicking **Unlink** under the **Linked service tokens** section. If you try to query the Semantic Layer with an unlinked credential, you'll experience an error in your BI tool because no valid token is mapped.

##### Manage from service token page[​](#manage-from-service-token-page "Direct link to Manage from service token page")

**View credential from service token**

* View your Semantic Layer credential directly by navigating to the **API tokens** and then **Service tokens** page.
* Select the service token to view the credential it's linked to. This is useful if you want to know which service tokens are mapped to credentials in your project.

###### Create a new service token[​](#create-a-new-service-token "Direct link to Create a new service token")

* From the **Service tokens** page, create a new service token and map it to the credential(s) (assuming the semantic layer permission exists). This is useful if you want to create a new service token and directly map it to a credential in your project.
* Make sure to select the correct permission set for the service token (Semantic Layer Only and Metadata Only).

[![Create a new service token and map credentials directly on the separate 'Service tokens page'.](/img/docs/dbt-cloud/semantic-layer/sl-create-service-token-page.png?v=2 "Create a new service token and map credentials directly on the separate 'Service tokens page'.")](#)Create a new service token and map credentials directly on the separate 'Service tokens page'.

#### Query the Semantic Layer[​](#query-the-semantic-layer "Direct link to Query the Semantic Layer")

This page will guide you on how to connect and use the following integrations to query your metrics:

* [Connect and query with Google Sheets](#connect-and-query-with-google-sheets)
* [Connect and query with Hex](#connect-and-query-with-hex)
* [Connect and query with Sigma](#connect-and-query-with-sigma)

The Semantic Layer enables you to connect and query your metric with various available tools like [PowerBI](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/power-bi.md), [Google Sheets](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/gsheets.md), [Hex](https://learn.hex.tech/docs/connect-to-data/data-connections/dbt-integration#dbt-semantic-layer-integration), [Microsoft Excel](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/excel.md), [Tableau](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/tableau.md), and more.

Query metrics using other tools such as [first-class integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md), [Semantic Layer APIs](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-api-overview.md), and [exports](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md) to expose tables of metrics and dimensions in your data platform and create a custom integrations.

##### Connect and query with Google Sheets[​](#connect-and-query-with-google-sheets "Direct link to Connect and query with Google Sheets")

The Google Sheets integration allows you to query your metrics using Google Sheets. This section will guide you on how to connect and use the Google Sheets integration.

To query your metrics using Google Sheets:

1. Make sure you have a [Gmail](http://gmail.com/) account.

2. To set up Google Sheets and query your metrics, follow the detailed instructions on [Google Sheets integration](https://docs.getdbt.com/docs/cloud-integrations/semantic-layer/gsheets.md).

3. Start exploring and querying metrics!

   <!-- -->

   * Query a metric, like `order_total`, and filter it with a dimension, like `order_date`.
   * You can also use the `group_by` parameter to group your metrics by a specific dimension.

[![Use the dbt Semantic Layer's Google Sheet integration to query metrics with a Query Builder menu.](/img/docs/dbt-cloud/semantic-layer/sl-gsheets.jpg?v=2 "Use the dbt Semantic Layer's Google Sheet integration to query metrics with a Query Builder menu.")](#)Use the dbt Semantic Layer's Google Sheet integration to query metrics with a Query Builder menu.

##### Connect and query with Hex[​](#connect-and-query-with-hex "Direct link to Connect and query with Hex")

This section will guide you on how to use the Hex integration to query your metrics using Hex. Select the appropriate tab based on your connection method:

* Query Semantic Layer with Hex
* Getting started with the Semantic Layer workshop

1. Navigate to the [Hex login page](https://app.hex.tech/login).
2. Sign in or make an account (if you don’t already have one).

* You can make Hex free trial accounts with your work email or a .edu email.

3. In the top left corner of your page, click on the **HEX** icon to go to the home page.
4. Then, click the **+ New project** button on the top right.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/hex_new.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

5. Go to the menu on the left side and select **Data browser**. Then select **Add a data connection**.
6. Click **Snowflake**. Provide your data connection a name and description. You don't need to your data warehouse credentials to use the Semantic Layer.

[![Select 'Data browser' and then 'Add a data connection' to connect to Snowflake.](/img/docs/dbt-cloud/semantic-layer/hex_new_data_connection.png?v=2 "Select 'Data browser' and then 'Add a data connection' to connect to Snowflake.")](#)Select 'Data browser' and then 'Add a data connection' to connect to Snowflake.

7. Under **Integrations**, toggle the dbt switch to the right to enable the dbt integration.

[![Click on the dbt toggle to enable the integration. ](/img/docs/dbt-cloud/semantic-layer/hex_dbt_toggle.png?v=2 "Click on the dbt toggle to enable the integration. ")](#)Click on the dbt toggle to enable the integration.

8. Enter the following information:

   <!-- -->

   * Select your version of dbt as 1.6 or higher
   * Enter your Environment ID
   * Enter your service or personal token
   * Make sure to click on the **Use Semantic Layer** toggle. This way, all queries are routed through dbt.
   * Click **Create connection** in the bottom right corner.

9. Hover over **More** on the menu shown in the following image and select **Semantic Layer**.

[![Hover over 'More' on the menu and select 'dbt Semantic Layer'.](/img/docs/dbt-cloud/semantic-layer/hex_make_sl_cell.png?v=2 "Hover over 'More' on the menu and select 'dbt Semantic Layer'.")](#)Hover over 'More' on the menu and select 'dbt Semantic Layer'.

10. Now, you should be able to query metrics using Hex! Try it yourself:

    <!-- -->

    * Create a new cell and pick a metric.
    * Filter it by one or more dimensions.
    * Create a visualization.

1) Click on the link provided to you in the workshop’s chat.
   <!-- -->
   * Look at the **Pinned message** section of the chat if you don’t see it right away.
2) Enter your email address in the textbox provided. Then, select **SQL and Python** to be taken to Hex’s home screen.

[![The 'Welcome to Hex' homepage.](/img/docs/dbt-cloud/semantic-layer/welcome_to_hex.png?v=2 "The 'Welcome to Hex' homepage.")](#)The 'Welcome to Hex' homepage.

3. Then click the purple Hex button in the top left corner.
4. Click the **Collections** button on the menu on the left.
5. Select the **Semantic Layer Workshop** collection.
6. Click the **Getting started with the Semantic Layer** project collection.

[![Click 'Collections' to select the 'Semantic Layer Workshop' collection.](/img/docs/dbt-cloud/semantic-layer/hex_collections.png?v=2 "Click 'Collections' to select the 'Semantic Layer Workshop' collection.")](#)Click 'Collections' to select the 'Semantic Layer Workshop' collection.

7. To edit this Hex notebook, click the **Duplicate** button from the project dropdown menu (as displayed in the following image). This creates a new copy of the Hex notebook that you own.

[![Click the 'Duplicate' button from the project dropdown menu to create a Hex notebook copy.](/img/docs/dbt-cloud/semantic-layer/hex_duplicate.png?v=2 "Click the 'Duplicate' button from the project dropdown menu to create a Hex notebook copy.")](#)Click the 'Duplicate' button from the project dropdown menu to create a Hex notebook copy.

8. To make it easier to find, rename your copy of the Hex project to include your name.

[![Rename your Hex project to include your name.](/img/docs/dbt-cloud/semantic-layer/hex_rename.png?v=2 "Rename your Hex project to include your name.")](#)Rename your Hex project to include your name.

9. Now, you should be able to query metrics using Hex! Try it yourself with the following example queries:

   * In the first cell, you can see a table of the `order_total` metric over time. Add the `order_count` metric to this table.
   * The second cell shows a line graph of the `order_total` metric over time. Play around with the graph! Try changing the time grain using the **Time unit** drop-down menu.
   * The next table in the notebook, labeled “Example\_query\_2”, shows the number of customers who have made their first order on a given day. Create a new chart cell. Make a line graph of `first_ordered_at` vs `customers` to see how the number of new customers each day changes over time.
   * Create a new semantic layer cell and pick one or more metrics. Filter your metric(s) by one or more dimensions.

[![Query metrics using Hex ](/img/docs/dbt-cloud/semantic-layer/hex_make_sl_cell.png?v=2 "Query metrics using Hex ")](#)Query metrics using Hex

##### Connect and query with Sigma[​](#connect-and-query-with-sigma "Direct link to Connect and query with Sigma")

This section will guide you on how to use the Sigma integration to query your metrics using Sigma. If you already have a Sigma account, simply log in and skip to step 6. Otherwise, you'll be using a Sigma account you'll create with Snowflake Partner Connect.

1. Go back to your Snowflake account. In the Snowflake UI, click on the home icon in the upper left corner. In the left sidebar, select **Data Products**. Then, select **Partner Connect**. Find the Sigma tile by scrolling or by searching for Sigma in the search bar. Click the tile to connect to Sigma.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-partner-connect.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

2. Select the Sigma tile from the list. Click the **Optional Grant** dropdown menu. Write **RAW** and **ANALYTICS** in the text box and then click **Connect**.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-optional-grant.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

3. Make up a company name and URL to use. It doesn’t matter what URL you use, as long as it’s unique.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-company-name.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

4. Enter your name and email address. Choose a password for your account.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-create-profile.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

5. Great! You now have a Sigma account. Before we get started, go back to Snowlake and open a blank worksheet. Run these lines.

* `grant all privileges on all views in schema analytics.SCHEMA to role pc_sigma_role;`
* `grant all privileges on all tables in schema analytics.SCHEMA to role pc_sigma_role;`

6. Click on your bubble in the top right corner. Click the **Administration** button from the dropdown menu.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-admin.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

7. Scroll down to the integrations section, then select **Add** next to the dbt integration.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-add-integration.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

8. In the **dbt Integration** section, fill out the required fields, and then hit save:

* Your dbt [service account token](https://docs.getdbt.com/docs/dbt-cloud-apis/service-tokens.md) or [personal access tokens](https://docs.getdbt.com/docs/dbt-cloud-apis/user-tokens.md).
* Your access URL of your existing Sigma dbt integration. Use `cloud.getdbt.com` as your access URL.
* Your dbt Environment ID.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-add-info.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

9. Return to the Sigma home page. Create a new workbook.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-make-workbook.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

10. Click on **Table**, then click on **SQL**. Select Snowflake `PC_SIGMA_WH` as your data connection.

[![Click the '+ New project' button on the top right](/img/docs/dbt-cloud/semantic-layer/sl-sigma-make-table.png?v=2 "Click the '+ New project' button on the top right")](#)Click the '+ New project' button on the top right

11. Go ahead and query a working metric in your project! For example, let's say you had a metric that measures various order-related values. Here’s how you would query it:
```

Example 4 (unknown):
```unknown
#### What's next[​](#whats-next "Direct link to What's next")

Great job on completing the comprehensive Semantic Layer guide 🎉! You should hopefully have gained a clear understanding of what the Semantic Layer is, its purpose, and when to use it in your projects.

You've learned how to:

* Set up your Snowflake environment and dbt, including creating worksheets and loading data.
* Connect and configure dbt with Snowflake.
* Build, test, and manage dbt projects, focusing on metrics and semantic layers.
* Run production jobs and query metrics with our available integrations.

For next steps, you can start defining your own metrics and learn additional configuration options such as [exports](https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports.md), [fill null values](https://docs.getdbt.com/docs/build/advanced-topics.md), [implementing Mesh with the Semantic Layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-faqs.md#how-can-i-implement-dbt-mesh-with-the-dbt-semantic-layer), and more.

Here are some additional resources to help you continue your journey:

* [Semantic Layer FAQs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-faqs.md)
* [Available integrations](https://docs.getdbt.com/docs/cloud-integrations/avail-sl-integrations.md)
* Demo on [how to define and query metrics with MetricFlow](https://www.loom.com/share/60a76f6034b0441788d73638808e92ac?sid=861a94ac-25eb-4fd8-a310-58e159950f5a)
* [Join our live demos](https://www.getdbt.com/resources/webinars/dbt-cloud-demos-with-experts)

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Quickstart with dbt Mesh

[Back to guides](https://docs.getdbt.com/guides.md)

dbt platform

Quickstart

Intermediate

[Menu ]()

#### Introduction[​](#introduction "Direct link to Introduction")

Mesh is a framework that helps organizations scale their teams and data assets effectively. It promotes governance best practices and breaks large projects into manageable sections — for faster data development. Mesh is available for [dbt Enterprise](https://www.getdbt.com/) accounts.

This guide will teach you how to set up a multi-project design using foundational concepts of [Mesh](https://www.getdbt.com/blog/what-is-data-mesh-the-definition-and-importance-of-data-mesh) and how to implement a data mesh in dbt:

* Set up a foundational project called “Jaffle | Data Analytics”
* Set up a downstream project called “Jaffle | Finance”
* Add model access, versions, and contracts
* Set up a dbt job that is triggered on completion of an upstream job

For more information on why data mesh is important, read this post: [What is data mesh? The definition and importance of data mesh](https://www.getdbt.com/blog/what-is-data-mesh-the-definition-and-importance-of-data-mesh).

Videos for you

You can check out [dbt Fundamentals](https://learn.getdbt.com/courses/dbt-fundamentals) for free if you're interested in course learning with videos.

You can also watch the [YouTube video on dbt and Snowflake](https://www.youtube.com/watch?v=kbCkwhySV_I\&list=PL0QYlrC86xQm7CoOH6RS7hcgLnd3OQioG).

##### Related content:[​](#related-content "Direct link to Related content:")

* [Data mesh concepts: What it is and how to get started](https://www.getdbt.com/blog/data-mesh-concepts-what-it-is-and-how-to-get-started)
* [Deciding how to structure your Mesh](https://docs.getdbt.com/best-practices/how-we-mesh/mesh-3-structures.md)
* [Mesh best practices guide](https://docs.getdbt.com/best-practices/how-we-mesh/mesh-4-implementation.md)
* [Mesh FAQs](https://docs.getdbt.com/best-practices/how-we-mesh/mesh-5-faqs.md)

#### Prerequisites​[​](#prerequisites "Direct link to Prerequisites​")

To leverage Mesh, you need the following:

* You must have a [dbt Enterprise-tier account](https://www.getdbt.com/get-started/enterprise-contact-pricing) [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")

* You have access to a cloud data platform, permissions to load the sample data tables, and dbt permissions to create new projects.

* This guide uses the Jaffle Shop sample data, including `customers`, `orders`, and `payments` tables. Follow the provided instructions to load this data into your respective data platform:

  <!-- -->

  * [Snowflake](https://docs.getdbt.com/guides/snowflake.md?step=3)
  * [Databricks](https://docs.getdbt.com/guides/databricks.md?step=3)
  * [Redshift](https://docs.getdbt.com/guides/redshift.md?step=3)
  * [BigQuery](https://docs.getdbt.com/guides/bigquery.md?step=3)
  * [Fabric](https://docs.getdbt.com/guides/microsoft-fabric.md?step=2)
  * [Starburst Galaxy](https://docs.getdbt.com/guides/starburst-galaxy.md?step=2)

This guide assumes you have experience with or fundamental knowledge of dbt. Take the [dbt Fundamentals](https://learn.getdbt.com/courses/dbt-fundamentals) course first if you are brand new to dbt.

#### Create and configure two projects[​](#create-and-configure-two-projects "Direct link to Create and configure two projects")

In this section, you'll create two new, empty projects in dbt to serve as your foundational and downstream projects:

* **Foundational projects** (or upstream projects) typically contain core models and datasets that serve as the base for further analysis and reporting.
* **Downstream projects** build on these foundations, often adding more specific transformations or business logic for dedicated teams or purposes.

For example, the always-enterprising and fictional account "Jaffle Labs" will create two projects for their data analytics and finance team: Jaffle | Data Analytics and Jaffle | Finance.

[![Create two new dbt projects named 'Jaffle | Data Analytics' and 'Jaffle Finance' ](/img/guides/dbt-mesh/project_names.png?v=2 "Create two new dbt projects named 'Jaffle | Data Analytics' and 'Jaffle Finance' ")](#)Create two new dbt projects named 'Jaffle | Data Analytics' and 'Jaffle Finance'

To [create](https://docs.getdbt.com/docs/cloud/about-cloud-setup.md) a new project in dbt:

1. From **Account settings**, go to **Projects**. Click **New project**.

2. Enter a project name and click **Continue**.

   <!-- -->

   * Use "Jaffle | Data Analytics" for one project
   * Use "Jaffle | Finance" for the other project

3. Select your data platform, then **Next** to set up your connection.

4. In the **Configure your environment** section, enter the **Settings** for your new project.

5. Click **Test Connection**. This verifies that dbt can access your data platform account.

6. Click **Next** if the test succeeded. If it fails, you might need to go back and double-check your settings.

   <!-- -->

   * For this guide, make sure you create a single [development](https://docs.getdbt.com/docs/dbt-cloud-environments.md#create-a-development-environment) and [Deployment](https://docs.getdbt.com/docs/deploy/deploy-environments.md) per project.

     <!-- -->

     * For "Jaffle | Data Analytics", set the default database to `jaffle_da`.
     * For "Jaffle | Finance", set the default database to `jaffle_finance`.

7. Continue the prompts to complete the project setup. Once configured, each project should have:

   <!-- -->

   * A data platform connection
   * New git repo
   * One or more [environments](https://docs.getdbt.com/docs/deploy/deploy-environments.md) (such as development, deployment)

[![Navigate to Account settings.](/img/guides/dbt-ecosystem/dbt-python-snowpark/5-development-schema-name/1-settings-gear-icon.png?v=2 "Navigate to Account settings.")](#)Navigate to Account settings.

[![Select projects from the menu.](/img/guides/dbt-mesh/select_projects.png?v=2 "Select projects from the menu.")](#)Select projects from the menu.

[![Create a new project in the Studio IDE.](/img/guides/dbt-mesh/create_a_new_project.png?v=2 "Create a new project in the Studio IDE.")](#)Create a new project in the Studio IDE.

[![Name your project.](/img/guides/dbt-mesh/enter_project_name.png?v=2 "Name your project.")](#)Name your project.

[![Select the relevant connection for your projects.](/img/guides/dbt-mesh/select_a_connection.png?v=2 "Select the relevant connection for your projects.")](#)Select the relevant connection for your projects.

##### Create a production environment[​](#create-a-production-environment "Direct link to Create a production environment")

In dbt, each project can have one deployment environment designated as "Production.". You must set up a ["Production" or "Staging" deployment environment](https://docs.getdbt.com/docs/deploy/deploy-environments.md) for each project you want to "mesh" together. This enables you to leverage Catalog in the [later steps](https://docs.getdbt.com/guides/mesh-qs.md?step=5#create-and-run-a-dbt-cloud-job) of this guide.

To set a production environment:

1. Navigate to **Deploy** -> **Environments**, then click **Create New Environment**.
2. Select **Deployment** as the environment type.
3. Under **Set deployment type**, select the **Production** button.
4. Select the dbt version.
5. Continue filling out the fields as necessary in the **Deployment connection** and **Deployment credentials** sections.
6. Click **Test Connection** to confirm the deployment connection.
7. Click **Save** to create a production environment.

[![Set your production environment as the default environment in your Environment Settings](/img/docs/dbt-cloud/using-dbt-cloud/prod-settings-1.png?v=2 "Set your production environment as the default environment in your Environment Settings")](#)Set your production environment as the default environment in your Environment Settings

#### Set up a foundational project[​](#set-up-a-foundational-project "Direct link to Set up a foundational project")

This upstream project is where you build your core data assets. This project will contain the raw data sources, staging models, and core business logic.

dbt enables data practitioners to develop in their tool of choice and comes equipped with a local [dbt CLI](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md) or in-browser [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md).

In this section of the guide, you will set the "Jaffle | Data Analytics" project as your foundational project using the Studio IDE.

1. First, navigate to the **Develop** page to verify your setup.
2. Click **Initialize dbt project** if you’ve started with an empty repo.
3. Delete the `models/example` folder.
4. Navigate to the `dbt_project.yml` file and rename the project (line 5) from `my_new_project` to `analytics`.
5. In your `dbt_project.yml` file, remove lines 39-42 (the `my_new_project` model reference).
6. In the **File Catalog**, hover over the project directory and click the **...**, then select **Create file**.
7. Create two new folders: `models/staging` and `models/core`.

##### Staging layer[​](#staging-layer "Direct link to Staging layer")

Now that you've set up the foundational project, let's start building the data assets. Set up the staging layer as follows:

1. Create a new YAML file `models/staging/sources.yml`.
2. Declare the sources by copying the following into the file and clicking **Save**.

models/staging/sources.yml
```

---

## run all the models associated with failed tests from the prior invocation of dbt build

**URL:** llms-txt#run-all-the-models-associated-with-failed-tests-from-the-prior-invocation-of-dbt-build

dbt build --select "1+result:fail" --state path/to/artifacts

---

## run only data tests defined singularly

**URL:** llms-txt#run-only-data-tests-defined-singularly

dbt test --select "test_type:singular"

---

## First, define the group and owner

**URL:** llms-txt#first,-define-the-group-and-owner

groups:
  - name: customer_success
    owner:
      name: Customer Success Team
      email: cx@jaffle.shop

---

## use 'parse' command to load a Manifest

**URL:** llms-txt#use-'parse'-command-to-load-a-manifest

res: dbtRunnerResult = dbtRunner().invoke(["parse"])
manifest: Manifest = res.result

---

## Run tests on all models with a particular tag (direct + indirect)

**URL:** llms-txt#run-tests-on-all-models-with-a-particular-tag-(direct-+-indirect)

dbt test --select "tag:my_model_tag"

---

## models in `models/marketing/ will be built in the "*_marketing" schema

**URL:** llms-txt#models-in-`models/marketing/-will-be-built-in-the-"*_marketing"-schema

**Contents:**
  - Custom target names
  - Data health signals Preview
  - Data health signals [Preview](https://docs.getdbt.com/docs/dbt-versions/product-lifecycles "Go to https://docs.getdbt.com/docs/dbt-versions/product-lifecycles")
  - Data health tile EnterpriseEnterprise +
  - Data health tile [Enterprise](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")[Enterprise +](https://www.getdbt.com/pricing "Go to https://www.getdbt.com/pricing")
  - Databricks and Apache Iceberg
  - dbt Catalog FAQs
  - dbt platform compatible track - changelog

models:
  my_project:
    marketing:
      +schema: marketing

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

{{ default_schema }}_{{ custom_schema_name | trim }}

{% macro generate_schema_name(custom_schema_name, node) -%}

{%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

{%- else -%}
    # The following is incorrect as it omits {{ default_schema }} before {{ custom_schema_name | trim }}. 
        {{ custom_schema_name | trim }}

-- put this in macros/get_custom_schema.sql

{% macro generate_schema_name(custom_schema_name, node) -%}
    {{ generate_schema_name_for_env(custom_schema_name, node) }}
{%- endmacro %}

select *
from a_big_table

-- limit the amount of data queried in dev
{% if target.name != 'prod' %}
where created_at > date_trunc('month', current_date)
{% endif %}

<iframe src='https://1234.metadata.ACCESS_URL/exposure-tile?uniqueId=exposure.EXPOSURE_NAME&environmentType=staging&environmentId=123456789&token=YOUR_METADATA_TOKEN' title='Exposure status tile' height='400'></iframe>
   
   https://metadata.ACCESS_URL/exposure-tile?uniqueId=exposure.EXPOSURE_NAME&environmentType=production&environmentId=220370&token=<YOUR_METADATA_TOKEN>
   
   https://metadata.ACCESS_URL/exposure-tile?uniqueId=exposure.EXPOSURE_NAME&environmentType=production&environmentId=ENV_ID_NUMBER&token=<YOUR_METADATA_TOKEN>
   
<iframe src='https://metadata.YOUR_ACCESS_URL/exposure-tile?name=<exposure_name>&jobId=<job_id>&token=<metadata_only_token>' title='Exposure Status Tile'></iframe>

<iframe src='https://metadata.emea.dbt.com/exposure-tile?name=<exposure_name>&jobId=<job_id>&token=<metadata_only_token>' title='Exposure Status Tile'></iframe>

https://metadata.YOUR_ACCESS_URL/exposure-tile?name=<exposure_name>&jobId=<job_id>&token=<metadata_only_token>

https://metadata.cloud.getdbt.com/exposure-tile?name=<exposure_name>&jobId=<job_id>&token=<metadata_only_token>

https://metadata.YOUR_ACCESS_URL/exposure-tile?name=<exposure_name>&jobId=<job_id>&token=<metadata_only_token>

https://metadata.au.dbt.com/exposure-tile?name=<exposure_name>&jobId=<job_id>&token=<metadata_only_token>

{{ config(
    tblproperties={
      'delta.enableIcebergCompatV2': 'true'
      'delta.universalFormat.enabledFormats': 'iceberg'
    }
 ) }}

catalogs:
  - name: unity_catalog
    active_write_integration: unity_catalog_integration
    write_integrations:
      - name: unity_catalog_integration
        table_format: iceberg
        catalog_type: unity
        file_format: delta

{{
    config(
        materialized = 'table',
        catalog_name = 'unity_catalog'

select * from {{ ref('jaffle_shop_customers') }}

**Examples:**

Example 1 (unknown):
```unknown
#### Understanding custom schemas[​](#understanding-custom-schemas "Direct link to Understanding custom schemas")

When first using custom schemas, it's a common misunderstanding to assume that a model *only* uses the new `schema` configuration; for example, a model that has the configuration `schema: marketing` would be built in the `marketing` schema. However, dbt puts it in a schema like `<target_schema>_marketing`.

There's a good reason for this deviation. Each dbt user has their own target schema for development (refer to [Managing Environments](#managing-environments)). If dbt ignored the target schema and only used the model's custom schema, every dbt user would create models in the same schema and would overwrite each other's work.

By combining the target schema and the custom schema, dbt ensures that objects it creates in your data warehouse don't collide with one another.

If you prefer to use different logic for generating a schema name, you can change the way dbt generates a schema name (see below).

##### How does dbt generate a model's schema name?[​](#how-does-dbt-generate-a-models-schema-name "Direct link to How does dbt generate a model's schema name?")

dbt uses a default macro called `generate_schema_name` to determine the name of the schema that a model should be built in.

The following code represents the default macro's logic:
```

Example 2 (unknown):
```unknown
<br />

<!-- -->

💡 Use Jinja's whitespace control to tidy your macros!

When you're modifying macros in your project, you might notice extra white space in your code in the `target/compiled` folder.

You can remove unwanted spaces and lines with Jinja's [whitespace control](https://docs.getdbt.com/faqs/Jinja/jinja-whitespace.md) by using a minus sign. For example, use `{{- ... -}}` or `{%- ... %}` around your macro definitions (such as `{%- macro generate_schema_name(...) -%} ... {%- endmacro -%}`).

#### Changing the way dbt generates a schema name[​](#changing-the-way-dbt-generates-a-schema-name "Direct link to Changing the way dbt generates a schema name")

If your dbt project has a custom macro called `generate_schema_name`, dbt will use it instead of the default macro. This allows you to customize the name generation according to your needs.

To customize this macro, copy the example code in the section [How does dbt generate a model's schema name](#how-does-dbt-generate-a-models-schema-name) into a file named `macros/generate_schema_name.sql` and make changes as necessary.

Be careful. dbt will ignore any custom `generate_schema_name` macros included in installed packages.

 Warning: Don't replace \`default\_schema\` in the macro

If you're modifying how dbt generates schema names, don't just replace `{{ default_schema }}_{{ custom_schema_name | trim }}` with `{{ custom_schema_name | trim }}` in the `generate_schema_name` macro.

If you remove `{{ default_schema }}`, it causes developers to override each other's models if they create their own custom schemas. This can also cause issues during development and continuous integration (CI).

❌ The following code block is an example of what your code *should not* look like:
```

Example 3 (unknown):
```unknown
##### generate\_schema\_name arguments[​](#generate_schema_name-arguments "Direct link to generate_schema_name arguments")

| Argument             | Description                                                                                  | Example                                              |
| -------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| custom\_schema\_name | The configured value of `schema` in the specified node, or `none` if a value is not supplied | `marketing`                                          |
| node                 | The `node` that is currently being processed by dbt                                          | `{"name": "my_model", "resource_type": "model",...}` |

##### Jinja context available in generate\_schema\_name[​](#jinja-context-available-in-generate_schema_name "Direct link to Jinja context available in generate_schema_name")

If you choose to write custom logic to generate a schema name, it's worth noting that not all variables and methods are available to you when defining this logic. In other words: the `generate_schema_name` macro is compiled with a limited Jinja context.

The following context methods *are* available in the `generate_schema_name` macro:

| Jinja context                                                                     | Type     | Available          |
| --------------------------------------------------------------------------------- | -------- | ------------------ |
| [target](https://docs.getdbt.com/reference/dbt-jinja-functions/target.md)         | Variable | ✅                 |
| [env\_var](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var.md)      | Variable | ✅                 |
| [var](https://docs.getdbt.com/reference/dbt-jinja-functions/var.md)               | Variable | Limited, see below |
| [exceptions](https://docs.getdbt.com/reference/dbt-jinja-functions/exceptions.md) | Macro    | ✅                 |
| [log](https://docs.getdbt.com/reference/dbt-jinja-functions/log.md)               | Macro    | ✅                 |
| Other macros in your project                                                      | Macro    | ✅                 |
| Other macros in your packages                                                     | Macro    | ✅                 |

##### Which vars are available in generate\_schema\_name?[​](#which-vars-are-available-in-generate_schema_name "Direct link to Which vars are available in generate_schema_name?")

Globally-scoped variables and variables defined on the command line with [--vars](https://docs.getdbt.com/docs/build/project-variables.md) are accessible in the `generate_schema_name` context.

##### Managing different behaviors across packages[​](#managing-different-behaviors-across-packages "Direct link to Managing different behaviors across packages")

See docs on macro `dispatch`: ["Managing different global overrides across packages"](https://docs.getdbt.com/reference/dbt-jinja-functions/dispatch.md)

#### A built-in alternative pattern for generating schema names[​](#a-built-in-alternative-pattern-for-generating-schema-names "Direct link to A built-in alternative pattern for generating schema names")

A common customization is to use the custom schema in production when provided, with the target schema serving only as a fallback if no custom schema is specified. In other environments, such as development and CI, custom schema configurations are ignored, defaulting to the target schema instead.

Production Environment (`target.name == 'prod'`)

| Target schema   | Custom schema | Resulting schema |
| --------------- | ------------- | ---------------- |
| analytics\_prod | None          | analytics\_prod  |
| analytics\_prod | marketing     | marketing        |

Development/CI Environment (`target.name != 'prod'`)

| Target schema            | Custom schema | Resulting schema         |
| ------------------------ | ------------- | ------------------------ |
| alice\_dev               | None          | alice\_dev               |
| alice\_dev               | marketing     | alice\_dev               |
| dbt\_cloud\_pr\_123\_456 | None          | dbt\_cloud\_pr\_123\_456 |
| dbt\_cloud\_pr\_123\_456 | marketing     | dbt\_cloud\_pr\_123\_456 |

Similar to the regular macro, this approach guarantees that schemas from different environments will not collide.

dbt ships with a macro for this use case — called `generate_schema_name_for_env` — which is disabled by default. To enable it, add a custom `generate_schema_name` macro to your project that contains the following code:

macros/get\_custom\_schema.sql
```

Example 4 (unknown):
```unknown
When using this macro, you'll need to set the target name in your production job to `prod`.

#### Managing environments[​](#managing-environments "Direct link to Managing environments")

In the `generate_schema_name` macro examples shown in the [built-in alternative pattern](#a-built-in-alternative-pattern-for-generating-schema-names) section, the `target.name` context variable is used to change the schema name that dbt generates for models. If the `generate_schema_name` macro in your project uses the `target.name` context variable, you must ensure that your different dbt environments are configured accordingly. While you can use any naming scheme you'd like, we typically recommend:

* **dev** — Your local development environment; configured in a `profiles.yml` file on your computer.
* **ci** — A [continuous integration](https://docs.getdbt.com/docs/cloud/git/connect-github.md) environment running on pull requests in GitHub, GitLab, and so on.
* **prod** — The production deployment of your dbt project, like in dbt, Airflow, or [similar](https://docs.getdbt.com/docs/deploy/deployments.md).

If your schema names are being generated incorrectly, double-check your target name in the relevant environment.

For more information, consult the [managing environments in dbt Core](https://docs.getdbt.com/docs/core/dbt-core-environments.md) guide.

#### Related docs[​](#related-docs "Direct link to Related docs")

* [Customize dbt models database, schema, and alias](https://docs.getdbt.com/guides/customize-schema-alias.md?step=1) to learn how to customize dbt models database, schema, and alias
* [Custom database](https://docs.getdbt.com/docs/build/custom-databases.md) to learn how to customize dbt model database
* [Custom aliases](https://docs.getdbt.com/docs/build/custom-aliases.md) to learn how to customize dbt model alias name

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Custom target names

#### dbt Scheduler[​](#dbt-scheduler "Direct link to dbt Scheduler")

You can define a custom target name for any dbt job to correspond to settings in your dbt project. This is helpful if you have logic in your dbt project that behaves differently depending on the specified target, for example:
```

---
