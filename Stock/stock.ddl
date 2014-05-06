DELIMITER $$
DROP FUNCTION IF EXISTS strike_interval $$
create function strike_interval(x decimal, symbol varchar(5))
  returns decimal(5,2)
  deterministic
begin
  declare get_strike_interval decimal(5,2);
  select strike_interval into get_strike_interval
  from symbol_type
  where symbol = symbol
  limit 1;

  if get_strike_interval is null then
    case when x <= 25
      then set get_strike_interval = 2.5;
      when x>25 and x<=200
      then set get_strike_interval = 5;
      else set get_strike_interval = 10;
      end case;
  end if;
  return get_strike_interval;
end
$$
DELIMITER ;

create table current_positions (
  symbol varchar(10),
  price_at_purchase decimal(10,2),
  low_call varchar(20),
  high_call varchar(20),
  outlook enum('bull', 'bear'),
  type enum('debit', 'credit'),
  low_strike decimal(10,2),
  high_strike decimal(10,2),
  low_fill decimal(10,2),
  high_fill decimal(10,2),
  qty int,
  status enum('current', 'complete')
);
