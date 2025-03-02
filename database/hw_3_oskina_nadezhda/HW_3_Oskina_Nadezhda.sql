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
) ;

-- Создание таблицы транзакций.
create table transaction (
    transaction_id int primary key,
    product_id int,
    customer_id int null,
    transaction_date varchar(30),
    online_order varchar(30),
    order_status varchar(30),
    brand varchar(30),
    product_line varchar(30),
    product_class varchar(30),
    product_size varchar(30),
    list_price float,
    standard_cost float,
    foreign key (customer_id) references customer (customer_id)
) ;

-- Вывод всех записей таблицы клиентов.
select * from customer c ;

-- Вывод всех записей таблицы транзакций.
select * from transaction t ;

-- Вывести распределение (количество) клиентов по сферам деятельности, отсортировав результат по убыванию количества.
select 
    job_industry_category, 
    count(distinct customer_id) as customer_count
from customer
group by job_industry_category
order by customer_count desc;

-- Найти сумму транзакций за каждый месяц по сферам деятельности, отсортировав по месяцам и по сфере деятельности.
select 
    date_trunc('month', to_date(t.transaction_date, 'DD.MM.YYYY')) as transaction_month,
    c.job_industry_category,
    sum(t.list_price:: numeric) as total_sales
from transaction t
join customer c on t.customer_id = c.customer_id
group by 1, 2
order by 1, 2;

-- Вывести количество онлайн-заказов для всех брендов в рамках подтвержденных заказов клиентов из сферы IT. 
select 
    t.brand, 
    count(*) as online_order_count
from transaction t
join customer c on t.customer_id = c.customer_id
where t.online_order = 'True'
  and t.order_status = 'Approved'
  and c.job_industry_category = 'IT'
group by t.brand
order by online_order_count desc;

-- Найти по всем клиентам сумму всех транзакций (list_price), максимум, минимум и количество транзакций, 
-- отсортировав результат по убыванию суммы транзакций и количества клиентов. 
-- Выполните двумя способами: используя только group by и используя только оконные функции. Сравните результат.

-- 1) Только group by 
select 
    c.customer_id,
    sum(t.list_price) as total,
    max(t.list_price) as max,
    min(t.list_price) as min,
    count(t.transaction_id) as count
from transaction t
join customer c on t.customer_id = c.customer_id
group by c.customer_id
order by total desc, count desc;

-- 2) Только оконные функции
select distinct 
    c.customer_id,
    sum(t.list_price) over (partition by c.customer_id) as total,
    max(t.list_price) over (partition by c.customer_id) as max,
    min(t.list_price) over (partition by c.customer_id) as min,
    count(t.transaction_id) over (partition by c.customer_id) as count
from transaction t
join customer c on t.customer_id = c.customer_id
order by total desc, count desc;

-- Найти имена и фамилии клиентов с минимальной/максимальной суммой транзакций за весь период
-- (сумма транзакций не может быть null). Напишите отдельные запросы для минимальной и максимальной суммы.

-- 1) Минимальная сумма
with customer_totals as (
    select 
        c.customer_id,
        c.first_name,
        c.last_name,
        sum(t.list_price) as total
    from transaction t
    join customer c on t.customer_id = c.customer_id
    group by c.customer_id, c.first_name, c.last_name
)
select first_name, last_name, total
from customer_totals
where total = (select min(total) from customer_totals);

-- 2) Максимальная сумма
with customer_totals as (
    select 
        c.customer_id,
        c.first_name,
        c.last_name,
        sum(t.list_price) as total
    from transaction t
    join customer c on t.customer_id = c.customer_id
    group by c.customer_id, c.first_name, c.last_name
)
select first_name, last_name, total
from customer_totals
where total = (select max(total) from customer_totals);

-- Вывести только самые первые транзакции клиентов. Решить с помощью оконных функций.
select customer_id, transaction_id, transaction_date, list_price
from (
    select 
        t.customer_id,
        t.transaction_id,
        t.transaction_date,
        t.list_price,
        row_number() over (partition by t.customer_id order by t.transaction_date asc, t.transaction_id asc) AS row_number
    from transaction t
) subquery
where row_number = 1;

-- Вывести имена, фамилии и профессии клиентов, между транзакциями которых был максимальный интервал (интервал вычисляется в днях).
with transaction_intervals as (
    select 
        t.customer_id,
        c.first_name,
        c.last_name,
        c.job_title,
        to_date(t.transaction_date, 'DD.MM.YYYY') as transaction_date,
        lag(to_date(t.transaction_date, 'DD.MM.YYYY')) over (partition by t.customer_id order by to_date(t.transaction_date, 'DD.MM.YYYY')) as prev_transaction_date,
        (to_date(t.transaction_date, 'DD.MM.YYYY') - lag(to_date(t.transaction_date, 'DD.MM.YYYY')) over (partition by t.customer_id order by to_date(t.transaction_date, 'DD.MM.YYYY'))) AS transaction_gap
    from transaction t
    join customer c on t.customer_id = c.customer_id
)
select first_name, last_name, job_title, transaction_gap
from transaction_intervals
order by transaction_gap desc;
where transaction_gap = (select max(transaction_gap) from transaction_intervals);