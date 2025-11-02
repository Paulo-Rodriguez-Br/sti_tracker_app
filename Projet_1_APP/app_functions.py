from dataclasses import dataclass, field

import pandas as pd
import streamlit as st

from Config_App import (
    common_results,
    profile_tags_full_list,
    sti_result_options,
    sti_test_types,
    stis_full_list,
)
from ScreeningLoader import ScreeningLoader
from UserPreferences import UserPreferences

REGISTER_FORM_TITLE = "### Register STI form"


@dataclass
class AppFunctions:
    """Streamlit-facing application functions: preference management and STI register workflow."""
    
    preferences: UserPreferences = field(default_factory=UserPreferences)
    screening: ScreeningLoader = field(default_factory=ScreeningLoader)
    
    @staticmethod
    def go_step(n: int, state_bloc: str) -> None:
        """Set the current step in a session-state block."""
        bloc = st.session_state.setdefault(state_bloc, {})
        
       # Paulo Rodriguez 02/11/2025 - We dont have self on static methods
       # so we save the logger reference in the session state
       # LOG: record step change 
        try:
            logger = st.session_state.get("_app_logger")
        except Exception:
            logger = None
        prev = bloc.get("step")
        bloc["step"] = n
        if logger:
            logger.debug("go_step: block=%s, from=%s, to=%s", state_bloc, prev, n)
    
    def test_register(self) -> None:
        """Render and manage the multi-step STI new test register."""
        AppFunctions._ensure_register_state()
        register = st.session_state["register"]
        
        # Paulo Rodriguez - 30/10/2025     
        # The test register form will only show the STIs the user wants to track
        # so it's essential to load his preferences here
        
        if not getattr(self.preferences, "_loaded", False):
            self.preferences.load_preferences()
        
        self.preferences.logger.debug(
            "test_register: loaded preferences (tracked_stis=%s, reminder=%s, tags=%s)",
            self.preferences.tracked_stis, self.preferences.reminder_hour, self.preferences.profile_tags
        )
        
        # Paulo Rodriguez 02/11/2025 - We dont have self on static methods
        # keep a handle to logger in session for static method logging as well
        st.session_state["_app_logger"] = self.preferences.logger
        
        if st.session_state["register"]["step"] == 1:
            
            with st.form("register_step_1", clear_on_submit=True):
                
                st.write(REGISTER_FORM_TITLE)
                     
                date_in = st.date_input("Test date")
                c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 2])                 
                next_clicked = c3.form_submit_button("Next")
                
                if next_clicked:
                    
                    register["date"] = date_in

                    self.preferences.logger.info("Register step 1 → 2: date set to %s", date_in)
                    AppFunctions.go_step(2, "register")
                       
        elif st.session_state["register"]["step"] == 2:
            
            with st.form("register_step_2", clear_on_submit=False):
                
                st.write(REGISTER_FORM_TITLE)
                st.write("Tested STIs")
                
                tested_stis = [option for option in self.preferences.tracked_stis 
                               if st.checkbox(option, key=f"reg_step2_cb_{option}")]
                
                c1, c2, c3, c4, c5 = st.columns([2, 1, 0.2, 1, 2])

                with c2:
                    back_clicked = st.form_submit_button("Back")
                
                with c4:
                    next_clicked = st.form_submit_button("Next")
                        
            if next_clicked:
                register["tested_stis"] = tested_stis
       
                self.preferences.logger.info(
                    "Register step 2 → 3: %d STI(s) selected: %s",
                    len(tested_stis), tested_stis
                )
                AppFunctions.go_step(3, "register")
                
            if back_clicked:

                self.preferences.logger.debug("Register step 2 → 1 (back)")
                AppFunctions.go_step(1, "register")
        
        
        elif st.session_state["register"]["step"] == 3:
            
            with st.form("register_step_3", clear_on_submit=False):
                
                st.write(REGISTER_FORM_TITLE)
                st.write("Test type and result for each selected STI")
                
                sti_realised_tests = {}
                results = {}
                
                for sti in register["tested_stis"]:
                    
                    test_options = sti_test_types.get(sti, ["Other / Don’t know"])
                    prev_test = register["sti_realised_tests"].get(sti)
                    test_index = test_options.index(prev_test) if prev_test in test_options else 0
                    
                    test_choices = st.selectbox(
                        label=f"{sti} – test type",
                        options=test_options,
                        index=test_index,
                        key=f"test_type_{sti}"
                        )
                    
                    sti_realised_tests[sti] = test_choices
                    
                    res_options = sti_result_options.get(sti, common_results)
                    prev_res = register["sti_results"].get(sti)
                    res_index = res_options.index(prev_res) if prev_res in res_options else 0   
                    
                    result_options = st.selectbox(
                        label=f"{sti} – result",
                        options=res_options,
                        index=res_index,
                        key=f"test_res_{sti}"
                        )
                    
                    results[sti] = result_options
            
                c1, c2, c3, c4, c5 = st.columns([2, 1, 0.2, 1, 2])

                with c2:
                    back_clicked = st.form_submit_button("Back")
                
                with c4:
                    next_clicked = st.form_submit_button("Next")
    
            if next_clicked:
                register["sti_realised_tests"] = sti_realised_tests
                register["sti_results"] = results

                self.preferences.logger.info(
                    "Register step 3 → 4: tests=%s | results=%s",
                    sti_realised_tests, results
                )
                AppFunctions.go_step(4, "register")
        
            if back_clicked:

                self.preferences.logger.debug("Register step 3 → 2 (back)")
                AppFunctions.go_step(2, "register")
                
        elif st.session_state["register"]["step"] == 4:
            
            register = st.session_state.setdefault("register", {})
            register.setdefault("test_location", "")
            register.setdefault("notes", "")
            
            with st.form("register_step_4", clear_on_submit=True):
                
                st.write(REGISTER_FORM_TITLE)
                
                test_location = st.text_input(
                    "Laboratory", 
                    placeholder="Enter test location or leave empty",
                    value=register["test_location"],
                    key="step4_location",
                    )
                
                notes = st.text_area(
                    "Observations",
                    placeholder="Enter any relevant notes...",
                    value=register["notes"],
                    key="step4_notes",
                    )
                            
                c1, c2, c3, c4, c5 = st.columns([2, 1, 0.2, 2, 2])

                with c2:
                    back_clicked = st.form_submit_button("Back")
                
                with c4:
                    finish_clicked = st.form_submit_button("Finish register")
            
            if back_clicked:
                register["test_location"] = test_location
                register["notes"] = notes

                self.preferences.logger.debug(
                    "Register step 4 → 3 (back): location=%s, notes_len=%d",
                    test_location, len(notes or "")
                )
                AppFunctions.go_step(3, "register")
            
            if finish_clicked:
                
                register["test_location"] = test_location
                register["notes"] = notes
                rows = self.screening.register_to_rows(register)

                self.preferences.logger.info(
                    "Register step 4 → finish: appending %d row(s) (location=%s, notes_len=%d)",
                    len(rows), test_location, len(notes or "")
                )
                self.screening.append_register(rows)
                AppFunctions.go_step(5, "register")
        
        elif st.session_state["register"]["step"] == 5:
            
            st.success("Register completed! ✅")
            st.caption("Choose what you want to do next:")
            
            left, mid1, mid2, right = st.columns([2, 1, 1, 2])
            with mid1:
                add_clicked = st.button("➕ Add another register", use_container_width=True)
            with mid2:
                home_clicked = st.button("🏠 Go to Home", use_container_width=True)
        
            if add_clicked:
                self.preferences.logger.info("Register finished: user chose to add another register")
                AppFunctions._reset_register_flow()
                st.rerun()
        
            if home_clicked:
                self.preferences.logger.info("Register finished: user returned to Home")
                AppFunctions.go_step(6, "register")
                st.rerun()
    
    @staticmethod
    def _ensure_register_state() -> None:
        """Ensure that the `register` dictionary contains all required keys."""
        reg = st.session_state.get("register")
        required = {
            "step", "date", "tested_stis", "sti_realised_tests",
            "sti_results", "test_location", "notes"
        }
        if not isinstance(reg, dict) or not required.issubset(reg.keys()):
            try:
                logger = st.session_state.get("_app_logger")
                if logger:
                    logger.warning(
                        "_ensure_register_state: invalid or incomplete register, resetting. got_keys=%s required=%s",
                        set(reg.keys()) if isinstance(reg, dict) else None, required
                    )
            except Exception:
                pass
            AppFunctions._reset_register_flow()
    
    @staticmethod
    def _reset_register_flow() -> None:
        """Reset the register flow in session state to initial values."""
        st.session_state["register"] = {
            "step": 1,
            "date": None,
            "tested_stis": [],
            "sti_realised_tests": {},
            "sti_results": {},
            "test_location": "",
            "notes": "",
        }

        try:
            logger = st.session_state.get("_app_logger")
            if logger:
                logger.info("Register flow reset to initial state")
        except Exception:
            pass
        
    def change_preferences(self) -> None:
        """
        Display and manage the user preferences form in the Streamlit interface.
        
        Allows the user to:
          - Select which STIs they want to track.
          - Choose a preferred reminder hour (HH:00 format).
          - Specify one or more identity/profile tags.
        
        The user can save changes or reset all preferences to defaults.
        Saved preferences are persisted using the UserPreferences class.
        
        """
        st.subheader("User Preferences")
        
        flash = st.session_state.pop("_flash_message", None)
        
        with st.form("prefs_form", clear_on_submit=True):
            
            tracked = st.multiselect(
                "Which STIs do you want to track?",
                stis_full_list,
                default=self.preferences.tracked_stis,
            )
        
            hours = [f"{h:02d}:00" for h in range(24)]
            reminder = st.selectbox(
                "Reminder hour",
                options=hours,
                index=hours.index(self.preferences.reminder_hour) if self.preferences.reminder_hour in hours else 8
            )
        
            tags = st.multiselect(
                "Profile tags",
                profile_tags_full_list,
                default=self.preferences.profile_tags,
                )
        
            c1, c2, c3, c4, c5 = st.columns([2, 1, 0.2, 2, 2])
            save_clicked = c1.form_submit_button("💾 Save")
            reset_clicked = c5.form_submit_button("🔄 Reset to default")
        
        if flash:
            kind, text = flash
            getattr(st, kind)(text)
            
        
        if save_clicked:
            self.preferences.set_preferences({
                "tracked_stis": tracked,
                "reminder_hour": reminder,
                "profile_tags": tags,
            })
            self.preferences.save_preferences()
            
            self.preferences.logger.info(
                "Preferences saved: tracked=%s, reminder=%s, tags=%s",
                tracked, reminder, tags
            )
            st.session_state["_flash_message"] = ("success", "Preferences saved ✅")
            st.rerun()
        
        
        if reset_clicked:
            self.preferences.reset_preferences()

            self.preferences.logger.warning("Preferences reset to default values by user action")
            st.session_state["_flash_message"] = ("info", "Preferences reset to default values.")
            st.rerun()
    
    def test_show(self) -> None:
        """Display test history with filters and (optional) manage/delete mode."""
        df = self.screening.register_show()
        df["Test_date"] = pd.to_datetime(df["Test_date"], errors="coerce")

        self.preferences.logger.debug("test_show: loaded %d record(s) for display", len(df))
        
        if df.empty:           
            st.info("No test history yet.")
        
        else:
            
            with st.sidebar.form("filters"):
                
                st.subheader("Filters")
            
                sti_options = sorted(df["STI"].dropna().unique().tolist())
                stis = st.multiselect(
                    "STIs",
                    options=sti_options
                    )
                
                min_ts = df["Test_date"].min()
                max_ts = df["Test_date"].max()
                min_date = min_ts.date() if pd.notna(min_ts) else None
                max_date = max_ts.date() if pd.notna(max_ts) else None         
                
                if min_date and max_date:
                    period = st.date_input("Test date", value=(min_date, max_date))
                else:
                    period = st.date_input("Test date")
                
                result_options = sorted(df["Result"].dropna().unique().tolist())
                result = st.multiselect(
                    "Result",
                    options=result_options)
            
                col_a, col_b = st.columns(2)
                apply_btn = col_a.form_submit_button("Apply")
                reset_btn = col_b.form_submit_button("Clear")
                
            if reset_btn:
                st.session_state["manage_mode"] = False
                st.session_state.pop("history_editor", None)

                self.preferences.logger.info("test_show: filters cleared, manage_mode reset")
                st.rerun()
                
            df_filtered = df.copy()
            
            if apply_btn:            
                mask = pd.Series(True, index=df_filtered.index)
                
                if stis:                
                    mask &= df_filtered["STI"].isin(stis)
                if result:
                    mask &= df_filtered["Result"].isin(result)
                
                    
                start_date = end_date = None
                if isinstance(period, (list, tuple)) and len(period) == 2:
                    start_date, end_date = period
                elif hasattr(period, "year"):
                    start_date = end_date = period
                
                if start_date:
                    start_ts = pd.to_datetime(start_date)
                    mask &= df_filtered["Test_date"] >= start_ts
                if end_date:
                    end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
                    mask &= df_filtered["Test_date"] <= end_ts
                    
                df_filtered = df_filtered.loc[mask]

                self.preferences.logger.info(
                    "test_show: filters applied (stis=%s, result=%s, start=%s, end=%s) → %d/%d rows",
                    stis, result, start_date, end_date, len(df_filtered), len(df)
                )
            
            df_filtered = df_filtered.sort_values("Test_date", ascending=False)
            
            st.caption(f"Showing {len(df_filtered)} out of {len(df)} records")
            
            manage = st.toggle("Manage mode", value=False, key="manage_mode")

            self.preferences.logger.debug("test_show: manage_mode=%s", manage)
            
            if manage:
                
                df_view = df_filtered.copy()
                df_view['delete'] = False
                
                check_rows = st.data_editor(
                    df_view,
                    column_config={"delete": st.column_config.CheckboxColumn("Delete row")},
                    use_container_width=True,
                    hide_index=False,
                    key="history_editor",                
                    )
                
                selected_labels = df_view.index[check_rows["delete"]].tolist()
                
                if selected_labels:
                    st.warning(f"You selected {len(selected_labels)} record(s) for deletion.")

                    self.preferences.logger.warning(
                        "test_show: %d row(s) selected for deletion (labels=%s)",
                        len(selected_labels), selected_labels
                    )
                    c1, c2 = st.columns(2)
                    if c1.button("Confirm delete", type="primary"):
                        
                        # Paulo Rodriguez - 30/10/2025
                        # build boolean mask against the full DataFrame by index labels
                        
                        full_index = self.screening.patient_history.index
                        mask = full_index.isin(selected_labels).tolist()

                        self.preferences.logger.warning(
                            "test_show: confirm delete pressed → deleting %d row(s)",
                            len(selected_labels)
                        )
                
                        self.screening.delete_rows(mask)
                        st.success("Records deleted successfully.")
                        st.rerun()
                    c2.button("Cancel")
            else:

                st.dataframe(df_filtered, use_container_width=True, hide_index=True)
