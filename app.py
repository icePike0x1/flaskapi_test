from flask import Flask
from flask import request, jsonify
import hashlib

user = {'username':'Igor'}

taskDatabase = {
                    
               }

id_to_uuid = {}
next_id = ''

app = Flask(__name__)

def chk_post_number(number):
    try:
        data=int(number)
    except:
        return False
    return True

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
@app.route('/tasks/<post_id>', methods=['GET'])
def list_tasks(post_id=None):
    if post_id:
        if chk_post_number(post_id) and post_id in taskDatabase:
            return taskDatabase[post_id]
        else:
            return f"you have to provide correct post ID (integer number)"
        
    else:
        return jsonify(taskDatabase)

@app.route('/tasks/', methods=['DELETE'])
@app.route('/tasks/<post_id>', methods=['DELETE'])
def delete_task(post_id=None):
        if post_id and chk_post_number(post_id):
            if post_id in taskDatabase:
#                 print(type(post_id))
#                 print(post_id)        
                task_hash = compute_hash(post_id)    
                del id_to_uuid[task_hash]
                del taskDatabase[post_id]        
                return f"task with ID {post_id} was deleted"
            else:
                return f"task with ID {post_id} does not exist..."
        else:
            return f"you have to provide correct post ID (integer number) to remove..."

@app.route('/tasks', methods=['POST'])
def add_task():
    if request.method == 'POST':
        global next_id
        data = request.get_json()
        if data:
            compute_next_id()
#             print(type(data))
#             print(data)
            taskDatabase[next_id] = dict(data)
            new_task_hash = compute_hash(next_id)
            id_to_uuid[new_task_hash] = next_id
            return_value = f"added new task with id: {next_id}" 
            return return_value


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')