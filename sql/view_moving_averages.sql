create view vw_moving_averages as

select *,
case 
when(ma_50 > ma_200) then 'Golden cross'
else 'Death cross'
end as signal

from(
select
trade_date,
nifty_price,

avg(nifty_price) over(
order by trade_date
rows between 49 preceding and current row
) as ma_50,

avg(nifty_price) over(
order by trade_date
rows between 199 preceding and current row
) as ma_200

from market_data
) t;