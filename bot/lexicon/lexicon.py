from typing import Dict

LEXICON: Dict[str, str] = {
    '/start': 'Здравствуйте\! 👋\nЭтот бот предназначен для отслеживания новых объявлений на Авито\. Выберите, что Вы хотите сделать, нажав на соответствующую кнопку в нижней части экрана\.',
    'list_entry': 'Список отслеживаемых ссылок:\n\n',
    'paste_new_link': 'Пожалуйста, отправьте полную ссылку на поисковую выдачу, которую хотите отслеживать\. Она должна начинаться на "https…"',
    'paste_new_heading': 'Пожалуйста, напишите, как бы Вы хотели назвать ссылку?',
    'error_paste_new_link': 'Ссылка не корректна\. Пожалуйста, проверьте ещё раз: ссылка должна быть полной и начинаться на "https…"',
    'empty_links': 'Отслеживаемые ссылки отсутствуют\.',
    'existing_link': 'Данная ссылка уже отслеживается\.',
    'abort_new_link': 'Добавление новой ссылки отменено\.',
    'success_new_link': 'Ссылка успешно добавлена\.',
    'number_remove_link': 'Пожалуйста, введите номер ссылки, которую Вы хотите удалить\.',
    'bad_number': 'Введённое Вами не является натуральным числом\.',
    'not_existing_number': 'Такого номера не существует\.',
    'success_remove_link': 'Ссылка успешно удалена\.'
}
