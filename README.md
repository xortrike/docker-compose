# Docker Compose

## Chrome
Configuration Google Chrome for SSL certificate.
Add file "rootCA.crt" to: Settings -> Advanced -> Privacy and Security -> Manage Certificates -> Authorities -> Import

## PHPStorm
Configuration debug: File -> Settings -> Languages & Frameworks -> PHP -> Debug -> DBGp Proxy
```sh
IDE key: PHP_STORM
Host: 172.23.0.4
Port: 9000
```
Configuration server name: File -> Settings -> Languages & Frameworks -> PHP -> Servers
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
Used container MailHog. Open web page mail server: http://127.0.0.1:8025/

## MySQL
Reconfiguration MySQL server.
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
```sh
SELECT `host`, `user`, `password` FROM `mysql`.`user`;
UPDATE `mysql`.`user` SET `host` = "%" WHERE `user` = "root" AND `host` = "127.0.0.1";
```
| Host      | User  | Password                                  |
|-----------|-------|-------------------------------------------|
| localhost | root  | *A4B6157319038724E3560894F7F932C8886EBFCF |
| %         | root  | *A4B6157319038724E3560894F7F932C8886EBFCF |
| %         | admin | *00A51F3F48415C7D4E8908980D443C29C69B60C9 |
```sh
DROP DATABASE `name_db`;
CREATE DATABASE `name_db`;
GRANT ALL PRIVILEGES ON `name_db`.* TO 'admin'@'%';
FLUSH PRIVILEGES;
```
Import Timezone Labels
```sh
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql
```

## User & Group
Check user existence
```
grep username /etc/passwd
```
Check group existence
```
grep groupname /etc/group
```
Changing user and group for PHP in file "/usr/local/etc/php-fpm.d/www.conf".
```
: ${APACHE_RUN_USER:=www-data}
: ${APACHE_RUN_GROUP:=www-data}
```
