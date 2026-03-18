from flask import Flask, render_template, request, redirect
app = Flask(__name__)
# __name__ is a built-in variable that tells how a file is being used.
# where this file is located,where templates folder is,where static files are
tasks = []
def load_tasks():
    try:
        with open("tasks.txt", "r") as file: 
            # automatically closes file.(safer and cleaner option)
            for line in file:
                parts = line.strip().split("|")
                # handle old data (without time)
                if len(parts) == 3:
                    task, date, done = parts
                    time = "00:00"
                else:
                    task, date, time, done = parts
                tasks.append({
                    "task": task,
                    "date": date,
                    "time": time,
                    "done": done == "True"
                })
    except:
        pass
def save_tasks():
    with open("tasks.txt", "w") as file:
        for t in tasks:
            file.write(f"{t['task']}|{t['date']}|{t['time']}|{t['done']}\n")
            # converts dict into string,saves in file
@app.route("/")
# it is decorator used to connect a specific URL path on your website to python function.
def index():
    return render_template("index.html", tasks=tasks)
#To display tasks on screen(Opens HTML file,Sends tasks data to it)
@app.route("/add", methods=["POST"])
# POST is used to send data
def add():
    task = request.form.get("task")
    date = request.form.get("date")
    time = request.form.get("time")
    # request → contains all data sent by user
    # form → data from HTML form
    # get("task") → gets value from input field named "task"
    if task and date and time:
        tasks.append({
            "task": task,
            "date": date,
            "time": time,
            "done": False
        })
        save_tasks()
    return redirect("/")
# prevents duplicate submission
@app.route("/done/<int:index>")
def done(index):
    tasks[index]["done"] = True
    # {"task": "Study", "done": False}
    # {"task": "Study", "done": True}
    save_tasks()
    return redirect("/")
@app.route("/delete/<int:index>")
def delete(index):
    tasks.pop(index)
    save_tasks()
    return redirect("/")
if __name__ == "__main__":
    load_tasks()
    app.run(debug=True)