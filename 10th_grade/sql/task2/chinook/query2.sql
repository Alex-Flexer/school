SELECT 
  alb.title AS album_name,
  art.name AS artist_name,
  SUM(inv.quantity) AS total_copies
FROM 
  album AS alb
  JOIN artist AS art ON alb.artist_id = art.artist_id
  JOIN track AS tr ON alb.album_id = tr.album_id
  JOIN invoice_line AS inv ON tr.track_id = inv.track_id
GROUP BY alb.title, art.name;
