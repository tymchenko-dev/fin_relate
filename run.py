from app import create_app
import os

# Set environment
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    debug_mode = config_name == 'development'
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0' if config_name == 'production' else '127.0.0.1')
    app.run(debug=debug_mode, port=port, host=host)
