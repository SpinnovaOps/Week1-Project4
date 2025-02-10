from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)


from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Helper function to load users from the JSON file
def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

# Helper function to save users to the JSON file
def save_users(users_data):
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=4)

# Route to display the signup page
@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required!"}), 400

    # Load existing users from JSON
    users_data = load_users()

    # Check if username already exists
    for user in users_data["users"]:
        if user["username"] == username:
            return "Username already exists"
        
        
        

    # Add new user to the users list
    new_user = {"username": username, "password": password}
    users_data["users"].append(new_user)

    # Save the updated users data to the JSON file
    save_users(users_data)

    #return jsonify({"message": f"User {username} signed up successfully!"}), 201
    return redirect(url_for('todo_list'))





def load_todo():
    with open('todo.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    users = load_users()['users']
    username = request.form['username']
    password = request.form['password']

    # Check if the credentials are valid
    for user in users:
        if user['username'] == username and user['password'] == password:
            return redirect(url_for('todo_list'))  # Redirect to todo-list app
    return "Invalid credentials. Please try again."

@app.route('/todo-list')
def todo_list():
    todo_data = load_todo()
    return render_template('todo.html', tasks=todo_data['tasks'], 
                           recent_added=todo_data['recently_added'], 
                           recent_deleted=todo_data['recently_deleted'])

@app.route('/add-task', methods=['POST'])
def add_task():
    new_task = request.form['task']
    todo_data = load_todo()

    # Add the new task to the task list and recently added
    new_task_id = len(todo_data['tasks']) + 1
    task = {"id": new_task_id, "task": new_task, "completed": False}
    todo_data['tasks'].append(task)
    todo_data['recently_added'].append(task)

    # Save the updated todo data to file
    with open('todo.json', 'w') as file:
        json.dump(todo_data, file, indent=4)

    return redirect(url_for('todo_list'))

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    todo_data = load_todo()
    task_to_delete = None

    # Find the task and delete it, moving it to recently_deleted
    for task in todo_data['tasks']:
        if task['id'] == task_id:
            task_to_delete = task
            break

    if task_to_delete:
        todo_data['tasks'].remove(task_to_delete)
        todo_data['recently_deleted'].append(task_to_delete)

        # Save the updated todo data to file
        with open('todo.json', 'w') as file:
            json.dump(todo_data, file, indent=4)

    return redirect(url_for('todo_list'))

@app.route('/view-recently-added')
def view_recently_added():
    todo_data = load_todo()
    return jsonify(todo_data['recently_added'])

@app.route('/view-recently-deleted')
def view_recently_deleted():
    todo_data = load_todo()
    return jsonify(todo_data['recently_deleted'])

if __name__ == '__main__':
    app.run(debug=True)







