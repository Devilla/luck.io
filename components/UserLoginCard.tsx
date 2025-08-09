'use client';

import { UserLogin } from '@/types/proov';
import { formatCurrency, formatDate } from '@/lib/api';
import { User, Key, TrendingUp, Shield, Calendar, LogOut } from 'lucide-react';

interface UserLoginCardProps {
  userLogin: UserLogin;
}

export default function UserLoginCard({ userLogin }: UserLoginCardProps) {
  const profitLoss = (userLogin.won || 0) - (userLogin.wagered || 0);
  const isProfit = profitLoss > 0;
  const isActive = !userLogin.deactivated_at && new Date(userLogin.expires_at) > new Date();

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <User className="h-6 w-6 text-primary-600" />
            <div>
              <h3 className="text-lg font-semibold text-gray-900">User Profile</h3>
              <p className="text-sm text-gray-600 font-mono">{userLogin.public_key.slice(0, 8)}...</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`badge ${isActive ? 'badge-success' : 'badge-danger'}`}>
              {isActive ? 'Active' : 'Inactive'}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {/* Key Statistics */}
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-primary-50 rounded-lg">
            <div className="text-xs font-bold text-primary-700">{(userLogin.bets || 0).toLocaleString()}</div>
            <div className="text-sm text-primary-600">Total Bets</div>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <div className="text-xs font-bold text-gray-700">
              {formatCurrency(userLogin.wagered || 0)}
            </div>
            <div className="text-sm text-gray-600">Total Wagered</div>
          </div>
          <div className={`text-center p-4 rounded-lg ${isProfit ? 'bg-success-50' : 'bg-danger-50'}`}>
            <div className={`text-xs font-bold ${isProfit ? 'text-success-700' : 'text-danger-700'}`}>
              {formatCurrency(userLogin.won || 0)}
            </div>
            <div className={`text-sm ${isProfit ? 'text-success-600' : 'text-danger-600'}`}>
              Total Won
            </div>
          </div>
        </div>

        {/* Profit/Loss */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-gray-600" />
              <span className="font-medium text-gray-900">Net Profit/Loss</span>
            </div>
            <div className={`text-xl font-bold ${isProfit ? 'text-success-600' : 'text-danger-600'}`}>
              {isProfit ? '+' : ''}{formatCurrency(profitLoss)}
            </div>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            Return on Investment: {(userLogin.wagered || 0) > 0 ? (((userLogin.won || 0) / (userLogin.wagered || 0)) * 100).toFixed(2) : '0.00'}%
          </div>
        </div>

        {/* Betting Limits & Restrictions */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <Shield className="h-4 w-4" />
            <span>Betting Limits</span>
          </h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Max Bets:</span>
              <div className="font-medium">{userLogin.max_bets || 'Unlimited'}</div>
            </div>
            <div>
              <span className="text-gray-600">Max Wagers:</span>
              <div className="font-medium">
                {userLogin.max_wagers ? formatCurrency(userLogin.max_wagers) : 'Unlimited'}
              </div>
            </div>
            <div>
              <span className="text-gray-600">Max Loss:</span>
              <div className="font-medium">
                {userLogin.max_loss ? formatCurrency(userLogin.max_loss) : 'Unlimited'}
              </div>
            </div>
            <div>
              <span className="text-gray-600">Withdrawals:</span>
              <div className={`font-medium ${userLogin.withdrawals ? 'text-success-600' : 'text-danger-600'}`}>
                {userLogin.withdrawals ? 'Enabled' : 'Disabled'}
              </div>
            </div>
          </div>
        </div>

        {/* Bet Size Limits */}
        {(userLogin.min_bet_size > 0 || userLogin.max_bet_size > 0) && (
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-3">Bet Size Limits</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              {userLogin.min_bet_size > 0 && (
                <div>
                  <span className="text-gray-600">Min Bet Size:</span>
                  <div className="font-medium">{formatCurrency(userLogin.min_bet_size)}</div>
                </div>
              )}
              {userLogin.max_bet_size > 0 && (
                <div>
                  <span className="text-gray-600">Max Bet Size:</span>
                  <div className="font-medium">{formatCurrency(userLogin.max_bet_size)}</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Game Restrictions */}
        {userLogin.distribution_id > 0 && (
          <div className="bg-warning-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-warning-900 mb-2">Game Restrictions</h4>
            <div className="text-sm">
              <div>
                <span className="text-warning-700">Restricted to Distribution ID:</span>
                <span className="font-medium ml-1">{userLogin.distribution_id}</span>
              </div>
              {userLogin.game && (
                <div className="mt-1">
                  <span className="text-warning-700">Game:</span>
                  <span className="font-medium ml-1">{userLogin.game}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Authentication Details */}
        <div>
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <Key className="h-4 w-4" />
            <span>Authentication</span>
          </h4>
          <div className="space-y-3">
            <div className="grid grid-cols-1 gap-2 text-sm">
              <div>
                <span className="text-gray-600">Wallet Address:</span>
                <div className="font-mono text-xs bg-gray-100 p-2 rounded break-all">
                  {userLogin.address}
                </div>
              </div>
              <div>
                <span className="text-gray-600">Public Key:</span>
                <div className="font-mono text-xs bg-gray-100 p-2 rounded break-all">
                  {userLogin.public_key}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Timestamps */}
        <div className="border-t pt-4">
          <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <Calendar className="h-4 w-4" />
            <span>Timeline</span>
          </h4>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-600">Created:</span>
              <span className="font-medium">{formatDate(userLogin.created_at)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Expires:</span>
              <span className="font-medium">{formatDate(userLogin.expires_at)}</span>
            </div>
            {userLogin.deactivated_at && (
              <div className="flex justify-between">
                <span className="text-gray-600 flex items-center space-x-1">
                  <LogOut className="h-3 w-3" />
                  <span>Deactivated:</span>
                </span>
                <span className="font-medium text-danger-600">
                  {formatDate(userLogin.deactivated_at)}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Signed Message */}
        <div className="border-t pt-4">
          <h4 className="text-sm font-medium text-gray-900 mb-2">Signed Message</h4>
          <div className="bg-gray-100 p-3 rounded-md">
            <pre className="text-xs whitespace-pre-wrap break-words">
              {userLogin.signed_message}
            </pre>
          </div>
          <div className="mt-2">
            <span className="text-xs text-gray-600">Signature:</span>
            <div className="font-mono text-xs bg-gray-100 p-2 rounded break-all mt-1">
              {userLogin.signature}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
