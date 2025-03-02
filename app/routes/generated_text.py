import os
import openai
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
from models.generated_text import db, GeneratedText

load_dotenv()
db = SQLAlchemy()
text = Blueprint("api/", __name__)

openai.api_key = os.getenv('OPENAI_KEY')

# Generate AI-generated response from OpenAI's API and store it in the database
@jwt_required()
@text.route("/generate-text", methods=["POST"])
def generate_text():
    data = request.get_json()
    prompt = data['prompt']
    user_id = data['user_id']

    try:
        # Call OpenAI API to generate text
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )

        # Save generated text
        generated_text = GeneratedText(
            user_id=user_id,
            prompt=prompt,
            response=response.choices[0].text)
    except Exception as e:
        return jsonify({"message": f"OpenAI API error: {str(e)}"}), 500

    db.session.add(generated_text)
    db.session.commit()

    return jsonify({"message": "Text generated and saved", "response": response.choices[0].text}), 201


# Retrieve stored generated text to its owner (user that created it)
@jwt_required()
@text.route("/generated-text/<int:id>", methods=["GET"])
def get_generated_text(id):
    generated_text = GeneratedText.query.get_or_404(id)

    # Check if the user trying to access is the owner
    user_id = get_jwt_identity()
    if str(generated_text.user_id) != user_id:
        return jsonify({"message": "Permission denied"}), 403

    return jsonify({
        "id": generated_text.id,
        "prompt": generated_text.prompt,
        "response": generated_text.response,
        "timestamp": generated_text.timestamp
    }), 200


# Update stored generated text by the id
@jwt_required()
@text.route("/generated-text/<int:id>", methods=["PUT"])
def update_generated_text(id):
    data = request.get_json()
    new_prompt = data['prompt']
    new_response = data['response']

    generated_text = GeneratedText.query.get_or_404(id)

    # Check if the user trying to update is the owner
    user_id = get_jwt_identity()
    if str(generated_text.user_id) != user_id:
        return jsonify({"message": "Permission denied"}), 403

    # If incoming data exist update generated text
    if new_prompt:
        generated_text.prompt = new_prompt
    if new_response:
        generated_text.response = new_response
    generate_text.timestamp = db.func.current_timestamp()

    db.session.commit()
    return jsonify({"message": "Text updated successfully"}), 200


# Delete stored generated text by the id
@jwt_required()
@text.route("/generated-text/<int:id>", methods=["DELETE"])
def delete_generated_text(id):
    generated_text = GeneratedText.query.get_or_404(id)

    # Check if the user trying to update is the owner
    user_id = get_jwt_identity()
    if str(generated_text.user_id) != user_id:
        return jsonify({"message": "Permission denied"}), 403
    
    db.session.delete(generated_text)
    db.session.commit()
    return jsonify({"message": "Text deleted successfully"}), 200
