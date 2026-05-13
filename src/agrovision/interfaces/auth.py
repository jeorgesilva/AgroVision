import hmac
import logging
import sys
from pathlib import Path

import streamlit as st

# Make the agrovision package importable from the Streamlit context
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_SRC_DIR = _PROJECT_ROOT / "src"
try:
    import agrovision  # noqa: F401
except ImportError:
    if _SRC_DIR.is_dir():
        sys.path.insert(0, str(_SRC_DIR))

from agrovision.utils.logging_config import setup_logging

setup_logging()
_log = logging.getLogger("agrovision.auth")


def require_login() -> None:
    """Gate the current page behind a username/password form.

    Credentials must be set in `.streamlit/secrets.toml`:

        [auth]
        username = "admin"
        password = "change_me"

    Calls st.stop() when the user is not authenticated, so any code placed
    after this call is only reachable by authenticated users.
    """
    if st.session_state.get("_authenticated"):
        return

    st.set_page_config(page_title="AgroVision — Login", page_icon="🔐", layout="centered")

    st.title("🔐 AgroVision — Login")
    st.caption("Insira as suas credenciais para aceder à plataforma.")

    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", use_container_width=True)

    if submitted:
        try:
            valid_user = hmac.compare_digest(username, st.secrets["auth"]["username"])
            valid_pass = hmac.compare_digest(password, st.secrets["auth"]["password"])
        except KeyError:
            st.error(
                "Configuração de autenticação não encontrada. "
                "Verifique o ficheiro `.streamlit/secrets.toml`."
            )
            _log.error("secrets.toml missing or [auth] section not found")
            st.stop()

        if valid_user and valid_pass:
            st.session_state["_authenticated"] = True
            _log.info("User '%s' authenticated successfully", username)
            st.rerun()
        else:
            _log.warning("Failed login attempt for user '%s'", username)
            st.error("Usuário ou senha incorretos.")

    st.stop()
