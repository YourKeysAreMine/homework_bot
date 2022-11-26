import requests
import os
import telegram
import time
import logging
import sys

from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD: int = 600
ENDPOINT: str = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS: dict = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяем наличие токенов, ID чата"""
    tokens = {
        'Токен Яндекс Практикума': PRACTICUM_TOKEN,
        'Токен Телеграмма': TELEGRAM_TOKEN,
        'ID Чата Телеграмма': TELEGRAM_CHAT_ID,
    }
    for key, value in tokens.items():
        if value is None:
            logging.critical(f'{key} отсутствует')
            return False
    return True


def send_message(bot: telegram.bot.Bot, message: str):
    """Направляем сообщение в телеграм чат"""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception:
        logging.error('Что-то не так, сообщение в телеграм не отправлено!')
    else:
        logging.debug('Сообщение в телеграм отправлено успешно!')


def get_api_answer(timestamp: int):
    """Получаем ответ от Яндекс.Домашка(тм)"""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            response.raise_for_status()
        logging.info('Ответ на запрос к API: 200 OK')
        return response.json()
    except requests.exceptions.RequestException:
        logging.error('Ошибка при запросе к Яндекс.Домашка(тм)')


def check_response(response: dict):
    """Проверяем ответ от Яндекс.Домашка(тм)"""
    if type(response) is dict:
        if type(response.get('homeworks')) is list:
            return response.get('homeworks')
        raise TypeError('В ответе API домашки под ключом' 
                        '`homeworks` данные приходят не в виде списка')
    raise TypeError('В ответе API домашки не содержится словарь')


def parse_status(homework: dict):
    """Извлекаем из ответа от Яндекс.Домашка(тм) информацию о статусе"""
    if 'status' in homework:
        if 'homework_name' in homework:
            homework_name = homework.get('homework_name')
            status = homework.get('status')
            if status in HOMEWORK_VERDICTS:
                verdict = HOMEWORK_VERDICTS[status]
                return (f'Изменился статус проверки работы'
                        f'"{homework_name}". {verdict}')
            else:
                raise KeyError('АPI домашки вернул неизвестный статус!')
        raise KeyError('В ответе API домашки нет ключа <status>')
    raise KeyError('В ответе API домашки нет ключа <homework_name>')


def main():
    """Основная логика работы бота."""
    logging.info('Бот запущен')
    if check_tokens():
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        timestamp = int(time.time())
        while True:
            try:
                response = get_api_answer(timestamp)
                homework_info = check_response(response)
                if len(homework_info) > 0:
                    message = parse_status(homework_info[0])
                    send_message(bot, message)
                    time.sleep(RETRY_PERIOD)
                logging.debug('Статус ДЗ не изменился!')
                time.sleep(RETRY_PERIOD)
            except Exception as error:
                message = f'Сбой в работе программы: {error}'
                send_message(bot, message)
                time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
