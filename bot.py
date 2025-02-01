from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import random

# Bot ka API Token yahan dalen
API_TOKEN = "7175839469:AAGZAd1HHRr77yOJK8tdExxjkziKiCA2SKM"  # 🚨 BotFather ka diya hua token dalen

# Captions ko text file se read karein
def load_captions():
    with open("captions.txt", "r", encoding="utf-8") as file:
        captions = file.readlines()
    return [caption.strip() for caption in captions]

# Caption options dikhane ka function
def send_caption_options(update: Update, context: CallbackContext):
    # Captions ko text file se load karein
    captions = load_captions()
    
    # Randomly 3 captions choose karein
    selected_captions = random.sample(captions, min(3, len(captions)))
    
    # Inline keyboard buttons banayein (har caption ke liye ek button)
    keyboard = [
        [InlineKeyboardButton(caption, callback_data=caption)] for caption in selected_captions
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # User ko options bhejein
    update.message.reply_text("Please is post ke liye ek caption choose karein:", reply_markup=reply_markup)

# User ke caption choice ko handle karein
def handle_caption_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    chosen_caption = query.data  # User ne jo caption choose kiya
    
    # Original post ko edit karein aur chosen caption add karein
    context.bot.edit_message_caption(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id - 1,  # Pichli message (post) ko edit karein
        caption=chosen_caption
    )
    
    # User ko confirmation bhejein
    query.answer(f"Caption added: {chosen_caption}")

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Commands aur handlers
    dispatcher.add_handler(CommandHandler("start", send_caption_options))
    dispatcher.add_handler(MessageHandler(Filters.photo, send_caption_options))
    dispatcher.add_handler(CallbackQueryHandler(handle_caption_choice))

    updater.start_polling()
    print("Bot running... ✅")
    updater.idle()

if __name__ == '__main__':
    main()
