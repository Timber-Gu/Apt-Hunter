# 🏠 Apt-Hunter

The author is a lazy person. That why I designed a modern web-based apartment hunting tool that scrapes apartments.com and uses AI to classify neighborhoods. No more manual searching - just fill out a form and let the tool do the work!

## ✨ Features

- **🌐 Modern Web Interface**: Beautiful, responsive design with real-time progress tracking
- **🤖 AI Neighborhood Classification**: GPT-4 powered neighborhood categorization
- **📊 Excel Export**: Download results in easy-to-use Excel format
- **🔍 Advanced Filtering**: Filter by price, bedroom type, and location
- **📱 Mobile Friendly**: Works perfectly on desktop and mobile devices
- **⚡ Real-time Updates**: Watch your search progress live

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Web Interface
Choose one of these methods:

**Option A: Double-click the batch file (Windows)**
```
start_web_interface.bat
```

**Option B: Python launcher with dependency checking**
```bash
python start_web_interface.py
```

**Option C: Direct launch**
```bash
python app.py
```

### 3. Open Your Browser
Navigate to **http://localhost:5000** and start searching!

## 📋 How to Use

### Basic Search
1. **Select Location**: Choose your city and state
2. **Set Budget**: Enter your maximum monthly rent ($500-$10,000)
3. **Choose Bedrooms**: Select studio, 1-bed, 2-bed, or 3+ bedrooms
4. **Set Search Depth**: Choose pages to scrape (1-50, recommended: 10-15)
5. **Click "Start Search"**: Watch the real-time progress!

### AI Classification (Optional)
1. Check **"Enable AI Neighborhood Classification"**
2. Enter your **OpenAI API Key** ([Get one here](https://openai.com/api/)) (You deploy this locally, no one can get your API, so don't worry)
3. The tool will automatically classify apartments by neighborhood

### View Results
- **Browser Table**: View results directly in your browser
- **Excel Download**: Get raw data as Excel file
- **Classified Excel**: Download AI-classified version

## 🛠️ Technical Details

### Core Components
- **Search Agent**: Selenium-based scraper for apartments.com
- **Classification Agent**: OpenAI GPT-4 integration for neighborhood classification
- **Web Interface**: Flask application with modern UI

### Supported Locations
Works with any city on apartments.com including:
- Seattle, WA • San Francisco, CA • New York, NY
- Los Angeles, CA • Chicago, IL • Boston, MA
- Austin, TX • Denver, CO • And many more!

## 🔧 Troubleshooting

### Common Issues
- **Chrome driver not found**: Install Google Chrome (driver auto-downloads)
- **Search failed**: Check internet connection and city/state combination
- **Classification failed**: Verify OpenAI API key and credits
- **No results**: Try higher price limit or more bedroom types

### Need Help?
Check the comprehensive troubleshooting guide: `TROUBLESHOOTING.md`

## 🔒 Privacy & Security
- ✅ No data permanently stored
- ✅ API keys only used during session
- ✅ All processing happens locally on your machine

## 📁 Project Structure
```
Apt-Hunter/
├── app.py                    # Main Flask web application
├── Search_Agent.py           # Apartment scraping logic
├── Classify_Agent.py         # AI classification logic
├── templates/                # Web interface templates
├── start_web_interface.bat   # Easy Windows launcher
├── requirements.txt          # Python dependencies
└── TROUBLESHOOTING.md       # Detailed troubleshooting guide
```

## 🆚 Why Use the Web Interface?

| Feature | Web Interface | Command Line |
|---------|---------------|--------------|
| Ease of Use | ✅ Form-based | ❌ Edit code |
| Real-time Progress | ✅ Live updates | ❌ Limited feedback |
| Results Viewing | ✅ Browser + Excel | ❌ Excel only |
| Error Handling | ✅ User-friendly | ❌ Technical errors |
| Multiple Searches | ✅ Easy restart | ❌ Manual restart |

## 🤝 Contributing

Built with Flask, Bootstrap 5, and modern web technologies. Contributions welcome!

## 📄 License

Available for personal use.

---

**Happy apartment hunting! 🏠✨**

*Transform your apartment search from tedious to effortless.*
