import asyncio
import sqlite3
import os
import time

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8650482928:AAF7d_gV7M81D3ZKVdhmoESDo8w424wjYG8"

ADMIN_ID = 8133480591

FORCE_CHANNEL = "@PANKAZXX_SHOP"
FORCE_GROUP = "@lama_updates"

LOG_CHANNEL = "@PANKAZXX_SHOP"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

db = sqlite3.connect("lama_complete.db")
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
 user_id INTEGER,
 product TEXT,
 item TEXT,
 created INTEGER
);

CREATE TABLE IF NOT EXISTS payments(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER,
 amount REAL,
 status TEXT
);
""")

db.commit()


def user_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Products", callback_data="products"),
         InlineKeyboardButton(text="👤 Profile", callback_data="profile")],
        [InlineKeyboardButton(text="🎁 Invite Centre", callback_data="invite"),
         InlineKeyboardButton(text="💰 Top Up", callback_data="topup")],
        [InlineKeyboardButton(text="🎟 Redeem", callback_data="redeem"),
         InlineKeyboardButton(text="🆘 Help", callback_data="help")]
    ])


def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Stats", callback_data="stats")],
        [InlineKeyboardButton(text="📦 Add Stock", callback_data="add_stock")],
        [InlineKeyboardButton(text="🛒 Orders", callback_data="orders")],
        [InlineKeyboardButton(text="💵 Add Balance", callback_data="balance")],
        [InlineKeyboardButton(text="📢 Broadcast", callback_data="broadcast")]
    ])


async def log(text):
    try:
        await bot.send_message(LOG_CHANNEL, text)
    except:
        pass


async def joined(user_id):
    try:
        a = await bot.get_chat_member(FORCE_CHANNEL, user_id)
        b = await bot.get_chat_member(FORCE_GROUP, user_id)
        return a.status not in ["left","kicked"] and b.status not in ["left","kicked"]
    except:
        return False


def join_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Channel", url="https://t.me/PANKAZXX_SHOP")],
        [InlineKeyboardButton(text="👥 Group", url="https://t.me/lama_updates")],
        [InlineKeyboardButton(text="✅ Verify", callback_data="verify")]
    ])


@dp.message(Command("start"))
async def start(m: Message):
    cur.execute("INSERT OR IGNORE INTO users(id) VALUES(?)",(m.from_user.id,))
    db.commit()

    if not await joined(m.from_user.id):
        await m.answer(
            "🔒 Join our channel and group first.",
            reply_markup=join_keyboard()
        )
        return

    await m.answer(
        "📝 Welcome to Lama Bot!\n\n"
        "I'm here to help you purchase subscriptions and digital services easily and securely.",
        reply_markup=user_keyboard()
    )


@dp.callback_query(F.data=="verify")
async def verify(c:CallbackQuery):
    if await joined(c.from_user.id):
        await c.message.edit_text(
            "📝 Welcome to Lama Bot!",
            reply_markup=user_keyboard()
        )
    else:
        await c.answer("Please join first")


@dp.callback_query(F.data=="profile")
async def profile(c:CallbackQuery):
    u=cur.execute(
        "SELECT balance,refs FROM users WHERE id=?",
        (c.from_user.id,)
    ).fetchone()

    await c.message.edit_text(
        f"👤 Profile\n\n💰 Balance: ${u[0]:.2f}\n🎁 Referrals: {u[1]}",
        reply_markup=user_keyboard()
    )


@dp.callback_query(F.data=="products")
async def products(c:CallbackQuery):
    rows=cur.execute("SELECT id,name,price FROM products").fetchall()

    kb=[
        [InlineKeyboardButton(
            text=f"{x[1]} ${x[2]}",
            callback_data=f"buy_{x[0]}"
        )] for x in rows
    ]

    await c.message.edit_text(
        "🛒 Products",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )


@dp.callback_query(F.data.startswith("buy_"))
async def buy(c:CallbackQuery):
    pid=int(c.data.split("_")[1])

    p=cur.execute(
        "SELECT name,price,stock FROM products WHERE id=?",
        (pid,)
    ).fetchone()

    if not p or not p[2]:
        return await c.answer("Out of stock")

    bal=cur.execute(
        "SELECT balance FROM users WHERE id=?",
        (c.from_user.id,)
    ).fetchone()[0]

    if bal < p[1]:
        return await c.answer("Low balance")

    item=p[2].split("\n")[0]
    left="\n".join(p[2].split("\n")[1:])

    cur.execute(
        "UPDATE users SET balance=balance-? WHERE id=?",
        (p[1],c.from_user.id)
    )

    cur.execute(
        "UPDATE products SET stock=? WHERE id=?",
        (left,pid)
    )

    cur.execute(
        "INSERT INTO orders(user_id,product,item,created) VALUES(?,?,?,?)",
        (c.from_user.id,p[0],item,int(time.time()))
    )

    db.commit()

    await c.message.answer(
        f"✅ Purchase Successful\n\n📦 {p[0]}\n\n🔐 {item}"
    )

    await log(
        f"🛒 New Order\nProduct: {p[0]}\nStatus: Delivered"
    )


@dp.message(Command("admin"))
async def admin(m:Message):
    if m.from_user.id==ADMIN_ID:
        await m.answer("⚙️ Admin Panel",reply_markup=admin_keyboard())


@dp.message(Command("addbalance"))
async def add_balance(m:Message):
    if m.from_user.id!=ADMIN_ID:
        return

    x=m.text.split()
    if len(x)<3:
        return await m.answer("/addbalance user amount")

    cur.execute(
        "UPDATE users SET balance=balance+? WHERE id=?",
        (float(x[2]),int(x[1]))
    )
    db.commit()

    await m.answer("✅ Balance added")


async def health(request):
    return web.Response(text="Lama Bot Running")


async def server():
    app=web.Application()
    app.router.add_get("/",health)
    runner=web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(
        runner,"0.0.0.0",
        int(os.getenv("PORT",10000))
    ).start()


async def main():
    await server()
    await dp.start_polling(bot)


if __name__=="__main__":
    asyncio.run(main())
