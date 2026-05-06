# src/agrovision/interfaces/streamlit_app.py
import logging

from agrovision.utils.logging_config import setup_logging

_USAGE = (
    "To run the Streamlit app use one of:\n"
    "  streamlit run app/streamlit/Home.py\n"
    "  streamlit run app/streamlit/pages/Detection.py\n"
    "  streamlit run app/streamlit/pages/VRA.py"
)


def main():
    setup_logging()
    logging.getLogger(__name__).info(_USAGE)


if __name__ == "__main__":
    main()
