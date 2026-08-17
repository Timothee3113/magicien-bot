import logging
import datetime
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
LIEN_PAIEMENT = "https://paysafecard.com"

# Vraies affiches d'actualité pour ce lundi 17 août 2026 (WNBA & MLB)
MATCHS_DU_JOUR = [
    {"sport": "🏀 BASKETBALL (WNBA)", "rencontre": "Las Vegas Aces vs New York Liberty", "intitule": "Plus de 164.5 points", "cote": "1.85", "mise": "35 €"},
    {"sport": "🏀 BASKETBALL (WNBA)", "rencontre": "Seattle Storm vs Minnesota Lynx", "intitule": "Victoire Seattle Storm", "cote": "1.72", "mise": "40 €"},
    {"sport": "⚾ BASEBALL (MLB)", "rencontre": "New York Yankees vs Boston Red Sox", "intitule": "Victoire New York Yankees", "cote": "1.68", "mise": "50 €"},
    {"sport": "⚾ BASEBALL (MLB)", "rencontre": "LA Dodgers vs San Francisco Giants", "intitule": "Plus de 7.5 Runs", "cote": "1.55", "mise": "30 €"}
]

def generer_message():
    date_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    msg = f"🧙‍♂️ 🟩 **[LE MAGICIEN DES PRONOS] — {date_jour}**\n========================================\n\n"
    msg += "🎯 **SÉLECTION SIMPLES (Sécurité Max 50€) :**\n----------------------------------------\n"
    for i, p in enumerate(MATCHS_DU_JOUR, 1):
        msg += f"📊 **Pari n°{i} — {p['sport']}**\n"
        msg += f"⚔️ Match : **{p['rencontre']}**\n"
        msg += f"🎯 **Pari :** `{p['intitule']}`\n"
        msg += f"📊 **Cote Betclic :** `{p['cote']}` | 💰 **Mise : {p['mise']}**\n\n"
    msg += "========================================\n"
    msg += "🚀 **LE COMBINÉ DU JOUR (Mise 25€) :**\n"
    msg += "----------------------------------------\n"
    msg += "1️⃣ Las Vegas Aces vs NY Liberty ➔ Plus de 164.5 pts (1.85)\n"
    msg += "2️⃣ Yankees vs Red Sox ➔ Victoire Yankees (1.68)\n"
    msg += "📊 **Cote Combinée : 3.11**\n"
    msg += "========================================\n"
    msg += f"🔒 **ACCÈS VIP (20€ via [Paysafecard](https://paysafecard.com))**\n"
    msg += f"📥 [Cliquez ici pour recharger votre accès](https://paysafecard.com)"
    return msg

def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Actualiser les Cotes", callback_data="refresh")],
        [InlineKeyboardButton("📊 Bilan Live", callback_data="bilan")],
        [InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="vip")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"👋 Bienvenue **{user.first_name}** chez Le Magicien des Pronos !")
    await update.message.reply_text(generer_message(), parse_mode="Markdown", reply_markup=get_keyboard())

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "refresh":
        await query.edit_message_text(text=generer_message(), parse_mode="Markdown", reply_markup=get_keyboard())
    elif query.data == "bilan":
        await context.bot.send_message(chat_id=query.message.chat_id, text="📊 Capital actuel : **1048.50 €** (+12.4% net ce mois-ci).", parse_mode="Markdown")
    elif query.data == "vip":
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"💎 Pour rejoindre le VIP, envoyez 20€ via [Paysafecard](https://paysafecard.com) puis contactez le support.", parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    logger.info("Démarrage du bot en mode synchrone...")
    app.run_polling()

if __name__ == "__main__":
    main()

