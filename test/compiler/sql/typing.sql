-- insert_simple :! :n
-- :username : VARCHAR(40)
-- :birth : DATE
INSERT INTO typing
(username, birth)
VALUES
(:username, :birth);

-- list_birthdays :? :*
-- :birth : DATE
SELECT *
FROM typing
WHERE birth = :birth;

-- list_all :? :*
SELECT *
FROM basic;