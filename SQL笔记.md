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

#### MYSQL解法

```mysql
delete from titles_test
where id not in 
(select * from 
    (select min(id) from titles_test group by emp_no) 
    as a );
```

#### 其他解法

（mysql会提示You can't specify target table for update in FROM clause错误，意思是，不能先select出同一表中的某些值，再update这个表(在同一语句中)

```mysql
delete from titles_test
where id not in  
    (select min(id) from titles_test group by emp_no) ;
```



## 查找字符串'10,A,B' 中逗号','出现的次数cnt

```mysql
select (length('10,A,B')-length(replact("10,A,B",",",""))) as cnt
```



## 按右边两个字母升序排序

### substr

```sql
select first_name from employees
order by substr(first_name,-2,2)
```

### right

```mysql
select first_name from employees
order by
right(first_name,2) asc
```



## 按照dept_no进行汇总，属于同一个部门的emp_no按照逗号进行连接，结果给出dept_no以及连接出的结果employees

```mysql
CREATE TABLE `dept_emp` (
`emp_no` int(11) NOT NULL,
`dept_no` char(4) NOT NULL,
`from_date` date NOT NULL,
`to_date` date NOT NULL,
PRIMARY KEY (`emp_no`,`dept_no`));
```

group_cocnat

```mysql
select dept_emp, group_concat(emp_no)
from dept_emp
group by dept_emp
```



## 对于employees表中，输出first_name排名(按first_name升序排序)为奇数的first_name

```sql
CREATE TABLE `employees` (
`emp_no` int(11) NOT NULL,
`birth_date` date NOT NULL,
`first_name` varchar(14) NOT NULL,
`last_name` varchar(16) NOT NULL,
`gender` char(1) NOT NULL,
`hire_date` date NOT NULL,
PRIMARY KEY (`emp_no`));

INSERT INTO employees VALUES
(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES
(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES
(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');
INSERT INTO employees VALUES
(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');
```

解法

```sql
select e1.first_name 
from employees e1
where 
(select count(*)
from employees e2
where e1.first_name>=e2.first_name)%2=1
```

