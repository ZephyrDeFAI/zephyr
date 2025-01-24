from flask import Blueprint, request, jsonify
from services.wallet_service import verify_wallet_signature
from services.user_service import create_user, get_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/connect-wallet', methods=['POST'])
def connect_wallet():
    try:
        data = request.get_json()
        wallet_address = data.get('wallet_address')
        signature = data.get('signature')
        
        if not wallet_address or not signature:
            return jsonify({"error": "Missing required parameters"}), 400
            
        # Verify wallet signature
        if not verify_wallet_signature(wallet_address, signature):
            return jsonify({"error": "Invalid signature"}), 401
            
        # Get or create user
        user = get_user(wallet_address)
        if not user:
            user = create_user(wallet_address)
            
        return jsonify({
            "status": "success",
            "user": user
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/user-profile', methods=['GET'])
def get_user_profile():
    try:
        wallet_address = request.args.get('wallet_address')
        if not wallet_address:
            return jsonify({"error": "Wallet address is required"}), 400
            
        user = get_user(wallet_address)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "status": "success",
            "user": user
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
