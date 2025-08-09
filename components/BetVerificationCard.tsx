'use client';

import { BetVerification, VerificationResult } from '@/types/proov';
import { formatCurrency, formatDate } from '@/lib/api';
import { CheckCircle, XCircle, AlertCircle, Shield, Hash, Clock } from 'lucide-react';

interface BetVerificationCardProps {
  verification: BetVerification;
}

export default function BetVerificationCard({ verification }: BetVerificationCardProps) {
  const allStepsPassed = verification.verification_steps.every(step => step.result);

  const getStepIcon = (result: boolean) => {
    return result ? (
      <CheckCircle className="h-5 w-5 text-success-600" />
    ) : (
      <XCircle className="h-5 w-5 text-danger-600" />
    );
  };

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Shield className="h-6 w-6 text-primary-600" />
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Bet Verification</h3>
              <p className="text-sm text-gray-600">
                {verification.bet_data.game_name} - Nonce {verification.bet_data.nonce}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`badge ${allStepsPassed ? 'badge-success' : 'badge-danger'}`}>
              {allStepsPassed ? 'All Checks Passed' : 'Verification Failed'}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {/* Overall Status */}
        <div className={`rounded-lg p-4 ${allStepsPassed ? 'bg-success-50 border border-success-200' : 'bg-danger-50 border border-danger-200'}`}>
          <div className="flex items-center space-x-3">
            {allStepsPassed ? (
              <CheckCircle className="h-6 w-6 text-success-600" />
            ) : (
              <AlertCircle className="h-6 w-6 text-danger-600" />
            )}
            <div>
              <h4 className={`font-medium ${allStepsPassed ? 'text-success-900' : 'text-danger-900'}`}>
                {allStepsPassed ? 'Bet Successfully Verified' : 'Verification Issues Found'}
              </h4>
              <p className={`text-sm ${allStepsPassed ? 'text-success-700' : 'text-danger-700'}`}>
                {verification.verification_steps.filter(s => s.result).length} of {verification.verification_steps.length} checks passed
              </p>
            </div>
          </div>
        </div>

        {/* Verification Steps */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-4">Verification Steps</h4>
          <div className="space-y-3">
            {verification.verification_steps.map((step, index) => (
              <div 
                key={index}
                className={`verification-step ${step.result ? 'success' : 'failed'}`}
              >
                <div className="flex-shrink-0">
                  {getStepIcon(step.result)}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-900">
                      Step {step.step}: {step.description}
                    </span>
                    <span className={`text-sm font-medium ${step.result ? 'text-success-600' : 'text-danger-600'}`}>
                      {step.result ? 'PASS' : 'FAIL'}
                    </span>
                  </div>
                  {step.data && (
                    <div className="mt-2">
                      <details className="text-sm">
                        <summary className="cursor-pointer text-gray-600 hover:text-gray-900">
                          View Details
                        </summary>
                        <pre className="mt-2 text-xs bg-gray-100 p-2 rounded overflow-x-auto">
                          {JSON.stringify(step.data, null, 2)}
                        </pre>
                      </details>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Random Data & Simulation */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3">Randomness & Simulation</h4>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-2">
                <Hash className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium">Random Integer</span>
              </div>
              <div className="font-mono text-sm break-all">
                {(verification.random_data.random_int || 0).toLocaleString()}
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-2">
                <Hash className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium">Random Float</span>
              </div>
              <div className="font-mono text-sm">
                {(verification.random_data.random_float || 0).toFixed(8)}
              </div>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-4">
            <div className="bg-primary-50 rounded-lg p-3">
              <span className="text-sm font-medium text-primary-900">Simulated Payout</span>
              <div className="text-lg font-bold text-primary-700">
                {(verification.random_data.simulated_payout || 0).toLocaleString()}
              </div>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-sm font-medium text-gray-900">Actual Payout</span>
              <div className="text-lg font-bold text-gray-700">
                {(verification.bet_data.raw_win || 0).toLocaleString()}
              </div>
            </div>
          </div>

          {verification.random_data.shard_won && (
            <div className="mt-4 bg-warning-50 rounded-lg p-3">
              <span className="text-sm font-medium text-warning-900">Shard Won</span>
              <div className="text-sm text-warning-700">
                {JSON.stringify(verification.random_data.shard_won)}
              </div>
            </div>
          )}
        </div>

        {/* Settlement Comparison */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3">Settlement Verification</h4>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Settlement Wagered:</span>
                <div className="font-medium">{(verification.settlement.wagered || 0).toLocaleString()}</div>
              </div>
              <div>
                <span className="text-gray-600">Settlement Won:</span>
                <div className="font-medium">{(verification.settlement.won || 0).toLocaleString()}</div>
              </div>
              <div>
                <span className="text-gray-600">Settlement Bets:</span>
                <div className="font-medium">{verification.settlement.bets || 0}</div>
              </div>
              <div>
                <span className="text-gray-600">Transaction ID:</span>
                <div className="font-mono text-xs break-all">{verification.settlement.txid}</div>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t border-gray-200">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Finalized:</span>
                <span className="font-medium">{formatDate(verification.settlement.finalized_at)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Game Distribution Info */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3">Game Distribution</h4>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-600">House Edge:</span>
                <div className="font-medium">{(verification.distribution.edge * 100).toFixed(2)}%</div>
              </div>
              <div>
                <span className="text-gray-600">Max Multiplier:</span>
                <div className="font-medium">{verification.distribution.max_multiplier}x</div>
              </div>
              <div>
                <span className="text-gray-600">Volatility:</span>
                <div className="font-medium">{verification.distribution.volatility_rating}/5</div>
              </div>
              <div>
                <span className="text-gray-600">Frontend Type:</span>
                <div className="font-medium">{verification.distribution.frontend_type}</div>
              </div>
            </div>
          </div>
        </div>

        {/* User Statistics */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3">User Statistics</h4>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div className="text-center">
                <div className="text-lg font-bold text-gray-900">{(verification.user_login.bets || 0).toLocaleString()}</div>
                <div className="text-gray-600">Total Bets</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-gray-900">{formatCurrency(verification.user_login.wagered || 0)}</div>
                <div className="text-gray-600">Total Wagered</div>
              </div>
              <div className="text-center">
                <div className="text-lg font-bold text-gray-900">{formatCurrency(verification.user_login.won || 0)}</div>
                <div className="text-gray-600">Total Won</div>
              </div>
            </div>
          </div>
        </div>

        {/* Verification Timestamp */}
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-500 border-t pt-4">
          <Clock className="h-4 w-4" />
          <span>Verification completed at {formatDate(new Date().toISOString())}</span>
        </div>
      </div>
    </div>
  );
}
