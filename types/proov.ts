// TypeScript interfaces for Proov Network API responses

export interface BetData {
  address: string;
  bet: number;
  bet_params: string | null;
  bet_type: string;
  created_at: string;
  currency: string;
  distribution_id: number;
  dollar_bet: number;
  dollar_win: number;
  exchange_rate: number;
  game_name: string;
  nonce: number;
  owner_address: string;
  owner_rank: number;
  proof: string;
  raw_bet: number;
  raw_win: number;
  request_body: string;
  request_signature: string;
  revealed_at: string;
  settlement: number;
  shard_from: number;
  shard_probability: number;
  shard_rate: number;
  shard_to: number;
  status: number;
  user_key: string;
  win: number;
}

export interface GameDistribution {
  distribution_id: number;
  game_name: string;
  title: string;
  bet_type: string;
  active: boolean;
  edge: number;
  max_multiplier: number;
  min_dollar_bet: number;
  max_dollar_bet: number;
  max_dollar_gain: number;
  frontend_type: string;
  bet_multiplier: number;
  config: Record<string, any> | null;
  volatility_rating: number;
}

export interface UserLogin {
  public_key: string;
  address: string;
  signed_message: string;
  signature: string;
  created_at: string;
  expires_at: string;
  deactivated_at: string | null;
  bets: number;
  wagered: number;
  won: number;
  max_bets: number;
  max_wagers: number;
  max_loss: number;
  min_bet_size: number;
  max_bet_size: number;
  distribution_id: number;
  game: string;
  withdrawals: boolean;
}

export interface Settlement {
  address: string;
  nonce: number;
  bets: number;
  wagered: number;
  won: number;
  txid: string;
  finalized_at: string;
}

export interface SignatureVerification {
  msg: string;
  public_key: string;
  signature: string;
}

export interface PayoutDistribution {
  [multiplier: string]: number;
}

export interface VerificationResult {
  step: number;
  description: string;
  result: boolean;
  data?: any;
}

export interface BetVerification {
  bet_data: BetData;
  distribution: GameDistribution;
  user_login: UserLogin;
  settlement: Settlement;
  verification_steps: VerificationResult[];
  payout_distribution: PayoutDistribution;
  random_data: {
    random_int: number;
    random_float: number;
    simulated_payout: number;
    shard_won: any;
  };
}

export interface SolanaTransaction {
  jsonrpc: string;
  result: any;
  id: number;
}

export interface ApiError {
  message: string;
  code?: number;
  details?: any;
}
