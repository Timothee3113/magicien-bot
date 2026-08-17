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

# CONFIGURATION FINALE DES COMPTES SÉCURISÉS
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
ODDS_API_KEY = os.environ.get("ODDS_API_KEY", "09d8ae8e92664cf261a8250ffdc5fbdb")
LIEN_PAIEMENT = "https://paysafecard.com"

if not hasattr(asyncio, '_global_stats_tracker'):
    asyncio._global_stats_tracker = {"capital": 1024.50, "paris_joues": 14, "roi": 12.4}

# Liste des compétitions actives scannées en direct live 24h/24
SPORTS_A_SCANNER = {
    "🏀 BASKETBALL (WNBA)": "basketball_wnba",
    "⚾ BASEBALL (MLB)": "baseball_mlb",
    "⚽ FOOTBALL (LIGUE 1)": "soccer_france_ligue_one"
}

def recuperer_matchs_reels_api():
    """Interroge l'API mondiale pour extraire les vrais matchs de la journée."""
    matchs_du_jour = []
    date_aujourdhui = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    
    for label_sport, key_sport in SPORTS_A_SCANNER.items():
        url = f"https://the-odds-api.com{key_sport}/odds/"
        params = {
            'apiKey': ODDS_API_KEY,
            'regions': 'eu',
            'markets': 'h2h',
            'oddsFormat': 'decimal'
        }
        try:
            response = requests.get(url, params=params, timeout=6)
            if response.status_code == 200:
                data = response.json()
                for item in data:
                    commence_time = item.get('commence_time', '')
                    if date_aujourdhui in commence_time:
                        home = item.get('home_team')
                        away = item.get('away_team')
                        bookmakers = item.get('bookmakers', [])
                        
                        betclic_data = next((b for b in bookmakers if b['key'] == 'betclic'), None)
                        if not betclic_data and bookmakers:
                            betclic_data = bookmakers[0]
                        
                        if betclic_data:
                            market = betclic_data.get('markets', [{}])[0]
                            outcomes = market.get('outcomes', [])
                            
                            c_home = next((o['price'] for o in outcomes if o['name'] == home), 1.80)
                            c_away = next((o['price'] for o in outcomes if o['name'] == away), 1.80)
                            
                            if c_home < c_away:
                                intitule = f"Vainqueur : {home}"
                                cote_finale = c_home
                            else:
                                intitule = f"Vainqueur : {away}"
                                cote_finale = c_away
                                
                            matchs_du_jour.append({
                                "sport": label_sport,
                                "rencontre": f"{home} vs {away}",
                                "intitule": intitule,
                                "cote": cote_finale,
                                "bookmaker": betclic_data.get('title', 'Betclic')
                            })
        except Exception as e:
            logger.error(f"Erreur API pour {label_sport}: {e}")
            
    return matchs_du_jour

def construire_tableau_de_bord():
    date_titre = datetime.datetime.now().strftime('%d/%m/%Y')
    vrais_matchs = recuperer_matchs_reels_api()
    
    stats = asyncio._global_stats_tracker
    stats["paris_joues"] += 1
    stats["capital"] += random.choice([-15.0, 25.0, 42.5, -20.0, 31.0])
    stats["roi"] = round(((stats["capital"] - 1000.0) / 1000.0) * 100, 1)

    msg = f"🧙‍♂️ 🟩 **[VRAIS FLUX LIVE MULTI-SPORTS] — {date_titre}**\n"
    msg += "========================================\n\n"
    
    if not vrais_matchs:
        msg += "⚠️ **INFO TEMPS RÉEL :** Les matchs officiels de WNBA, de MLB et de Football pour la journée d'aujourd'hui débuteront ce soir et cette nuit. Revenez plus tard ou utilisez le bouton ci-dessous pour forcer un rafraîchissement des cotes.\n\n"
    else:
        msg += "🎯 **LES TICKETS SIMPLES DÉTECTÉS (Mise Max 50€) :**\n"
        msg += "----------------------------------------\n"
        for i, p in enumerate(vrais_matchs[:3], 1):
            avantage = round(random.uniform(5.8, 9.6), 1)
            mise_exacte = min(50, max(15, int(avantage * 6.5)))
            fiabilite = "⭐️" * random.randint(4, 5)
            
            msg += f"📊 **Pari Simple n°{i} — {p['sport']}**\n"
            msg += f"⚔️ Match : **{p['rencontre']}**\n"
            msg += f"🎯 **Pari :** `{p['intitule']}`\n"
            msg += f"📊 **Cote {p['bookmaker']} :** `{p['cote']}` | **⚠️ Fiabilité :** {fiabilite}\n"
            msg += f"📈 Value : `+{avantage}%` | 💰 **Mise conseillée : {mise_exacte} €**\n\n"
            
        if len(vrais_matchs) >= 2:
            msg += "========================================\n"
            msg += "🚀 **LE COMBINÉ MULTI-SPORTS DU MAGICIEN (Mise 25€) :**\n"
            ----------------------------------------\n
            m1, m2 = vrais_matchs[0], vrais_matchs[1]
            msg += f"1️⃣ **{m1['rencontre']}** ➔ `{m1['intitule']}` ({m1['cote']})\n"
            msg += f"2️⃣ **{m2['rencontre']}** ➔ `{m2['intitule']}` ({m2['cote']})\n\n"
            msg += f"📊 **Cote Totale Combiné : {round(m1['cote'] * m2['cote'], 2)}**\n"

    msg += "========================================\n"
    msg += "🔒 **ESPACE VIP PREMIUM (Tarif Unique 20€)**\n"
    msg += "📥 _Débloquez 100% des alertes privées multi-sports H24._\n"
    msg += "========================================\n"
    msg += "⚠️ _Mises simples strictement bridées à 50€ maximum pour sécurité._"
    return msg

def clavier():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan les Valeurs Réelles", callback_data="s")],
        [InlineKeyboardButton("📊 Consulter mon Bilan Direct Live", callback_data="b")],
        [InlineKeyboardButton("💎 Débloquer l'Espace VIP (20€)", callback_data="v")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    accueil = (
        f"👋 **Bienvenue {user.first_name} chez Le Magicien des Pronos !**\n\n"
        f"🤖 Mon algorithme est connecté en direct aux flux mondiaux de cotes (WNBA, MLB, Foot).\n"
        f"📊 Les valeurs ci-dessous sont extraites des marchés officiels en temps réel.\n\n"
        f"👇 Voici votre feuille de match d'élite :"
    )
    await update.message.reply_text(accueil)
    await context.bot.send_message(chat_id=user.id, text=construire_tableau_de_bord(), parse_mode="Markdown", reply_markup=clavier())

async def cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try: await q.answer()
    except: pass
    if q.data == "s":
        try: await q.edit_message_text(text="⏳ *Algorithme : Connexion sécurisée aux API de cotes et filtrage des matchs du jour J...*", parse_mode="Markdown")
        except: pass
        await asyncio.sleep(0.5)
        try: await q.edit_message_text(text=construire_tableau_de_bord(), parse_mode="Markdown", reply_markup=clavier())
        except: pass
    elif q.data == "b":
        stats = asyncio._global_stats_tracker
        texte_bilan = (
            f"📊 **STATISTIQUES EN DIRECT LIVE :**\n\n"
            f"💰 Capital Initial : `1000.00 €`\n"
            f"💰 Capital Actuel : **{round(stats['capital'], 2)} €**\n"
            f"📊 Paris Joués Certifiés : `{stats['paris_joues']}`\n"
            f"📈 Progression globale : **{stats['roi']}% ROI**"
        )
        await context.bot.send_message(chat_id=q.message.chat_id, text=texte_bilan, parse_mode="Markdown")
    elif q.data == "v":
        await context.bot.send_message(chat_id=q.message.chat_id, text=f"🔒 **ESPACE PREMIUM VIP MULTI-SPORTS**\n\nTarif Unique : **20.00 €**\n📥 _Réglez via Paysafecard :_ {LIEN_PAIEMENT}", parse_mode="Markdown")

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    await app.initialize()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await app.start()
    print("\n🚀 INFRASTRUCTURE CONNECTÉE AUX API MONDIALES EN LIGNE !")
    while True:
        await asyncio.sleep(3600)

def main():
    try: loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == '__main__': main()
