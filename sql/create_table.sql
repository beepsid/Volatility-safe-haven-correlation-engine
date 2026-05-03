CREATE TABLE market_data (
    trade_date DATE PRIMARY KEY,
    nifty_price NUMERIC,
    gold_price NUMERIC,
    nifty_return NUMERIC,
    gold_return NUMERIC,
    nifty_vol_30d NUMERIC,
    nifty_rsi_14 NUMERIC,
    high_vol_flag BOOLEAN,
    gold_on_crash_days NUMERIC
);