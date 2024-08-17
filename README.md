# fapi_app

# Task 1
To run a project
``` bash
docker compose up
```


# Task 2
``` sql
UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE sn.name = SPLIT_PART(fn.name, '.', 1)
```

``` sql
CREATE INDEX idx_full_names_name on full_names(name);
CREATE INDEX idx_short_names_name on short_names(name);

UPDATE full_names fn
SET status = sn.status
FROM short_names sn
WHERE sn.name = SPLIT_PART(fn.name, '.', 1)

DROP INDEX IF EXISTS idx_full_names_name;
DROP INDEX IF EXISTS idx_short_names_name;
```

``` sql
WITH matched_names AS (
    SELECT fn.id, sn.status
    FROM full_names fn
    JOIN short_names sn
    ON sn.name = split_part(fn.name, '.', 1)
)
UPDATE full_names fn
SET status = mn.status
FROM matched_names mn
WHERE fn.id = mn.id;
```

``` sql
CREATE INDEX idx_full_names_name on full_names(name);
CREATE INDEX idx_short_names_name on short_names(name);

WITH matched_names AS (
    SELECT fn.id, sn.status
    FROM full_names fn
    JOIN short_names sn
    ON sn.name = split_part(fn.name, '.', 1)
)
UPDATE full_names fn
SET status = mn.status
FROM matched_names mn
WHERE fn.id = mn.id;

DROP INDEX IF EXISTS idx_full_names_name;
DROP INDEX IF EXISTS idx_short_names_name;
```
