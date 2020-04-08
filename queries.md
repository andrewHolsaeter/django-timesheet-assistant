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
