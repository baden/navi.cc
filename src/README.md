## Перечень компонентов системы.

Все компоненты должны собираться в каталог build основного каталога.
Содержимое каталога отправляется на сервер

### www

Клиентское HTML5-приложение.
Доступно по протоколу HTTP в виде статики через nginx.

### point

Точки сбора данных с приборов.

#### point/v4-http

Устаревающий протокол для всех ранее выпущенных приборов

### api

Сервер API.
Доступен через nginx прокси по адресу domain/api/.* перенаправление на порт 8280.

### channel

Сервер дуплексного соединения.
Доступен через прямое WebSocket-соединение domain:8281.