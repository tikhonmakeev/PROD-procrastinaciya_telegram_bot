# Бот-медиум  

Пользователь регистрирует свои каналы на сайте, добавляя бота в админов канала  
Через код подтверждения проверяется принадлежность  

Дальше бот используется для отложенной отправки постов в каналы, получая `таски` от сервера  
У этих постов могут быть прикрепленные файлы, markdown оформление и так далее, и тому подобное  

В целом он управляется сервом в локальном докер-контейнере, получая `асинхронные http-request'ы`  
Пример сервера есть в [тестовом Flask-приложении](test.py)

Бот можно запустить вне докер-контейнера, тогда нужно заменить `server_url` в [main.py](main.py)  

Запуская `docker-compose up --build`, поднимаются и бот, и тестовый сервер  
  
  
# Алгоритм реального использования  
![один-клиент-ждет](https://github.com/user-attachments/assets/37942649-48e8-4249-95fe-7ea5f8ac3dc7)
![сервер-получил-новое](https://github.com/user-attachments/assets/61ec0900-e11f-42ba-8a66-f84fc9a0fb5d)
![клиент-получил-таск](https://github.com/user-attachments/assets/f0e0383e-254c-476e-9531-7a5e5f488107)
![бот-отправил-сообщение](https://github.com/user-attachments/assets/fd4e8497-1efb-4024-acc1-db3acb12742c)
![один-клиент-ждет](https://github.com/user-attachments/assets/9dea1575-6021-43aa-904d-ecbebdeea806)
