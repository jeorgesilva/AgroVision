import logging
import sys

_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(_formatter)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure the agrovision package logger. Call once from entry points."""
    root = logging.getLogger("agrovision")
    if not root.handlers:
        root.addHandler(_handler)
    root.setLevel(level)
    root.propagate = False
