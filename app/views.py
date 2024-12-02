from app import app

@app.route('/') # route - defines the route/path to which the function is mapped
def index():
    return "Hello World!!!"
# @ symbol declares a decorator - provides meta information to the interpreter/library
