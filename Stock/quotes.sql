create table quotes (
  symbol varchar(10) not null default '',
  close_date date,
  open decimal(10,2) not null default 0.00,
  high decimal(10,2) not null default 0.00,
  low decimal(10,2) not null default 0.00,
  close decimal(10,2) not null default 0.00,
  volume int,
  adj_close decimal(10,2) not null default 0.00
)
;

alter table quotes add unique index(symbol, close_date);
