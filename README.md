# Docker Compose

## Chrome
Configuration Google Chrome for SSL certificate.
Add file "rootCA.crt" to: Settings -> Advanced -> Privacy and Security -> Manage Certificates -> Authorities -> Import

## MySQL
```sh
/usr/bin/mysql_secure_installation
```
  - Enter current password for root (enter for none): 1234
  - Switch to unix_socket authentication [Y/n]        N
  - Change the root password? [Y/n]                   N
  - Remove anonymous users? [Y/n]                     Y
  - Disallow root login remotely? [Y/n]               N
  - Remove test database and access to it? [Y/n]      Y
  - Reload privilege tables now? [Y/n]                Y

Auto-install, not working now.
```sh
debconf-set-selections <<< "название_пакета имя_вопроса тип_вопроса значение"
debconf-set-selections <<< "postfix postfix/mailname string your.hostname.com"
debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
apt-get install --assume-yes postfix
```

```sh
SELECT host, user, password FROM mysql.user;
```
| Host      | User  | Password                                  |
|-----------|-------|-------------------------------------------|
| localhost | root  | *A4B6157319038724E3560894F7F932C8886EBFCF |
| %         | root  | *A4B6157319038724E3560894F7F932C8886EBFCF |
| %         | admin | *00A51F3F48415C7D4E8908980D443C29C69B60C9 |
```sh
DROP DATABASE `dbname`;
CREATE DATABASE `dbname`;
GRANT ALL PRIVILEGES ON `dbname`.* TO 'admin'@'%';
FLUSH PRIVILEGES;
```

## PHPStorm
File -> Settings -> Languages & Frameworks -> PHP -> Debug -> DBGp Proxy
```sh
IDE key: PHP_STORM
Host: 172.23.0.4
Port: 9000
```

File -> Settings -> Languages & Frameworks -> PHP -> Servers
```sh
Name: example.local
Host: example.local
Port: 443
Use path mappings:
/var/www/html
/var/www/html/pub
```

Optionally, to tell PhpStorm which path mapping configuration should be used for a connection from a certain machine, the value of the PHP_IDE_CONFIG environment variable should be set to serverName=SomeName, where SomeName is the name of the server configured on the Languages & Frameworks | PHP | Servers page of the Settings/Preferences dialog Ctrl+Alt+S.

## Email
```sh
echo "My message" | mail -s "My Subject" email@example.com
mail -s "My Subject" email@example.com
```
```sh
/etc/init.d/sendmail status
/etc/init.d/sendmail start
/etc/init.d/postfix status
```
```sh
docker run -d --name postfix -p "25:25"  \
    -e SMTP_SERVER=smtp.example.com \
    -e SMTP_USERNAME=email@example.com \
    -e SMTP_PASSWORD=XXXXXXXX \
    -e SERVER_HOSTNAME=helpdesk.mycompany.com \
    juanluisbaptiste/postfix
```
```sh
docker run -d --name postfix -P \
    -e SMTP_SERVER=smtp.gmail.com \
    -e SMTP_USERNAME=email@example.com \
    -e SMTP_PASSWORD=XXXXXXXX \
    -e SERVER_HOSTNAME=gmail.com \
    juanluisbaptiste/postfix
```
