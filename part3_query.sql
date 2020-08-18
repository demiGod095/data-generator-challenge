-- this file has the query required for generating the output in part3

-- added for displaying column names
.header on

SELECT a1.ticket_id,
       -- difference in Unix times divided by 3600 to convert to hours
       (a2.performed_at - a1.performed_at) / 3600      AS time_spent_open,
       (a3.performed_at - a2.performed_at) / 3600      AS time_spent_waiting_on_customer,
       (a5.performed_at - a4.performed_at) / 3600      AS time_spent_waiting_for_response,
       (a6.performed_at - a5.performed_at) / 3600      AS time_till_resolution,
       -- aggregate function on table to get the earliest activity with 'contacted' as true
       (MIN(a7.performed_at) - a1.performed_at) / 3600 as time_to_first_response
FROM activity a1
         -- Self join the table for multiple values.
         INNER JOIN activity a2 ON a2.ticket_id = a1.ticket_id
         INNER JOIN activity a3 ON a3.ticket_id = a1.ticket_id
         INNER JOIN activity a4 ON a4.ticket_id = a1.ticket_id
         INNER JOIN activity a5 ON a5.ticket_id = a1.ticket_id
         INNER JOIN activity a6 ON a6.ticket_id = a1.ticket_id
         INNER JOIN activity a7 ON a7.ticket_id = a1.ticket_id
WHERE a1.status_enum = (SELECT id from enum_status WHERE status_type = 'Open')
  AND a2.status_enum = (SELECT id from enum_status WHERE status_type = 'Waiting for Customer')
  AND a3.status_enum = (SELECT id from enum_status WHERE status_type = 'Waiting for Third Party')
  AND a4.status_enum = (SELECT id from enum_status WHERE status_type = 'Pending')
  AND a5.status_enum = (SELECT id from enum_status WHERE status_type = 'Resolved')
  AND a6.status_enum = (SELECT id from enum_status WHERE status_type = 'Closed')
  -- once all the status are done, get the rows with when the customer has been contacted
  AND a7.contacted_customer = true
-- Group required for aggregate function, MIN
GROUP BY a1.ticket_id
-- Order added for a cleaner look
ORDER BY a1.ticket_id
