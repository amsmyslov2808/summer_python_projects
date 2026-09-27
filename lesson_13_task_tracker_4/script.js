// Массив хранит состояние приложения. Каждый объект описывает одну задачу:
// её уникальный идентификатор, текст и признак выполнения.
let tasks = [
    {
        id:1,
        title:"Задача 1",
        is_complete: false
    },
    {
        id:2,
        title:"Задача 2",
        is_complete: false
    }
];

// Последний выданный идентификатор. Счётчик позволяет не переиспользовать id
// после удаления задачи и надёжно находить нужный объект в обработчиках событий.
let task_global_id = 2;

function get_next_task_id(){
    task_global_id++;

    return task_global_id;
}

// Полностью перестраивает видимый список по текущему содержимому tasks.
// Такой подход сохраняет интерфейс синхронизированным с данными после любого изменения.
function render_tasks(){

    let ul = document.getElementById("tasklist");

    // Удаляем старые элементы перед повторной отрисовкой, иначе задачи дублировались бы.
    ul.innerHTML = "";

    for (let task of tasks){
        // Диагностический вывод помогает увидеть объект задачи в консоли браузера.
        console.dir(task);

        let li = document.createElement("li");

        // Дополнительный класс включает зачёркивание текста выполненной задачи.
        if (task.is_complete == true){
            li.className = "task completed";
        }else{
            li.className = "task";
        }
        
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.is_complete;

        // Замыкание запоминает id именно этой задачи и передаёт его обработчику.
        checkbox.addEventListener("change", ()=>change_status_checkbox_click(task.id));

        let span = document.createElement("span");
        span.className = "task-title";
        span.textContent = task.title;

        let button = document.createElement("button");
        button.className = "delete-button";
        button.textContent = "Удалить";

        // Удаление выполняется по id, поэтому не зависит от позиции задачи в списке.
        button.addEventListener("click", ()=>delete_task_button_click(task.id));

        // Собираем строку задачи и только после этого добавляем её в список.
        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(button);

        ul.appendChild(li);
    }

}

// Пересчитывает статистику по данным, а не по HTML-элементам страницы.
function render_stats(){
    let div = document.getElementById("stats");

    let complete_tasks = 0;

    // Отдельно считаем задачи, у которых установлен признак выполнения.
    for (let task of tasks){
        if (task.is_complete == true){
            complete_tasks++;
        }
    }

    div.textContent = `Выполнено ${complete_tasks} из ${tasks.length}`;

}

// Первая отрисовка показывает стартовые задачи и исходную статистику
// сразу после загрузки документа.
render_tasks();
render_stats();

// Создаёт задачу из текста поля ввода и обновляет обе части интерфейса.
function add_task_button_click(){
    let input = document.getElementById("taskInput");

    let title = input.value.trim();
    let id = get_next_task_id();
    let is_complete = false;

    // Новая задача всегда начинается как невыполненная и получает уникальный id.
    let newTask = {
        id:id,
        title:title,
        is_complete:is_complete
    }

    tasks.push(newTask);

    // Очищаем поле, чтобы пользователь мог сразу вводить следующую задачу.
    input.value = "";

    render_tasks();
    render_stats();
}

// Находит задачу по id и удаляет ровно один элемент из массива.
function delete_task_button_click(id){
    let delete_index = tasks.findIndex(task=>task.id==id);

    tasks.splice(delete_index,1);

    render_tasks();
    render_stats();
}

// Переключает состояние выбранной задачи между выполненным и невыполненным.
function change_status_checkbox_click(id){
    let status_index = tasks.findIndex(task=>task.id==id);

    if (tasks[status_index].is_complete == true){
        tasks[status_index].is_complete = false;
    }else{
        tasks[status_index].is_complete = true;
    }

    // Повторная отрисовка обновляет checkbox, оформление текста и счётчик.
    render_tasks();
    render_stats();
}
