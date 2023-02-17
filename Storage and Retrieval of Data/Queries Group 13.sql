# Key Insights from the Optimization Process:

# 1. Optimizing Data Types

	# To improve the efficiency and storage of our queries, we reviewed the data types in our table
	# creation script. Initially, many of the columns were using the varchar data type with unnecessarily
	# large character sizes.

	# After our revision, we changed the data types of certain values to more appropriate formats,
	# such as date or integer. We also reduced the sizes of most varchar and integer data types
	# (converting them to smallint or tinyint where applicable) to match their actual needs and
	# allow for better scalability of the database.

# 2. Improving Query Performance through the Creation of Foreign Keys and Indexes
    
	# In the initial phase of our script, we did not include Foreign Keys or Indexes. However, to improve
	# the efficiency of our queries, we added both Foreign Keys and Indexes to the final version of our script.
	# To evaluate the impact of the changes we made, using both schemas we ran the five queries used to answer
    # question F and the two views created to answer question G. We then compared the results in terms of:
        
		# 2.1. Duration / Fetch Time
            
			# While the difference may not be significant, we observed a decrease in the time needed to run the same
            # query, indicating an improvement in efficiency. This modest impact is likely due to the fact that we
            # are working with a small database. Please see the note below for further elaboration on this topic.
                
		# 2.2. Evaluation in Query Processing
            
            # By analyzing the query execution plan, we can determine how many rows each step of the query
            # needs to examine in order to produce the final result. By adding indexes to the columns that
            # are being evaluated in the query, we can significantly improve performance by reducing the number of
            # rows that need to be scanned. Once again we saw modest impact when applying this technique.
            # Please see the note below for further elaboration on this topic.
                
# 3. Final Note:

	# Additionally, it is unlikely that any techniques we implement to improve or optimize efficiency will have
    # significant practical results due to the small amount of data currently stored in our tables. However, if
    # the tables were to contain a larger number of rows, we would likely see improvements in efficiency."

USE MINIMARKET_CHAIN;

# C. Create two triggers:
# (1) One for updates (you can choose any updating process, for example, if a
# product is sold, the trigger may update the available stock of products).

# This trigger will update the field OUT_INVENTORY in the INVENTORY table whenever
# a new sale is inserted into the SALES table."

DELIMITER $$
CREATE TRIGGER UPDATE_INVENTORY
AFTER INSERT
ON SALES
FOR EACH ROW
BEGIN
	UPDATE INVENTORY
    SET OUT_INVENTORY=OUT_INVENTORY+NEW.QUANTITY
	WHERE ENTRY_ID=NEW.ENTRY_ID;
END$$
DELIMITER ;

# (2) A trigger that inserts a row in a "log" table (your ERD should include a log table).
# For defence, you should have ready the scripts to demonstrate that the trigger works.

# When a product is sold and a sale is inserted in the SALES Table, this trigger
# will record the action in the LOG table."

DELIMITER $$
CREATE TRIGGER LOG_AFTER_SALES
AFTER INSERT
ON SALES
FOR EACH ROW
BEGIN
	INSERT LOG(`DATE_TIME`, `USER`, `ACTION`, `MESSAGE`) values
    (NOW(), USER(), "Adding a new SALE", CONCAT(NEW.QUANTITY," Unit(s) related to ", NEW.ENTRY_ID, " was/were sold."));
END$$
DELIMITER ;

# A trigger that after an update in the INVENTORY TABLE (automatic update
# as we have a trigger that updates INVENTORY TABLE whenever a sale happens)
# will record the action in the LOG Table.

DELIMITER $$
CREATE TRIGGER LOG_UPDATE_INVENTORY
AFTER UPDATE
ON INVENTORY
FOR EACH ROW
BEGIN
	INSERT `LOG`(`DATE_TIME`, `USER`, `ACTION`, `MESSAGE`) values
    (NOW(), USER(), "Updating QUANTITY", CONCAT(NEW.OUT_INVENTORY, " Unit(s) out of ", NEW.IN_INVENTORY, " related to ", NEW.ENTRY_ID, " already left the inventory."));
END$$
DELIMITER ;

# A trigger that in case we want to eliminate any record related to old prices
# in the PRICE_HISTORY Table will record the action in the LOG Table.

SET SQL_SAFE_UPDATES = 0;

DELIMITER $$
CREATE TRIGGER DELETE_PRICE_HISTORY
AFTER DELETE
ON PRICE_HISTORY
FOR EACH ROW
BEGIN
	INSERT `LOG`(`DATE_TIME`, `USER`, `ACTION`, `MESSAGE`) values
    (NOW(), USER(), "Deleting a PRICE.", CONCAT("Deleting older price of Batch ", OLD.BATCH_ID, " as it ended on the ", OLD.END_DATE,"."));
END$$
DELIMITER ;

# F. Using MySQL, write the queries to retrieve the following information:

# 1. List all the customer's names, dates, and products or services used/booked/rented/bought
# by these customers in a range of two dates.

SELECT CONCAT(C.CUSTOMER_FIRST_NAME, " " ,C.CUSTOMER_LAST_NAME) AS CUSTOMER_NAME, 
		I.INVOICE_DATE AS DATE_PURCHASE,
		W.PRODUCT_NAME AS PRODUCT
FROM CUSTOMER AS C
JOIN INVOICE AS I ON C.CUSTOMER_ID=I.CUSTOMER_ID
JOIN SALES AS S ON I.INVOICE_ID=S.INVOICE_ID
JOIN INVENTORY AS INV ON INV.ENTRY_ID=S.ENTRY_ID
JOIN WAREHOUSE AS W ON W.BATCH_ID=INV.BATCH_ID
WHERE I.INVOICE_DATE BETWEEN "2020-03-01" AND "2021-06-01"
ORDER BY CUSTOMER_NAME;

# To improve the query execution plan, we can created an index on the INVOICE_DATE field
# in the INVOICE table. This will allow the evaluation process to occur more efficiently
# by enabling faster lookups and sorting of the data.

# Fetch Time w/ Foreign Keys: 0.016 Seconds.
# Fetch Time w/o Foregin Keys: 0.016 Seconds.
# Query Execution plan w/ Foreign Keys: 1 Row per Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 120 Rows on SALES Table; 1 Row per remaining Table.

# 2. List the best three customers/products/services/places (you are free to define the criteria
# for what means "best").

 # In this question, we have defined the term 'best' as the total amount spent per client, regardless of the
 # number of purchases made or the location of those purchases."
 
SELECT CONCAT(C.CUSTOMER_FIRST_NAME, " " ,C.CUSTOMER_LAST_NAME) AS CUSTOMER_NAME,
		ROUND(SUM(S.QUANTITY*PH.PRICE*(1-P.DISCOUNT)),2) as AMOUNT_SPENT
FROM CUSTOMER AS C
JOIN INVOICE AS I ON I.CUSTOMER_ID=C.CUSTOMER_ID
JOIN SALES AS S ON S.INVOICE_ID=I.INVOICE_ID
JOIN INVENTORY AS INV ON INV.ENTRY_ID=S.ENTRY_ID
JOIN WAREHOUSE AS W ON W.BATCH_ID=INV.BATCH_ID
JOIN PRICE_HISTORY AS PH ON PH.BATCH_ID=W.BATCH_ID
JOIN PROMOTION AS P ON P.PROMOTION_ID=I.PROMOTION_ID
WHERE I.INVOICE_DATE BETWEEN PH.START_DATE AND PH.END_DATE
GROUP BY C.CUSTOMER_ID 
ORDER BY AMOUNT_SPENT DESC
LIMIT 3;

# Fetch Time w/ Foreign Keys: 0.016 Seconds.
# Fetch Time w/o Foreign Keys: 0.016 Seconds.
# Query Execution plan w/ Foreign Keys: 4 Rows on WAREHOUSE Table; 1 Row per Remaining Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 8 Rows on PRICE_HISTORY Table; 120 Rows on SALES Table; 1 Row per Remaining Table.

# 3. Get the average amount of sales/booking/rents/deliveries for a period that involves 2 or
# more years, as in the following example. This query only returns one record:

SELECT CONCAT(MONTH(DATE_SUB(NOW(),INTERVAL 2 YEAR)), "/", YEAR(DATE_SUB(NOW(),INTERVAL 2 YEAR)), 
		" - ", MONTH(NOW()), "/", YEAR(NOW())) AS PERIOD_OF_SALES,
		CONCAT(ROUND(SUM(S.QUANTITY*PH.PRICE*(1-P.DISCOUNT)),2),"€") AS TOTAL_SALES,
        CONCAT(ROUND(SUM(S.QUANTITY*PH.PRICE*(1-P.DISCOUNT))/2,2),"€") AS YEARLY_AVERAGE,
		CONCAT(ROUND(SUM(S.QUANTITY*PH.PRICE*(1-P.DISCOUNT))/(2*12),2),"€") AS MONTHLY_AVERAGE
FROM INVOICE AS I
JOIN SALES AS S ON S.INVOICE_ID=I.INVOICE_ID
JOIN INVENTORY AS INV ON INV.ENTRY_ID=S.ENTRY_ID
JOIN WAREHOUSE AS W ON W.BATCH_ID=INV.BATCH_ID
JOIN PRICE_HISTORY AS PH ON PH.BATCH_ID=W.BATCH_ID
JOIN PROMOTION AS P ON P.PROMOTION_ID=I.PROMOTION_ID
WHERE I.INVOICE_DATE > DATE(DATE_SUB(NOW(),INTERVAL 2 YEAR))
AND I.INVOICE_DATE BETWEEN PH.START_DATE AND PH.END_DATE;

# Fetch Time w/ Foreign Keys: 0.016 Seconds.
# Fetch Time w/o Foreign Keys: 0.016 Seconds.
# Query Execution plan w/ Foreign Keys: 4 Rows on WAREHOUSE Table; 1 Row per Remaining Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 8 Rows on PRICE_HISTORY Table; 120 Rows on SALES Table; 1 Row per Remaining Table.

# 4. Get the total sales/bookings/rents/deliveries by geographical location (city/country).

# In this analysis, we assumed that the geographical location of each minimarket corresponds to the city in which
# it is located. Therefore, we grouped the total sales by location. All of the minimarkets in this study are located in Portugal.

SELECT M.LOCATION,
		CONCAT(ROUND(SUM(S.QUANTITY*PH.PRICE*(1-P.DISCOUNT)),2),"€") AS TOTAL_SALES
FROM PRICE_HISTORY AS PH
JOIN WAREHOUSE AS W ON W.BATCH_ID=PH.BATCH_ID
JOIN INVENTORY AS INV ON INV.BATCH_ID=W.BATCH_ID
JOIN SALES AS S ON S.ENTRY_ID=INV.ENTRY_ID
JOIN MINIMARKET AS M ON M.MINIMARKET_ID=INV.MINIMARKET_ID
JOIN INVOICE AS I ON I.INVOICE_ID=S.INVOICE_ID
JOIN PROMOTION AS P ON P.PROMOTION_ID=I.PROMOTION_ID
GROUP BY M.LOCATION;

# Fetch Time w/ Foreign Keys: 0.016 Seconds.
# Fetch Time w/o Foreign Keys: 0.016 Seconds.
# Query Execution plan w/ Foreign Keys: 4 Rows on WAREHOUSE Table; 1 Row per Remaining Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 8 Rows on PRICE_HISTORY Table; 120 Rows on SALES Table; 1 Row per Remaining Table.

# 5. List all the locations where products/services were sold, and the product has customer's
# ratings (Yes, your ERD must consider that customers can give ratings).

# In this analysis, we wanted to find all combinations of locations and products for which there is at least one
# customer rating. To do this, we grouped the data by location and product, which automatically excluded any
# locations where a specific product was not sold. We then added a condition to our selection criteria to only include
# cases where the customer rating is not null."

SELECT M.LOCATION,
		W.PRODUCT_NAME
FROM MINIMARKET AS M
JOIN INVENTORY AS INV ON INV.MINIMARKET_ID=M.MINIMARKET_ID
JOIN WAREHOUSE AS W ON W.BATCH_ID=INV.BATCH_ID
JOIN SALES AS S ON S.ENTRY_ID=INV.ENTRY_ID
WHERE S.CUSTOMER_RATING IS NOT NULL
GROUP BY M.LOCATION, W.PRODUCT_NAME
ORDER BY M.LOCATION;

# To improve the query execution plan, we created an index on the CUSTOMER_RATING field
# in the LOCATION table. This will allow the evaluation process to occur more efficiently
# by enabling faster lookups and sorting of the data.

# Fetch Time w/ Foreign Keys: 0.016 Seconds.
# Fetch Time w/o Foreign Keys: 0.016 Seconds.
# Query Execution plan w/ Foreign Keys: 4 Rows on WAREHOUSE Table; 1 Row per Remaining Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 120 Rows on SALES Table; 1 Row per Remaining Table.

# G. Your business process includes the generation of an INVOICE (the invoice in next page is
# just an example). Create two views to recreate the information on the INVOICE, one view for
# the head and totals, one view for the details.

# The view HEAD_TOTALS will display the following information for each invoice: invoice number (as a unique identifier),
# date of issue, client name, client street address, client phone number, subtotal (before any discounts are applied),
# discount amount, and total price."

CREATE VIEW HEAD_TOTALS AS
SELECT I.INVOICE_ID,
		I.INVOICE_DATE AS DATE_OF_ISSUE,
        M.MINIMARKET_NAME,
        M.LOCATION AS MINIMARKET_LOCATION,
        M.ADRESS AS MINIMARKET_ADRESS,
		CONCAT(C.CUSTOMER_FIRST_NAME, " ",C.CUSTOMER_LAST_NAME) AS CLIENT_NAME,
        C.ADRESS AS CLIENT_ADRESS,
        SUM(PH.PRICE*S.QUANTITY) AS SUBTOTAL,
        CONCAT(ROUND(P.DISCOUNT*100,1),"%") AS DISCOUNT,
        ROUND(SUM(PH.PRICE*S.QUANTITY)*(1-P.DISCOUNT),2) AS TOTAL_PRICE
FROM INVOICE AS I
JOIN PROMOTION AS P ON P.PROMOTION_ID=I.PROMOTION_ID
JOIN CUSTOMER AS C ON C.CUSTOMER_ID=I.CUSTOMER_ID
JOIN SALES AS S ON S.INVOICE_ID=I.INVOICE_ID
JOIN INVENTORY AS INV ON INV.ENTRY_ID=S.ENTRY_ID
JOIN WAREHOUSE AS W ON W.BATCH_ID=INV.BATCH_ID
JOIN PRICE_HISTORY AS PH ON PH.BATCH_ID=W.BATCH_ID
JOIN EMPLOYEE AS E ON E.EMPLOYEE_ID=I.EMPLOYEE_ID
JOIN MINIMARKET AS M ON M.MINIMARKET_ID=E.MINIMARKET_ID
WHERE I.INVOICE_DATE BETWEEN PH.START_DATE AND PH.END_DATE 
GROUP BY I.INVOICE_ID;

# Fetch Time w/ Foreign Keys: 0.016 Seconds.
# Fetch Time w/o Foreign Keys: 0.016 Seconds.
# Query Execution plan w/ Foreign Keys: 4 Rows on WAREHOUSE Table; 1 Row per Remaining Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 8 Rows on PRICE_HISTORY Table; 24 Rows on INVENTORY Table; 120 ROWS on SALES Table; 1 Row per Remaining Table.

# The view DETAILS will display the following information for each invoice line item: invoice number (as a unique identifier),
# product name, product cost, quantity, and total amount (before any discounts are applied)."

CREATE VIEW DETAILS AS
SELECT I.INVOICE_ID,
		W.PRODUCT_NAME,
        PH.PRICE AS UNIT_PRICE,
        S.QUANTITY,
        PH.PRICE*S.QUANTITY AS AMOUNT
FROM INVOICE AS I
JOIN SALES AS S ON S.INVOICE_ID=I.INVOICE_ID
JOIN INVENTORY AS INV ON INV.ENTRY_ID=S.ENTRY_ID
JOIN WAREHOUSE AS W ON W.BATCH_ID=INV.BATCH_ID
JOIN PRICE_HISTORY AS PH ON PH.BATCH_ID=W.BATCH_ID
WHERE I.INVOICE_DATE BETWEEN PH.START_DATE AND PH.END_DATE
ORDER BY I.INVOICE_ID;

SELECT *
FROM DETAILS;

# Fetch Time w/ Foreign Keys: 0.016 seconds.
# Fetch Time w/o Foreign Keys: 0.016 seconds.
# Query Execution plan w/ Foreign Keys: 4 Rows on WAREHOUSE Table; 1 Row per Remaining Table.
# Query Execution plan w/o Foreign Keys: 4 Rows on WAREHOUSE Table; 8 Rows on PRICE_HISTORY Table; 120 Rows on SALES Table.
