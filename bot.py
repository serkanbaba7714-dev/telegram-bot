import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8789263066:AAFet94vItZ2wwBg0DEpobRKnNQGDAVgx_s"

users = {}
groups = set()
daily_bonus = {}
last_name = ""

male_names = [
    "Ahmet","Mehmet","Ali","Hasan","Murat","Emre","Burak","Can","Eren","Onur"
]

female_names = [
    "Ayşe","Fatma","Zeynep","Elif","Merve","Seda","Cansu","Buse","Derya","Esra"
]

def get_user(user_id):
    if user_id not in users:
        users[user_id] = 10000

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)
    groups.add(update.effective_chat.id)
    await update.message.reply_text("Memduh Dayı geldi yeğenim 😎")

# BAKİYE
async def bakiye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)
    await update.message.reply_text(f"Bakiyen: {users[user_id]} Memduh Lirası yeğenim 💰")

# SLOT
async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)

    kazanma = random.choice([True, False])

    if kazanma:
        kazanc = random.randint(2000, 5000)
        users[user_id] += kazanc
        mesajlar = [
            f"Helal sana yeğenim {kazanc} Memduh Lirası cebe indirdin yine 😏",
            f"Valla bugün senin günün yeğenim {kazanc} Memduh Lirası aldın 🔥",
            f"Makineyi çözmüşsün yeğenim {kazanc} Memduh Lirası senin 💰",
        ]
    else:
        kayip = random.randint(1000, 3000)
        users[user_id] -= kayip
        mesajlar = [
            f"Ne yaptın be yeğenim {kayip} Memduh Lirası gitti 😅",
            f"Cenabet misin yeğenim yine {kayip} kaybettin 🤦‍♂️",
            f"Bugün senden hayır yok yeğenim {kayip} uçtu gitti 😂",
        ]

    await update.message.reply_text(random.choice(mesajlar))

# GÜNLÜK BONUS
async def gunluk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    get_user(user_id)

    now = datetime.now()

    if user_id in daily_bonus:
        if now - daily_bonus[user_id] < timedelta(hours=24):
            await update.message.reply_text("Daha yeni aldın yeğenim yarın gel 😏")
            return

    users[user_id] += 10000
    daily_bonus[user_id] = now

    await update.message.reply_text("Günlük 10.000 Memduh Lirası aldın yeğenim 💰")

# TOPLİST
async def topliste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    siralama = sorted(users.items(), key=lambda x: x[1], reverse=True)

    mesaj = "🏆 En Zenginler:\n\n"

    for i, (user_id, bakiye) in enumerate(siralama[:5], start=1):
        mesaj += f"{i}. {bakiye} Memduh Lirası\n"

    await update.message.reply_text(mesaj)

# FAKE MESAJ
async def fake_activity(context: ContextTypes.DEFAULT_TYPE):
    global last_name

    for chat_id in groups:
        try:
            if random.choice([True, False]):
                name = random.choice(male_names)
                mesajlar = [
                    f"🔥 {name} sağlam vurdu yeğenlerim kasa dağıldı!",
                    f"💰 {name} yine aldı yürüdü yeğenlerim!",
                ]
            else:
                name = random.choice(female_names)
                mesajlar = [
                    f"🔥 {name} resmen uçtu yeğenlerim parayı topladı!",
                    f"💰 {name} bugün coşmuş yeğenlerim!",
                ]

            while name == last_name:
                name = random.choice(male_names + female_names)

            last_name = name

            await context.bot.send_message(chat_id, random.choice(mesajlar))

        except:
            pass

# BOT
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("bakiyem", bakiye))
app.add_handler(CommandHandler("slotoyna", slot))
app.add_handler(CommandHandler("gunluk", gunluk))
app.add_handler(CommandHandler("topliste", topliste))

app.job_queue.run_repeating(fake_activity, interval=1200, first=10)

print("Bot çalışıyor...")
app.run_polling()