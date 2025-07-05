# main.py
"""
PopMart Professional Checkout Bot
Automated monitoring and purchasing system for PopMart collectibles
Supports multiple characters, real-time stock monitoring, and secure checkout
"""

import json
import random
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

try:
    from seleniumbase import BaseCase
    from seleniumbase import SB

    SELENIUMBASE_AVAILABLE = True
except ImportError:
    SELENIUMBASE_AVAILABLE = False
    print("❌ SeleniumBase not available. Install with: pip install seleniumbase")

try:
    import config
except ImportError:
    print("❌ config.py not found. Please create it with your credentials.")
    config = None


class PopMartCheckoutBot:
    def __init__(self):
        self.sb = None
        self.logged_in = False
        self.monitoring = False
        self.session_start_time = datetime.now()
        self.total_checks = 0
        self.products_found = 0

        # PopMart search URLs for different character collections
        self.character_collections = {
            'Space Molly': 'https://www.popmart.com/ca/search/SPACE%20MOLLY',
            'The Monsters': 'https://www.popmart.com/ca/search/THE%20MONSTERS',
            'Molly': 'https://www.popmart.com/ca/search/MOLLY',
            'Twinkle Twinkle': 'https://www.popmart.com/ca/search/TWINKLE%20TWINKLE',
            'LABUBU': 'https://www.popmart.com/ca/search/LABUBU'
        }

        # Load configuration from config file
        self.target_character = getattr(config, 'CHARACTER', 'Space Molly')
        self.auto_checkout = getattr(config, 'AUTO_CHECKOUT', False)

        # Validate character exists in our supported list
        if self.target_character not in self.character_collections:
            print(f"⚠️  Warning: Character '{self.target_character}' not found")
            print(f"📋 Available: {list(self.character_collections.keys())}")
            self.target_character = 'Space Molly'

    def print_header(self):
        """Display startup banner with bot configuration"""
        print("\n" + "═" * 70)
        print("🤖 POPMART CHECKOUT BOT v2.0")
        print("═" * 70)
        print(f"🎯 Target Character: {self.target_character}")
        print(f"🛒 Mode: {'AUTO-CHECKOUT' if self.auto_checkout else 'MONITOR ONLY'}")
        print(f"🌐 Search URL: {self.character_collections[self.target_character]}")
        print(f"⏰ Started: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("═" * 70)

    def print_status_header(self, cycle_num):
        """Show current scan cycle information"""
        current_time = datetime.now()
        elapsed = current_time - self.session_start_time

        print(f"\n╔{'═' * 68}╗")
        print(
            f"║ 🔄 SCAN CYCLE #{cycle_num:03d} - {current_time.strftime('%H:%M:%S'):<20} Runtime: {str(elapsed).split('.')[0]:<10} ║")
        print(f"╚{'═' * 68}╝")

    def print_product_summary(self, products):
        """Display product discovery results"""
        print(f"\n📦 PRODUCT DISCOVERY SUMMARY")
        print(f"┌{'─' * 50}┐")
        print(f"│ Total Products Found: {len(products):<25} │")
        print(f"│ Search Method: Advanced Scroll + Pagination    │")
        print(f"│ Duplicate Removal: ✅ Enabled                │")
        print(f"└{'─' * 50}┘")

        if products:
            print(f"\n🔍 SAMPLE PRODUCTS:")
            for i, product in enumerate(products[:5], 1):
                name = product['name'][:45] + "..." if len(product['name']) > 45 else product['name']
                print(f"   {i:02d}. {name}")
            if len(products) > 5:
                print(f"   ... and {len(products) - 5} more products")

    def print_availability_check(self, current, total, product_name, available, price=0):
        """Show progress of individual product checks"""
        progress = "█" * (current * 20 // total) + "░" * (20 - current * 20 // total)
        percentage = (current * 100 // total)

        name_display = product_name[:35] + "..." if len(product_name) > 35 else product_name

        if available:
            status = f"✅ AVAILABLE - ${price:.2f}"
            print(f"   [{progress}] {percentage:3d}% │ {name_display:<38} │ {status}")
        else:
            status = "❌ OUT OF STOCK"
            print(f"   [{progress}] {percentage:3d}% │ {name_display:<38} │ {status}")

    def print_scan_results(self, available_products, total_products):
        """Display summary of scan results"""
        print(f"\n📊 SCAN RESULTS")
        print(f"┌{'─' * 68}┐")
        print(
            f"│ Products Scanned: {total_products:<10} │ Available: {len(available_products):<10} │ Out of Stock: {total_products - len(available_products):<8} │")
        print(f"└{'─' * 68}┘")

        if available_products:
            print(f"\n🟢 AVAILABLE PRODUCTS:")
            print(f"┌{'─' * 68}┐")
            for i, product in enumerate(available_products, 1):
                name = product['name'][:40] + "..." if len(product['name']) > 40 else product['name']
                print(f"│ {i:02d}. {name:<43} │ ${product['price']:.2f} │")
            print(f"└{'─' * 68}┘")
        else:
            print(f"\n🔴 NO PRODUCTS CURRENTLY AVAILABLE")

    def print_purchase_prompt(self, product_name, price, url):
        """Show purchase confirmation dialog"""
        print(f"\n{'🚨' * 25}")
        print(f"{'  🛒 PURCHASE OPPORTUNITY DETECTED!':^50}")
        print(f"{'🚨' * 25}")
        print(f"\n╔{'═' * 68}╗")
        print(f"║ 📦 Product: {product_name[:50]:<50} ║")
        print(f"║ 💰 Price: ${price:.2f} CAD{' ' * 42} ║")
        print(f"║ 🔗 URL: {url[:55]:<55} ║")
        print(f"╚{'═' * 68}╝")

    def print_next_check_countdown(self, seconds, mode):
        """Display countdown until next scan"""
        mode_text = "AUTO-CHECKOUT" if mode == "checkout" else "MONITOR"
        emoji = "🎯" if mode == "checkout" else "👀"

        print(f"\n{emoji} {mode_text} MODE - Next scan in {seconds} seconds...")
        print(f"{'─' * 50}")

    def setup_browser(self):
        """Initialize browser with appropriate settings"""
        if not SELENIUMBASE_AVAILABLE:
            print("❌ SeleniumBase required for checkout bot")
            return False

        try:
            self.sb = SB(
                uc=True,
                headed=True,
                browser="chrome",
                page_load_strategy="eager",
                disable_csp=True,
                disable_ws=True,
                block_images=False,
                user_data_dir="/tmp/popmart_bot",
            )
            return True
        except Exception as e:
            print(f"❌ Browser setup failed: {e}")
            return False

    def start_session(self):
        """Main session handler"""
        if not self.setup_browser():
            return False

        try:
            with self.sb as sb:
                self.driver = sb

                # Browser fingerprint modifications
                sb.execute_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                    });
                """)

                return self.run_bot_sequence()

        except Exception as e:
            print(f"❌ Session failed: {e}")
            return False

    def run_bot_sequence(self):
        """Execute main bot workflow"""
        try:
            self.print_header()

            # User authentication
            if not self.login():
                return False

            # Execute monitoring based on config
            if self.auto_checkout:
                self.monitor_and_checkout()
            else:
                self.monitor_products()

            return True

        except KeyboardInterrupt:
            print(f"\n\n🛑 Bot stopped by user")
            self.print_session_summary()
            return False

    def print_session_summary(self):
        """Display final session statistics"""
        end_time = datetime.now()
        duration = end_time - self.session_start_time

        print(f"\n📈 SESSION SUMMARY")
        print(f"┌{'─' * 50}┐")
        print(f"│ Session Duration: {str(duration).split('.')[0]:<30} │")
        print(f"│ Total Scan Cycles: {self.total_checks:<29} │")
        print(f"│ Products Monitored: {self.products_found:<28} │")
        print(f"│ Mode: {'AUTO-CHECKOUT' if self.auto_checkout else 'MONITOR ONLY':<36} │")
        print(f"└{'─' * 50}┘")

    def login(self):
        """Handle user authentication"""
        if not config:
            print("❌ No config file found")
            return False

        sb = self.driver

        try:
            print("🔑 Authenticating...")

            # Check existing session
            sb.open("https://www.popmart.com/ca/account")
            sb.sleep(2)

            current_url = sb.get_current_url()
            if "account" in current_url.lower() and "login" not in current_url.lower():
                print("✅ Already authenticated!")
                self.logged_in = True
                return True

            # Navigate to login form
            sb.open("https://www.popmart.com/ca/user/login")
            sb.sleep(3)

            # Handle initial popups
            self.accept_terms()
            self.handle_popups()

            # Check if form is needed
            email_selector = 'input[placeholder="Enter your e-mail address"]'
            if not sb.is_element_present(email_selector):
                print("✅ Already authenticated!")
                self.logged_in = True
                return True

            # Fill login form
            print("📧 Entering credentials...")
            sb.wait_for_element(email_selector, timeout=10)
            sb.type(email_selector, config.POPMART_EMAIL)
            sb.sleep(1)

            continue_btn = 'button.ant-btn.ant-btn-primary.index_loginButton__O6r8l'
            sb.click(continue_btn)
            sb.sleep(3)

            password_selector = 'input[placeholder="Enter your password"]'
            sb.wait_for_element(password_selector, timeout=10)
            sb.type(password_selector, config.POPMART_PASSWORD)
            sb.sleep(1)

            signin_btn = 'button[type="submit"].ant-btn.ant-btn-primary.index_loginButton__O6r8l'
            sb.click(signin_btn)
            sb.sleep(5)

            # Check login success
            current_url = sb.get_current_url()
            if "login" not in current_url.lower():
                print("✅ Authentication successful!")
                self.logged_in = True
                self.save_login_session()
                return True
            else:
                print("❌ Authentication failed")
                return False

        except Exception as e:
            print(f"❌ Login error: {e}")
            return False

    def accept_terms(self):
        """Accept terms of service if presented"""
        sb = self.driver
        terms_selectors = [
            'button:contains("Accept")', 'button:contains("ACCEPT")',
            'button:contains("I Accept")', 'button:contains("I Agree")',
            'button:contains("Agree")', 'button:contains("OK")',
            'button:contains("Continue")', '[class*="accept"]',
            '[class*="agree"]', '[id*="accept"]', '[id*="agree"]'
        ]

        for selector in terms_selectors:
            try:
                if sb.is_element_present(selector):
                    sb.click(selector)
                    sb.sleep(2)
                    break
            except:
                continue

    def handle_popups(self):
        """Close any modal dialogs or popups"""
        sb = self.driver
        popup_selectors = [
            "div:contains('OK')", "button:contains('Accept')",
            "button:contains('ACCEPT')", ".modal .close",
            ".popup .close", '[aria-label="Close"]',
            '.close-button', '.popup-close'
        ]

        for selector in popup_selectors:
            try:
                if sb.is_element_present(selector):
                    sb.click(selector)
                    sb.sleep(1)
            except:
                continue

    def save_login_session(self):
        """Store session cookies for future use"""
        try:
            cookies = self.driver.get_cookies()
            with open('popmart_session.json', 'w') as f:
                json.dump(cookies, f)
        except Exception as e:
            pass

    def monitor_products(self):
        """Monitor products without purchasing (view-only mode)"""
        if self.target_character not in self.character_collections:
            print("❌ Invalid character selection")
            return

        search_url = self.character_collections[self.target_character]
        self.monitoring = True
        cycle_count = 0

        while self.monitoring:
            try:
                cycle_count += 1
                self.total_checks = cycle_count

                self.print_status_header(cycle_count)

                # Fetch current product list
                products = self.get_collection_products(search_url)
                self.products_found = len(products)

                if not products:
                    print("⚠️  No products found - retrying in 30 seconds...")
                    time.sleep(30)
                    continue

                self.print_product_summary(products)

                # Check stock status for each product
                print(f"\n🔍 CHECKING AVAILABILITY...")
                available_products = []

                for i, product in enumerate(products, 1):
                    stock_status = self.check_product_stock_quick(product)

                    if stock_status['available']:
                        available_products.append({
                            'name': product['name'],
                            'price': stock_status['price'],
                            'url': product['url']
                        })

                    self.print_availability_check(i, len(products), product['name'],
                                                  stock_status['available'], stock_status['price'])

                    time.sleep(random.uniform(1, 2))

                self.print_scan_results(available_products, len(products))
                self.print_next_check_countdown(15, "monitor")
                time.sleep(15)

            except KeyboardInterrupt:
                self.monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitor error: {e}")
                time.sleep(10)

    def monitor_and_checkout(self):
        """Monitor products with automatic purchasing enabled"""
        if self.target_character not in self.character_collections:
            print("❌ Invalid character selection")
            return

        search_url = self.character_collections[self.target_character]
        self.monitoring = True
        cycle_count = 0

        while self.monitoring:
            try:
                cycle_count += 1
                self.total_checks = cycle_count

                self.print_status_header(cycle_count)

                # Get current product listings
                products = self.get_collection_products(search_url)
                self.products_found = len(products)

                if not products:
                    print("⚠️  No products found - retrying in 15 seconds...")
                    time.sleep(15)
                    continue

                self.print_product_summary(products)

                # Check each product for availability
                print(f"\n🔍 CHECKING AVAILABILITY...")
                available_products = []

                for i, product in enumerate(products, 1):
                    stock_status = self.check_product_stock_quick(product)

                    if stock_status['available']:
                        available_products.append({
                            'name': product['name'],
                            'price': stock_status['price'],
                            'url': product['url']
                        })

                        self.print_availability_check(i, len(products), product['name'],
                                                      stock_status['available'], stock_status['price'])

                        # Show purchase opportunity
                        self.print_purchase_prompt(product['name'], stock_status['price'], product['url'])

                        if self.ask_user_confirmation(product['name'], stock_status['price'], product['url']):
                            print("\n🚀 Initiating checkout process...")

                            if self.checkout_product_direct(product['url']):
                                print("\n🎉 CHECKOUT SUCCESSFUL!")
                                print("✅ Order completed - stopping bot")
                                self.monitoring = False
                                return True
                            else:
                                print("❌ Checkout failed - continuing monitoring...")
                        else:
                            print("⏭️  Skipping - continuing monitoring...")
                    else:
                        self.print_availability_check(i, len(products), product['name'],
                                                      stock_status['available'], stock_status['price'])

                    time.sleep(random.uniform(1, 2))

                self.print_scan_results(available_products, len(products))
                self.print_next_check_countdown(10, "checkout")
                time.sleep(10)

            except KeyboardInterrupt:
                self.monitoring = False
                break
            except Exception as e:
                print(f"❌ Auto-checkout error: {e}")
                time.sleep(10)

    def ask_user_confirmation(self, product_name, price, product_url):
        """Get user confirmation for purchase"""
        while True:
            choice = input(f"\n💳 Purchase this product for ${price:.2f}? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no")

    def get_collection_products(self, search_url):
        """Extract product information from search results"""
        sb = self.driver

        try:
            sb.open(search_url)
            sb.sleep(3)
            self.handle_popups()

            # Scroll through all available products
            print("🔄 Loading products (Advanced Scroll + Pagination)...")
            previous_height = 0
            scroll_attempts = 0
            max_scrolls = 40

            while scroll_attempts < max_scrolls:
                sb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sb.sleep(2)

                new_height = sb.execute_script("return document.body.scrollHeight")

                if new_height == previous_height:
                    # Look for load more buttons
                    load_more_selectors = [
                        'button:contains("Load More")', 'button:contains("Show More")',
                        'button:contains("更多")', 'button:contains("查看更多")',
                        '.load-more', '.show-more', '[class*="load-more"]',
                        '[class*="show-more"]', '[class*="more"]'
                    ]

                    clicked = False
                    for selector in load_more_selectors:
                        try:
                            if sb.is_element_present(selector):
                                sb.click(selector)
                                sb.sleep(3)
                                clicked = True
                                break
                        except:
                            continue

                    if not clicked:
                        # Try keyboard navigation as fallback
                        try:
                            sb.press_keys("body", "PAGE_DOWN")
                            sb.sleep(1)
                            sb.press_keys("body", "END")
                            sb.sleep(2)
                        except:
                            pass

                        new_height_after = sb.execute_script("return document.body.scrollHeight")
                        if new_height_after == new_height:
                            break
                        else:
                            new_height = new_height_after

                previous_height = new_height
                scroll_attempts += 1

            # Extract product data
            products = []

            # Primary method: find product links
            try:
                product_links = sb.find_elements('a[href*="/products/"]')
                for link in product_links:
                    try:
                        url = link.get_attribute('href')
                        if not url or '/products/' not in url:
                            continue

                        if url.startswith('/'):
                            url = 'https://www.popmart.com' + url

                        name = link.text.strip()
                        if not name:
                            try:
                                parent = link.find_element("xpath", "..")
                                name = parent.text.strip().split('\n')[0].strip()
                            except:
                                pass

                        if not name:
                            try:
                                name = url.split('/')[-1].replace('-', ' ').title()
                            except:
                                name = "Unknown Product"

                        if name and len(name) > 0:
                            products.append({'name': name, 'url': url})
                    except:
                        continue
            except:
                pass

            # Secondary method: search within product containers
            if len(products) < 10:
                container_selectors = [
                    'div[class*="product"]', 'div[class*="item"]',
                    'div[class*="card"]', 'div[class*="goods"]',
                    'li[class*="product"]', 'li[class*="item"]',
                    '[data-testid*="product"]', '.product-card',
                    '.item-card', '.goods-card'
                ]

                for selector in container_selectors:
                    try:
                        if sb.is_element_present(selector):
                            elements = sb.find_elements(selector)
                            for element in elements:
                                try:
                                    link = element.find_element("css selector", 'a[href*="/products/"]')
                                    url = link.get_attribute('href')

                                    if not url or '/products/' not in url:
                                        continue

                                    if url.startswith('/'):
                                        url = 'https://www.popmart.com' + url

                                    name = ""
                                    name_selectors = [
                                        'h3', 'h4', 'h5', 'h6', '.title', '.name',
                                        '.product-name', '[class*="title"]', '[class*="name"]'
                                    ]

                                    for name_sel in name_selectors:
                                        try:
                                            name_elem = element.find_element("css selector", name_sel)
                                            if name_elem and name_elem.text.strip():
                                                name = name_elem.text.strip()
                                                break
                                        except:
                                            continue

                                    if not name:
                                        name = element.text.strip().split('\n')[0].strip()

                                    if not name:
                                        try:
                                            name = url.split('/')[-1].replace('-', ' ').title()
                                        except:
                                            name = "Unknown Product"

                                    if name and len(name) > 0:
                                        products.append({'name': name, 'url': url})
                                except:
                                    continue

                            if products:
                                break
                    except:
                        continue

            # Remove duplicate entries
            unique_products = []
            seen_urls = set()
            for product in products:
                if product['url'] not in seen_urls:
                    unique_products.append(product)
                    seen_urls.add(product['url'])

            return unique_products

        except Exception as e:
            print(f"❌ Error getting products: {e}")
            return []

    def check_product_stock_quick(self, product):
        """Verify product availability and extract pricing"""
        sb = self.driver

        try:
            sb.open(product['url'])
            sb.sleep(2)

            # Clear any modal dialogs
            popup_selectors = [
                'button:contains("OK")', 'button:contains("Accept")',
                'button:contains("确定")', 'button:contains("接受")',
                '.close-button', '.popup-close', '[aria-label="Close"]'
            ]

            for selector in popup_selectors:
                try:
                    if sb.is_element_present(selector):
                        sb.click(selector)
                        sb.sleep(1)
                        break
                except:
                    continue

            # Check if product is available
            available = True

            # Method 1: Search page source for out-of-stock indicators
            out_of_stock_texts = [
                "OUT OF STOCK", "SOLD OUT", "UNAVAILABLE", "COMING SOON",
                "库存不足", "售罄", "即将上市", "Not Available", "Temporarily Out of Stock"
            ]

            page_text = sb.get_page_source().upper()
            for text in out_of_stock_texts:
                if text in page_text:
                    available = False
                    break

            # Method 2: Check add to cart button status
            if available:
                cart_selectors = [
                    'button:contains("ADD TO CART")', 'button:contains("Add to Cart")',
                    'button:contains("BUY NOW")', 'button:contains("加入购物车")',
                    'button:contains("立即购买")', 'button[class*="add-to-cart"]',
                    'button[class*="buy-now"]', 'button[class*="cart"]',
                    'button[id*="add-to-cart"]', 'button[id*="buy-now"]'
                ]

                cart_button_found = False
                for selector in cart_selectors:
                    try:
                        if sb.is_element_present(selector):
                            element = sb.find_element(selector)
                            if element and element.is_enabled() and element.is_displayed():
                                button_text = element.text.upper()
                                if "OUT OF STOCK" not in button_text and "SOLD OUT" not in button_text:
                                    cart_button_found = True
                                    break
                    except:
                        continue

                if not cart_button_found:
                    available = False

            # Method 3: Check for disabled purchase buttons
            if available:
                disabled_selectors = [
                    'button[disabled]', 'button[class*="disabled"]',
                    'button[class*="inactive"]', '.btn-disabled', '.button-disabled'
                ]

                for selector in disabled_selectors:
                    try:
                        if sb.is_element_present(selector):
                            element = sb.find_element(selector)
                            if "add" in element.text.lower() or "buy" in element.text.lower():
                                available = False
                                break
                    except:
                        continue

            # Extract product pricing
            price = 0.0
            price_selectors = [
                '[class*="price"]', '[class*="cost"]', '[class*="amount"]',
                'span:contains("$")', 'div:contains("$")',
                'span:contains("CAD")', 'div:contains("CAD")',
                '.product-price', '.item-price', '.goods-price'
            ]

            for selector in price_selectors:
                try:
                    if sb.is_element_present(selector):
                        price_elements = sb.find_elements(selector)
                        for price_elem in price_elements:
                            price_text = price_elem.text.strip()
                            if "$" in price_text or "CAD" in price_text:
                                price_match = re.search(r'(\d+\.?\d*)', price_text.replace(',', ''))
                                if price_match:
                                    price = float(price_match.group(1))
                                    break
                        if price > 0:
                            break
                except:
                    continue

            return {'available': available, 'price': price}

        except Exception as e:
            return {'available': False, 'price': 0.0}

    def checkout_product_direct(self, product_url):
        """Execute purchase workflow for specific product"""
        sb = self.driver

        try:
            print("🛒 Fast checkout initiated...")

            sb.open(product_url)
            sb.sleep(1)

            # Handle any popups
            popup_selectors = [
                'button:contains("OK")', 'button:contains("Accept")', '.close-button'
            ]

            for selector in popup_selectors:
                try:
                    if sb.is_element_present(selector):
                        sb.click(selector)
                        break
                except:
                    continue

            # Add product to cart
            print("🛍️ Adding to cart...")
            cart_selectors = [
                'button:contains("ADD TO CART")',
                'button:contains("Add to Cart")',
                'button:contains("BUY NOW")'
            ]

            added = False
            for selector in cart_selectors:
                try:
                    if sb.is_element_present(selector):
                        sb.click(selector)
                        print("✅ Added to cart!")
                        added = True
                        break
                except:
                    continue

            if not added:
                print("❌ Could not add to cart")
                return False

            sb.sleep(1)

            # Navigate to shopping cart
            print("🛒 Proceeding to cart...")
            sb.open("https://www.popmart.com/ca/cart")
            sb.sleep(1)

            return self.complete_checkout_fast()

        except Exception as e:
            print(f"❌ Checkout error: {e}")
            return False

    def complete_checkout_fast(self):
        """Process checkout form and payment"""
        sb = self.driver

        try:
            print("💳 Processing checkout...")

            # Find checkout button
            checkout_selectors = [
                'button:contains("CHECKOUT")',
                'button:contains("PROCEED")',
                'a:contains("CHECKOUT")'
            ]

            for selector in checkout_selectors:
                try:
                    if sb.is_element_present(selector):
                        sb.click(selector)
                        break
                except:
                    continue

            sb.sleep(1)

            # Fill required forms
            self.fill_forms_fast()

            # Submit order
            return self.finalize_order_fast()

        except Exception as e:
            print(f"❌ Checkout error: {e}")
            return False

    def fill_forms_fast(self):
        """Populate checkout forms with user data"""
        sb = self.driver

        if not config:
            return

        # Define form field mappings
        fields = {
            'first_name': [config.FIRST_NAME, ['input[name*="first"]', 'input[placeholder*="First"]']],
            'last_name': [config.LAST_NAME, ['input[name*="last"]', 'input[placeholder*="Last"]']],
            'address': [config.ADDRESS, ['input[name*="address"]', 'input[placeholder*="Address"]']],
            'city': [config.CITY, ['input[name*="city"]', 'input[placeholder*="City"]']],
            'zip': [config.ZIP_CODE, ['input[name*="zip"]', 'input[name*="postal"]']],
            'phone': [config.PHONE_NUMBER, ['input[name*="phone"]', 'input[placeholder*="Phone"]']],
            'card_number': [config.CREDIT_CARD_NUMBER, ['input[name*="card"]', 'input[placeholder*="Card"]']],
            'expiry': [config.EXPIRATION_DATE, ['input[name*="expir"]', 'input[placeholder*="MM/YY"]']],
            'cvv': [config.SECURITY_CODE_CVV, ['input[name*="cvv"]', 'input[name*="security"]']],
            'name_on_card': [config.NAME_ON_CARD, ['input[name*="cardholder"]', 'input[placeholder*="Name"]']]
        }

        for field_name, (value, selectors) in fields.items():
            if value:
                for selector in selectors:
                    try:
                        if sb.is_element_present(selector):
                            sb.clear(selector)
                            sb.type(selector, value)
                            break
                    except:
                        continue

    def finalize_order_fast(self):
        """Submit final order"""
        sb = self.driver

        print("🎯 Placing order...")

        # Look for order submission buttons
        order_selectors = [
            'button:contains("PLACE ORDER")',
            'button:contains("COMPLETE ORDER")',
            'button:contains("BUY NOW")',
            'button:contains("PURCHASE")'
        ]

        for selector in order_selectors:
            try:
                if sb.is_element_present(selector):
                    print("🚀 Submitting order...")
                    sb.click(selector)
                    sb.sleep(2)

                    # Look for success confirmation
                    success_selectors = [
                        ':contains("SUCCESS")',
                        ':contains("CONFIRMED")',
                        ':contains("ORDER PLACED")',
                        ':contains("THANK YOU")'
                    ]

                    for indicator in success_selectors:
                        if sb.is_element_present(indicator):
                            print("🎉 Order successful!")
                            return True

                    print("✅ Order submitted successfully")
                    return True
            except:
                continue

        print("⚠️ Could not locate order button")
        return False


def main():
    """Entry point for the application"""
    print("🚀 Initializing PopMart Checkout Bot...")

    if not SELENIUMBASE_AVAILABLE:
        print("❌ SeleniumBase required. Install with: pip install seleniumbase")
        return

    if not config:
        print("❌ config.py required with credentials")
        return

    bot = PopMartCheckoutBot()

    try:
        bot.start_session()
    except KeyboardInterrupt:
        print("\n🛑 Bot terminated by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()