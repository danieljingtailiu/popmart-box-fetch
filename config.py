# config.py
# Enhanced PopMart Bot Configuration

# --- LOGIN CREDENTIALS ---
# Your login details for the Pop Mart website.
# The bot will use these to sign in at the start.
POPMART_EMAIL = "johndoe@gmail.com"
POPMART_PASSWORD = "123456789"

# --- CHARACTER SELECTION ---
# Choose which character collection to monitor
# Available options: "Space Molly", "The Monsters", "Molly", "Twinkle Twinkle", "LABUBU"
CHARACTER = "Molly"

# --- AUTO-CHECKOUT SETTINGS ---
# Set to True to automatically purchase when products become available
# Set to False to only monitor and report availability
AUTO_CHECKOUT = True

# --- PRODUCT & URL SETTINGS ---
# Legacy settings - now handled by CHARACTER selection above
TARGET_PRODUCT_URL = "https://www.popmart.com/ca/search/SPACE%20MOLLY"  # Space Molly search
LOGIN_URL = "https://www.popmart.com/ca/account"


# --- SHIPPING & CONTACT INFORMATION ---
# Even though you are logged in, it's good to have these as a backup
# in case the site doesn't auto-fill correctly.
# The bot will try to skip filling these if they are already populated.
FIRST_NAME = "Bob"
LAST_NAME = "Builder"
ADDRESS = "SAMPLE"
APARTMENT = ""  # Leave as "" if not applicable
CITY = "SAMPLE"
STATE_PROVINCE = "SAMPLE"
ZIP_CODE = "SAMPLE"
COUNTRY = "Canada"
PHONE_NUMBER = "123456789"  # Optional, but recommended

# --- PAYMENT INFORMATION (CREDIT CARD) ---
# This is still required as payment info is rarely saved for security reasons.
# The bot will attempt to input this information into the secure payment iframe.
CREDIT_CARD_NUMBER = "1111222233334444"
NAME_ON_CARD = "Bob R Builder"
EXPIRATION_DATE = "1228"  # Format: MMYY, e.g., "1228" for December 2028
SECURITY_CODE_CVV = "123"

# --- ADVANCED SETTINGS ---
# Monitoring intervals (in seconds)
MONITOR_INTERVAL = 15  # Fast monitoring - every 15 seconds
AUTO_CHECKOUT_INTERVAL = 10  # Very fast auto-checkout - every 10 seconds

# Delay ranges for human-like behavior (in seconds)
MIN_DELAY = 0.3
MAX_DELAY = 1.0

