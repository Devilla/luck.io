#!/usr/bin/env python3
import requests
import json

def test_proov_api():
    PROOV_BASE_URL = 'https://rpc1.proov.network'
    address = "6kRQgeBFq3Qh32rP16cGz9gisfMUM6umFpPZVwkQx8Ez"
    nonce = 43359
    
    print(f"Testing Proov API for address: {address}, nonce: {nonce}")
    print("=" * 60)
    
    # Test bet details
    try:
        bet_url = f"{PROOV_BASE_URL}/solana/bets/{address}/{nonce}"
        print(f"Fetching: {bet_url}")
        bet_resp = requests.get(bet_url, timeout=20)
        print(f"Status: {bet_resp.status_code}")
        
        if bet_resp.status_code == 200:
            bet_data = bet_resp.json()
            print("Bet Data Keys:", list(bet_data.keys()))
            print(f"Game: {bet_data.get('game_name')}")
            print(f"Bet Amount: ${bet_data.get('dollar_bet'):.2f}")
            print(f"Win Amount: ${bet_data.get('dollar_win', 0):.2f}")
            print(f"Win Multiplier: {bet_data.get('dollar_win', 0) / bet_data.get('dollar_bet', 1):.1f}x")
            print(f"User Key: {bet_data.get('user_key')}")
            print(f"Distribution ID: {bet_data.get('distribution_id')}")
            
            # Test user login
            user_key = bet_data.get("user_key")
            if user_key:
                print(f"\nFetching user data for: {user_key}")
                user_url = f"{PROOV_BASE_URL}/solana/login/key/{user_key}"
                user_resp = requests.get(user_url, timeout=20)
                print(f"User API Status: {user_resp.status_code}")
                
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    print("User Data Keys:", list(user_data.keys()))
                    print(f"Total Bets: {user_data.get('bets', 0):,}")
                    print(f"Total Wagered: ${user_data.get('wagered', 0):,.2f}")
                    print(f"Total Won: ${user_data.get('won', 0):,.2f}")
                    rtp = (user_data.get('won', 0) / user_data.get('wagered', 1) * 100) if user_data.get('wagered', 0) > 0 else 0
                    print(f"Overall RTP: {rtp:.2f}%")
                else:
                    print(f"User API Error: {user_resp.text}")
            
            # Test game distribution
            distribution_id = bet_data.get("distribution_id")
            if distribution_id:
                print(f"\nFetching game distribution for ID: {distribution_id}")
                dist_url = f"{PROOV_BASE_URL}/games/distributions/{distribution_id}"
                dist_resp = requests.get(dist_url, timeout=20)
                print(f"Distribution API Status: {dist_resp.status_code}")
                
                if dist_resp.status_code == 200:
                    dist_data = dist_resp.json()
                    print("Distribution Data Keys:", list(dist_data.keys()))
                    print(f"Game Name: {dist_data.get('game_name')}")
                    print(f"Max Multiplier: {dist_data.get('max_multiplier')}x")
                    print(f"House Edge: {dist_data.get('edge', 0) * 100:.2f}%")
                else:
                    print(f"Distribution API Error: {dist_resp.text}")
                    
        else:
            print(f"Bet API Error: {bet_resp.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_proov_api()
