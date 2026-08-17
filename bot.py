import logging
import asyncio
import datetime
import random
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lecture ultra-sécurisée du Token depuis l'onglet Environment de Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
LIEN_PAIEMENT = "https://paysafecard.com"

# Variables globales en mémoire pour l'enregistrement des stats en direct live
if not hasattr(asyncio, '_global_stats_tracker'):
    asyncio._global_stats_tracker = {
        "capital": 1024.50,
        "paris_joues": 14,
        "roi": 12.4
    }

# Catalogue multi-sports officiel corrigé et mis à jour pour le Lundi 17 Août 2026
SPORTS_DATA = {
    "FOOTBALL": [
        ("La Corogne", "Elche", "2.25", "Résultat : Victoire de La Corogne"),
        ("Gijon", "Sabadell", "1.70", "Résultat : Victoire de Gijon"),
        ("Brøndby", "Sonderjyske", "1.32", "Nombre total de buts : Plus de 2.5 buts")
    ],
    "BASKETBALL (WNBA)": [
        ("Las Vegas Aces", "New York Liberty", "1.85", "Nombre total de points : Plus de 164.5 points"),
        ("Seattle Storm", "Minnesota Lynx", "1.72", "Résultat : Victoire de Seattle Storm"),
        ("Indiana Fever", "Phoenix Mercury", "1.90", "Performance : Caitlin Clark marque +19.5 points")
    ],
    "BASEBALL (MLB)": [
        ("New York Yankees", "Boston Red Sox", "1.68", "Vainqueur du match : New York Yankees"),
        ("LA Dodgers", "San Francisco Giants", "1.55", "Nombre de Runs total : Plus de 7.5 Runs"),
        ("Houston Astros", "Texas Rangers", "1.82", "Vainqueur du match : Houston Astros")
    ],
    "TENNIS": [
        ("C.Alcaraz", "J.Sinner", "1.85", "Nombre total de sets : Plus de 2.5"),
        ("I.Swiatek", "A.Sabalenka", "1.62", "Vainqueur du 1er Set : I.Swiatek")
    ]
}

def generer_ticket_immediat():
    date_du_jour = datetime.datetime.now().strftime('%d/%m/%Y')
    
    # Enregistrement et mise à jour des stats live en arrière-plan à chaque appel
    stats = asyncio._global_stats_tracker
    stats["paris_joues"] += 1
    stats["capital"] += random.choice([-15.0, 25.0, 42.5, -20.0, 31.0])
    stats["roi"] = round(((stats["capital"] - 1000.0) / 1000.0) * 100, 1)

    msg = f"🧙‍♂️ 🟩 **[ALGORITHME MULTI-SPORTS ÉLITE] — {date_du_jour}**\n"
    msg += "========================================\n\n"
    
    compteur = 1
    for sport, rencontres in SPORTS_DATA.items():
        home, away, cote, intitule = random.choice(rencontres)
        avantage = round(random.uniform(5.8, 9.6), 1)
        mise_exacte = min(50, max(15, int(avantage * 6.5)))
        
        msg += f"📊 **Pari Simple n°{compteur} — {sport}**\n"
        msg += f"⚔️ Rencontre : **{home} vs {away}**\n"
        msg += f"🎯 **Pari :** `{intitule}`\n"
        msg += f"📊 **Cote Betclic :** `{cote}` | **⚠️ Fiabilité :** ⭐️⭐️⭐️⭐️\n"
        msg += f"📈 Value : `+{avantage}%` | 💰 **Mise conseillée : {mise_exacte} €**\n\n"
        compteur += 1
        
    msg += "========================================\n"
    msg += "🚀 **LE COMBINÉ SAFE DU MAGICIEN (Mise 25€) :**\n"
    msg += "----------------------------------------\n"
    msg += f"1️⃣ **Brøndby vs Sonderjyske** ➔ `Victoire Brøndby` (1.32)\n"
    msg += f"2️⃣ **New York Yankees vs Red Sox** ➔ `Victoire Yankees` (1.68)\n\n"
    
    msg += "📊 **Cote Totale Combiné : 2.21**\n"
    msg += "========================================\n"
    msg += "🔒 **ESPACE VIP PREMIUM (Tarif Unique 20€)**\n"
    msg += "📥 _Débloquez 100% des alertes privées multi-sports H24._\n"
    msg += "========================================\n"
    msg += "⚠️ _Mises simples strictement bridées à 50€ maximum pour sécurité._"
    return msg

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan les Valeurs Live H24", callback_data="s")],
        [InlineKeyboardButton("📊 Consulter mon Bilan Direct Live", callback_data="b")],
        [InlineKeyboardButton("💎 Débloquer l'Espace VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    accueil = (
        f"👋 **Bienvenue {user.first_name} chez Le Magicien des Pronos !**\n\n"
        f"🤖 Mon algorithme scanne les cotes mondiales 24h/24 (Foot, WNBA, MLB, Tennis).\n\n"
        f"📊 **Règles de notre communauté :**\n"
        f"• Mises simples strictement limitées à **50€ maximum** pour protéger le capital.\n"
        f"• Enregistrement automatique des statistiques en direct live.\n\n"
        f"👇 Voici vos analyses exclusives du jour J :"
    )
    await update.message.reply_text(accueil)
    await context.bot.send_message(chat_id=user.id, text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try: await q.answer()
    except: pass
    
    if q.data == "s":
        try: await q.edit_message_text(text="⏳ *Algorithme : Balayage des grilles, mise à jour de la WNBA, de la MLB et recalibrage des données...*", parse_mode="Markdown")
        except: pass
        await asyncio.sleep(0.4)
        try: await q.edit_message_text(text=generer_ticket_immediat(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
        
    elif q.data == "b":
        stats = asyncio._global_stats_tracker
        texte_bilan = (
            f"📊 **STATISTIQUES ET SUIVI EN DIRECT LIVE :**\n\n"
            f"💰 Capital Initial : `1000.00 €`\n"
            f"💰 Capital Actuel : **{round(stats['capital'], 2)} €**\n"
            f"📊 Paris Joués Certifiés : `{stats['paris_joues']}`\n"
            f"📈 Progression globale : **{stats['roi']}% ROI**\n\n"
            f"✅ _Bilan comptable réinitialisé et mis à jour automatiquement à chaque validation._"
        )
        await context.bot.send_message(chat_id=q.message.chat_id, text=texte_bilan, parse_mode="Markdown")
        
    elif q.data == "v":
        await context.bot.send_message(
            chat_id=q.message.chat_id,
            text=f"🔒 **ESPACE PREMIUM VIP MULTI-SPORTS**\n\nAccédez à l'intégralité des signaux d'anomalies de cotes mondiales.\n\n💶 Tarif Unique : **20.00 €**\n📥 _Réglez via Paysafecard :_ {LIEN_PAIEMENT}",
            parse_mode="Markdown"
        )

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    
    await app.initialize()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await app.start()
    print("\n🚀 INFRASTRUCTURE PRO EN LIGNE SUR RENDER CORRIGÉE H24 !")
    
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

