from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint('main', __name__)

workouts = []

@main.route('/')
def home():
  return render_template('index.html')

@main.route('/add', methods=['POST'])
def add_workout():
  workout = request.form.get('workout')
  duration = request.form.get('duration')

  if not workout or not duration:
    flash("Please enter both workout and duration.", "error")
    return redirect(url_for('main.home'))

  try:
    duration = int(duration)
    workouts.append({"workout": workout, "duration": duration})
    flash(f"'{workout}' added successfully!", "success")
  except ValueError:
    flash("Duration must be a number.", "error")

  return redirect(url_for('main.home'))

@main.route('/workouts')
def view_workouts():
  return render_template('workouts.html', workouts=workouts)
