# src/agrovision/interfaces/streamlit_app.py

def main():
    """
    This is the main entry point for the Streamlit application.
    You can run this file to start the Streamlit server.
    
    Example:
        $ streamlit run src/agrovision/interfaces/streamlit_app.py
    """
    # This is a placeholder. In a real application, you might have a multipage setup here
    # or some other logic to select which page to show.
    # For now, we will rely on the user to run the individual pages from the `app/streamlit` directory.
    print("To run the Streamlit app, please run one of the following commands:")
    print("streamlit run app/streamlit/Home.py")
    print("streamlit run app/streamlit/Detection.py")
    print("streamlit run app/streamlit/VRA.py")


if __name__ == "__main__":
    main()
