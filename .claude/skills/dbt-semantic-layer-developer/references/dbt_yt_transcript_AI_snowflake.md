Building Agentic Workflows Using The dbt MCP Server And Snowflake

Introductions and Theme

Hey everyone, thanks for joining us today. Our talk for Snowflake Build is going to be around building agentic workflows using the dbt MCP server and Snowflake. Who do you have here with you today? My name is Sarah Golinsky. I’m a technical product marketing manager over at dbt Labs. I’m Jason Ganz. I’m the senior manager of developer experience and AI at dbt Labs.

From about 2016 to 2023, we saw the modern data stack emerge to help organizations transform raw data into trustworthy and usable insights. It gave us reliable pipelines, governed metrics, and scalable transformation workflows—basically everything data teams needed to build confidence in what they were measuring, reporting, and making decisions on. But times have changed, and data practitioners—really all of us—are now faced with widespread AI adoption and are left to tackle what might feel like a familiar set of challenges. These challenges have resurfaced in new forms and have been shaped by new technologies.

In the modern data stack, we asked questions like: Can I trust the data behind this dashboard? Are we all using the same definition of revenue? How do I scale my models and keep everything in sync as teams grow? In this AI era, those questions haven’t disappeared; they’ve evolved. Now they sound more like: Can I trust the answer an AI system gives me? How do I know that it’s grounded in the right metric or logic? How do I manage dozens, if not hundreds, of models, agents, and prompts across workflows without losing control?

The truth is AI is running into the exact same problems the modern data stack already sought to solve: reliability, governance, scalability, access, and safe automation. That’s where the Model Context Protocol, or MCP, comes in. MCP acts as a standardized bridge between these two eras, connecting AI systems to the trusted data models, definitions, and workflows that we’ve spent a lot of resources and time building. It brings the discipline and governance of the modern data stack into the world of intelligent systems so we can move faster without sacrificing trust.

What MCP Is and Why It Matters

MCP—Model Context Protocol—is an open-source standard by Anthropic that lets AI applications talk to external systems in a consistent and governed way. It follows a client-server architecture pattern, and you can think of it like a universal adapter that any host, like Claude Desktop or Cursor, can use to connect to one or more MCP servers.

Why does this matter? It gives us interoperability—being able to swap hosts or servers without rewiring anything. Permissioning—having one policy model that governs access everywhere for anyone. Auditability—every request and response is typed and logged. That’s what makes it safe enough for enterprise data and AI to meet.

Each server in the MCP ecosystem can expose three capabilities:

- Tools: executable functions AI applications can invoke to perform actions, like running an API call or a database query.

- Resources: data sources that provide context to the AI system, like file contents, records, or query results.

- Prompts: reusable templates that structure how AI interacts with language models.

Together, these three form a stable interface for AI systems to work with trusted tools and data without breaking governance. You don’t need a custom adapter for each AI app anymore—they all simply speak MCP.

Where dbt Comes In

Earlier this year, we released the dbt MCP server. This server connects everything you already trust in your dbt project to an AI-enabled client. Think of it as a glue layer. AI asks a question and the dbt MCP server maps that to the right bit of context—your models, your metrics, your job details—compiles what’s needed, and returns structured and reliable results. It brings more than just vibes to your analytics code.

You have two options for deploying the dbt MCP server:

- Local: runs on your laptop alongside your dbt project. It’s perfect for local development with something like Cursor or Claude since it ensures the code you’re writing locally matches what the agent has access to.

- Remote: hosted in the dbt platform, with clients connecting over the network. It’s easier to set up, maintain, and manage because it’s already running in dbt. Remote servers enable longer-running, multi-user, multi-tenant agents and can be accessed by web applications. Keep this in mind as you evaluate use cases and map to the right deployment option.

Why use the dbt MCP server? Consider the context gap we see when applying LLMs to data use cases. If you ask an LLM “What is the capital of California?” it says Sacramento because it learned it in training. If you ask “What was the temperature in Sacramento today?” it can do a web search and give you a high and low. But if you ask “What are our bestselling products in Sacramento?” it doesn’t know how to respond because it lacks your business context—what products you sell, where you sell them, and how well they perform. That’s the gap.

When you give AI agents structured and governed context, you get reliability. Without structured context, agents guess your data model, hallucinate table names, invent joins, or misunderstand metric logic. Plug them into dbt through the MCP server, and they have direct access to models, joins, metric definitions, lineage, dependencies, and job runs—the same source of truth your data team uses. Instead of guessing what the customers table looks like or how revenue is calculated, the agent just knows.

You also get autonomy. Think about the time teams spend explaining context—where data lives, why a job failed, what the definition of an active user is. With the dbt MCP server, AI can navigate your project independently. It understands dependencies, knows what models exist, how they relate, and how they’re defined. Engineers spend less time in documentation and more time building. With that context to your dbt assets, AI becomes a self-sufficient collaborator instead of something you have to babysit and validate.

You get consistency. When five people ask their AI tools about a revenue metric, you want them all to get the same answer. With MCP connecting to dbt, every agent—whether it’s in Claude, Cursor, or a custom workflow—references the same canonical definitions. This is even more powerful paired with something like the dbt Semantic Layer.

And you get safety. As we move toward more autonomous agents, you don’t want an AI assistant with unfettered access to your warehouse running arbitrary queries or modifying production models. The dbt MCP server gives governed guardrails so agents work within defined permissions—read-only where needed, action where appropriate—like granting API access instead of database credentials to prod.

How the dbt MCP Server Works: Four Use Cases

We consider the MCP server the way you connect everything you do with dbt to everything you do in an AI workflow. Many Snowflake users today use dbt to build, manage, and orchestrate high-quality data workflows on Snowflake. Once you have those assets, there are many things you can do with them. When we built the MCP server, we talked to teams to learn which AI workflows would be most relevant for speeding them up and accelerating value. We found four use cases: Discover, Consume, Develop, and Operate.

Discover: Find and Understand Project Assets

Use agentic AI systems to get a deeper understanding of what data assets exist in your project and weave them into AI workflows. Search is a great example. If you’ve been looking for a specific model or a granular piece of logic—like how marketing attribution is managed—simple keyword search may not get you what you need. Discover tools leverage LLM superpowers to understand things that sound similar. If you’re looking for “revenue” and it’s called “rev,” the model can contextually link this.

Tools include:

- Get all models: in a workflow where you might ask “Where do I define my revenue?” Claude goes and gets a list of all your models. This works well—even in moderately large dbt projects—because the model can perform a needle-in-a-haystack search across models to determine which ones to learn more about.

- Get model details: returns model details like source code, columns, and importantly, descriptions. The model performs data discovery, looks around your project, and starts navigating the data.

- Get model parents: navigates the DAG to find where logic is defined, how models are connected, and builds context on assets.

- Get column lineage: traces a given column through the dbt project. It’s useful in discovery and development—if a column is modified, you know what else is impacted.

Consume: Ask Questions and Query Data

This maps to talk-to-your-data or agentic data analyst workflows. Ask natural language questions like “What was my revenue last month?” or “How many users do I have in X location?” Anything the model needs to know that lives in your structured data, the consume tools attempt to query.

Two ways to interact:

- Semantic Layer: list metrics, get dimensions, and query metrics. If you ask “What was my quarterly revenue last year?” the model finds a revenue metric and breaks it out by time/quarter dimensions, then executes and returns results. Teams adopt semantic layers for questions needing utmost precision and accuracy.

- Execute SQL: rather than using the predefined semantic layer, the model writes a query itself. Discovery tools help list which models are needed and the underlying structures, then Execute SQL runs the query and returns metrics. A common pattern is multiple levels of trust: some agent workflows sit only on the semantic layer, while broader or more free-form analytics use Execute SQL tooling.

Develop: Build and Update dbt Projects with Agents

This is about writing and updating your dbt projects that sit on Snowflake. Over the past year in software engineering, we’ve seen a rise in co-pilot and agentic development experiences. Data teams are getting those same capabilities. The develop tools integrate dbt development into an agentic loop.

You could ask for a new model to be built—say, take existing revenue and build a breakout table on top of it by dimension, persisting it in your dbt project. Make the request, and with build, compile, list, run, show, and test tools, an agentic coding framework operates on your project.

You might ask: “I already have the dbt CLI enabled in my environment—what’s the benefit of layering MCP on top?” We found that even though you can run workflows just hitting the CLI, we see superior performance in development use cases when you layer MCP.

A particularly useful tool is Show. If you’ve ever built a dbt model, you know an important part of iteration is looking at your data. You make a transformation, write a model, and see what happens. Using Show, the model shows you what it has done. The loop is: you request a transformation, it edits the file, runs dbt build/test as needed to instantiate objects in the database, then runs dbt show to inspect whether the data matches the request. By giving the right tools at the right time, the model substantially improves how it assists you in developing dbt projects.

Operate: Orchestrate Jobs and Keep Data Healthy

It’s one thing to have correct data definitions in dbt and say “Here’s the DAG I want to instantiate in Snowflake.” It’s another to have it orchestrated, jobs running, failures surfaced, data up to date, accurate, and with no failing jobs. Operate tools are about operating on top of your dbt project and making it more efficient.

You can set up workflows to say: “For my past week’s dbt jobs, give me an overview of what happened and whether there were failures.” What’s going on with orchestration? You can get back job run artifacts—if a job fails, see what failed and why. This helps dynamic debugging workflows. You can string these into a self-remediation pipeline: after a job fails, extract errors, take them to develop tools, propose a fix. The four buckets feed into each other and enable dynamic AI workflows on your datasets.

Adoption and Agents

Since launching the dbt MCP server this year, over 400 companies are making more than 30,000 calls to the dbt MCP server every month, and that number is rising quickly. We anticipate this will become a primary skill set for the dbt developer, analytics engineer, and data engineer: how to build the right context into your dbt project and orchestrate tooling with MCP servers to operate on top of that data and hook into agentic workflows.

We’ve talked about the first set of tools available, and you can already string them into powerful workflows. Over time, expect longer time-horizon agentic workflows with more steps, higher-order goals, and more comprehensive tooling.

There are two ways to get involved with the dbt MCP server. You might want to build it yourself—custom agentic workflows, looping together multiple MCPs and clients to stitch dynamic data workflows. Or, if you want to get started out of the box with solutions targeted at best practices operating on dbt and Snowflake, you can use dbt Agents. We have four agents rolling out: analyst agent, discovery agent, observability agent, and developer agent. These map to the four use cases described earlier. Rather than hooking up your own workflows, we provide out-of-the-box solutions. Honestly, both are great, and if you’re interested in trying these out, we look forward to hearing from and working with you, and to increasing functionality of these agents and the tooling to build custom workflows.

Getting Started and Community

How do you get started with the dbt MCP server? The dbt MCP local server is open source and available on GitHub. You can read the dbt MCP server documentation on our documentation site. If you haven’t joined the dbt community, go to getdbt.com/community and join the dbt MCP server discussion group. It’s a vibrant channel where people are building the future of how AI workflows interact with data, and it’s exciting to see practitioners push the forefront of these workflows.

If you’re a dbt user on Snowflake—a pattern many teams are adopting—connect MCP to your project, pick one of the four use cases, and start playing around. You’ll likely be surprised by the amount of value you can get in a short time. Moving forward, there are open questions on productionizing for the long term and scaling to global workflows. This will take everyone in the industry pushing together. Thank you for joining, thank you for trying it out, and please get in touch as you try the MCP server. Let us know what’s working for you and how you’d like to build agentic workflows on top of dbt and Snowflake.