# WowBaseBot

_This project is written in Python and uses the aiogram libraries to work with the Telegram bot. A Redis database is used to store application data._

## Project setup

Get a Telegram bot authorization token from [@BotFather](https://t.me/BotFather).

Install the [Anaconda](https://www.anaconda.com/download) virtual environment management system.

Install Redis.

```shell
sudo apt install redis
```

Install Redis for MacOS or Linux using [Brew](https://brew.sh/).

```shell
brew install redis
```

Clone this project.

```shell
git clone https://github.com/wow64cpu/WowBaseBot
```

Create an environment for this project.

```shell
conda create --name WowBaseBot python=3.10 -y
```

To activate this environment, use:

```shell
conda activate WowBaseBot
```

Go to the project root folder.

```shell
cd WowBaseBot
```

Install dependencies.

```shell
pip install -r requirements.txt
```

Copy the `.env.dist` file to `.env` file and fill it with actual values.

```shell
cp .env.dist .env
nano .env
```

Launch the bot.

```shell
python bot.py
```

## Environment Variables

| Name             | Description                                                       |
|------------------|-------------------------------------------------------------------|
| `BOT_TOKEN`      | Telegram bot authorization token                                  |
| `SU`             | Telegram ID of superuser                                          |
| `ADMINS`         | Telegram ID of admins separated by commas (can be empty)          |
| `USE_REDIS`      | Boolean value indicating the enabled status of the Redis database |
| `REDIS_HOST`     | Redis database connection host                                    |
| `REDIS_PORT`     | Redis database connection port                                    |
| `REDIS_DB`       | Redis database number used                                        |
| `REDIS_PASSWORD` | Redis database connection password                                |

## File Structure

<details>
    <summary>Click to expand a general overview of the project's file structure</summary>

```shell
WowBaseBot/ # Папка проекта
├── tgbot/ # Основной код
│ ├── filters/ # Основные фильтры для роутера
│ │ ├── __init__.py
│ │ ├── admin.py # Фильтр админов
│ │ └── su.ext # Фильтр супер-пользователей
│ │
│ ├── handlers/ # Основные хэндлеры
│ │ ├── admin/ # Хэндлеры админов
│ │ │ ├── __init__.py
│ │ │ ├── actions.py # Инициализация роутера действий
│ │ │ ├── admin.py # Инициализация админских роутеров
│ │ │ ├── main_menu.py # Инициализация роутера и хэндлеров главного меню
│ │ │ ├── misc.py # Инициализация различных других роутеров и хэндлеров
│ │ │ └── utils.py # Вспомогательный код
│ │ │
│ │ ├── su/ # Хэндлеры супер-пользователей
│ │ │ ├── admins/ # Хэндлеры управления админами
│ │ │ │ ├── __init__.py
│ │ │ │ ├── add.py # Инициализация роутера и хэндлеров приглашения админа
│ │ │ │ ├── admins.py # Инициализация общего роутера и остальных хэндлеров управления админами
│ │ │ │ └── remove.py # Инициализация роутера и хэндлеров удаления админа
│ │ │ │
│ │ │ ├── __init__.py
│ │ │ ├── main_menu.py # Инициализация роутера и хэндлеров главного меню
│ │ │ ├── su.py # Инициализация роутеров супер-пользователей
│ │ │ └── utils.py # Вспомогательный код
│ │ │
│ │ ├── user/ # Хэндлеры обычных пользователей
│ │ │ ├── __init__.py
│ │ │ ├── deep_links.py # Инициализация роутера и хэндлеров диплинков
│ │ │ ├── main_menu.py # Инициализация роутера и хэндлеров главного меню
│ │ │ ├── user.py # Инициализация роутеров обычных пользователей
│ │ │ └── utils.py # Вспомогательный код
│ │ │
│ │ ├── __init__.py
│ │ ├── base.py # Инициализация общего роутера и хэндлеров
│ │ └── form.py # Инициализация хэндлеров для форм
│ │
│ ├── keyboards/ # Разметка кнопок 
│ │ ├── menu/ # Разметка кнопок меню
│ │ │ ├── admins/ # Меню админов
│ │ │ │ ├── __init__.py
│ │ │ │ └── admins.py # Общая разметка меню админов
│ │ │ │
│ │ │ ├── __init__.py
│ │ │ ├── buttons.py # Конструкторы кнопок
│ │ │ └── main.py # Общая разметка меню
│ │ │
│ │ ├── __init__.py
│ │ └── form.py # Конструкторы меню для форм 
│ │
│ ├── middlewares/ # Код для промежуточного ПО aiogram
│ │ ├── __init__.py
│ │ └── config.py # Классы для встраивания промежуточного ПО конфига и диспетчера
│ │
│ ├── misc/ # Различный вспомогательный код
│ │ ├── forms/ # Код для форм
│ │ │ ├── inputs/ # Код для инпутов
│ │ │ │ ├── validators/ # Код для валидаторов
│ │ │ │ │ ├── __init__.py
│ │ │ │ │ └── validator.py # Модель валидатора и функции-конструкторы базовых валидаторов
│ │ │ │ │
│ │ │ │ ├── __init__.py
│ │ │ │ └── input.py # Модель инпута и функции-конструкторы базовых инпутов
│ │ │ │
│ │ │ ├── __init__.py
│ │ │ └── form.py # Модель формы и различных её составных частей и общие функции-конструкторы форм
│ │ │
│ │ ├── states/ # Код для стейт-машин
│ │ │ ├── __init__.py
│ │ │ └── states.py # Стейт-машины форм и навигатора
│ │ │
│ │ ├── storage/ # Код для работы с БД
│ │ │ ├── __init__.py
│ │ │ ├── storage.py # Код для инициализации БД и организации удобного доступа к остальным объектам для работы с БД
│ │ │ ├── storage_admins.py # Код для работы с админами
│ │ │ ├── storage_common.py # Базовый код для работы с данными
│ │ │ ├── storage_data_transfer_gateway.py # Код для работы с шлюзом передачи данных
│ │ │ ├── storage_deep_links.py # Код для работы с диплинками
│ │ │ ├── storage_forms.py # Код для работы с формами
│ │ │ ├── storage_mapper.py # Код для работы с какой-то штукой типа линковки
│ │ │ ├── storage_scheduler.py # Код для работы с планировщиков задач
│ │ │ ├── storage_su.py # Код для работы с супер-пользователями
│ │ │ └── storage_users.py # Код для работы с пользователями
│ │ │
│ │ ├── strings/ # Код для строк
│ │ │ ├── menu/ # Строки меню
│ │ │ │ ├── __init__.py
│ │ │ │ ├── admins_menu.py # Строки меню админа
│ │ │ │ ├── su_main_menu.py # Строки меню супер-пользователя
│ │ │ │ └── user_main_menu.py # Строки меню обычного пользователя
│ │ │ │
│ │ │ ├── __init__.py
│ │ │ ├── actions.py # Строки общих действий
│ │ │ ├── base.py # Общие базовые строки
│ │ │ ├── debug.py
│ │ │ ├── escape.py
│ │ │ └── strings.py # Объект для доступа
│ │ │
│ │ ├── __init__.py
│ │ ├── actions.py # Модели действий навигации и форм
│ │ ├── base.py # Базовая модель компонента системы
│ │ ├── regex.py # Объект с различными регулярками
│ │ ├── singleton.py # Модель синглтона
│ │ └── utils.py # Общий вспомогательный код
│ │
│ ├── models/ # Модели различных компонентов системы
│ │ ├── __init__.py
│ │ ├── actions.py # Модель и функция-конструктор действия отправки сообщения
│ │ ├── data_transfer_gateway.py # Модель и функция-конструктор шлюза передачи данных
│ │ ├── mapper.py # Модель и функция-конструктор какой-то штуки типа линковки
│ │ ├── meta_data.py # Модель и функция-конструктор мета-данных сообщения
│ │ ├── scheduler.py # Модели и функции-конструкторы для планирования задач
│ │ ├── support.py # Модель и функция-конструктор поддержки
│ │ └── user.py # Модель и функция-конструктор пользователя
│ │
│ ├── navigator/ # Код навигатора между экранами (экран - это по сути просто сообщение)
│ │ ├── __init__.py
│ │ └── screens.py # Модель и словарь экранов
│ │
│ ├── services/ # Код различных сервисов
│ │ ├── __init__.py
│ │ └── broadcaster.py # Функции рассылки сообщений
│ │
│ ├── __init__.py # Инициализация пакета
│ ├── bootstrap.py # Инициализация различных компонентов
│ └── config.py # Модели конфигов
│
├── .env.dist # Пример главного конфига
├── .gitignore # Описание того, что не включено в репозиторий
├── bot.example.service # Пример службы для запуска бота в качестве демона
├── bot.py # Точка входа для запуска бота
├── README.MD # Описание проекта
└── requirements.txt # Зависимости Python
```
</details>
