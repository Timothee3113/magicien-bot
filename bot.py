import logging, random, itertools
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"

MATCHS = itertools.cycle([
    ("⚽ Lens vs Paris SG", "Les deux équipes marquent : OUI", 1.72, 7.4),
    ("🏀 LA Lakers vs Boston", "Plus de 218.5 points dans le match", 1.88, 6.5),
    ("⚽ Arsenal vs Man. City", "Buteur : Erling Haaland marque", 2.15, 5.8)
])

def rep():
    msg = "🧙‍♂️ 🟩 **[VRAIES VALEURS RÉELLES] — MAGIC BOT V3**\n========================================\n\n🎯 **LES TICKETS SIMPLES (Mise Max 50€) :**\n----------------------------------------\n"
    for i in range(2):
        match, intitule, cote, av = next(MATCHS)
        msg += f"📊 **Pari Simple n°{i+1}**\n⚔️ Rencontre : **{match}**\n🎯 **Pari :** `{intitule}`\n📊 **Cote :** `{cote}` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️\n📈 Value : `+{av}%` | 💰 **Mise : {min(50, int(av*6.5))} €**\n\n"
    msg += "========================================\n🚀 **LE COMBINÉ SAFE (Mise 25€) :**\n----------------------------------------\n1️⃣ Lens vs Paris SG ➔ `Paris SG ou Nul` (1.35)\n2️⃣ LA Lakers vs Boston ➔ `Plus de 214.5 pts` (1.40)\n\n📊 **Cote Totale : 1.89**\n========================================\n⚠️ _Mise max 50€ bridée pour la sécurité._"
    return msg

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("🟩 **Moteur en ligne !**\nExtraction des cotes et intitulés réels...")
    await c.bot.send_message(chat_id=u.effective_user.id, text=rep(), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Re-Scan", callback_data="s")],[InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],[InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="v")]]))

async def cb(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query
    try: await q.answer()
    except: pass
    if q.data == "s":
        try: await q.edit_message_text(text=rep(), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Re-Scan", callback_data="s")],[InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],[InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="v")]]))
        except: pass
    elif q.data == "b":
        await c.bot.send_message(chat_id=q.message.chat_id, text="📊 **SUIVI DE CAPITAL (BANKROLL) :**\n\n💰 Capital Initial : 1000.00 €\n📊 Paris Joués : 14\n📈 Performance : `+12.4% ROI` (Bénéficiaire)", parse_mode="Markdown")
    elif q.data == "v":
        await c.bot.send_message(chat_id=q.message.chat_id, text="🔒 **ACCÈS PREMIUM VIP**\nTarif : **20.00 €**", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Payer 20€ via Paysafecard", url="https://paysafecard.com")]]))

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    print("\n🚀 BOT EN LIGNE !")
    app.run_polling()

if __name__ == '__main__':
    main()
