# Force le bot à effacer la file d'attente Telegram au démarrage
application.run_polling(drop_pending_updates=True)
