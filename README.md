# ⬡ Universal Orchestration & Synthesis Engine

The engine (Version 3.0.0) is a **Workspace-Native, Multi-Agent Capability & Persona Synthesis Engine**. It is designed to act as an "AI that builds AI" workspace environment, running inside your local IDE context. 

Instead of relying on heavy database backends, vector storage SaaS, or proprietary web interfaces, the engine operates entirely via the **File-System-as-a-UI** paradigm. By managing state, metadata, and memory directly in portable, atomic Markdown files, the system achieves maximum token efficiency, infinite portability, and zero corporate data leakage.

---

## 🛡️ Core Architectural Principles

1. **Workspace-Native & IDE-Driven**: All agent orchestration, capability building, and documentation happen inside your active IDE workspace. The AI uses local configuration rules to load instruction models dynamically.
2. **Atomic Markdown Flat-File RAG**: Avoids heavy, slow vector databases. Threat manuals, configurations, and inventory schemas are broken down into tiny, targeted `.md` files. High-performance queries are run using local terminal utilities (like `ripgrep` or script wrappers).
3. **Obsidian Dependency Graph**: Connections between skills, personas, and scripts are kept in lightweight files containing bidirectional wiki links (`[[Dependency_Name]]`). The analyst can open the `/connections/` folder in [Obsidian](https://obsidian.md/) to visualize the evolving workspace knowledge graph.
4. **Token Conservation & JIT Ingestion**: Large files (>500 lines) are never read raw. Instead, local Python abstractions slice and filter logs, databases, and schemas before feeding them to the active context window.

---

## 📂 Directory Layout

```text
.
├── META_PROMPT.md                  # Master System Directive (Source of Truth)
├── manifest.json                   # Token Gatekeeper: Taxonomy & capability index
├── requirements.txt                # Programmatic package dependencies
│
├── /connections/                   # Obsidian Graph: Wiki-link dependency nodes
├── /ideation/                      # Drop Zone: Raw PDFs, HTML, logs, scratchpads
├── /imported_skills/               # Staging: Raw community tools awaiting refinement
│
├── /skills/                        # Compiled capabilities (Markdown packages)
│   ├── /generic/                   # Open Source: Clean, sanitized, environment-agnostic
│   └── /private/                   # Corporate: Specific infrastructure/regional configurations
│
├── /perimeter_knowledge/           # Flat-File RAG Vault
│   ├── /imported/                  # Ground Truth: Static lists (asset registers, manuals)
│   └── /ai_generated/              # Deductive Memory: AI-learned naming heuristics
│
├── /personas/                      # CrewAI / LangGraph orchestration deployment layer
└── /scripts/                       # Local Python utilities (e.g. search_vault.py)
```

---

## 🛠️ Requirements & Toolchain

All capabilities and personas are compiled and validated using the libraries declared in `requirements.txt`:
* **Data Ingestion**: `docling` translates PDFs, logs, and manuals in `/ideation/` into clean Markdown.
* **Orchestration**: `crewai`, `langgraph`, and `langchain-core` define multi-agent schemas, memories, and routing logic inside `/personas/`.
* **Security Context**: `pyattck` queries MITRE ATT&CK techniques, `nvdlib` checks CVE metrics, and `stix2` processes standardized threat intel packages.
* **Detection Translation**: `pysigma` and `sigma-cli` translate Sigma log rules into queries (e.g., Splunk, Sentinel KQL, XQL).
* **Syntax Validation**: `tree-sitter` and `tree-sitter-python` perform AST validation checks on synthesized Python scripts before completion.
* **Configuration**: `python-dotenv` manages API keys and targets securely.

---

## 🚀 Quick Setup Guide

To bootstrap the engine in your preferred IDE chat assistant:

### 1. Install Dependencies
Run the standard installation command to configure your local toolchain:
```bash
pip install -r requirements.txt
```

### 2. Configure Your IDE Pointer
The assistant is directed to fetch and apply the root `META_PROMPT.md` using the corresponding IDE rules file:
* **Antigravity**: Matches `.antigravityrules` or `.geminirules`
* **VS Code (Copilot / Cline / Roo Code)**: Matches [.github/copilot-instructions.md](.github/copilot-instructions.md) and [.clinerules](.clinerules)
* **Cursor**: Matches [.cursorrules](.cursorrules)
* **Windsurf**: Create a `.windsurfrules` file with:
  ```text
  Instruction: Read and apply META_PROMPT.md
  ```

Once opened, the AI assistant will automatically read `META_PROMPT.md` first, adopt the Canary Status protocol (`[◈ Console Active | Status: Optimized & Connected]`), and follow all data sanitization, directory structure, and validation rules.

---

## 🔄 Development Workflow (How to Compile Skills & Personas)

Follow this lifecycle to build and deploy capabilities dynamically:

1. **Staging / Drop Zone**:
   * For raw brainstorms, vendor PDFs, or logs: Save them in the `/ideation/` folder.
   * For existing community repositories or external scripts: Clone or extract them into `/imported_skills/`.
2. **Trigger Compilation**:
   * Open your IDE chat assistant and command it: 
     > *"Compile the [skill_name] from /imported_skills/ into a generic capability."*
3. **Automatic Synthesis & Optimization**:
   * The engine reads the staged assets and strips unnecessary boilerplate.
   * Compiles the target capability directory inside `/skills/generic/` or `/skills/private/` matching the **Skill Compilation Standard**.
   * Creates the Obsidian graph note in `/connections/` using the Connection Protocol.
   * Registers the new capability in `manifest.json`.
4. **Deployment**:
   * Ask the assistant to generate a multi-agent routing persona in `/personas/` (e.g., using `crewai` or `langgraph`) that loads and executes the compiled capability.
