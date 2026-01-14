# BanditForge

BanditForge simulates multi-armed bandits with epsilon-greedy and UCB strategies.

## Quick start

```bash
python -m app.server --port 5173
```

Open http://localhost:5173

## API

- POST `/api/simulate` `{ "arms": [0.1,0.4,0.2], "rounds": 200, "epsilon": 0.1 }`
- POST `/api/ucb` `{ "arms": [0.1,0.4,0.2], "rounds": 200 }`

