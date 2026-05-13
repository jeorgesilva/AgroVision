import logging
import subprocess
import sys
from pathlib import Path

from agrovision.utils.logging_config import setup_logging

# All Streamlit pages now live next to this file inside the package.
# Path(__file__).resolve().parent always points to the interfaces/ directory
# regardless of the working directory when the process is launched.
_HERE = Path(__file__).resolve().parent
_HOME_PAGE = _HERE / "Home.py"


def main() -> None:
    setup_logging()
    log = logging.getLogger(__name__)
    log.info("Launching Streamlit app: %s", _HOME_PAGE)
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(_HOME_PAGE)],
        check=True,
    )


if __name__ == "__main__":
    main()
