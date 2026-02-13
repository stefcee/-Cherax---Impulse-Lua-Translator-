# 🚀 Impulse Language Translator

**Professional translation tool for Impulse nested JSON language files**

Created by **[Stefc3](https://github.com/Stefcee)**

## ✨ Features

- 🌍 **56 Languages supported** - French, German, Spanish, Chinese, Russian, Japanese, and many more
- 📦 **Nested JSON structure** - Handles complex menu translations perfectly
- 💾 **Resume function** - Cache system saves progress if interrupted
- ⚡ **3 Speed modes** - Slow/Safe, Normal, or Fast batch translation
- 🎯 **Smart handling** - Preserves null values and nested structure automatically

## 🛡️ Important

**⚠️ Use a VPN to avoid Google Translate rate limits!**  
Change your IP if you encounter translation errors during the process.

## 📋 Requirements

- Python 3.7 or higher
- Windows, Linux, or macOS

## 📥 Installation

### Method 1: Quick Start (Windows)
1. Download all 3 files: `ImpulseLanguageTranslator.py`, `START_TRANSLATOR.bat`, `requirements.txt`
2. Double-click `START_TRANSLATOR.bat` to auto-install dependencies & launch

### Method 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the translator
python ImpulseLanguageTranslator.py
```

## 🎮 Usage

1. **Select Source File** - Choose your `generated.json` file
2. **Choose Target Language** - Select from 56 available languages (e.g., French, German)
3. **Set Translation Speed**:
   - **Slow & Safe** - Single translation mode, safest for rate limits
   - **Normal** (Recommended) - Balanced batch translation
   - **Fast** - Maximum speed, higher risk of rate limits
4. **Click START** - Translation takes approximately 15-20 minutes for 2700+ entries
5. **Output** - File automatically saves as `generated_FR.json` (or your selected language code)

## 🌍 Supported Languages

Afrikaans, Albanian, Arabic, Armenian, Azerbaijani, Basque, Belarusian, Bengali, Bulgarian, Catalan, Chinese (Simplified), Chinese (Traditional), Croatian, Czech, Danish, Dutch, English, Estonian, Filipino, Finnish, **French**, Galician, Georgian, **German**, Greek, Gujarati, Haitian Creole, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Irish, Italian, **Japanese**, Kannada, Korean, Latvian, Lithuanian, Macedonian, Malay, Maltese, Norwegian, Persian, Polish, Portuguese, Romanian, **Russian**, Serbian, Slovak, Slovenian, **Spanish**, Swahili, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese, Welsh, Yiddish

## 💡 Tips

- **VPN is essential** - Switch VPN servers if you hit rate limits
- **Normal speed recommended** - Best balance between speed and reliability
- **Resume anytime** - Close and restart - your progress is saved
- **Check cache files** - Files named `cache_XX_nested.json` contain your progress

## 🔧 Troubleshooting

### "Rate limit exceeded" error
- Switch to a different VPN server/location
- Use slower translation speed
- Wait 10-15 minutes before retrying

### Translation stops unexpectedly
- Your progress is automatically saved
- Click START again to resume from where you left off
- Check the log window for specific error messages

### "Missing 'strings' key" error
- Ensure your JSON file has the correct Impulse structure
- File must contain a `"strings"` object at the root level

## 📂 File Structure

```
ImpulseLanguageTranslator/
│
├── ImpulseLanguageTranslator.py  # Main program
├── START_TRANSLATOR.bat           # Windows quick launch
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🎯 Perfect For

- Complex nested JSON language files
- Bulk translations (2000+ entries)
- Multi-language mod distribution

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available for personal and commercial use.

---

## 👨‍💻 Author

**Stefc3**  
- GitHub: [@Stefcee](https://github.com/Stefcee)
- Discord: [Discord Server](https://DC.gg/chatify)

*This project was developed with AI assistance from Claude Sonnet*

---

⭐ **If this tool helped you, consider giving it a star!** ⭐
