from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')  # route for main page
def render_main():
    return "<h1>start</h1>"

app.run('0.0.0.0', 8000, debug=True)