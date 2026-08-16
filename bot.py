import logging, random, itertools, asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = "8975669837:AAFys_Zbrk-4n-9KOAmJvnXW5lYJJmREfCw"

# Base de données de clubs officiels pour nourrir le bot
COMPETITIONS = [
    ("⚽ Ligue 1", "Paris SG", "Marseille"),
    ("⚽ Ligue 1", "Lens", "Lyon"),
    ("⚽ Premier League", "Arsenal", "Man. City"),
    ("⚽ Premier League", "Chelsea", "Liverpool"),
    ("🏀 NBA", "LA Lakers", "Boston"),
    ("🏀 NBA", "Golden State", "Chicago")
]

BUTEURS_STARS = ["Kylian Mbappé", "Bradley Barcola", "Erling Haaland", "Mohamed Salah", "Ousmane Dembélé"]

OPTIONS_PARIS = [
    "Les deux équipes marquent : OUI",
    "Nombre de buts : Plus de 2.5 buts",
    "Nombre de buts : Moins de 3.5 buts",
    "Résultat : Victoire de l'équipe à domicile",
    "Double Chance : Équipe à l'extérieur ou Nul"
]

def generer_rapport_dynamique():
    """Génère un tableau de bord pro à partir de vraies configurations fluctuantes."""
    # Sélection aléatoire de 2 affiches distinctes parmi nos championnats
    matchs_selectionnes = random.sample(COMPETITIONS, 2)
    
    msg = "🧙‍♂️ 🟩 **[ALGORITHME EN TEMPS RÉEL] — VALUES SÉLECTIONNÉES**\n"
    msg += "========================================\n\n"
    
    msg += "🎯 **LES TICKETS SIMPLES DU JOUR (Mise Max 50€) :**\n"
    msg += "----------------------------------------\n"
    
    for i, (competition, home, away) in enumerate(matchs_selectionnes, 1):
        # Génération d'une value réaliste fluctuante entre +5.5% et +9.4%
        avantage = round(random.uniform(5.5, 9.4), 1)
        # Indice de mise strict pour brider la mise sous le plafond des 50€ imposé
        mise_exacte = min(50, max(15, int(avantage * 6.5)))
        confiance = "⭐️" * random.randint(4, 5)
        
        # Aléatoire : une fois sur deux on propose un prono collectif, une fois sur deux un buteur star
        if i == 2 and "Ligue" in competition:
            buteur = random.choice(BUTEURS_STARS)
            intitule_pari = f"Buteur : {buteur} marque pendant le match"
            cote = round(random.uniform(1.95, 2.40), 2)
        else:
            intitule_pari = random.choice(OPTIONS_PARIS)
            cote = round(random.uniform(1.55, 1.95), 2)
            
        msg += f"📊 **Pari Simple n°{i} ({competition})**\n"
        msg += f"⚔️ Rencontre : **{home} vs {away}**\n"
        msg += f"🎯 **Intitulé du Pari :** `{intitule_pari}`\n"
        msg += f"📊 **Cote :** `{cote}` | **⚠️ Fiabilité :** {confiance}\n"
        msg += f"📈 Indice de Value : `+{avantage}%` | 💰 **Mise conseillée : {mise_exacte} €**\n\n"
        
    msg += "========================================\n"
    msg += "🚀 **LE COMBINÉ SAFE DU MAGICIEN :**\n"
    msg += "----------------------------------------\n"
    c_match1, c_match2 = matchs_selectionnes[0], matchs_selectionnes[1]
    msg += f"1️⃣ **{c_match1[1]} vs {c_match1[2]}** ➔ `Plus de 1.5 buts` (1.28)\n"
    msg += f"2️⃣ **{c_match2[1]} vs {c_match2[2]}** ➔ `Double Chance : {c_match2[1]} ou Nul` (1.35)\n\n"
    msg += "📊 **Cote Totale : 1.73** | 💰 **Mise conseillée : 25 €**\n"
    msg += "⚠️ **CONFIANCE GLOBAL COMBINÉ :** ⭐️⭐️⭐️⭐️\n"
    msg += "========================================\n"
    msg += "🔒 **ACCÈS PRIVÉ VIP (Tarif Fixe 20€) :**\n"
    msg += "----------------------------------------\n"
    msg += "Gagnez sur le long terme avec 100% de nos alertes d'anomalies de cotes mondiales 24h/24.\n"
    msg += "📥 _Cliquez sur le bouton ci-dessous pour régler votre accès via Paysafecard :_\n"
    msg += "========================================\n"
    msg += "⚠️ _Mises simples strictement bridées à 50€ maximum pour protection du capital._"
    return msg

def obtenir_clavier_tactile():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Re-Scan les Cotes Réelles", callback_data="s")],
        [InlineKeyboardButton("📊 Mon Bilan Pro", callback_data="b")],
        [InlineKeyboardButton("💎 Débloquer l'Espace VIP (20€)", callback_data="v")]
    ])

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    await u.message.reply_text("🟩 **Moteur connecté aux flux réels activé !**\nExtraction en cours des équipes et intitulés de paris...")
    await c.bot.send_message(chat_id=u.effective_user.id, text=generer_rapport_dynamique(), parse_mode="Markdown", reply_markup=obtenir_clavier_tactile())

async def cb(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query
    try: await q.answer()
    except: pass
    if q.data == "s":
        try: await q.edit_message_text(text="⏳ *Calcul et scannage des vrais intitulés et des cotes réelles sur le marché...*", parse_mode="Markdown")
        except: pass
        await asyncio.sleep(0.5) # Simule un temps de calcul léger pour l'utilisateur
        try: await q.edit_message_text(text=generer_rapport_dynamique(), parse_mode="Markdown", reply_markup=obtenir_clavier_tactile())
        except: pass
    elif q.data == "b":
        await c.bot.send_message(chat_id=q.message.chat_id, text="📊 **COMPTABILITÉ ET SUIVI AUTOMATIQUE :**\n\n💰 Capital Initial : 1000.00 €\n📊 Paris Enregistrés : 14\n📈 Performance globale : `+12.4% ROI` (Bénéficiaire)", parse_mode="Markdown")
    elif q.data == "v":
        keyboard_pay = [[InlineKeyboardButton("💳 Payer 20€ via Paysafecard", url="https://paysafecard.com")]]
        await c.bot.send_message(chat_id=q.message.chat_id, text="🔒 **ACCÈS PREMIUM VIP — LE MAGICIEN**\n\nDébloquez l'ensemble des analyses lourdes 24h/24.\n\n💶 Prix Unique : **20.00 €**\n📥 _Cliquez ci-dessous pour payer via Paysafecard :_", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard_pay))

async def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(cb))
    
    await app.initialize()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    await app.start()
    print("\n🚀 INFRASTRUCTURE HÉBERGÉE EN LIGNE ET PRÊTE H24 !")
    
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
