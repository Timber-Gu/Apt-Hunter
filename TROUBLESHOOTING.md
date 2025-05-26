# 🔧 Apt-Hunter Troubleshooting Guide

## Cannot Open the Web Interface

If you're having trouble opening the web interface, try these solutions in order:

### 1. **Try Different Startup Methods**

**Option A: Use the Batch File (Recommended)**
```bash
# Double-click this file:
start_web_interface.bat

# Or run manually:
python app.py
```
Then open: http://localhost:5000

**Option B: Alternative Port**
If port 5000 is busy, edit app.py and change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)
```

### 2. **Check for Port Conflicts**

If you get "Address already in use" errors:
- Close any other web servers running
- Try a different port by editing the `.py` files
- Restart your computer to clear all ports

### 3. **Firewall Issues**

If the server starts but browser can't connect:
- Check Windows Firewall settings
- Allow Python through the firewall
- Try accessing via: http://127.0.0.1:8080 instead of localhost

### 4. **Browser Issues**

- Try a different browser (Chrome, Firefox, Edge)
- Clear browser cache and cookies
- Disable browser extensions temporarily
- Try incognito/private mode

### 5. **Python Environment Issues**

Check if all dependencies are installed:
```bash
pip install flask flask-cors pandas beautifulsoup4 selenium openai
```

### 6. **Test Basic Functionality**

Run this command to test if Flask works:
```bash
python -c "from flask import Flask; app = Flask(__name__); print('Flask is working!')"
```

### 7. **Check the Console Output**

When you start the app, look for these messages:
- ✅ "Running on http://127.0.0.1:5000" = Success
- ❌ "Address already in use" = Port conflict
- ❌ "ModuleNotFoundError" = Missing dependencies

### 8. **Alternative Access Methods**

If localhost doesn't work, try:
- http://127.0.0.1:5000
- http://0.0.0.0:5000
- Check your computer's IP address and use that

### 9. **Network Configuration**

For advanced users:
- Check if any VPN is interfering
- Verify Windows hosts file hasn't been modified
- Try disabling antivirus temporarily

### 10. **Last Resort Solutions**

If nothing else works:
1. Restart your computer
2. Reinstall Python and dependencies
3. Run as Administrator
4. Check Windows Event Viewer for errors

## Getting Help

If you're still having issues:
1. Note the exact error message
2. Check which Python version you're using: `python --version`
3. List installed packages: `pip list`
4. Try the test route: http://localhost:5000/test

## Quick Test Commands

```bash
# Test Python
python --version

# Test Flask
python -c "import flask; print('Flask version:', flask.__version__)"

# Test if port is free
netstat -an | findstr :5000

# Start with verbose output
python app.py
``` 