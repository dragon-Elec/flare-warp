## **Project Blueprint: `Flare WARP` and `pywarpcli` Library (Revision 5)**

### 1. Project Overview & Mission

**Mission:** To build a new GTK application by first creating a standalone, reusable Python library (`pywarpcli`) that provides a clean interface to the `warp-cli` tool. The project will follow a clean, multi-layered architecture to ensure maintainability and scalability.

**End State:**
1.  A Python package but in first  stages just py files, `pywarpcli`, that provides a clean, object-oriented API to `warp-cli`.
2.  A `workflows` layer that orchestrates reusable, multi-step `warp-cli` operations.
3.  A modular `app` layer containing the application's unique features and user interface.
4.  A minimal `main.py` entry point to launch the application.

### 2. Guiding Principles

*   **Clear Separation of Layers:** Each layer has a distinct responsibility and should not contain logic belonging to another. if there is somthing that can be used across between all py files and functions it can be placed in its appopriate place maybe in lib/pywarp or outside 
*   **Pragmatic Controller Pattern:** In `pywarpcli`, create controller files only for major, multi-command groups (e.g., `dns`, `registration`). Simple, standalone commands (e.g., `connect`, `status`) should be implemented as direct methods within the main `WarpClient` class withen explixity told commented area. 
*   **Structured `DualOutput` API:** Library functions will return a single `DualOutput` object (a generic dataclass). This object cleanly encapsulates both the structured data model (`.model`) and the raw CLI output (`.raw_output`), ensuring a readable, type-safe, and unambiguous API.
*   **Focus on Core Features (Phase 1):** Initial development will focus on essential features: connection, status, stats, and DNS family settings.
*   **Synchronous Library, Asynchronous GUI:** The `pywarpcli` library methods will be synchronous (blocking). The application layer is responsible for calling these methods in background threads to keep the UI responsive.
* **Modern Python Syntax:** The project will use modern Python (3.9+) conventions, including built-in generic types (`list[str]`, `dict[str, Any]`) for all type hints.
### 3. Phase 1: Core Library & Application Structure

#### 3.1. Final Project Structure

```
project_folder/
├── main.py                 # The single entry point to start the application.
│
├── app/                      # The Application Layer
│   ├── __init__.py
│   ├── features/           # For application-specific feature modules
│   │   ├── __init__.py
│   │   └── (e.g., wireshark_config.py, backup_manager.py, ...)
│   │
│   └── ui/                 # For modular UI components
│       ├── __init__.py
│       ├── main_window.py    # Code for the main window
│       ├── main_window.ui  # Layout for the main window
│       └── (e.g., settings_window.py, settings_window.ui, ...)
│
├── pywarpcli/              # Layer 1: The core library (Engine)
│   ├── __init__.py
│   ├── client.py           # The main engine: WarpClient class
│   ├── exceptions.py       # Custom exceptions for predictable error handling
│   ├── models.py           # Defines structured data objects (dataclasses)
│   ├── types.py            # Reusable API type definitions (e.g., DualOutput)
│   │
│   └── controllers/
│       ├── __init__.py
│       ├── base.py         # A simple BaseController for code reuse
│       └── dns.py          # Controller for 'warp-cli dns ...'
│
└── workflows/              # Layer 2: Multi-step business logic
    ├── __init__.py
    └── connection_workflows.py # Example for complex connection/setup sequences
```

#### 3.2. Component Breakdown: `pywarpcli` Library (The Engine)

*   **`exceptions.py`**: Defines custom errors (`WarpCLIError`, `CommandFailedError`).
*   **`models.py`**: Defines `dataclass` structures (`WarpStatus`, `WarpStats`).
*   **`client.py`**: The central `WarpClient` class.
    *   Contains the private `_run_command` engine.
    *   Initializes controllers for command groups (e.g., `self.dns = DnsController(self)`).
    *   Provides direct methods for simple commands (`connect()`, `disconnect()`, `get_status()`).
*   **`controllers/dns.py`**: `DnsController` class to handle `warp-cli dns` subcommands.
*  **`types.py`**: Defines reusable, high-level type structures for the library's API, such as the generic `DualOutput` container.

#### 3.3. Application & UI Development Plan

The application will be built with a clear separation between its unique features and its user interface components.

*   **Application Features (`app/features/`):** This package will contain the application's unique, high-level logic. Each distinct feature (e.g., configuring Wireshark, managing specific tunnel profiles) should be implemented in its own module within this directory. These modules will orchestrate calls to the `workflows` and `pywarpcli` layers to achieve their goals.
*   **User Interface (`app/ui/`):** This package will contain the presentation layer, built with GTK.
    *   **Modularity:** Each major UI component (like the main window, a settings dialog, etc.) should be self-contained with its own `.py` file for logic/handlers and a corresponding `.ui` file for layout.
    *   **Responsibility:** The Python code in this layer is responsible for handling user input (button clicks, text entry) and displaying data. It acts as the "view" and calls upon the "features" to perform the actual work.
*   **Entry Point (`main.py`):** A minimal script at the project root responsible for initializing and running the main application window from the `app/ui/` package.

### 4. The Workflows Layer

The `workflows/` directory contains **reusable, generic sequences** of `pywarpcli` calls.

*   **Purpose:** To abstract away common, multi-step `warp-cli` operations. A workflow should be generic enough that it could potentially be used by a different application. It knows nothing about the UI or specific application features.
*   **Distinction from Application Logic:** While a workflow is "logic," it is **generic and reusable**. The logic in `app/features/` is **specific and unique** to your application. A feature module will often *call* a workflow as one of its steps.

### 5. Phase 2 & Beyond: Future Expansion

This architecture is designed for growth. To add new `warp-cli` functionality (e.g., `registration`):
1.  Add a `RegistrationController` in `pywarpcli/controllers/`.
2.  Add any necessary data models to `pywarpcli/models.py`.
3.  Initialize the new controller in `pywarpcli/client.py`.

To add new application functionality (e.g., a "Secure Backup" feature):
1.  Create a new `secure_backup.py` module in `app/features/`.
2.  Implement the feature logic, using the library and workflows.
3.  Design and implement any required UI components in `app/ui/`.
4.  Connect the UI to the feature module.

**Future Challenges to Address:**
*   **Interactive Commands:** Implement a mechanism to handle commands that require user interaction (e.g., browser login), likely using `subprocess.Popen`.
*   **Privileged Commands:** Design a strategy for commands requiring root privileges, potentially using `pkexec` for a graphical sudo prompt.

### 6. Development Workflow (Step-by-Step for Phase 1)

1.  **Create File Structure:** Create all directories and empty `__init__.py` files as defined in the structure diagram.
2.  **Build `pywarpcli` Iteratively with Focused Testing:**
    >     *   For each new piece of functionality (e.g., status, dns commands), follow this loop:
    >         a. Implement the necessary library components (`models.py`, `client.py`, new controllers, etc.).
    >         b. Create a **temporary, dedicated test script** in the project root (e.g., `test_status.py`, `test_dns.py`). These scripts are for development only and will not be part of the final application.
    >         c. Use the script to call and verify the new library function from the command line.
    >     *   This ensures each part of the library is confirmed to work correctly before any UI code is written for it.

    *   Create a simple test script (`test_library.py`, not part of the final project) to verify all library functions work correctly before touching any UI code.
3.  **Build the Application Shell:**
    *   Create a basic `main_window.ui` and `main_window.py` in `app/ui/`.
    *   Write the `main.py` entry point to launch this empty window.
4.  **Implement Features & Connect UI:**
    *   Create initial modules in `app/features/` for core functionality.
    *   Wire the UI components in `main_window.py` to call the feature modules, using the required `threading.Thread` and `GLib.idle_add()` pattern.
5.  **Test:** Thoroughly test the integrated application.
