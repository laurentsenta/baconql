-- :name count_all :? :s
SELECT COUNT(*)
FROM basic;

-- :name insert_simple :! :n
-- :in :username : VARCHAR(40)
INSERT INTO basic
(username)
VALUES
(:username);

-- :name list_all :? :*
SELECT *
FROM basic;