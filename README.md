# Raggamuffin

A fully private, local personal search engine for LLMs. Your data stays yours.

## What is this?

Raggamuffin is a local-first semantic search engine that indexes your documents, images, messages, and conversations—then exposes them to LLMs via MCP (Model Context Protocol).

No cloud. No telemetry. No rendering your personal data to oligarchs.

Works with **any** model, including local ones running on your machine.

## Why?

Because good search through everything on your machine shouldn't require handing your data over to someone else. This has been a long-held dream: REALLY GOOD and FULLY PRIVATE search.

## Tech Stack

- **FastAPI** + async MCP server
- **FastEmbed** for embeddings
- **SQLAlchemy** + **SQLite** for storage
- **Jinja2** for templating document context

## Requirements

- Python 3.12+
- A decent GPU, Apple MPS, or AI coprocessor (you don't need mountains of RAM)

## Status

Early development. Very rough data architecture phase. Vibes are being coded.

If you know what all this means and want to contribute, give me a poke.

## Roadmap

- [ ] Core document indexing pipeline
- [ ] Embedding generation with FastEmbed
- [ ] MCP server implementation
- [ ] Telegram integration
- [ ] System API integration (Mac Spotlight, metadata harvesting)

Like a spider in the web—connecting communities and conversations.

## Author

**Mathijs de Bruin** — mathijs@mathijsfietst.nl

Founder and inventor of [ipfs-search.com](https://ipfs-search.com), which I ran for 7 years. Raggamuffin is the spiritual successor: same dream of great search, but this time fully private and local.

## License

[AGPL-3.0](LICENSE)
