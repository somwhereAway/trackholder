генерация миграция алембик
```bash
alembic revision --autogenerate -m "First migration" 
```
применение миграций
```bash
alembic upgrade head 
```

запушить образы контейнеров
```bash
docker build -t akromerd/trackholder_app .
docker push  akromerd/trackholder_app
```
на сервере
```bash
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
```
# Выполняет миграции и сбор статики
```bash
sudo docker compose -f docker-compose.production.yml exec app alembic upgrade head
```
логи нджинкс сервера
```bash
tail -n 10 /var/log/nginx/access.log
```
логи контейнера
```bash
docker logs my_container
```
```bash
sudo docker compose -f docker-compose.production.yml up -d
```

### 2. Просмотр логов для всех контейнеров в этом `docker-compose` файле:

После запуска контейнеров можно посмотреть логи всех сервисов, указанных в `docker-compose.production.yml`, с помощью команды:

```bash
sudo docker compose -f docker-compose.production.yml logs
```

### 3. Просмотр логов в реальном времени:

Чтобы следить за логами в реальном времени, добавьте флаг `-f`:

```bash
sudo docker compose -f docker-compose.production.yml logs -f
```

### 4. Просмотр логов конкретного сервиса:

Чтобы посмотреть логи конкретного сервиса, добавьте имя сервиса после команды `logs`. Например, если у вас есть сервис с именем `app`, команда будет:

```bash
sudo docker compose -f docker-compose.production.yml logs app
```

### 5. Просмотр ограниченного количества строк логов:

Вы также можете указать количество строк, которые нужно увидеть, с помощью флага `--tail`:

```bash
sudo docker compose -f docker-compose.production.yml logs --tail 100
```

Эти команды помогут вам управлять логами контейнеров, запущенных через `docker-compose.production.yml`.

Чтобы посмотреть модели (или таблицы) в базе данных PostgreSQL, запущенной в Docker-контейнере, выполните следующие шаги:

## Как смотреть БД

### 1. Подключитесь к контейнеру PostgreSQL

Сначала найдите имя или ID контейнера с PostgreSQL, если вы его не знаете. Выполните:

```bash
docker ps
```

Затем выполните команду, чтобы подключиться к контейнеру PostgreSQL:

```bash
docker exec -it <container_name_or_id> psql -U <username> -d <database_name>
```

- `<container_name_or_id>` — имя или ID контейнера PostgreSQL.
- `<username>` — имя пользователя PostgreSQL, которое вы указали при настройке.
- `<database_name>` — имя базы данных, в которой вы хотите посмотреть модели (таблицы).

Пример команды:

```bash
docker exec -it postgres_container psql -U myuser -d mydatabase
sudo docker compose -f docker-compose.production.yml exec -it db psql -U app_user -d app
```

### 2. Просмотрите таблицы в базе данных

После подключения к базе данных вы окажетесь в командной строке `psql`. Чтобы увидеть все таблицы (или модели) в текущей базе данных, выполните:

```sql
\dt
```

Эта команда выведет список всех таблиц в базе данных. 

### 3. Дополнительные полезные команды

- **Посмотреть все схемы** (если вы используете несколько схем):  
  ```sql
  \dn
  ```

- **Посмотреть таблицы в определённой схеме** (например, `public`):  
  ```sql
  \dt public.*
  ```

- **Получить информацию о структуре конкретной таблицы**:
  ```sql
  \d <table_name>
  ```

- **Вывести список всех команд**:
  ```sql
  \?
  ```

- **Выйти из `psql`**:
  ```sql
  \q
  ```

### Полный пример

```bash
docker exec -it postgres_container psql -U myuser -d mydatabase
```

В `psql`:

```sql
\dt          -- Просмотр таблиц
\d my_table  -- Просмотр структуры конкретной таблицы
``` 

Эти команды помогут вам легко получить доступ к структуре базы данных PostgreSQL внутри контейнера.



## Отключение параоля 

Если это допустимо, рекомендуется настроить `sudo` на выполнение команд Docker без запроса пароля:

1. Откройте файл `sudoers` на сервере:
   ```bash
   sudo visudo
   ```
2. Добавьте строку, чтобы разрешить запуск Docker-команд без запроса пароля для нужного пользователя:
   ```plaintext
   your_user_name ALL=(ALL) NOPASSWD: /usr/bin/docker
   ```

Это даст возможность использовать команды Docker с `sudo` без запроса пароля, что облегчит деплой.
## Создание копии в ручную.
```bash

sudo docker run --rm -v  trackholder_pg_data:/volume -v /home/andrey/trackholder/backup:/backup alpine tar czf /backup/pg_data_backup.tar.gz -C /volume .

sudo docker run --rm -v  trackholder_files:/volume -v /home/andrey/trackholder/backup:/backup alpine tar czf /backup/files_backup.tar.gz -C /volume .
```
```bash
scp -i ~/.ssh/id_rsa -r andrey@45.8.127.18:/home/andrey/trackholder/backup/ C:\Users\андрей\backup
```
