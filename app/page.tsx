'use client';

import { useState, useEffect } from 'react';
import { BetData, GameDistribution, UserLogin, BetVerification } from '@/types/proov';
import { ProovAPI } from '@/lib/api';
import BetCard from '@/components/BetCard';
import GameDistributionCard from '@/components/GameDistributionCard';
import UserLoginCard from '@/components/UserLoginCard';
import BetVerificationCard from '@/components/BetVerificationCard';
import { Search, Loader2, AlertCircle, BarChart3, Shield, Users, Gamepad2 } from 'lucide-react';

export default function HomePage() {
  // State management
  const [activeTab, setActiveTab] = useState<'search' | 'verification' | 'distributions' | 'analytics'>('search');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Search states
  const [betAddress, setBetAddress] = useState('6kRQgeBFq3Qh32rP16cGz9gisfMUM6umFpPZVwkQx8Ez');
  const [betNonce, setBetNonce] = useState('43359');
  
  // Data states
  const [betData, setBetData] = useState<BetData | null>(null);
  const [gameDistribution, setGameDistribution] = useState<GameDistribution | null>(null);
  const [userLogin, setUserLogin] = useState<UserLogin | null>(null);
  const [betVerification, setBetVerification] = useState<BetVerification | null>(null);
  const [gameDistributions, setGameDistributions] = useState<GameDistribution[]>([]);

  // Load sample data on component mount
  useEffect(() => {
    loadSampleData();
    loadGameDistributions();
  }, []);

  const loadSampleData = async () => {
    if (!betAddress || !betNonce) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // Load bet data
      const bet = await ProovAPI.getBetDetails(betAddress, parseInt(betNonce));
      setBetData(bet);
      
      // Load game distribution
      const distribution = await ProovAPI.getGameDistribution(bet.distribution_id);
      setGameDistribution(distribution);
      
      // Load user login
      const user = await ProovAPI.getUserLogin(bet.user_key);
      setUserLogin(user);
      
    } catch (err) {
      console.error('Error loading data:', err);
      setError('Failed to load data. This might be due to CORS restrictions when calling external APIs.');
      
      // Load sample data for demonstration
      loadDemoData();
    } finally {
      setLoading(false);
    }
  };

  const loadDemoData = () => {
    // Sample data based on the provided API responses
    const sampleBet: BetData = {
      address: "6kRQgeBFq3Qh32rP16cGz9gisfMUM6umFpPZVwkQx8Ez",
      bet: 5.848503619000001,
      bet_params: null,
      bet_type: "main",
      created_at: "2025-08-01T00:40:57.230591Z",
      currency: "wSOL",
      distribution_id: 20080,
      dollar_bet: 1000.0000000000001,
      dollar_win: 1661000,
      exchange_rate: 170.98390719028453,
      game_name: "MadameFortune",
      nonce: 43359,
      owner_address: "5or7BFp7S5wf1DLizS2ieQGxArjXmk5DdCGAPoVJJqsK",
      owner_rank: 10,
      proof: "fAcNJffU13JzKFJyShKV5xaWhuEXgjWZeytstdGmmo9wP2c3Ca6DpP1Bu5pC8np8QZ8SsLTHiKMZp6rmLysZ7bTsrU3JHFxgrwpeqShhX3gUsQzD6D2kGYfQ7GnMMx6i2EQsbGvCiZL2uxKiAcwQM8wwPB1ckn6vaQmqXva14mWg7HYLC2Ki62mRjH3vo8keiZrtwEbDfxYi1LXRFZvsnL7jFhRVTUBwVAnfTAww5EUx8G72iCvbF3Ft9o6JJ6Nnpx2VMd7gd2CZgakJtDPiqCNLygiw6kdpys9XzsxwgmPFWz9J61LRN69eboreoFUbMdrmd1gANeU8PuNjucJEnzZTUKpTjpknFZNkn7waKrs6ZTQQq8F8kyaSWk6NoPez4AXQE2EDkm6DAntx8NxUn4m4HpLvTUUdZbCpg3a8WwReKDtVjmqa9",
      raw_bet: 5848503619,
      raw_win: 9714364511159,
      request_body: "5EUbFcasB2bSEmDkbHH5rxvRPX7NG9ZJuG3pDZRJy9ErzGwFKNfz1Lyxc6Uvg2YQcvUh6PprNDfae7jVab9DDayQWBbscuWfLA43CFMGEiBwPm49RqvA7hfvpwA2UfsPgd2CfGZjAiKEwhbgcASmLT5NgUC4khH4CUcDUnZiBo3Ss7sJG4",
      request_signature: "2U3HXJiFXgqzSSbRTMWedrv1NGKydjytpBBfByWPpXrTTLp5NBtwsfuDxmsVoUpqYs6Rz31c1RAnWCUZp3bJ8ZPsHsPVQVa69ohwpZriE66gzYDB8EpKe6gfHTym3QC1kKWiJhQwptWTwL",
      revealed_at: "2025-08-01T00:43:24Z",
      settlement: 43359,
      shard_from: 42,
      shard_probability: 0.024506556316855423,
      shard_rate: 0.3,
      shard_to: 92,
      status: 5,
      user_key: "PWK3R19q1Qfao1TzHT6SA1QnnfZ1bnZBE2AEmG3rvay",
      win: 9714.364511159001
    };

    const sampleDistribution: GameDistribution = {
      distribution_id: 20080,
      game_name: "MadameFortune",
      title: "Madame Fortune",
      bet_type: "main",
      active: true,
      edge: 0.03800310862116518,
      max_multiplier: 5000,
      min_dollar_bet: 0.1,
      max_dollar_bet: 1000,
      max_dollar_gain: 10000000,
      frontend_type: "eslot",
      bet_multiplier: 20,
      config: null,
      volatility_rating: 3
    };

    const sampleUser: UserLogin = {
      public_key: "PWK3R19q1Qfao1TzHT6SA1QnnfZ1bnZBE2AEmG3rvay",
      address: "5or7BFp7S5wf1DLizS2ieQGxArjXmk5DdCGAPoVJJqsK",
      signed_message: "You are approving public key PWK3R19q1Qfao1TzHT6SA1QnnfZ1bnZBE2AEmG3rvay to login and sign bets until 2025-08-02 10:52:47\nAllowed to initiate withdrawals back to the initial wallet\n",
      signature: "nY9jILygUEIDRsIGWOzHoj7m/m/2MPupeE2/dg5+e3Q+ykzg8wHxGU+5n8f4y3Pirx7Jcdjp8Pjh9NOKQqoQDA==",
      created_at: "2025-07-26T10:52:47.754798Z",
      expires_at: "2025-08-02T10:52:47.754793Z",
      deactivated_at: "2025-08-01T00:44:59.158157Z",
      bets: 4435,
      wagered: 2817342.2,
      won: 4546619.399474312,
      max_bets: 0,
      max_wagers: 0,
      max_loss: 0,
      min_bet_size: 0,
      max_bet_size: 0,
      distribution_id: 0,
      game: "",
      withdrawals: true
    };

    setBetData(sampleBet);
    setGameDistribution(sampleDistribution);
    setUserLogin(sampleUser);
  };

  const loadGameDistributions = async () => {
    try {
      const distributions = await ProovAPI.getGameDistributions();
      setGameDistributions(distributions);
    } catch (err) {
      console.error('Error loading distributions:', err);
      // Load sample distributions
      setGameDistributions([
        {
          distribution_id: 20080,
          game_name: "MadameFortune",
          title: "Madame Fortune",
          bet_type: "main",
          active: true,
          edge: 0.03800310862116518,
          max_multiplier: 5000,
          min_dollar_bet: 0.1,
          max_dollar_bet: 1000,
          max_dollar_gain: 10000000,
          frontend_type: "eslot",
          bet_multiplier: 20,
          config: null,
          volatility_rating: 3
        }
      ]);
    }
  };

  const handleVerifyBet = async () => {
    if (!betAddress || !betNonce) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const verification = await ProovAPI.verifyBet(betAddress, parseInt(betNonce));
      setBetVerification(verification);
      setActiveTab('verification');
    } catch (err) {
      console.error('Error verifying bet:', err);
      setError('Failed to verify bet. This might be due to CORS restrictions when calling external APIs.');
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'search', label: 'Bet Search', icon: Search },
    { id: 'verification', label: 'Verification', icon: Shield },
    { id: 'distributions', label: 'Games', icon: Gamepad2 },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">L</span>
                </div>
                <h1 className="text-xl font-bold text-gray-900">Lucky.io</h1>
              </div>
              <span className="text-sm text-gray-500">Proov Network Analytics</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Real-time Gaming Analytics & Verification
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-warning-50 border border-warning-200 rounded-md p-4">
            <div className="flex">
              <AlertCircle className="h-5 w-5 text-warning-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-warning-800">Notice</h3>
                <div className="mt-2 text-sm text-warning-700">
                  <p>{error}</p>
                  <p className="mt-1">Demo data is being displayed instead.</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Search Tab */}
        {activeTab === 'search' && (
          <div className="space-y-8">
            {/* Search Form */}
            <div className="card">
              <div className="card-header">
                <h2 className="text-lg font-semibold text-gray-900">Search Bet Details</h2>
              </div>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="address" className="block text-sm font-medium text-gray-700 mb-1">
                      Bet Address
                    </label>
                    <input
                      type="text"
                      id="address"
                      value={betAddress}
                      onChange={(e) => setBetAddress(e.target.value)}
                      className="input"
                      placeholder="Enter bet address"
                    />
                  </div>
                  <div>
                    <label htmlFor="nonce" className="block text-sm font-medium text-gray-700 mb-1">
                      Nonce
                    </label>
                    <input
                      type="text"
                      id="nonce"
                      value={betNonce}
                      onChange={(e) => setBetNonce(e.target.value)}
                      className="input"
                      placeholder="Enter nonce"
                    />
                  </div>
                </div>
                <div className="flex space-x-3">
                  <button
                    onClick={loadSampleData}
                    disabled={loading}
                    className="btn btn-primary"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        Loading...
                      </>
                    ) : (
                      <>
                        <Search className="h-4 w-4 mr-2" />
                        Search Bet
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleVerifyBet}
                    disabled={loading || !betData}
                    className="btn btn-secondary"
                  >
                    <Shield className="h-4 w-4 mr-2" />
                    Verify Bet
                  </button>
                </div>
              </div>
            </div>

            {/* Results */}
            {(betData || gameDistribution || userLogin) && (
              <div className="grid-responsive">
                {betData && <BetCard bet={betData} />}
                {gameDistribution && <GameDistributionCard distribution={gameDistribution} />}
                {userLogin && <UserLoginCard userLogin={userLogin} />}
              </div>
            )}
          </div>
        )}

        {/* Verification Tab */}
        {activeTab === 'verification' && (
          <div className="space-y-6">
            {betVerification ? (
              <BetVerificationCard verification={betVerification} />
            ) : (
              <div className="text-center py-12">
                <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Verification Data</h3>
                <p className="text-gray-600">
                  Search for a bet and click "Verify Bet" to see verification results.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Distributions Tab */}
        {activeTab === 'distributions' && (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-gray-900">Game Distributions</h2>
              <span className="text-sm text-gray-600">
                {gameDistributions.length} games available
              </span>
            </div>
            <div className="grid-responsive">
              {gameDistributions.map((distribution) => (
                <GameDistributionCard 
                  key={distribution.distribution_id} 
                  distribution={distribution} 
                />
              ))}
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Sample Analytics Cards */}
              <div className="card">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-600">$1,661,000</div>
                  <div className="text-sm text-gray-600">Total Winnings</div>
                </div>
              </div>
              <div className="card">
                <div className="text-center">
                  <div className="text-3xl font-bold text-success-600">1,661x</div>
                  <div className="text-sm text-gray-600">Max Multiplier</div>
                </div>
              </div>
              <div className="card">
                <div className="text-center">
                  <div className="text-3xl font-bold text-warning-600">3.8%</div>
                  <div className="text-sm text-gray-600">House Edge</div>
                </div>
              </div>
            </div>
            <div className="card">
              <div className="text-center py-12">
                <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Analytics Coming Soon</h3>
                <p className="text-gray-600">
                  Advanced analytics and visualization features will be available here.
                </p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
