// Единый адрес коллекции задач в FastAPI. Для работы приложения backend должен
// быть запущен на порту 8000, а frontend — открыт через сервер на порту 5500.
const API_URL = "http://127.0.0.1:8000/api/tasks";

// Это временная локальная копия данных для отрисовки интерфейса. Главным
// источником данных является SQLite: после перезагрузки страницы массив снова
// заполняется ответом от backend.
let tasks = [];

// Полностью перестраивает список <ul> по актуальному содержимому массива tasks.
function render_tasks(){
    let ul = document.getElementById("tasklist");

    // Удаляем прежние <li>, чтобы при повторной отрисовке строки не дублировались.
    ul.innerHTML = "";

    for (let task of tasks){
        let li = document.createElement("li");

        // Выполненная задача получает дополнительный класс completed. CSS
        // использует его, чтобы зачеркнуть текст и изменить его цвет.
        li.className = task.is_complete ? "task completed" : "task";

        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.is_complete;

        // При переключении передаём id задачи и новое состояние checkbox.
        // Замыкание сохраняет данные именно той задачи, для которой создано поле.
        checkbox.addEventListener(
            "change",
            () => change_status_checkbox_click(task.id, checkbox.checked)
        );

        let span = document.createElement("span");
        span.className = "task-title";
        span.textContent = task.title;

        let button = document.createElement("button");
        button.className = "delete-button";
        button.textContent = "Удалить";

        // Удаление выполняется по id из базы, а не по позиции задачи в массиве.
        button.addEventListener("click", () => delete_task_button_click(task.id));

        // Собираем одну строку задачи и добавляем её в общий список.
        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(button);
        ul.appendChild(li);
    }
}

// Считает выполненные задачи по данным, не анализируя HTML-разметку страницы.
function render_stats(){
    let div = document.getElementById("stats");
    let complete_tasks = 0;

    for (let task of tasks){
        if (task.is_complete === true){
            complete_tasks++;
        }
    }

    div.textContent = `Выполнено ${complete_tasks} из ${tasks.length}`;
}

// Показывает понятное сообщение пользователю, а технические детали оставляет в
// консоли разработчика. Это помогает диагностировать сетевые и серверные ошибки.
function show_error(message, error){
    console.error(message, error);
    document.getElementById("stats").textContent = message;
}

// Получает полный список задач из SQLite через GET /api/tasks и синхронизирует
// с ним интерфейс. Эта функция вызывается при загрузке и после каждого изменения.
async function load_tasks(){
    try{
        // fetch возвращает Promise, поэтому await ждёт получения HTTP-ответа.
        const response = await fetch(API_URL);

        // fetch не считает статусы 4xx и 5xx исключениями автоматически.
        // response.ok равен true только для успешных статусов 200–299.
        if (!response.ok){
            throw new Error(`HTTP ${response.status}`);
        }

        // response.json() преобразует JSON-массив из ответа в объекты JavaScript.
        tasks = await response.json();

        // Обновляем список и статистику только после получения свежих данных.
        render_tasks();
        render_stats();
    }catch(error){
        show_error("Не удалось загрузить задачи", error);
    }
}

// Отправляет название новой задачи в backend через POST /api/tasks.
async function add_task_button_click(){
    let input = document.getElementById("taskInput");
    let title = input.value.trim();

    // Не отправляем запрос, если поле пустое или содержит только пробелы.
    if (title === ""){
        return;
    }

    try{
        const response = await fetch(API_URL, {
            method: "POST",

            // Заголовок сообщает FastAPI, что тело запроса содержит JSON.
            headers: {
                "Content-Type": "application/json"
            },

            // JSON.stringify преобразует объект JavaScript в JSON-строку.
            body: JSON.stringify({title: title})
        });

        if (!response.ok){
            throw new Error(`HTTP ${response.status}`);
        }

        // Поле очищается только после того, как backend успешно сохранил задачу.
        input.value = "";

        // Не добавляем объект в tasks вручную: повторно читаем истинные данные из
        // SQLite, включая id, который база назначила автоматически.
        await load_tasks();
    }catch(error){
        show_error("Не удалось добавить задачу", error);
    }
}

// Просит backend удалить конкретную задачу через DELETE /api/tasks/{id}.
async function delete_task_button_click(id){
    try{
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok){
            throw new Error(`HTTP ${response.status}`);
        }

        // После успешного удаления снова получаем весь актуальный список.
        await load_tasks();
    }catch(error){
        show_error("Не удалось удалить задачу", error);
    }
}

// Передаёт backend новое состояние задачи через PATCH /api/tasks/{id}.
// PATCH подходит здесь, потому что меняется только поле is_complete.
async function change_status_checkbox_click(id, is_complete){
    try{
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({is_complete: is_complete})
        });

        if (!response.ok){
            throw new Error(`HTTP ${response.status}`);
        }

        await load_tasks();
    }catch(error){
        show_error("Не удалось изменить задачу", error);

        // Если запрос не прошёл, повторная загрузка возвращает checkbox в
        // фактическое состояние, которое сейчас хранится в базе.
        await load_tasks();
    }
}

// script.js подключён с атрибутом defer, поэтому к моменту выполнения HTML уже
// разобран и все нужные элементы доступны. Сразу загружаем сохранённые задачи.
load_tasks();
