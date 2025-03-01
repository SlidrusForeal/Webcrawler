# Простой веб-краулер на Python

Этот проект представляет собой простой веб-краулер, реализованный на Python с использованием библиотек **requests** и **BeautifulSoup**. Он предназначен для обхода веб-страниц с учетом следующих особенностей:

- **Начальный URL:** Краулер запрашивает URL, с которого необходимо начать обход.
- **robots.txt:** Перед посещением страницы осуществляется проверка разрешений согласно файлу robots.txt.
- **Ограничение по домену:** Краулер следует по гиперссылкам только в пределах того же домена.
- **Глубина обхода:** Ограничение глубины обхода установлено на 3 уровня.
- **Задержка между запросами:** Между запросами происходит задержка в 1 секунду для соблюдения этики краулинга.
- **Избежание повторных посещений:** Один и тот же URL не обрабатывается повторно.
- **Сохранение результатов:** Для каждой посещенной страницы сохраняются URL и заголовок (из тега `<title>`) в текстовый файл `crawled_pages.txt`.
- **Логирование:** Использование модуля `logging` позволяет сохранять информацию о ходе работы в файл `crawler.log`.

## Установка

1. Клонируйте или загрузите репозиторий с проектом.
2. Установите необходимые зависимости, выполнив команду:

   ```bash
   pip install -r requirements.txt
   ```

## Запуск

Чтобы запустить веб-краулер, выполните команду:

```bash
python your_crawler_file.py
```

После запуска программа запросит у вас начальный URL. Результаты обхода сохраняются в файл `crawled_pages.txt`, а подробная информация записывается в `crawler.log`.

## Особенности и улучшения

- **Обработка ошибок:** Реализована базовая обработка исключений при выполнении HTTP-запросов.
- **Итеративный обход:** Применяется очередь для обхода страниц, что позволяет избежать проблем с глубиной рекурсии.
- **Проверка типа контента:** Перед обработкой страницы проверяется, что контент является HTML.
- **Асинхронность (будущая доработка):** Возможно расширение функционала за счет использования асинхронных запросов с помощью `aiohttp` и `asyncio`.

## Лицензия MIT

Данный проект предоставляется для ознакомительных целей. Используйте и модифицируйте его в соответствии с вашими задачами.
