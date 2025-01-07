document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("task-form");
    const tasksList = document.getElementById("tasks-list");

    // Fetch and display tasks
    fetchTasks();

    taskForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const title = document.getElementById("title").value;
        const description = document.getElementById("description").value;

        const task = {
            title: title,
            description: description
        };

        // Add task through API
        fetch("http://localhost:5000/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(task)
        })
        .then(response => response.json())
        .then(() => {
            fetchTasks(); // Refresh task list
            taskForm.reset();
        });
    });

    function fetchTasks() {
        fetch("http://localhost:5000/tasks")
        .then(response => response.json())
        .then(tasks => {
            tasksList.innerHTML = "<ul>" + tasks.map(task => `<li>${task.title}: ${task.description}</li>`).join('') + "</ul>";
        });
    }
});
