# 🤖 PopMart Box Fetch

**Professional automated monitoring and purchasing system for PopMart collectibles**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![SeleniumBase](https://img.shields.io/badge/SeleniumBase-4.0+-green.svg)](https://seleniumbase.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ⚠️ Important Disclaimer & Bot Competition Reality

### 🚨 **Understanding the Competition Landscape**

This browser-based automation tool operates within realistic limitations and is designed for moderate competition scenarios. Here's what you need to know:

#### **🔴 High Competition Releases (LABUBU, Limited Drops)**
- **API-Based Bots Dominate**: Advanced scalpers use reverse-engineered mobile API endpoints
- **No FECU Token Required**: Mobile APIs bypass the encrypted FECU token system used by web browsers
- **Sub-Second Speed**: Direct API calls achieve checkout times under 1 second
- **Browser Disadvantage**: This tool cannot compete with API-based bots on speed alone

#### **🟢 Recommended Target Collections**
- **Molly Series**: Lower bot competition, higher success rates
- **Twinkle Twinkle**: Less targeted by scalpers, good availability windows
- **Space Molly**: Moderate competition, decent success chances
- **Hirono*: Variable competition depending on specific releases

#### **🔧 Technical Reality**
```
Web Browser Method (This Bot):
├── Requires DOM parsing and rendering
├── Subject to FECU token encryption
├── ~2-5 second checkout times
└── Human-like interaction patterns

Mobile API Method (Scalper Bots):
├── Direct API endpoint access
├── No FECU token requirements
├── ~0.5-1 second checkout times
└── Unlimited concurrent requests
```

### **💡 When This Bot Works Best**
- **Restocks of existing items** (less bot attention)
- **Non-LABUBU character releases** (lower competition)
- **Regional availability differences** (timing advantages)
- **Monitoring and alerts** (even if manual checkout needed)

---

## 🎯 Overview

PopMart Box Fetch is a sophisticated automation tool designed to monitor and purchase limited-edition collectibles from PopMart. Built with advanced web scraping techniques and intelligent stock monitoring, this bot ensures you never miss out on your favorite character releases.

## ✨ Key Features

### 🔥 **Advanced Product Discovery**
- **Multi-Character Support**: Monitor Space Molly, LABUBU, The Monsters, Molly, and Twinkle Twinkle
- **Intelligent Scrolling**: Advanced pagination with infinite scroll detection
- **Duplicate Prevention**: Smart filtering to avoid redundant product entries
- **Real-Time Updates**: Live product availability tracking

### 🚀 **Lightning-Fast Checkout**
- **Auto-Login**: Persistent session management with cookie storage
- **Smart Form Filling**: Automatic population of shipping and payment details
- **Purchase Confirmation**: User-controlled buying with confirmation prompts
- **Error Recovery**: Robust error handling and retry mechanisms

### 📊 **Professional Interface**
- **Real-Time Progress Bars**: Visual feedback during product scanning
- **Detailed Reporting**: Comprehensive session summaries and statistics
- **Clean Output**: Professional console interface with organized data display
- **Session Tracking**: Monitor runtime, cycles, and success rates

### 🛡️ **Security & Reliability**
- **Anti-Detection**: Browser fingerprint masking and human-like behavior
- **Session Persistence**: Secure cookie management and login state preservation
- **Rate Limiting**: Intelligent delays to prevent IP blocking
- **Popup Handling**: Automatic dismissal of modal dialogs and interruptions

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/popmart-box-fetch.git
cd popmart-box-fetch
```

2. **Install dependencies**
```bash
pip install seleniumbase
```

3. **Configure your settings**
Create a `config.py` file with your credentials:
```python
# Login credentials
POPMART_EMAIL = "your_email@example.com"
POPMART_PASSWORD = "your_password"

# Bot configuration
CHARACTER = "Molly"  # Options: "Space Molly", "LABUBU", "The Monsters", "Molly", "Twinkle Twinkle"
AUTO_CHECKOUT = True  # True for auto-purchase, False for monitoring only

# Shipping information
FIRST_NAME = "John"
LAST_NAME = "Doe"
ADDRESS = "123 Main Street"
CITY = "Vancouver"
ZIP_CODE = "V6B 1A1"
PHONE_NUMBER = "604-555-0123"

# Payment details
CREDIT_CARD_NUMBER = "4111111111111111"
NAME_ON_CARD = "John Doe"
EXPIRATION_DATE = "1228"  # MMYY format
SECURITY_CODE_CVV = "123"
```

4. **Run the bot**
```bash
python main.py
```

## 🎮 Usage

### Monitor Mode
Set `AUTO_CHECKOUT = False` in config.py to run in monitor-only mode:
- Continuously scans for product availability
- Reports stock status and pricing
- No automatic purchasing

### Auto-Checkout Mode
Set `AUTO_CHECKOUT = True` for automatic purchasing:
- Monitors products in real-time
- Prompts for user confirmation when products are available
- Completes checkout process automatically upon approval

### Character Selection
Choose your target character in config.py:
- **"Space Molly"** - Futuristic space-themed collectibles
- **"LABUBU"** ⚠️ - Popular rabbit-like character series (high bot competition)
- **"The Monsters"** - Cute monster-themed figures
- **"Molly"** ✅ - Classic Molly character variations (recommended)
- **"Twinkle Twinkle"** ✅ - Sparkly magical-themed collection (recommended)

## 📺 Sample Output

```
🚀 Initializing PopMart Checkout Bot...

═════════════════════════════════════════════════════════════════════
🤖 POPMART CHECKOUT BOT v2.0
═════════════════════════════════════════════════════════════════════
🎯 Target Character: Molly
🛒 Mode: AUTO-CHECKOUT
🌐 Search URL: https://www.popmart.com/ca/search/MOLLY
⏰ Started: 2024-01-15 21:27:04
═════════════════════════════════════════════════════════════════════

🔑 Authenticating...
✅ Already authenticated!

╔════════════════════════════════════════════════════════════════════╗
║ 🔄 SCAN CYCLE #001 - 21:27:04           Runtime: 0:00:15          ║
╚════════════════════════════════════════════════════════════════════╝

🔄 Loading products (Advanced Scroll + Pagination)...

📦 PRODUCT DISCOVERY SUMMARY
┌──────────────────────────────────────────────────────────────────────┐
│ Total Products Found: 37                         │
│ Search Method: Advanced Scroll + Pagination      │
│ Duplicate Removal: ✅ Enabled                   │
└──────────────────────────────────────────────────┘

🔍 SAMPLE PRODUCTS:
  01. MOLLY × INSTINCTOY GLOW Series Vinyl Plush...
  02. MOLLY Hirono Vacation Series Vinyl Plush...
  03. MOLLY The Monsters Series Vinyl Plush...
  04. MOLLY Carb-Lover Series Figures...
  05. MOLLY Baby Molly My Huggable Discovery...
  ... and 32 more products

🔍 CHECKING AVAILABILITY...
  [████████████████████] 100% │ MOLLY × INSTINCTOY GLOW Series...      │ ❌ OUT OF STOCK
  [████████████████████] 100% │ MOLLY Hirono Vacation Series...        │ ✅ AVAILABLE - $42.99
  [████████████████████] 100% │ MOLLY The Monsters Series...           │ ❌ OUT OF STOCK
  [████████████████████] 100% │ MOLLY Carb-Lover Series...             │ ❌ OUT OF STOCK

🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
 🛒 PURCHASE OPPORTUNITY DETECTED!
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

╔════════════════════════════════════════════════════════════════════╗
║ 📦 Product: MOLLY Hirono Vacation Series Vinyl Plush              ║
║ 💰 Price: $42.99 CAD                                              ║
║ 🔗 URL: https://www.popmart.com/ca/products/2018/MOLLY-Hirono     ║
╚════════════════════════════════════════════════════════════════════╝

💳 Purchase this product for $42.99? (y/n): y

🚀 Initiating checkout process...
🛒 Fast checkout initiated...
🛍️ Adding to cart...
✅ Added to cart!
🛒 Proceeding to cart...
💳 Processing checkout...
🎯 Placing order...
🚀 Submitting order...
🎉 Order successful!

🎉 CHECKOUT SUCCESSFUL!
✅ Order completed - stopping bot

📈 SESSION SUMMARY
┌──────────────────────────────────────────────────┐
│ Session Duration: 0:02:35                        │
│ Total Scan Cycles: 1                            │
│ Products Monitored: 37                           │
│ Mode: AUTO-CHECKOUT                              │
└──────────────────────────────────────────────────┘
```

## 🔧 Technical Details

### Architecture
- **SeleniumBase Framework**: Robust web automation with anti-detection features
- **Intelligent Scrolling**: Handles infinite scroll and pagination automatically
- **Multi-Method Stock Checking**: Combines DOM analysis, text scanning, and button state detection
- **Session Management**: Persistent login with encrypted cookie storage

### Performance Optimizations
- **Parallel Processing**: Concurrent product availability checks
- **Smart Caching**: Reduces redundant requests and improves speed
- **Optimized Selectors**: Fine-tuned CSS selectors for maximum compatibility
- **Rate Limiting**: Prevents overwhelming servers while maintaining speed

### Browser Compatibility
- **Chrome**: Primary support with undetected-chromedriver
- **Anti-Detection**: Masked browser fingerprints and human-like behavior patterns
- **Headless Mode**: Optional background operation for server deployment

## 🛡️ Security & Privacy

- **Local Storage**: All credentials and session data stored locally
- **Encrypted Sessions**: Secure cookie management with automatic cleanup
- **No Data Collection**: Bot operates independently without external data transmission
- **User Control**: Manual confirmation required for all purchases

## 📋 Supported Characters

| Character | Collection URL | Description | Bot Competition Level |
|-----------|---------------|-------------|----------------------|
| **Space Molly** | `/search/SPACE%20MOLLY` | Futuristic space-themed collectibles | 🟡 Medium |
| **LABUBU** | `/search/LABUBU` | Popular rabbit-like character series | 🔴 **Very High** |
| **The Monsters** | `/search/THE%20MONSTERS` | Cute monster-themed figures | 🟡 Medium |
| **Molly** | `/search/MOLLY` | Classic Molly character variations | 🟢 **Low-Medium** |
| **Twinkle Twinkle** | `/search/TWINKLE%20TWINKLE` | Sparkly magical-themed collection | 🟢 **Low-Medium** |

## ⚠️ Important Notes

### Bot Competition Reality
- **LABUBU Releases**: Expect heavy competition from API-based bots that bypass browser limitations
- **API Bots**: Some competitors use reverse-engineered mobile APIs for instant checkout (sub-second speeds)
- **Best Success Rate**: Focus on Molly, Twinkle Twinkle, or less popular collections
- **Realistic Expectations**: This browser-based approach prioritizes reliability over raw speed

### Legal Compliance
- **Terms of Service**: Ensure compliance with PopMart's ToS before use
- **Rate Limiting**: Bot includes built-in delays to respect server resources
- **Personal Use**: Intended for personal collecting, not commercial resale

### Responsible Usage
- **Manual Confirmation**: All purchases require user approval
- **Reasonable Limits**: Avoid excessive requests that could impact site performance
- **Account Security**: Use secure, unique passwords and enable 2FA when possible

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or suggest improvements.

### Development Setup
```bash
git clone https://github.com/yourusername/popmart-box-fetch.git
cd popmart-box-fetch
pip install -r requirements.txt
```

### Code Style
- Follow PEP 8 guidelines
- Include comprehensive docstrings
- Add unit tests for new features
- Maintain backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. **Check the Issues**: Browse existing GitHub issues for solutions
2. **Create an Issue**: Submit a detailed bug report or feature request
3. **Documentation**: Review the code comments and docstrings

## 🌟 Acknowledgments

- **SeleniumBase**: For providing an excellent web automation framework
- **PopMart Community**: For inspiration and feedback
- **Open Source Contributors**: For continuous improvements and bug fixes

---

**⭐ If this project helped you secure your favorite PopMart collectibles, please consider giving it a star!**

*Built with ❤️ for the PopMart collecting community*