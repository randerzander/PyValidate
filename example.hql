set hive.execution.engine=tez;

drop table input;
drop table target;
drop table failed_records;

create external table if not exists input(text string)
location '/user/dev/input/';

create table if not exists target(a int, b int, c int) stored as orc;

add file validate.py;
create table failed_records stored as orc as
select * from (
  -- Takes advantage of the fact that transform assumes two return columns: key & value
  -- when none are manually specified
  select transform('target', *) using 'validate.py'
  from input
) inner
where key = '-1';

select value from failed_records;
