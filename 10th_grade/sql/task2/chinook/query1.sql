SELECT 
  tb.invoice_id,
  tr.track_id,
  tr.name AS track_name,
  md.name AS media_type_name,
  tb.quantity,
  tb.unit_price
FROM 
  invoice_line AS tb
  JOIN track tr ON tb.track_id = tr.track_id
  JOIN media_type AS md ON tr.media_type_id = md.media_type_id
WHERE 
  tb.invoice_id = 1;
