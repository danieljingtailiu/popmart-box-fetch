# unified_monitor.py
"""
Unified PopMart Monitor - Smart bot that figures out what kind of product you're watching
Works with regular PopMart stuff and those PopNow mystery boxes without you having to tell it which is which
"""

import time
from datetime import datetime
import json
import os
import random

class UnifiedPopMartMonitor:
    def __init__(self, driver=None):
        self.driver = driver
        self.products = {}
        self.load_all_products()
        
    def load_all_products(self):
        """Loads up all your products - both regular ones and PopNow mystery boxes"""
        # Load normal products
        normal_file = 'popmart_products.json'
        if os.path.exists(normal_file):
            with open(normal_file, 'r') as f:
                normal_products = json.load(f)
                # Auto-detect product type based on URL
                for pid, info in normal_products.items():
                    if '/pop-now/' in info.get('url', ''):
                        info['type'] = 'popnow'
                    else:
                        info['type'] = 'normal'
                    self.products[pid] = info
        
        # Load PopNow products
        popnow_file = 'popnow_products.json'
        if os.path.exists(popnow_file):
            with open(popnow_file, 'r') as f:
                popnow_products = json.load(f)
                # Mark as PopNow products
                for pid, info in popnow_products.items():
                    info['type'] = 'popnow'
                    self.products[pid] = info
        
        # Add default products if none loaded
        if not self.products:
            self.products = {
                '2710': {
                    'name': 'THE MONSTERS Big into Energy Series',
                    'url': 'https://www.popmart.com/ca/products/2710/',
                    'type': 'normal'
                },
                '293': {
                    'name': 'PopNow Mystery Box Set',
                    'url': 'https://www.popmart.com/ca/pop-now/set/293',
                    'type': 'popnow'
                }
            }
        
        print(f"✅ Loaded {len(self.products)} total products")
        normal_count = sum(1 for p in self.products.values() if p.get('type') == 'normal')
        popnow_count = sum(1 for p in self.products.values() if p.get('type') == 'popnow')
        print(f"   - {normal_count} normal products")
        print(f"   - {popnow_count} PopNow products")
    
    def detect_product_type(self):
        """Figures out if we're looking at a regular product or one of those PopNow mystery box pages"""
        try:
            # Method 1: Check URL
            current_url = self.driver.current_url
            if '/pop-now/' in current_url:
                return 'popnow'
            
            # Method 2: Check for specific elements
            result = self.driver.execute_script("""
                // Check for PopNow specific elements
                const buttons = document.querySelectorAll('button');
                let hasPopNowButtons = false;
                let hasNormalButtons = false;
                
                for (let btn of buttons) {
                    const text = btn.textContent.toUpperCase();
                    if (text.includes('BUY MULTIPLE BOXES') || text.includes('NOTIFY ME WHEN START')) {
                        hasPopNowButtons = true;
                    }
                    if (btn.className && btn.className.includes('index_usBtn__')) {
                        hasNormalButtons = true;
                    }
                }
                
                // Check for PopNow specific classes
                const popNowElements = document.querySelectorAll('[class*="ant-checkbox"], [class*="index_chooseMulitityBtn"]');
                if (popNowElements.length > 0) hasPopNowButtons = true;
                
                return {
                    hasPopNowButtons: hasPopNowButtons,
                    hasNormalButtons: hasNormalButtons,
                    url: window.location.href
                };
            """)
            
            if result['hasPopNowButtons']:
                return 'popnow'
            elif result['hasNormalButtons']:
                return 'normal'
            else:
                # Default based on URL pattern
                return 'popnow' if '/pop-now/' in result['url'] else 'normal'
                
        except Exception as e:
            print(f"⚠️ Error detecting product type: {e}")
            # Default to normal
            return 'normal'
    
    def inject_high_speed_monitor(self, product_type):
        """Injects the super-fast monitoring code that catches stock changes the moment they happen"""
        if product_type == 'popnow':
            monitor_js = """
            window.stockMonitor = {
                isMonitoring: false,
                lastButtonText: null,
                checkCount: 0,
                
                startHighSpeedMonitor: function() {
                    if (this.isMonitoring) return;
                    this.isMonitoring = true;
                    
                    console.log('High-speed PopNow monitor initialized');
                    
                    // Method 1: MutationObserver for instant detection
                    const observer = new MutationObserver((mutations) => {
                        for (let mutation of mutations) {
                            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                                // Check if it's a button
                                const target = mutation.target;
                                if (target.tagName === 'BUTTON') {
                                    this.checkButtonState(target);
                                }
                            }
                            
                            // Also check childList for dynamic content
                            if (mutation.type === 'childList') {
                                mutation.addedNodes.forEach(node => {
                                    if (node.nodeType === 1) { // Element node
                                        this.scanForButton(node);
                                    }
                                });
                            }
                        }
                    });
                    
                    // Observe entire body for any changes
                    observer.observe(document.body, {
                        attributes: true,
                        childList: true,
                        subtree: true,
                        attributeFilter: ['class', 'disabled']
                    });
                    
                    // Method 2: High-frequency polling as backup (250ms)
                    this.startPolling();
                    
                    // Method 3: Animation frame monitoring for visual changes
                    this.startAnimationFrameMonitor();
                },
                
                startPolling: function() {
                    setInterval(() => {
                        this.findAndCheckButton();
                        this.checkCount++;  // Increment on every poll
                    }, 250); // 4 checks per second
                },
                
                startAnimationFrameMonitor: function() {
                    let frameCount = 0;
                    const check = () => {
                        frameCount++;
                        if (frameCount % 60 === 0) {  // Every 60 frames (roughly 1 second at 60fps)
                            this.checkCount++;
                        }
                        this.findAndCheckButton();
                        if (this.isMonitoring) {
                            requestAnimationFrame(check);
                        }
                    };
                    requestAnimationFrame(check);
                },
                
                findAndCheckButton: function() {
                    this.checkCount++;  // Always increment
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        const btnText = btn.textContent.trim().toUpperCase();
                        if (btnText.includes('BUY MULTIPLE BOXES') || btnText.includes('NOTIFY ME WHEN START')) {
                            this.checkButtonState(btn);
                            break;
                        }
                    }
                },
                
                scanForButton: function(element) {
                    if (element.tagName === 'BUTTON') {
                        const btnText = element.textContent.trim().toUpperCase();
                        if (btnText.includes('BUY MULTIPLE BOXES') || btnText.includes('NOTIFY ME WHEN START')) {
                            this.checkButtonState(element);
                        }
                    }
                    
                    // Recursively check children
                    const buttons = element.querySelectorAll('button');
                    buttons.forEach(btn => {
                        const btnText = btn.textContent.trim().toUpperCase();
                        if (btnText.includes('BUY MULTIPLE BOXES') || btnText.includes('NOTIFY ME WHEN START')) {
                            this.checkButtonState(btn);
                        }
                    });
                },
                
                checkButtonState: function(button) {
                    const btnText = button.textContent.trim().toUpperCase();
                    
                    // Detect the specific button state changes
                    const wasBuyButton = this.lastButtonText === 'BUY';
                    const wasNotifyButton = this.lastButtonText === 'NOTIFY';
                    const isBuyButton = btnText.includes('BUY MULTIPLE BOXES');
                    const isNotifyButton = btnText.includes('NOTIFY ME WHEN START');
                    
                    // Stock is available if button is "Buy Multiple Boxes"
                    const isInStock = isBuyButton;
                    
                    // Store state change
                    if (btnText !== this.lastButtonText) {
                        console.log('PopNow button text changed:', btnText);
                        
                        // Critical: Detect NOTIFY -> BUY transition (restock moment)
                        if (wasNotifyButton && isBuyButton) {
                            console.log('🚨 POPNOW RESTOCK DETECTED! NOTIFY -> BUY transition');
                            window.__stockJustBecameAvailable = true;
                        }
                        
                        this.lastButtonText = btnText;
                        
                        // Set flag for any stock availability
                        if (isInStock) {
                            window.__stockAvailable = true;
                        }
                    }
                    // Update status (always update for check counting)
                    window.__stockStatus = {
                        available: isInStock,
                        buttonText: btnText,
                        timestamp: Date.now(),
                        checkCount: ++this.checkCount
                    };
                },
                
                clickBuyMultipleBoxes: function() {
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        const btnText = btn.textContent.trim().toUpperCase();
                        if (btnText.includes('BUY MULTIPLE BOXES')) {
                            btn.click();
                            return true;
                        }
                    }
                    return false;
                }
            };
            
            // Start monitoring immediately
            window.stockMonitor.startHighSpeedMonitor();
            """
        else:
            monitor_js = """
            window.stockMonitor = {
                isMonitoring: false,
                lastButtonClass: null,
                checkCount: 0,
                
                startHighSpeedMonitor: function() {
                    if (this.isMonitoring) return;
                    this.isMonitoring = true;
                    
                    console.log('High-speed monitor initialized');
                    
                    // Method 1: MutationObserver for instant detection
                    const observer = new MutationObserver((mutations) => {
                        for (let mutation of mutations) {
                            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                                // Check if it's the ADD TO BAG button
                                const target = mutation.target;
                                if (target.textContent && target.textContent.includes('ADD TO BAG')) {
                                    this.checkButtonState(target);
                                }
                            }
                            
                            // Also check childList for dynamic content
                            if (mutation.type === 'childList') {
                                mutation.addedNodes.forEach(node => {
                                    if (node.nodeType === 1) { // Element node
                                        this.scanForButton(node);
                                    }
                                });
                            }
                        }
                    });
                    
                    // Observe entire body for any changes
                    observer.observe(document.body, {
                        attributes: true,
                        childList: true,
                        subtree: true,
                        attributeFilter: ['class', 'disabled']
                    });
                    
                    // Method 2: High-frequency polling as backup (250ms)
                    this.startPolling();
                    
                    // Method 3: Animation frame monitoring for visual changes
                    this.startAnimationFrameMonitor();
                },
                
                startPolling: function() {
                    setInterval(() => {
                        this.findAndCheckButton();
                        this.checkCount++;  // Increment on every poll
                    }, 250); // 4 checks per second
                },
                
                startAnimationFrameMonitor: function() {
                    let frameCount = 0;
                    const check = () => {
                        frameCount++;
                        if (frameCount % 60 === 0) {  // Every 60 frames (roughly 1 second at 60fps)
                            this.checkCount++;
                        }
                        this.findAndCheckButton();
                        if (this.isMonitoring) {
                            requestAnimationFrame(check);
                        }
                    };
                    requestAnimationFrame(check);
                },
                
                findAndCheckButton: function() {
                    this.checkCount++;  // Always increment
                    const buttons = document.querySelectorAll('div[class*="index_usBtn__"]');
                    for (let btn of buttons) {
                        if (btn.textContent && btn.textContent.includes('ADD TO BAG')) {
                            this.checkButtonState(btn);
                            break;
                        }
                    }
                },
                
                scanForButton: function(element) {
                    if (element.classList && element.classList.toString().includes('index_usBtn__')) {
                        if (element.textContent && element.textContent.includes('ADD TO BAG')) {
                            this.checkButtonState(element);
                        }
                    }
                    
                    // Recursively check children
                    const buttons = element.querySelectorAll('div[class*="index_usBtn__"]');
                    buttons.forEach(btn => {
                        if (btn.textContent && btn.textContent.includes('ADD TO BAG')) {
                            this.checkButtonState(btn);
                        }
                    });
                },
                
                checkButtonState: function(button) {
                    const currentClass = button.className;
                    
                    // Detect the specific class change from black to red
                    const wasBlack = this.lastButtonClass && this.lastButtonClass.includes('index_black__');
                    const isRed = currentClass.includes('index_red__');
                    const isBlack = currentClass.includes('index_black__');
                    
                    // Stock is available if button has red class
                    const isInStock = isRed && !isBlack;
                    
                    // Store state change
                    if (currentClass !== this.lastButtonClass) {
                        console.log('Button class changed:', currentClass);
                        
                        // Critical: Detect black -> red transition (restock moment)
                        if (wasBlack && isRed) {
                            console.log('🚨 RESTOCK DETECTED! Black -> Red transition');
                            window.__stockJustBecameAvailable = true;
                        }
                        
                        this.lastButtonClass = currentClass;
                        
                        // Set flag for any stock availability
                        if (isInStock) {
                            window.__stockAvailable = true;
                        }
                    }
                    // Update status (always update for check counting)
                    window.__stockStatus = {
                        available: isInStock,
                        buttonClass: currentClass,
                        timestamp: Date.now(),
                        checkCount: ++this.checkCount
                    };
                },
                
                clickAddToBag: function() {
                    const buttons = document.querySelectorAll('div[class*="index_usBtn__"]');
                    for (let btn of buttons) {
                        if (btn.textContent && btn.textContent.includes('ADD TO BAG')) {
                            // Only click if it has red class (in stock)
                            if (btn.className.includes('index_red__')) {
                                btn.click();
                                return true;
                            }
                        }
                    }
                    return false;
                }
            };
            
            // Start monitoring immediately
            window.stockMonitor.startHighSpeedMonitor();
            """
        
        self.driver.execute_script(monitor_js)
    
    def monitor_product(self, product_id, callback=None, skip_navigation=False):
        """Main monitoring function - watches a single product and figures out what type it is automatically"""
        if product_id not in self.products:
            # Try to guess based on ID pattern
            is_popnow = len(product_id) == 3 and product_id.isdigit() and int(product_id) < 500
            
            print(f"⚠️ Product ID {product_id} not in config, creating entry...")
            if is_popnow:
                url = f"https://www.popmart.com/ca/pop-now/set/{product_id}"
                product_type = 'popnow'
            else:
                url = f"https://www.popmart.com/ca/products/{product_id}/"
                product_type = 'normal'
            
            self.products[product_id] = {
                'name': f'Product {product_id}',
                'url': url,
                'type': product_type
            }
        
        product = self.products[product_id]
        
        # Navigate if needed
        if not skip_navigation:
            print(f"📍 Navigating to product page...")
            self.driver.get(product['url'])
            time.sleep(0.8)  # Much faster navigation
        
        # Auto-detect product type from page
        detected_type = self.detect_product_type()
        print(f"\n🔍 Auto-detected product type: {detected_type.upper()}")
        
        # Update product type if different from config
        if product.get('type') != detected_type:
            print(f"📝 Updating product type from {product.get('type', 'unknown')} to {detected_type}")
            product['type'] = detected_type
        
        print(f"⚡ HIGH-SPEED Monitoring: {product['name']}")
        print(f"🔗 URL: {product['url']}")
        
        if detected_type == 'popnow':
            print("🎯 Watching for: NOTIFY ME WHEN START → Buy Multiple Boxes")
        else:
            print("🎯 Watching for: black button → red button (ADD TO BAG)")
        
        # Inject appropriate monitor
        try:
            self.inject_high_speed_monitor(detected_type)
            print("✅ Monitor script injected successfully")
        except Exception as e:
            print(f"❌ Failed to inject monitor script: {e}")
            return
        
        # Initial check
        time.sleep(0.2)  # Quick initial check
        try:
            if detected_type == 'popnow':
                initial_check = self.driver.execute_script("""
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        const text = btn.textContent.trim().toUpperCase();
                        if (text.includes('BUY MULTIPLE BOXES')) {
                            return {found: true, type: 'buy', text: btn.textContent};
                        } else if (text.includes('NOTIFY ME WHEN START')) {
                            return {found: true, type: 'notify', text: btn.textContent};
                        }
                    }
                    return {found: false};
                """)
                
                if initial_check['found']:
                    if initial_check['type'] == 'buy':
                        print(f"✅ Product is IN STOCK: {initial_check['text']}")
                    else:
                        print(f"🔴 Product is OUT OF STOCK: {initial_check['text']}")
            else:
                initial_check = self.driver.execute_script("""
                    const buttons = document.querySelectorAll('div[class*="index_usBtn__"]');
                    for (let btn of buttons) {
                        if (btn.textContent && btn.textContent.includes('ADD TO BAG')) {
                            return {
                                found: true,
                                className: btn.className,
                                text: btn.textContent
                            };
                        }
                    }
                    return {found: false};
                """)
                
                if initial_check['found']:
                    print(f"✅ Button found: {initial_check['text']}")
                    print(f"📋 Initial class: {initial_check['className']}")
        except Exception as e:
            print(f"⚠️ Error during initial check: {e}")
        
        print("\n🚀 Monitor active - Checking multiple times per second...")
        if detected_type == 'popnow':
            print("🎯 Watching for: NOTIFY ME WHEN START → Buy Multiple Boxes")
        else:
            print("👁️ Watching for button class change: index_black__ → index_red__")
        print("📊 Starting monitoring loop...")
        
        check_count = 0
        last_status_check = time.time()
        last_behavior = time.time()
        monitoring_active = True
        loop_iterations = 0
        
        while monitoring_active:
            try:
                loop_iterations += 1
                if loop_iterations == 1:
                    print("✅ Monitoring loop started successfully")
                
                # Fast check every 100ms
                time.sleep(0.1)
                
                # Check for restock moment
                try:
                    restock_detected = self.driver.execute_script("return window.__stockJustBecameAvailable || false;")
                except Exception as e:
                    print(f"\n⚠️ Error checking restock status: {e}")
                    restock_detected = False
                
                if restock_detected:
                    print(f"\n{'🚨'*30}")
                    print("💥 RESTOCK MOMENT DETECTED! 💥")
                    print(f"{'🚨'*30}")
                    
                    # Get full status
                    status = self.driver.execute_script("return window.__stockStatus;")
                    status['product_id'] = product_id
                    status['product_name'] = product['name']
                    status['url'] = product['url']
                    status['product_type'] = detected_type
                    
                    # Clear flag
                    self.driver.execute_script("window.__stockJustBecameAvailable = false;")
                    
                    if callback:
                        monitoring_active = callback(status)
                        if not monitoring_active:
                            break
                    continue
                
                # Regular stock check
                try:
                    stock_available = self.driver.execute_script("return window.__stockAvailable || false;")
                except Exception as e:
                    print(f"\n⚠️ Error checking stock status: {e}")
                    stock_available = False
                
                if stock_available:
                    status = self.driver.execute_script("return window.__stockStatus;")
                    if status and status.get('available'):
                        status['product_id'] = product_id
                        status['product_name'] = product['name']
                        status['url'] = product['url']
                        status['product_type'] = detected_type
                        
                        print(f"\n🟢 STOCK AVAILABLE - {product['name']}")
                        
                        if callback:
                            monitoring_active = callback(status)
                            if not monitoring_active:
                                break
                        
                        self.driver.execute_script("window.__stockAvailable = false;")
                
                # Status update every 2 seconds
                if time.time() - last_status_check > 2:
                    try:
                        js_status = self.driver.execute_script("""
                            return window.__stockStatus || {
                                checkCount: window.stockMonitor ? window.stockMonitor.checkCount : 0,
                                available: false
                            };
                        """)
                        
                        check_count = js_status.get('checkCount', 0)
                        is_available = js_status.get('available', False)
                        
                        status_icon = "🟢" if is_available else "🔴"
                        
                        if detected_type == 'popnow':
                            status_text = "In Stock (Buy Multiple)" if is_available else "Out of Stock (Notify Me)"
                        else:
                            button_class = js_status.get('buttonClass', 'unknown')
                            status_text = "RED (In Stock)" if "index_red__" in button_class else "BLACK (Out of Stock)"
                        
                        print(f"\r{status_icon} Checks: {check_count:,} | Status: {status_text} | Type: {detected_type.upper()}", end='', flush=True)
                        
                        last_status_check = time.time()
                    except Exception as e:
                        print(f"\n⚠️ Error updating status: {e}")
                
                # Light human behavior every 30 seconds
                if time.time() - last_behavior > 30:
                    self.driver.execute_script("window.scrollBy(0, 10);")
                    time.sleep(0.1)
                    self.driver.execute_script("window.scrollBy(0, -10);")
                    last_behavior = time.time()
                
            except KeyboardInterrupt:
                print("\n\n⌨️ Monitoring stopped by user (Ctrl+C)")
                break
            except Exception as e:
                print(f"\n⚠️ Monitoring error: {type(e).__name__}: {e}")
                print("📍 Attempting to continue monitoring...")
                time.sleep(0.5)
                try:
                    # Try to reinject monitor
                    detected_type = self.detect_product_type()
                    self.inject_high_speed_monitor(detected_type)
                    print("✅ Monitor reinjected")
                except Exception as reinject_error:
                    print(f"❌ Failed to reinject monitor: {reinject_error}")
                    print("⚠️ Monitoring may be degraded")
        
        print(f"\n📊 Monitoring ended after {loop_iterations} iterations")
    
    def monitor_multiple_products(self, product_ids, callback=None):
        """Watches multiple products at once - opens them in different tabs and keeps an eye on all of them"""
        print(f"\n⚡ Monitoring {len(product_ids)} products")
        
        # Open tabs and detect types
        tab_products = []
        
        for i, product_id in enumerate(product_ids):
            if product_id not in self.products:
                print(f"⚠️ Product {product_id} not in config, will auto-detect...")
                # Create placeholder
                self.products[product_id] = {
                    'name': f'Product {product_id}',
                    'url': f'https://www.popmart.com/ca/products/{product_id}/',
                    'type': 'unknown'
                }
            
            product = self.products[product_id]
            
            if i == 0:
                self.driver.get(product['url'])
            else:
                self.driver.execute_script(f"window.open('{product['url']}', '_blank');")
            
            time.sleep(0.8)  # Faster tab opening
            
            all_handles = self.driver.window_handles
            self.driver.switch_to.window(all_handles[-1])
            
            # Detect type and inject monitor
            detected_type = self.detect_product_type()
            product['type'] = detected_type
            self.inject_high_speed_monitor(detected_type)
            
            tab_products.append((all_handles[-1], product_id, detected_type))
            print(f"✅ Tab {i+1}: {product['name']} ({detected_type})")
        
        print("\n🚀 High-speed monitoring active on all tabs...")
        
        check_count = 0
        tab_index = 0
        
        while True:
            try:
                handle, product_id, product_type = tab_products[tab_index]
                self.driver.switch_to.window(handle)
                
                # Quick check
                restock = self.driver.execute_script("return window.__stockJustBecameAvailable || false;")
                stock = self.driver.execute_script("return window.__stockAvailable || false;")
                
                if restock or stock:
                    status = self.driver.execute_script("return window.__stockStatus;")
                    if status:
                        status['product_id'] = product_id
                        status['product_name'] = self.products[product_id]['name']
                        status['url'] = self.products[product_id]['url']
                        status['product_type'] = product_type
                        
                        print(f"\n🟢 STOCK AVAILABLE - {self.products[product_id]['name']} ({product_type})")
                        
                        if callback:
                            if not callback(status):
                                break
                        
                        self.driver.execute_script("window.__stockJustBecameAvailable = false;")
                        self.driver.execute_script("window.__stockAvailable = false;")
                
                tab_index = (tab_index + 1) % len(tab_products)
                check_count += 1
                
                if tab_index == 0:
                    print(f"\r⚡ Cycles: {check_count // len(tab_products)} | Checking all products...", end='', flush=True)
                
                time.sleep(0.2)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                time.sleep(0.5)
    
    # Keep the stealth methods for backwards compatibility
    def monitor_single_product_stealth(self, product_id, callback=None, skip_navigation=False):
        """Use unified monitoring instead"""
        return self.monitor_product(product_id, callback, skip_navigation)
    
    def monitor_multiple_products_stealth(self, product_ids, callback=None):
        """Use unified monitoring instead"""
        return self.monitor_multiple_products(product_ids, callback)
    
    def monitor_single_product_fast(self, product_id, callback=None, skip_navigation=False):
        """Use unified monitoring instead"""
        return self.monitor_product(product_id, callback, skip_navigation)
    
    def monitor_multiple_products_fast(self, product_ids, callback=None):
        """Use unified monitoring instead"""
        return self.monitor_multiple_products(product_ids, callback)
    
    def get_all_product_ids(self):
        """Get all available product IDs"""
        return list(self.products.keys())