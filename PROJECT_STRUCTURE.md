# 📁 Apt-Hunter Project Structure

## Core Files

### Main Application
- **`app.py`** - Main Flask web application (runs on port 5000)
- **`Search_Agent.py`** - Apartment scraping logic
- **`Classify_Agent.py`** - AI neighborhood classification

### Web Interface Templates
- **`templates/base.html`** - Base template with high-end styling
- **`templates/index.html`** - Main search form page
- **`templates/results.html`** - Search results display
- **`templates/error.html`** - Error page

### Startup Options
- **`start_web_interface.bat`** - Windows batch file (double-click to start)
- **`start_web_interface.py`** - Python launcher with dependency checking

### Configuration & Documentation
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Main project documentation
- **`README_WebInterface.md`** - Web interface specific guide
- **`TROUBLESHOOTING.md`** - Troubleshooting guide
- **`PROJECT_STRUCTURE.md`** - This file

## How to Start

### Option 1: Batch File (Easiest)
```bash
# Double-click this file:
start_web_interface.bat
```

### Option 2: Python Launcher (With Dependency Check)
```bash
python start_web_interface.py
```

### Option 3: Direct Launch
```bash
python app.py
```

## Access the Application
- **Main Interface:** http://localhost:5000
- **Test Page:** http://localhost:5000/test

## Project Features
- ✅ High-end glass morphism design
- ✅ Real-time progress tracking
- ✅ AI neighborhood classification
- ✅ Excel export functionality
- ✅ Responsive mobile design
- ✅ Comprehensive error handling
- ✅ Easy startup options

## Cleaned Up
- ❌ Removed redundant test files
- ❌ Removed duplicate templates
- ❌ Removed old log files
- ❌ Removed Python cache files
- ❌ Removed mock data files 