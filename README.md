# Archivator

A project-based storage and trash management tool designed for VFX pipelines.

Archivator provides a structured way to manage multiple projects, each with its own storage and dedicated trash system — enabling safe deletion, recovery, and future automation of cleanup workflows.

---

## Overview

Archivator acts as a **centralized storage manager** where each project is defined by:

- A **Project Root** (active working directory)
- A **Trash Directory** (safe deletion zone)

Instead of permanently deleting files, tools can move them to a project-specific trash folder, allowing recovery and controlled cleanup.

---

## Features

- Manage multiple projects
- Per-project trash directories
- Add, edit, and remove projects
- Search projects by name
- Custom project thumbnails
- Open project or trash in file explorer
- Empty trash safely per project
- Basic CLI support (work in progress)

---

## Screenshots

### Project Browser
<img width="895" height="616" alt="image" src="https://github.com/user-attachments/assets/0744dbd5-6474-4051-90ef-9298b24bd8ae" />


### Project Settings
<img width="894" height="618" alt="image" src="https://github.com/user-attachments/assets/356cb7c2-7ba7-4475-bcdc-fe1fe6ac8d39" />

---

## Example Integration

Archivator is designed to integrate with production tools.

A reference implementation is available via the Prism plugin:

👉 https://github.com/ClaireBenes/PrismPlugin-TrashManager

This plugin demonstrates how Archivator can be used as a backend to:
- Redirect file deletion to a safe trash system
- Restore deleted files
- Provide direct access to project trash from within a DCC pipeline

---

## Roadmap

Planned improvements include:

### Packaging
- Distribute Archivator as a pip-installable package
- Remove need for local path dependencies in integrations

### Automated Cleanup System
- Detect unused or unreferenced files
- Move candidates to trash safely
- Configurable rules:
  - Target directories
  - Time-based thresholds
  - Dependency validation

### Pipeline Intelligence
- Non-destructive cleanup workflows
- Smarter file analysis to prevent breaking projects

---

## Technical Details

- Python 3.11
- PySide6 (Qt-based UI)
- Windows (currently supported platform)

---

## Installation (Current)

Archivator is not yet packaged.

Clone the repository and run locally:

```bash
git clone https://github.com/ClaireBenes/Archivator
