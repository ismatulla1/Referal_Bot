import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Kanal ID (raqamli) va username (string) alohida bo‘ladi
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # masalan: -1001234567890
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # masalan: @Innova_physics

PRIVATE_GROUP_LINK = os.getenv("PRIVATE_GROUP_LINK")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
REQUIRED_REFERRALS = int(os.getenv("REQUIRED_REFERRALS", 7))

ADMINS = [int(x) for x in os.getenv("ADMINS", "5833169967").split(",") if x]

MODE = os.getenv("MODE", "WEBHOOK") # WEBHOOK yoki LOCAL
PORT = int(os.getenv("PORT", 10000)) # Render avtomatik PORT beradi
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")  # Render UR