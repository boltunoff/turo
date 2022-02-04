create table raw_turo_transactions (

type TEXT
,reservation_url TEXT
,vehicle TEXT
,vehicle_id int
,date DATE
,earnings DOUBLE
,payment DOUBLE
,failed payment DOUBLE
,file_date DATE
);

create table norm_turo_transactions (

type TEXT
,reservation_url TEXT
,vehicle TEXT
,vehicle_id int
,date DATE
,earnings DOUBLE
,earnings_seq int
,payment DOUBLE
,failed payment DOUBLE
,file_date DATE
,reservation_id
,extract_create_date
,extract_update_date
--,PK: reservation_id, Date, Earnings(amount)
);


create table reservation_details (

reservation_id int
,trip_start_dt date
,trip_end_dt date
,trip_start_time datetime
,trip_end_time datetime
,total_earnings DOUBLE --(not including reimbursements..)
--,.. future fields
--,parsing detailed receipt get fields for
--tolls, smoking, cleaning, tickets, pickup drop off location, etc.
,create_dt date
,update_dt date
,ipass_requested Boolean
,ipass_requested_amt DOUBLE

);