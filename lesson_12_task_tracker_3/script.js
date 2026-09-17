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

function render_tasks(){

    let ul = document.getElementById("tasklist");

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

        let span = document.createElement("span");
        span.className = "task-title";
        span.textContent = task.title;

        let button = document.createElement("button");
        button.className = "delete-button";
        button.textContent = "Удалить";

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