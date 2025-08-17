# 🤖 PopMart Unified Bot

**Intelligent automated monitoring and purchasing system for PopMart collectibles**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![SeleniumBase](https://img.shields.io/badge/SeleniumBase-Latest-green.svg)](https://seleniumbase.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What This Bot Does

PopMart Unified Bot is a smart automation system that monitors PopMart products and handles checkout automatically. It works with **both regular products and PopNow mystery box sets**, automatically detecting which type you're monitoring without any configuration needed.

## ⚠️ **IMPORTANT: Manual Payment Required**

**🛑 The bot does NOT complete payment automatically for security reasons**

- **What the bot does**: Monitors stock, adds items to cart, clicks "CHECK OUT"
- **What the bot does NOT do**: Enter payment info, click "PROCEED TO PAY", complete transaction
- **Your responsibility**: Complete payment manually on the payment page
- **Why**: Keeps your payment information private and secure

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
- **Regular Products**: THE MONSTERS series, HIRONO figures, Baby Molly & Tabby, **LABUBU Summer Ride**
- **PopNow Sets**: THE MONSTERS mystery boxes (IDs: 293, 170)
- **Total**: 7 products (5 regular + 2 PopNow)

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

## 🎮 **Step-by-Step Usage Guide**

### **Step 1: Start the Bot**
```bash
python main.py
```
The bot will start and show you the welcome screen.

### **Step 2: Setup Checkout Browser**
1. **Bot opens a Chrome browser** (this is your checkout browser)
2. **You see this message:**
   ```
   🔐 LOGIN TO CHECKOUT BROWSER
   1. Login to your PopMart account
   2. Complete any captchas
   3. Stay logged in - DO NOT close this browser
   ```
3. **Login to PopMart** in this browser
4. **Press ENTER** when logged in
5. **Keep this browser open** - it stays ready for checkout

### **Step 3: Setup Monitor Browser**
1. **Bot opens a second Chrome browser** (this is your monitoring browser)
2. **You see available products:**
   ```
   📦 Available products:
   
   🛍️ Normal Products:
     2710: THE MONSTERS Big into Energy Series
     3189: HIRONO Reshape Series Figures
     3501: Baby Molly & Baby Tabby Series Figures
     2088: THE MONSTERS Let's Checkmate Series-Vinyl Plush Doll
     3566: LABUBU Summerr Ride Figure
   
   🎁 PopNow Sets:
     293: THE MONSTERS - Exciting Macaron Vinyl Face Blind Box
     170: THE MONSTERRS Let's Checkmate Series-Fridge Magnet Blind Box
   ```

### **Step 4: Choose What to Monitor**
**💡 RECOMMENDATION: Choose ONE product ID for best results**

**Good choices:**
- Enter `2710` (for THE MONSTERS Energy Series)
- Enter `3566` (for LABUBU Summer Ride - CONFIRMED WORKING!)
- Enter `293` (for PopNow mystery box)
- Enter `3189` (for HIRONO figures)

**You can also:**
- Enter `all` (monitors everything - slower)
- Enter `2710,293` (multiple products - not recommended)

**Example:**
```
Your choice: 2710
```

### **Step 5: Choose Whole Set or Single Box (Single Product Only)**
```
📦 Whole set(y) or Single Box(n)? (y/n): y
```
- **Type `y`** - Bot will prioritize whole set selection during checkout
- **Type `n`** - Bot will add single box to bag
- **Note**: This option only appears when monitoring a single product

### **Step 6: Enable Auto-Checkout**
```
🤖 Enable auto-checkout? (y/n): y
```
- **Type `y`** - Bot will automatically checkout when stock is found
- **Type `n`** - Bot will only alert you (no automatic purchase)

### **Step 7: Start Monitoring**
```
✅ Press ENTER to START monitoring...
```
1. **Press ENTER** to begin
2. **Bot navigates** to your chosen product
3. **Monitoring starts** - you'll see:
   ```
   🟢 Checks: 1,234 | Status: Out of Stock (BLACK) | Type: NORMAL
   ```

### **Step 8: When Stock is Found**
**If stock becomes available:**
1. **Bot detects instantly** and shows:
   ```
   🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
   💥 RESTOCK MOMENT DETECTED! 💥
   🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
   ```

2. **Auto-checkout begins** (if enabled):
   ```
   ⚡ QUICK CHECKOUT: THE MONSTERS Big into Energy Series
   📦 Buy Multiple Boxes... (for PopNow)
   🛒 Add to bag...
   ✅ Checkout...
   ```

3. **🛑 BOT STOPS HERE** - **MANUAL PAYMENT REQUIRED**

### **Step 9: Manual Payment Completion**
**⚠️ IMPORTANT: The bot does NOT complete payment automatically**

1. **Bot clicks "CHECK OUT" button** and stops
2. **Payment page opens** in the checkout browser
3. **YOU must complete payment manually**:
   - Enter shipping address
   - Enter payment information
   - Click "PROCEED TO PAY" or similar final button
4. **Bot will NOT click payment buttons** for security reasons
5. **Don't close the browser** until payment is confirmed

---

## 📺 **What You'll Actually See**

### **When You Start the Bot:**
```
⚡ PopMart Bot - Unified Auto-Detection Edition
============================================================
🧠 Smart Detection: Automatically detects product type
🔍 Supports: Normal products & PopNow sets
============================================================

🔍 Starting monitor browser...
✅ Monitor browser ready

🔐 LOGIN TO CHECKOUT BROWSER
============================================================
⚠️ IMPORTANT: This browser will be used for checkout
1. Login to your PopMart account
2. Complete any captchas
3. Stay logged in - DO NOT close this browser
============================================================

✅ Press ENTER when logged in...
```

### **Choosing Products:**
```
📦 Available products:

🛍️ Normal Products:
  2710: THE MONSTERS Big into Energy Series
  3189: HIRONO Reshape Series Figures
  3501: Baby Molly & Baby Tabby Series Figures
  2088: THE MONSTERS Let's Checkmate Series-Vinyl Plush Doll
  3566: LABUBU Summerr Ride Figure

🎁 PopNow Sets:
  293: THE MONSTERS - Exciting Macaron Vinyl Face Blind Box
  170: THE MONSTERRS Let's Checkmate Series-Fridge Magnet Blind Box

💡 Options:
  - Enter product ID(s) separated by comma
  - Type 'all' to monitor all products
  - Enter any ID (bot will auto-detect type)

Your choice: 2710

📦 Whole set(y) or Single Box(n)? (y/n): y

🤖 Enable auto-checkout? (y/n): y

✅ Detected product type: NORMAL
✅ Press ENTER to START monitoring...
```

### **During Monitoring:**
```
⚡ HIGH-SPEED Monitoring: THE MONSTERS Big into Energy Series
🔗 URL: https://www.popmart.com/ca/products/2710/
🎯 Watching for: black button → red button (ADD TO BAG)

✅ Monitor script injected successfully
✅ Button found: ADD TO BAG
📋 Initial class: index_usBtn__abc123 index_black__def456

🚀 Monitor active - Checking multiple times per second...
👁️ Watching for button class change: index_black__ → index_red__
📊 Starting monitoring loop...
✅ Monitoring loop started successfully

🔴 Checks: 1,247 | Status: BLACK (Out of Stock) | Type: NORMAL
```

### **When Stock is Found:**
```
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
💥 RESTOCK MOMENT DETECTED! 💥
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

============================================================
🎯 STOCK FOUND: THE MONSTERS Big into Energy Series
📦 Product Type: NORMAL
⏰ Time: 2024-01-15 14:23:17
============================================================

⚡ QUICK CHECKOUT: THE MONSTERS Big into Energy Series
🛒 Add to bag...
🛒 Going to cart...
✅ Ultra-fast select all...
🚀 Ultra-fast checkout button...

⏱️ CHECKOUT COMPLETED IN: 2.34 seconds!
🛒 MANUAL COMPLETION REQUIRED

============================================================
🛒 MANUAL CHECKOUT TIME
============================================================
• Checkout button has been clicked
• You are now on the payment page
• Complete payment manually in the browser
• Bot will stop monitoring after getting the product
============================================================
```

## 🚨 **Competition Reality Check**

### **LABUBU & High-Demand Releases**
- **✅ CONFIRMED: This bot works with LABUBU** (tested and verified!)
- **⚠️ Competition is intense** - Many bots are targeting LABUBU
- **🤖 API-based bots** can checkout in <1 second
- **🌐 This browser-based bot** takes ~2-4 seconds
- **🎯 Still worth trying** - Success depends on timing and luck
- **💡 Best strategy**: Monitor single LABUBU product for maximum speed

### **Success Rates by Product Type**
- **🎁 PopNow mystery boxes**: Good success rate (less competition)
- **🔄 Regular restocks**: Very good success rate (less bot attention)
- **👥 Less popular characters**: Excellent success rate (HIRONO, Baby Molly)
- **🔥 LABUBU releases**: Challenging but **CONFIRMED WORKING** (choose single product!)
- **⭐ Single product monitoring**: **MUCH BETTER** than monitoring multiple products

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
4. Go to cart automatically
5. Click "Select All" checkbox
6. Click "CHECK OUT" button
7. **🛑 BOT STOPS HERE** - User completes payment manually

### **Regular Product Checkout**
1. **Choose whole set or single box** (if whole set preference enabled)
2. Click "ADD TO BAG" button
3. Go to cart automatically
4. Click "Select All" checkbox
5. Click "CHECK OUT" button
6. **🛑 BOT STOPS HERE** - User completes payment manually

**Note**: The bot intentionally stops at the checkout page for security reasons. You must complete payment manually.

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

### **🎯 MOST IMPORTANT: Choose Single Product**
- **✅ DO**: Enter one product ID (e.g., `2710`)
- **❌ DON'T**: Monitor multiple products at once
- **Why**: Single product = faster detection and checkout

### **🚀 Other Success Tips**
1. **Have payment ready**: Credit card info saved in browser
2. **Stable internet**: Wired connection better than WiFi
3. **Monitor restocks**: Not just new releases (less competition)
4. **Try off-peak hours**: Early morning (6-8 AM) or late night (11 PM-1 AM)
5. **Keep browsers open**: Don't close them between sessions
6. **For LABUBU**: Be extra quick with payment completion
7. **Payment speed is crucial**: The bot gets you to checkout fast, but you must complete payment quickly
8. **Pre-save payment info**: Have shipping address and payment method ready in browser

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

*Remember: payment completion is manual for privacy, ensure the speed to enter payment info is fast or have your payment info pre saved*
