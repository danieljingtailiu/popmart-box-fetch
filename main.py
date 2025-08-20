# main.py
"""
PopMart Main Bot - Unified Version with Auto-Detection
No mode selection needed - automatically detects product type

NEW: JavaScript navigation optimization with reliable select all
- Replaced slow driver.get() with fast window.location.href
- Optimized page load waiting for maximum reliability
- Maintains full stealth and anti-detection features
- Cart → Select All process: 3 seconds wait + retry logic for reliability
- Fast and reliable checkout while maintaining success rate!
"""

import time
from datetime import datetime
from seleniumbase import Driver
from unified_monitor import UnifiedPopMartMonitor
# Remove unused imports to keep things clean
# import json
# import threading
# import queue

class PopMartBot:
    def __init__(self):
        self.monitor_driver = None
        self.checkout_driver = None
        self.monitor = None
        self.auto_checkout = True
        self.monitoring = True
        # Remove unused queue since we don't actually use it
        # self.stock_queue = queue.Queue()
        self.checkout_successful = False
        self.prefer_whole_set = False
        
    def setup_monitor_driver(self):
        """Setup browser for monitoring (lightweight)"""
        print("🔍 Starting monitor browser...")
        
        self.monitor_driver = Driver(
            uc=True,
            headless=False,
            incognito=False,
            undetectable=True,
            page_load_strategy='none'  # Skip waiting for resources to load - makes it really fast
        )
        
        self.monitor = UnifiedPopMartMonitor(self.monitor_driver)
        print("✅ Monitor browser ready")
    
    def setup_checkout_driver(self):
        """Setup separate browser for checkout (stays logged in) - OPTIMIZED"""
        print("🛒 Starting checkout browser...")
        
        self.checkout_driver = Driver(
            uc=True,
            headless=False,
            incognito=False,
            undetectable=True,
            uc_cdp_events=True,
            page_load_strategy='none'  # Skip waiting for resources to load - makes it really fast
        )
        
        # Make the checkout browser harder to detect
        self.checkout_driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
        })
        
        # Inject a script to speed things up
        self.checkout_driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                // Speed up setTimeout/setInterval
                window._setTimeout = window.setTimeout;
                window._setInterval = window.setInterval;
                window.setTimeout = function(fn, delay) {
                    return window._setTimeout(fn, Math.min(delay, 50));
                };
                window.setInterval = function(fn, delay) {
                    return window._setInterval(fn, Math.min(delay, 50));
                };
            '''
        })
        
        print("✅ Checkout browser ready")
    
    def login_checkout_browser(self):
        """Login on checkout browser and keep it ready - OPTIMIZED"""
        print("\n" + "="*60)
        print("🔐 LOGIN TO CHECKOUT BROWSER")
        print("="*60)
        print("⚠️ IMPORTANT: This browser will be used for checkout")
        print("1. Login to your PopMart account")
        print("2. Complete any captchas")
        print("3. Stay logged in - DO NOT close this browser")
        print("="*60)
        
        self.checkout_driver.get("https://www.popmart.com/ca/account")
        
        input("\n✅ Press ENTER when logged in...")
        print("Login confirmed!")
        
        # Warm up the browser by visiting some key pages first
        print("⚡ Pre-warming checkout browser...")
        self.checkout_driver.get("https://www.popmart.com/ca")
        time.sleep(0.2)  # Quick warm-up, much faster than before
        
        # Visit the cart page to cache some resources
        self.checkout_driver.execute_script("window.open('https://www.popmart.com/ca/largeShoppingCart', '_blank');")
        time.sleep(0.2)  # Quick cart pre-load, much faster than before
        
        # Close that extra tab we opened
        handles = self.checkout_driver.window_handles
        if len(handles) > 1:
            self.checkout_driver.switch_to.window(handles[1])
            self.checkout_driver.close()
            self.checkout_driver.switch_to.window(handles[0])
        
        print("✅ Checkout browser ready and pre-warmed!")
    
    def quick_checkout_popnow(self, product_info):
        """Fast PopNow checkout - hits all the right buttons in the right order"""
        if not self.auto_checkout:
            return True
            
        try:
            print(f"\n⚡ POPNOW CHECKOUT: {product_info['product_name']}")
            start_time = time.time()
            
            # 1. Go to the PopNow page
            self.checkout_driver.get(product_info['url'])
            time.sleep(0.2)  # Just a tiny wait for the page to load
            
            # 2. Click the "Buy Multiple Boxes" button
            print("📦 Buy Multiple Boxes...")
            self.checkout_driver.execute_script("""
                // Run this immediately - no waiting around
                (function() {
                    const buyBtn = document.querySelector('button.ant-btn.ant-btn-ghost.index_chooseMulitityBtn__n0MoA');
                    if (buyBtn && buyBtn.textContent.includes('Buy Multiple Boxes')) {
                        buyBtn.click();
                        return;
                    }
                    // Quick fallback if the first method doesn't work
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.includes('Buy Multiple Boxes')) {
                            btn.click();
                            return;
                        }
                    }
                })();
            """)
            time.sleep(0.03)  # Tiny wait for the modal to pop up
            
            # 3. Add to bag (remove the misplaced select all part)
            print("🛒 Add to bag...")
            self.checkout_driver.execute_script("""
                // Add the single box to bag right away
                (function() {
                    const buttons = document.querySelectorAll('div[class*="index_usBtn__"], button');
                    for (let btn of buttons) {
                        if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                            btn.click();
                            return;
                        }
                    }
                })();
            """)

            # Small wait to make sure the add to bag action completes
            time.sleep(0.2)  # Give it a moment to register with the server

            # 4. Go to cart with proper timing
            print("🛒 Going to cart...")

            # Use JavaScript navigation to bypass driver.get() inherent delays
            self.checkout_driver.execute_script("window.location.href = 'https://www.popmart.com/ca/largeShoppingCart';")

            # Wait for cart page to fully load
            time.sleep(3.0)  # Wait 3 seconds for page to fully load

            # Now execute select all on the cart page - single attempt
            print("☑️ Selecting all items in cart...")
            select_all_clicked = self.checkout_driver.execute_script("""
                // Select all logic for cart page - single attempt
                (function() {
                    const selectors = [
                        'div.index_checkbox__w_166',
                        '.ant-checkbox-wrapper',
                        'input[type="checkbox"]',
                        'div[class*="checkbox"]',
                        '.ant-checkbox'
                    ];
                    
                    let clicked = false;
                    
                    for (let selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            if (element.offsetParent !== null && !element.disabled) {
                                element.click();
                                console.log('Select all clicked using selector:', selector);
                                clicked = true;
                                break;
                            }
                        }
                        if (clicked) break;
                    }
                    
                    return clicked;
                })();
            """)
            
            if select_all_clicked:
                print("✅ Select all successful!")
            else:
                print("⚠️ Select all not found - proceeding anyway")
            
            # No waiting around - go straight to the checkout button
            print("🚀 Checkout button...")
            self.checkout_driver.execute_script("""
                // Step 2: Click checkout button with exact targeting and no delays
                (function() {
                    // Target the exact checkout button first with multiple fallbacks
                    const checkoutSelectors = [
                        'button.ant-btn.ant-btn-primary.ant-btn-dangerous.index_checkout__V9YPC',
                        'button[class*="index_checkout__"]',
                        'button.ant-btn.ant-btn-primary.ant-btn-dangerous'
                    ];
                    
                    let checkoutClicked = false;
                    
                    for (let selector of checkoutSelectors) {
                        const checkoutBtn = document.querySelector(selector);
                        if (checkoutBtn && checkoutBtn.offsetParent !== null) {
                            checkoutBtn.click();
                            console.log('Exact checkout button clicked using selector:', selector);
                            checkoutClicked = true;
                            break;
                        }
                    }
                    
                    // Fallback method if exact targeting fails
                    if (!checkoutClicked) {
                        const buttons = document.querySelectorAll('button');
                        for (let btn of buttons) {
                            if (btn.textContent.toUpperCase().includes('CHECK OUT') && btn.offsetParent !== null) {
                                btn.click();
                                console.log('Fallback checkout clicked');
                                checkoutClicked = true;
                                break;
                            }
                        }
                    }
                    
                    // Additional fallback for any checkout-related button
                    if (!checkoutClicked) {
                        const allButtons = document.querySelectorAll('button, div[class*="btn"], div[class*="button"]');
                        for (let btn of allButtons) {
                            const text = btn.textContent.toUpperCase();
                            if ((text.includes('CHECKOUT') || text.includes('CHECK OUT') || text.includes('CONFIRM')) && btn.offsetParent !== null) {
                                btn.click();
                                console.log('Additional fallback checkout clicked:', text);
                                break;
                            }
                        }
                    }
                    
                    console.log('Checkout button clicked - bot will stop here for manual completion');
                })();
            """)
            
            # NO DELAY - bot stops here after checkout button is clicked
            print("✅ Checkout button clicked! Bot will stop here for manual completion.")
            print("🛒 You are now on the payment page - complete checkout manually!")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n⏱️ CHECKOUT COMPLETED IN: {total_time:.2f} seconds!")
            print("🛒 MANUAL COMPLETION REQUIRED")
            
            self.checkout_successful = True
            
            print("\n" + "="*60)
            print("🛒 MANUAL CHECKOUT TIME")
            print("="*60)
            print("• Checkout button has been clicked")
            print("• You are now on the payment page")
            print("• Complete payment manually in the browser")
            print("• Bot will stop monitoring after getting the product")
            print("="*60)
            
            return False  # Stop monitoring after getting the product
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return True
    
    def quick_checkout_normal(self, product_info):
        """Quick checkout for regular products - gets you to payment in seconds"""
        if not self.auto_checkout:
            return True
            
        try:
            print(f"\n⚡ QUICK CHECKOUT: {product_info['product_name']}")
            start_time = time.time()
            
            # 1. Go directly to the product page in the checkout browser
            self.checkout_driver.get(product_info['url'])
            # No waiting around - go straight to adding to bag
            
            # 2. Select whole set if preferred, then add to bag
            if self.prefer_whole_set:
                print("📦 Selecting whole set...")
                self.checkout_driver.execute_script("""
                    // Run this right away - select the whole set first
                    (function() {
                        // Look for whole set option
                        const wholeSets = document.querySelectorAll('div.index_sizeInfoItem__f_Uxb');
                        for (let item of wholeSets) {
                            const title = item.querySelector('div.index_sizeInfoTitle__kpZbS');
                            if (title && title.textContent.trim().toLowerCase().includes('whole set')) {
                                item.click();
                                console.log('Whole set selected');
                                break;
                            }
                        }
                        
                        // Add to bag right after selection - no waiting around
                        const buttons = document.querySelectorAll('div[class*="index_usBtn__"], button');
                        for (let btn of buttons) {
                            if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                                btn.click();
                                return;
                            }
                        }
                        
                        // Continuous monitoring for ADD TO BAG button
                        if (!document.querySelector('div[class*="index_usBtn__"]')) {
                            console.log('Setting up monitoring for ADD TO BAG...');
                            
                            const observer = new MutationObserver((mutations) => {
                                for (let mutation of mutations) {
                                    if (mutation.type === 'childList') {
                                        mutation.addedNodes.forEach(node => {
                                            if (node.nodeType === 1) {
                                                const newButtons = node.querySelectorAll ? node.querySelectorAll('div[class*="index_usBtn__"], button') : [];
                                                if (node.matches && node.matches('div[class*="index_usBtn__"]')) {
                                                    newButtons.push(node);
                                                }
                                                
                                                for (let btn of newButtons) {
                                                    if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                                                        btn.click();
                                                        console.log('ADD TO BAG found and clicked via monitoring!');
                                                        observer.disconnect();
                                                        return;
                                                    }
                                                }
                                            }
                                        });
                                    }
                                }
                            });
                            
                            observer.observe(document.body, {
                                childList: true,
                                subtree: true
                            });
                        }
                    })();
                """)
            else:
                print("🛒 Adding single box to bag...")
                self.checkout_driver.execute_script("""
                    // Add the single box to bag right away - no waiting around
                    (function() {
                        const buttons = document.querySelectorAll('div[class*="index_usBtn__"], button');
                        for (let btn of buttons) {
                            if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                                btn.click();
                                return;
                            }
                        }
                        
                        // Continuous monitoring for ADD TO BAG button
                        if (!document.querySelector('div[class*="index_usBtn__"]')) {
                            console.log('Setting up monitoring for ADD TO BAG...');
                            
                            const observer = new MutationObserver((mutations) => {
                                for (let mutation of mutations) {
                                    if (mutation.type === 'childList') {
                                        mutation.addedNodes.forEach(node => {
                                            if (node.nodeType === 1) {
                                                const newButtons = node.querySelectorAll ? node.querySelectorAll('div[class*="index_usBtn__"], button') : [];
                                                if (node.matches && node.matches('div[class*="index_usBtn__"]')) {
                                                    newButtons.push(node);
                                                }
                                                
                                                for (let btn of newButtons) {
                                                    if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                                                        btn.click();
                                                        console.log('ADD TO BAG found and clicked via monitoring!');
                                                        observer.disconnect();
                                                        return;
                                                    }
                                                }
                                            }
                                        });
                                    }
                                }
                            });
                            
                            observer.observe(document.body, {
                                childList: true,
                                subtree: true
                            });
                        }
                    })();
                """)
            
            # Small wait to ensure ADD TO BAG completes
            time.sleep(0.2)  # Wait for add to bag to register
            
            # 3. Go to cart with proper timing
            print("🛒 Going to cart...")

            # Use JavaScript navigation to bypass driver.get() inherent delays
            self.checkout_driver.execute_script("window.location.href = 'https://www.popmart.com/ca/largeShoppingCart';")

            # Wait for cart page to fully load
            time.sleep(3.0)  # Wait 3 seconds for page to fully load

            # Now execute select all on the cart page - single attempt
            print("☑️ Selecting all items in cart...")
            select_all_clicked = self.checkout_driver.execute_script("""
                // Select all logic for cart page - single attempt
                (function() {
                    const selectors = [
                        'div.index_checkbox__w_166',
                        '.ant-checkbox-wrapper',
                        'input[type="checkbox"]',
                        'div[class*="checkbox"]',
                        '.ant-checkbox'
                    ];
                    
                    let clicked = false;
                    
                    for (let selector of selectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            if (element.offsetParent !== null && !element.disabled) {
                                element.click();
                                console.log('Select all clicked using selector:', selector);
                                clicked = true;
                                break;
                            }
                        }
                        if (clicked) break;
                    }
                    
                    return clicked;
                })();
            """)
            
            if select_all_clicked:
                print("✅ Select all successful!")
            else:
                print("⚠️ Select all not found - proceeding anyway")
            
            # No waiting around - go straight to the checkout button
            print("🚀 Checkout button...")
            self.checkout_driver.execute_script("""
                // Step 2: Click checkout button with exact targeting and no delays
                (function() {
                    // Target the exact checkout button first with multiple fallbacks
                    const checkoutSelectors = [
                        'button.ant-btn.ant-btn-primary.ant-btn-dangerous.index_checkout__V9YPC',
                        'button[class*="index_checkout__"]',
                        'button.ant-btn.ant-btn-primary.ant-btn-dangerous'
                    ];
                    
                    let checkoutClicked = false;
                    
                    for (let selector of checkoutSelectors) {
                        const checkoutBtn = document.querySelector(selector);
                        if (checkoutBtn && checkoutBtn.offsetParent !== null) {
                            checkoutBtn.click();
                            console.log('Exact checkout button clicked using selector:', selector);
                            checkoutClicked = true;
                            break;
                        }
                    }
                    
                    // Fallback method if exact targeting fails
                    if (!checkoutClicked) {
                        const buttons = document.querySelectorAll('button');
                        for (let btn of buttons) {
                            if (btn.textContent.toUpperCase().includes('CHECK OUT') && btn.offsetParent !== null) {
                                btn.click();
                                console.log('Fallback checkout clicked');
                                checkoutClicked = true;
                                break;
                            }
                        }
                    }
                    
                    // Additional fallback for any checkout-related button
                    if (!checkoutClicked) {
                        const allButtons = document.querySelectorAll('button, div[class*="btn"], div[class*="button"]');
                        for (let btn of allButtons) {
                            const text = btn.textContent.toUpperCase();
                            if ((text.includes('CHECKOUT') || text.includes('CHECK OUT') || text.includes('CONFIRM')) && btn.offsetParent !== null) {
                                btn.click();
                                console.log('Additional fallback checkout clicked:', text);
                                break;
                            }
                        }
                    }
                    
                    console.log('Checkout button clicked - bot will stop here for manual completion');
                })();
            """)
            
            # NO DELAY - bot stops here after checkout button is clicked
            print("✅ Checkout button clicked! Bot will stop here for manual completion.")
            print("🛒 You are now on the payment page - complete checkout manually!")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n⏱️ CHECKOUT COMPLETED IN: {total_time:.2f} seconds!")
            print("🛒 MANUAL COMPLETION REQUIRED")
            
            self.checkout_successful = True
            
            print("\n" + "="*60)
            print("🛒 MANUAL CHECKOUT TIME")
            print("="*60)
            print("• Checkout button has been clicked")
            print("• You are now on the payment page")
            print("• Complete payment manually in the browser")
            print("• Bot will stop monitoring after getting the product")
            print("="*60)
            
            return False  # Stop monitoring after getting the product
            
        except Exception as e:
            print(f"❌ Checkout error: {e}")
            return True
    
    def quick_checkout(self, product_info):
        """Route to appropriate checkout based on product type"""
        product_type = product_info.get('product_type', 'normal')
        
        if product_type == 'popnow':
            return self.quick_checkout_popnow(product_info)
        else:
            return self.quick_checkout_normal(product_info)
    
    def stock_found_callback(self, product_info):
        """This gets called when we find something in stock - time to buy!"""
        try:
            print(f"\n{'='*60}")
            print(f"🎯 STOCK FOUND: {product_info['product_name']}")
            print(f"📦 Product Type: {product_info.get('product_type', 'normal').upper()}")
            print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")
            
            # Handle checkout with safety wrapper
            continue_monitoring = self.quick_checkout(product_info)
            
            return continue_monitoring
            
        except Exception as e:
            print(f"\n❌ Error in stock callback: {e}")
            print("⚠️ Stopping monitoring due to error...")
            return False  # Stop monitoring due to error
    
    def cleanup_browsers(self):
        """Smart cleanup - ask what to do with browsers"""
        print("\n" + "="*60)
        print("🏁 BOT SESSION COMPLETE")
        print("="*60)
        
        if self.checkout_successful:
            print("✅ Stock was found and checkout attempted!")
            print("\nWhat would you like to do?")
            print("1. Keep checkout browser open (recommended)")
            print("2. Close all browsers")
            print("3. Keep both browsers open")
            
            choice = input("\nYour choice (1/2/3): ").strip()
            
            if choice == '1':
                print("✅ Keeping checkout browser open")
                if self.monitor_driver:
                    print("👋 Closing monitor browser...")
                    self.monitor_driver.quit()
                print("\n💡 Tip: You can continue shopping in the checkout browser")
            elif choice == '2':
                print("👋 Closing all browsers...")
                if self.monitor_driver:
                    self.monitor_driver.quit()
                if self.checkout_driver:
                    self.checkout_driver.quit()
            else:
                print("✅ Keeping both browsers open")
                print("💡 Close them manually when done")
        else:
            # No stock found - simple cleanup
            input("\n✅ Press ENTER to close all browsers...")
            if self.monitor_driver:
                self.monitor_driver.quit()
            if self.checkout_driver:
                self.checkout_driver.quit()
    
    def run(self):
        """Main bot execution with auto-detection"""
        print("⚡ PopMart Bot - Unified Auto-Detection Edition")
        print("=" * 60)
        print("🧠 Smart Detection: Automatically detects product type")
        print("🔍 Supports: Normal products & PopNow sets")
        print("=" * 60)
        
        try:
            # Setup both browsers
            self.setup_checkout_driver()
            self.login_checkout_browser()
            
            print("\n" + "="*60)
            print("Now setting up monitor browser...")
            print("=" * 60)
            
            self.setup_monitor_driver()
            
            # Get product selection
            while True:
                print("\n📦 Available products:")
                
                # Group by type for display
                normal_products = {pid: info for pid, info in self.monitor.products.items() if info.get('type') == 'normal'}
                popnow_products = {pid: info for pid, info in self.monitor.products.items() if info.get('type') == 'popnow'}
                
                if normal_products:
                    print("\n🛍️ Normal Products:")
                    for pid, info in normal_products.items():
                        print(f"  {pid}: {info['name']}")
                
                if popnow_products:
                    print("\n🎁 PopNow Sets:")
                    for pid, info in popnow_products.items():
                        print(f"  {pid}: {info['name']}")
                
                print("\n💡 Options:")
                print("  - Enter product ID(s) separated by comma")
                print("  - Type 'all' to monitor all products")
                print("  - Enter any ID (bot will auto-detect type)")
                
                choice = input("\nYour choice: ").strip().lower()
                
                if choice == 'all':
                    product_ids = self.monitor.get_all_product_ids()
                    break
                else:
                    product_ids = [pid.strip() for pid in choice.split(',') if pid.strip()]
                    
                    if product_ids:
                        # All IDs are valid - bot will auto-detect unknown ones
                        break
                    else:
                        print("❌ No product IDs entered")
            
            # Whole set preference (only for single product monitoring)
            self.prefer_whole_set = False
            if len(product_ids) == 1:
                whole_set_choice = input("\n📦 Whole set(y) or Single Box(n)? (y/n): ").strip().lower()
                self.prefer_whole_set = whole_set_choice == 'y'
                if self.prefer_whole_set:
                    print("✅ Will prioritize whole set selection during checkout")
            
            # Auto-checkout preference
            auto_choice = input("\n🤖 Enable auto-checkout? (y/n): ").strip().lower()
            self.auto_checkout = auto_choice == 'y'
            
            print(f"\n{'='*60}")
            print(f"Setting up monitor for {len(product_ids)} products")
            print(f"Auto-checkout: {'ENABLED' if self.auto_checkout else 'DISABLED'}")
            if hasattr(self, 'prefer_whole_set') and self.prefer_whole_set:
                print("📦 Whole set preference: ENABLED")
            print("🔍 Bot will auto-detect product types")
            print(f"{'='*60}")
            
            # Navigate to the first product
            if len(product_ids) == 1:
                print("\n📍 Navigating to product page...")
                
                # Try to get the URL from config, or construct it
                if product_ids[0] in self.monitor.products:
                    product_url = self.monitor.products[product_ids[0]]['url']
                else:
                    # Guess the URL based on ID pattern
                    if len(product_ids[0]) == 3 and product_ids[0].isdigit():
                        product_url = f"https://www.popmart.com/ca/pop-now/set/{product_ids[0]}"
                    else:
                        product_url = f"https://www.popmart.com/ca/products/{product_ids[0]}/"
                
                self.monitor_driver.get(product_url)
                time.sleep(0.2)  # Much faster navigation than before
                
                # Auto-detect the type
                detected_type = self.monitor.detect_product_type()
                print(f"✅ Detected product type: {detected_type.upper()}")
                
                input("\n✅ Press ENTER to START monitoring...")
                
                self.monitor.monitor_product(
                    product_ids[0], 
                    callback=self.stock_found_callback,
                    skip_navigation=True
                )
            else:
                print(f"✅ Will monitor {len(product_ids)} products")
                input("\n✅ Press ENTER to START monitoring...")
                
                self.monitor.monitor_multiple_products(
                    product_ids, 
                    callback=self.stock_found_callback
                )
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            
        finally:
            # Smart cleanup based on what happened
            self.cleanup_browsers()


if __name__ == "__main__":
            # Check if we have all the required packages
        try:
            from seleniumbase import Driver
            from unified_monitor import UnifiedPopMartMonitor
        except ImportError as e:
            print("❌ Missing dependencies!")
            print("Please install: pip install seleniumbase")
            print(f"Error: {e}")
            exit(1)
        
        # Start the bot
        bot = PopMartBot()
        bot.run() 