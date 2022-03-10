import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        dealer = request.form['dealer']
        year = request.form['year']
        price = request.form['price']
        distance = request.form['distance']
        owner = request.form['owner']
        fuel = request.form['fuel']
        transmission = request.form['transmission']
        fuel_diesel = 0
        fuel_petrol = 0
        if fuel==1:
            fuel_petrol = 1
        if fuel==2:
            fuel_diesel = 1
        if not year or not price or not distance or not owner:
            return render_template('index.html', warn="Please fill all the fields")
        else:
            prediction = model.predict([[price,distance,owner,year,fuel_diesel,fuel_petrol,dealer,transmission]])
            output = round(prediction[0],2)
            if output<0:
                return render_template('index.html',message="Sorry, Your can can't be sold")
            return render_template('index.html',message="Expected selling price of your car is {} Lakhs".format(output))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)