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

            # Validate inputs
            if weight_pounds <= 0 or height_inches <= 0 or age <= 0 or sex not in ["M", "F"]:
                return render_template("BMRCalc.html", error="Please enter valid values for weight, height, age, and sex ('M' or 'F').", 
                                       weight=weight_pounds, height=height_inches, age=age, sex=sex)

            # Convert weight to kilograms and height to centimeters
            weight_kg = weight_pounds * 0.453592
            height_cm = height_inches * 2.54

            if sex == "M":
                bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
            elif sex == "F":
                bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

            bmr = round(bmr, 0)

            return render_template("BMRCalc.html", bmr=bmr, weight=weight_pounds, height=height_inches, age=age, sex=sex)

        except ValueError:
            return render_template("BMRCalc.html", error="Please enter valid numeric values for weight, height, and age.", 
                                   weight=request.form["weight"], height=request.form["height"], age=request.form["age"], sex=request.form["sex"])

    return render_template("BMRCalc.html", bmr=None)




@app.route("/third", methods=["GET", "POST"])
def BMICalc():
    if request.method == "POST":
        try:
            height_feet = float(request.form["heightFeet"])
            height_inches = float(request.form["heightInches"])
            weight_pounds = float(request.form["weight"])

            if height_feet <= 0 or height_inches < 0 or weight_pounds <= 0:
                return render_template("BMICalc.html", error="Please enter positive values for height and weight.", bmi=None)

            # Convert height to total inches and then to meters
            total_height_inches = (height_feet * 12) + height_inches
            height_meters = total_height_inches * 0.0254

            # Convert weight to kilograms
            weight_kg = weight_pounds * 0.453592

            # Check if height_meters is zero (to avoid division by zero)
            if height_meters == 0:
                return render_template("BMICalc.html", error="Please enter a valid height (non-zero value).", bmi=None)

            # Calculate BMI
            bmi = weight_kg / (height_meters ** 2)
            bmi = round(bmi, 2)

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
        
        # Validate food input
        if not food or not food.isalpha():
            return render_template("food_diary.html", food_entries=food_entries, error="Please enter a valid food item without numbers or special characters.")
        
        try:
            calories = int(calories)
            if calories < 0:
                return render_template("food_diary.html", food_entries=food_entries, error="Calories cannot be negative.")
            food_entries.append({"food": food, "calories": calories})
        except ValueError:
            return render_template("food_diary.html", food_entries=food_entries, error="Please enter a valid number for calories.")

    total_calories = sum(entry["calories"] for entry in food_entries)
    return render_template("food_diary.html", food_entries=food_entries, total_calories=total_calories)

#allows the application to run
if __name__ == "__main__":
    app.run(debug=True)
