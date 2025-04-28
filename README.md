# Reproduce Pydantic AI Issue #1292

Simple reproduction of a Pydantic AI issue related to prematurely stopping streaming linked [here](https://github.com/pydantic/pydantic-ai/issues/1292).

In my use case, I was using bedrock + claude 3.7 sonnet. But it appears as though other models are facing the same issue.

Python requirements:

If using `uv`, simply run:

```bash
uv sync
```

Otherwise, the pip requirements are:

```pip-requirements
pydantic-ai==0.1.6
```

## Running

```bash
# Note that not_working.py doesn't stream the text after the tool call
uv run python not_working.py

# Note that working.py streams the text after the tool call
uv run python working.py
```

`working.py` is a work-around that worked for me, but might not fit all use cases.
