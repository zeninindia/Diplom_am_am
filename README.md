# Diplom

## **Final diploma**

**Проект по ручному тестированию (тест-кейсы, чек-листы, баг-репорты) находится по ссылке:**

`https://awesome2345.yonote.ru/share/201c0bac-738e-4913-8583-911b19bdedfd`

**Что включено в ручное тестирование:**
1. Чек-листы для проверки основного функционала
2. Тест-кейсы для UI и API
3. Баг-репорты с найденными дефектами
4. Отчеты о тестировании


### Steps
1. Cклонировать проект `git clone https://github.com/zeninindia/Diplom.git`
2. Установить все зависимости `pip install -r requirements.txt` (чтобы мне вытащить все зависимости `pip freeze`)
3. Запустить тесты `pytest`
4. В тестах создан метод в классе для первой простой капчи, все последующие проверки на то что я не робот,
прокликиваются вручную.
5. Создать папку allure-report `allure generate ./allure-results -c -o ./allure-report`
6. Вызвать отображение allure-results `allure serve ./allure-results`

### Браузер
Chrome: Браузер для UI-тестирования ChromeDriver: 
Драйвер для Chrome (автоматически управляется через webdriver-manager или системный путь)

### File .env
1. Создайте файл `.env` в корне проекта
2. Заполните переменные своими данными:
- URL=https://api.poiskkino.dev/
- KEY=your_api_key_here


### Список установок:

* pip install pytest sylenium
* pip install pytest
* *pip install webdriver-manager*
* pip install selenium webdriver-manager
* pip install requests pytest pytest-html pytest-cov responses python-dotenv loguru allure-pytest
* python -m venv test_env
* python -m pip install --upgrade pip setuptools wheel
* pip install -r requirements.txt
* pip install requests
* pip install selenium
* pip install allure


### Полезные ссылки

* Это про **маркдаун**, и как их использовать [Markdown](https://www.markdownguide.org/basic-syntax/)
* Нужно выбрать те функции с которыми работаем и вот [генератор файла **.gitignore**](https://www.toptal.com/developers/gitignore/api/python,windows,pycharm,visualstudiocode,test)
* Это [API](https://api.poiskkino.dev) документация сайта **Кинопоиск**

### Структура проекта
      
    Diplom_am_am/
    ├── Pages/                  # Файлы PageObject файлы классов API & UI
    │   ├── __init__.py
    │   ├── p_class.py          # Пользовательские классы (API)
    │   └── ui_class.py         # Пользовательские классы (UI)
    ├── Tests/                  # Директория с тестами
    │   ├── __init__.py
    │   ├── test.py             # Тесты для API (requests)
    │   └── test_ui.py          # Тесты для UI (requests)
    ├── .env.example            # Файл с переменными окружения 
    ├── __init__.py            
    ├── conftest.py             # Конфигурационный файл для pytest (фикстуры API & UI)
    ├── pytest.ini              # Настройки для pytest
    ├── README.md               # Описание проекта
    ├── .gitignore              # Игнорируемые файлы для Git
    ├── requirements.txt        # Зависимости проекта (pip)
    └── External Libraries/     # Внешние библиотеки (если не через pip)