# CryptoQuant API 路由节点详细注释整理

---

## Exchange Flows 交易所流量

- `exchange-flows/reserve`  
  获取指定交易所的币种储备量（余额），衡量交易所持有的该币种总量。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/reserve?exchange=<exchange>&window=<window>
  ```

- `exchange-flows/netflow`  
  获取指定交易所的净流入（inflow - outflow），反映资金进出交易所的净变化。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/netflow?exchange=<exchange>&window=<window>
  ```

- `exchange-flows/inflow`  
  获取指定交易所的流入量，表示有多少币被转入交易所。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/inflow?exchange=<exchange>&window=<window>
  ```

- `exchange-flows/outflow`  
  获取指定交易所的流出量，表示有多少币被转出交易所。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/outflow?exchange=<exchange>&window=<window>
  ```

- `exchange-flows/transactions-count`  
  获取指定交易所的充值/提现交易次数。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/transactions-count?exchange=<exchange>&window=<window>
  ```

- `exchange-flows/addresses-count`  
  获取指定交易所的充值/提现地址数量。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/addresses-count?exchange=<exchange>&window=<window>
  ```

- `exchange-flows/in-house-flow`  
  获取交易所内部钱包之间的资金流动。
  
  ```python
  cryptoquant|<under_asset>/exchange-flows/in-house-flow?exchange=<exchange>&window=<window>
  ```

---

## Flow Indicator 资金流动指标

- `flow-indicator/mpi`  
  矿工头寸指数（Miner Position Index），衡量矿工出售压力。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/mpi?window=<window>
  ```

- `flow-indicator/exchange-shutdown-index`  
  交易所关闭指数，反映交易所暂停充值/提现的情况。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/exchange-shutdown-index?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/exchange-whale-ratio`  
  交易所巨鲸比率，大额转账占比，衡量大户行为。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/exchange-whale-ratio?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/fund-flow-ratio`  
  资金流动比率，衡量资金进出交易所的活跃度。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/fund-flow-ratio?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/stablecoins-ratio`  
  稳定币比率，衡量交易所持有的稳定币占比。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/stablecoins-ratio?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/exchange-inflow-age-distribution`  
  交易所流入币龄分布，分析流入币的持有时间分布。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/exchange-inflow-age-distribution?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/exchange-inflow-supply-distribution`  
  交易所流入币供应分布，分析流入币的供应量分布。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/exchange-inflow-supply-distribution?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/exchange-inflow-cdd`  
  交易所流入币的币天销毁（Coin Days Destroyed）。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/exchange-inflow-cdd?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/exchange-supply-ratio`  
  交易所供应比率，衡量交易所持有币量与总供应量的比值。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/exchange-supply-ratio?exchange=<exchange>&window=<window>
  ```

- `flow-indicator/miner-supply-ratio`  
  指定矿池的供应比率。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/miner-supply-ratio?miner=<miner>&window=<window>
  ```

- `flow-indicator/bank-supply-ratio`  
  指定银行（如锚定币发行方）的供应比率。
  
  ```python
  cryptoquant|<under_asset>/flow-indicator/bank-supply-ratio?bank=<bank>&window=<window>
  ```

---

## Market Indicator 市场指标

- `market-indicator/estimated-leverage-ratio`  
  估算杠杆率，反映合约市场的杠杆使用情况。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/estimated-leverage-ratio?exchange=<exchange>&window=<window>
  ```

- `market-indicator/funding-rates`  
  合约资金费率，反映多空力量对比。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/funding-rates?exchange=<exchange>&window=<window>
  ```

- `market-indicator/open-interest`  
  合约未平仓量，衡量市场活跃度。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/open-interest?exchange=<exchange>&window=<window>
  ```

- `market-indicator/long-short-ratio`  
  多空比，反映市场情绪。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/long-short-ratio?exchange=<exchange>&window=<window>
  ```

- `market-indicator/taker-buy-sell-volume`  
  主动买入/卖出成交量。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/taker-buy-sell-volume?exchange=<exchange>&window=<window>
  ```

- `market-indicator/taker-buy-sell-ratio`  
  主动买入/卖出比率。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/taker-buy-sell-ratio?exchange=<exchange>&window=<window>
  ```

- `market-indicator/basis`  
  期现价差。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/basis?exchange=<exchange>&window=<window>
  ```

- `market-indicator/funding-rate-prediction`  
  资金费率预测。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/funding-rate-prediction?exchange=<exchange>&window=<window>
  ```

- `market-indicator/average-funding-rate`  
  平均资金费率。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/average-funding-rate?exchange=<exchange>&window=<window>
  ```

- `market-indicator/average-open-interest`  
  平均未平仓量。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/average-open-interest?exchange=<exchange>&window=<window>
  ```

- `market-indicator/average-estimated-leverage-ratio`  
  平均估算杠杆率。
  
  ```python
  cryptoquant|<under_asset>/market-indicator/average-estimated-leverage-ratio?exchange=<exchange>&window=<window>
  ```

---

## Network Indicator 链上指标

- `network-indicator/active-addresses`  
  活跃地址数。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/active-addresses?window=<window>
  ```

- `network-indicator/new-addresses`  
  新增地址数。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/new-addresses?window=<window>
  ```

- `network-indicator/large-transactions`  
  大额转账数。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/large-transactions?window=<window>
  ```

- `network-indicator/mean-transaction-value`  
  平均转账金额。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/mean-transaction-value?window=<window>
  ```

- `network-indicator/median-transaction-value`  
  中位数转账金额。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/median-transaction-value?window=<window>
  ```

- `network-indicator/transactions-count`  
  链上转账次数。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/transactions-count?window=<window>
  ```

- `network-indicator/utxo-count`  
  UTXO（未花费输出）数量。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/utxo-count?window=<window>
  ```

- `network-indicator/fees`  
  链上手续费总额。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/fees?window=<window>
  ```

- `network-indicator/supply`  
  链上供应量。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/supply?window=<window>
  ```

- `network-indicator/block-count`  
  区块数量。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/block-count?window=<window>
  ```

- `network-indicator/block-interval`  
  区块间隔。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/block-interval?window=<window>
  ```

- `network-indicator/difficulty`  
  挖矿难度。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/difficulty?window=<window>
  ```

- `network-indicator/hashrate`  
  全网算力。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/hashrate?window=<window>
  ```

- `network-indicator/fees-transaction`  
  单笔交易平均手续费。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/fees-transaction?window=<window>
  ```

- `network-indicator/tokens-transferred`  
  转账代币数量。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/tokens-transferred?window=<window>
  ```

- `network-indicator/block-bytes`  
  区块字节数。
  
  ```python
  cryptoquant|<under_asset>/network-indicator/block-bytes?window=<window>
  ```

---

## Miner Flows 矿工流动

- `miner-flows/miner-outflow`  
  矿工流出量。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-outflow?window=<window>
  ```

- `miner-flows/miner-inflow`  
  矿工流入量。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-inflow?window=<window>
  ```

- `miner-flows/miner-netflow`  
  矿工净流入。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-netflow?window=<window>
  ```

- `miner-flows/miner-reserve`  
  矿工持币量。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-reserve?window=<window>
  ```

- `miner-flows/miner-to-exchange-flow`  
  矿工到交易所流量。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-to-exchange-flow?window=<window>
  ```

- `miner-flows/miner-to-miner-flow`  
  矿工之间的流量。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-to-miner-flow?window=<window>
  ```

- `miner-flows/miner-revenue`  
  矿工收入。
  
  ```python
  cryptoquant|<under_asset>/miner-flows/miner-revenue?window=<window>
  ```

---

## Inter-Entity Flows 实体间流动

- `inter-entity-flows/miner-to-miner`  
  矿工到矿工的流动。
  
  ```python
  cryptoquant|<under_asset>/inter-entity-flows/miner-to-miner?from_miner=<from_miner>&to_miner=<to_miner>&window=<window>
  ```

- `inter-entity-flows/miner-to-exchange`  
  矿工到交易所的流动。
  
  ```python
  cryptoquant|<under_asset>/inter-entity-flows/miner-to-exchange?from_miner=<from_miner>&to_exchange=<to_exchange>&window=<window>
  ```

- `inter-entity-flows/exchange-to-miner`  
  交易所到矿工的流动。
  
  ```python
  cryptoquant|<under_asset>/inter-entity-flows/exchange-to-miner?from_exchange=<from_exchange>&to_miner=<to_miner>&window=<window>
  ```

- `inter-entity-flows/miner-to-entity`  
  矿工到实体的流动。
  
  ```python
  cryptoquant|<under_asset>/inter-entity-flows/miner-to-entity?from_miner=<from_miner>&to_entity=<to_entity>&window=<window>
  ```

- `inter-entity-flows/entity-to-miner`  
  实体到矿工的流动。
  
  ```python
  cryptoquant|<under_asset>/inter-entity-flows/entity-to-miner?from_entity=<from_entity>&to_miner=<to_miner>&window=<window>
  ```

- `inter-entity-flows/entity-to-entity`  
  实体到实体的流动。
  
  ```python
  cryptoquant|<under_asset>/inter-entity-flows/entity-to-entity?from_entity=<from_entity>&to_entity=<to_entity>&window=<window>
  ```

---

## Bank Flows 银行流动

- `bank-flows/bank-inflow`  
  银行流入量。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-inflow?window=<window>
  ```

- `bank-flows/bank-outflow`  
  银行流出量。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-outflow?window=<window>
  ```

- `bank-flows/bank-netflow`  
  银行净流入。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-netflow?window=<window>
  ```

- `bank-flows/bank-reserve`  
  银行持币量。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-reserve?window=<window>
  ```

- `bank-flows/bank-to-exchange-flow`  
  银行到交易所流量。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-to-exchange-flow?window=<window>
  ```

- `bank-flows/bank-to-bank-flow`  
  银行之间的流量。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-to-bank-flow?window=<window>
  ```

- `bank-flows/bank-revenue`  
  银行收入。
  
  ```python
  cryptoquant|<under_asset>/bank-flows/bank-revenue?window=<window>
  ```

---

## Fund Data 基金数据

- `fund-data/etf-inflow`  
  ETF流入量。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-inflow?window=<window>
  ```

- `fund-data/etf-outflow`  
  ETF流出量。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-outflow?window=<window>
  ```

- `fund-data/etf-netflow`  
  ETF净流入。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-netflow?window=<window>
  ```

- `fund-data/etf-reserve`  
  ETF持币量。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-reserve?window=<window>
  ```

- `fund-data/etf-to-exchange-flow`  
  ETF到交易所流量。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-to-exchange-flow?window=<window>
  ```

- `fund-data/etf-to-etf-flow`  
  ETF之间的流量。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-to-etf-flow?window=<window>
  ```

- `fund-data/etf-revenue`  
  ETF收入。
  
  ```python
  cryptoquant|<under_asset>/fund-data/etf-revenue?window=<window>
  ```

---

## Market Data 市场数据

- `market-data/price`  
  币价数据。
  
  ```python
  cryptoquant|<under_asset>/market-data/price?window=<window>
  ```

- `market-data/ohlcv`  
  K线数据（开高低收量）。
  
  ```python
  cryptoquant|<under_asset>/market-data/ohlcv?window=<window>
  ```

- `market-data/volume`  
  成交量。
  
  ```python
  cryptoquant|<under_asset>/market-data/volume?window=<window>
  ```

- `market-data/volatility`  
  波动率。
  
  ```python
  cryptoquant|<under_asset>/market-data/volatility?window=<window>
  ```

- `market-data/price-drawdown`  
  最大回撤。
  
  ```python
  cryptoquant|<under_asset>/market-data/price-drawdown?window=<window>
  ```

- `market-data/price-drawup`  
  最大回升。
  
  ```python
  cryptoquant|<under_asset>/market-data/price-drawup?window=<window>
  ```

- `market-data/capitalization`  
  市值。
  
  ```python
  cryptoquant|<under_asset>/market-data/capitalization?window=<window>
  ```

---

## Network Data 链上数据

- `network-data/utxo-count`  
  UTXO（未花费输出）数量。
  
  ```python
  cryptoquant|<under_asset>/network-data/utxo-count?window=<window>
  ```

- `network-data/fees`  
  链上手续费总额。
  
  ```python
  cryptoquant|<under_asset>/network-data/fees?window=<window>
  ```

- `network-data/supply`  
  链上供应量。
  
  ```python
  cryptoquant|<under_asset>/network-data/supply?window=<window>
  ```

- `network-data/transactions-count`  
  链上转账次数。
  
  ```python
  cryptoquant|<under_asset>/network-data/transactions-count?window=<window>
  ```

- `network-data/addresses-count`  
  链上地址数量。
  
  ```python
  cryptoquant|<under_asset>/network-data/addresses-count?window=<window>
  ```

- `network-data/tokens-transferred`  
  转账代币数量。
  
  ```python
  cryptoquant|<under_asset>/network-data/tokens-transferred?window=<window>
  ```

- `network-data/block-bytes`  
  区块字节数。
  
  ```python
  cryptoquant|<under_asset>/network-data/block-bytes?window=<window>
  ```

- `network-data/block-count`  
  区块数量。
  
  ```python
  cryptoquant|<under_asset>/network-data/block-count?window=<window>
  ```

- `network-data/block-interval`  
  区块间隔。
  
  ```python
  cryptoquant|<under_asset>/network-data/block-interval?window=<window>
  ```

- `network-data/fees-transaction`  
  单笔交易平均手续费。
  
  ```python
  cryptoquant|<under_asset>/network-data/fees-transaction?window=<window>
  ```

- `network-data/difficulty`  
  挖矿难度。
  
  ```python
  cryptoquant|<under_asset>/network-data/difficulty?window=<window>
  ```

- `network-data/hashrate`  
  全网算力。
  
  ```python
  cryptoquant|<under_asset>/network-data/hashrate?window=<window>
  ```

- `network-data/active-addresses`  
  活跃地址数。
  
  ```python
  cryptoquant|<under_asset>/network-data/active-addresses?window=<window>
  ```

- `network-data/new-addresses`  
  新增地址数。
  
  ```python
  cryptoquant|<under_asset>/network-data/new-addresses?window=<window>
  ```

- `network-data/large-transactions`  
  大额转账数。
  
  ```python
  cryptoquant|<under_asset>/network-data/large-transactions?window=<window>
  ```

- `network-data/mean-transaction-value`  
  平均转账金额。
  
  ```python
  cryptoquant|<under_asset>/network-data/mean-transaction-value?window=<window>
  ```

---

## Mempool Statistics 内存池统计

- `mempool-statistics/mempool-size`  
  内存池大小。
  
  ```python
  cryptoquant|<under_asset>/mempool-statistics/mempool-size?window=<window>
  ```

- `mempool-statistics/mempool-fee`  
  内存池手续费。
  
  ```python
  cryptoquant|<under_asset>/mempool-statistics/mempool-fee?window=<window>
  ```

- `mempool-statistics/mempool-count`  
  内存池交易数量。
  
  ```python
  cryptoquant|<under_asset>/mempool-statistics/mempool-count?window=<window>
  ```

---

## Lightning Network Statistics 闪电网络统计

- `lightning-network-statistics/node-count`  
  闪电网络节点数量。
  
  ```python
  cryptoquant|<under_asset>/lightning-network-statistics/node-count?window=<window>
  ```

- `lightning-network-statistics/channel-count`  
  闪电网络通道数量。
  
  ```python
  cryptoquant|<under_asset>/lightning-network-statistics/channel-count?window=<window>
  ```

- `lightning-network-statistics/capacity`  
  闪电网络容量。
  
  ```python
  cryptoquant|<under_asset>/lightning-network-statistics/capacity?window=<window>
  ```

--- 
