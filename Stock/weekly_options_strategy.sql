-- Current findings

Wins/Loss ratio is about the same for up and down days
+-----------+-----------+------------+---------+
| direction | win_total | loss_total | win_pct |
+-----------+-----------+------------+---------+
| DOWN      |      9354 |         40 |  0.9957 |
| UP        |     11083 |         78 |  0.9930 |
+-----------+-----------+------------+---------+
2 rows in set (16.04 sec)

Roughly the same for Thursday and Friday
-- Thursday
+-----------+------------+---------+
| win_total | loss_total | win_pct |
+-----------+------------+---------+
|     10685 |         72 |  0.9933 |
+-----------+------------+---------+
1 row in set (8.36 sec)
-- Friday
+-----------+------------+---------+
| win_total | loss_total | win_pct |
+-----------+------------+---------+
|      9752 |         46 |  0.9953 |
+-----------+------------+---------+
1 row in set (8.26 sec)

-- base query
    select q.symbol,
        q.prev_close_date,
        q.prev_close,
        q.close_date,
        q.close,
        q.pct_change,
        next_thu.close_date next_thu_close_date,
        next_thu.close next_thu_close,
        if (q.pct_change>=0, q.close+(3*strike_interval(q.close, q.symbol)), q.close-(3*strike_interval(q.close, q.symbol))) strike_price,
        if (q.pct_change>=0 and next_thu.close < q.close+(3*strike_interval(q.close, q.symbol)), 'WIN', if(q.pct_change<0 and next_thu.close > q.close-(3*strike_interval(q.close, q.symbol)), 'WIN', 'LOSE')) outcome
      from quotes q
      join quotes next_thu on q.symbol = next_thu.symbol
        and next_thu.close_date = date_add(q.close_date, interval (10 - weekday(q.close_date)) day)
      where q.prev_close is not null
        and (q.pct_change >= 1 or q.pct_change <= -1)
        -- Let's test against Thusday historicals (if you wanna change to Friday's, set weekday(q.close_date)=4
        and weekday(q.close_date)=3;


-- What moves should I make?
select q.*, st.type, st.strike_interval,
 winloss.win_total,
 winloss.loss_total,
 winloss.win_pct
from quotes q
join symbol_type st on q.symbol = st.symbol
join (
  select -- case when r2.pct_growth >= 1 then 'UP' else 'DOWN' end direction,
    wl1.symbol,
    sum(case when wl1.outcome='WIN' then 1 else 0 end) win_total,
    sum(case when wl1.outcome='LOSE' then 1 else 0 end) loss_total,
    sum(case when wl1.outcome='WIN' then 1 else 0 end) /sum(1) win_pct
  from (
    select q.symbol,
        q.prev_close_date,
        q.prev_close,
        q.close_date,
        q.close,
        q.pct_change,
        next_thu.close_date next_thu_close_date,
        next_thu.close next_thu_close,
        if (q.pct_change>=0, q.close+(3*strike_interval(q.close, q.symbol)), q.close-(3*strike_interval(q.close, q.symbol))) strike_price,
        if (q.pct_change>=0 and next_thu.close < q.close+(3*strike_interval(q.close, q.symbol)), 'WIN', if(q.pct_change<0 and next_thu.close > q.close-(3*strike_interval(q.close, q.symbol)), 'WIN', 'LOSE')) outcome
      from quotes q
      join quotes next_thu on q.symbol = next_thu.symbol
        and next_thu.close_date = date_add(q.close_date, interval (10 - weekday(q.close_date)) day)
      where q.prev_close is not null
        and (q.pct_change >= 1 or q.pct_change <= -1)
        -- Let's test against Thusday historicals (if you wanna change to Friday's, set weekday(q.close_date)=4
        -- weekday(q.close_date)=2 for Wed, weekday(q.close_date)=1 for Tue
        and weekday(q.close_date)=3) wl1
    group by wl1.symbol) winloss on winloss.symbol = q.symbol
where q.close_date = curdate()
  and (q.pct_change >= 1 or q.pct_change <= -1)
--  and st.type = 'etf'
order by st.type, winloss.win_pct desc, winloss.win_total desc
;

-- How did last week do?
select q.*,
  next_thu.close next_thu_close,
  if (q.pct_change>=0 and next_thu.close < q.close+(3*strike_interval(q.close, q.symbol)), 'WIN', if(q.pct_change<0 and next_thu.close > q.close-(3*strike_interval(q.close, q.symbol)), 'WIN', 'LOSE')) outcome
from quotes q
join quotes next_thu on q.symbol = next_thu.symbol
  and next_thu.close_date = date_add(q.close_date, interval (10 - weekday(q.close_date)) day)
join symbol_type st on q.symbol = st.symbol
-- q.close_date should be a previous Thursday
where q.close_date = '2014-04-24'
  and (q.pct_change >= 1 or q.pct_change <= -1)
  and st.type = 'etf'
;

-- Count of winners last week
select res.outcome, count(1)
from (
  select q.*,
    if (q.pct_change>=0 and next_thu.close < q.close+(3*strike_interval(q.close, q.symbol)), 'WIN', if(q.pct_change<0 and next_thu.close > q.close-(3*strike_interval(q.close, q.symbol)), 'WIN', 'LOSE')) outcome
  from quotes q
  join quotes next_thu on q.symbol = next_thu.symbol
    and next_thu.close_date = date_add(q.close_date, interval (10 - weekday(q.close_date)) day)
  join symbol_type st on q.symbol = st.symbol
  where q.close_date = '2014-04-24'
    and (q.pct_change >= 1 or q.pct_change <= -1)
    and st.type = 'etf') res
group by res.outcome
;

set @pct_change := 0.75;
set @strikes_out := 2;

select q.*,
 winloss.win_total,
 winloss.loss_total,
 winloss.win_pct
from quotes q
join symbol_type st on q.symbol = st.symbol
join (
  select -- case when r2.pct_growth >= 1 then 'UP' else 'DOWN' end direction,
    wl1.symbol,
    sum(case when wl1.outcome='WIN' then 1 else 0 end) win_total,
    sum(case when wl1.outcome='LOSE' then 1 else 0 end) loss_total,
    sum(case when wl1.outcome='WIN' then 1 else 0 end) /sum(1) win_pct
  from (
    select q.symbol,
        q.prev_close_date,
        q.prev_close,
        q.close_date,
        q.close,
        q.pct_change,
        next_thu.close_date next_thu_close_date,
        next_thu.close next_thu_close,
        if (q.pct_change>=0, q.close+(@strikes_out*strike_interval(q.close, q.symbol)), q.close-(@strikes_out*strike_interval(q.close, q.symbol))) strike_price,
        if (q.pct_change>=0 and next_thu.close < q.close+(@strikes_out*strike_interval(q.close, q.symbol)), 'WIN', if(q.pct_change<0 and next_thu.close > q.close-(@strikes_out*strike_interval(q.close, q.symbol)), 'WIN', 'LOSE')) outcome
      from quotes q
      join quotes next_thu on q.symbol = next_thu.symbol
        and next_thu.close_date = date_add(q.close_date, interval (10 - weekday(q.close_date)) day)
      where q.prev_close is not null
        and (q.pct_change >= @pct_change or q.pct_change <= -(@pct_change))
        -- Let's test against Thusday historicals (if you wanna change to Friday's, set weekday(q.close_date)=4
        and weekday(q.close_date)=3) wl1
    group by wl1.symbol) winloss on winloss.symbol = q.symbol
where q.close_date = curdate()
  and (q.pct_change >= @pct_change or q.pct_change <= -(@pct_change))
  and st.type = 'etf'
order by winloss.win_pct desc, winloss.win_total desc
;


-- 3 up move strategy shows 91% risk when examining T/W/Th, 93% on W/Th/F
select st.type,
  sum(case when (r.outcome='WIN') then 1 else 0 end) win_total,
  sum(case when (r.outcome='LOSE') then 1 else 0 end) win_total,
  sum(case when (r.outcome='WIN') then 1 else 0 end) / count(1) win_pct
from (
select
  thu.symbol,
--  move1.close_date m1_close_date,
  move2.close_date m2_close_date,
  move3.close_date m3_close_date,
  thu.close_date,
--  move1.close m1_close,
  move2.close m2_close,
  move3.close m3_close,
  thu.close,
  case when (move3.pct_change>=0)
    then move3.close+(3*strike_interval(move3.close, move3.symbol))
    when (move3.pct_change<0)
    then move3.close-(3*strike_interval(move3.close, move3.symbol))
    end strike_boundary,
  if (move3.pct_change>=0 and thu.close < move3.close+(3*strike_interval(move3.close, move3.symbol)), 'WIN',
    if (move3.pct_change<0 and thu.close > move3.close-(3*strike_interval(move3.close, move3.symbol)), 'WIN', 'LOSE')) outcome
from quotes thu
join quotes move3 on move3.symbol = thu.symbol and move3.close_date = date_sub(thu.close_date, interval 7 day)
join quotes move2 on move2.symbol = thu.symbol and move3.prev_close_date = move2.close_date
 join quotes move1 on move1.symbol = thu.symbol and move2.prev_close_date = move1.close_date
where weekday(thu.close_date)=3
  and ((move3.pct_change>=1
        and move2.pct_change>=1
        and move1.pct_change>=1
        )
    or (move3.pct_change<=-1
        and move2.pct_change<=-1
        and move1.pct_change<=-1
        ))
    ) r
join symbol_type st on r.symbol = st.symbol
group by st.type
;
