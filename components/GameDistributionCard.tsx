'use client';

import { GameDistribution } from '@/types/proov';
import { formatCurrency } from '@/lib/api';
import { Gamepad2, TrendingUp, Star, Settings } from 'lucide-react';

interface GameDistributionCardProps {
  distribution: GameDistribution;
}

export default function GameDistributionCard({ distribution }: GameDistributionCardProps) {
  const getVolatilityColor = (rating: number) => {
    if (rating <= 2) return 'text-success-600 bg-success-100';
    if (rating <= 3) return 'text-warning-600 bg-warning-100';
    return 'text-danger-600 bg-danger-100';
  };

  const getVolatilityText = (rating: number) => {
    if (rating <= 2) return 'Low';
    if (rating <= 3) return 'Medium';
    return 'High';
  };

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Gamepad2 className="h-6 w-6 text-primary-600" />
            <div>
              <h3 className="text-lg font-semibold text-gray-900">{distribution.title}</h3>
              <p className="text-sm text-gray-600">{distribution.game_name}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`badge ${distribution.active ? 'badge-success' : 'badge-danger'}`}>
              {distribution.active ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {/* Key Metrics */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-primary-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-1">
              <TrendingUp className="h-4 w-4 text-primary-600" />
              <span className="text-sm font-medium text-primary-900">House Edge</span>
            </div>
            <div className="text-2xl font-bold text-primary-700">
              {(distribution.edge * 100).toFixed(2)}%
            </div>
          </div>

          <div className="bg-warning-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-1">
              <Star className="h-4 w-4 text-warning-600" />
              <span className="text-sm font-medium text-warning-900">Max Multiplier</span>
            </div>
            <div className="text-2xl font-bold text-warning-700">
              {distribution.max_multiplier?.toLocaleString()}x
            </div>
          </div>
        </div>

        {/* Betting Limits */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3">Betting Limits</h4>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-xs text-gray-600 mb-1">Min Bet</div>
              <div className="font-semibold text-gray-900">
                {formatCurrency(distribution.min_dollar_bet)}
              </div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-xs text-gray-600 mb-1">Max Bet</div>
              <div className="font-semibold text-gray-900">
                {formatCurrency(distribution.max_dollar_bet)}
              </div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-xs text-gray-600 mb-1">Max Gain</div>
              <div className="font-semibold text-gray-900">
                {formatCurrency(distribution.max_dollar_gain)}
              </div>
            </div>
          </div>
        </div>

        {/* Game Properties */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3">Game Properties</h4>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <span className="text-sm text-gray-600">Frontend Type:</span>
              <div className="font-medium capitalize">{distribution.frontend_type}</div>
            </div>
            <div>
              <span className="text-sm text-gray-600">Bet Type:</span>
              <div className="font-medium capitalize">{distribution.bet_type}</div>
            </div>
            <div>
              <span className="text-sm text-gray-600">Bet Multiplier:</span>
              <div className="font-medium">{distribution.bet_multiplier}x</div>
            </div>
            <div>
              <span className="text-sm text-gray-600">Distribution ID:</span>
              <div className="font-medium">{distribution.distribution_id}</div>
            </div>
          </div>
        </div>

        {/* Volatility Rating */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Settings className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-900">Volatility Rating</span>
            </div>
            <span className={`badge ${getVolatilityColor(distribution.volatility_rating)}`}>
              {getVolatilityText(distribution.volatility_rating)} ({distribution.volatility_rating}/5)
            </span>
          </div>
          <div className="mt-2">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`h-2 rounded-full ${
                  distribution.volatility_rating <= 2 ? 'bg-success-500' : 
                  distribution.volatility_rating <= 3 ? 'bg-warning-500' : 'bg-danger-500'
                }`}
                style={{ width: `${(distribution.volatility_rating / 5) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Configuration */}
        {distribution.config && (
          <div className="border-t pt-4">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Configuration</h4>
            <pre className="text-xs bg-gray-100 p-3 rounded-md overflow-x-auto">
              {JSON.stringify(distribution.config, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
