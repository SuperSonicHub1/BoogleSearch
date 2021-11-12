from flask import Flask, jsonify, request, render_template
from autocomplete import autocomplete as ac


app = Flask('app')

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/autocomplete')
def autocomplete():
    """Grabs Google's kooky autocomplete API and reformats it for the front-end."""
    # Tests for existance of query
    query = request.args.get('q', '')
    return jsonify(ac(query, kind="boogle"))


app.run(host='0.0.0.0', port=8080, debug=True)