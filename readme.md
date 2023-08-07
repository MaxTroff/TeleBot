deserts&beverages

Для работы бота необходимо запустить файл main.py;

Для изменения внешнего API сайта необходимо в файле .env изменить RAPID_API_KEY, RAPID_API_HOST, API_BASE_URL, а также настроить различные функции скрипта api.py в соответствии с API и предоставляемой информацией нового сайта;

Команды, воспринимаемые ботом: 

-Команда /all: вывод списка всех товаров указанной категории;
    После ввода команды у пользователя запрашивается:
        1. Название категории, в которой необходимо вывести список всех товаров;

-Команда /low: вывод минимальных по стоимости товаров;
    После ввода команды у пользователя запрашивается:
        1.Товар, по которому будет проводиться поиск (самая низкая стоимость);
        2. Количество товаров категории, которое необходимо вывести(не более 10);

-Команда /high: вывод максимальных по стоимости товаров;
    После ввода команды у пользователя запрашивается:
        1.Товар, по которому будет проводиться поиск (самая высокая стоимость);
        2. Количество товаров категории, которое необходимо вывести(не более 10);

-Команда /custom: вывод товаров из пользовательского диапазона по стоимости;
    После ввода команды у пользователя запрашивается:
        1. Товар, по которому будет проводиться поиск;
        2. Диапазон значений выборки(цена от и до);
        3. Количество товаров категории, которые необходимо вывести(не более 10);

-Команда /desc: вывод описания товара с указанным id;
    После ввода команды у пользователя запрашивается:
        1. Название категории, в которой будет искомый товар;
        -Далее пользователю предоставляется список всех доступных названий и id товаров в указанной категории;
        2. id товара, к которому необходимо вывести описание;

-Команда /photo: вывод фоотографии товара с указанным id;
    После ввода команды у пользователя запрашивается:
        1. Название категории, в которой будет искомый товар;
        -Далее пользователю предоставляется список всех доступных названий и id товаров в указанной категории;
        2. id товара, к которому необходимо вывести фотографию;

-Команда /history: краткая история запросов;
    После ввода команды выводится краткая история запросов пользователя(последние
    десять запросов);

-Команда /help: доступные команды;
    После ввода команды выводятся доступные команды бота;