from flask import Flask, render_template, request
import sql_handler
from sql_handler import _DB_SESSION, Task, _BASE


app = Flask(__name__)
sql_handler.init()

print(_BASE.metadata.tables.keys())
results = Task.query.all()
print(results)

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		task_name = request.form['task_name']
		task = Task(task_name)
		_DB_SESSION.add(task)
		_DB_SESSION.commit()
	
	tasks = Task.query.all()
	return render_template('base.html', tasks=tasks)

@app.teardown_appcontext
def shutdown_session(exception=None):
	_DB_SESSION.remove()

if __name__ == "__main__":
	app.run(debug=True)
