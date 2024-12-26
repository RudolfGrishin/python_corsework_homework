# Название проекта
PARIS-SAINT-GERMAIN
## Описание
Этот проект содержит функции для в себе функции для работы с ключами API и предоставление различных данных по сортировке.
## Установка
1. Склонируйте репозиторий:
2. https://github.com/RudolfGrishin/python_corsework_homework
3. Установите зависимости:
```
[tool.poetry]
name = "coursework-1"
version = "0.1.0"
description = ""
authors = ["Rudolf.Grishin <sumlyaninov74@mail.ru>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.13"
requests = "^2.32.3"
pandas = "^2.2.3"


[tool.poetry.group.lint.dependencies]
flake8 = "^7.1.1"
mypy = "^1.14.0"
black = "^24.10.0"
isort = "^5.13.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.mypy]
disallow_untyped_defs = true
no_implicit_optional = true
warn_return_any = true
exclude = 'venv'

[tool.black]
line-length = 119
exclude = '.git'

[tool.isort]
line_length = 119
```
## Использование:
В данном проекте собраны функции которые разложены по модулям, в пакете src, можно найти все модули с описанными в них функциями для работы приложения. В пакете tests, собраны все тесты для тестирований функций из пакета src, так же в проекте есть файл .env_template в данном файле присутствует информация по api ключу и так же по github! Вместо данных что указанны в данном файле необходимо указать свои.
## Документация:
[GitHub]  https://github.com/RudolfGrishin/python_corsework_homework данная ссылка переведёт вас на мой репозиторий и вы сможете ознакомиться по лучше с моим проектом. 
## Лицензия:
Проект распространяется под [лицензией MIT](LICENSE)
