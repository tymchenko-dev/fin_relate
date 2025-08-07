from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '127.0.0.1')  # Можно переопределить через переменную окружения
    app.run(debug=debug_mode, port=port, host=host)
