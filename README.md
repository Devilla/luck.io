# Luck.io - Proov Network Analytics

A comprehensive Next.js application for analyzing and verifying bets on the Proov Network gaming platform. This application provides real-time analytics, bet verification, and detailed insights into gaming data.

## Features

🎰 **Bet Analysis**
- Detailed bet information display
- Profit/loss calculations
- Multiplier analysis
- Shard information

🔍 **Bet Verification**
- 6-step verification process
- Signature validation
- Payout verification
- Settlement confirmation

🎮 **Game Distribution Analysis**
- House edge calculations
- Volatility ratings
- Betting limits
- Payout structures

👤 **User Analytics**
- User statistics
- Betting patterns
- Authentication details
- Session analysis

## Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **API Client**: Axios
- **Charts**: Recharts

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Run the development server**:
```bash
npm run dev
```

3. **Open your browser**:
Navigate to [http://localhost:3000](http://localhost:3000)

## Usage

### Bet Search
1. Enter a bet address and nonce in the search form
2. Click "Search Bet" to load bet details
3. View comprehensive bet information including:
   - Bet amount and winnings
   - Game details
   - Shard information
   - Timestamps and addresses

### Bet Verification
1. After loading a bet, click "Verify Bet"
2. View the 6-step verification process:
   - Login message signature verification
   - Bet request signature verification
   - Oracle randomness validation
   - Payout calculation verification
   - Shard award verification
   - Settlement value confirmation

### Game Distributions
- Browse available games and their configurations
- View house edge, volatility ratings, and betting limits
- Analyze game-specific settings

### Analytics Dashboard
- View aggregated statistics
- Monitor platform performance
- Analyze betting patterns

## API Integration

The application integrates with several Proov Network endpoints:

- `/solana/bets/{address}/{nonce}` - Bet details
- `/games/distributions` - Game configurations
- `/games/distributions/{id}` - Specific game distribution
- `/solana/login/key/{publicKey}` - User authentication
- `/solana/settlements/{address}/{nonce}` - Settlement data
- `/solana/signers` - Oracle signers

## Example Data

The application includes sample data based on the provided API responses:

**Sample Bet**: Address `6kRQgeBFq3Qh32rP16cGz9gisfMUM6umFpPZVwkQx8Ez`, Nonce `43359`
- Game: Madame Fortune
- Bet: $1,000 (5.85 SOL)
- Win: $1,661,000 (9,714.36 SOL)
- Multiplier: 1,661x

## Components

### Core Components

- **BetCard**: Displays comprehensive bet information
- **GameDistributionCard**: Shows game configuration and limits
- **UserLoginCard**: User authentication and statistics
- **BetVerificationCard**: Multi-step verification process

### Features

- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Real-time Data**: Live API integration with error handling
- **Interactive UI**: Tabbed navigation and collapsible sections
- **TypeScript**: Full type safety throughout the application

## CORS Considerations

Since this is a client-side application calling external APIs, you may encounter CORS restrictions. For production use, consider:

1. Setting up a backend proxy
2. Using Next.js API routes as middleware
3. Configuring CORS on the Proov Network APIs

## Development

### Project Structure

```
├── app/                    # Next.js 13+ app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx          # Home page
├── components/            # React components
│   ├── BetCard.tsx
│   ├── GameDistributionCard.tsx
│   ├── UserLoginCard.tsx
│   └── BetVerificationCard.tsx
├── lib/                   # Utility libraries
│   └── api.ts            # API client functions
├── types/                 # TypeScript type definitions
│   └── proov.ts          # Proov Network types
└── public/               # Static assets
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Proov Network for providing the gaming platform APIs
- Next.js team for the excellent framework
- Tailwind CSS for the utility-first styling approach
