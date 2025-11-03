# 🧬 STI Tracker

A **Streamlit** application for managing and tracking **Sexually Transmitted Infections (STI)** test history and user preferences.  
All data is stored **locally** — ensuring privacy and control for the user.

---

## 📋 Overview

**STI Tracker** allows users to:
- Register new STI test results using a clean, multi-step interface.  
- View and filter previous test history.  
- Manage preferences such as:
  - Which STIs to track.
  - Reminder hour.
  - Profile tags (custom identifiers).  

Each user’s data is stored securely on their own machine — no online database or data sharing.

---

## 🧱 Project Structure

```
STI_Tracker/
├── app_main.py              # Application entry point
├── app_ui.py                # User interface (navigation & routing)
├── app_functions.py         # Main app logic (register, preferences, history)
├── UserPreferences.py       # Manages user preferences storage & validation
├── ScreeningLoader.py       # Handles saving/loading STI test history
├── Config_App.py            # Static configuration (lists, columns, etc.)
├── log_files/               # Generated folder for logs
├── patient_files/           # Folder where patient history CSV is stored
└── preference_settings/     # Folder where user preferences JSON is stored
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

*(if you don’t have a requirements.txt yet, you can create one using `pip freeze > requirements.txt`)*

### 2. Run the app
```bash
streamlit run app_main.py
```

### 3. Use the interface
- The app will open automatically in your browser.  
- On first launch, you’ll be asked to configure your preferences.  
- Then, you can register test results, view history, or adjust your settings at any time.

---

## 🧩 Key Features

| Feature | Description |
|----------|-------------|
| 🧪 **Test Register** | Step-by-step form to add new STI test results. |
| 📊 **History View** | Displays all saved tests with filters by STI, result, and date range. |
| ⚙️ **User Preferences** | Configure tracked STIs, reminder hour, and profile tags. |
| 💾 **Local Storage** | All data (CSV, JSON, logs) are stored locally — private by design. |
| 🧠 **Persistent Session** | Keeps track of current workflow (step and page). |
| 🧾 **Logging System** | Detailed logs for debugging and transparency. |

---

## 🧠 Technical Notes

- Built with **Streamlit** for UI and interactivity.  
- Uses **Pandas** for data handling.  
- Implements a **dataclass-based architecture** for clean separation between UI, logic, and data layers.  
- Logging is centralized — ensuring actions like loading/saving preferences or patient history are traceable.

---

## 🧰 Future Improvements

- Add authentication or user profiles.
- Add automatic notifying system when the user needs to do again his test (at reminder_hour)
- Export patient history as PDF or Excel.  
- Add visualization (charts for test trends).  
- Cloud backup or synchronization (optional).  
- Multilingual interface (EN/FR/PT).

---

## Demonstração
[🎥 Presentation Video](https://drive.google.com/file/d/1K7v64KhIAHksUdIjpBsi3Ub7jHBQfBVc/view)
ou

## 👨‍💻 Author

**Paulo Rodriguez**  
_DU - Data Analytics Master Student – Sorbonne Pantheon 1
📅 *October 2025*  

---

## 🧾 License

This project is provided for educational purposes.  
You’re free to explore, modify, and learn from it.
