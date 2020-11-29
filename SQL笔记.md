# SQL笔记

## 删除重复值，取最小值

有如下表和数据，删除表中重复记录，保留id最小值的记录

```mysql
CREATE TABLE IF NOT EXISTS titles_test (
id int(11) not null primary key,
emp_no int(11) NOT NULL,
title varchar(50) NOT NULL,
from_date date NOT NULL,
to_date date DEFAULT NULL);

insert into titles_test values 
('1', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('2', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('3', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('4', '10004', 'Senior Engineer', '1995-12-03', '9999-01-01'),
('5', '10001', 'Senior Engineer', '1986-06-26', '9999-01-01'),
('6', '10002', 'Staff', '1996-08-03', '9999-01-01'),
('7', '10003', 'Senior Engineer', '1995-12-03', '9999-01-01');
```

#### MSQL解法：

```mysql
delete from titles_test
where id not in 
(select * from 
    (select min(id) from titles_test group by emp_no) 
    as a );
```

#### 其他解法：

（mysql会提示You can't specify target table for update in FROM clause错误，意思是，不能先select出同一表中的某些值，再update这个表(在同一语句中)

```mysql
delete from titles_test
where id not in  
    (select min(id) from titles_test group by emp_no) ;
```

