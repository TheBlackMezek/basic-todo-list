from flask import Flask, render_template, request, jsonify, make_response
import sql_handler
from sql_handler import _DB_SESSION, Task


app = Flask(__name__)
sql_handler.init()


@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		task_name = request.form['task_name']
		task = Task(task_name)
		_DB_SESSION.add(task)
		_DB_SESSION.commit()
	
	tasks = Task.query.all()
	return render_template('base.html', tasks=tasks)


@app.route('/set-task-name', methods=['POST'])
def set_task_name():
	req = request.get_json()
	print(f"Setting name of task {req['task_id']} to \"{req['task_name']}\"")

	task = _DB_SESSION.query(Task).filter_by(id=req['task_id']).first()
	task.name = req['task_name']
	_DB_SESSION.commit()

	res = make_response(jsonify({"message": "Task name changed"}), 200)
	return res


@app.route('/set-task-done', methods=['POST'])
def set_task_done():
	req = request.get_json()
	print(f"Setting done status of task {req['task_id']} to \"{req['task_done']}\"")

	task = _DB_SESSION.query(Task).filter_by(id=req['task_id']).first()
	task.done = req['task_done']
	_DB_SESSION.commit()

	res = make_response(jsonify({"message": "Task name changed"}), 200)
	return res


@app.teardown_appcontext
def shutdown_session(exception=None):
	_DB_SESSION.remove()


if __name__ == "__main__":
	app.run(debug=True)
