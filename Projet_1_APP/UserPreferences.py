import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, List, Optional


@dataclass
class UserPreferences:
    """Holds and persists user preferences for the app.

    Attributes:
        save_dir: Directory where the preferences file will be stored.
        tracked_stis: STIs (sexually transmitted infections) the user wants to track.
        reminder_hour: Preferred reminder time in 'HH:MM' (24h) or None.
        profile_tags: User profile tags (e.g., 'HSH' — men who have sex with men,
            'PrEP' — pre-exposure prophylaxis users).
    """
    
    _FILENAME: ClassVar[str] = "preferences.json"
    
    # Default to a project-local folder so the app is portable without extra setup.
    save_dir: Path = Path(__file__).resolve().parent / "preference_settings"
    tracked_stis: List[str] = field(default_factory=list)
    profile_tags: List[str] = field(default_factory=list)
    reminder_hour: Optional[str] = None
    _loaded: bool = field(init=False, default=False, repr=False)

    logger: Optional[logging.Logger] = field(init=False, default=None, repr=False)
    
    def __post_init__(self) -> None:
        """Initialize directories and logging after dataclass creation."""
        self.save_dir = Path(self.save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.configure_logging()
    
    def build_path(self) -> Path:    
        """Return the full path to a file."""  
        return self.save_dir / self._FILENAME
    
    def set_preferences(self, preferences_dict: dict[str, Any]) -> None:
        """Update user preferences from a dictionary.

        Only keys present in the input are updated.

        Args:
            preferences_dict: Dictionary that may include:
                - 'tracked_stis' (List[str])
                - 'reminder_hour' (str, format 'HH:MM')
                - 'profile_tags' (List[str])
        """
        self.tracked_stis = preferences_dict.get('tracked_stis', self.tracked_stis)
        self.reminder_hour = preferences_dict.get('reminder_hour', self.reminder_hour)
        self.profile_tags = preferences_dict.get('profile_tags', self.profile_tags)
        
    def load_preferences(self) -> bool:
        """Load user preferences from the JSON file.

        If the file does not exist or is invalid, default values are kept (No preferences; the user will
        have to configure before using the app).
        """ 
        
        # Paulo Rodriguez 02/11/2025
        # Avoid re-loading and re-logging on every Streamlit rerun
        if self._loaded:
            
            return True
        
        path = self.build_path()
        try:
            with open(path, "r", encoding="utf-8") as file:
                
                preferences_dict = json.load(file)
                self.set_preferences(preferences_dict)
                
            self.logger.info("Preferences loaded successfully from %s", path)
            self._loaded = True
            return True
                
        except FileNotFoundError:
            
            self.logger.warning("Preferences file not found at %s. Using defaults.", path)
            self._loaded = True
            return False
        
        except json.JSONDecodeError:
            
            self.logger.error("Invalid JSON file at %s. Using defaults.", path)
            self._loaded = True
            return False
            
    def save_preferences(self) -> None:
        """Save user preferences to a JSON file."""
        preferences_dict = self.to_dict()
        
        with open(self.build_path(), "w", encoding="utf-8") as file:
            
            json.dump(preferences_dict, file, indent=4, ensure_ascii=False)
    
    def reset_preferences(self) -> None:
        """
        Reset user preferences to their default (empty) values.
    
        This method clears all tracked STIs, reminder hour, and profile tags,
        then saves the default preferences to persistent storage.
        It does not replace the preferences instance, ensuring consistency.
        
        """
        self.set_preferences({
            "tracked_stis": [],
            "reminder_hour": None,
            "profile_tags": [],
        })
        self.save_preferences()
            
    def to_dict(self) -> dict[str, Any]:       
        """Return instance attributes (preferences) as a plain dictionary."""   
        return {
                "tracked_stis": self.tracked_stis,
                "reminder_hour": self.reminder_hour,
                "profile_tags": self.profile_tags,
                }
    
    def is_configured(self) -> bool:  
        """Return True if preferences are configured (onboarding not required)."""   
        return bool(self.tracked_stis)

    def configure_logging(self, level: int = logging.INFO) -> None:
        """Set up file and console logging for the app.
    
        Creates a 'log_files' folder in the save directory and configures
        a logger with both file ('app.log') and console output.
    
        Args:
            level: Logging level (default: logging.INFO).
        """

        if hasattr(self, "logger") and getattr(self.logger, "handlers", []):
            return
    
        log_dir_path = Path(self.save_dir).parent / "log_files"
        log_dir_path.mkdir(parents=True, exist_ok=True)
        log_file_path = log_dir_path / "app.log"
        
        # Paulo Rodriguez – 28/10/2025
        # Use a single, shared logger for the whole app
        logger = logging.getLogger("STITracker")
        logger.setLevel(level)
    
        # Paulo Rodriguez – 28/10/2025
        # Configure logging only once to avoid adding duplicate handlers.
        # This ensures that log messages are not printed or written multiple times
        # even when the logger is accessed from multiple modules or classes.
        if not logger.handlers:
            fmt = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )
    
            file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
            file_handler.setFormatter(fmt)
    
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(fmt)
    
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
    
            logger.propagate = False
            logger.info("Logging initialized → %s", log_file_path)
    
        self.logger = logger
    
                