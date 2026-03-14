# Jinja-Sql-Optimizer - Jinja Basics

**Pages:** 3

---

## This change (from Jinja to dbt templater) will make linting slower

**URL:** llms-txt#this-change-(from-jinja-to-dbt-templater)-will-make-linting-slower

---

## Utility macros

**URL:** llms-txt#utility-macros

Our dbt project heavily uses this suite of utility macros, especially:
- `surrogate_key`
- `test_equality`
- `pivot`
{% enddocs %}

{% docs __snowplow__ %}

---

## repository_root/my_dbt_project_in_a_subdirectory/packages.yml

**URL:** llms-txt#repository_root/my_dbt_project_in_a_subdirectory/packages.yml

**Contents:**
  - Lint and format your code

packages:
  - local: ../shared_macros

[sqlfluff]
templater = dbt

**Examples:**

Example 1 (unknown):
```unknown
In this example, `../shared_macros` is a relative path that tells dbt to look for:

* `..` — Go one directory up (to `repository_root`).
* `/shared_macros` — Find the `shared_macros` folder in the root directory.

To work around this limitation, use the [Studio IDE](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/develop-in-the-cloud.md), which fully supports relative paths in `packages.yml`.

#### FAQs[​](#faqs "Direct link to FAQs")

 What's the difference between the dbt CLI and dbt Core?

The Cloud CLI and [dbt Core](https://github.com/dbt-labs/dbt-core), an open-source project, are both command line tools that enable you to run dbt commands.

The key distinction is the Cloud CLI is tailored for dbt's infrastructure and integrates with all its [features](https://docs.getdbt.com/docs/cloud/about-cloud/dbt-cloud-features).

 How do I run both the dbt CLI and dbt Core?

For compatibility, both the Cloud CLI and dbt Core are invoked by running `dbt`. This can create path conflicts if your operating system selects one over the other based on your $PATH environment variable (settings).

If you have dbt Core installed locally, either:

1. Install using the `pip3 install dbt` [pip](https://docs.getdbt.com/docs/cloud/cloud-cli-installation.md?install=pip#install-dbt-cloud-cli) command.
2. Install natively, ensuring you either deactivate the virtual environment containing dbt Core or create an alias for the Cloud CLI.
3. (Advanced users) Install natively, but modify the $PATH environment variable to correctly point to the Cloud CLI binary to use both Cloud CLI and dbt Core together.

You can always uninstall the Cloud CLI to return to using dbt Core.

 How to create an alias?

To create an alias for the Cloud CLI:<br />

1. Open your shell's profile configuration file. Depending on your shell and system, this could be `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, or another file.<br />

2. Add an alias that points to the Cloud CLI binary. For example:`alias dbt-cloud="path_to_dbt_cloud_cli_binary`

   Replace `path_to_dbt_cloud_cli_binary` with the actual path to the Cloud CLI binary, which is `/opt/homebrew/bin/dbt`. With this alias, you can use the command `dbt-cloud` to invoke the Cloud CLI.<br />

3. Save the file and then either restart your shell or run `source` on the profile file to apply the changes. As an example, in bash you would run: `source ~/.bashrc`<br />

4. Test and use the alias to run commands:<br />

   * To run the Cloud CLI, use the `dbt-cloud` command: `dbt-cloud command_name`. Replace 'command\_name' with the specific dbt command you want to execute. <br />
   * To run the dbt Core, use the `dbt` command: `dbt command_name`. Replace 'command\_name' with the specific dbt command you want to execute. <br />

This alias will allow you to use the `dbt-cloud` command to invoke the Cloud CLI while having dbt Core installed natively.

 Why am I receiving a \`Stuck session\` error when trying to run a new command?

TheCloud CLI allows only one command that writes to the data warehouse at a time. If you attempt to run multiple write commands simultaneously (for example, `dbt run` and `dbt build`), you will encounter a `stuck session` error. To resolve this, cancel the specific invocation by passing its ID to the cancel command. For more information, refer to [parallel execution](https://docs.getdbt.com/reference/dbt-commands.md#parallel-execution).

I'm getting a "Session occupied" error in dbt CLI?

If you're receiving a `Session occupied` error in the Cloud CLI or if you're experiencing a long-running session, you can use the `dbt invocation list` command in a separate terminal window to view the status of your active session. This helps debug the issue and identify the arguments that are causing the long-running session.

To cancel an active session, use the `Ctrl + Z` shortcut.

To learn more about the `dbt invocation` command, see the [dbt invocation command reference](https://docs.getdbt.com/reference/commands/invocation.md).

Alternatively, you can reattach to your existing session with `dbt reattach` and then press `Control-C` and choose to cancel the invocation.

#### Was this page helpful?

YesNo

[Privacy policy](https://www.getdbt.com/cloud/privacy-policy)[Create a GitHub issue](https://github.com/dbt-labs/docs.getdbt.com/issues)

This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.


---

### Lint and format your code

Enhance your development workflow by integrating with popular linters and formatters like [SQLFluff](https://sqlfluff.com/), [sqlfmt](http://sqlfmt.com/), [Black](https://black.readthedocs.io/en/latest/), and [Prettier](https://prettier.io/). Leverage these powerful tools directly in the Studio IDE without interrupting your development flow.

Details

What are linters and formatters?

Linters analyze code for errors, bugs, and style issues, while formatters fix style and formatting rules. Read more about when to use linters or formatters in the [FAQs](#faqs)

In the Studio IDE, you can perform linting, auto-fix, and formatting on five different file types:

* SQL — [Lint](#lint) and fix with SQLFluff, and [format](#format) with sqlfmt
* YAML, Markdown, and JSON — Format with Prettier
* Python — Format with Black

Each file type has its own unique linting and formatting rules. You can [customize](#customize-linting) the linting process to add more flexibility and enhance problem and style detection.

By default, the IDE uses sqlfmt rules to format your code, making it convenient to use right away. However, if you have a file named `.sqlfluff` in the root directory of your dbt project, the IDE will default to SQLFluff rules instead.

[![Use SQLFluff to lint/format your SQL code, and view code errors in the Code Quality tab.](/img/docs/dbt-cloud/cloud-ide/sqlfluff.gif?v=2 "Use SQLFluff to lint/format your SQL code, and view code errors in the Code Quality tab.")](#)Use SQLFluff to lint/format your SQL code, and view code errors in the Code Quality tab.

[![Use sqlfmt to format your SQL code.](/img/docs/dbt-cloud/cloud-ide/sqlfmt.gif?v=2 "Use sqlfmt to format your SQL code.")](#)Use sqlfmt to format your SQL code.

[![Format YAML, Markdown, and JSON files using Prettier.](/img/docs/dbt-cloud/cloud-ide/prettier.gif?v=2 "Format YAML, Markdown, and JSON files using Prettier.")](#)Format YAML, Markdown, and JSON files using Prettier.

[![Use the config button to select your tool.](/img/docs/dbt-cloud/cloud-ide/ide-sql-popup.png?v=2 "Use the config button to select your tool.")](#)Use the config button to select your tool.

[![Customize linting by configuring your own linting code rules, including dbtonic linting/styling.](/img/docs/dbt-cloud/cloud-ide/ide-sqlfluff-config.png?v=2 "Customize linting by configuring your own linting code rules, including dbtonic linting/styling.")](#)Customize linting by configuring your own linting code rules, including dbtonic linting/styling.

#### Lint[​](#lint "Direct link to Lint")

With the Studio IDE, you can seamlessly use [SQLFluff](https://sqlfluff.com/), a configurable SQL linter, to warn you of complex functions, syntax, formatting, and compilation errors. This integration allows you to run checks, fix, and display any code errors directly within the Cloud Studio IDE:

* Works with Jinja and SQL,
* Comes with built-in [linting rules](https://docs.sqlfluff.com/en/stable/rules.html). You can also [customize](#customize-linting) your own linting rules.
* Empowers you to [enable linting](#enable-linting) with options like **Lint** (displays linting errors and recommends actions) or **Fix** (auto-fixes errors in the Studio IDE).
* Displays a **Code Quality** tab to view code errors, provides code quality visibility and management.

Ephemeral models not supported

Linting doesn't support ephemeral models in dbt v1.5 and lower. Refer to the [FAQs](#faqs) for more info.

##### Enable linting[​](#enable-linting "Direct link to Enable linting")

Linting is available on all branches, including your protected primary git branch. Since the Studio IDE prevents commits to the protected branch, it prompts you to commit those changes to a new branch.

1. To enable linting, open a `.sql` file and click the **Code Quality** tab.

2. Click on the **`</> Config`** button on the bottom right side of the [console section](https://docs.getdbt.com/docs/cloud/dbt-cloud-ide/ide-user-interface.md#console-section), below the **File editor**.

3. In the code quality tool config pop-up, you have the option to select **sqlfluff** or **sqlfmt**.

4. To lint your code, select the **sqlfluff** radio button. (Use sqlfmt to [format](#format) your code)

5. Once you've selected the **sqlfluff** radio button, go back to the console section (below the **File editor**) to select the **Lint** or **Fix** dropdown button:

   <!-- -->

   * **Lint** button — Displays linting issues in the Studio IDE as wavy underlines in the **File editor**. You can hover over an underlined issue to display the details and actions, including a **Quick Fix** option to fix all or specific issues. After linting, you'll see a message confirming the outcome. Linting doesn't rerun after saving. Click **Lint** again to rerun linting.
   * **Fix** button — Automatically fixes linting errors in the **File editor**. When fixing is complete, you'll see a message confirming the outcome.
   * Use the **Code Quality** tab to view and debug any code errors.

[![Use the Lint or Fix button in the console section to lint or auto-fix your code.](/img/docs/dbt-cloud/cloud-ide/ide-lint-format-console.gif?v=2 "Use the Lint or Fix button in the console section to lint or auto-fix your code.")](#)Use the Lint or Fix button in the console section to lint or auto-fix your code.

##### Customize linting[​](#customize-linting "Direct link to Customize linting")

SQLFluff is a configurable SQL linter, which means you can configure your own linting rules instead of using the default linting settings in the IDE. You can exclude files and directories by using a standard `.sqlfluffignore` file. Learn more about the syntax in the [.sqlfluffignore syntax docs](https://docs.sqlfluff.com/en/stable/configuration.html#id2).

To configure your own linting rules:

1. Create a new file in the root project directory (the parent or top-level directory for your files). Note: The root project directory is the directory where your `dbt_project.yml` file resides.
2. Name the file `.sqlfluff` (make sure you add the `.` before `sqlfluff`).
3. [Create](https://docs.sqlfluff.com/en/stable/configuration/setting_configuration.html#new-project-configuration) and add your custom config code.
4. Save and commit your changes.
5. Restart the Studio IDE.
6. Test it out and happy linting!

###### Snapshot linting[​](#snapshot-linting "Direct link to Snapshot linting")

By default, dbt lints all modified `.sql` files in your project, including snapshots. [Snapshots](https://docs.getdbt.com/docs/build/snapshots.md) can be defined in YAML *and* `.sql` files, but their SQL isn't lintable and can cause errors during linting.

To prevent SQLFluff from linting snapshot files, add the snapshots directory to your `.sqlfluffignore` file (for example `snapshots/`).

Note that you should explicitly exclude snapshots in your `.sqlfluffignore` file since dbt doesn't automatically ignore snapshots on the backend.

##### Configure dbtonic linting rules[​](#configure-dbtonic-linting-rules "Direct link to Configure dbtonic linting rules")

Refer to the [Jaffle shop SQLFluff config file](https://github.com/dbt-labs/jaffle-shop-template/blob/main/.sqlfluff) for dbt-specific (or dbtonic) linting rules we use for our own projects:

dbtonic config code example provided by dbt Labs
```

---
