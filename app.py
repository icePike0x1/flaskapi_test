from flask import Flask
from flask import request, jsonify
import hashlib

user = {'username':'Igor'}

taskDatabase = {
                    
               }

id_to_uuid = {}
next_id = ''

app = Flask(__name__)

def compute_next_id():
    global next_id
    next_id = None 
    if taskDatabase:
        existing_ids = sorted(int(id_) for id_ in taskDatabase)
        for i in range(1, existing_ids[-1]):
            if i not in existing_ids:
                next_id = str(i)
                break
        if not next_id:
            next_id = str(existing_ids[-1] + 1)
    else:
        next_id = '1'

def compute_hash(task_id):
    task_pre_hash = str(taskDatabase[str(task_id)])
    h = hashlib.sha1()
    h.update(task_pre_hash.encode())
    task_hash = h.hexdigest()
    
    return task_hash

@app.route('/tasks', methods=['GET'])
def list_tasks():
    if request.method == 'GET':
        return jsonify(taskDatabase)
    
@app.route('/tasks', methods=['DELETE'])
def delete_task():
    if request.method == 'DELETE':
        data = request.get_json()
        if data:
            print(type(data))
            print(data)        
            task_id = data['id']
            task_hash = compute_hash(task_id)    
            del id_to_uuid[task_hash]
            del taskDatabase[task_id]        
            return f"task with ID {task_id} was deleted"

@app.route('/tasks', methods=['POST'])
def add_task():
    if request.method == 'POST':
        global next_id
        data = request.get_json()
        if data:
            compute_next_id()
            print(type(data))
            print(data)
            taskDatabase[next_id] = dict(data)
            new_task_hash = compute_hash(next_id)
            id_to_uuid[new_task_hash] = next_id
            return_value = f"added new task with id: {next_id}" 
            return return_value


if __name__ == '__main__':
    app.run()
