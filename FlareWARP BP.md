## **Project Blueprint: `Flare WARP` and `pywarpcli` Library (Revision 6)**

### 1. Project Overview & Mission

**Mission:** To build a new GTK application by first creating a standalone, reusable Python library (`pywarpcli`) that provides a clean interface to the `warp-cli` tool. The project will follow a clean, multi-layered architecture to ensure maintainability and scalability.

**End State:**
1.  **[COMPLETED]** A Python package `pywarpcli` that provides a clean, object-oriented API to `warp-cli`.
2.  **[COMPLETED]** A `workflows` layer that orchestrates reusable, multi-step `warp-cli` operations.
3.  A modular `app` layer containing the application's unique features and user interface.
4.  A minimal `main.py` entry point to launch the application.

### 2. Guiding Principles

*   **Clear Separation of Layers:** Each layer has a distinct responsibility.
*   **Pragmatic Controller Pattern:** Controllers are used for major command groups (`dns`, `registration`, `mode`, `settings`). Simple commands (`connect`, `status`) are direct methods in `WarpClient`.
*   **Structured `DualOutput` API:** Library functions return a `DualOutput` object containing both a structured model and the raw output.
*   **JSON-First Approach:** The library forces `warp-cli --json` for all commands to ensure robust, machine-readable output parsing.
*   **Synchronous Library, Asynchronous GUI:** Library methods are synchronous. The app layer handles threading.

### 3. Phase 1: Core Library (Completed)

The `pywarpcli` library is now feature-complete for the intended UI scope.
> **Note:** The library is **not yet a full 1:1 mirror** of the official `warp-cli`. Some administrative and setup commands (e.g., `registration new`, `tunnel endpoint`) are currently deferred.

#### 3.1. Implemented Features
*   **Core Client (`client.py`):**
    *   `connect()`, `disconnect()`
    *   `get_status()`, `get_stats()`
*   **DNS Controller (`controllers/dns.py`):**
    *   `get_stats()`
    *   `set_families(mode)` (off, malware, full)
*   **Registration Controller (`controllers/registration.py`):**
    *   `show()`
    *   `get_devices()`
    *   `get_organization()`
*   **Mode Controller (`controllers/mode.py`):**
    *   `set_mode(mode)` (warp, doh, etc.)
*   **Settings Controller (`controllers/settings.py`):**
    *   `get_list()` (Parses JSON settings)

#### 3.2. Project Structure
```
project_folder/
├── main.py                 # Entry point (Pending)
├── app/                    # Application Layer (Pending)
│   ├── features/
│   └── ui/
├── pywarpcli/              # Core Library (Done)
│   ├── client.py
│   ├── exceptions.py
│   ├── models.py
│   ├── types.py
│   └── controllers/
│       ├── base.py
│       ├── dns.py
│       ├── registration.py
│       ├── mode.py
│       └── settings.py
└── workflows/              # Workflows (Done)
    ├── connection_workflows.py
    └── registration_workflows.py
```

### 4. Phase 2: Application & UI Development (Next Steps)

The application will be built with GTK4/Libadwaita.

*   **User Interface (`app/ui/`):**
    *   **Simple Mode:** A compact window with a big toggle button and mode selector (WARP vs DNS-only).
    *   **Advanced Mode:** An expanded view showing detailed stats, logs, and settings.
*   **Application Features (`app/features/`):**
    *   Logic to bridge the UI events to the `pywarpcli` library.

### 5. Future Expansion & Deferred Items

*   **Setup / Admin Commands:**
    *   `registration new` (Register new client)
    *   `registration delete` (Unregister)
    *   `registration license` (Add license key)
    *   `account` (Zero Trust login)
*   **Interactive Commands:** Handling browser logins or TOS prompts.
*   **Privileged Commands:** Handling root-only commands (e.g., `tunnel endpoint`).

### 6. Development Workflow

1.  **[DONE] Build `pywarpcli`:** Library is implemented and verified with test scripts.
2.  **Build the Application Shell:**
    *   Create `main_window.ui` and `main_window.py`.
    *   Implement "Simple Mode" first.
3.  **Implement Features & Connect UI:**
    *   Wire the UI to the library.
4.  **Test:** Verify the full application flow.
