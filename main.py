# popmart_bot.py
import time
import random
from seleniumbase import SB
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Import user-defined configuration
try:
    import config
except ImportError:
    print("ERROR: config.py file not found. Please create it and fill in your details.")
    exit()


def run_bot():
    """
    Main function to run the Pop Mart purchasing bot.
    """
    with SB(uc=True, proxy=config.PROXY, headless=False) as sb:
        try:
            # 1. Navigate to the product page
            print(f"Navigating to product page: {config.TARGET_PRODUCT_URL}")
            sb.open(config.TARGET_PRODUCT_URL)

            # 2. Wait for the product to be available and add to cart
            add_to_cart_button_selector = "button[data-aid='productAddToCart']"
            print("Waiting for 'Add to Cart' button to become available...")

            # Wait for up to 30 minutes (180 * 10 seconds)
            # This loop handles waiting for the drop
            sb.wait_for_element(add_to_cart_button_selector, timeout=1800)
            print("Product is available! Adding to cart...")
            sb.click(add_to_cart_button_selector)

            # 3. Wait for cart to update and proceed to checkout
            # The site may show a mini-cart, we need to go to the main checkout page.
            print("Proceeding to checkout...")
            time.sleep(1 + random.uniform(0.5, 1))  # Wait for mini-cart to appear

            # Using a direct navigation to checkout is often more reliable
            checkout_url = "https://www.popmart.com/ca/checkouts"
            sb.open(checkout_url)

            # 4. Fill out contact and shipping information
            print("Filling out shipping and contact information...")
            sb.wait_for_element('input[placeholder="Email"]', timeout=30)
            sb.type('input[placeholder="Email"]', config.EMAIL)
            sb.type('input[placeholder="First name"]', config.FIRST_NAME)
            sb.type('input[placeholder="Last name"]', config.LAST_NAME)
            sb.type('input[placeholder="Address"]', config.ADDRESS)
            if config.APARTMENT:
                sb.type('input[placeholder="Apartment, suite, etc. (optional)"]', config.APARTMENT)
            sb.type('input[placeholder="City"]', config.CITY)
            sb.type('input[placeholder="ZIP code"]', config.ZIP_CODE)

            print("Information form filled. Continuing to shipping.")
            sb.click('button:contains("Continue to shipping")')

            # 5. Select shipping method
            print("Selecting shipping method...")
            sb.wait_for_element('button:contains("Continue to payment")', timeout=30)
            sb.click('button:contains("Continue to payment")')

            # 6. Fill out payment information
            # This is the most critical and complex part, as payment fields are in a secure iframe.
            print("Switching to payment iframe...")
            sb.wait_for_frame("iframe[title*='Secure payment']", timeout=30)

            print("Filling credit card details...")
            # Card Number
            sb.type('input[name="number"]', config.CREDIT_CARD_NUMBER)

            # Name on Card
            sb.type('input[name="name"]', config.NAME_ON_CARD)

            # Expiration Date
            sb.type('input[name="expiry"]', config.EXPIRATION_DATE)

            # CVV
            sb.type('input[name="verification_value"]', config.SECURITY_CODE_CVV)

            # Switch back to the main page content
            sb.switch_to_default_content()
            print("Payment details filled.")

            # 7. Finalize Purchase
            pay_now_button_selector = 'button:contains("Pay now")'
            print("Attempting to finalize purchase...")
            sb.wait_for_element(pay_now_button_selector, timeout=15)
            # sb.click(pay_now_button_selector)  # UNCOMMENT THIS LINE TO ACTUALLY PURCHASE

            print("=" * 40)
            print("BOT EXECUTION COMPLETED!")
            print("The 'Pay now' button was located. If it was uncommented, the purchase would have been attempted.")
            print("Please check the browser window for the result.")
            print("=" * 40)

        except (TimeoutException, NoSuchElementException) as e:
            print("\n" + "=" * 40)
            print("AN ERROR OCCURRED!")
            print(f"Reason: A required element was not found in time, or the page structure has changed.")
            print(f"Details: {e}")
            print("This could be due to the product selling out, a CAPTCHA, or a website update.")
            print("Please check the browser window for more details.")
            print("=" * 40)

        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

        finally:
            print("\nBot script has finished. The browser window will remain open for 5 minutes for inspection.")
            time.sleep(300)


if __name__ == "__main__":
    run_bot()

