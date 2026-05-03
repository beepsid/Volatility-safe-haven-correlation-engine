create view vw_gold_price_during_crash as

select 
date_trunc('week', trade_date) as week,
avg(gold_price) as gold_price_on_crash,
count(*) as crash_days
from market_data
where high_vol_flag='True'
group by week
order by week;