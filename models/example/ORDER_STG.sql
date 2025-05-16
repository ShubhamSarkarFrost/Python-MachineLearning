{{ config(schema='L2_PROCESSING') }}
SELECT
    ORDERID,
    ORDERDATE,
    CUSTOMERID,
    EMPLOYEEID,
    STOREID,
    STATUS AS STATUSCD,
    CASE
        WHEN STATUS = '01' THEN 'In Progress'
        WHEN STATUS = '02' THEN 'Completed'
        WHEN STATUS = '03' THEN 'Cancelled'
        WHEN STATUS = '04' THEN 'Pending'
        ELSE NULL
    END AS STATUSDESC,
    UPDATED_AT
FROM ADMIN_OMS.L1_LANDING.ORDERS