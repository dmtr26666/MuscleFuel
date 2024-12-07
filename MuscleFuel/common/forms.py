from django import forms

class CalorieCalculatorForm(forms.Form):
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    ACTIVITY_LEVEL_CHOICES = [
        (1.2, 'Sedentary (little to no exercise)'),
        (1.375, 'Lightly active (light exercise 1-3 days/week)'),
        (1.55, 'Moderately active (moderate exercise 3-5 days/week)'),
        (1.725, 'Very active (hard exercise 6-7 days/week)'),
        (1.9, 'Extra active (very hard exercise/physical job)'),
    ]
    GOAL_CHOICES = [
        ('maintain', 'Maintain Weight'),
        ('gain', 'Gain Muscle'),
        ('lose', 'Lose Fat'),
    ]

    age = forms.IntegerField(label="Age", min_value=1)
    weight = forms.FloatField(label="Weight (kg)", min_value=1)
    height = forms.FloatField(label="Height (cm)", min_value=1)
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES)
    activity_level = forms.ChoiceField(label="Activity Level", choices=ACTIVITY_LEVEL_CHOICES)
    goal = forms.ChoiceField(label="Goal", choices=GOAL_CHOICES)
