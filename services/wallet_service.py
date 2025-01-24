from solana.rpc.api import Client
from solana.publickey import PublicKey
import base58
import nacl.signing

def verify_wallet_signature(wallet_address: str, signature: bytes) -> bool:
    """
    Verify a wallet signature against the provided wallet address
    """
    try:
        # Convert wallet address to PublicKey
        public_key = PublicKey(wallet_address)
        
        # Verify the signature
        verifier = nacl.signing.VerifyKey(bytes(public_key))
        verifier.verify(signature)
        
        return True
    except Exception as e:
        print(f"Error verifying signature: {str(e)}")
        return False

def get_wallet_balance(wallet_address: str) -> float:
    """
    Get the SOL balance for a wallet address
    """
    try:
        client = Client("https://api.mainnet-beta.solana.com")
        public_key = PublicKey(wallet_address)
        balance = client.get_balance(public_key)
        return balance.value / 1e9  # Convert lamports to SOL
    except Exception as e:
        print(f"Error getting wallet balance: {str(e)}")
        return 0.0
