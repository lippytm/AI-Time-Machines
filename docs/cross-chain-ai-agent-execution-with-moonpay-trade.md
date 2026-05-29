# Cross-Chain AI Agent Execution with MoonPay Trade

## Summary

MoonPay Trade, powered by MoonPay's Decent.xyz acquisition, gives institutions and enterprises a single API surface for 200+ chains and protocols. For AI-Time-Machines, that creates a practical pattern for AI agents that can reason about a goal, request a route, wait for human approval, and execute a cross-chain transaction without hardcoding every bridge or network.

This tutorial is intentionally quote-first and approval-first. It is a prototype architecture, not financial advice and not a recommendation to run live funds without security review.

## Use Case

> “Move 25 USDC from Solana to Base so a business automation agent can pay for an on-chain service.”

The agent should not immediately transact. It should:

1. Extract the intent.
2. Request a quote.
3. Explain the route, fees, destination, and risks.
4. Ask for human approval.
5. Execute only after approval and only with configured limits.
6. Log the transaction hash and approval receipt.

## Architecture

```text
AI-Time-Machines agent
  ↓ extracts intent
Factory.ai CrossChainAgent template
  ↓ builds payload
MoonPay Trade / Decent routing
  ↓ quote + route metadata
Human approval gate
  ↓ approved only
MoonPay Trade execution
  ↓
Audit log + transaction hash + follow-up agent actions
```

## Environment Variables

```bash
MOONPAY_TRADE_API_KEY=your_key_here
MOONPAY_TRADE_BASE_URL=https://api.moonpay.com
MOONPAY_TRADE_QUOTE_PATH=/trade/v1/quote
MOONPAY_TRADE_EXECUTION_PATH=/trade/v1/execute
```

MoonPay may provide account-specific endpoints; keep these configurable.

## Intent Schema

```json
{
  "source_chain": "solana",
  "destination_chain": "base",
  "from_asset": "USDC",
  "to_asset": "USDC",
  "amount": "25.00",
  "wallet_address": "0x_or_solana_wallet",
  "destination_address": "optional_destination_wallet",
  "slippage_bps": 50,
  "memo": "AI-Time-Machines cross-chain service payment"
}
```

## Pseudocode

```python
from integrations.moonpay_trade import CrossChainExecutionRequest, MoonPayTradeClient

client = MoonPayTradeClient()
intent = CrossChainExecutionRequest(
    source_chain="solana",
    destination_chain="base",
    from_asset="USDC",
    to_asset="USDC",
    amount="25.00",
    wallet_address="demo-wallet",
    memo="AI-Time-Machines service payment",
)

quote = client.quote(intent, dry_run=True)
print(quote)

# Show quote in UI and require explicit human approval.
approved = ask_human_to_approve(quote)

if approved:
    result = client.execute(intent, dry_run=False)
    log_transaction(result)
```

## Approval UI Copy

**Cross-chain transaction request**

- From: Solana / USDC
- To: Base / USDC
- Amount: 25.00
- Destination: [wallet]
- Slippage limit: 0.50%
- Route: [from quote]
- Estimated fees: [from quote]
- Quote expires: [from quote]

Buttons: **Approve transaction** / **Reject**

## Safety Checklist

- Never let the model hold raw private keys.
- Use wallet/custody infrastructure with policy limits.
- Default to dry-run mode.
- Require human approval for live execution.
- Enforce max daily volume, max slippage, and allowlisted destination addresses.
- Log approval, quote, route, transaction hash, model prompt, and model output.
- Run a testnet/sandbox flow before mainnet.

## Business Funnel Tie-In

This tutorial supports three monetization paths:

1. **lippytmai.getbizfunds.com** — “Need funding for an AI/Web3 business automation product? Start here.”
2. **lippytmai.zo.computer** — “Run the business from a cloud computer with AI agents and automation.”
3. **AI-Time-Machines / Factory.ai** — “Build the agent workflow that connects cloud work, funding funnels, and on-chain execution.”

## Next Step

Pair this tutorial with the Factory.ai `CrossChainAgent` template so AI-Time-Machines can present it as a practical demo: prompt → quote → approval → execution plan.
