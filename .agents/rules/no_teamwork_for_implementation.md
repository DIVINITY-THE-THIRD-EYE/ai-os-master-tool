# Rule: No Teamwork or Subagents for File Implementation

## Constraint
Never use `teamwork_preview`, `invoke_subagent`, or any subagent delegation
for tasks that involve writing files, generating content, or implementing
a plan into a repository.

## When This Applies
- Generating markdown specification files
- Creating YAML configuration files
- Writing JSON schemas
- Building directory structures
- Implementing any plan that produces files on disk

## Required Behavior
Implement all files directly using `write_to_file` and `multi_replace_file_content`
tools in parallel batches. Use multiple simultaneous `write_to_file` calls
to maximize speed.

## Rationale
- teamwork_preview consumes large quota and causes RESOURCE_EXHAUSTED errors
- Direct writing is faster and more reliable for file generation tasks
- Subagent delegation adds latency and failure points for straightforward writes

## Exception
Teamwork or subagents may only be used when the task requires:
- Live web browsing
- Running terminal commands in a separate environment
- Tasks explicitly requested by the user to use teamwork
