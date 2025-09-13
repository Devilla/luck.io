/*
  Standalone script to fetch settlements from the provided endpoint and
  compute the total number of bets across the returned records.
  It paginates by repeatedly requesting with a moving `before` cursor
  derived from the last record's finalized_at timestamp.

  Usage:
    node scripts/sum_bets.js [--url <endpoint_url>]

  Defaults to the provided recent settlements URL if no --url is specified.
*/

const axios = require('axios');

async function main() {
  const defaultUrl = 'https://rpc1.proov.network/solana/settlements/recent?before=1756375363866';

  const args = process.argv.slice(2);
  let endpointUrl = defaultUrl;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--url' && i + 1 < args.length) {
      endpointUrl = args[i + 1];
      i += 1;
    }
  }

  try {
    let nextUrl = new URL(endpointUrl);
    const basePath = `${nextUrl.origin}${nextUrl.pathname}`;
    const getBeforeParam = () => nextUrl.searchParams.get('before');
    const setBeforeParam = (value) => {
      nextUrl.searchParams.set('before', String(value));
    };

    let totalBets = 0;
    let numRecords = 0;
    let pages = 0;

    // Optional: allow limiting pages via CLI for safety
    const pageLimitArgIndex = args.indexOf('--max-pages');
    const maxPages = pageLimitArgIndex !== -1 && args[pageLimitArgIndex + 1]
      ? Math.max(1, parseInt(args[pageLimitArgIndex + 1], 10) || 0)
      : Infinity;

    while (pages < maxPages) {
      const response = await axios.get(nextUrl.toString(), {
        timeout: 20000,
        headers: {
          'Accept': 'application/json',
        },
        decompress: true,
        maxRedirects: 2,
      });

      if (!Array.isArray(response.data)) {
        console.error('Unexpected response shape. Expected an array.');
        break;
      }

      const records = response.data;
      if (records.length === 0) {
        break; // no more data
      }

      for (const record of records) {
        const betsValue = typeof record?.bets === 'number' ? record.bets : 0;
        totalBets += betsValue;
        numRecords += 1;
      }

      pages += 1;

      // Use the last record's finalized_at as the next cursor
      const last = records[records.length - 1];
      // finalized_at looks like an ISO string; convert to epoch ms
      // If the API expects ms number for `before`, use Date.parse
      const lastFinalizedAt = last && typeof last.finalized_at === 'string'
        ? Date.parse(last.finalized_at)
        : undefined;

      if (!lastFinalizedAt || Number.isNaN(lastFinalizedAt)) {
        break; // cannot paginate further safely
      }

      // Decrement by 1 ms to avoid fetching the same boundary record again
      const nextBefore = lastFinalizedAt - 1;
      setBeforeParam(nextBefore);

      // Also preserve any other original query params (e.g., limit) in nextUrl
      // URL object retains them automatically. Ensure path stays the same
      nextUrl = new URL(`${basePath}?${nextUrl.searchParams.toString()}`);
    }

    console.log(JSON.stringify({
      startUrl: endpointUrl,
      pagesFetched: pages,
      numRecords,
      totalBets,
    }, null, 2));
  } catch (error) {
    if (error.response) {
      console.error(`HTTP ${error.response.status}:`, error.response.data);
    } else {
      console.error('Request failed:', error.message);
    }
    process.exitCode = 1;
  }
}

main();


