# Бот - ассистент

Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнаёт статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

## Основные функции программы

- раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
- при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
- логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

## Описание функций программы

- **Функция main()** в ней описана основная логика работы программы. Все остальные функции должны запускаться из неё.
- **Функция check_tokens()** проверяет доступность переменных окружения, которые необходимы для работы программы. Если отсутствует хотя бы одна переменная окружения — продолжать работу бота нет смысла.
- **Функция get_api_answer()** делает запрос к единственному эндпоинту API-сервиса. В качестве параметра в функцию передается временная метка. В случае успешного запроса должна вернуть ответ API, приведя его из формата JSON к типам данных Python.
- **Функция check_response()** проверяет ответ API на соответствие документации. В качестве параметра функция получает ответ API, приведенный к типам данных Python.
- **Функция parse_status()** извлекает из информации о конкретной домашней работе статус этой работы. В качестве параметра функция получает только один элемент из списка домашних работ. В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, содержащую один из вердиктов словаря HOMEWORK_VERDICTS.
- **Функция send_message()** отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.

## Технологии
- Python 3.8
- Telegram-bot 13

### Авторы
Закиров Сергей

### License
MIT
