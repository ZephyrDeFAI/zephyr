from flask import Blueprint, request, jsonify
from services.data_service import process_onchain_data, upload_to_ipfs
from services.solana_service import get_defi_data

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/upload', methods=['POST'])
def upload_data():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
            
        file = request.files['file']
        user_id = request.form.get('user_id')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        # Upload file to IPFS
        ipfs_hash = upload_to_ipfs(file)
        
        return jsonify({
            "status": "success",
            "ipfs_hash": ipfs_hash
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/onchain-data', methods=['GET'])
def get_onchain_data():
    try:
        data_type = request.args.get('type', 'transactions')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        # Get data from Solana blockchain
        raw_data = get_defi_data(data_type, start_time, end_time)
        
        # Process the raw data
        processed_data = process_onchain_data(raw_data)
        
        return jsonify({
            "status": "success",
            "data": processed_data
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
