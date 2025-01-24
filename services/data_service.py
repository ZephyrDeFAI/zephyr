import ipfshttpclient
import pandas as pd
from typing import Dict, List, Any
import json
import os

# Initialize IPFS client
def get_ipfs_client():
    try:
        return ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    except Exception as e:
        print(f"Error connecting to IPFS: {str(e)}")
        return None

def upload_to_ipfs(file) -> str:
    """
    Upload a file to IPFS
    """
    client = get_ipfs_client()
    if not client:
        raise Exception("Failed to connect to IPFS")
    
    try:
        result = client.add(file)
        return result['Hash']
    finally:
        client.close()

def get_from_ipfs(ipfs_hash: str) -> bytes:
    """
    Get a file from IPFS
    """
    client = get_ipfs_client()
    if not client:
        raise Exception("Failed to connect to IPFS")
    
    try:
        return client.cat(ipfs_hash)
    finally:
        client.close()

def process_onchain_data(raw_data: List[Dict]) -> List[Dict]:
    """
    Process raw blockchain data into a format suitable for model training
    """
    processed_data = []
    
    for item in raw_data:
        processed_item = {
            "timestamp": item.get("timestamp"),
            "transaction_type": item.get("type"),
            "amount": float(item.get("amount", 0)),
            "fee": float(item.get("fee", 0)),
            "success": bool(item.get("success", True))
        }
        
        # Add additional features based on transaction type
        if processed_item["transaction_type"] == "swap":
            processed_item.update({
                "token_in": item.get("token_in"),
                "token_out": item.get("token_out"),
                "price_impact": float(item.get("price_impact", 0))
            })
        elif processed_item["transaction_type"] == "liquidity":
            processed_item.update({
                "pool_address": item.get("pool_address"),
                "token_amount": float(item.get("token_amount", 0))
            })
            
        processed_data.append(processed_item)
    
    return processed_data

def save_dataset(data: List[Dict], user_id: str) -> str:
    """
    Save a dataset to local storage and return its ID
    """
    dataset_id = str(uuid.uuid4())
    dataset_dir = f"data/datasets/{user_id}"
    os.makedirs(dataset_dir, exist_ok=True)
    
    with open(f"{dataset_dir}/{dataset_id}.json", 'w') as f:
        json.dump(data, f, indent=2)
    
    return dataset_id

def load_dataset(dataset_id: str, user_id: str) -> List[Dict]:
    """
    Load a dataset from local storage
    """
    dataset_path = f"data/datasets/{user_id}/{dataset_id}.json"
    
    if not os.path.exists(dataset_path):
        raise ValueError(f"Dataset {dataset_id} not found")
    
    with open(dataset_path, 'r') as f:
        return json.load(f)

def convert_to_dataframe(data: List[Dict]) -> pd.DataFrame:
    """
    Convert a list of dictionaries to a pandas DataFrame
    """
    return pd.DataFrame(data)
