from flask import Flask
from routes import student_bp, summary_bp

app = Flask(__name__)

app.register_blueprint(student_bp, url_prefix='/students')
app.register_blueprint(summary_bp, url_prefix='/students/<int:id>/summary')

if __name__ == '__main__':
    app.run(debug=True)
