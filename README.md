# Stake Limbo Selenium Bot

Python automation script for interacting with the Stake Limbo game using
Selenium and undetected-chromedriver.  
The script detects win/loss outcomes by reading the computed UI color and
stops based on a user-defined loss limit.

> ⚠️ For educational and experimental purposes only.

---

## Features

- Persistent Chrome user profile (keeps login session)
- Automatic bet button interaction
- Win/Loss detection using computed CSS color
- Configurable maximum loss limit
- Audible alert when max losses are reached
- User-controlled session restart
- Clean session-based execution (no infinite loops)

---

## Requirements

### System
- macOS/Windows
- Google Chrome installed
- Python 3.9 or higher

### Python Dependencies

Install dependencies using pip:

```bash
pip install selenium undetected-chromedriver webdriver-manager playsound3
