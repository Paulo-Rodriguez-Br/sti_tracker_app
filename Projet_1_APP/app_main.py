import streamlit as st

from app_ui import AppUI


def main() -> None:
    """Initialize the app, handle onboarding, and dispatch to the UI router."""
    st.set_page_config(page_title="STI Tracker", layout="wide")

    ui = AppUI()

    prefs = ui.app_functions.preferences
    prefs.load_preferences()
    onboarding: bool = not prefs.is_configured()

    if onboarding:
        ui.set_page("preferences")
        st.session_state["_pref_first_time"] = True

    ui.side_bar(onboarding=onboarding)
    ui.router(onboarding=onboarding)
    
    # Paulo Rodriguez - 30/10/2025
    # Show a one-time helper message the first time the Preferences page is opened
    if ui.get_page() == "preferences" and st.session_state.pop("_pref_first_time", False):
        st.info("👋 First time here: configure your preferences to get started.")


if __name__ == "__main__":
    main()