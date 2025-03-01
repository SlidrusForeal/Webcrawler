import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import time
import logging
from collections import deque

# Настройка логирования: записи сохраняются в файл "crawler.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='crawler.log',
    filemode='w'
)

def setup_robot_parser(start_url, user_agent):
    """
    Загружает и анализирует файл robots.txt для домена начального URL.
    """
    parsed = urlparse(start_url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        logging.info(f"robots.txt успешно загружен с {robots_url}")
    except Exception as e:
        logging.error(f"Ошибка при загрузке robots.txt с {robots_url}: {e}")
    return rp

def crawl(start_url, max_depth, user_agent):
    """
    Итеративный обход страниц с использованием очереди.
    - start_url: начальный URL для обхода.
    - max_depth: максимальная глубина обхода.
    - user_agent: строка, идентифицирующая бота.
    """
    parsed_start = urlparse(start_url)
    domain = parsed_start.netloc
    rp = setup_robot_parser(start_url, user_agent)

    visited = set()
    queue = deque([(start_url, 0)])
    output_file = "crawled_pages.txt"

    # Очищаем файл результатов перед началом обхода
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("")

    while queue:
        url, depth = queue.popleft()

        # Прекращаем обход, если превышена максимальная глубина
        if depth > max_depth:
            continue

        # Если URL уже посещён, пропускаем его
        if url in visited:
            continue

        # Проверка разрешения согласно robots.txt
        if not rp.can_fetch(user_agent, url):
            logging.info(f"[Пропущено - robots.txt]: {url}")
            continue

        visited.add(url)
        logging.info(f"[Уровень {depth}] Обработка: {url}")

        try:
            response = requests.get(url, headers={'User-Agent': user_agent}, timeout=10)
            time.sleep(1)  # задержка 1 секунда между запросами
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при запросе {url}: {e}")
            continue

        if response.status_code != 200:
            logging.warning(f"Страница {url} недоступна (статус {response.status_code})")
            continue

        # Проверяем, что полученный контент является HTML
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            logging.info(f"Пропущен URL, не являющийся HTML: {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        # Сохраняем URL и заголовок в файл
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{url} - {title}\n")

        # Поиск и обработка всех ссылок на странице
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(url, href)  # корректная обработка относительных ссылок
            parsed_link = urlparse(full_url)
            # Ограничиваем обход ссылками в пределах того же домена
            if parsed_link.netloc != domain:
                continue
            if full_url not in visited:
                queue.append((full_url, depth + 1))

    logging.info("Обход завершен. Результаты сохранены в %s", output_file)
    print("Обход завершен. Результаты сохранены в", output_file)

def main():
    start_url = input("Введите начальный URL: ").strip()
    if not start_url:
        print("URL не может быть пустым.")
        return
    user_agent = "MyWebCrawlerBot"
    max_depth = 13
    crawl(start_url, max_depth, user_agent)

if __name__ == "__main__":
    main()
