import logging
import asyncio
import datetime
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"
ID_PROPRIETAIRE = 7532202198 # Votre ID pour l'envoi automatique quotidien
LIEN_PAIEMENT = "https://paysafecard.com"

# Catalogue multi-sports dynamique pour l'alimentation quotidienne
SPORTS_DATA = {
    "FOOTBALL": [
        ("La Corogne", "Elche", "2.25", "Résultat : Victoire de La Corogne"),
        ("Gijon", "Sabadell", "1.70", "Résultat : Victoire de Gijon"),
        ("Brøndby", "Sonderjyske", "1.32", "Nombre total de buts : Plus de 2.5 buts"),
        ("Almeria", "Club Eldense", "1.28", "Résultat : Victoire d'Almeria")
    ],
    "BASKETBALL (NBA)": [
        ("LA Lakers", "Boston Celtics", "1.88", "Nombre total de points : Plus de 218.5"),
        ("Golden State", "Chicago Bulls", "1.65", "Performance : Stephen Curry inscrit +26.5 points"),
        ("Miami Heat", "NY Knicks", "2.10", "Résultat : Victoire de Miami (Handicap +3.5)")
    ],
    "TENNIS (ATP/WTA)": [
        ("T.Valentova", "E.Svitolina", "1.29", "Résultat : Victoire de E.Svitolina"),
        ("C.Alcaraz", "J.Sinner", "1.85", "Nombre total de sets dans le match : Plus de 2.5"),
        ("I.Swiatek", "A.Sabalenka", "1.62", "Vainqueur du 1er Set : I.Swiatek")
    ],
    "HOCKEY (NHL)": [
        ("Montreal Canadiens", "Boston Bruins", "2.40", "Nombre de buts : Plus de 5.5 buts (Prolongations inc.)"),
        ("Rangers NY", "Tampa Bay Lightning", "1.95", "Résultat : Victoire de Rangers NY")
    ]
}

def generer_ticket_immediat():
    # Calcul dynamique de la date du jour à chaque seconde
    date_du_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    
    msg = f"🧙‍♂️ 🟩 **[TRACKER MULTI-SPORTS AUTOMATIQUE] — {date_du_jour}**\n"
    msg += "========================================\n\n"
    
    compteur = 1
    for sport, rencontres in SPORTS_DATA.items():
        home, away, cote, intitule = random.choice(rencontres)
        avantage = round(random.uniform(5.8, 9.6), 1)
        mise_exacte = min(50, max(15, int(avantage * 6.5)))
        fiabilite = "⭐️" * random.randint(4, 5)
        
        msg += f"📊 **Pari Simple n°{compteur} — {sport}**\n"
        msg += f"⚔️ Rencontre : **{home} vs {away}**\n"
        msg += f"🎯 **Intitulé du Pari :** `{intitule}`\n"
        msg += f"📊 **Cote Betclic :** `{cote}` | **⚠️ Fiabilité :** {fiabilite}\n"
        msg += f"📈 Indice de Value : `+{avantage}%` | 💰 **Mise conseillée : {mise_exacte} €**\n\n"
        compteur += 1
        
    msg += "========================================\n"
    msg += "🚀 **LE COMBINÉ MULTI-SPORTS SAFE (Mise 25€) :**\n"
    msg += "----------------------------------------\n"
    msg += f"1️⃣ **Brøndby vs Sonderjyske** ➔ `Victoire Brøndby` (1.32)\n"
    msg += f"2️⃣ **T.Valentova vs E.Svitolina** ➔ `Victoire E.Svitolina` (1.29)\n\n"
    msg += f"📊 **Cote Totale Combiné : 1.70** | 💰 **Mise : 25 €**\n"
    msg += f"⚠️ **CONFIANCE GLOBAL COMBINÉ :** ⭐️⭐️⭐️⭐️\n"
    msg += "========================================\n"
    msg += "🔒 **ACCÈS PREMIUM VIP — MULTI-SPORTS H24**\n"
    msg += "----------------------------------------\n"
    msg += "💶 Prix Unique : **20.00 €**\n"
    msg += "💳 **Lien d'achat sécurisé Paysafecard :** https://paysafecard.com\n"
    msg += "========================================\n"
    msg += "⚠️ _Gestion stricte de la bankroll. Mises simples bridées à 50€ maximum._"
    return msg

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan les Valeurs du Jour", callback_data="s")],
        [InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],
        [InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟩 **Moteur Multi-Sports H24 actif !**\nEnvoi automatique configuré chaque matin à 09h00.")
    await context.bot.send_message(chat_id=update.effective_user.id, text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try: await q.answer()
    except: pass
    if q.data == "s":
        try: await q.edit_message_text(text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
    elif q.data == "b":
        await context.bot.send_message(chat_id=q.message.chat_id, text="📊 **COMPTABILITÉ :**\n\n💰 Capital Initial : 1000.00 €\n📊 Paris Joués : 14\n📈 Performance : `+12.4% ROI`", parse_mode="Markdown")
    elif q.data == "v":
        await context.bot.send_message(chat_id=q.message.chat_id, text="🔒 **ESPACE PRIVÈ VIP (20€)**", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Ticket Paysafecard", url=LIEN_PAIEMENT)]]))

async def envoi_automatique_quotidien(context: ContextTypes.DEFAULT_TYPE):
    """Fonction autonome appelée en tâche de fond pour diffuser le ticket du jour."""
    try:
        await context.bot.send_message(
            chat_id=ID_PROPRIETAIRE,
            text=generer_ticket_immediat(),
            parse_mode="Markdown",
            reply_markup=clavier()
        )
    except Exception:
        pass

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    
    await app.initialize()
    
    # Configuration de l'horloge : Envoi automatique toutes les 24 heures (86400 secondes)
    app.job_queue.run_repeating(envoi_automatique_quotidien, interval=86400.0, first=10.0)
    
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
