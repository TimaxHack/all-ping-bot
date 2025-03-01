import telebot
from telebot import types
import time
import os

# Токен вашего бота от BotFather
BOT_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
print(BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['text'])
def ping_on_mention(message):
    # Проверяем, что это группа или супергруппа
    if message.chat.type not in ['group', 'supergroup']:
        return
    
    # Получаем информацию о боте
    bot_info = bot.get_me()
    bot_username = f"@{bot_info.username}"
    
    # Проверяем, упомянут ли бот или это ответ на его сообщение
    if (message.text and bot_username in message.text) or \
       (message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id):
        
        chat_id = message.chat.id
        
        try:
            # Проверяем права бота
            admins = bot.get_chat_administrators(chat_id)
            if bot_info.id not in [admin.user.id for admin in admins]:
                bot.reply_to(message, "Мне нужны права администратора!")
                return
            
            # Получаем всех администраторов, исключая ботов
            members = [admin.user for admin in admins if not admin.user.is_bot]
                        
            if not members:
                bot.reply_to(message, "Не удалось найти участников! Все боты?")
                return
            
            # Формируем сообщение с упоминаниями (MarkdownV2)
            mention_text = ""
            for member in members:
                if member.username:
                    # Экранируем подчеркивания в username
                    username = member.username.replace('_', r'\_')
                    mention_text += f"@{username} "
                else:
                    name = member.first_name.replace('\\', r'\\').replace('_', r'\_').replace('*', r'\*').replace('[', r'\[').replace(']', r'\]').replace('_', r'\_')
                    mention_text += f"[{name}](tg://user?id={member.id}) "
            
            # Убираем лишний пробел в конце
            mention_text = mention_text.strip()
            
            # Отправляем сообщение с MarkdownV2
            bot.reply_to(message, mention_text, parse_mode='MarkdownV2', disable_web_page_preview=True)
            
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)