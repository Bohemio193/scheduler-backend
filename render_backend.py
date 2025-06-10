#!/usr/bin/env python3
"""
Backend Flask optimizado para Render
Scheduler Pro - Sistema de mensajería programada
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuración para Render
PORT = int(os.environ.get('PORT', 10000))

# Datos de ejemplo (simulando base de datos)
messages_db = {
    "scheduled": [],
    "sent": [],
    "templates": [
        {"id": 1, "name": "Reunión", "content": "Recordatorio: Tienes una reunión a las {time}"},
        {"id": 2, "name": "Medicamento", "content": "Es hora de tomar tu medicamento"},
        {"id": 3, "name": "Ejercicio", "content": "¡Hora de hacer ejercicio! 💪"}
    ]
}

users_db = {
    "demo@scheduler.com": {
        "password": "demo123",
        "name": "Usuario Demo"
    }
}

@app.route('/')
def home():
    """Página de inicio con información del API"""
    return jsonify({
        "message": "Scheduler Pro Backend API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/api/auth/login",
            "/api/messages",
            "/api/messages/send",
            "/api/templates"
        ]
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Autenticación de usuarios"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        logger.info(f"Intento de login para: {email}")
        
        if email in users_db and users_db[email]['password'] == password:
            return jsonify({
                "success": True,
                "user": {
                    "email": email,
                    "name": users_db[email]['name']
                },
                "token": "demo_token_123"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Credenciales incorrectas"
            }), 401
            
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error del servidor"
        }), 500

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Obtener todos los mensajes"""
    try:
        return jsonify({
            "success": True,
            "data": messages_db
        })
    except Exception as e:
        logger.error(f"Error obteniendo mensajes: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error obteniendo mensajes"
        }), 500

@app.route('/api/messages', methods=['POST'])
def schedule_message():
    """Programar un nuevo mensaje"""
    try:
        data = request.get_json()
        
        new_message = {
            "id": len(messages_db["scheduled"]) + 1,
            "content": data.get('content'),
            "schedule_time": data.get('schedule_time'),
            "recipient": data.get('recipient'),
            "type": data.get('type', 'sms'),
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
        
        messages_db["scheduled"].append(new_message)
        logger.info(f"Mensaje programado: {new_message['id']}")
        
        return jsonify({
            "success": True,
            "message": "Mensaje programado exitosamente",
            "data": new_message
        })
        
    except Exception as e:
        logger.error(f"Error programando mensaje: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error programando mensaje"
        }), 500

@app.route('/api/messages/send', methods=['POST'])
def send_immediate():
    """Enviar mensaje inmediato"""
    try:
        data = request.get_json()
        
        sent_message = {
            "id": len(messages_db["sent"]) + 1,
            "content": data.get('content'),
            "recipient": data.get('recipient'),
            "type": data.get('type', 'sms'),
            "status": "sent",
            "sent_at": datetime.now().isoformat()
        }
        
        messages_db["sent"].append(sent_message)
        logger.info(f"Mensaje enviado: {sent_message['id']}")
        
        return jsonify({
            "success": True,
            "message": "Mensaje enviado exitosamente",
            "data": sent_message
        })
        
    except Exception as e:
        logger.error(f"Error enviando mensaje: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error enviando mensaje"
        }), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Obtener plantillas de mensajes"""
    try:
        return jsonify({
            "success": True,
            "data": messages_db["templates"]
        })
    except Exception as e:
        logger.error(f"Error obteniendo plantillas: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error obteniendo plantillas"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificación de salud del servidor"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint no encontrado"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Error interno del servidor"
    }), 500

if __name__ == '__main__':
    logger.info(f"Iniciando servidor en puerto {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)