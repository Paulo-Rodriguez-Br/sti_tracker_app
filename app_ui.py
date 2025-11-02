from dataclasses import dataclass, field

import streamlit as st

from app_functions import AppFunctions


@dataclass
class AppUI:
    """High-level UI wrapper that wires navigation to app functions."""

    app_functions: AppFunctions = field(default_factory=AppFunctions)

    def __post_init__(self) -> None:
        """Initialize default routing state."""
        st.session_state.setdefault("route", {"page": "home"})

    @staticmethod
    def set_page(page: str) -> None:
        """Set the current page in session state."""
        st.session_state.setdefault("route", {})["page"] = page

    @staticmethod
    def get_page(default: str = "home") -> str:
        """Return the current page from session state (or a default)."""
        return st.session_state.setdefault("route", {}).get("page", default)

    def side_bar(self, onboarding: bool = False) -> None:
        """Render the sidebar navigation and handle page switching."""
        st.sidebar.title("🧭 Navigation")

        if onboarding:
            
            # Paulo Rodriguez - 30/10/2025
            # During onboarding, restrict navigation to Preferences
            st.sidebar.radio("Go to:", ["⚙️ Preferences"], index=0, key="sidebar_menu")
            self.set_page("preferences")
            
            return

        menu = {
            "🏠 Home": "home",
            "🧪 Register Test": "register",
            "📊 Test History": "history",
            "⚙️ Preferences": "preferences",
        }

        current_page = self.get_page()
        keys = list(menu.keys())
        values = list(menu.values())
        try:
            current_index = values.index(current_page)
        except ValueError:
            current_index = 0

        choice = st.sidebar.radio("Go to:", keys, index=current_index, key="sidebar_menu")
        chosen_page = menu[choice]

        if chosen_page != current_page:
            self.set_page(chosen_page)
            if chosen_page == "register":
                
                # Paulo Rodriguez - 31/10/2025
                # Reset the register wizard to step 1 when entering the flow
                
                st.session_state.setdefault("register", {})["step"] = 1
            st.rerun()

        st.sidebar.markdown("---")
        st.sidebar.caption("💾 App data stored locally")
        st.sidebar.caption("🔒 All data is private and not shared")

    def view_home(self) -> None:
        """Render the Home page with quick-action buttons."""
        st.title("🏠 Home")
        st.write("Welcome! Use the menu on the left.")

        c1, c2, c3 = st.columns(3)

        if c1.button("➕ New register", use_container_width=True):
            self.set_page("register")
            st.session_state.setdefault("register", {})["step"] = 1
            st.rerun()

        if c2.button("📜 History", use_container_width=True):
            self.set_page("history")
            st.rerun()

        if c3.button("⚙️ Preferences", use_container_width=True):
            self.set_page("preferences")
            st.rerun()

    def router(self, onboarding: bool = False) -> None:
        """Dispatch to the correct view based on current page and onboarding."""
        page = self.get_page()

        if onboarding and page != "preferences":
            self.set_page("preferences")
            self.app_functions.change_preferences()
            return

        if page == "home":
            self.view_home()
        elif page == "register":
            self.app_functions._ensure_register_state()
            self.app_functions.test_register()
        elif page == "history":
            self.app_functions.test_show()
        elif page == "preferences":
            self.app_functions.change_preferences()
        else:
            self.view_home()
