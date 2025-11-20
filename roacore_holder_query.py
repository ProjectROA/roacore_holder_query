# token_stats_top5.py
from solana.rpc.api import Client
from solana.publickey import PublicKey
import json

ROACORE_TOKEN_MINT = "5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7"
SOLANA_RPC = "https://api.mainnet-beta.solana.com"


def get_top_holders(token_mint, top_n=5):
    client = Client(SOLANA_RPC)
    mint_pubkey = PublicKey(token_mint)

    # Get decimals
    supply = client.get_token_supply(mint_pubkey)
    decimals = supply['result']['value']['decimals']

    # Get all accounts
    TOKEN_PROGRAM_ID = PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
    accounts = client.get_program_accounts(
        TOKEN_PROGRAM_ID,
        encoding="jsonParsed",
        filters=[
            {"dataSize": 165},
            {"memcmp": {"offset": 0, "bytes": str(mint_pubkey)}}
        ]
    )

    # Extract balances
    holders = []
    for acc in accounts['result']:
        info = acc['account']['data']['parsed']['info']
        balance = int(info['tokenAmount']['amount'])
        if balance > 0:
            holders.append({
                'address': info['owner'],
                'balance': balance / (10 ** decimals)
            })

    # Sort and get top N
    holders.sort(key=lambda x: x['balance'], reverse=True)

    return holders[:top_n]


if __name__ == "__main__":
    top5 = get_top_holders(ROACORE_TOKEN_MINT, 5)
    print(json.dumps(top5, indent=2))