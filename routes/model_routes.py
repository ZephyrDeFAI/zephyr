from flask import Blueprint, request, jsonify
from services.model_service import train_model, deploy_model, evaluate_model
from services.ollama_service import deploy_to_ollama

bp = Blueprint('model', __name__, url_prefix='/model')

@bp.route('/train', methods=['POST'])
def train():
    try:
        data = request.get_json()
        dataset_id = data.get('dataset_id')
        model_params = data.get('model_params', {})
        user_id = data.get('user_id')
        
        if not all([dataset_id, user_id]):
            return jsonify({"error": "Missing required parameters"}), 400
            
        training_job = train_model(dataset_id, model_params, user_id)
        
        return jsonify({
            "status": "success",
            "job_id": training_job.id
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/deploy', methods=['POST'])
def deploy():
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        deployment_type = data.get('deployment_type', 'ollama')
        
        if not model_id:
            return jsonify({"error": "Model ID is required"}), 400
            
        if deployment_type == 'ollama':
            deployment = deploy_to_ollama(model_id)
        else:
            deployment = deploy_model(model_id, deployment_type)
            
        return jsonify({
            "status": "success",
            "deployment": deployment
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        data = request.get_json()
        model_id = data.get('model_id')
        test_data = data.get('test_data')
        
        if not all([model_id, test_data]):
            return jsonify({"error": "Missing required parameters"}), 400
            
        evaluation = evaluate_model(model_id, test_data)
        
        return jsonify({
            "status": "success",
            "evaluation": evaluation
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
