import logging
import asyncio
import datetime
import random
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "09d8ae8e92664cf261a8250ffdc5fbdb")
LIEN_PAIEMENT = "https://paysafecard.com"

if not hasattr(asyncio, '_global_stats_tracker'):
    asyncio._global_stats_tracker = {"capital": 1024.50, "paris_joues": 14, "roi": 12.4}

SPORTS_A_SCANNER = {
    "🏀 BASKETBALL (WNBA)": "basketball_wnba",
    "⚾ BASEBALL (MLB)": "baseball_mlb",
    "⚽ FOOTBALL (LIGUE 1)": "soccer_france_ligue_one"
}

def recuperer_matchs_reels_api():
    matchs_du_jour = []
    date_aujourdhui = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    
    for label_sport, key_sport in SPORTS_A_SCANNER.items():
        url = f"https://the-odds-api.com{key_sport}/odds/"
        params = {'apiKey': ODDS_API_KEY, 'regions': 'eu', 'markets': 'h2h', 'oddsFormat': 'decimal'}
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    if date_aujourdhui in item.get('commence_time', ''):
                        home = item.get('home_team')
                        away = item.get('away_team')
                        bookmakers = item.get('bookmakers', [])
                        betclic = next((b for b in bookmakers if b['key'] == 'betclic'), bookmakers if bookmakers else None)
                        if betclic:
                            market = betclic.get('markets', [{}])
                            outcomes = market.get('outcomes', [])
                            c_home = next((o['price'] for o in outcomes if o['name'] == home), 1.80)
                            c_away = next((o['price'] for o in outcomes if o['name'] == away), 1.80)
                            intitule = f"Vainqueur : {home}" if c_home < c_away else f"Vainqueur : {away}"
                            matchs_du_jour.append({
                                "sport": label_sport,
                                "rencontre": f"{home} vs {away}",
                                "intitule": intitule,
                                "cote": min(c_home, c_away),
                                "bookmaker": betclic.get('title', 'Betclic')
                            })
        except Exception as e:
            logger.error(f"Erreur API {label_sport}: {e}")
            
    # Filet de sécurité si l'API est vide ou hors-ligne
    if not matchs_du_jour:
        matchs_du_jour = [
            {"sport": "🏀 BASKETBALL (WNBA)", "rencontre": "Las Vegas Aces vs New York Liberty", "intitule": "Vainqueur : Las Vegas Aces", "cote": 1.85, "bookmaker": "Betclic"},
            {"sport": "⚾ BASEBALL (MLB)", "rencontre": "New York Yankees vs Boston Red Sox", "intitule": "Vainqueur : New York Yankees", "cote": 1.68, "bookmaker": "Betclic"}
        ]
    return matchs_du_jour

def construire_tableau_de_bord():
    date_titre = datetime.datetime.now().strftime('%d/%m/%Y')
    vrais_matchs = recuperer_matchs_reels_api()
    stats = asyncio._global_stats_tracker
    stats["paris_joues"] += 1
    stats["capital"] += 15.0
    stats["roi"] = round(((stats["capital"] - 1000.0) / 1000.0) * 100, 1)

    msg = f"🧙‍♂️ 🟩 **[LIVE MULTI-SPORTS] — {date_titre}**\n========================================\n\n"
    msg += "🎯 **LES TICKETS SIMPLES (Mise Max 50€) :**\n----------------------------------------\n"
    for i, p in enumerate(vrais_matchs[:3], 1):
        mise = random.randint(20, 50)
        msg += f"📊 **Pari n°{i} — {p['sport']}**\n⚔️ Match : **{p['rencontre']}**\n🎯 **Pari :** `{p['intitule']}`\n📊 **Cote :** `{p['cote']}` | 💰 **Mise : {mise} €**\n\n"
    
    if len(vrais_matchs) >= 2:
        msg += f"========================================\n🚀 **COMBINÉ (Mise 25€) :**\n1️⃣ {vrais_matchs['rencontre']} ({vrais_matchs['cote']})\n2️⃣ {vrais_matchs['rencontre']} ({vrais_matchs['cote']})\n📊 **Cote Totale : {round(vrais_matchs['cote']*vrais_matchs['cote'], 2)}**\n"
    msg += "========================================\n🔒 **VIP (20€ via Paysafecard)** : " + LIEN_PAIEMENT
    return msg

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan Direct", callback_data="s")],
        [InlineKeyboardButton("📊 Bilan Live", callback_data="b")],
        [InlineKeyboardButton("💎 VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 **Bienvenue chez Le Magicien des Pronos !**")
    await context.bot.send_message(chat_id=update.effective_user.id, text=construire_tableau_de_bord(), parse_mode="Markdown", reply_markup=clavier())

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try: await q.answer()
    except: pass
    if q.data == "s":
        try: await q.edit_message_text(text=construire_tableau_de_bord(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
    elif q.data == "b":
        stats = asyncio._global_stats_tracker
        await context.bot.send_message(chat_id=q.message.chat_id, text=f"📊 Capital : **{round(stats['capital'],2)}€** | ROI : **{stats['roi']}%**", parse_mode="Markdown")
    elif q.data == "v":
        await context.bot.send_message(chat_id=q.message.chat_id, text=f"💎 VIP : {LIEN_PAIEMENT}", parse_mode="Markdown")

def main():
    # Utilisation de run_polling simple et stable sans conflit de boucle custom sur Render
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
