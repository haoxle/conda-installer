# ✅ Miniconda Environment Installer – Project Checklist

## 🔧 1. Setup & Input Validation
- [x] Verify `miniconda.exe` path is valid and callable (do not assume it's in PATH)
- [x] Accept YAML file or directory of YAMLs as input (`--envdir`)
- [x] Validate that input files end with `.yaml` or `.yml`

## 📄 2. YAML Parsing & Safety
- [x] Parse YAML files safely using `pyyaml`
- [x] Ensure required keys exist: `name`, `dependencies`
- [x] Reject or ignore unsupported keys like `output`, `metadata`, etc.

## ⚙️ 3. Conda Environment Logic
- [x] If it exists → run: `conda env update -n <name> -f <file>`
- [x] If it doesn't exist → run: `conda env create -f <file>`

## 🗂️ 4. Multiple YAML Files
- [x] Support processing all `.yaml`/`.yml` files in a folder (`--envdir`)
- [x] Apply create/update logic to each file individually

## 🧪 5. Error Handling & Logging
- [x] Use `subprocess.run(..., check=True)` with `try/except` for errors
- [x] Catch and display readable errors (e.g. file not found, bad YAML, Conda error)
- [x] Print/log which environment is being processed and the result
- [x] Exit with a non-zero code if anything fails

## 🧼 6. User Experience
- [ ] Display progress for each environment creation/update
- [ ] Clean and readable CLI messages

## 🧩 7. Optional Features
- [ ] Load `.env` file to set `MINICONDA_EXE` path automatically
- [ ] Add terminal colors using `rich` (optional)
- [ ] Support custom output directory for Conda environments via CLI argument
