# Protection
Дипломная работа ИТМО

1. Создать базу данных в СУБД PostgreSQL "labor_protection" и загрузить в нее бекап файл labor_protection.bak из основной ветки репозитория
2. в файле app.py в сроке app.config['SQLALCHEMY_DATABASE_URI'] необходимо указать Ваши параметрты от СУБД
3. запустить исполняемый файл laborprotection.py
4. В базу данных добавлено 3 пользователя:
   Owen21 - пользователь с ролью Администартор, пароль 123
   Alymova- пользователь с ролью менедженер, пароль 123
   user2- пользователь с ролью пользователь, пароль 123
5. В папку tests - добавлены файлы для тестирования доступности стриниц и тестирования создания мест обучения
