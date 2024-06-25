#Creates an instance of the flask object
from flask import Flask, request, render_template
app = Flask(__name__)

# Initialize the food_entries list at the top level of the app
food_entries = []

#Maps url route and returns content
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/second", methods=["GET", "POST"])
def BMRCalc():
    if request.method == "POST":
        try:
            weight_pounds = float(request.form["weight"])
            height_inches = float(request.form["height"])
            age = int(request.form["age"])
            sex = request.form["sex"].upper()

            # Convert weight to kilograms and height to centimeters
            weight_kg = weight_pounds * 0.453592
            height_cm = height_inches * 2.54

            if sex == "M":
                bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
            elif sex == "F":
                bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
            else:
                return render_template("BMRCalc.html", error="Invalid sex. Please enter 'M' or 'F'.", bmr=None)

            bmr = round(bmr, 3)

            return render_template("BMRCalc.html", bmr=bmr)
        except ValueError:
            return render_template("BMRCalc.html", error="Please enter valid numeric values for weight, height, and age.", bmr=None)
    return render_template("BMRCalc.html", bmr=None)
    

@app.route("/third", methods=["GET", "POST"])
def BMICalc():
    if request.method == "POST":
        try:
            height_feet = float(request.form["heightFeet"])
            height_inches = float(request.form["heightInches"])
            weight_pounds = float(request.form["weight"])

            # Convert height to total inches and then to meters
            total_height_inches = (height_feet * 12) + height_inches
            height_meters = total_height_inches * 0.0254

            # Convert weight to kilograms
            weight_kg = weight_pounds * 0.453592

            # Calculate BMI
            bmi = weight_kg / (height_meters ** 2)

            bmi = round(bmi, 3)
            
            return render_template("BMICalc.html", bmi=bmi)
        except ValueError:
            return render_template("BMICalc.html", error="Please enter valid numeric values for weight and height.", bmi=None)
    return render_template("BMICalc.html", bmi=None)
  




@app.route("/fourth", methods=["GET", "POST"])
def food_diary():
    global food_entries
    if request.method == "POST":
        food = request.form.get("food")
        calories = request.form.get("calories")
        try:
            calories = int(calories)
            food_entries.append({"food": food, "calories": calories})
        except ValueError:
            return render_template("food_diary.html", food_entries=food_entries, error="Please enter a valid number for calories.")
    
    total_calories = sum(entry["calories"] for entry in food_entries)
    return render_template("food_diary.html", food_entries=food_entries, total_calories=total_calories)

#allows the application to run
if __name__ == "__main__":
    app.run(debug=True)