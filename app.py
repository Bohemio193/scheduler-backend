from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app, origins=["*"], allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Lista en memoria para almacenar los mensajes enviados
mensajes_enviados = []

# Ruta raíz para verificar que el backend funciona
@app.route('/', methods=['GET'])
def home():
    return "¡Backend funcionando correctamente desde Flask en Render!"

# Ruta de estado del backend
@app.route('/status', methods=['GET'])
def status():
    current_time = datetime.now().isoformat()
    return jsonify({
        'message': 'Backend funcionando correctamente',
        'time': current_time,
        'total_messages': len(mensajes_enviados)
    })

# Ruta para enviar mensajes
@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()
        contacto = data.get('contact')
        mensaje = data.get('message')
        
        if not contacto or not mensaje:
            return jsonify({'error': 'Faltan datos de contacto o mensaje'}), 400
        
        nuevo_mensaje = {
            'id': len(mensajes_enviados) + 1,
            'contact': contacto.strip(),
            'message': mensaje.strip(),
            'timestamp': datetime.now().isoformat(),
            'status': 'enviado'
        }
        
        mensajes_enviados.append(nuevo_mensaje)
        logger.info(f"Mensaje enviado a {contacto}: {mensaje}")
        
        return jsonify({
            'status': 'Mensaje enviado correctamente',
            'message_id': nuevo_mensaje['id'],
            'timestamp': nuevo_mensaje['timestamp']
        }), 201
        
    except Exception as e:
        logger.error(f"Error al enviar mensaje: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# Ruta para obtener todos los mensajes enviados
@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({
        'messages': mensajes_enviados,
        'total': len(mensajes_enviados)
    })

# Iniciar el servidor
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
