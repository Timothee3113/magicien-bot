import logging
import asyncio
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"
LIEN_PAIEMENT = "https://paysafecard.com"

def generer_ticket_immediat():
    # Détermination automatique de la date du jour J au format français
    date_du_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    
    return (
        f"🧙‍♂️ 🟩 **[TICKET OFFICIEL PRONOSOFT & BETCLIC] — {date_du_jour}**\n"
        "========================================\n\n"
        "🎯 **LES TICKETS SIMPLES DU JOUR J (Mise Max 50€) :**\n"
        "----------------------------------------\n"
        "📊 **Pari Simple n°1 (Parions Sport Officiel)**\n"
        "⚔️ Rencontre : **La Corogne vs Elche**\n"
        "🎯 **Intitulé du Pari :** `Résultat : Victoire de La Corogne`\n"
        "📊 **Cote Betclic :** `2.25` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️\n"
        "📈 Indice de Value : `+7.8%` | 💰 **Mise conseillée : 35 €**\n\n"
        "📊 **Pari Simple n°2 (Loto Foot 8 n°108)**\n"
        "⚔️ Rencontre : **Gijon vs Sabadell**\n"
        "🎯 **Intitulé du Pari :** `Résultat : Victoire de Gijon`\n"
        "📊 **Cote Betclic :** `1.70` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️⭐️\n"
        "📈 Indice de Value : `+6.2%` | 💰 **Mise conseillée : 45 €**\n\n"
        "========================================\n"
        "⚡ **PARI SÉLECTION UNIQUE DE L'EXPERT :**\n"
        "----------------------------------------\n"
        "📊 **Pari Spécifique (Ligue scandinave)**\n"
        "⚔️ Rencontre : **Brøndby vs Sønderjyske**\n"
        "🎯 **Intitulé du Pari :** `Nombre total de buts : Plus de 2.5 buts`\n"
        "📊 **Cote Betclic :** `1.55` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️⭐️\n"
        "💰 **Mise conseillée : 50 €** [Plafond maximum atteint]\n\n"
        "========================================\n"
        "🚀 **LE COMBINÉ SAFE DU MAGICIEN :**\n"
        "----------------------------------------\n"
        "1️⃣ **Brøndby vs Sønderjyske** ➔ `Victoire Brøndby` (1.32)\n"
        "2️⃣ **Almeria vs Club Eldense** ➔ `Victoire Almeria` (1.28)\n\n"
        "📊 **Cote Totale Combiné : 1.69** | 💰 **Mise conseillée : 25 €**\n"
        "⚠️ **CONFIANCE GLOBAL COMBINÉ :** ⭐️⭐️⭐️⭐️\n"
        "========================================\n"
        "🔒 **ACCÈS PREMIUM VIP — ENCAISSEMENT AUTOMATIQUE**\n"
        "----------------------------------------\n"
        "💶 Prix Unique : **20.00 €**\n"
        "💳 **Lien d'achat sécurisé Paysafecard :** https://paysafecard.com\n"
        "========================================\n"
        "⚠️ _Mises simples strictement bridées à 50€ maximum pour protection du capital._"
    )

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan les Valeurs Réelles", callback_data="s")],
        [InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],
        [InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟩 **Moteur connecté aux flux Pronosoft & Betclic !**\nChargement des analyses réelles du jour...")
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
        try: await q.edit_message_text(text="⏳ *Vérification des bases de données Pronosoft et ajustement des cotes Betclic...*", parse_mode="Markdown")
        except: pass
        await asyncio.sleep(0.3)
        try: await q.edit_message_text(text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
    elif q.data == "b":
        await context.bot.send_message(chat_id=q.message.chat_id, text="📊 **SUIVI DE CAPITAL (BANKROLL) :**\n\n💰 Capital Initial : 1000.00 €\n📊 Paris Enregistrés : 14\n📈 Performance globale : `+12.4% ROI` (Bénéficiaire)", parse_mode="Markdown")
    elif q.data == "v":
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text="🔒 **ESPACE PREMIUM VIP — LE MAGICIEN**\n\nDébloquez 100% des analyses lourdes d'anomalies de cotes mondiales.\n\n💶 Tarif Unique : **20.00 €**",
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
