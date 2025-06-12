# Instrucciones para actualizar tu repositorio en GitHub

## Paso 1: Eliminar archivo actual
1. Ve a tu repositorio: https://github.com/Bohemio193/scheduler-backend
2. Haz clic en el archivo `app.py`
3. Haz clic en el ícono de papelera (🗑️) para eliminarlo
4. Escribe "Delete old app.py" en el commit message
5. Haz clic en "Commit changes"

## Paso 2: Subir archivo corregido
1. En la página principal del repositorio, haz clic en "Add file" → "Upload files"
2. Arrastra el archivo `app_render_fixed.py` (o cópialo desde aquí)
3. **IMPORTANTE**: Antes de hacer commit, renombra el archivo de `app_render_fixed.py` a `app.py`
4. Escribe "Add corrected app.py for Render" en el commit message
5. Haz clic en "Commit changes"

## Contenido del archivo app.py (copia esto si no puedes subir el archivo):

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["*"], allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Lista para almacenar mensajes enviados
mensajes_enviados = []

@app.route('/status', methods=['GET'])
def status():
    """Endpoint para verificar el estado del backend"""
    current_time = datetime.now().isoformat()
    return jsonify({
        'message': 'Backend funcionando correctamente', 
        'time': current_time,
        'total_messages': len(mensajes_enviados)
    })

@app.route('/send-message', methods=['POST'])
def send_message():
    """Endpoint para enviar mensajes"""
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type debe ser application/json'}), 400
        
        data = request.get_json()
        contacto = data.get('contact')
        mensaje = data.get('message')
        
        if not contacto or not mensaje:
            return jsonify({'error': 'Faltan datos de contacto o mensaje'}), 400
        
        if not contacto.strip() or not mensaje.strip():
            return jsonify({'error': 'Contacto y mensaje no pueden estar vacíos'}), 400
        
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

@app.route('/messages', methods=['GET'])
def get_messages():
    """Endpoint para obtener todos los mensajes enviados"""
    return jsonify({
        'messages': mensajes_enviados,
        'total': len(mensajes_enviados)
    })

@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    """Endpoint para obtener un mensaje específico por ID"""
    mensaje = next((msg for msg in mensajes_enviados if msg['id'] == message_id), None)
    
    if not mensaje:
        return jsonify({'error': 'Mensaje no encontrado'}), 404
    
    return jsonify(mensaje)

@app.route('/messages', methods=['DELETE'])
def clear_messages():
    """Endpoint para limpiar todos los mensajes"""
    global mensajes_enviados
    count = len(mensajes_enviados)
    mensajes_enviados = []
    
    return jsonify({
        'message': f'Se eliminaron {count} mensajes',
        'total_deleted': count
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == "__main__":
    # Usar puerto de Render si está disponible
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

## Paso 3: Verificar archivos en tu repositorio
Asegúrate de tener exactamente estos 3 archivos:
- `app.py` (el archivo corregido de arriba)
- `requirements.txt` (con Flask==2.3.3, Flask-CORS==4.0.0, gunicorn==21.2.0)
- `Procfile` (con: web: python app.py)

## Paso 4: Deploy en Render
Una vez que tengas los archivos actualizados, regresa a Render y haz clic en "Implementar servicio web"
