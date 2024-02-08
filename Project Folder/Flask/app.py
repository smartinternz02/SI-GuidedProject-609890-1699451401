import pickle
from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates")
try:
    model = pickle.load(open("lr.pkl", "rb"))
except Exception as e:
    app.logger.error(f"Error loading model: {str(e)}")

@app.route('/')
def inp():
    return render_template('index.html')

@app.route("/prediction", methods=['GET', 'POST'])
def predict():
    low = eval(request.form["low"])
    high = eval(request.form["high"])
    volume = eval(request.form["volume"])
    open_val = eval(request.form["open"]) 
    company = eval(request.form["company"])
    year = eval(request.form["year"])
    month = eval(request.form["month"])
    day = eval(request.form["day"])

    try:
        prediction = model.predict([[open_val, high, low, volume, year, month, day, company]])
        out = prediction[0]
        print("Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out))
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return render_template("inner-page.html", p="Error in prediction")

    return render_template("inner-page.html", p="Forecasted closing price on {}/{}/{} is $ {}".format(day, month, year, out))

if __name__ == '__main__':
    app.run(debug=True)