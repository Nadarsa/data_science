-- Создание таблицы клиентов.
create table customer (
    customer_id int primary key,
    first_name varchar(50),
    last_name varchar(50),
    gender varchar(30),
    dob varchar(50),
    job_title varchar(50),
    job_industry_category varchar(50),
    wealth_segment varchar(50),
    deceased_indicator varchar(50),
    owns_car varchar(30),
    address varchar(50),
    postcode varchar(30),
    state varchar(30),
    country varchar(30),
    property_valuation int
);

-- Создание таблицы транзакций.
create table transaction (
    transaction_id int primary key,
    product_id int,
    customer_id int null,
    transaction_date VARCHAR(30),
    online_order varchar(30),
    order_status varchar(30),
    brand varchar(30),
    product_line varchar(30),
    product_class varchar(30),
    product_size varchar(30),
    list_price float,
    standard_cost float,
    foreign key (customer_id) references customer (customer_id)
);

-- Вывод всех записей таблицы клиентов.
select * from customer c ;

-- Вывод всех записей таблицы транзакций.
select * from transaction t  ;

-- Вывести все уникальные бренды, у которых стандартная стоимость выше 1500 долларов.
select distinct brand from "transaction" t 
where t.standard_cost > 1500;

-- Вывести все подтвержденные транзакции за период '2017-04-01' по '2017-04-09' включительно.
select * from "transaction" t 
where t.transaction_date between '2017-04-01' and '2017-04-09'
and t.order_status = 'Approved';

-- Вывести все профессии у клиентов из сферы IT или Financial Services, которые начинаются с фразы 'Senior'.
select distinct job_title from customer
where job_industry_category in ('IT', 'Financial Services') and job_title like 'Senior%' ;

-- Вывести все бренды, которые закупают клиенты, работающие в сфере Financial Services
select distinct brand 
from "transaction" t 
left join customer c on c.customer_id = t.customer_id 
where c.job_industry_category = 'Financial Services'

-- Вывести 10 клиентов, которые оформили онлайн-заказ продукции из брендов 'Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles'.
select distinct t.customer_id, c.first_name, c.last_name
from "transaction" t 
left join customer c on c.customer_id = t.customer_id 
where t.brand in ('Giant Bicycles', 'Norco Bicycles', 'Trek Bicycles')
and t.online_order = 'True'
limit 10;

-- Вывести всех клиентов, у которых нет транзакций.
select c.customer_id
from customer c 
left join "transaction" t on t.customer_id = c.customer_id 
where t.transaction_id is null;

-- Вывести всех клиентов из IT, у которых транзакции с максимальной стандартной стоимостью.
select c.customer_id, c.first_name, c.last_name 
from "transaction" t 
left join customer c on c.customer_id = t.customer_id 
where c.job_industry_category = 'IT'
and t.standard_cost = 
	(select max(t2.standard_cost) from "transaction" t2
	left join customer c2 on c2.customer_id = t2.customer_id 
	where c2.job_industry_category = 'IT');

-- Вывести всех клиентов из сферы IT и Health, у которых есть подтвержденные транзакции за период '2017-07-07' по '2017-07-17'.
select distinct c.customer_id, c.first_name, c.last_name 
from "transaction" t 
left join customer c on c.customer_id = t.customer_id
where t.transaction_date between '2017-07-07' and '2017-07-17'
and t.order_status = 'Approved'
and c.job_industry_category in ('IT', 'Health');
