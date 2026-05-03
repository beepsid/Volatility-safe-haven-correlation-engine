-- crash days
select trade_date, nifty_return, gold_return
from market_data
where high_vol_flag;

-- avg gold return on crash days
select avg(gold_return) as avg_gold_return_on_crash
from market_data
where high_vol_flag;

-- weekly crash analysis
select 
date_trunc('week', trade_date) as week,
avg(gold_return) as avg_gold_return,
count(*) as crash_days
from market_data
where high_vol_flag
group by week
order by week;

-- overall correlation
select corr(nifty_return, gold_return) as overall_corr
from market_data;

-- crash correlation
select corr(nifty_return, gold_return) as crash_corr
from market_data
where high_vol_flag;

-- volatility buckets
select
case 
when nifty_vol_30d < 0.005 then 'low'
when nifty_vol_30d < 0.01 then 'medium'
else 'high'
end as vol_bucket,
avg(gold_return) as avg_gold_return,
count(*) as days
from market_data
group by vol_bucket;

-- monthly trend
select 
date_trunc('month', trade_date) as month,
avg(nifty_return) as nifty,
avg(gold_return) as gold
from market_data
group by month
order by month;