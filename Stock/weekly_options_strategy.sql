-- I was skeptical of my calcuations.  98% win rate on 3 strikes OTM.  Down to 2 = ~96%, down to 1 = ~95%.
-- What was I doing wrong?  So how about ATM... <50%!  Yep, this calculation is right!
set @strikes_otm := 3;

select r.symbol,
  get_prev.close_date previous_close_date,
  get_prev.close previous_close,
  r.close_date,
  r.close,
  ((r.close/get_prev.close)-1)*100 pct_growth,
  next_thu.close_date next_thu_close_date,
  next_thu.close next_thu_close,
  -- This is our strike interval
  -- (case when r.close<=25 then 2.5 when r.close>25 and r.close<=200 then 5 else 10 end) strike_interval,
  -- we always want to compare against 3 strikes OTM
  case when (((r.close/get_prev.close)-1)*100 > 1 and next_thu.close<(r.close+(@strikes_otm*((case when r.close<=25 then 2.5 when r.close>25 and r.close<=200 then 5 else 10 end)))))
    then 'WIN'
    when (((r.close/get_prev.close)-1)*100 < 1 and next_thu.close>(r.close-(@strikes_otm*((case when r.close<=25 then 2.5 when r.close>25 and r.close<=200 then 5 else 10 end)))))
    then 'WIN'
    else 'LOSE'
    end outcome
from quotes get_prev
join (
  select qcur.close_date, qcur.symbol, qcur.close, max(qprev.close_date) previous_close
  from quotes qprev
  join (
    select close_date, symbol, close
    from quotes
    where weekday(close_date) in (3, 4)
      and close_date > '2013-01-03') qcur on qcur.symbol = qprev.symbol and qprev.close_date < qcur.close_date
  group by qcur.close_date, qcur.symbol, qcur.close) r on r.symbol = get_prev.symbol and r.previous_close = get_prev.close_date
join quotes next_thu on r.symbol = next_thu.symbol and next_thu.close_date = date_add(r.close_date, interval (10 - weekday(r.close_date))  day)
where abs(((r.close/get_prev.close)-1)*100)>=1
;

