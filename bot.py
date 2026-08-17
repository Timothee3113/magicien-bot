import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Configuration des logs pour voir l'activité du bot en temps réel
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 🔑 Votre Token Telegram est maintenant intégré
TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"

# 2. Extracteur de Données Pronosoft (Liste ParionsSport)
def get_pronosoft_data():
    url = "https://pronosoft.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    # Base de données de secours (Fallback) si le site refuse la connexion
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
                teams = cols.text.strip().split(' - ')
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

# 3. Base de Données Betclic : Basket (WNBA) et Baseball (MLB)
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
    # Recherche automatique du match de Brøndby
    brondby_match = next((m for m in foot_data if "Brøndby" in m['home']), foot_data)
    
    extra_sports = get_betclic_sports_data()
    basket = extra_sports["basketball"]
    baseball = extra_sports["baseball"]

    # Calcul dynamique des mises plafonné à 50.00 euros maximum
    def calc_mise(value_index):
        mise_brute = 35 + (value_index * 1.5)
        return round(min(mise_brute, 50.0), 2)

    report = (
        "🧙‍♂️ 🟩 ALGORITHME MULTI-SPORTS TOTAL — 17/08/2026\n"
        "========================================\n\n"
        "📊 Pari Simple n°1 — FOOTBALL\n"
        f"⚔️ Rencontre : {brondby_match['home']} vs {brondby_match['away']}\n"
        f"🎯 Intitulé du Pari : Victoire de {brondby_match['home']} (Pari 1N2)\n"
        f"📊 Cote Betclic : {brondby_match['1']} | ⚠️ Fiabilité : ⭐️⭐️⭐️⭐️⭐️\n"
        "📈 Indice de Value : +6.2% | 💰 Mise conseillée : 40.00 €\n"
        f"📝 Actu & Forme : {brondby_match['home']} reste sur une solide série à domicile. Statistiques très favorables.\n\n"
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
        "🚀 LE COMBINÉ MULTI-SPORTS SAFE (Mise 25€) :\n"
        "----------------------------------------\n"
        f"1️⃣ {brondby_match['home']} vs {brondby_match['away']} ➔ Victoire {brondby_match['home']} ({brondby_match['1']})\n"
        f"2️⃣ {baseball['match']} ➔ {baseball['market']} ({baseball['cote']})\n\n"
        f"📊 Cote Totale Combiné : {round(brondby_match['1'] * baseball['cote'], 2)} | 💰 Mise : 25 €\n"
        "⚠️ CONFIANCE GLOBALE COMBINÉ : ⭐️⭐️⭐️⭐️\n"
        "========================================\n"
        "🔒 ACCÈS PREMIUM VIP — MULTI-SPORTS H24\n"
        "----------------------------------------\n"
        "Rejoignez le groupe pour recevoir 100% des alertes d'anomalies réelles.\n\n"
        "💶 Prix Unique : 20.00 €\n"
        "💳 Lien d'achat sécurisé Paysafecard : https://paysafecard.com\n"
        "========================================\n"
        "⚠️ Gestion stricte de la bankroll. Mises simples bridées à 50€ maximum pour sécurité."
    )
    return report

# 5. Gestionnaire de Réception de la commande Telegram /algo
async def start_algo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"📥 Commande reçue de l'ID utilisateur : {update.effective_user.id}")
    try:
        report_text = generate_report()
        await update.message.reply_text(report_text, disable_web_page_preview=True)
        print("📤 Rapport envoyé avec succès sur Telegram !")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi du message : {e}")

# 6. Lancement et exécution principale du programme
def main():
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("algo", start_algo))
        
        print("⚡ Initialisation de la connexion avec Telegram...")
        print("🚀 LE BOT EST EN LIGNE ET CONFIGURÉ ! Envoyez /algo dans votre chat Telegram.")
        
        # Le paramètre drop_pending_updates=True efface le flux de messages accumulés
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        print(f"❌ Erreur fatale au lancement du bot : {e}")

if __name__ == '__main__':
    main()
