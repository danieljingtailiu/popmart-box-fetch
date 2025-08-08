# 🤖 PopMart Unified Bot

**Intelligent automated monitoring and purchasing system for PopMart collectibles**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![SeleniumBase](https://img.shields.io/badge/SeleniumBase-Latest-green.svg)](https://seleniumbase.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What This Bot Does

PopMart Unified Bot is a smart automation system that monitors PopMart products and handles checkout automatically. It works with **both regular products and PopNow mystery box sets**, automatically detecting which type you're monitoring without any configuration needed.

### 🧠 **Smart Features**
- **Auto-Detection**: Automatically figures out if you're monitoring regular products or PopNow sets
- **Lightning-Fast Monitoring**: Uses advanced techniques to catch restocks the moment they happen
- **Dual Browser System**: Separate browsers for monitoring and checkout for maximum speed
- **Crash-Resistant**: Built to handle errors gracefully and keep running
- **Works with LABUBU**: Yes, it works with LABUBU products too (though competition is fierce!)

## ⚡ **Speed & Performance**

### **Monitoring Speed**
- **100ms checks**: Monitors every 0.1 seconds for instant detection
- **Triple monitoring**: Uses MutationObserver + Polling + Animation Frame for maximum coverage
- **Instant restock detection**: Catches the exact moment stock becomes available

### **Checkout Speed**
- **PopNow products**: ~2 seconds from detection to payment page
- **Regular products**: ~3-4 seconds from detection to payment page
- **Pre-warmed browsers**: Checkout browser stays logged in and ready

## 🛠️ **Installation & Setup**

### **Requirements**
- Python 3.8 or higher
- Chrome browser
- PopMart account

### **Quick Start**
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/popmart-unified-bot.git
cd popmart-unified-bot

# 2. Install dependencies
pip install seleniumbase

# 3. Run the bot
python main.py
```

That's it! No configuration files needed. The bot will:
1. Ask you to login to PopMart in the checkout browser
2. Show you available products from `popmart_products.json`
3. Let you choose which products to monitor
4. Start monitoring automatically

## 📦 **Supported Products**

The bot automatically detects product types from your `popmart_products.json` file:

### **Current Products** (from popmart_products.json)
- **Regular Products**: THE MONSTERS series, HIRONO figures, Baby Molly & Tabby
- **PopNow Sets**: THE MONSTERS mystery boxes (IDs: 293, 170)

### **Adding New Products**
Just add them to `popmart_products.json`:
```json
{
  "YOUR_PRODUCT_ID": {
    "name": "Product Name",
    "url": "https://www.popmart.com/ca/products/YOUR_PRODUCT_ID/"
  }
}
```

The bot will automatically detect if it's a regular product or PopNow set based on the URL.

## 🎮 **How to Use**

### **Step 1: Start the Bot**
```bash
python main.py
```

### **Step 2: Login**
- Bot opens a checkout browser
- Login to your PopMart account
- Keep this browser open (it stays logged in)

### **Step 3: Choose Products**
- Bot shows available products
- Enter product IDs (e.g., `2710,293`) or type `all`
- Bot auto-detects product types

### **Step 4: Enable Auto-Checkout**
- Choose `y` for automatic purchasing
- Choose `n` for monitoring only

### **Step 5: Monitor**
- Bot opens monitoring browser
- Watches for stock changes in real-time
- Shows live status updates

### **Step 6: Checkout** (if auto-checkout enabled)
- Bot detects stock availability
- Automatically completes checkout process
- Takes you to payment page
- You complete payment manually

## 🚨 **Competition Reality Check**

### **LABUBU & High-Demand Releases**
- **This bot works with LABUBU** ✅
- **But competition is intense** ⚠️
- API-based bots can checkout in <1 second
- This browser-based bot takes ~2-4 seconds
- **Still worth trying** - many people succeed!

### **Best Success Rates**
- **PopNow mystery boxes**: Good success rate
- **Regular restocks**: Very good success rate  
- **Less popular characters**: Excellent success rate
- **LABUBU new releases**: Challenging but possible

### **Why This Bot Still Works**
- **Instant detection**: Catches restocks immediately
- **Reliable**: Doesn't crash like many other bots
- **Human-like**: Harder for PopMart to detect
- **Dual browser**: Checkout browser stays ready

## 🔧 **Technical Details**

### **Monitoring System**
```
Triple Monitoring Approach:
├── MutationObserver: Instant DOM change detection
├── High-frequency polling: 250ms backup checks  
└── Animation frame monitoring: Visual change detection
```

### **PopNow Checkout Process**
1. Click "Buy Multiple Boxes" button
2. Select all checkboxes automatically
3. Click "ADD TO BAG"
4. Click "View" to go to cart
5. Click "Confirm and Check out"
6. Click "PROCEED TO PAY"
7. User completes payment

### **Regular Product Checkout**
1. Click "ADD TO BAG" button
2. Go to cart automatically
3. Select all items
4. Click checkout
5. Click "PROCEED TO PAY"
6. User completes payment

## 🛡️ **Safety Features**

- **Crash protection**: Bot continues running even if errors occur
- **Browser safety**: Browsers don't auto-close after checkout
- **Error recovery**: Automatically reinjects monitoring code if needed
- **Human behavior**: Light scrolling to avoid detection
- **Session management**: Keeps you logged in across sessions

## ⚠️ **Important Notes**

### **Legal & Ethical Use**
- For personal use only (not commercial resale)
- Respects PopMart's servers with reasonable delays
- Requires manual payment completion
- User is responsible for following PopMart's Terms of Service

### **Realistic Expectations**
- **Not guaranteed**: No bot can guarantee success
- **Competition exists**: Other bots are also running
- **Manual payment**: You must complete payment yourself
- **Account risk**: Use at your own discretion

### **Best Practices**
- Don't run multiple instances simultaneously
- Don't monitor too many products at once
- Complete payments quickly when successful
- Keep your PopMart account secure

## 🔍 **Troubleshooting**

### **Common Issues**
- **"No products found"**: Check your `popmart_products.json` file
- **Login issues**: Make sure you're logged into the checkout browser
- **Monitoring stops**: Bot will try to restart automatically
- **Checkout fails**: Payment page should still be open for manual completion

### **Getting Help**
- Check the console output for error messages
- Make sure Chrome browser is up to date
- Ensure stable internet connection
- Try restarting the bot if issues persist

## 📈 **Success Tips**

1. **Monitor multiple products**: Increases your chances
2. **Focus on PopNow sets**: Often less competition
3. **Be ready for payment**: Have payment info ready
4. **Monitor during restocks**: Not just new releases
5. **Try different times**: Early morning or late night often better

## 🤝 **Contributing**

Want to improve the bot? Contributions welcome!

```bash
git clone https://github.com/yourusername/popmart-unified-bot.git
cd popmart-unified-bot
# Make your changes
# Submit a pull request
```

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

**🎯 Built for PopMart collectors who want a reliable, intelligent bot that actually works**

*Remember: This bot gives you an edge, but success still requires timing, luck, and quick payment completion!*
