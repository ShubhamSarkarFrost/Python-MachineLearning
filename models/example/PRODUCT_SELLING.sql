{{ config(schema='L2_PROCESSING') }}

WITH ProductSales AS (
    SELECT
        P.PRODUCTID,
        P.NAME,
        SUM(OI.QUANTITY) AS TOTAL_UNITS_SOLD,
        SUM(OI.QUANTITY * OI.UNITPRICE) AS TOTAL_REVENUE
    FROM
        ADMIN_OMS.L1_LANDING.ORDERITEMS OI
    JOIN
        ADMIN_OMS.L1_LANDING.PRODUCTS P ON OI.PRODUCTID = P.PRODUCTID
    GROUP BY
        P.PRODUCTID,
        P.NAME
),

RankedProductSales AS (
    SELECT
        *,
        RANK() OVER (ORDER BY TOTAL_REVENUE DESC) AS REVENUE_RANK
    FROM
        ProductSales
)

SELECT *
FROM RankedProductSales
WHERE REVENUE_RANK = 1 -- Best-selling products
   OR REVENUE_RANK = (SELECT MAX(REVENUE_RANK) FROM RankedProductSales) -- Low-selling products