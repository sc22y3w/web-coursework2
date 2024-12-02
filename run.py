# importing the app package and runs the server with debugging
from app import app
if __name__ == "__main__":
  app.run(debug=True)

# QUICK LOAD: python -m flask run

# Run with debug mode:
## set FLASK_APP=run.py
## set FLASK_DEBUG=1
## flask run