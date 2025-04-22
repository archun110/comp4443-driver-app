# Driver Behavior Analysis (COMP4443 Group Project)

This project analyzes driver behavior using PySpark and visualizes the results through a Flask-based dashboard.

## Features
- Spark job to summarize driving behaviors
- Flask app to display interactive charts
- Supports deployment on AWS EMR and Elastic Beanstalk

## Folder Structure
- `spark_jobs/` - PySpark processing script
- `templates/` - HTML templates
- `results/` - Generated summary and speed data

## Setup
```bash
pip install -r requirements.txt
python app.py
