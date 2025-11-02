from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar, Optional

import pandas as pd

from Config_App import patient_history_columns
from UserPreferences import UserPreferences


@dataclass
class ScreeningLoader(UserPreferences):
    """Handles loading, saving, and updating patient STI test history data.

    Inherits from UserPreferences to use the same saving directory
    structure and logging configuration.
    """
    
    _FILENAME: ClassVar[str] = "patient_history.csv"
    
    save_dir: Path = Path(__file__).resolve().parent / "patient_files"   
    patient_history: Optional[pd.DataFrame] = None
    

    def __post_init__(self) -> None:
        """Initialize directories after dataclass creation."""
        super().__post_init__()
        self.build_path().parent.mkdir(parents=True, exist_ok=True)

    def load_patient_history(self) -> None:
        """Load patient history from CSV file.

        If the file does not exist, creates an empty DataFrame with
        predefined columns from Config_App.patient_history_columns.
        """
        path_to_history = self.build_path()
        
        try:   
            self.patient_history = pd.read_csv(path_to_history)
            self.logger.info("Patient history loaded successfully from %s.", path_to_history)
        except FileNotFoundError:   
            self.patient_history = pd.DataFrame(columns=patient_history_columns)
            self.logger.warning("History data not found, using empty dataframe.")
            
    def save_patient_history(self) -> None:
        """Save patient history to CSV file.

       If patient_history is empty or invalid, logs a warning instead.
       """
        path_to_history = self.build_path()
        
        if self.patient_history is None:
            self.logger.warning("No patient history to save at %s.", path_to_history)
            
            return
        
        try:
            self.patient_history.to_csv(path_to_history, index=False)
            self.logger.info("Patient history saved to %s.", path_to_history)  
        except Exception:
            self.logger.exception("Failed to save patient history to %s.", path_to_history)
            
    @staticmethod
    def register_to_rows(register: dict[str, Any]) -> pd.DataFrame:
        """Convert a patient test register dictionary (from Streamlit forms)
        into one or more DataFrame rows.

        Args:
            register: Dictionary containing patient test information.

        Returns:
            A DataFrame with one row per tested STI, formatted according
            to patient_history_columns.
        """
        tested_stis = register.get("tested_stis", []) or []
        td = pd.to_datetime(register.get("date"), errors="coerce")
        date_val = td.date() if pd.notna(td) else None
        
        rows = [{
                    "Test_date": date_val,
                    "STI": sti,
                    "Test_type": register.get("sti_realised_tests", {}).get(sti),
                    "Result": register.get("sti_results", {}).get(sti),
                    "Location": register.get("test_location", ""),
                    "Notes": register.get("notes", ""),
                    "Entry_ts": pd.Timestamp.utcnow().normalize()
                } for sti in tested_stis]
        
        return pd.DataFrame(rows, columns=patient_history_columns)
    
    def append_register(self, df: pd.DataFrame) -> None:
        """Append a new test register DataFrame to the patient history.

        Loads the history if not already in memory, appends new rows, and
        saves the updated CSV file.
        
        Args:
            df: DataFrame to append to the current patient history.
        """
        if self.patient_history is None:
            self.load_patient_history()

        if df is None or df.empty:
            self.logger.warning("append_register called with an empty DataFrame — nothing added.")
            
            return
            
        self.patient_history = pd.concat([self.patient_history, df], ignore_index=True)   
        self.save_patient_history()
        
        self.logger.info("Patient history updated with %d new row(s).", len(df))
    
    def register_show(self) -> pd.DataFrame:
        """Return a copy of the current patient history DataFrame to be shown
        on the app.

        Automatically loads the file if not already in memory, renames
        the 'Entry_ts' (entry timestamp) column to 'Register_date' for clarity.
        """
        if self.patient_history is None:
            self.load_patient_history()
            
        df = self.patient_history.copy()
        df = df.rename(columns={"Entry_ts": "Register_date"})
    
        return df

    def delete_rows(self, mask: pd.Series | list[bool]) -> None:
        """Delete rows from patient history using a boolean mask.

        Args:
            mask: Boolean mask (pd.Series or list[bool]) with same length as patient_history.
        """
        if self.patient_history is None:          
            self.load_patient_history()
        
        if mask is None or len(mask) != len(self.patient_history):  
            self.logger.warning("Invalid mask length or empty mask — nothing deleted.")
            
            return
        
        mask_series = pd.Series(mask, index=self.patient_history.index)
        self.patient_history = self.patient_history.loc[~mask_series].reset_index(drop=True)
        self.save_patient_history()
        
        self.logger.info("Deleted %d rows from patient history.", int(mask_series.sum()))
