
.headers on
.mode markdown

SELECT
	-- open.ticket_id,
	-- datetime(open.performed_at, 'unixepoch', 'localtime') AS t1,
	-- datetime(wait.performed_at, 'unixepoch', 'localtime') as t2,
	open.ticket_id, open.id, open.status_enum as s1, 
	datetime(open.performed_at, 'unixepoch', 'localtime') AS t1,
	wait.id, wait.status_enum as s2, 
	datetime(wait.performed_at, 'unixepoch', 'localtime') AS t2,
	(wait.performed_at - open.performed_at)/60 AS time_to_
FROM activity open, activity wait

where open.ticket_id == wait.ticket_id
AND	open.status_enum == 0
AND wait.status_enum == 1


GROUP BY open.ticket_id;

.exit
