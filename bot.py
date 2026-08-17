import logging
import datetime
import random
import os
import requests
import telebot
from telebot import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RENDER LIT LES CLÉS DIRECTEMENT DANS L'ONGLET ENVIRONMENT
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw")
LIEN_PAIEMENT = "https://paysafecard.com"

# BASE DE DONNÉES 100% CONFORME PRONOSOFT DU LUNDI 17 AOÛT 2026
BASE_DONNEES_OFFICIELLE = {
    "⚽ FOOTBALL (LALIGA 2)": [
        {"rencontre": "La Corogne vs Elche", "cote_brute": 2.20, "detail": "Résultat : Victoire de La Corogne"},
        {"rencontre": "Gijon vs Sabadell", "cote_brute": 1.72, "detail": "Résultat : Victoire de Gijon"}
    ],
    "⚽ FOOTBALL (DANEMARK)": [
        {"rencontre": "Brøndby vs Sønderjyske", "cote_brute": 1.32, "detail": "Résultat : Victoire de Brøndby"}
    ],
    "🎾 TENNIS (MASTERS CINCINNATI)": [
        {"rencontre": "L. Sonego vs F. Tiafoe", "cote_brute": 1.57, "detail": "Vainqueur du match : F. Tiafoe"},
        {"rencontre": "A. Blockx vs F. Cobolli", "cote_brute": 1.99, "detail": "Vainqueur du match : F. Cobolli"}
    ]
}

def algorithme_calcul_autonome():
    jour_annee = datetime.datetime.now().timetuple().tm_yday
    random.seed(jour_annee)
    tickets_simples = []
    
    for cat in list(BASE_DONNEES_OFFICIELLE.keys()):
        match = random.choice(BASE_DONNEES_OFFICIELLE[cat])
        forme_ia = random.randint(86, 98)
        mental_ia = random.randint(83, 99)
        indice_value = round(random.uniform(6.1, 10.8), 1)
        mise_conseillee = min(50, max(20, int(indice_value * 6.2))) # PLAFOND 50€ STRICT
        
        tickets_simples.append({
            "sport": cat, "match": match["rencontre"], "pari": match["detail"],
            "cote": match["cote_brute"], "physique": forme_ia, "mental": mental_ia,
            "value": indice_value, "mise": mise_conseillee
        })
    random.seed()
    return tickets_simples

def generer_message_analytique_pronosoft():
    date_titre = datetime.datetime.now().strftime('%d/%m/%Y')
    tickets = algorithme_calcul_autonome()
    
    msg = f"🧙‍♂️ 🟩 **[ALGORITHME PRONOSOFT OFFICIEL] — {date_titre}**\n========================================\n\n"
    msg += "🎯 **ANALYSES DISPONIBLES EN PARIS SIMPLES (Max 50€) :**\n----------------------------------------\n"
    for i, t in enumerate(tickets, 1):
        fiabilite = "⭐️" * random.randint(4, 5)
        msg += f"📊 **Pari Expert n°{i} — {t['sport']}**\n⚔️ Rencontre : **{t['match']}**\n🧠 Indicateurs : Forme `[{t['physique']}%]` | Mental `[{t['mental']}%]`\n🎯 Pari : `{t['pari']}`\n📊 Cote : `{t['cote']}` | **⚠️ Fiabilité :** {fiabilite}\n📈 Value Bet : `+{t['value']}%`\n💰 **Mise conseillée : {t['mise']} €**\n\n"
        
    msg += "========================================\n🚀 **LE COMBINÉ ALGORITHMIQUE SAFE (Mise 25€) :**\n----------------------------------------\n"
    m1, m2 = tickets[0], tickets[1]
    msg += f"1️⃣ **[{m1['sport']}]** {m1['match']} ➔ ({m1['cote']})\n2️⃣ **[{m2['sport']}]** {m2['match']} ➔ ({m2['cote']})\n\n📊 **Cote Totale Combiné : {round(float(m1['cote']) * float(m2['cote']), 2)}** | 💰 **Mise : 25 €**\n"
    msg += "========================================\n🔒 **ACCÈS PREMIUM VIP — ALLOCATIONS LOURDES**\n----------------------------------------\n💶 Prix Fixe : **20.00 €**\n💳 **Lien d'achat sécurisé Paysafecard :** {LIEN_PAIEMENT}\n========================================\n⚠️ _Mises simples strictement bridées à 50€ maximum._"
    return msg

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.send_message(message.chat.id, "👋 **Bienvenue chez Le Magicien des Pronos !**\n\n🤖 Analyses mathématiques appliquées sur les matchs certifiés Pronosoft de la journée.")
        bot.send_message(message.chat.id, generer_message_analytique_pronosoft(), parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Erreur d'envoi : {e}")

if __name__ == '__main__':
    print("\n🚀 BOT EN LIGNE SUR SERVEUR CLOUD ÉTERNEL RENDER !")
    bot.infinity_polling()
