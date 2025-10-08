## 🚀 Проект Otus OpenCart

Проект включает приложение OpenCart и набор автоматизированных тестов (pytest + Selenium).

### Шаги
1. Склонировать проект
```bash
   git clone https://github.com/avdarya/otus_open_cart.git
   cd otus_open_cart
```
2. 	Создать .env из шаблона и заполнить поля
```bash
    cp .env_sample .env
```
🔹 Для локального запуска тестов раскомментировать строки в .env:
```bash
    ## Local Tests
    LOCAL_IP=127.0.0.1
    OPENCART_PORT=8082
    # ## Docker Tests
    # LOCAL_IP=opencart
    # OPENCART_PORT=8080
```

🔹 Для запуска тестов в контейнере раскомментировать строки в .env:
```bash
    ## Local Tests
    # LOCAL_IP=127.0.0.1
    # OPENCART_PORT=8082
    ## Docker Tests
    LOCAL_IP=opencart
    OPENCART_PORT=8080
```

3. Собрать и запустить OpenCart и MariaDB:
```bash
    docker compose up -d --build
```

4. Собрать Docker-образ с тестами:
```bash
    docker build -t tests -f Dockerfile.tests.dockerfile .
```

5. Запустить тесты:

🔹 Локальный запуск тестов
- Создать виртуальное окружение
```bash
     python -m venv venv
```
- Активировать виртуальное окружение:

-- macOS/Linux:
```bash
    source venv/bin/activate 
```
-- Windows (PowerShell):
```bash
    venv\Scripts\activate.bat
```
- Установить зависимости
```bash
    pip install -r requirements.txt
```
- Запустить тесты
```bash
    pytest 
```
-- с указанием браузера (--browser=ch, --browser=ff, --browser=ya)
```bash
    pytest --browser=ff
```
-- с указанием базового URL (--base_url=http://localhost:8082)
```bash
    pytest --base_url=http://localhost:8082
```
-- с выбором уровня логирования (например, --project_log_level=DEBUG) и сохранения логов в файл (--log_to_file)
```bash
    pytest --project_log_level=INFO --log_to_file
```
🔹 Запуск тестов внутри Docker
```bash
    docker run -it --rm \
      --network=otus_open_cart_default \
      --env-file .env \
      tests
```
-- с указанием браузера (--browser=chrome, --browser=firefox, --browser=yandex)
```bash
    docker run -it --rm \
      --network=otus_open_cart_default \
      --env-file .env \
      tests --browser=firefox
```
-- с указанием базового URL
```basah
docker run -it --rm \
  --network=otus_open_cart_default \
  --env-file .env \
  tests --base_url=http://opencart:8080
```