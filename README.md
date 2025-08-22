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
3. Запустить контейнер
```bash
    docker compose up -d --build
```
4. Создать виртуальное окружение
```bash
     python -m venv venv
```
5. Установить зависимости
```bash
    pip install -r requirements.txt
```
6. Активировать виртуальное окружение
- macOS/Linux:
```bash
    source venv/bin/activate 
```
- Windows (PowerShell):
```bash
    venv\Scripts\activate.bat
```
7. Запустить тесты:
```bash
    pytest 
```
- с указанием браузера (--browser=ch, --browser=ff, --browser=ya)
```bash
    pytest --browser=ff
```
- с указанием базового URL (--base_url=http://localhost:8082)
```bash
    pytest --base_url=http://localhost:8082
```
- с выбором уровня логирования (например, --project_log_level=DEBUG) и сохранения логов в файл (--log_to_file)
```bash
pytest --project_log_level=INFO --log_to_file
```


