# 🚀 LinkOffer - Партнёрская программа
## Проект партнёрской программы с разделением на рекламодателей и партнёров

### ✨ Возможности
#### 👥 Для партнёров: Реферальные ссылки, статистика, выплаты

### 📊 Для рекламодателей: CPA-кампании, аналитика, контроль бюджета
#### ⚙️ Для менеджеров: Модерация, настройка тарифов, мониторинг

### 🛠 Технологии
#### Backend: Python 3.12, Django, Django REST Framework, Celery, PostgreSQL, Redis

### Frontend: Vite, Tailwind CSS, DaisyUI, Font Awesome
#### Инфраструктура: Gunicorn, Nginx


### Инструкция по развёртыванию Django
1. venv\Scripts\activate
2. Заполнить .env файл
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py collectstatic
6. python manage.py runserver

### Инструкция по развёртыванию Vite
1. yarn install
2. yarn vite (для разработки) 
3. yarn vite build (для production) 
