# COE-Encora AIVA AppGov

AIVA AppGov is a Python-based project for document ingestion and processing, developed as part of the COE-Encora AIVA initiative. This repository contains scripts and supporting directories to extract, ingest, and process data into structured outputs for downstream use.

## Contents

- `main.py` — Primary entry point for running the application.
- `ingest.py` — Data ingestion and preprocessing utilities.
- `src/` — Source code and helper modules.
- `data/` — Input datasets and raw documents (not tracked if large).
- `db/` — Local database or storage used by ingestion (e.g., vector store).
- `output/` — Generated outputs, reports, and processed artifacts.
- `requirements.txt` — Python dependencies.

## Requirements\n
- Python 3.8+
- pip

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.\venv\Scripts\activate  # Windows
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Quick Start

1. Ensure dependencies are installed as shown above.
2. Prepare your input files under the `data/` directory.
3. Run the ingestion step to populate local storage: 

```bash
python ingest.py
```

4. Run the main application:

```bash
python main.py
```

Notes: The exact CLI arguments (if any) for `ingest.py` and `main.py` are defined in their respective files — check the top of each script or run them with `-h`/`--help` to see available options.

## Project Structure

This repository follows a simple layout to separate concerns: ingestion, processing, and outputs. Keep raw and large datasets out of version control; use `data/` as a working folder and add any large files to `.gitignore`.

## Development

- Use the `src/` directory for reusable modules and unit tests.
- Add new dependencies to `requirements.txt`.
- Open an issue or pull request for changes.

## Contributing

Contributions are welcome. Please: 
- Fork the repository
- Create a feature branch
- Submit a pull request with a clear description of changes

## License

No license is specified in this repository. If you plan to share this project publicly, consider adding an appropriate LICENSE file (for example, MIT, Apache-2.0, etc.).

## Contact

For questions or help, contact the repository owner: prasunsamir-encora.
