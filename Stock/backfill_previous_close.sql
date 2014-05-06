-- mysql -u root stock < backfill_previous_close.sql 

drop temporary table if exists backfill_previous_close;

create temporary table backfill_previous_close (
close_date date,
symbol varchar(10),
prev_close_date date,
prev_close decimal(10,2)
)
;

insert into backfill_previous_close
select
-- qcur.symbol, qcur.close_date, qcur.close, qpre.close_date prev_close_date, qpre.close prev_close
  qcur.close_date, qcur.symbol, qpre.close_date prev_close_date, qpre.close prev_close
from (
  select q.symbol, q.close_date, q.close, max(qprev.close_date) prev_close_date
  from quotes q
  join (
    select symbol, close_date
    from quotes
  ) qprev on q.symbol = qprev.symbol and qprev.close_date < q.close_date
  where 1=1
    -- All null columns
    -- and q.prev_close_date is null
    and q.close_date >= curdate()
  group by q.symbol, q.close_date) qcur
join quotes qpre on qcur.symbol = qpre.symbol and qcur.prev_close_date = qpre.close_date
order by 1, 2
;

update quotes q
join backfill_previous_close b on q.symbol=b.symbol and q.close_date = b.close_date
set q.prev_close_date = b.prev_close_date, q.prev_close=b.prev_close,
q.direction = (case when (q.close>b.prev_close) then 'up' when q.close<b.prev_close then 'down' else 'neutral' end),
q.pct_change = ((q.close/b.prev_close)-1)*100
;

drop temporary table backfill_previous_close;

