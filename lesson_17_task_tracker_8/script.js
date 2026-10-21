let tasks = [];


function render_tasks(){

    let ul = document.getElementById("tasklist");

    ul.innerHTML = "";

    for (let task of tasks){
        console.dir(task);

        let li = document.createElement("li");

        if (task.is_complete == true){
            li.className = "task completed";
        }else{
            li.className = "task";
        }
        
        let checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.is_complete;

        checkbox.addEventListener("change", ()=>change_status_checkbox_click(task.id));

        let span = document.createElement("span");
        span.className = "task-title";
        span.textContent = task.title;

        let button = document.createElement("button");
        button.className = "delete-button";
        button.textContent = "Удалить";

        button.addEventListener("click", ()=>delete_task_button_click(task.id));

        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(button);

        ul.appendChild(li);
    }

}

function render_stats(){
    let div = document.getElementById("stats");

    let complete_tasks = 0;

    for (let task of tasks){
        if (task.is_complete == true){
            complete_tasks++;
        }
    }

    div.textContent = `Выполнено ${complete_tasks} из ${tasks.length}`;

}

async function load_tasks(){
    let response = await fetch("http://127.0.0.1:8000/api/tasks");

    console.dir(response);

    tasks = await response.json();

    console.dir(tasks);

    render_tasks();
    render_stats();
}

load_tasks();

async function delete_task_button_click(id){
    let response = await fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {method: "DELETE"});

    if (!response.ok) {
        alert("Ошибка удаления задачи");
    }

    load_tasks();
}

async function add_task_button_click(){
    let input = document.getElementById("taskInput");

    let title = input.value.trim();
    let id = 0;
    let is_complete = false;

    let newTask = {
        id:id,
        title:title,
        is_complete:is_complete
    }

    let response = await fetch("http://127.0.0.1:8000/api/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(newTask)
    });

    if (!response.ok) {
        alert("Ошибка добавления задачи");
        return;
    }

    input.value = "";

    load_tasks();
}

async function change_status_checkbox_click(id){
    let task = tasks.find(task=>task.id==id);

    let updatedTask = {
        id: task.id,
        title: task.title,
        is_complete: !task.is_complete
    };

   
    let response = await fetch(`http://127.0.0.1:8000/api/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(updatedTask)
    });

    if (!response.ok) {
        alert("Ошибка обновления задачи");
        return;
    }
   

    load_tasks();
}
