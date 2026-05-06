import os
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
import streamlit as st

class SessionManager:
    """
    Manages processing sessions using Medallion Architecture logic.
    - Bronze: Raw inputs (orthomosaics).
    - Silver: Processed data (detections, intermediate rasters).
    - Gold: Final outputs (VRA maps, reports, shapefiles).
    """

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.sessions_dir = self.base_dir / "sessions"
        self._ensure_base_structure()

    def _ensure_base_structure(self):
        """Ensures the sessions directory exists."""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, prefix: str = "") -> dict:
        """
        Creates a new session directory structure.
        Returns a dictionary with session ID and paths.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"{timestamp}_{prefix}" if prefix else timestamp
        session_path = self.sessions_dir / session_id

        # Define medallion layers
        paths = {
            "root": session_path,
            "bronze": session_path / "bronze", # Raw Images
            "silver": session_path / "silver", # Detections, Metadata
            "gold": session_path / "gold",     # VRA Maps, Reports
            "logs": session_path / "logs"
        }

        # Create directories
        for p in paths.values():
            p.mkdir(parents=True, exist_ok=True)

        logging.info(f"Session created: {session_id}")

        return {
            "id": session_id,
            "paths": {k: str(v) for k, v in paths.items()}
        }

    def save_manifest(self, session_data: dict, metadata: dict = None):
        """Saves a JSON manifest with session details in the root session folder."""
        manifest_path = Path(session_data["paths"]["root"]) / "manifest.json"

        data = {
            "session_id": session_data["id"],
            "created_at": datetime.now().isoformat(),
            "paths": session_data["paths"],
            "metadata": metadata or {}
        }

        with open(manifest_path, "w") as f:
            json.dump(data, f, indent=4)

        logging.getLogger(__name__).info("Manifest saved to: %s", manifest_path)

    @staticmethod
    def clear_st_session():
        """Clears relevant Streamlit session state keys to reset the app state."""
        keys_to_clear = [
            "current_session",
            "last_uploaded_file",
            "current_ortho_path",
            "vra_path",
            "ortho_path",
            "shp_dir",
            "processed_data",
            "uploaded_file_buffer"
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
