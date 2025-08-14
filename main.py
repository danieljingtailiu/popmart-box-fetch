# main_unified.py
"""
PopMart Main Bot - Unified Version with Auto-Detection
No mode selection needed - automatically detects product type
"""

import time
from datetime import datetime
from seleniumbase import Driver
from unified_monitor import UnifiedPopMartMonitor
import json
import threading
import queue

class PopMartBot:
    def __init__(self):
        self.monitor_driver = None
        self.checkout_driver = None
        self.monitor = None
        self.auto_checkout = True
        self.monitoring = True
        self.stock_queue = queue.Queue()
        self.checkout_successful = False
        
    def setup_monitor_driver(self):
        """Setup browser for monitoring (lightweight)"""
        print("🔍 Starting monitor browser...")
        
        self.monitor_driver = Driver(
            uc=True,
            headless=False,
            incognito=False,
            undetectable=True
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
            page_load_strategy='eager'  # Don't wait for all resources
        )
        
        # Extra stealth for checkout browser
        self.checkout_driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
        })
        
        # Pre-inject speed optimization script
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
        
        # Pre-warm the browser by visiting key pages
        print("⚡ Pre-warming checkout browser...")
        self.checkout_driver.get("https://www.popmart.com/ca")
        time.sleep(0.5)
        
        # Pre-visit cart to cache resources
        self.checkout_driver.execute_script("window.open('https://www.popmart.com/ca/largeShoppingCart', '_blank');")
        time.sleep(0.5)
        
        # Close the extra tab
        handles = self.checkout_driver.window_handles
        if len(handles) > 1:
            self.checkout_driver.switch_to.window(handles[1])
            self.checkout_driver.close()
            self.checkout_driver.switch_to.window(handles[0])
        
        print("✅ Checkout browser ready and pre-warmed!")
    
    def quick_checkout_popnow(self, product_info):
        """Lightning-fast PopNow checkout - hits all the right buttons in the right order"""
        if not self.auto_checkout:
            return True
            
        try:
            print(f"\n⚡ POPNOW LIGHTNING CHECKOUT: {product_info['product_name']}")
            start_time = time.time()
            
            # 1. Go to PopNow page - MINIMAL WAIT
            self.checkout_driver.get(product_info['url'])
            time.sleep(0.4)  # Slightly increased to ensure page loads
            
            # 2. Click "Buy Multiple Boxes" - FAST
            print("📦 Buy Multiple Boxes...")
            self.checkout_driver.execute_script("""
                // Target the exact button element
                const buyBtn = document.querySelector('button.ant-btn.ant-btn-ghost.index_chooseMulitityBtn__n0MoA');
                if (buyBtn && buyBtn.textContent.includes('Buy Multiple Boxes')) {
                    buyBtn.click();
                } else {
                    // Fallback method
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.includes('Buy Multiple Boxes')) {
                            btn.click();
                            break;
                        }
                    }
                }
            """)
            time.sleep(0.2)  # Quick wait for modal
            
            # 3. PROPERLY Click SELECT ALL checkbox
            print("☑️ Select all...")
            self.checkout_driver.execute_script("""
                // Wait a tiny bit for checkboxes to render
                setTimeout(() => {
                    // Method 1: Click the first checkbox (usually select all)
                    const checkboxes = document.querySelectorAll('input[type="checkbox"].ant-checkbox-input');
                    if (checkboxes.length > 0) {
                        checkboxes[0].click();
                        console.log('Clicked select all checkbox');
                    }
                    
                    // Method 2: Ensure all are selected (backup)
                    setTimeout(() => {
                        const allCheckboxes = document.querySelectorAll('input[type="checkbox"].ant-checkbox-input');
                        allCheckboxes.forEach((cb, index) => {
                            if (index > 0 && !cb.checked) {  // Skip first (select all), check others
                                console.log(`Checkbox ${index} was not checked, clicking it`);
                                cb.click();
                            }
                        });
                    }, 100);
                }, 100);
            """)
            time.sleep(0.2)  # Quick wait for selection
            
            # 4. Click "ADD TO BAG"
            print("🛒 Add to bag...")
            self.checkout_driver.execute_script("""
                const buttons = document.querySelectorAll('button');
                for (let btn of buttons) {
                    if (btn.textContent.includes('ADD TO BAG')) {
                        btn.click();
                        break;
                    }
                }
            """)
            time.sleep(0.3)  # Quick wait for success notification
            
            # 5. Click "View" button - FAST
            print("👁️ View cart...")
            view_clicked = self.checkout_driver.execute_script("""
                // Target the exact View button element
                const viewBtn = document.querySelector('div.index_seeConfirmBtn__3mE7p');
                if (viewBtn && viewBtn.textContent.trim() === 'View') {
                    viewBtn.click();
                    return true;
                } else {
                    // Fallback method
                    const elements = document.querySelectorAll('div');
                    for (let el of elements) {
                        if (el.textContent.trim() === 'View' && el.offsetParent !== null) {
                            el.click();
                            return true;
                        }
                    }
                }
                return false;
            """)
            
            if not view_clicked:
                self.checkout_driver.get("https://www.popmart.com/ca/largeShoppingCart")
            
            time.sleep(0.4)  # Quick wait for cart
            
            # 6. Click "CONFIRM AND CHECK OUT" - FAST
            print("✅ Checkout...")
            self.checkout_driver.execute_script("""
                // Target the exact checkout button element
                const checkoutBtn = document.querySelector('button.ant-btn.ant-btn-primary.ant-btn-dangerous.index_checkout__V9YPC');
                if (checkoutBtn) {
                    checkoutBtn.click();
                } else {
                    // Fallback method
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.includes('CONFIRM AND CHECK OUT')) {
                            btn.click();
                            break;
                        }
                    }
                }
            """)
            time.sleep(0.8)  # Wait for payment page to load
            
            # 7. Click "PROCEED TO PAY" - FINAL STEP
            print("💳 Pay...")
            self.checkout_driver.execute_script("""
                // Target the exact payment button element
                const payBtn = document.querySelector('button.ant-btn.ant-btn-primary.ant-btn-dangerous.index_placeOrderBtn__wgYr6');
                if (payBtn) {
                    payBtn.click();
                } else {
                    // Fallback method
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.toUpperCase().includes('PROCEED TO PAY')) {
                            btn.click();
                            break;
                        }
                    }
                }
            """)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            print(f"\n⏱️ CHECKOUT COMPLETED IN: {total_time:.2f} seconds!")
            print("💳 COMPLETE PAYMENT NOW!")
            
            self.checkout_successful = True
            
            print("\n" + "="*60)
            print("💳 PAYMENT TIME")
            print("="*60)
            print("• Complete your payment in the checkout browser")
            print("• DO NOT CLOSE the checkout browser")
            print("• Monitoring has stopped - checkout browser stays open")
            print("="*60)
            
            return False  # Stop monitoring but keep browsers open
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return True
    
    def quick_checkout_normal(self, product_info):
        """Super quick checkout for regular products - gets you to payment in seconds"""
        if not self.auto_checkout:
            return True
            
        try:
            print(f"\n⚡ QUICK CHECKOUT: {product_info['product_name']}")
            
            # 1. Go directly to product page in checkout browser
            self.checkout_driver.get(product_info['url'])
            time.sleep(0.3)  # Reduced from 0.5s
            
            # 2. Click ADD TO BAG immediately - no setTimeout
            self.checkout_driver.execute_script("""
                const buttons = document.querySelectorAll('div[class*="index_usBtn__"], button');
                for (let btn of buttons) {
                    if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                        btn.click();
                        break;
                    }
                }
            """)
            
            time.sleep(0.3)  # Reduced from 0.5s
            
            # 3. Go to cart immediately
            self.checkout_driver.get("https://www.popmart.com/ca/largeShoppingCart")
            time.sleep(0.3)  # Reduced from 0.5s
            
            # 4. Select all and checkout in one script - faster execution
            self.checkout_driver.execute_script("""
                // Click select all immediately
                const selectAll = document.querySelector('div.index_checkbox__w_166');
                if (selectAll) selectAll.click();
                
                // Click checkout immediately after
                setTimeout(() => {
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.toUpperCase().includes('CHECK OUT')) {
                            btn.click();
                            break;
                        }
                    }
                }, 200);  // Reduced from 300ms
            """)
            
            time.sleep(0.5)  # Reduced from 1s
            
            # 5. Click proceed to pay
            self.checkout_driver.execute_script("""
                // Target the exact payment button element
                const payBtn = document.querySelector('button.ant-btn.ant-btn-primary.ant-btn-dangerous.index_placeOrderBtn__wgYr6');
                if (payBtn) {
                    payBtn.click();
                } else {
                    // Fallback method
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.toUpperCase().includes('PROCEED TO PAY')) {
                            btn.click();
                            break;
                        }
                    }
                }
            """)
            
            print("✅ Reached payment page!")
            print("⚠️ COMPLETE PAYMENT MANUALLY NOW!")
            
            self.checkout_successful = True
            
            print("\n" + "="*60)
            print("💳 PAYMENT TIME")
            print("="*60)
            print("• Complete your payment in the checkout browser")
            print("• DO NOT CLOSE the checkout browser")
            print("• Monitoring has stopped - checkout browser stays open")
            print("="*60)
            
            return False  # Stop monitoring but keep browsers open
            
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
            
            # Add to queue for checkout
            self.stock_queue.put(product_info)
            
            # Handle checkout with safety wrapper
            continue_monitoring = self.quick_checkout(product_info)
            
            return continue_monitoring
            
        except Exception as e:
            print(f"\n❌ Error in stock callback: {e}")
            print("⚠️ Continuing monitoring despite error...")
            return True  # Continue monitoring even if checkout fails
    
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
            
            # Auto-checkout preference
            auto_choice = input("\n🤖 Enable auto-checkout? (y/n): ").strip().lower()
            self.auto_checkout = auto_choice == 'y'
            
            print(f"\n{'='*60}")
            print(f"Setting up monitor for {len(product_ids)} products")
            print(f"Auto-checkout: {'ENABLED' if self.auto_checkout else 'DISABLED'}")
            print("🔍 Bot will auto-detect product types")
            print(f"{'='*60}")
            
            # Navigate to first product
            if len(product_ids) == 1:
                print("\n📍 Navigating to product page...")
                
                # Try to get URL from config, or construct it
                if product_ids[0] in self.monitor.products:
                    product_url = self.monitor.products[product_ids[0]]['url']
                else:
                    # Guess URL based on ID pattern
                    if len(product_ids[0]) == 3 and product_ids[0].isdigit():
                        product_url = f"https://www.popmart.com/ca/pop-now/set/{product_ids[0]}"
                    else:
                        product_url = f"https://www.popmart.com/ca/products/{product_ids[0]}/"
                
                self.monitor_driver.get(product_url)
                time.sleep(2)
                
                # Auto-detect type
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
    # Check for dependencies
    try:
        from seleniumbase import Driver
        from unified_monitor import UnifiedPopMartMonitor
    except ImportError as e:
        print("❌ Missing dependencies!")
        print("Please install: pip install seleniumbase")
        print(f"Error: {e}")
        exit(1)
    
    # Run bot
    bot = PopMartBot()
    bot.run() 