import sys
import os
import pytest

# Ensure root path is added
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app

@pytest.fixture
def client():
  app = create_app()
  app.config['TESTING'] = True
  client = app.test_client()
  yield client

def test_home_page_loads(client):
  """Check if home page loads successfully"""
  response = client.get('/')
  assert response.status_code == 200
  assert b"Add Workout" in response.data

def test_add_workout_valid(client):
  """Check if adding a valid workout works"""
  response = client.post('/add', data={
    'workout': 'Push Ups',
    'duration': '15'
  }, follow_redirects=True)
  assert response.status_code == 200
  assert b"added successfully" in response.data

def test_add_workout_invalid(client):
  """Check invalid workout entry (missing duration)"""
  response = client.post('/add', data={
    'workout': 'Plank',
    'duration': ''
  }, follow_redirects=True)
  assert b"Please enter both workout and duration." in response.data

def test_view_workouts_page(client):
  """Check workouts page loads"""
  response = client.get('/workouts')
  assert response.status_code == 200
