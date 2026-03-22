# Addon: ai

## v5 reference

`wex-5/addons/ai/`

## Commands

- [ ] `talk/ask` — ask a question to an LLM
- [ ] `talk/about_file` — analyze a file with an LLM

## Supporting pieces

- [ ] AI service configuration (model, API keys)
- [ ] `@ai_tool` decorator — mark Python functions as AI tools

## v5 dependencies

- `langchain`, `langchain-openai`, `langchain-cohere`
- `openai`
- `chromadb` (vector database)
- `langchain-postgres` (vector store)

## v6 target

- Dedicated `wex-addon-ai` package (to create)
- AI/LLM plumbing → evaluate reuse of `PACKAGES/PYTHON/packages/` or new package
