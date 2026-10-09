import logging
import time
import requests
import pandas as pd
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Logging ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = "8933483041:AAErRKc9MOMO8BRYsg5rMoMWtEI4R3SxJdc"
CHAT_ID = "5300589139"

PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "PAXGUSDT", "EURUSDT", "GBPUSDT"]

def get_binance_klines(symbol, interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume', '_1', '_2', '_3', '_4', '_5', '_6'])
        df['close'] = df['close'].astype(float)
        return df
    except Exception as e:
        print(f"Veri hatasi ({symbol}): {e}")
        return None

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def start(update: Update, context: CallbackContext):
    keyboard = [
        ['📊 Anlık BTC Analizi', '🌟 Altın (PAXG) Durumu'],
        ['🚀 Popüler Altcoinler', '⚙️ Sistem Durumu']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("🤖 V12 Ultimate Engine Aktif! İstediğin analizi seçebilirsin:", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == '📊 Anlık BTC Analizi':
        df = get_binance_klines('BTCUSDT', '15m', 50)
        if df is not None:
            price = df['close'].iloc[-1]
            rsi = calculate_rsi(df).iloc[-1]
            update.message.reply_text(f"⚡ **BTC/USDT Anlık Durum**\n\nFiyat: ${price:,.2f}\nRSI (15m): {rsi:.1f}")
        else:
            update.message.reply_text("Veri çekilemedi, lütfen tekrar dene.")
            
    elif text == '🌟 Altın (PAXG) Durumu':
        df = get_binance_klines('PAXGUSDT', '15m', 50)
        if df is not None:
            price = df['close'].iloc[-1]
            rsi = calculate_rsi(df).iloc[-1]
            update.message.reply_text(f"🌟 **PAXG (Altın) Anlık Durum**\n\nFiyat: ${price:,.2f}\nRSI (15m): {rsi:.1f}")
        else:
            update.message.reply_text("Veri çekilemedi, lütfen tekrar dene.")
            
    elif text == '⚙️ Sistem Durumu':
        update.message.reply_text("✅ Engine v12 7/24 Kesintisiz Modda Çalışıyor!")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("V12 Engine On Render Online!")
    updater.idle()

if __name__ == '__main__':
    main()

