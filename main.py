import asyncio
import sqlite3
import time
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

BOT_TOKEN = "8650482928:AAF7d_gV7M81D3ZKVdhmoESDo8w424wjYG8"

ADMIN_ID = 8133480591
LOG_CHANNEL = "@PANKAZXX_SHOP"
UPDATE_GROUP = "@lama_updates"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

db = sqlite3.connect("lama_store.db")
cur = db.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS users(
 id INTEGER PRIMARY KEY,
 balance REAL DEFAULT 0,
 refs INTEGER DEFAULT 0,
 banned INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS products(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT,
 price REAL,
 stock TEXT
);

CREATE TABLE IF NOT EXISTS orders(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user INTEGER,
 product TEXT,
 item TEXT,
 time INTEGER
);

CREATE TABLE IF NOT EXISTS payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user INTEGER,
 amount REAL,
 status TEXT
);

CREATE TABLE IF NOT EXISTS codes(
 code TEXT PRIMARY KEY,
 amount REAL
);
""")

db.commit()

cooldown = {}

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Products", callback_data="products"),
            InlineKeyboardButton(text="👤 Profile", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="🎁 Invite Centre", callback_data="invite"),
            InlineKeyboardButton(text="💰 Top Up Balance", callback_data="topup")
        ],
        [
            InlineKeyboardButton(text="🎟 Redeem Code", callback_data="redeem"),
            InlineKeyboardButton(text="📜 Bot Policy", callback_data="policy")
        ],
        [
            InlineKeyboardButton(text="🆘 Help", callback_data="help")
        ]
    ])

def admin_check(uid):
    return uid == ADMIN_ID


async def log(text):
    try:
        await bot.send_message(LOG_CHANNEL, text)
    except:
        pass


@dp.message(Command("start"))
async def start(message: Message):

    uid = message.from_user.id

    cur.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (uid,)
    )

    db.commit()

    await message.answer(
        "📝 Welcome to Lama Bot!\n\n"
        "I'm here to help you purchase subscriptions and digital services easily and securely.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):

    user = cur.execute(
        "SELECT balance,refs FROM users WHERE id=?",
        (call.from_user.id,)
    ).fetchone()

    await call.message.edit_text(
        f"👤 Profile\n\n"
        f"💰 Balance: ${user[0]:.2f}\n"
        f"🎁 Referrals: {user[1]}",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data == "products")
async def products(call: CallbackQuery):

    rows = cur.execute(
        "SELECT id,name,price FROM products"
    ).fetchall()

    buttons = []

    for p in rows:
        buttons.append([
            InlineKeyboardButton(
                text=f"{p[1]} - ${p[2]}",
                callback_data=f"buy:{p[0]}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅ Back",
            callback_data="home"
        )
    ])

    await call.message.edit_text(
        "🛒 Available Products",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        )
    )


@dp.callback_query(F.data.startswith("buy:"))
async def buy(call: CallbackQuery):

    if call.from_user.id in cooldown:
        if time.time()-cooldown[call.from_user.id] < 3:
            return

    cooldown[call.from_user.id]=time.time()

    pid=int(call.data.split(":")[1])

    product=cur.execute(
        "SELECT name,price,stock FROM products WHERE id=?",
        (pid,)
    ).fetchone()

    if not product:
        return

    if product[2]=="":
        return await call.answer("Out of stock")

    balance=cur.execute(
        "SELECT balance FROM users WHERE id=?",
        (call.from_user.id,)
    ).fetchone()[0]

    if balance < product[1]:
        return await call.answer("Insufficient balance")

    item=product[2].split("\n")[0]
    remaining="\n".join(product[2].split("\n")[1:])

    cur.execute(
        "UPDATE users SET balance=balance-? WHERE id=?",
        (product[1],call.from_user.id)
    )

    cur.execute(
        "UPDATE products SET stock=? WHERE id=?",
        (remaining,pid)
    )

    cur.execute(
        "INSERT INTO orders(user,product,item,time) VALUES(?,?,?,?)",
        (call.from_user.id,product[0],item,int(time.time()))
    )

    db.commit()

    await call.message.answer(
        f"✅ Purchase Successful\n\n"
        f"📦 {product[0]}\n\n"
        f"🔐 Your Details:\n{item}"
    )

    await log(
        f"🛒 New Purchase\n"
        f"User: {call.from_user.id}\n"
        f"Product: {product[0]}"
    )


@dp.callback_query(F.data=="topup")
async def topup(call:CallbackQuery):

    await call.message.edit_text(
        "💰 Binance Pay Top Up\n\n"
        "Send payment screenshot to admin.\n"
        "Admin will verify and add balance.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data=="invite")
async def invite(call:CallbackQuery):

    me=await bot.get_me()

    await call.message.edit_text(
        f"🎁 Invite Centre\n\n"
        f"https://t.me/{me.username}?start={call.from_user.id}\n\n"
        "Every 10 referrals = $1",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data=="help")
async def help_button(call:CallbackQuery):

    await call.message.edit_text(
        "🆘 Support\n\n@PANKAZXX_support",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data=="policy")
async def policy(call:CallbackQuery):

    await call.message.edit_text(
        "📜 Policy\n\n"
        "Use the service responsibly.",
        reply_markup=main_menu()
    )


@dp.callback_query(F.data=="home")
async def home(call:CallbackQuery):

    await call.message.edit_text(
        "📝 Welcome to Lama Bot!",
        reply_markup=main_menu()
    )


# ---------- ADMIN ----------


@dp.message(Command("admin"))
async def admin(message:Message):

    if not admin_check(message.from_user.id):
        return

    await message.answer(
        "⚙ Admin Panel\n\n"
        "/addproduct name price stock\n"
        "/balance user amount\n"
        "/stats\n"
        "/broadcast text"
    )


@dp.message(Command("addproduct"))
async def addproduct(message:Message):

    if not admin_check(message.from_user.id):
        return

    data=message.text.split(" ",3)

    if len(data)<4:
        return await message.answer(
            "/addproduct name price stock"
        )

    cur.execute(
        "INSERT INTO products(name,price,stock) VALUES(?,?,?)",
        (data[1],float(data[2]),data[3])
    )

    db.commit()

    await message.answer("✅ Product added")


@dp.message(Command("balance"))
async def balance(message:Message):

    if not admin_check(message.from_user.id):
        return

    data=message.text.split()

    cur.execute(
        "UPDATE users SET balance=balance+? WHERE id=?",
        (float(data[2]),int(data[1]))
    )

    db.commit()

    await message.answer("✅ Balance updated")


@dp.message(Command("stats"))
async def stats(message:Message):

    if admin_check(message.from_user.id):

        users=cur.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        products=cur.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        await message.answer(
            f"📊 Stats\nUsers: {users}\nProducts: {products}"
        )


async def main():
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(main())
