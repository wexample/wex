# Contributing to this documentation

You are reading this file because you want to improve this documentation.

## General rules

- Write all documentation in English
- Keep information concise to save data and reader time
- Avoid multiline code examples when possible, use simple lists instead
- Start each file by explaining why the reader is reading it: "You are reading this file [because, if, when]..."
  Note that the reader is not the "user" (the person this documentation is about), but a third party tasked with performing actions for the user
- You can add and edit everything, fix typos and English language quality, remove non-relevant content, but in other
  hand you should respect the existing information as the documentation starts to be quite mature.

## Summary files

Each `_summary.md` file should contain a brief presentation followed by the directory structure files list. Followed by the **exact** directory content list (except `_summary.md` and `_entrypoint.md`) with a description placed in a "Directory registry" subtitle.

### About directory registries

Every time you change the directory structure bay adding, removing or changing file names, you should update the `_summary.md` file.

The `Directory registry` in summaries presents brief content descriptions to help users quickly find needed information.
- Use 📄 prefix before a file
- Use 📁 prefix before a directory

### Example

- 📄 filename.md: This is a brief file description
- 📁 dirname: This is a brief directory description

## Lists

- Use only markdown symbols (-, *) instead of ordered lists

## Directory registry

Like any other one, this is the registry of the current directory.

- 📄 exporting-skeleton.md: This file contains the instructions on how to create a new documentation, based on the structure of current one