-- iron condor, what is our range (floor to tens place)
select r.close_range, count(1)
from (
  select q.symbol, q.close_date,
    qthu.close_date next_thu_close_date,
    abs(q.close-qthu.close),
    floor(abs(q.close-qthu.close)/10)*10 close_range
  from quotes q
  join quotes qthu on q.symbol = qthu.symbol and qthu.close_date = date_add(q.close_date, interval 7 day)
  where weekday(q.close_date) = 3
    and q.symbol = '^RUT') r
group by r.close_range
;

-- iron condor deviation, looks like the trend seams to be bearish
select r.close_range, count(1)
from (
  select q.symbol, q.close_date,
    qthu.close_date next_thu_close_date,
    (qthu.close-q.close) diff,
    floor((q.close-qthu.close)/10)*10 close_range
  from quotes q
  join quotes qthu on q.symbol = qthu.symbol and qthu.close_date = date_add(q.close_date, interval 7 day)
  where weekday(q.close_date) = 3
    and q.symbol = '^RUT') r
group by r.close_range
;
