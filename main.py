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
        self.prefer_whole_set = False
        
    def setup_monitor_driver(self):
        """Setup browser for monitoring (lightweight)"""
        print("🔍 Starting monitor browser...")
        
        self.monitor_driver = Driver(
            uc=True,
            headless=False,
            incognito=False,
            undetectable=True,
            page_load_strategy='none'  # Don't wait for any resources - FASTEST
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
            page_load_strategy='none'  # Don't wait for any resources - FASTEST
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
        time.sleep(0.2)  # Much faster pre-warming
        
        # Pre-visit cart to cache resources
        self.checkout_driver.execute_script("window.open('https://www.popmart.com/ca/largeShoppingCart', '_blank');")
        time.sleep(0.2)  # Much faster cart pre-loading
        
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
            
            # 1. Go to PopNow page - ULTRA FAST
            self.checkout_driver.get(product_info['url'])
            time.sleep(0.2)  # Minimal wait for page load
            
            # 2. Click "Buy Multiple Boxes" - ULTRA FAST
            print("📦 Buy Multiple Boxes...")
            self.checkout_driver.execute_script("""
                // Immediate execution - no delays
                (function() {
                    const buyBtn = document.querySelector('button.ant-btn.ant-btn-ghost.index_chooseMulitityBtn__n0MoA');
                    if (buyBtn && buyBtn.textContent.includes('Buy Multiple Boxes')) {
                        buyBtn.click();
                        return;
                    }
                    // Ultra fast fallback
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.includes('Buy Multiple Boxes')) {
                            btn.click();
                            return;
                        }
                    }
                })();
            """)
            time.sleep(0.03)  # Ultra minimal wait for modal
            
            # 3. ULTRA FAST SELECT ALL checkbox
            print("☑️ Select all...")
            self.checkout_driver.execute_script("""
                // Immediate execution - no setTimeout delays
                (function() {
                    // The REAL select all button is usually a div with checkbox-like behavior
                    // Try the most common selectors in order of likelihood
                    const selectAllSelectors = [
                        'div.index_checkbox__w_166',  // Main select all div
                        '.ant-checkbox-wrapper',       // Ant Design checkbox wrapper
                        'div[class*="checkbox"]',     // Any div with checkbox in class
                        'input[type="checkbox"]',     // Actual checkbox input
                        '.ant-checkbox'               // Ant Design checkbox class
                    ];
                    
                    let selectAllClicked = false;
                    
                    // First, try to find and click the select all button
                    for (let selector of selectAllSelectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            // Check if this looks like a select all button
                            if (element.offsetParent !== null && !element.disabled) {
                                // Click it immediately
                                element.click();
                                console.log('Select all clicked using selector:', selector);
                                selectAllClicked = true;
                                break;
                            }
                        }
                        if (selectAllClicked) break;
                    }
                    
                    // If still not clicked, try clicking ALL checkboxes
                    if (!selectAllClicked) {
                        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                        if (allCheckboxes.length > 0) {
                            allCheckboxes.forEach((cb, index) => {
                                if (!cb.checked && cb.offsetParent !== null) {
                                    cb.click();
                                    console.log('Individual checkbox clicked:', index);
                                }
                            });
                            selectAllClicked = true;
                        }
                    }
                    
                    // Final fallback: click any clickable element that might be select all
                    if (!selectAllClicked) {
                        const clickableElements = document.querySelectorAll('div[class*="checkbox"], .ant-checkbox-wrapper, div[role="checkbox"]');
                        if (clickableElements.length > 0) {
                            clickableElements[0].click();
                            console.log('Fallback select all clicked');
                        }
                    }
                    
                    console.log('Select all process completed');
                })();
            """)
            
            # NO DELAY - proceed immediately to add to bag
            print("🛒 Add to bag...")
            self.checkout_driver.execute_script("""
                // Immediate single box add to bag
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
            
            # Small wait to ensure ADD TO BAG completes
            time.sleep(0.5)  # Wait for add to bag to register
            
            # 4. Go to cart immediately with optimized timing
            print("🛒 Going to cart...")
            
            # ULTRA AGGRESSIVE APPROACH: Start monitoring for select all on CURRENT page
            # This will make the select all process lightning fast
            self.checkout_driver.execute_script("""
                // Pre-load select all monitoring on current page
                window.__selectAllPreloaded = true;
                console.log('Select all monitoring pre-loaded for ultra-fast performance');
            """)
            
            # AGGRESSIVE APPROACH: Start trying to click select all BEFORE page loads
            self.checkout_driver.execute_script("""
                // Start monitoring for select all IMMEDIATELY
                window.__selectAllClicked = false;
                
                // Function to try clicking select all
                function trySelectAll() {
                    if (window.__selectAllClicked) return;
                    
                    const selectAllSelectors = [
                        'div.index_checkbox__w_166',
                        '.ant-checkbox-wrapper',
                        'div[class*="checkbox"]',
                        'input[type="checkbox"]',
                        '.ant-checkbox'
                    ];
                    
                    for (let selector of selectAllSelectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            if (element.offsetParent !== null && !element.disabled) {
                                element.click();
                                console.log('Select all clicked early using selector:', selector);
                                window.__selectAllClicked = true;
                                return true;
                            }
                        }
                    }
                    return false;
                }
                
                // Try immediately
                trySelectAll();
                
                // Set up continuous monitoring
                const observer = new MutationObserver(() => {
                    if (!window.__selectAllClicked) {
                        trySelectAll();
                    }
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
                
                // Also try with polling - ULTRA FAST
                const pollInterval = setInterval(() => {
                    if (trySelectAll() || window.__selectAllClicked) {
                        clearInterval(pollInterval);
                        observer.disconnect();
                    }
                }, 5); // Check every 5ms for maximum speed
                
                // Clean up after 2 seconds
                setTimeout(() => {
                    clearInterval(pollInterval);
                    observer.disconnect();
                }, 2000);
            """)
            
            # Navigate to cart AFTER setting up the monitoring
            self.checkout_driver.get("https://www.popmart.com/ca/largeShoppingCart")
            
            # 5. ULTRA FAST select all and checkout - additional attempt if needed
            print("✅ Ultra-fast select all...")
            self.checkout_driver.execute_script("""
                // Step 1: Click select all if not already clicked
                (function() {
                    if (window.__selectAllClicked) {
                        console.log('Select all already clicked, skipping...');
                        return;
                    }
                    // The REAL select all button is usually a div with checkbox-like behavior
                    // Try the most common selectors in order of likelihood
                    const selectAllSelectors = [
                        'div.index_checkbox__w_166',  // Main select all div
                        '.ant-checkbox-wrapper',       // Ant Design checkbox wrapper
                        'div[class*="checkbox"]',     // Any div with checkbox in class
                        'input[type="checkbox"]',     // Actual checkbox input
                        '.ant-checkbox'               // Ant Design checkbox class
                    ];
                    
                    let selectAllClicked = false;
                    
                    // First, try to find and click the select all button
                    for (let selector of selectAllSelectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            // Check if this looks like a select all button
                            if (element.offsetParent !== null && !element.disabled) {
                                // Click it immediately
                                element.click();
                                console.log('Select all clicked using selector:', selector);
                                selectAllClicked = true;
                                break;
                            }
                        }
                        if (selectAllClicked) break;
                    }
                    
                    // If still not clicked, try clicking ALL checkboxes
                    if (!selectAllClicked) {
                        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                        if (allCheckboxes.length > 0) {
                            allCheckboxes.forEach((cb, index) => {
                                if (!cb.checked && cb.offsetParent !== null) {
                                    cb.click();
                                    console.log('Individual checkbox clicked:', index);
                                }
                            });
                            selectAllClicked = true;
                        }
                    }
                    
                    // Final fallback: click any clickable element that might be select all
                    if (!selectAllClicked) {
                        const clickableElements = document.querySelectorAll('div[class*="checkbox"], .ant-checkbox-wrapper, div[role="checkbox"]');
                        if (clickableElements.length > 0) {
                            clickableElements[0].click();
                            console.log('Fallback select all clicked');
                        }
                    }
                    
                    // AGGRESSIVE APPROACH: Continuous monitoring for select all elements
                    if (!selectAllClicked) {
                        console.log('Setting up continuous monitoring for select all...');
                        
                        const observer = new MutationObserver((mutations) => {
                            for (let mutation of mutations) {
                                if (mutation.type === 'childList') {
                                    // Check newly added nodes
                                    mutation.addedNodes.forEach(node => {
                                        if (node.nodeType === 1) { // Element node
                                            // Look for select all in new elements
                                            for (let selector of selectAllSelectors) {
                                                const newElements = node.querySelectorAll ? node.querySelectorAll(selector) : [];
                                                if (node.matches && node.matches(selector)) {
                                                    newElements.push(node);
                                                }
                                                
                                                for (let element of newElements) {
                                                    if (element.offsetParent !== null && !element.disabled && !selectAllClicked) {
                                                        element.click();
                                                        console.log('Select all found and clicked via monitoring!');
                                                        selectAllClicked = true;
                                                        observer.disconnect();
                                                        return;
                                                    }
                                                }
                                            }
                                        }
                                    });
                                }
                            }
                        });
                        
                        // Start observing for new elements
                        observer.observe(document.body, {
                            childList: true,
                            subtree: true
                        });
                        
                        // Also try aggressive polling as backup
                        let attempts = 0;
                        const maxAttempts = 20;
                        const pollInterval = setInterval(() => {
                            attempts++;
                            
                            // Try all selectors again
                            for (let selector of selectAllSelectors) {
                                const elements = document.querySelectorAll(selector);
                                for (let element of elements) {
                                    if (element.offsetParent !== null && !element.disabled && !selectAllClicked) {
                                        element.click();
                                        console.log('Select all clicked via polling on attempt', attempts);
                                        selectAllClicked = true;
                                        clearInterval(pollInterval);
                                        observer.disconnect();
                                        return;
                                    }
                                }
                            }
                            
                            if (attempts >= maxAttempts) {
                                clearInterval(pollInterval);
                                observer.disconnect();
                                console.log('Select all polling stopped after', maxAttempts, 'attempts');
                            }
                        }, 25); // Check every 25ms for maximum speed
                    }
                    
                    console.log('Select all process completed');
                })();
            """)
            
            # NO DELAY - proceed immediately to checkout
            print("🚀 Ultra-fast checkout button...")
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
        """Super quick checkout for regular products - gets you to payment in seconds"""
        if not self.auto_checkout:
            return True
            
        try:
            print(f"\n⚡ ULTRA-FAST CHECKOUT: {product_info['product_name']}")
            start_time = time.time()
            
            # 1. Go directly to product page in checkout browser
            self.checkout_driver.get(product_info['url'])
            # NO DELAY - proceed immediately to add to bag
            
            # 2. Select whole set if preferred, then add to bag - ULTRA FAST
            if self.prefer_whole_set:
                print("📦 Selecting whole set...")
                self.checkout_driver.execute_script("""
                    // Immediate execution - select whole set first
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
                        
                        // Immediately add to bag after selection - NO DELAY
                        const buttons = document.querySelectorAll('div[class*="index_usBtn__"], button');
                        for (let btn of buttons) {
                            if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                                btn.click();
                                return;
                            }
                        }
                        
                        // AGGRESSIVE APPROACH: Continuous monitoring for ADD TO BAG button
                        if (!document.querySelector('div[class*="index_usBtn__"]')) {
                            console.log('Setting up continuous monitoring for ADD TO BAG...');
                            
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
                    // Immediate single box add to bag - NO DELAY
                    (function() {
                        const buttons = document.querySelectorAll('div[class*="index_usBtn__"], button');
                        for (let btn of buttons) {
                            if (btn.textContent.toUpperCase().includes('ADD TO BAG')) {
                                btn.click();
                                return;
                            }
                        }
                        
                        // AGGRESSIVE APPROACH: Continuous monitoring for ADD TO BAG button
                        if (!document.querySelector('div[class*="index_usBtn__"]')) {
                            console.log('Setting up continuous monitoring for ADD TO BAG...');
                            
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
            time.sleep(0.5)  # Wait for add to bag to register
            
            # 3. Go to cart immediately with optimized timing
            print("🛒 Going to cart...")
            
            # ULTRA AGGRESSIVE APPROACH: Start monitoring for select all on CURRENT page
            # This will make the select all process lightning fast
            self.checkout_driver.execute_script("""
                // Pre-load select all monitoring on current page
                window.__selectAllPreloaded = true;
                console.log('Select all monitoring pre-loaded for ultra-fast performance');
            """)
            
            # AGGRESSIVE APPROACH: Start trying to click select all BEFORE page loads
            self.checkout_driver.execute_script("""
                // Start monitoring for select all IMMEDIATELY
                window.__selectAllClicked = false;
                
                // Function to try clicking select all
                function trySelectAll() {
                    if (window.__selectAllClicked) return;
                    
                    const selectAllSelectors = [
                        'div.index_checkbox__w_166',
                        '.ant-checkbox-wrapper',
                        'div[class*="checkbox"]',
                        'input[type="checkbox"]',
                        '.ant-checkbox'
                    ];
                    
                    for (let selector of selectAllSelectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            if (element.offsetParent !== null && !element.disabled) {
                                element.click();
                                console.log('Select all clicked early using selector:', selector);
                                window.__selectAllClicked = true;
                                return true;
                            }
                        }
                    }
                    return false;
                }
                
                // Try immediately
                trySelectAll();
                
                // Set up continuous monitoring
                const observer = new MutationObserver(() => {
                    if (!window.__selectAllClicked) {
                        trySelectAll();
                    }
                });
                
                observer.observe(document.body, {
                    childList: true,
                    subtree: true
                });
                
                // Also try with polling - ULTRA FAST
                const pollInterval = setInterval(() => {
                    if (trySelectAll() || window.__selectAllClicked) {
                        clearInterval(pollInterval);
                        observer.disconnect();
                    }
                }, 5); // Check every 5ms for maximum speed
                
                // Clean up after 2 seconds
                setTimeout(() => {
                    clearInterval(pollInterval);
                    observer.disconnect();
                }, 2000);
            """)
            
            # Navigate to cart AFTER setting up the monitoring
            self.checkout_driver.get("https://www.popmart.com/ca/largeShoppingCart")
            
            # 4. ULTRA FAST select all and checkout - additional attempt if needed
            print("✅ Ultra-fast select all...")
            self.checkout_driver.execute_script("""
                // Step 1: Click select all if not already clicked
                (function() {
                    if (window.__selectAllClicked) {
                        console.log('Select all already clicked, skipping...');
                        return;
                    }
                    // The REAL select all button is usually a div with checkbox-like behavior
                    // Try the most common selectors in order of likelihood
                    const selectAllSelectors = [
                        'div.index_checkbox__w_166',  // Main select all div
                        '.ant-checkbox-wrapper',       // Ant Design checkbox wrapper
                        'div[class*="checkbox"]',     // Any div with checkbox in class
                        'input[type="checkbox"]',     // Actual checkbox input
                        '.ant-checkbox'               // Ant Design checkbox class
                    ];
                    
                    let selectAllClicked = false;
                    
                    // First, try to find and click the select all button
                    for (let selector of selectAllSelectors) {
                        const elements = document.querySelectorAll(selector);
                        for (let element of elements) {
                            // Check if this looks like a select all button
                            if (element.offsetParent !== null && !element.disabled) {
                                // Click it immediately
                                element.click();
                                console.log('Select all clicked using selector:', selector);
                                selectAllClicked = true;
                                break;
                            }
                        }
                        if (selectAllClicked) break;
                    }
                    
                    // If still not clicked, try clicking ALL checkboxes
                    if (!selectAllClicked) {
                        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
                        if (allCheckboxes.length > 0) {
                            allCheckboxes.forEach((cb, index) => {
                                if (!cb.checked && cb.offsetParent !== null) {
                                    cb.click();
                                    console.log('Individual checkbox clicked:', index);
                                }
                            });
                            selectAllClicked = true;
                        }
                    }
                    
                    // Final fallback: click any clickable element that might be select all
                    if (!selectAllClicked) {
                        const clickableElements = document.querySelectorAll('div[class*="checkbox"], .ant-checkbox-wrapper, div[role="checkbox"]');
                        if (clickableElements.length > 0) {
                            clickableElements[0].click();
                            console.log('Fallback select all clicked');
                        }
                    }
                    
                    // AGGRESSIVE APPROACH: Continuous monitoring for select all elements
                    if (!selectAllClicked) {
                        console.log('Setting up continuous monitoring for select all...');
                        
                        const observer = new MutationObserver((mutations) => {
                            for (let mutation of mutations) {
                                if (mutation.type === 'childList') {
                                    // Check newly added nodes
                                    mutation.addedNodes.forEach(node => {
                                        if (node.nodeType === 1) { // Element node
                                            // Look for select all in new elements
                                            for (let selector of selectAllSelectors) {
                                                const newElements = node.querySelectorAll ? node.querySelectorAll(selector) : [];
                                                if (node.matches && node.matches(selector)) {
                                                    newElements.push(node);
                                                }
                                                
                                                for (let element of newElements) {
                                                    if (element.offsetParent !== null && !element.disabled && !selectAllClicked) {
                                                        element.click();
                                                        console.log('Select all found and clicked via monitoring!');
                                                        selectAllClicked = true;
                                                        observer.disconnect();
                                                        return;
                                                    }
                                                }
                                            }
                                        }
                                    });
                                }
                            }
                        });
                        
                        // Start observing for new elements
                        observer.observe(document.body, {
                            childList: true,
                            subtree: true
                        });
                        
                        // Also try aggressive polling as backup
                        let attempts = 0;
                        const maxAttempts = 20;
                        const pollInterval = setInterval(() => {
                            attempts++;
                            
                            // Try all selectors again
                            for (let selector of selectAllSelectors) {
                                const elements = document.querySelectorAll(selector);
                                for (let element of elements) {
                                    if (element.offsetParent !== null && !element.disabled && !selectAllClicked) {
                                        element.click();
                                        console.log('Select all clicked via polling on attempt', attempts);
                                        selectAllClicked = true;
                                        clearInterval(pollInterval);
                                        observer.disconnect();
                                        return;
                                    }
                                }
                            }
                            
                            if (attempts >= maxAttempts) {
                                clearInterval(pollInterval);
                                observer.disconnect();
                                console.log('Select all polling stopped after', maxAttempts, 'attempts');
                            }
                        }, 25); // Check every 25ms for maximum speed
                    }
                    
                    console.log('Select all process completed');
                })();
            """)
            
            # NO DELAY - proceed immediately to checkout button
            print("🚀 Ultra-fast checkout button...")
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
            print("• Bot will stop monitoring after getting the product")
            print("="*60)
            
            print("\n✅ Checkout completed! Bot will stop monitoring.")
            print("💡 You can complete payment in the checkout browser")
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
            
            # Add to queue for checkout
            self.stock_queue.put(product_info)
            
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
                time.sleep(0.8)  # Much faster navigation
                
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