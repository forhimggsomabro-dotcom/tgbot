import asyncio
import json
import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# =========================================================
# CONFIGURATION
# =========================================================

BOT_TOKEN = "8650482928:AAE9Cx1pBiQ_R_hkl6u6ABf4otxp0L1E4G0"
ADMIN_ID = 8133480591

# Public usernames such as "@mychannel", or numeric IDs such as -1001234567890.
CHANNEL_ID: str | int = "@PANKAZXX_SHOP"
GROUP_ID: str | int = "https://t.me/+IQ4_X5pUfXo1NzM1"

# Optional stock announcement group.
# Set to 0 to disable forwarding.
STOCK_GROUP_ID: int = 0

CHANNEL_LINK = "https://t.me/your_channel"
GROUP_LINK = "https://t.me/your_group"
SUPPORT_LINK = "https://t.me/PANKAZXX_support"

DATABASE_FILE = "database.json"
BACKUP_FILE = "database_backup.json"

DEFAULT_REFERRAL_REWARD = 20
DEFAULT_MIN_ACTIVE_REFERRALS = 1

# =========================================================
# DATABASE
# =========================================================

DEFAULT_DB = {
    "users": {},
    "products": {},
    "orders": {},
    "coupons": {},
    "redeem_codes": {},
    "transactions": [],
    "settings": {
        "referral_reward": DEFAULT_REFERRAL_REWARD,
        "min_active_referrals": DEFAULT_MIN_ACTIVE_REFERRALS,
        "total_sales": 0,
        "total_revenue": 0,
        "maintenance": False,
    },
}


def deep_copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


def load_database() -> dict:
    if not os.path.exists(DATABASE_FILE):
        return deep_copy(DEFAULT_DB)

    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        return deep_copy(DEFAULT_DB)

    for key, default_value in DEFAULT_DB.items():
        if key not in loaded:
            loaded[key] = deep_copy(default_value)

    for key, default_value in DEFAULT_DB["settings"].items():
        loaded["settings"].setdefault(key, default_value)

    return loaded


db = load_database()
db_lock = asyncio.Lock()


async def save_database() -> None:
    async with db_lock:
        temporary = DATABASE_FILE + ".tmp"
        with open(temporary, "w", encoding="utf-8") as file:
            json.dump(db, file, ensure_ascii=False, indent=2)
        os.replace(temporary, DATABASE_FILE)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


def get_user(user_id: int | str) -> dict | None:
    return db["users"].get(str(user_id))


def ensure_user(from_user: types.User, referred_by: str | None = None) -> tuple[dict, bool]:
    user_id = str(from_user.id)
    existing = db["users"].get(user_id)

    if existing:
        existing["username"] = from_user.username or ""
        existing["name"] = from_user.full_name
        existing["last_seen"] = now_iso()
        return existing, False

    valid_referrer = None
    if referred_by and referred_by.isdigit() and referred_by != user_id:
        if referred_by in db["users"]:
            valid_referrer = referred_by

    user = {
        "id": from_user.id,
        "username": from_user.username or "",
        "name": from_user.full_name,
        "balance": 0,
        "banned": False,
        "verified": False,
        "referred_by": valid_referrer,
        "referrals": [],
        "active_referrals": [],
        "referral_rewarded": False,
        "joined_at": now_iso(),
        "last_seen": now_iso(),
        "orders": [],
        "used_coupons": [],
        "used_codes": [],
    }
    db["users"][user_id] = user

    if valid_referrer:
        referrer = db["users"][valid_referrer]
        if user_id not in referrer["referrals"]:
            referrer["referrals"].append(user_id)

    return user, True


def add_transaction(user_id: int | str, amount: int, transaction_type: str, note: str) -> None:
    db["transactions"].append(
        {
            "id": str(int(time.time() * 1000)),
            "user_id": str(user_id),
            "amount": amount,
            "type": transaction_type,
            "note": note,
            "created_at": now_iso(),
        }
    )
    if len(db["transactions"]) > 5000:
        db["transactions"] = db["transactions"][-5000:]


# =========================================================
# BOT INITIALIZATION
# =========================================================

if BOT_TOKEN == "PUT_YOUR_NEW_BOT_TOKEN_HERE":
    print("WARNING: Add your new bot token to BOT_TOKEN before running.")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


# =========================================================
# FSM STATES
# =========================================================

class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_user_lookup = State()
    waiting_add_balance = State()
    waiting_remove_balance = State()
    waiting_ban_user = State()
    waiting_unban_user = State()

    waiting_product_name = State()
    waiting_product_price = State()
    waiting_product_stock = State()
    waiting_product_items = State()
    waiting_delete_product = State()
    waiting_edit_product = State()

    waiting_coupon = State()
    waiting_redeem_code = State()
    waiting_referral_reward = State()
    waiting_min_referrals = State()
    waiting_restore_file = State()


class UserStates(StatesGroup):
    waiting_coupon = State()
    waiting_redeem_code = State()


# =========================================================
# KEYBOARDS
# =========================================================

def cb(text: str, data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=data)


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("🛍 Products", "user_products"), cb("💰 Wallet", "user_wallet")],
            [cb("👥 Refer & Earn", "user_referral"), cb("📜 My Orders", "user_orders")],
            [cb("🎟 Apply Coupon", "user_coupon"), cb("🎁 Redeem Code", "user_redeem")],
            [InlineKeyboardButton(text="🆘 Support", url=SUPPORT_LINK)],
        ]
    )


def force_join_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Join Channel", url=CHANNEL_LINK)],
            [cb("✅ Verify Membership", "verify_join")],
        ]
    )


def admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("📊 Dashboard", "admin_dashboard"), cb("👥 Users", "admin_users")],
            [cb("📦 Products", "admin_products"), cb("💰 Balance", "admin_balance")],
            [cb("📢 Broadcast", "admin_broadcast"), cb("🎟 Coupons", "admin_coupons")],
            [cb("🎁 Redeem Codes", "admin_codes"), cb("⚙ Settings", "admin_settings")],
            [cb("💾 Backup", "admin_backup"), cb("♻ Restore", "admin_restore")],
            [cb("🏠 User Menu", "back_main")],
        ]
    )


def admin_users_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("🔎 Find User", "admin_find_user")],
            [cb("🚫 Ban", "admin_ban"), cb("✅ Unban", "admin_unban")],
            [cb("⬅ Back", "admin_home")],
        ]
    )


def admin_balance_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("➕ Add Balance", "admin_add_balance")],
            [cb("➖ Remove Balance", "admin_remove_balance")],
            [cb("⬅ Back", "admin_home")],
        ]
    )


def admin_products_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("➕ Add Product", "admin_add_product")],
            [cb("✏ Edit Product", "admin_edit_product")],
            [cb("🗑 Delete Product", "admin_delete_product")],
            [cb("📋 View Products", "admin_view_products")],
            [cb("⬅ Back", "admin_home")],
        ]
    )


def admin_coupons_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("➕ Create Coupon", "admin_create_coupon")],
            [cb("📋 View Coupons", "admin_view_coupons")],
            [cb("⬅ Back", "admin_home")],
        ]
    )


def admin_codes_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("➕ Create Redeem Code", "admin_create_code")],
            [cb("📋 View Codes", "admin_view_codes")],
            [cb("⬅ Back", "admin_home")],
        ]
    )


def admin_settings_menu() -> InlineKeyboardMarkup:
    status = "ON" if db["settings"]["maintenance"] else "OFF"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("💸 Referral Reward", "admin_ref_reward")],
            [cb("👤 Minimum Active Referrals", "admin_min_refs")],
            [cb(f"🛠 Maintenance: {status}", "admin_toggle_maintenance")],
            [cb("⬅ Back", "admin_home")],
        ]
    )


def back_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[cb("⬅ Main Menu", "back_main")]])


def back_admin_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[cb("⬅ Admin Panel", "admin_home")]])


# =========================================================
# MEMBERSHIP / ACCESS
# =========================================================

async def member_is_joined(chat_id: str | int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in {"member", "administrator", "creator", "restricted"}
    except Exception:
        return False


async def verify_membership(user_id: int) -> bool:
    return await member_is_joined(CHANNEL_ID, user_id)


async def activate_referral(user_id: int) -> None:
    user = get_user(user_id)
    if not user:
        return

    referrer_id = user.get("referred_by")
    if not referrer_id or user.get("referral_rewarded"):
        return

    referrer = get_user(referrer_id)
    if not referrer:
        return

    uid = str(user_id)
    if uid not in referrer["active_referrals"]:
        referrer["active_referrals"].append(uid)

    reward = int(db["settings"]["referral_reward"])
    referrer["balance"] += reward
    user["referral_rewarded"] = True
    add_transaction(referrer_id, reward, "referral", f"Active referral reward for user {user_id}")

    try:
        await bot.send_message(
            int(referrer_id),
            f"🎉 Your referral became active!\n\n"
            f"💰 ₹{reward} was added to your wallet.",
        )
    except Exception:
        pass


async def user_access_message(message: Message) -> bool:
    user = get_user(message.from_user.id)
    if user and user.get("banned"):
        await message.answer("🚫 You are banned from using this bot.")
        return False

    if db["settings"]["maintenance"] and not is_admin(message.from_user.id):
        await message.answer("🛠 The bot is currently under maintenance. Please try again later.")
        return False

    if not await verify_membership(message.from_user.id):
        await message.answer(
            "🔒 Join our channel to continue.",
            reply_markup=force_join_menu(),
        )
        return False

    if user and not user.get("verified"):
        user["verified"] = True
        await activate_referral(message.from_user.id)
        await save_database()

    return True


# =========================================================
# USER COMMANDS
# =========================================================

@dp.message(Command("start"))
async def command_start(message: Message) -> None:
    referral = None
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) == 2:
        referral = parts[1].strip()

    user, created = ensure_user(message.from_user, referral)
    await save_database()

    if user.get("banned"):
        await message.answer("🚫 You are banned from using this bot.")
        return

    if not await verify_membership(message.from_user.id):
        await message.answer(
            "✨ Welcome to PankazXX AI Store!\n\n"
            "To unlock the bot, join the channel and then press Verify.",
            reply_markup=force_join_menu(),
        )
        return

    if not user.get("verified"):
        user["verified"] = True
        await activate_referral(message.from_user.id)
        await save_database()

    await message.answer(
        f"👋 Welcome, {message.from_user.full_name}!\n\n"
        "Choose an option below:",
        reply_markup=main_menu(),
    )


@dp.callback_query(F.data == "verify_join")
async def callback_verify_join(callback: CallbackQuery) -> None:
    user, _ = ensure_user(callback.from_user)
    if await verify_membership(callback.from_user.id):
        if not user.get("verified"):
            user["verified"] = True
            await activate_referral(callback.from_user.id)
            await save_database()
        await callback.message.answer("✅ Membership verified successfully.", reply_markup=main_menu())
    else:
        await callback.answer("Join the channel first.", show_alert=True)


@dp.callback_query(F.data == "back_main")
async def callback_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    if not await user_access_message(callback.message):
        return
    await callback.message.answer("🏠 Main Menu", reply_markup=main_menu())


@dp.callback_query(F.data == "user_wallet")
async def callback_wallet(callback: CallbackQuery) -> None:
    user = get_user(callback.from_user.id)
    if not user:
        return
    await callback.message.answer(
        f"💰 Wallet\n\n"
        f"Available balance: ₹{user['balance']}\n"
        f"Active referrals: {len(user['active_referrals'])}\n"
        f"Total orders: {len(user['orders'])}",
        reply_markup=back_main_keyboard(),
    )


@dp.callback_query(F.data == "user_referral")
async def callback_referral(callback: CallbackQuery) -> None:
    user = get_user(callback.from_user.id)
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start={callback.from_user.id}"
    reward = db["settings"]["referral_reward"]
    minimum = db["settings"]["min_active_referrals"]

    await callback.message.answer(
        f"👥 Refer & Earn\n\n"
        f"Your link:\n{link}\n\n"
        f"💸 Reward per active referral: ₹{reward}\n"
        f"✅ Active referrals: {len(user['active_referrals'])}\n"
        f"📌 Minimum active referrals required: {minimum}",
        reply_markup=back_main_keyboard(),
    )


@dp.callback_query(F.data == "user_products")
async def callback_products(callback: CallbackQuery) -> None:
    if not db["products"]:
        await callback.message.answer("📦 No products are available right now.", reply_markup=back_main_keyboard())
        return

    rows = []
    for product_id, product in db["products"].items():
        rows.append(
            [
                cb(
                    f"🛒 {product['name']} — ₹{product['price']} ({len(product['stock_items'])} left)",
                    f"product:{product_id}",
                )
            ]
        )
    rows.append([cb("⬅ Main Menu", "back_main")])
    await callback.message.answer("🛍 Available Products", reply_markup=InlineKeyboardMarkup(inline_keyboard=rows))


@dp.callback_query(F.data.startswith("product:"))
async def callback_product_details(callback: CallbackQuery) -> None:
    product_id = callback.data.split(":", 1)[1]
    product = db["products"].get(product_id)
    if not product:
        await callback.answer("Product not found.", show_alert=True)
        return

    stock_count = len(product["stock_items"])
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [cb("✅ Buy Now", f"buy:{product_id}")],
            [cb("⬅ Products", "user_products")],
        ]
    )
    await callback.message.answer(
        f"📦 {product['name']}\n\n"
        f"📝 {product.get('description', 'Digital product')}\n"
        f"💵 Price: ₹{product['price']}\n"
        f"📊 Stock: {stock_count}",
        reply_markup=keyboard,
    )


@dp.callback_query(F.data.startswith("buy:"))
async def callback_buy_product(callback: CallbackQuery) -> None:
    user = get_user(callback.from_user.id)
    if not user:
        return

    product_id = callback.data.split(":", 1)[1]
    product = db["products"].get(product_id)

    if not product:
        await callback.answer("Product no longer exists.", show_alert=True)
        return

    minimum = int(db["settings"]["min_active_referrals"])
    if len(user["active_referrals"]) < minimum:
        await callback.answer(
            f"You need at least {minimum} active referral(s) before buying.",
            show_alert=True,
        )
        return

    if not product["stock_items"]:
        await callback.answer("This product is out of stock.", show_alert=True)
        return

    price = int(product["price"])
    if user["balance"] < price:
        await callback.answer(
            f"Insufficient balance. You need ₹{price}.",
            show_alert=True,
        )
        return

    stock_item = product["stock_items"].pop(0)
    user["balance"] -= price

    order_id = str(int(time.time() * 1000))
    order = {
        "id": order_id,
        "user_id": str(callback.from_user.id),
        "product_id": product_id,
        "product_name": product["name"],
        "price": price,
        "delivered_item": stock_item,
        "created_at": now_iso(),
    }
    db["orders"][order_id] = order
    user["orders"].append(order_id)
    db["settings"]["total_sales"] += 1
    db["settings"]["total_revenue"] += price
    add_transaction(callback.from_user.id, -price, "purchase", f"Purchased {product['name']}")
    await save_database()

    await callback.message.answer(
        f"✅ Purchase Successful\n\n"
        f"📦 Product: {product['name']}\n"
        f"💵 Paid: ₹{price}\n\n"
        f"🔐 Your delivery:\n<code>{stock_item}</code>\n\n"
        "Keep this information private.",
        parse_mode="HTML",
        reply_markup=back_main_keyboard(),
    )

    try:
        await bot.send_message(
            ADMIN_ID,
            f"🛒 New Order\n\n"
            f"Order: {order_id}\n"
            f"User: {callback.from_user.id}\n"
            f"Product: {product['name']}\n"
            f"Amount: ₹{price}",
        )
    except Exception:
        pass


@dp.callback_query(F.data == "user_orders")
async def callback_orders(callback: CallbackQuery) -> None:
    user = get_user(callback.from_user.id)
    order_ids = user.get("orders", [])[-10:]

    if not order_ids:
        await callback.message.answer("📜 You have no orders yet.", reply_markup=back_main_keyboard())
        return

    lines = ["📜 Your Recent Orders\n"]
    for order_id in reversed(order_ids):
        order = db["orders"].get(order_id)
        if order:
            lines.append(
                f"• {order['product_name']} — ₹{order['price']}\n"
                f"  ID: {order_id}\n"
                f"  Date: {order['created_at']}"
            )
    await callback.message.answer("\n\n".join(lines), reply_markup=back_main_keyboard())


@dp.callback_query(F.data == "user_coupon")
async def callback_user_coupon(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(UserStates.waiting_coupon)
    await callback.message.answer("🎟 Send the coupon code.")


@dp.message(UserStates.waiting_coupon)
async def process_user_coupon(message: Message, state: FSMContext) -> None:
    user = get_user(message.from_user.id)
    code = (message.text or "").strip().upper()
    coupon = db["coupons"].get(code)

    if not coupon or not coupon.get("active", True):
        await message.answer("❌ Invalid or inactive coupon.")
        await state.clear()
        return

    if code in user["used_coupons"]:
        await message.answer("❌ You have already used this coupon.")
        await state.clear()
        return

    uses_left = int(coupon.get("uses_left", 0))
    if uses_left <= 0:
        await message.answer("❌ This coupon has reached its usage limit.")
        await state.clear()
        return

    amount = int(coupon["amount"])
    user["balance"] += amount
    user["used_coupons"].append(code)
    coupon["uses_left"] -= 1
    add_transaction(message.from_user.id, amount, "coupon", f"Coupon {code}")
    await save_database()
    await state.clear()

    await message.answer(f"✅ Coupon applied. ₹{amount} added to your wallet.", reply_markup=main_menu())


@dp.callback_query(F.data == "user_redeem")
async def callback_user_redeem(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(UserStates.waiting_redeem_code)
    await callback.message.answer("🎁 Send your redeem code.")


@dp.message(UserStates.waiting_redeem_code)
async def process_user_redeem(message: Message, state: FSMContext) -> None:
    user = get_user(message.from_user.id)
    code = (message.text or "").strip().upper()
    redeem = db["redeem_codes"].get(code)

    if not redeem or not redeem.get("active", True):
        await message.answer("❌ Invalid or inactive redeem code.")
        await state.clear()
        return

    if code in user["used_codes"]:
        await message.answer("❌ You have already used this code.")
        await state.clear()
        return

    uses_left = int(redeem.get("uses_left", 0))
    if uses_left <= 0:
        await message.answer("❌ This redeem code has reached its limit.")
        await state.clear()
        return

    amount = int(redeem["amount"])
    user["balance"] += amount
    user["used_codes"].append(code)
    redeem["uses_left"] -= 1
    add_transaction(message.from_user.id, amount, "redeem", f"Redeem code {code}")
    await save_database()
    await state.clear()

    await message.answer(f"✅ Code redeemed. ₹{amount} added to your wallet.", reply_markup=main_menu())


# =========================================================
# ADMIN PANEL
# =========================================================

@dp.message(Command("admin"))
async def command_admin(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    await message.answer("👑 Admin Panel", reply_markup=admin_menu())


@dp.callback_query(F.data == "admin_home")
async def callback_admin_home(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_admin(callback.from_user.id):
        return
    await state.clear()
    await callback.message.answer("👑 Admin Panel", reply_markup=admin_menu())


@dp.callback_query(F.data == "admin_dashboard")
async def callback_admin_dashboard(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        return

    users = list(db["users"].values())
    verified = sum(1 for user in users if user.get("verified"))
    banned = sum(1 for user in users if user.get("banned"))
    total_balance = sum(int(user.get("balance", 0)) for user in users)
    total_stock = sum(len(product.get("stock_items", [])) for product in db["products"].values())

    await callback.message.answer(
        "📊 Statistics Dashboard\n\n"
        f"👥 Total users: {len(users)}\n"
        f"✅ Verified users: {verified}\n"
        f"🚫 Banned users: {banned}\n"
        f"📦 Products: {len(db['products'])}\n"
        f"📚 Total stock items: {total_stock}\n"
        f"🛒 Total sales: {db['settings']['total_sales']}\n"
        f"💵 Total revenue: ₹{db['settings']['total_revenue']}\n"
        f"💰 User wallet total: ₹{total_balance}",
        reply_markup=back_admin_keyboard(),
    )


@dp.callback_query(F.data == "admin_users")
async def callback_admin_users(callback: CallbackQuery) -> None:
    if is_admin(callback.from_user.id):
        await callback.message.answer("👥 User Management", reply_markup=admin_users_menu())


@dp.callback_query(F.data == "admin_find_user")
async def callback_find_user(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_user_lookup)
    await callback.message.answer("Send the Telegram user ID.")


@dp.message(AdminStates.waiting_user_lookup)
async def process_find_user(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        return
    uid = (message.text or "").strip()
    user = get_user(uid)
    await state.clear()

    if not user:
        await message.answer("❌ User not found.", reply_markup=back_admin_keyboard())
        return

    await message.answer(
        f"👤 User Details\n\n"
        f"ID: {uid}\n"
        f"Name: {user.get('name')}\n"
        f"Username: @{user.get('username') or 'none'}\n"
        f"Balance: ₹{user.get('balance', 0)}\n"
        f"Verified: {user.get('verified')}\n"
        f"Banned: {user.get('banned')}\n"
        f"Referrals: {len(user.get('referrals', []))}\n"
        f"Active referrals: {len(user.get('active_referrals', []))}\n"
        f"Orders: {len(user.get('orders', []))}",
        reply_markup=back_admin_keyboard(),
    )


@dp.callback_query(F.data == "admin_ban")
async def callback_ban_user(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_ban_user)
    await callback.message.answer("Send the user ID to ban.")


@dp.message(AdminStates.waiting_ban_user)
async def process_ban_user(message: Message, state: FSMContext) -> None:
    uid = (message.text or "").strip()
    user = get_user(uid)
    await state.clear()
    if not user:
        await message.answer("❌ User not found.")
        return
    user["banned"] = True
    await save_database()
    await message.answer(f"🚫 User {uid} has been banned.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_unban")
async def callback_unban_user(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_unban_user)
    await callback.message.answer("Send the user ID to unban.")


@dp.message(AdminStates.waiting_unban_user)
async def process_unban_user(message: Message, state: FSMContext) -> None:
    uid = (message.text or "").strip()
    user = get_user(uid)
    await state.clear()
    if not user:
        await message.answer("❌ User not found.")
        return
    user["banned"] = False
    await save_database()
    await message.answer(f"✅ User {uid} has been unbanned.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_balance")
async def callback_admin_balance(callback: CallbackQuery) -> None:
    await callback.message.answer("💰 Balance Management", reply_markup=admin_balance_menu())


@dp.callback_query(F.data == "admin_add_balance")
async def callback_add_balance(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_add_balance)
    await callback.message.answer("Send: USER_ID AMOUNT\nExample: 123456789 500")


@dp.message(AdminStates.waiting_add_balance)
async def process_add_balance(message: Message, state: FSMContext) -> None:
    try:
        uid, amount_text = (message.text or "").split(maxsplit=1)
        amount = int(amount_text)
        if amount <= 0:
            raise ValueError
        user = get_user(uid)
        if not user:
            raise KeyError
    except (ValueError, KeyError):
        await message.answer("❌ Invalid format or user. Send: USER_ID AMOUNT")
        return

    user["balance"] += amount
    add_transaction(uid, amount, "admin_add", f"Added by admin {ADMIN_ID}")
    await save_database()
    await state.clear()
    await message.answer(f"✅ Added ₹{amount} to user {uid}.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_remove_balance")
async def callback_remove_balance(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_remove_balance)
    await callback.message.answer("Send: USER_ID AMOUNT\nExample: 123456789 100")


@dp.message(AdminStates.waiting_remove_balance)
async def process_remove_balance(message: Message, state: FSMContext) -> None:
    try:
        uid, amount_text = (message.text or "").split(maxsplit=1)
        amount = int(amount_text)
        if amount <= 0:
            raise ValueError
        user = get_user(uid)
        if not user:
            raise KeyError
    except (ValueError, KeyError):
        await message.answer("❌ Invalid format or user. Send: USER_ID AMOUNT")
        return

    removed = min(user["balance"], amount)
    user["balance"] -= removed
    add_transaction(uid, -removed, "admin_remove", f"Removed by admin {ADMIN_ID}")
    await save_database()
    await state.clear()
    await message.answer(f"✅ Removed ₹{removed} from user {uid}.", reply_markup=back_admin_keyboard())


# =========================================================
# ADMIN PRODUCTS
# =========================================================

@dp.callback_query(F.data == "admin_products")
async def callback_admin_products(callback: CallbackQuery) -> None:
    await callback.message.answer("📦 Product Management", reply_markup=admin_products_menu())


@dp.callback_query(F.data == "admin_add_product")
async def callback_add_product(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_product_name)
    await callback.message.answer("Send the product name.")


@dp.message(AdminStates.waiting_product_name)
async def process_product_name(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if not name:
        await message.answer("Send a valid name.")
        return
    await state.update_data(product_name=name)
    await state.set_state(AdminStates.waiting_product_price)
    await message.answer("Send the product price as a whole number.")


@dp.message(AdminStates.waiting_product_price)
async def process_product_price(message: Message, state: FSMContext) -> None:
    try:
        price = int((message.text or "").strip())
        if price < 0:
            raise ValueError
    except ValueError:
        await message.answer("Send a valid whole-number price.")
        return
    await state.update_data(product_price=price)
    await state.set_state(AdminStates.waiting_product_items)
    await message.answer(
        "Send stock items, one item per line.\n\n"
        "Example:\nemail1:password1\nemail2:password2"
    )


@dp.message(AdminStates.waiting_product_items)
async def process_product_items(message: Message, state: FSMContext) -> None:
    items = [line.strip() for line in (message.text or "").splitlines() if line.strip()]
    data = await state.get_data()
    name = data["product_name"]
    price = data["product_price"]

    product_id = str(int(time.time() * 1000))
    db["products"][product_id] = {
        "id": product_id,
        "name": name,
        "description": "Digital AI service product",
        "price": price,
        "stock_items": items,
        "created_at": now_iso(),
    }
    await save_database()
    await state.clear()
    await message.answer(
        f"✅ Product created.\n\nName: {name}\nPrice: ₹{price}\nStock: {len(items)}",
        reply_markup=back_admin_keyboard(),
    )


@dp.callback_query(F.data == "admin_view_products")
async def callback_view_products(callback: CallbackQuery) -> None:
    if not db["products"]:
        await callback.message.answer("No products found.", reply_markup=back_admin_keyboard())
        return

    lines = ["📋 Products\n"]
    for product_id, product in db["products"].items():
        lines.append(
            f"ID: {product_id}\n"
            f"Name: {product['name']}\n"
            f"Price: ₹{product['price']}\n"
            f"Stock: {len(product['stock_items'])}"
        )
    text = "\n\n".join(lines)
    for start in range(0, len(text), 3900):
        await callback.message.answer(text[start:start + 3900], reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_delete_product")
async def callback_delete_product(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_delete_product)
    await callback.message.answer("Send the product ID to delete.")


@dp.message(AdminStates.waiting_delete_product)
async def process_delete_product(message: Message, state: FSMContext) -> None:
    product_id = (message.text or "").strip()
    await state.clear()
    product = db["products"].pop(product_id, None)
    if not product:
        await message.answer("❌ Product not found.")
        return
    await save_database()
    await message.answer(f"🗑 Deleted {product['name']}.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_edit_product")
async def callback_edit_product(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_edit_product)
    await callback.message.answer(
        "Send:\nPRODUCT_ID | NEW_PRICE | STOCK_ITEMS\n\n"
        "Separate stock items with semicolons.\n"
        "Example:\n123456 | 299 | account1;account2"
    )


@dp.message(AdminStates.waiting_edit_product)
async def process_edit_product(message: Message, state: FSMContext) -> None:
    try:
        product_id, price_text, stock_text = [part.strip() for part in (message.text or "").split("|", 2)]
        product = db["products"][product_id]
        price = int(price_text)
        items = [item.strip() for item in stock_text.split(";") if item.strip()]
    except (ValueError, KeyError):
        await message.answer("❌ Invalid format or product ID.")
        return

    product["price"] = price
    product["stock_items"].extend(items)
    await save_database()
    await state.clear()
    await message.answer(
        f"✅ Product updated.\nNew price: ₹{price}\nAdded stock: {len(items)}",
        reply_markup=back_admin_keyboard(),
    )


# =========================================================
# ADMIN BROADCAST
# =========================================================

@dp.callback_query(F.data == "admin_broadcast")
async def callback_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_broadcast)
    await callback.message.answer(
        "📢 Send the message, photo, video, document, or other content to broadcast.\n"
        "Use /cancel to stop."
    )


@dp.message(Command("cancel"))
async def command_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    if is_admin(message.from_user.id):
        await message.answer("Cancelled.", reply_markup=admin_menu())
    else:
        await message.answer("Cancelled.", reply_markup=main_menu())


@dp.message(AdminStates.waiting_broadcast)
async def process_broadcast(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        return

    user_ids = list(db["users"].keys())
    progress = await message.answer(f"📤 Broadcasting to {len(user_ids)} users...")

    sent = 0
    failed = 0

    for index, uid in enumerate(user_ids, start=1):
        try:
            await bot.copy_message(
                chat_id=int(uid),
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            sent += 1
        except Exception:
            failed += 1

        if index % 25 == 0:
            try:
                await progress.edit_text(
                    f"📤 Broadcast progress\n\n"
                    f"Processed: {index}/{len(user_ids)}\n"
                    f"Sent: {sent}\n"
                    f"Failed: {failed}"
                )
            except Exception:
                pass
        await asyncio.sleep(0.04)

    await state.clear()
    await progress.edit_text(
        f"✅ Broadcast finished\n\n"
        f"Sent: {sent}\n"
        f"Failed: {failed}",
        reply_markup=back_admin_keyboard(),
    )


# =========================================================
# ADMIN COUPONS / REDEEM CODES
# =========================================================

@dp.callback_query(F.data == "admin_coupons")
async def callback_admin_coupons(callback: CallbackQuery) -> None:
    await callback.message.answer("🎟 Coupon Management", reply_markup=admin_coupons_menu())


@dp.callback_query(F.data == "admin_create_coupon")
async def callback_create_coupon(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_coupon)
    await callback.message.answer("Send: CODE AMOUNT USES\nExample: WELCOME50 50 100")


@dp.message(AdminStates.waiting_coupon)
async def process_create_coupon(message: Message, state: FSMContext) -> None:
    try:
        code, amount_text, uses_text = (message.text or "").split(maxsplit=2)
        amount = int(amount_text)
        uses = int(uses_text)
        if amount <= 0 or uses <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Send: CODE AMOUNT USES")
        return

    code = code.upper()
    db["coupons"][code] = {
        "amount": amount,
        "uses_left": uses,
        "active": True,
        "created_at": now_iso(),
    }
    await save_database()
    await state.clear()
    await message.answer(f"✅ Coupon {code} created.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_view_coupons")
async def callback_view_coupons(callback: CallbackQuery) -> None:
    if not db["coupons"]:
        await callback.message.answer("No coupons found.", reply_markup=back_admin_keyboard())
        return
    text = "🎟 Coupons\n\n" + "\n".join(
        f"{code}: ₹{item['amount']} | Uses left: {item['uses_left']}"
        for code, item in db["coupons"].items()
    )
    await callback.message.answer(text[:4000], reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_codes")
async def callback_admin_codes(callback: CallbackQuery) -> None:
    await callback.message.answer("🎁 Redeem Code Management", reply_markup=admin_codes_menu())


@dp.callback_query(F.data == "admin_create_code")
async def callback_create_code(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_redeem_code)
    await callback.message.answer("Send: CODE AMOUNT USES\nExample: GIFT100 100 10")


@dp.message(AdminStates.waiting_redeem_code)
async def process_create_code(message: Message, state: FSMContext) -> None:
    try:
        code, amount_text, uses_text = (message.text or "").split(maxsplit=2)
        amount = int(amount_text)
        uses = int(uses_text)
        if amount <= 0 or uses <= 0:
            raise ValueError
    except ValueError:
        await message.answer("❌ Send: CODE AMOUNT USES")
        return

    code = code.upper()
    db["redeem_codes"][code] = {
        "amount": amount,
        "uses_left": uses,
        "active": True,
        "created_at": now_iso(),
    }
    await save_database()
    await state.clear()
    await message.answer(f"✅ Redeem code {code} created.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_view_codes")
async def callback_view_codes(callback: CallbackQuery) -> None:
    if not db["redeem_codes"]:
        await callback.message.answer("No redeem codes found.", reply_markup=back_admin_keyboard())
        return
    text = "🎁 Redeem Codes\n\n" + "\n".join(
        f"{code}: ₹{item['amount']} | Uses left: {item['uses_left']}"
        for code, item in db["redeem_codes"].items()
    )
    await callback.message.answer(text[:4000], reply_markup=back_admin_keyboard())


# =========================================================
# ADMIN SETTINGS / BACKUP / RESTORE
# =========================================================

@dp.callback_query(F.data == "admin_settings")
async def callback_admin_settings(callback: CallbackQuery) -> None:
    await callback.message.answer("⚙ Bot Settings", reply_markup=admin_settings_menu())


@dp.callback_query(F.data == "admin_ref_reward")
async def callback_ref_reward(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_referral_reward)
    await callback.message.answer("Send the new referral reward amount.")


@dp.message(AdminStates.waiting_referral_reward)
async def process_ref_reward(message: Message, state: FSMContext) -> None:
    try:
        amount = int((message.text or "").strip())
        if amount < 0:
            raise ValueError
    except ValueError:
        await message.answer("Send a valid whole number.")
        return
    db["settings"]["referral_reward"] = amount
    await save_database()
    await state.clear()
    await message.answer(f"✅ Referral reward changed to ₹{amount}.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_min_refs")
async def callback_min_refs(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_min_referrals)
    await callback.message.answer("Send the minimum active referrals required to buy.")


@dp.message(AdminStates.waiting_min_referrals)
async def process_min_refs(message: Message, state: FSMContext) -> None:
    try:
        amount = int((message.text or "").strip())
        if amount < 0:
            raise ValueError
    except ValueError:
        await message.answer("Send a valid whole number.")
        return
    db["settings"]["min_active_referrals"] = amount
    await save_database()
    await state.clear()
    await message.answer(f"✅ Minimum active referrals changed to {amount}.", reply_markup=back_admin_keyboard())


@dp.callback_query(F.data == "admin_toggle_maintenance")
async def callback_toggle_maintenance(callback: CallbackQuery) -> None:
    db["settings"]["maintenance"] = not db["settings"]["maintenance"]
    await save_database()
    status = "enabled" if db["settings"]["maintenance"] else "disabled"
    await callback.message.answer(f"🛠 Maintenance mode {status}.", reply_markup=admin_settings_menu())


@dp.callback_query(F.data == "admin_backup")
async def callback_backup(callback: CallbackQuery) -> None:
    await save_database()
    shutil.copy2(DATABASE_FILE, BACKUP_FILE)
    await callback.message.answer_document(
        FSInputFile(BACKUP_FILE),
        caption="💾 Database backup",
        reply_markup=back_admin_keyboard(),
    )


@dp.callback_query(F.data == "admin_restore")
async def callback_restore(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_restore_file)
    await callback.message.answer("♻ Send a valid database JSON backup file.")


@dp.message(AdminStates.waiting_restore_file, F.document)
async def process_restore(message: Message, state: FSMContext) -> None:
    global db

    document = message.document
    if not document.file_name.lower().endswith(".json"):
        await message.answer("❌ Send a .json file.")
        return

    temporary_path = "restore_upload.json"
    await bot.download(document, destination=temporary_path)

    try:
        with open(temporary_path, "r", encoding="utf-8") as file:
            restored = json.load(file)
        required = {"users", "products", "orders", "coupons", "redeem_codes", "transactions", "settings"}
        if not required.issubset(restored.keys()):
            raise ValueError("Invalid structure")
    except (OSError, json.JSONDecodeError, ValueError):
        await message.answer("❌ Invalid backup file.")
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
        return

    shutil.copy2(DATABASE_FILE, BACKUP_FILE) if os.path.exists(DATABASE_FILE) else None
    db = restored
    await save_database()

    if os.path.exists(temporary_path):
        os.remove(temporary_path)

    await state.clear()
    await message.answer("✅ Database restored successfully.", reply_markup=admin_menu())


# =========================================================
# STOCK GROUP FORWARDING
# =========================================================

@dp.message(F.chat.id == STOCK_GROUP_ID)
async def forward_stock_group_message(message: Message) -> None:
    if STOCK_GROUP_ID == 0:
        return

    sent = 0
    for uid, user in db["users"].items():
        if not user.get("verified") or user.get("banned"):
            continue
        try:
            await bot.copy_message(
                chat_id=int(uid),
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            sent += 1
        except Exception:
            pass
        await asyncio.sleep(0.04)

    try:
        await bot.send_message(ADMIN_ID, f"📦 Stock update forwarded to {sent} users.")
    except Exception:
        pass


# =========================================================
# FALLBACK
# =========================================================

@dp.message()
async def fallback(message: Message) -> None:
    ensure_user(message.from_user)
    await save_database()

    if not await user_access_message(message):
        return

    await message.answer("Use the buttons below.", reply_markup=main_menu())


# =========================================================
# STARTUP
# =========================================================

async def main() -> None:
    await save_database()
    print("PankazXX AI Store Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
