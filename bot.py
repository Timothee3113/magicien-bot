import logging
import datetime
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
LIEN_PAIEMENT = "https://paysafecard.com"

MATCHS_DU_JOUR = [
    {"sport": "🏀 BASKETBALL (WNBA)", "rencontre": "Las Vegas Aces vs New York Liberty", "intitule": "Plus de 164.5 points", "cote": "1.85", "mise": "35 €"},
    {"sport": "⚾ BASEBALL (MLB)", "rencontre": "New York Yankees vs Boston Red Sox", "intitule": "Victoire New York Yankees", "cote": "1.68", "mise": "50 €"}
]

def generer_message():
    date_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    msg = f"🧙‍♂️ 🟩 **[LE MAGICIEN DES PRONOS] — {date_jour}**\n========================================\n\n"
    for i, p in enumerate(MATCHS_DU_JOUR, 1):
        msg += f"📊 **Pari n°{i} — {p['sport']}**\n⚔️ Match : **{p['rencontre']}**\n🎯 **Pari :** `{p['intitule']}`\n📊 **Cote :** `{p['cote']}` | 💰 **Mise : {p['mise']}**\n\n"
    msg += "========================================\n"
    msg += f"🔒 **ACCÈS VIP (20€ via [Paysafecard](https://paysafecard.com))**"
    return msg

def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Actualiser", callback_data="refresh")],
        [InlineKeyboardButton("💎 VIP (20€)", callback_data="vip")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bienvenue chez Le Magicien des Pronos !")
    await update.message.reply_text(generer_message(), parse_mode="Markdown", reply_markup=get_keyboard())

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await query.edit_message_text(text=generer_message(), parse_mode="Markdown", reply_markup=get_keyboard())
    elif query.data == "vip":
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"💎 VIP : {LIEN_PAIEMENT}", parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.run_polling()

if __name__ == "__main__":
    main()
