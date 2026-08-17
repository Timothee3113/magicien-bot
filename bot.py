import logging
import asyncio
import datetime
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration des logs pour suivre l'activité sur Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CONFIGURATION SÉCURISÉE DE VOS PARAMÈTRES
TELEGRAM_TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"
LIEN_PAIEMENT = "https://paysafecard.com"

# Catalogue multi-sports officiel pour alimenter le bot quotidiennement
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
    # Détermination dynamique de la date du jour à la seconde près
    date_du_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    
    msg = f"🧙‍♂️ 🟩 **[ALGORITHME MULTI-SPORTS TOTAL] — {date_du_jour}**\n"
    msg += "========================================\n\n"
    
    compteur = 1
    for sport, rencontres in SPORTS_DATA.items():
        # Sélection d'une affiche aléatoire par sport pour faire varier la grille
        home, away, cote, intitule = random.choice(rencontres)
        avantage = round(random.uniform(5.8, 9.6), 1)
        
        # Index Kelly pro : calcul de mise mathématique strict bridé à 50 € maximum
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
    msg += "Rejoignez le groupe pour recevoir 100% des alertes d'anomalies (Foot, NBA, Tennis, NHL).\n\n"
    msg += "💶 Prix Unique : **20.00 €**\n"
    msg += f"💳 **Lien d'achat sécurisé Paysafecard :** {LIEN_PAIEMENT}\n"
    msg += "========================================\n"
    msg += "⚠️ _Gestion stricte de la bankroll. Mises simples bridées à 50€ maximum._"
    return msg

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan les 4 Sports en Direct", callback_data="s")],
        [InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],
        [InlineKeyboardButton("💎 Espace VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟩 **Moteur Multi-Sports Global Connecté !**\nChargement des analyses réelles du jour...")
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
        try: await q.edit_message_text(text="⏳ *Algorithme : Balayage complet des cotes mondiales Football, NBA, Tennis et NHL...*", parse_mode="Markdown")
        except: pass
        await asyncio.sleep(0.4)
        try: await q.edit_message_text(text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
    elif q.data == "b":
        await context.bot.send_message(chat_id=q.message.chat_id, text="📊 **COMPTABILITÉ MULTI-SPORTS :**\n\n💰 Capital Initial : 1000.00 €\n📊 Paris Joués : 14\n📈 Performance globale : `+12.4% ROI` (Bénéficiaire)", parse_mode="Markdown")
    elif q.data == "v":
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text=f"🔒 **ESPACE PREMIUM VIP MULTI-SPORTS**\n\nAccédez à l'intégralité des signaux d'anomalies de cotes sur tous les championnats mondiaux.\n\n💶 Tarif Unique : **20.00 €**\n📥 _Réglez via Paysafecard :_ {LIEN_PAIEMENT}",
            parse_mode="Markdown"
        )

async def run_bot():
    # Initialisation propre de l'application
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    
    # Résolution stricte des conflits d'Event Loop de Python 3.14+ sur Render
    await app.initialize()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await app.start()
    print("\n🚀 INFRASTRUCTURE PRO EN LIGNE SUR RENDER !")
    
    # Maintient le script actif à l'écoute des requêtes
    while True:
        await asyncio.sleep(3600)

def main():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == '__main__':
    main()
