# Archivator – Architecture Overview

## 📌 Goal
Archivator is a standalone, software-agnostic archiving system designed to manage project-based file deletion, recovery, and automated cleanup. It integrates with external tools (e.g., DCCs like Prism) through a simple API, without embedding any software-specific logic.

---

# 🧱 Project Structure Overview
```
archivator/
│
├── core/
├── services/
├── cli/
├── ui/
└── config/
```
---

# 🧠 CORE LAYER (Pure Logic)

The **core** contains all fundamental logic. It is independent from UI, CLI, or external software.

---

## `models.py`

### `Project`
Represents a single project configuration.

**Responsibilities:**
- Store project metadata (id, name, root path, trash directory)
- Store collection settings and scan paths
- Provide helper methods (e.g., checking if a file belongs to the project)

---

## `registry.py`

### `ProjectRegistry`
Manages all project configurations stored in `projects.json`.

**Responsibilities:**
- Load and save project data
- Add, remove, and update projects
- Ensure data validity (unique trash directories, valid paths)
- Provide access to all registered projects

---

## `resolver.py`

### `ProjectResolver`
Determines which project a given file belongs to.

**Responsibilities:**
- Take a file path as input
- Match it against known project roots
- Return the corresponding `Project` object

---

## `trash_manager.py`

### `TrashManager`
Handles all file deletion and recovery operations.

**Responsibilities:**
- Move files to the correct project trash directory
- Preserve original folder structure inside trash
- Restore files to their original location
- Empty a project's trash safely

---

## `collector.py`

### `Collector`
Implements automated cleanup logic.

**Responsibilities:**
- Scan project directories
- Apply cleanup rules (e.g., file age, type)
- Move eligible files to trash

---

## `exceptions.py`

### Custom Exceptions

**Examples:**
- `ProjectNotFoundError`
- `InvalidProjectError`

**Purpose:**
- Provide clear and structured error handling

---

# 🚀 SERVICE LAYER (Orchestration)

The **services** layer acts as the main entry point for external systems (CLI, UI, plugins).

---

## `archive_service.py`

### `ArchiveService`
High-level interface for all archive operations.

**Responsibilities:**
- Move files to trash (resolving project automatically)
- Restore files
- Empty trash
- Add and list projects

**Note:**
This is the primary API used by external tools like Prism.

---

## `scheduler_service.py`

### `SchedulerService`
Manages automated background tasks.

**Responsibilities:**
- Read project collection settings
- Schedule periodic cleanup jobs
- Execute collector tasks at defined intervals

---

# 💻 CLI LAYER

## `cli/main.py`

### CLI Entry Point

**Responsibilities:**
- Provide command-line access to Archivator
- Parse user commands
- Call `ArchiveService` methods

**Examples:**
- Add project
- Move file to trash
- Restore file
- Start background scheduler

---

# 🖥️ UI LAYER

## `ui/app.py`

### `ArchivatorApp`
Main graphical application.

**Responsibilities:**
- Display project list
- Allow editing project settings
- Trigger archive operations via `ArchiveService`

---

## `ui/views/`

### UI Components

**Responsibilities:**
- Define visual elements (project grid, settings panels, etc.)
- Handle user interaction

---

# ⚙️ CONFIGURATION

## `config/projects.json`

### Project Database

**Purpose:**
- Store all project configurations

**Contains:**
- Project metadata (id, name, root)
- Trash directory
- Collection settings
- Paths to scan

---

# 🧭 Design Principles

- **Software-agnostic:** No dependency on external tools (Prism, ShotGrid, etc.)
- **Path-driven:** File paths determine project context automatically
- **Single source of truth:** All project data stored in one registry file
- **Separation of concerns:** Clear distinction between logic, orchestration, and interface
- **Extensible:** Easy to add new features (rules, UI, integrations)

---

# 🔌 Integration Philosophy

External tools (e.g., Prism) interact with Archivator by simply calling:


Archivator handles:
- Project detection
- Trash routing
- File operations

No external system needs to manage project configuration.

---

# ✅ Summary

Archivator is designed as a modular, maintainable system where:
- The **core** handles logic
- The **services** expose functionality
- The **interfaces (CLI/UI)** provide access
- External tools remain lightweight and decoupled

This architecture ensures scalability, flexibility, and ease of integration in production pipelines.

# 🧩 Architecture Diagram
<img width="501" height="521" alt="Archivator" src="https://github.com/user-attachments/assets/c2c652d1-133e-4c7a-857a-2351737719be" />
