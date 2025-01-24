import requests
import json
from typing import Dict, Any, Optional
import os

class OllamaService:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        
    def deploy_to_ollama(self, model_id: str) -> Dict[str, Any]:
        """
        Deploy a model to Ollama
        """
        try:
            # Load model configuration
            model_config = self._load_model_config(model_id)
            
            # Create Modelfile
            modelfile_content = self._create_modelfile(model_config)
            
            # Save Modelfile
            modelfile_path = f"models/{model_id}/Modelfile"
            os.makedirs(os.path.dirname(modelfile_path), exist_ok=True)
            with open(modelfile_path, 'w') as f:
                f.write(modelfile_content)
            
            # Create model in Ollama
            response = requests.post(
                f"{self.base_url}/api/create",
                json={
                    "name": f"zephyr_{model_id}",
                    "path": modelfile_path
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to create model: {response.text}")
            
            return {
                "status": "success",
                "model_name": f"zephyr_{model_id}",
                "deployment_time": str(datetime.datetime.now())
            }
            
        except Exception as e:
            print(f"Error deploying to Ollama: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _load_model_config(self, model_id: str) -> Dict[str, Any]:
        """
        Load model configuration from storage
        """
        config_path = f"models/{model_id}/config.json"
        if not os.path.exists(config_path):
            raise ValueError(f"Model configuration not found for {model_id}")
            
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _create_modelfile(self, config: Dict[str, Any]) -> str:
        """
        Create Ollama Modelfile content
        """
        modelfile = f"""
FROM {config.get('base_model', 'llama2')}
PARAMETER temperature {config.get('temperature', 0.7)}
PARAMETER top_p {config.get('top_p', 0.9)}
PARAMETER top_k {config.get('top_k', 40)}
        """
        
        # Add custom parameters
        for key, value in config.get('custom_parameters', {}).items():
            modelfile += f"\nPARAMETER {key} {value}"
            
        return modelfile.strip()
    
    def predict(self, model_name: str, input_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make predictions using a deployed model
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": f"zephyr_{model_name}",
                    "prompt": json.dumps(input_data)
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Prediction failed: {response.text}")
                
            return response.json()
            
        except Exception as e:
            print(f"Error making prediction: {str(e)}")
            return None
    
    def list_models(self) -> List[str]:
        """
        List all deployed models
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                raise Exception(f"Failed to list models: {response.text}")
                
            models = response.json()
            return [model['name'] for model in models if model['name'].startswith('zephyr_')]
            
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return []
