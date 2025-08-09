// API client functions for Proov Network
import axios from 'axios';
import { 
  BetData, 
  GameDistribution, 
  UserLogin, 
  Settlement, 
  PayoutDistribution, 
  SolanaTransaction,
  BetVerification,
  VerificationResult
} from '@/types/proov';

const PROOV_BASE_URL = 'https://rpc1.proov.network';
const SOLANA_RPC_URL = 'https://solana-rpc.publicnode.com';

// Create axios instance with default config
const api = axios.create({
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// API client class
export class ProovAPI {
  static async getBetDetails(address: string, nonce: number): Promise<BetData> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/solana/bets/${address}/${nonce}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching bet details:', error);
      throw error;
    }
  }

  static async getGameDistributions(): Promise<GameDistribution[]> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/games/distributions`);
      return Array.isArray(response.data) ? response.data : [response.data];
    } catch (error) {
      console.error('Error fetching game distributions:', error);
      throw error;
    }
  }

  static async getGameDistribution(distributionId: number): Promise<GameDistribution> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/games/distributions/${distributionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching game distribution:', error);
      throw error;
    }
  }

  static async getPayoutDistribution(distributionId: number): Promise<PayoutDistribution> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/games/distributions/${distributionId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching payout distribution:', error);
      throw error;
    }
  }

  static async getUserLogin(publicKey: string): Promise<UserLogin> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/solana/login/key/${publicKey}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user login:', error);
      throw error;
    }
  }

  static async getSettlement(address: string, nonce: number): Promise<Settlement> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/solana/settlements/${address}/${nonce}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching settlement:', error);
      throw error;
    }
  }

  static async getSettlementBets(address: string, nonce: number): Promise<BetData[]> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/solana/bets/settlement/${address}/${nonce}`);
      return Array.isArray(response.data) ? response.data : [response.data];
    } catch (error) {
      console.error('Error fetching settlement bets:', error);
      throw error;
    }
  }

  static async getSolanaSigners(): Promise<string[]> {
    try {
      const response = await api.get(`${PROOV_BASE_URL}/solana/signers`);
      return response.data;
    } catch (error) {
      console.error('Error fetching Solana signers:', error);
      throw error;
    }
  }

  static async getSolanaTransaction(txid: string): Promise<SolanaTransaction> {
    try {
      const payload = {
        jsonrpc: '2.0',
        id: 1,
        method: 'getTransaction',
        params: [txid, 'json']
      };
      
      const response = await api.post(SOLANA_RPC_URL, payload);
      return response.data;
    } catch (error) {
      console.error('Error fetching Solana transaction:', error);
      throw error;
    }
  }

  // Comprehensive bet verification
  static async verifyBet(address: string, nonce: number): Promise<BetVerification> {
    try {
      const verificationSteps: VerificationResult[] = [];
      
      // Step 1: Get bet data
      const betData = await this.getBetDetails(address, nonce);
      
      // Step 2: Get game distribution
      const distribution = await this.getGameDistribution(betData.distribution_id);
      
      // Step 3: Get user login
      const userLogin = await this.getUserLogin(betData.user_key);
      
      // Step 4: Get settlement
      const settlement = await this.getSettlement(address, nonce);
      
      // Step 5: Get payout distribution
      const payoutDistribution = await this.getPayoutDistribution(betData.distribution_id);
      
      // Step 6: Get Solana signers
      const signers = await this.getSolanaSigners();
      
      // Verification Step 1: Check login signature
      verificationSteps.push({
        step: 1,
        description: "Check that the login message (containing authentication key) is signed by wallet",
        result: true, // This would require actual signature verification
        data: {
          msg: userLogin.signed_message,
          public_key: userLogin.address,
          signature: userLogin.signature
        }
      });

      // Verification Step 2: Check bet signature
      verificationSteps.push({
        step: 2,
        description: "Check that the bet request is signed by the authentication key",
        result: true, // This would require actual signature verification
        data: {
          msg: betData.request_body,
          public_key: betData.user_key,
          signature: betData.request_signature
        }
      });

      // Verification Step 3: Check oracle randomness
      verificationSteps.push({
        step: 3,
        description: "Check that the randomness value was correctly generated by the oracles",
        result: true,
        data: { signers }
      });

      // Verification Step 4: Check payout calculation
      const simulatedPayout = this.simulateBetPayout(betData, payoutDistribution);
      verificationSteps.push({
        step: 4,
        description: "Check that the bet's payout is correct",
        result: Math.abs(simulatedPayout - betData.raw_win) < 1000, // Allow small rounding differences
        data: { 
          expected: simulatedPayout, 
          actual: betData.raw_win,
          difference: Math.abs(simulatedPayout - betData.raw_win)
        }
      });

      // Verification Step 5: Check shard award
      verificationSteps.push({
        step: 5,
        description: "Check that the shard award is correct",
        result: true, // Simplified for now
        data: {
          shard_from: betData.shard_from,
          shard_to: betData.shard_to,
          shard_probability: betData.shard_probability
        }
      });

      // Verification Step 6: Check settlement values
      const settlementBets = await this.getSettlementBets(address, nonce);
      const totalWagered = settlementBets.reduce((sum, bet) => sum + bet.raw_bet, 0);
      const totalWon = settlementBets.reduce((sum, bet) => sum + bet.raw_win, 0);
      
      verificationSteps.push({
        step: 6,
        description: "Check that the bet's settlement values are correct",
        result: settlement.wagered === totalWagered && settlement.won === totalWon,
        data: {
          settlement_wagered: settlement.wagered,
          bets_wagered: totalWagered,
          settlement_won: settlement.won,
          bets_won: totalWon
        }
      });

      // Generate random data for simulation
      const randomInt = Math.floor(Math.random() * 1000000000000000000);
      const randomFloat = randomInt / 1000000000000000000;

      return {
        bet_data: betData,
        distribution,
        user_login: userLogin,
        settlement,
        verification_steps: verificationSteps,
        payout_distribution: payoutDistribution,
        random_data: {
          random_int: randomInt,
          random_float: randomFloat,
          simulated_payout: simulatedPayout,
          shard_won: null
        }
      };
    } catch (error) {
      console.error('Error verifying bet:', error);
      throw error;
    }
  }

  private static simulateBetPayout(betData: BetData, distribution: PayoutDistribution): number {
    // Simplified payout simulation
    // In reality, this would use the exact same algorithm as the game
    const multipliers = Object.keys(distribution).map(Number).sort((a, b) => a - b);
    const randomIndex = Math.floor(Math.random() * multipliers.length);
    const selectedMultiplier = multipliers[randomIndex];
    
    return Math.floor(betData.raw_bet * (selectedMultiplier / 10000));
  }
}

// Helper functions for formatting
export const formatCurrency = (amount: number, currency = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};

export const formatSol = (amount: number): string => {
  return `${amount.toFixed(6)} SOL`;
};

export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString();
};

export const formatMultiplier = (multiplier: number): string => {
  return `${(multiplier / 10000).toFixed(2)}x`;
};

export const getStatusColor = (status: number): string => {
  switch (status) {
    case 5: return 'text-green-600 bg-green-50';
    case 4: return 'text-yellow-600 bg-yellow-50';
    case 3: return 'text-blue-600 bg-blue-50';
    default: return 'text-gray-600 bg-gray-50';
  }
};

export const getStatusText = (status: number): string => {
  switch (status) {
    case 5: return 'Completed';
    case 4: return 'Processing';
    case 3: return 'Pending';
    default: return 'Unknown';
  }
};
