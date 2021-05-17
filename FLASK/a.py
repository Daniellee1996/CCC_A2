from flask import Flask, render_template, Response, request ,jsonify
import json

app = Flask(__name__)

xdays = ["shirts", "cardigan", "sneaker", "pants", "highheel", "sock"]
yvalues = [5, 20, 36, 10, 10, 20]
json_data = json.dumps({"xdays": xdays, "yvalues": yvalues})

@app.route("/viewdata", methods=["POST"])
def viewdata():
    if request.method == "POST":
        return json_data
    else:
        return json_data


@app.route('/')
def hello():
    return render_template('my_template.html')
    


if __name__ == "__main__":
    app.run(debug=True,port=5000)