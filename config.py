# region •••••••••••••••• ОСНОВНЫЕ НАСТРОЙКИ
from os import environ  # Импортируем библиотеку для работы с переменными

# Токен для авторизации приложения:
# Тоокен генирируется автоматически при создание приложения на странице https://discord.com/developers/applications
token = environ['APP_TOKEN']

# Тип окружения, в котором производится запуск
environment_type = environ['APP_ENVIRONMENT'].lower()
assert environment_type in ['test', 'prod'], f"Wrong environment type: {environment_type}, must be 'test' or 'prod'"

# endregion ••••••••••••• ОСНОВНЫЕ НАСТРОЙКИ // КОНЕЦ


# region •••••••••••••••• ОСНОВНАЯ ИНФОРМАЦИЯ
# Краткое описание приложения:
app_short_description = 'E.D.O.K. — Elite Dangerous Outfitting Keeper'

# Полное описание приложения:
app_full_description = 'Приложение для вывода списка с ссылками на сборки кораблей с сервиса Coriolis EDCD Edition.'

# Приглашение на сервер поддержки
app_support_server_invite = 'https://discord.gg/HFqmXPvMxC'

# Ссылка на репозиторий на GitHub
app_github_url = 'https://github.com/LostVault/edok'

# endregion ••••••••••••• ОСНОВНАЯ ИНФОРМАЦИЯ // КОНЕЦ
