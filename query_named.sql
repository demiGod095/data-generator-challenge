SELECT aOpen.ticket_id,
       aWait1.performed_at - aOpen.performed_at AS time_spent_open,
       aWait2.performed_at - aWait1.performed_at AS time_spent_waiting_on_customer,
       aPending.performed_at - aWait2.performed_at AS time_spent_waiting_for_response,
       aResolved.performed_at - aPending.performed_at AS time_till_resolution,
       aClosed.performed_at - aResolved.performed_at AS t5
FROM activity aOpen
    inner join activity aWait1 on aWait1.ticket_id = aOpen.ticket_id
    inner join activity aWait2 on aWait2.ticket_id = aOpen.ticket_id
    inner join activity aPending on aPending.ticket_id = aOpen.ticket_id
    inner join activity aResolved on aResolved.ticket_id = aOpen.ticket_id
    inner join activity aClosed on aClosed.ticket_id = aOpen.ticket_id

WHERE aOpen.status_enum = (SELECT id from enum_status WHERE status_type = 'Open') AND
      aWait1.status_enum = (SELECT id from enum_status WHERE status_type = 'Waiting for Customer') AND
      aWait2.status_enum = (SELECT id from enum_status WHERE status_type = 'Waiting for Third Party') AND
      aPending.status_enum = (SELECT id from enum_status WHERE status_type = 'Pending') AND
      aResolved.status_enum = (SELECT id from enum_status WHERE status_type = 'Resolved') AND
      aClosed.status_enum = (SELECT id from enum_status WHERE status_type = 'Closed')