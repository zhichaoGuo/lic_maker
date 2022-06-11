from serve import app
from serve.index import index
from serve import DataBase



app.register_blueprint(index)
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050,debug=False)
