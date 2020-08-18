-- this file has the query required for generating the output in part3

-- added for displaying column names
.header on

SELECT a1.ticket_id,
       (a2.performed_at - a1.performed_at) / 60      AS time_spent_open,
       (a3.performed_at - a2.performed_at) / 60      AS time_spent_waiting_on_customer,
       (a5.performed_at - a4.performed_at) / 60      AS time_spent_waiting_for_response,
       (a6.performed_at - a5.performed_at) / 60      AS time_till_resolution,
       (MIN(a7.performed_at) - a1.performed_at) / 60 as time_to_first_response
FROM activity a1
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
  AND a7.contacted_customer = true
GROUP BY a1.ticket_id
ORDER BY a1.ticket_id
