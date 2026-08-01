# Install Token Economy Framework

Token Economy is a framework of tools, skills, and operating rules that a project uses to optimize token consumption. The framework is **scaffolding** — the project that uses it (whatever you build, write, or work on) is **not part of Token Economy**.

Project-local install (in an existing project that already contains the framework files):

```bash
./INSTALL.sh
```

Dry run:

```bash
./INSTALL.sh --dry-run
```

The installer links the active skills into repo-local host directories, refreshes
the resident catalogs, and runs repo-local skill helpers. Verify the result with:

```bash
./te doctor
./te hooks doctor
./te wiki index
```

## Fresh Checkout

Clone into a new directory, then install. The installer never clears the current
directory and does not write user-global configuration by default.

```bash
git clone https://github.com/SaarShai/token-economy.git token-economy
cd token-economy
./INSTALL.sh --dry-run
./INSTALL.sh
./te doctor && ./te hooks doctor && ./te wiki lint --strict --fail-on-error
```

Optional global integrations must be requested explicitly:

```bash
./INSTALL.sh --graphify
./INSTALL.sh --global-claude-hooks
```
