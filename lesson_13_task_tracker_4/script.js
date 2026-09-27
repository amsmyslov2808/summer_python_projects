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

let task_global_id = 2;

function get_next_task_id(){
    task_global_id++;

    return task_global_id;
}


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

render_tasks();
render_stats();

function add_task_button_click(){
    let input = document.getElementById("taskInput");

    let title = input.value.trim();
    let id = get_next_task_id();
    let is_complete = false;

    let newTask = {
        id:id,
        title:title,
        is_complete:is_complete
    }

    tasks.push(newTask);

    input.value = "";

    render_tasks();
    render_stats();
}

function delete_task_button_click(id){
    let delete_index = tasks.findIndex(task=>task.id==id);

    tasks.splice(delete_index,1);

    render_tasks();
    render_stats();
}

function change_status_checkbox_click(id){
    let status_index = tasks.findIndex(task=>task.id==id);

    if (tasks[status_index].is_complete == true){
        tasks[status_index].is_complete = false;
    }else{
        tasks[status_index].is_complete = true;
    }

    render_tasks();
    render_stats();
}
