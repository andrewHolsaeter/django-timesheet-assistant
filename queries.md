# Queries
## Timesheet
Project | Sub_Project.Description 
```
SELECT / Show all sub_project descriptions and their project names 
SELECT p.name, sp.description FROM sub_projects sp
INNER JOIN projects p
ON p.id = sp.project_id;
```

SELECT sub_project subscriptions for a given project
```
SELECT sp.description FROM sub_projects sp
INNER JOIN projects p
ON p.id = sp.project_id
WHERE p.name = 'OpenLab';
```

full-id and description for a given project
```
SELECT sp.description, p.id || '-' || sp.id AS full_id FROM sub_projects sp
INNER JOIN projects p
ON p.id = sp.project_id
WHERE p.name = 'OpenLab';
```

## Date Times - Example
Create a table with optional start, end, and span and auto created_at TIMESTAMP
```
CREATE TABLE test_dates(
id serial PRIMARY KEY,
start_at TIME,
end_at TIME,
span TIME,
created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);
```

### Using start_at and end_at
Insert into that table span of 30 minutes using interval`
```
INSERT INTO test_dates(start_at, end_at) VALUES (
NOW() - interval '15 minutes', NOW() + interval '15 minutes');
```

Confirm that insert by calculating interval:
```
SELECT d.end_at - d.start_at FROM test_dates d;
```
INSERT start_at NOW() and update later end_at with NOW()
```
INSERT INTO test_dates(start_at) VALUES (NOW());

UPDATE test_dates SET end_at = NOW() WHERE id = <id>;
```

Calculate span and convert to hours
```
SELECT extract(epoch from d.end_at - d.start_at)/3600 FROM test_dates d;
```

### Using span 
!NOTE! Need to add another day column so I can get weeknumber when just inserting span
Insert span only
```
INSERT INTO test_dates(span) VALUES ('1h 30m'::interval);
```

### Using date
```
UPDATE test_dates
SET date = NOW()
WHERE test_dates.id = <id>;
```
Get week number
```
SELECT to_char(d.date, 'IW') AS week FROM test_dates d;
```

Insert a span a week ago
```
INSERT INTO test_dates(span, date)
VALUES (1.25, NOW()- '1 week'::interval);
```

### Using all three
Calculate span when there is both end and start
```
SELECT extract(epoch from d.end_at - d.start_at)/3600 FROM test_dates d
WHERE d.start_at IS NOT NULL
AND d.end_at IS NOT NULL;
```


Conditional calculation of span
```
SELECT *,
	CASE
	WHEN d.span IS NOT NULL THEN d.span
	WHEN d.start_at IS NOT NULL AND d.end_at IS NOT NULL THEN d.end_at - d.start_at
	ELSE NULL
	END
FROM test_dates d
WHERE to_char(d.date, 'IW') = '15';
```



```
SELECT * FROM generate_series(
date_trunc('day', to_date('202015', 'iyyyiw')),
date_trunc('day', to_date('202015', 'iyyyiw') + 6),
'1 day'
) AS t
FULL OUTER JOIN (SELECT d.date, d.sub_project_id,
  SUM( CASE
   WHEN d.span IS NOT NULL THEN d.span
   WHEN d.start_at IS NOT NULL AND d.end_at IS NOT NULL THEN d.end_at - d.start_at
   ELSE NULL
  END) AS  hours
FROM test_dates d
WHERE to_char(d.date, 'IW') = '15'
GROUP BY 1, d.sub_project_id) y
on t = y.date
;
```

```
SELECT days.date, ts.sub_project_id, ts.hours FROM generate_series(
date_trunc('day', to_date('202015', 'iyyyiw')),
date_trunc('day', to_date('202015', 'iyyyiw') + 6),
'1 day'
) days
FULL OUTER JOIN 
(SELECT d.date, d.sub_project_id,
  SUM( CASE
   WHEN d.span IS NOT NULL THEN d.span
   WHEN d.start_at IS NOT NULL AND d.end_at IS NOT NULL THEN d.end_at - d.start_at
   ELSE NULL
  END) AS  hours
FROM test_dates d
WHERE to_char(d.date, 'IW') = '15'
GROUP BY 1, d.sub_project_id) ts
ON days.date = ts.date;
```

```
create or replace function sp_test()
returns void as
$$

declare cases character varying;
declare sql_statement text;
begin
    drop table if exists temp_series;
    create temporary  table temp_series as
    SELECT to_char(generate_series(
      date_trunc('day', to_date('202015', 'iyyyiw')),
      date_trunc('day', to_date('202015', 'iyyyiw') + 6),
      '1 day'),'YYYY-MM-DD') as series;

    select string_agg(concat('max(case when t1.series=','''',series,'''',' then t1.series else ''0000-00-00'' end) as ','"', series,'"'),',') into cases from temp_series;

    drop table if exists temp_data;
    sql_statement=concat('create temporary table temp_data as select ',cases ,' 
    from temp_series t1');

    raise notice '%',sql_statement;
    execute sql_statement;
end;
$$
language 'plpgsql';
```

```
SELECT d.date, sp.project_id, sp.index, SUM( CASE
   WHEN d.span IS NOT NULL THEN d.span
   WHEN d.start_at IS NOT NULL AND d.end_at IS NOT NULL THEN d.end_at - d.start_at
   ELSE NULL
  END) AS hours
FROM test_dates d
JOIN sub_projects sp ON d.sub_project_id = sp.index
WHERE to_char(d.date, 'IW') = '15'
GROUP BY d.date, sp.project_id, sp.index
ORDER BY d.date, sp.project_id, sp.index;
```