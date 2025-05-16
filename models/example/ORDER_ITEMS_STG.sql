-- models:
--   +transient: false
--   my_new_project:
--     # Applies to all files under models/example/
--     # example:
--     #   +materialized: table

--   CUSTOMER_STG:
--     schema: L2_PROCESSING
--   ORDER_STG:
--     schema: L2_PROCESSING
--   ORDERITEMS_STG:
--     schema: L2_PROCESSING
{{ config(schema='L2_PROCESSING') }}

SELECT
    ORDERITEMID,
    ORDERID,
    PRODUCTID,
    QUANTITY,
    UNITPRICE,
    QUANTITY * UNITPRICE AS TOTALPRICE,
    UPDATED_AT
FROM ADMIN_OMS.L1_LANDING.ORDERITEMS