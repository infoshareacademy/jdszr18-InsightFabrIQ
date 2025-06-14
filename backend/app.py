from flask import Flask
from flask_cors import CORS
from routes import predict, images

app = Flask(__name__)
CORS(app)


app.register_blueprint(predict.bp)
app.register_blueprint(images.bp)


@app.route('/')
def home():
    return {'message': 'API is running!'}


if __name__ == '__main__':
    app.run(debug=True)
