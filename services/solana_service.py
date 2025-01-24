from solana.rpc.api import Client
from solana.rpc.types import MemcmpOpts
from typing import List, Dict
import datetime

class SolanaService:
    def __init__(self):
        self.client = Client("https://api.mainnet-beta.solana.com")
        
    def get_defi_data(self, data_type: str, start_time: str, end_time: str) -> List[Dict]:
        """
        Get DeFi-related data from Solana blockchain
        """
        try:
            if data_type == "transactions":
                return self._get_transaction_data(start_time, end_time)
            elif data_type == "liquidity":
                return self._get_liquidity_data(start_time, end_time)
            else:
                raise ValueError(f"Unsupported data type: {data_type}")
        except Exception as e:
            print(f"Error fetching Solana data: {str(e)}")
            return []
            
    def _get_transaction_data(self, start_time: str, end_time: str) -> List[Dict]:
        """
        Get transaction data from specified time range
        """
        start_timestamp = datetime.datetime.fromisoformat(start_time).timestamp()
        end_timestamp = datetime.datetime.fromisoformat(end_time).timestamp()
        
        # Get signatures for address
        # In production, you would want to filter for specific programs
        signatures = self.client.get_signatures_for_address(
            "YOUR_PROGRAM_ID",
            before=str(int(end_timestamp)),
            until=str(int(start_timestamp))
        )
        
        transactions = []
        for sig in signatures.value:
            tx = self.client.get_transaction(sig.signature)
            if tx:
                transactions.append(self._parse_transaction(tx))
                
        return transactions
        
    def _get_liquidity_data(self, start_time: str, end_time: str) -> List[Dict]:
        """
        Get liquidity pool data from specified time range
        """
        # This would typically involve querying specific liquidity pool programs
        # and parsing their state data
        return []
        
    def _parse_transaction(self, transaction: Dict) -> Dict:
        """
        Parse a raw transaction into a structured format
        """
        return {
            "signature": transaction.get("transaction", {}).get("signatures", [])[0],
            "timestamp": transaction.get("block_time"),
            "success": transaction.get("meta", {}).get("err") is None,
            "fee": transaction.get("meta", {}).get("fee", 0),
            # Add more transaction details as needed
        }
        
    def get_token_accounts(self, wallet_address: str) -> List[Dict]:
        """
        Get all token accounts for a wallet
        """
        try:
            accounts = self.client.get_token_accounts_by_owner(
                wallet_address,
                MemcmpOpts(offset=0, bytes="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
            )
            
            return [self._parse_token_account(account) for account in accounts.value]
        except Exception as e:
            print(f"Error fetching token accounts: {str(e)}")
            return []
            
    def _parse_token_account(self, account: Dict) -> Dict:
        """
        Parse a raw token account into a structured format
        """
        data = account.get("account", {}).get("data", {})
        return {
            "mint": data.get("mint"),
            "owner": data.get("owner"),
            "amount": data.get("amount"),
            "delegate": data.get("delegate"),
            "state": data.get("state")
        }
