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
## Data & Architecture

Archivator relies on a lightweight, filesystem-based approach for managing data and state.

### Persistence

The system maintains a persistent state through two main mechanisms:

- **Project Registry (JSON)**  
  A central configuration file stores all registered projects, including their root paths, trash directories, and metadata.

- **Per-File Metadata (.archivator.json)**  
  When files are moved to trash, associated metadata files are created to store:
  - Original file path
  - Deletion date
  - Grouping information (for related files)

This approach keeps the system simple, transparent, and easy to inspect or modify without requiring a database.

---

### Execution Model

Archivator currently operates in an **on-demand mode**:

- Actions such as *move to trash* and *restore* are executed immediately
- No background processing or job queue is implemented yet

This design keeps the tool lightweight while allowing future extension toward more advanced workflows.

---

### Configuration Granularity (Planned)

Configuration is currently defined at the **project level**, but the system is designed to support more granular rules in the future.

Planned extensions include:

- Rules based on **file types** (e.g. `.exr`, `.ma`, `.abc`)
- Context-aware behavior (e.g. render vs compositing outputs)
- Department-specific configurations

Example use case:
- Limit the number of stored versions for heavy render outputs (EXR)
- Keep more history for lighter or critical files

---

### Future Architecture

Archivator is currently a **local application**, but a client/server architecture is being considered for future development.

This would enable:

- Centralized file analysis and cleanup
- Background processing (scheduler-based tasks)
- Better permission and access management
- Integration via APIs (e.g. REST) with external tools such as Prism

This evolution would allow Archivator to scale from a local tool to a more production-ready pipeline service.

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
