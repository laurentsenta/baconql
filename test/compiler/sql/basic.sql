-- count_all :? :s
SELECT COUNT(*)
FROM basic;

-- insert_simple :i :n
-- :username : VARCHAR(40)
INSERT INTO basic
(username, created)
VALUES
  (:username, CURRENT_DATE);