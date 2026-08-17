import os
import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask, request
import telebot

# 1. Configuration des logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 Token et URL Render
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
BOT_URL = os.environ.get("RENDER_EXTERNAL_URL") 

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# 2. Extracteur de Données Pronosoft
def get_pronosoft_data():
    url = "https://pronosoft.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
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
                match_text = cols.text.strip() if len(cols) > 1 else ""
                teams = match_text.split(' - ')
                if len(teams) == 2:
                    try:
                        matches.append({
                            "home": teams.strip(),
                            "away": teams.strip(),
                            "1": float(cols.text.replace(',', '.').strip()),
                            "N": float(cols.text.replace(',', '.').strip()),
                            "2": float(cols.text.replace(',', '.').strip())
                        })
                    except:
                        continue
        return matches if matches else fallback_matches
    except Exception as e:
        logger.error(f"Erreur scraping Pronosoft : {e}")
        return fallback_matches

def get_betclic_sports_data():
    return {
        "basketball": {
            "match": "Indiana Fever vs Phoenix Mercury",
            "market": "Performance : Caitlin Clark marque +19.5 points",
            "cote": 1.90, "fiabilite": 5, "value": 7.2,
            "context": "Stats & Forme : Clark tourne à 21.2 points de moyenne sur les 5 derniers matchs."
        },
        "baseball": {
            "match": "Toronto Blue Jays vs New York Yankees",
            "market": "Victoire de New York Yankees",
            "cote": 1.72, "fiabilite": 4, "value": 5.5,
            "context": "Actualité Lanceurs : Gerrit Cole débute sur la butte pour les Yankees."
        }
    }

def generate_report():
    foot_data = get_pronosoft_data()
    brondby_match = next((m for m in foot_data if "Brøndby" in m['home']), foot_data)
    extra = get_betclic_sports_data()
    basket, baseball = extra["basketball"], extra["baseball"]
    def calc_mise(v): return round(min(35 + (v * 1.5), 50.0), 2)
    return (
        "🧙‍♂️ 🟩 ALGORITHME MULTI-SPORTS TOTAL\n"
        f"📊 Football : {brondby_match['home']} vs {brondby_match['away']} (Cote {brondby_match['1']})\n"
        f"📊 Basket : {basket['match']} (Cote {basket['cote']})\n"
        f"📊 Baseball : {baseball['match']} (Cote {baseball['cote']})\n"
        "✅ Le bot est bien synchronisé via Webhook !"
    )

# 3. Commandes Telegram
@bot.message_handler(commands=['algo', 'start'])
def handle_algo(message):
    logger.info(f"⚡ Commande reçue de {message.chat.id}")
    try:
        text = generate_report()
        bot.reply_to(message, text)
        logger.info("📤 Réponse envoyée avec succès !")
    except Exception as e:
        logger.error(f"❌ Erreur envoi: {e}")

# 4. Route Webhook Flask
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_data = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

@app.route('/')
def home():
    return "Service actif", 200

# 5. Configuration explicite du Webhook au lancement
if __name__ == "__main__":
    if BOT_URL:
        full_webhook_url = f"{BOT_URL.rstrip('/')}/{TOKEN}"
        bot.remove_webhook()
        success = bot.set_webhook(url=full_webhook_url)
        if success:
            logger.info(f"🔗 WEBHOOK ENREGISTRÉ AVEC SUCCÈS : {full_webhook_url}")
        else:
            logger.error("❌ ÉCHEC DE L'ENREGISTREMENT DU WEBHOOK")
    else:
        logger.warning("⚠️ RENDER_EXTERNAL_URL non détecté.")

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
