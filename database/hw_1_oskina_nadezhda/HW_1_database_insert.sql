INSERT INTO Job (job_id, job_title, job_industry_category) VALUES
(1, 'Executive Secretary', 'Health'),
(2, 'Administrative Officer', 'Financial Services'),
(3, 'Recruiting Manager', 'Property'),
(4, '', 'IT'),
(5, 'Senior Editor', 'n/a');

INSERT INTO Location (postcode, state, country) VALUES
(2016, 'New South Wales', 'Australia'),
(2153, 'New South Wales', 'Australia'),
(4211, 'QLD', 'Australia'),
(2448, 'New South Wales', 'Australia'),
(3216, 'VIC', 'Australia');

INSERT INTO Brand (brand_id, brand_name, product_line) VALUES
(1, 'Solex', 'Standard'),
(2, 'Trek Bicycles', 'Standard'),
(3, 'OHM Cycles', 'Standard'),
(4, 'Norco Bicycles', 'Standard'),
(5, 'Giant Bicycles', 'Standard');

INSERT INTO Product (product_id, brand_id, product_class, product_size, list_price, standard_cost) VALUES
(2, 1, 'medium', 'medium', 71.49, 53.62),
(3, 2, 'medium', 'large', 2091.47, 388.92),
(37, 3, 'low', 'medium', 1793.43, 248.82),
(88, 4, 'medium', 'medium', 1198.46, 381.10),
(78, 5, 'medium', 'large', 1765.30, 709.48);

INSERT INTO Customer (customer_id, first_name, last_name, gender, DOB, job_id, wealth_segment, deceased_indicator, owns_car, address, postcode, property_valuation) VALUES
(1, 'Laraine', 'Medendorp', 'F', '1953-10-12', 1, 'Mass Customer', 'N', TRUE, '060 Morning Avenue', 2016, 10),
(2, 'Eli', 'Bockman', 'Male', '1980-12-16', 2, 'Mass Customer', 'N', TRUE, '6 Meadow Vale Court', 2153, 10),
(3, 'Arlin', 'Dearle', 'Male', '1954-01-20', 3, 'Mass Customer', 'N', TRUE, '0 Holy Cross Court', 4211, 9),
(4, 'Talbot', '', 'Male', '1961-10-03', 4, 'Mass Customer', 'N', FALSE, '17979 Del Mar Point', 2448, 4),
(5, 'Sheila-kathryn', 'Calton', 'Female', '1977-05-13', 5, 'Affluent Customer', 'N', TRUE, '9 Oakridge Court', 3216, 9);

INSERT INTO Transaction (transaction_id, customer_id, product_id, transaction_date, online_order, order_status) VALUES
(1, 1, 2, '2017-02-25', FALSE, 'Approved'),
(2, 2, 3, '2017-05-21', TRUE, 'Approved'),
(3, 3, 37, '2017-10-16', FALSE, 'Approved'),
(4, 4, 88, '2017-08-31', FALSE, 'Approved'),
(5, 5, 78, '2017-10-01', TRUE, 'Approved');