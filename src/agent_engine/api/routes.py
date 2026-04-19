# src/agent_engine/api/routes.py
from flask import Blueprint, request, Response, stream_with_context, render_template, jsonify
import json
import sys
import os

# Add the path to the project
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agent_engine.core.message import Message
from agent_engine.core.conversation import Conversation
from agent_engine.core.agent import Agent
from agent_engine.infrastructure.database.sql_repository import SQLRepository

chat_bp = Blueprint('chat', __name__, template_folder='templates', url_prefix='/api/v1')
storage = SQLRepository()
default_agent = Agent()

@chat_bp.route("/chat/<session_id>", methods=["GET", "POST"])
def chat(session_id):
    if request.method == "GET":
        conv = storage.load(session_id)
        history = []
        if conv:
            history = [{"role": m.role, "content": m.content} for m in conv.messages]
        return render_template("index.html", history=history, session_id=session_id)

    # --- POST request ---
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    user_content = data.get("content")
    
    if not user_content:
        return jsonify({"error": "Content is required"}), 400

    # 1. Load or create the conversation
    conv = storage.load(session_id)
    if not conv:
        conv = Conversation()
    
    # 2. Add user message
    conv.add_message(Message(role="user", content=user_content))

    def generate():
        full_response = ""
        try:
            for chunk in default_agent.generate_stream(conv):
                if chunk:
                    full_response += chunk
                    yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            
            # Save assistant message after the stream is completed
            if full_response.strip():
                conv.add_message(Message(role="assistant", content=full_response))
                storage.save(session_id, conv)
            
            # Signal to end the stream
            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    # This is important - you must return a Response object
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream; charset=utf-8',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # important for nginx
        }
    )
