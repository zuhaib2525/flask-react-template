import React, { useEffect, useState } from "react";
import { getTasks, createTask, updateTask, deleteTask } from "../services/TaskService";

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const { data } = await getTasks();
    setTasks(data);
  };

  const handleAdd = async () => {
    if (!newTask.trim()) return;
    await createTask({ title: newTask });
    setNewTask("");
    fetchTasks();
  };

  const handleUpdate = async (id, title) => {
    await updateTask(id, { title });
    fetchTasks();
  };

  const handleDelete = async (id) => {
    await deleteTask(id);
    fetchTasks();
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Task Manager</h2>

      {/* Add Task */}
      <div className="flex mb-4">
        <input
          type="text"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
          className="border p-2 flex-1"
          placeholder="Enter new task"
        />
        <button
          onClick={handleAdd}
          className="bg-blue-500 text-white px-4 ml-2 rounded"
        >
          Add
        </button>
      </div>

      {/* Task List */}
      <ul>
        {tasks.map((task) => (
          <li key={task.id} className="flex justify-between items-center mb-2">
            <input
              type="text"
              defaultValue={task.title}
              onBlur={(e) => handleUpdate(task.id, e.target.value)}
              className="border p-2 flex-1"
            />
            <button
              onClick={() => handleDelete(task.id)}
              className="bg-red-500 text-white px-3 ml-2 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TaskList;
