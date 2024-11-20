from flask import Flask, render_template_string, request
import subprocess
import threading

app = Flask(__name__)

# HTML template for the web interface
html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Live Bash Console</title>
    <style>
      body { font-family: monospace; }
      #output { white-space: pre-wrap; word-wrap: break-word; background: #222; color: #fff; padding: 10px; height: 300px; overflow-y: scroll; }
      input { width: 100%; padding: 10px; font-size: 1.2em; background-color: #333; color: #fff; border: none; }
    </style>
  </head>
  <body>
    <h1>Live Bash Console</h1>
    <div id="output">{{ output }}</div>
    <form action="/" method="POST">
      <input type="text" name="command" placeholder="Enter command..." />
    </form>
  </body>
  <script>
    setInterval(function() {
      fetch('/output')
        .then(response => response.text())
        .then(text => document.getElementById('output').innerText = text);
    }, 1000);
  </script>
</html>
'''

# In-memory output storage
console_output = ""

# Run bash command and capture live output
def run_command(command):
    global console_output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        console_output += line.decode("utf-8")
    process.stdout.close()
    process.wait()

@app.route("/", methods=["GET", "POST"])
def index():
    global console_output
    if request.method == "POST":
        command = request.form["command"]
        threading.Thread(target=run_command, args=(command,)).start()
    return render_template_string(html_template, output=console_output)

@app.route("/output")
def output():
    return console_output

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
