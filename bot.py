import logging
import asyncio
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"
LIEN_PAIEMENT = "https://paysafecard.com"

def generer_ticket_immediat():
    # Détermination dynamique et automatique de la date du jour J en temps réel
    date_du_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    
    return (
        f"🧙‍♂️ 🟩 **[TICKET OFFICIEL DU JOUR] — {date_du_jour}**\n"
        "========================================\n\n"
        "🎯 **LES TICKETS SIMPLES (Mise Max 50€) :**\n"
        "----------------------------------------\n"
        "📊 **Pari Simple n°1 (Ligue 1)**\n"
        "⚔️ Rencontre : **Lens vs Paris SG**\n"
        "🎯 **Pari :** `Les deux équipes marquent : OUI`\n"
        "📊 **Cote :** `1.72` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️⭐️\n"
        "📈 Value : `+7.4%` | 💰 **Mise : 50 €**\n\n"
        "📊 **Pari Simple n°2 (Premier League)**\n"
        "⚔️ Rencontre : **Arsenal vs Man. City**\n"
        "🎯 **Pari :** `Buteur : Erling Haaland marque`\n"
        "📊 **Cote :** `2.15` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️\n"
        "📈 Value : `+5.8%` | 💰 **Mise : 38 €**\n\n"
        "========================================\n"
        "🚀 **LE COMBINÉ SAFE (Mise 25€) :**\n"
        "----------------------------------------\n"
        "1️⃣ Lens vs Paris SG ➔ `Paris SG ou Nul` (1.35)\n"
        "2️⃣ LA Lakers vs Boston ➔ `Plus de 214.5 pts` (1.40)\n\n"
        "📊 **Cote Totale : 1.89**\n"
        "========================================\n"
        "⚠️ _Mise max 50€ bridée pour la sécurité._"
    )

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan", callback_data="s")],
        [InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],
        [InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟩 **Moteur en ligne !**\nChargement des analyses du jour...")
    await context.bot.send_message(
        chat_id=update.effective_user.id,
        text=generer_ticket_immediat(),
        parse_mode="Markdown",
        reply_markup=clavier()
    )

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try: await q.answer()
    except: pass
    if q.data == "s":
        try: await q.edit_message_text(text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
    elif q.data == "b":
        await context.bot.send_message(chat_id=q.message.chat_id, text="📊 **BILAN :** `+12.4% ROI`", parse_mode="Markdown")
    elif q.data == "v":
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text="🔒 **ESPACE VIP**\nTarif : **20.00 €**",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Payer via Paysafecard", url=LIEN_PAIEMENT)]])
        )

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    await app.initialize()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await app.start()
    while True: await asyncio.sleep(3600)

def main():
    try: loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == '__main__':
    main()
