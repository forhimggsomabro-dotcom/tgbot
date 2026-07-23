"""
Lama Bot Final - Render Compatible
Aiogram 3.25

Install:
pip install aiogram==3.25.0 aiohttp aiosqlite python-dotenv

Set BOT_TOKEN before running.
"""

import asyncio
import os
import sqlite3
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8650482928:AAF7d_gV7M81D3ZKVdhmoESDo8w424wjYG8"

ADMIN_ID = 8133480591
LOG_CHANNEL = "@PANKAZXX_SHOP"
UPDATE_GROUP = "@lama_updates"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

db = sqlite3.connect("lama.db")
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
 item TEXT
);
""")

db.commit()


def menu():
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


async def send_log(text):
    try:
        await bot.send_message(LOG_CHANNEL, text)
    except Exception:
        pass


@dp.message(Command("start"))
async def start(message: Message):
    cur.execute("INSERT OR IGNORE INTO users(id) VALUES(?)",
                (message.from_user.id,))
    db.commit()

    await message.answer(
        "📝 Welcome to Lama Bot!\n\n"
        "I'm here to help you purchase subscriptions and digital services easily and securely.",
        reply_markup=menu()
    )


@dp.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    data = cur.execute(
        "SELECT balance,refs FROM users WHERE id=?",
        (call.from_user.id,)
    ).fetchone()

    await call.message.edit_text(
        f"👤 Profile\n\n💰 Balance: ${data[0]:.2f}\n🎁 Referrals: {data[1]}",
        reply_markup=menu()
    )


@dp.callback_query(F.data == "products")
async def products(call: CallbackQuery):
    rows = cur.execute("SELECT id,name,price FROM products").fetchall()

    buttons = [
        [InlineKeyboardButton(
            text=f"{x[1]} ${x[2]}",
            callback_data=f"buy_{x[0]}"
        )]
        for x in rows
    ]

    buttons.append([InlineKeyboardButton(text="⬅ Back", callback_data="home")])

    await call.message.edit_text(
        "🛒 Products",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )


@dp.callback_query(F.data.startswith("buy_"))
async def buy(call: CallbackQuery):
    pid = int(call.data.split("_")[1])

    product = cur.execute(
        "SELECT name,price,stock FROM products WHERE id=?",
        (pid,)
    ).fetchone()

    if not product or not product[2]:
        return await call.answer("Out of stock")

    user = cur.execute(
        "SELECT balance FROM users WHERE id=?",
        (call.from_user.id,)
    ).fetchone()

    if user[0] < product[1]:
        return await call.answer("Insufficient balance")

    item = product[2].split("\n")[0]
    left = "\n".join(product[2].split("\n")[1:])

    cur.execute(
        "UPDATE users SET balance=balance-? WHERE id=?",
        (product[1], call.from_user.id)
    )

    cur.execute(
        "UPDATE products SET stock=? WHERE id=?",
        (left, pid)
    )

    cur.execute(
        "INSERT INTO orders(user,product,item) VALUES(?,?,?)",
        (call.from_user.id, product[0], item)
    )

    db.commit()

    await call.message.answer(
        f"✅ Purchase Successful\n\n"
        f"📦 {product[0]}\n\n"
        f"🔐 Account:\n{item}"
    )

    await send_log(
        f"🛒 Purchase\nUser: {call.from_user.id}\nProduct: {product[0]}"
    )


@dp.callback_query()
async def buttons(call: CallbackQuery):
    if call.data == "home":
        await call.message.edit_text("📝 Welcome to Lama Bot!", reply_markup=menu())
    elif call.data == "topup":
        await call.message.edit_text(
            "💰 Binance Pay Top Up\nSend payment proof to admin.",
            reply_markup=menu()
        )
    elif call.data == "invite":
        me = await bot.get_me()
        await call.message.edit_text(
            f"🎁 Invite:\nhttps://t.me/{me.username}?start={call.from_user.id}",
            reply_markup=menu()
        )
    elif call.data == "help":
        await call.message.edit_text("@PANKAZXX_support", reply_markup=menu())


@dp.message(Command("admin"))
async def admin(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer(
            "⚙ Admin\n\n"
            "/addproduct name price stock\n"
            "/balance user amount\n"
            "/stats"
        )


@dp.message(Command("addproduct"))
async def add_product(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    data = message.text.split(" ", 3)

    if len(data) < 4:
        return await message.answer(
            "/addproduct Netflix 5 email:pass"
        )

    cur.execute(
        "INSERT INTO products(name,price,stock) VALUES(?,?,?)",
        (data[1], float(data[2]), data[3])
    )
    db.commit()

    await message.answer("✅ Product added")


@dp.message(Command("stats"))
async def stats(message: Message):
    if message.from_user.id == ADMIN_ID:
        users = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        products = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]

        await message.answer(
            f"📊 Users: {users}\n📦 Products: {products}"
        )


async def health(request):
    return web.Response(text="Lama Bot Running")


async def web_server():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        int(os.getenv("PORT", 10000))
    )

    await site.start()


async def main():
    await web_server()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
