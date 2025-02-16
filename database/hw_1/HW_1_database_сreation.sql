CREATE DATABASE homework_1;

CREATE TABLE Job (
    job_id INT PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    job_industry_category VARCHAR(100) NOT NULL
);

CREATE TABLE Location (
    postcode INT PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

CREATE TABLE Brand (
    brand_id INT PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    product_line VARCHAR(100) NOT NULL
);

CREATE TABLE Product (
    product_id INT PRIMARY KEY,
    brand_id INT NOT NULL,
    product_class VARCHAR(50) NOT NULL,
    product_size VARCHAR(50) NOT NULL,
    list_price DECIMAL(10,2) NOT NULL,
    standard_cost DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_product_brand FOREIGN KEY (brand_id) REFERENCES Brand(brand_id)
);

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    DOB DATE NOT NULL,
    job_id INT,  -- Внешний ключ
    wealth_segment VARCHAR(50) NOT NULL,
    deceased_indicator CHAR(1) CHECK (deceased_indicator IN ('Y', 'N')) NOT NULL,
    owns_car BOOLEAN NOT NULL,
    address VARCHAR(255) NOT NULL,
    postcode INT NOT NULL,  -- Внешний ключ
    property_valuation INT NOT NULL,
    CONSTRAINT fk_customer_job FOREIGN KEY (job_id) REFERENCES Job(job_id),
    CONSTRAINT fk_customer_location FOREIGN KEY (postcode) REFERENCES Location(postcode)
);

CREATE TABLE Transaction (
    transaction_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    online_order BOOLEAN NOT NULL,
    order_status VARCHAR(50) CHECK (order_status IN ('Approved', 'Cancelled', 'Pending')) NOT NULL,
    CONSTRAINT fk_transaction_customer FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    CONSTRAINT fk_transaction_product FOREIGN KEY (product_id) REFERENCES Product(product_id)
);