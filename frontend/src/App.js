import React, { Component } from 'react';
import { io } from 'socket.io-client';
import './App.css';

const API_URL = 'http://localhost:5001/api/tasks';

class App extends Component {
  state = {
    tasks: [],
    title: '',
    description: ''
  };

  socket = null;

  componentDidMount() {
    // Fetch existing tasks from backend
    this.fetchTasks();

    // Connect to backend socket
    this.socket = io('http://localhost:5001');

    this.socket.on('task_added', (task) => {
      this.setState({ tasks: [...this.state.tasks, task] });
    });

    this.socket.on('task_updated', (updatedTask) => {
      this.setState({
        tasks: this.state.tasks.map(task =>
          task.id === updatedTask.id ? updatedTask : task
        )
      });
    });

    this.socket.on('task_deleted', ({ id }) => {
      this.setState({
        tasks: this.state.tasks.filter(task => task.id !== id)
      });
    });
  }

  fetchTasks = async () => {
    try {
      const res = await fetch(API_URL);
      const data = await res.json();
      this.setState({ tasks: data });
    } catch (err) {
      console.error('Failed to fetch tasks:', err);
    }
  };

  handleChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleAddTask = async () => {
    const { title, description } = this.state;
    if (!title) return;

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description })
      });
      if (!res.ok) throw new Error('Failed to add task');
      this.setState({ title: '', description: '' });
    } catch (err) {
      console.error(err);
    }
  };

  handleDeleteTask = async (id) => {
    try {
      const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete task');
    } catch (err) {
      console.error(err);
    }
  };

  toggleComplete = async (task) => {
    try {
      const res = await fetch(`${API_URL}/${task.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task.completed })
      });
      if (!res.ok) throw new Error('Failed to update task');
    } catch (err) {
      console.error(err);
    }
  };

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Real-time Task Manager</h1>

          <div className="task-input">
            <input
              type="text"
              name="title"
              placeholder="Task title"
              value={this.state.title}
              onChange={this.handleChange}
            />
            <input
              type="text"
              name="description"
              placeholder="Task description"
              value={this.state.description}
              onChange={this.handleChange}
            />
            <button onClick={this.handleAddTask}>Add Task</button>
          </div>

          <ul className="task-list">
            {this.state.tasks.map(task => (
              <li key={task.id} className={task.completed ? 'completed' : ''}>
                <h3 onClick={() => this.toggleComplete(task)}>{task.title}</h3>
                <p>{task.description}</p>
                <button onClick={() => this.handleDeleteTask(task.id)}>Delete</button>
              </li>
            ))}
          </ul>
        </header>
      </div>
    );
  }
}

export default App;
