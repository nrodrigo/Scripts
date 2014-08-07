



select r.symbol,
  sum(case when (diff <= 10) then 1 else 0 end) r_000_010,
  sum(case when (diff > 10 and diff <= 20) then 1 else 0 end) r_010_020,
  sum(case when (diff > 20 and diff <= 30) then 1 else 0 end) r_020_030,
  sum(case when (diff > 30 and diff <= 40) then 1 else 0 end) r_030_040,
  sum(case when (diff > 40 and diff <= 50) then 1 else 0 end) r_040_050,
  sum(case when (diff > 50 and diff <= 60) then 1 else 0 end) r_050_060,
  sum(case when (diff > 60 and diff <= 70) then 1 else 0 end) r_060_070,
  sum(case when (diff > 70 and diff <= 80) then 1 else 0 end) r_070_080,
  sum(case when (diff > 80 and diff <= 90) then 1 else 0 end) r_080_090,
  sum(case when (diff > 90 and diff <= 100) then 1 else 0 end) r_090_100,
  sum(case when (diff > 100 and diff <= 110) then 1 else 0 end) r_100_110,
  sum(case when (diff > 110 and diff <= 120) then 1 else 0 end) r_110_120,
  sum(case when (diff > 120 and diff <= 130) then 1 else 0 end) r_120_130,
  sum(case when (diff > 130 and diff <= 140) then 1 else 0 end) r_130_140,
  sum(case when (diff > 140 and diff <= 150) then 1 else 0 end) r_140_150,
  sum(case when (diff > 150 and diff <= 160) then 1 else 0 end) r_150_160,
  sum(case when (diff > 160 and diff <= 170) then 1 else 0 end) r_160_170,
  sum(case when (diff > 170 and diff <= 180) then 1 else 0 end) r_170_180,
  sum(case when (diff > 180 and diff <= 190) then 1 else 0 end) r_180_190,
  sum(case when (diff > 190 and diff <= 200) then 1 else 0 end) r_190_200,
  sum(case when (diff > 200 and diff <= 210) then 1 else 0 end) r_200_210
from (
  select q.symbol, q.close_date close_date1, q2.close_date close_date2, abs(q2.close-q.close) diff
  from quotes q
  join symbol_type st on q.symbol = st.symbol
  join quotes q2 on q.symbol = q2.symbol and q.close_date = date_sub(q2.close_date, interval 3 week)
  where weekday(q.close_date)=3
    and st.type = 'index') r
group by r.symbol
;

select r.symbol,
  sum(case when (r.diff<0) then 1 else 0 end) negatives,
  sum(case when (r.diff>0) then 1 else 0 end) positives
from (
  select q.symbol, q.close_date close_date1, q2.close_date close_date2, q.close close1, q2.close close2, (q2.close-q.close) diff
  from quotes q
  join symbol_type st on q.symbol = st.symbol
  join quotes q2 on q.symbol = q2.symbol and q.close_date = date_sub(q2.close_date, interval 2 week)
  where weekday(q.close_date)=3
    and st.type = 'index'
    and q.symbol in ('XEO', '^OEX')
 --   and abs(q2.close-q.close) between 20 and 40
    ) r
group by r.symbol
    ;
