# Docker Compose

## Docker
Run the docker.bash file via /bin/bash.
This will help you use docker containers.

## Magento
Run the magento.bash file via /bin/bash.
This will help you use commands Magento 2 CLI terminal.

## Docker Projects
Run the docker.pyc file via /bin/python3.
This will help you use docker containers.

Required creating the "projects.json" file by example:
```json
[
    {
        "name": "Magento 2",
        "dockerPath": "/home/user/Magento 2/docker",
        "magento": {
            "container": "magento234_php-fpm_1",
            "user": "www-data",
            "groups": ["cache", "indexer", "setup"]
        },
        "tools": {
            "webContainer": "magento2_nginx_1",
            "phpContainer": "magento2_php-fpm_1",
            "mysqlContainer": "magento2_mariadb_1",
            "mysqlUser": "root",
            "mysqlPassword": "1234",
            "mysqlDumpDir": "/home/user/Magento 2/dumps",
            "esContainer": "magento2_elasticsearch_1",
            "redisContainer": "magento2_redis_1"
        }
    }
]
```
  - **name** - Project name (recommended)
  - **dockerPath** - Полный путь каталога где находится docker-compose.yml файл (обязательно)

  - **magento** - Конфигурация для работы модуля: magento (при использовании)
  - **container** - Полное имя PHP контейнера (обязательно)
  - **groups** - Группы команд которые будет видно, остальные будут скрыты (по желанию)

  - **tools** - Конфигурация для работы модуля: tools (при использовании)
  - **phpContainer** - Полное имя PHP контейнера (обязательно для XDebugger команд)
  - **mysqlContainer** - Полное имя PHP контейнера (обязательно для MySQL команд)
  - **mysqlUser** - Имя пользователя для доступа к MySQL (обязательно для MySQL команд)
  - **mysqlPassword** - Пароль пользователя для доступа к MySQL (обязательно для MySQL команд)
  - **mysqlDumpDir** - Полный путь для експорта/импорта базы данных (рекомендовано)
  - **esContainer** - Полное имя Elasticsearch контейнера (обязательно для Elasticsearch команд)
  - **redisContainer** - Full name the redis container (required for redis commands).

В вашем распоряжении удобное управление всеми проектами и их контейнерами. В целях безопасности и предотвращения сбоя/конфликтов между контейнерами, запуск двух и более проектов одновременно, не предусмотренно.

Step #1 - Projects list
Select project and run

Step #2 - Containers list
Select container and 
Выбор контейнера для управления
Запуск дополнительных утилит, таких как magento and tools.

### Desktop - Linux
You can create desktop link
1. Open folder: ~/.local/share/applications
2. Create file with name: docker-projects.desktop
3. File content the next:
```ini
[Desktop Entry]
Version=1.0
Name=Docker Projects
Comment=Terminal for docker projects
Exec=python3 /home/user/projects/docker.pyc
Icon=/home/user/projects/docker.png
Path=/home/user/projects
Terminal=true
Type=Application
Categories=Application;
```
