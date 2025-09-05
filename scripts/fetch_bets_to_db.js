/*
  Fetch all bets for a given address using the Proov endpoint:
    https://rpc1.proov.network/solana/bets/{address}?nonce=<startNonce>

  Pagination strategy:
  - The endpoint appears to return bets in descending nonce order.
  - We iterate pages and track the minimum nonce seen; after each page, we
    set the next request's `nonce` to (minNonce - 1). We also support a
    `--step` option to jump by a fixed decrement if needed.
  - The user asked to "change the nonce for every 100 bets"; we implement a
    `--page-size` hint (default 100) and switch pages after we accumulate
    about that many bets. If the endpoint returns fewer than requested, we
    still proceed using the min nonce boundary.

  Storage:
  - Persist to Postgres using node-postgres (pg). Table `bets` keyed on
    (address, nonce). Connection via --db-url or env DATABASE_URL.

  Usage:
    node scripts/fetch_bets_to_db.js --address <address> --start-nonce <n>
      --db-url <postgres_url> [--page-size 100] [--max-pages 1000] [--step 0]
      [--no-db --output ./bets.jsonl] [--output-format json|jsonl] [--until-nonce 0]
*/

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const { Pool } = require('pg');

function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

async function ensureSchema(client) {
  await client.query(`
    CREATE TABLE IF NOT EXISTS bets (
      address TEXT NOT NULL,
      nonce INTEGER NOT NULL,
      created_at TIMESTAMPTZ,
      bet DOUBLE PRECISION,
      win DOUBLE PRECISION,
      currency TEXT,
      game_name TEXT,
      distribution_id INTEGER,
      raw_bet BIGINT,
      raw_win BIGINT,
      owner_address TEXT,
      bet_type TEXT,
      status INTEGER,
      payload_json JSONB,
      PRIMARY KEY (address, nonce)
    );
  `);
}

async function fetchBetsPage(baseUrl, address, nonce) {
  const url = `${baseUrl}/solana/bets/${address}?nonce=${nonce}`;
  const res = await axios.get(url, {
    timeout: 20000,
    headers: { 'Accept': 'application/json' },
    decompress: true,
    maxRedirects: 2,
  });
  if (!Array.isArray(res.data)) {
    throw new Error('Unexpected response shape from bets endpoint');
  }
  return res.data;
}

async function upsertBets(client, address, bets) {
  if (bets.length === 0) return 0;
  const rows = bets.map((b) => ({
    address,
    nonce: b.nonce,
    created_at: b.created_at,
    bet: typeof b.bet === 'number' ? b.bet : null,
    win: typeof b.win === 'number' ? b.win : null,
    currency: b.currency ?? null,
    game_name: b.game_name ?? null,
    distribution_id: typeof b.distribution_id === 'number' ? b.distribution_id : null,
    raw_bet: typeof b.raw_bet === 'number' ? b.raw_bet : null,
    raw_win: typeof b.raw_win === 'number' ? b.raw_win : null,
    owner_address: b.owner_address ?? null,
    bet_type: b.bet_type ?? null,
    status: typeof b.status === 'number' ? b.status : null,
    payload_json: b,
  }));

  await client.query('BEGIN');
  try {
    for (const r of rows) {
      await client.query(
        `INSERT INTO bets (
           address, nonce, created_at, bet, win, currency, game_name,
           distribution_id, raw_bet, raw_win, owner_address, bet_type, status, payload_json
         ) VALUES (
           $1, $2, $3, $4, $5, $6, $7,
           $8, $9, $10, $11, $12, $13, $14
         )
         ON CONFLICT (address, nonce) DO NOTHING`,
        [
          r.address,
          r.nonce,
          r.created_at ? new Date(r.created_at) : null,
          r.bet,
          r.win,
          r.currency,
          r.game_name,
          r.distribution_id,
          r.raw_bet,
          r.raw_win,
          r.owner_address,
          r.bet_type,
          r.status,
          r.payload_json,
        ]
      );
    }
    await client.query('COMMIT');
  } catch (e) {
    await client.query('ROLLBACK');
    throw e;
  }
  return rows.length;
}

async function main() {
  const args = process.argv.slice(2);
  const getArg = (name, fallback) => {
    const i = args.indexOf(name);
    return i !== -1 && args[i + 1] !== undefined ? args[i + 1] : fallback;
  };

  const address = getArg('--address');
  const startNonceStr = getArg('--start-nonce');
  const dbUrl = getArg('--db-url', process.env.DATABASE_URL);
  const baseUrl = getArg('--base-url', 'https://rpc1.proov.network');
  const pageSize = parseInt(getArg('--page-size', '100'), 10);
  const maxPages = parseInt(getArg('--max-pages', '1000'), 10);
  const step = parseInt(getArg('--step', '0'), 10); // fixed decrement if provided
  const noDb = args.includes('--no-db');
  const outputPath = getArg('--output', path.join(process.cwd(), 'bets.jsonl'));
  const outputFormat = getArg('--output-format', 'jsonl');
  const untilNonceStr = getArg('--until-nonce');
  const untilNonce = untilNonceStr !== undefined ? parseInt(untilNonceStr, 10) : undefined;

  if (!address || !startNonceStr || (!dbUrl && !noDb)) {
    console.error('Usage: node scripts/fetch_bets_to_db.js --address <address> --start-nonce <n> --db-url <postgres_url> [--page-size 100] [--max-pages 1000] [--step 0] [--no-db --output ./bets.jsonl] [--output-format json|jsonl] [--until-nonce 0]');
    process.exit(1);
  }

  let currentNonce = parseInt(startNonceStr, 10);
  if (!Number.isFinite(currentNonce)) {
    console.error('Invalid --start-nonce');
    process.exit(1);
  }

  let pool, client, outputStream;
  if (!noDb) {
    pool = new Pool({ connectionString: dbUrl });
    client = await pool.connect();
    await ensureSchema(client);
  } else {
    const flags = outputFormat === 'json' ? 'w' : 'a';
    outputStream = fs.createWriteStream(outputPath, { flags });
    if (outputFormat === 'json') {
      outputStream.write('[');
    }
  }

  let totalInserted = 0;
  let pages = 0;
  let keepGoing = true;

  while (keepGoing && pages < maxPages) {
    try {
      const bets = await fetchBetsPage(baseUrl, address, currentNonce);
      if (bets.length === 0) {
        break;
      }

      let insertedCount;
      if (!noDb) {
        insertedCount = await upsertBets(client, address, bets);
        totalInserted += insertedCount;
      } else {
        if (outputFormat === 'jsonl') {
          for (const b of bets) {
            outputStream.write(`${JSON.stringify(b)}\n`);
          }
        } else {
          for (let i = 0; i < bets.length; i += 1) {
            if (totalInserted + i > 0) outputStream.write(',');
            outputStream.write(JSON.stringify(bets[i]));
          }
        }
        insertedCount = bets.length;
        totalInserted += insertedCount;
      }
      pages += 1;

      // Determine next nonce: either step decrement or min(nonce)-1
      const minNonce = bets.reduce((m, b) => Math.min(m, Number(b.nonce || Infinity)), Infinity);

      if (!Number.isFinite(minNonce)) {
        // fallback to decrementing by 1 if we cannot infer
        currentNonce = currentNonce - 1;
      } else {
        currentNonce = step && Number.isFinite(step) && step > 0
          ? currentNonce - step
          : minNonce - 1;
      }

      if (insertedCount < pageSize) {
        // Heuristic: if we got fewer than pageSize, likely at the end soon;
        // continue one more iteration; if next yields 0, loop will break
      }

      if (untilNonce !== undefined && currentNonce <= untilNonce) {
        break;
      }
    } catch (err) {
      if (err.response && err.response.status === 404) {
        // No more pages at this nonce; stop
        keepGoing = false;
        break;
      }
      console.error('Error fetching page:', err.message);
      // small backoff then continue
      await new Promise((r) => setTimeout(r, 500));
      // Decrement to avoid hot loop on same nonce
      currentNonce = currentNonce - 1;
    }
  }

  console.log(JSON.stringify({
    address,
    startNonce: parseInt(startNonceStr, 10),
    lastNonce: currentNonce,
    pages,
    totalInserted,
    dbUrlProvided: Boolean(dbUrl),
    outputPath: noDb ? outputPath : undefined,
  }, null, 2));
  
  if (outputStream) {
    if (outputFormat === 'json') outputStream.write(']');
    outputStream.end();
  }
  if (client) client.release();
  if (pool) await pool.end();
}

main();


