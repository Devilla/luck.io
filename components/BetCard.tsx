'use client';

import { BetData } from '@/types/proov';
import { formatCurrency, formatSol, formatDate, getStatusColor, getStatusText } from '@/lib/api';
import { Calendar, DollarSign, TrendingUp, Hash } from 'lucide-react';

interface BetCardProps {
  bet: BetData;
}

export default function BetCard({ bet }: BetCardProps) {
  const profitLoss = bet.dollar_win - bet.dollar_bet;
  const isWin = profitLoss > 0;
  const multiplier = bet.dollar_win / bet.dollar_bet;

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">{bet.game_name}</h3>
          <span className={`badge ${getStatusColor(bet.status)}`}>
            {getStatusText(bet.status)}
          </span>
        </div>
        <div className="flex items-center space-x-2 mt-2">
          <Hash className="h-4 w-4 text-gray-400" />
          <span className="text-sm text-gray-600">Nonce: {bet.nonce}</span>
        </div>
      </div>

      <div className="space-y-4">
        {/* Bet Amount & Winnings */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-1">
              <DollarSign className="h-4 w-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Bet Amount</span>
            </div>
            <div className="text-lg font-bold text-gray-900">
              {formatCurrency(bet.dollar_bet)}
            </div>
            <div className="text-sm text-gray-500">
              {formatSol(bet.bet)} {bet.currency}
            </div>
          </div>

          <div className={`rounded-lg p-4 ${isWin ? 'bg-success-50' : 'bg-danger-50'}`}>
            <div className="flex items-center space-x-2 mb-1">
              <TrendingUp className="h-4 w-4 text-gray-400" />
              <span className="text-sm font-medium text-gray-600">Winnings</span>
            </div>
            <div className={`text-lg font-bold ${isWin ? 'text-success-700' : 'text-danger-700'}`}>
              {formatCurrency(bet.dollar_win)}
            </div>
            <div className="text-sm text-gray-500">
              {formatSol(bet.win)} {bet.currency}
            </div>
          </div>
        </div>

        {/* Profit/Loss & Multiplier */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-sm font-medium text-gray-600">Profit/Loss</span>
            <div className={`text-lg font-bold ${isWin ? 'text-success-600' : 'text-danger-600'}`}>
              {isWin ? '+' : ''}{formatCurrency(profitLoss)}
            </div>
          </div>
          <div>
            <span className="text-sm font-medium text-gray-600">Multiplier</span>
            <div className="text-lg font-bold text-gray-900">
              {multiplier.toFixed(2)}x
            </div>
          </div>
        </div>

        {/* Game Details */}
        <div className="border-t pt-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Distribution ID:</span>
              <div className="font-medium">{bet.distribution_id}</div>
            </div>
            <div>
              <span className="text-gray-600">Owner Rank:</span>
              <div className="font-medium">#{bet.owner_rank}</div>
            </div>
            <div>
              <span className="text-gray-600">Exchange Rate:</span>
              <div className="font-medium">{bet.exchange_rate.toFixed(2)}</div>
            </div>
            <div>
              <span className="text-gray-600">Settlement:</span>
              <div className="font-medium">{bet.settlement}</div>
            </div>
          </div>
        </div>

        {/* Shard Information */}
        {bet.shard_probability > 0 && (
          <div className="bg-primary-50 rounded-lg p-3">
            <h4 className="text-sm font-medium text-primary-900 mb-2">Shard Information</h4>
            <div className="grid grid-cols-3 gap-2 text-sm">
              <div>
                <span className="text-primary-600">Range:</span>
                <div className="font-medium">{bet.shard_from} - {bet.shard_to}</div>
              </div>
              <div>
                <span className="text-primary-600">Rate:</span>
                <div className="font-medium">{(bet.shard_rate * 100).toFixed(1)}%</div>
              </div>
              <div>
                <span className="text-primary-600">Probability:</span>
                <div className="font-medium">{(bet.shard_probability * 100).toFixed(2)}%</div>
              </div>
            </div>
          </div>
        )}

        {/* Timestamps */}
        <div className="border-t pt-4">
          <div className="space-y-2 text-sm">
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-gray-400" />
              <span className="text-gray-600">Created:</span>
              <span className="font-medium">{formatDate(bet.created_at)}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Calendar className="h-4 w-4 text-gray-400" />
              <span className="text-gray-600">Revealed:</span>
              <span className="font-medium">{formatDate(bet.revealed_at)}</span>
            </div>
          </div>
        </div>

        {/* Addresses */}
        <div className="bg-gray-50 rounded-lg p-3">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Addresses</h4>
          <div className="space-y-2 text-xs">
            <div>
              <span className="text-gray-600">Bet Address:</span>
              <div className="font-mono break-all">{bet.address}</div>
            </div>
            <div>
              <span className="text-gray-600">Owner Address:</span>
              <div className="font-mono break-all">{bet.owner_address}</div>
            </div>
            <div>
              <span className="text-gray-600">User Key:</span>
              <div className="font-mono break-all">{bet.user_key}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
