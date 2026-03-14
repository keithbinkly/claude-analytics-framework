# Jinja-Sql-Optimizer - Utility Packages

**Pages:** 2

---

## ignore all .py files with "codegen" in the filename

**URL:** llms-txt#ignore-all-.py-files-with-"codegen"-in-the-filename

---

## Convert the runGeneratedAt, executeStartedAt, and executeCompletedAt columns to datetime

**URL:** llms-txt#convert-the-rungeneratedat,-executestartedat,-and-executecompletedat-columns-to-datetime

model_df['runGeneratedAt'] = pd.to_datetime(model_df['runGeneratedAt'])
model_df['executeStartedAt'] = pd.to_datetime(model_df['executeStartedAt'])
model_df['executeCompletedAt'] = pd.to_datetime(model_df['executeCompletedAt'])

---
