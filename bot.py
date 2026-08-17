import os
import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import telebot

# 1. Configuration des logs pour suivre l'activité sur le tableau de bord Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 Récupération du Token et de l'URL publique de Render
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
BOT_URL = os.environ.get("RENDER_EXTERNAL_URL") 

# Initialisation sécurisée du bot et du micro-serveur Flask
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# 2. Extracteur de Données Pronosoft (Entièrement corrigé)
def get_pronosoft_data():
    url = "https://pronosoft.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # Base de données de secours (Fallback) si le site bloque la requête
    fallback_matches = [
        {"home": "Brøndby", "away": "Sønderjyske", "1": 1.32, "N": 4.55, "2": 6.30},
        {"home": "La Corogne", "away": "Elche", "1": 2.25, "N": 3.10, "2": 3.50},
        {"home": "Cardiff", "away": "Wrexham", "1": 2.30, "N": 3.30, "2": 2.65}
    ]
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return fallback_matches
            
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []
        rows = soup.find_all('tr', class_=['even', 'odd'])
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 5:
                # Correction du crash : on extrait le texte cellule par cellule
                match_text = cols[1].text.strip() if len(cols) > 1 else ""
                teams = match_text.split(' - ')
                if len(teams) == 2:
                    try:
                        matches.append({
                            "home": teams[0].strip(),
                            "away": teams[1].strip(),
                            "1": float(cols[2].text.replace(',', '.').strip()),
                            "N": float(cols[3].text.replace(',', '.').strip()),
                            "2": float(cols[4].text.replace(',', '.').strip())
                        })
                    except:
                        continue
        return matches if matches else fallback_matches
    except Exception as e:
        logger.error(f"Erreur scraping Pronosoft : {e}")
        return fallback_matches

# 3. Base de Données Betclic de simulation
def get_betclic_sports_data():
    return {
        "basketball": {
            "match": "Indiana Fever vs Phoenix Mercury",
            "market": "Performance : Caitlin Clark marque +19.5 points",
            "cote": 1.90,
            "fiabilite": 5,
            "value": 7.2,
            "context": "Stats & Forme : Clark tourne à 21.2 points de moyenne sur les 5 derniers matchs. Phoenix affiche d'importantes faiblesses sur les lignes extérieures."
        },
        "baseball": {
            "match": "Toronto Blue Jays vs New York Yankees",
            "market": "Victoire de New York Yankees",
            "cote": 1.72,
            "fiabilite": 4,
            "value": 5.5,
            "context": "Actualité Lanceurs : Gerrit Cole débute sur la butte pour les Yankees avec une ERA de 2.85. Toronto est en baisse d'efficacité offensive."
        }
    }

# 4. Générateur Automatique du Rapport Algorithmique
def generate_report():
    foot_data = get_pronosoft_data()
    brondby_match = next((m for m in foot_data if "Brøndby" in m['home']), foot_data[0])
    
    extra_sports = get_betclic_sports_data()
    basket = extra_sports["basketball"]
    baseball = extra_sports["baseball"]

    def calc_mise(value_index):
        return round(min(35 + (value_index * 1.5), 50.0), 2)

    return (
        "🧙‍♂️ 🟩 ALGORITHME MULTI-SPORTS TOTAL — 17/08/2026\n"
        "========================================\n\n"
        "📊 Pari Simple n°1 — FOOTBALL\n"
        f"⚔️ Rencontre : {brondby_match['home']} vs {brondby_match['away']}\n"
        f"🎯 Intitulé du Pari : Victoire de {brondby_match['home']} (Pari 1N2)\n"
        f"📊 Cote Betclic : {brondby_match['1']} | ⚠️ Fiabilité : ⭐️⭐️⭐️⭐️⭐️\n"
        "📈 Indice de Value : +6.2% | 💰 Mise conseillée : 40.00 €\n"
        f"📝 Actu & Forme : {brondby_match['home']} reste sur une solide série à domicile.\n\n"
        "📊 Pari Simple n°2 — BASKETBALL (WNBA)\n"
        f"⚔️ Rencontre : {basket['match']}\n"
        f"🎯 Intitulé du Pari : {basket['market']}\n"
        f"📊 Cote Betclic : {basket['cote']} | ⚠️ Fiabilité : {'⭐️' * basket['fiabilite']}\n"
        f"📈 Indice de Value : +{basket['value']}% | 💰 Mise conseillée : {calc_mise(basket['value'])} €\n"
        f"📝 Actu & Forme : {basket['context']}\n\n"
        "📊 Pari Simple n°3 — BASEBALL (MLB)\n"
        f"⚔️ Rencontre : {baseball['match']}\n"
        f"🎯 Intitulé du Pari : {baseball['market']}\n"
        f"📊 Cote Betclic : {baseball['cote']} | ⚠️ Fiabilité : {'⭐️' * baseball['fiabilite']}\n"
        f"📈 Indice de Value : +{baseball['value']}% | 💰 Mise conseillée : {calc_mise(baseball['value'])} €\n"
        f"📝 Actu & Forme : {baseball['context']}\n\n"
        "========================================\n"
        "🚀 LE COMBINÉ MULTI-SPORTS SAFE :\n"
        "----------------------------------------\n"
        f"1️⃣ {brondby_match['home']} ➔ Victoire ({brondby_match['1']})\n"
        f"2️⃣ {baseball['match']} ➔ {baseball['market']} ({baseball['cote']})\n\n"
        f"📊 Cote Totale Combiné : {round(brondby_match['1'] * baseball['cote'], 2)} | 💰 Mise : 25 €\n"
        "========================================\n"
        "🔒 ACCÈS PREMIUM VIP — MULTI-SPORTS H24\n"
        "💶 Prix Unique : 20.00 €\n"
        "💳 Lien : https://paysafecard.com\n"
        "========================================\n"
        "⚠️ Mises simples bridées à 50€ maximum pour sécurité."
    )

# 5. Gestionnaire de commandes Telegram (/algo)
@bot.message_handler(commands=['algo'])
def handle_algo(message):
    try:
        report_text = generate_report()
        bot.reply_to(message, report_text, disable_web_page_preview=True)
        logger.info(f"Rapport envoyé à l'utilisateur {message.chat.id}")
    except Exception as e:
        logger.error(f"Erreur envoi message : {e}")

# 6. Routage HTTP Flask pour la réception des Webhooks de Telegram
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

@app.route('/')
def home():
    return "Bot de calcul en ligne et fonctionnel !", 200

# 7. Exécution et liaison automatique du Webhook
if __name__ == "__main__":
    if BOT_URL:
        bot.remove_webhook()
        bot.set_webhook(url=BOT_URL + '/' + TOKEN)
        logger.info(f"Webhook lié avec succès à l'adresse : {BOT_URL}")
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

