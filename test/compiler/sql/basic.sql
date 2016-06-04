-- count_all :? :s
SELECT COUNT(*)
FROM basic;

-- insert_simple :! :n
-- :username : VARCHAR(40)
INSERT INTO basic
(username)
VALUES
(:username);

-- list_all :? :*
SELECT *
FROM basic;