from flask import Flask, request, render_template_string

app = Flask(__name__)

def compatibility_score(p1_answers, p2_answers):
    score = 0
    max_score = len(p1_answers) * 5
    
    for a1, a2 in zip(p1_answers, p2_answers):
        difference = abs(a1 - a2)
        score += (5 - difference)
    
    percentage = (score / max_score) * 100
    return round(percentage, 2)

questions = [
    "I prioritize studies over relationship.",
    "I like spending free time with my partner.",
    "I am comfortable sharing personal problems.",
    "I expect daily communication.",
    "I enjoy going out (movies, cafes, trips).",
    "I believe in giving personal space.",
    "I am serious about long-term commitment.",
    "I am okay with public display of affection.",
    "I manage money carefully.",
    "I trust my partner completely."
]

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>College Love Calculator</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #ff758c, #ff7eb3);
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            padding: 20px;
            color: white;
            font-size: 40px;
        }

        .container {
            width: 95%;
            max-width: 1000px;
            margin: auto;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
        }

        .question-box {
            margin-bottom: 25px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .question-text {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }

        select, input {
            padding: 8px;
            font-size: 16px;
            margin: 5px;
        }

        button {
            padding: 12px 25px;
            font-size: 18px;
            background: #ff4d6d;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
        }

        button:hover {
            background: #e63950;
        }

        .result {
            margin-top: 40px;
            text-align: center;
        }

        .percentage {
            font-size: 50px;
            font-weight: bold;
        }

        .bar-container {
            background: #ddd;
            border-radius: 20px;
            width: 100%;
            height: 30px;
            margin-top: 20px;
        }

        .bar {
            height: 30px;
            border-radius: 20px;
            text-align: center;
            color: white;
            font-weight: bold;
            line-height: 30px;
            transition: width 1s ease-in-out;
        }

        .names {
            font-size: 28px;
            margin-bottom: 15px;
        }

    </style>
</head>
<body>

<h1>❤️ College Couple Compatibility Calculator ❤️</h1>

<div class="container">

<form method="POST">

<h3>Enter Names</h3>
<input type="text" name="name1" placeholder="First Person Name" required>
<input type="text" name="name2" placeholder="Second Person Name" required>

<hr><br>

{% for i in range(questions|length) %}
<div class="question-box">
    <div class="question-text">
        Q{{i+1}}. {{questions[i]}}
    </div>

    <label>Person 1:</label>
    <select name="p1_q{{i}}">
        {% for num in range(1,6) %}
        <option value="{{num}}">{{num}}</option>
        {% endfor %}
    </select>

    <label>Person 2:</label>
    <select name="p2_q{{i}}">
        {% for num in range(1,6) %}
        <option value="{{num}}">{{num}}</option>
        {% endfor %}
    </select>
</div>
{% endfor %}

<br>
<center>
<button type="submit">Calculate Compatibility ❤️</button>
</center>

</form>

{% if result %}
<div class="result">
    <div class="names">{{name1}} ❤️ {{name2}}</div>
    <div class="percentage">{{percentage}}%</div>
    <p>{{message}}</p>

    <div class="bar-container">
        <div class="bar"
        style="width: {{percentage}}%;
        background:
        {% if percentage > 70 %}#28a745
        {% elif percentage > 40 %}#ffc107
        {% else %}#dc3545
        {% endif %};">
        {{percentage}}%
        </div>
    </div>
</div>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name1 = request.form["name1"]
        name2 = request.form["name2"]

        answers1 = []
        answers2 = []

        for i in range(len(questions)):
            answers1.append(int(request.form[f"p1_q{i}"]))
            answers2.append(int(request.form[f"p2_q{i}"]))

        percentage = compatibility_score(answers1, answers2)

        if percentage > 85:
            message = "🔥 Power Couple! Strong emotional & practical match."
        elif percentage > 70:
            message = "💖 Very Good Match! Just maintain communication."
        elif percentage > 55:
            message = "🙂 Decent Match. Needs understanding & effort."
        elif percentage > 40:
            message = "⚠️ Some major differences. Talk more openly."
        else:
            message = "❌ High mismatch. Values & expectations differ."

        return render_template_string(HTML_PAGE,
                                      result=True,
                                      name1=name1,
                                      name2=name2,
                                      percentage=percentage,
                                      message=message,
                                      questions=questions)

    return render_template_string(HTML_PAGE,
                                  result=False,
                                  questions=questions)


if __name__ == "__main__":
    app.run()
