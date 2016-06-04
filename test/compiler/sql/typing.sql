-- insert_simple :! :n
-- :username : VARCHAR(40)
-- :birth : DATE
INSERT INTO typing
(username, birth)
VALUES
(:username, :birth);

-- get_user :? :1
-- :username : VARCHAR(40)
-- >birth : DATE
-- _doc retrieve a user by name
-- _doc this needs a multiline explanation
SELECT *
FROM typing
WHERE username = username
LIMIT 1;

-- list_birthdays :? :*
-- :birth : DATE
SELECT *
FROM typing
WHERE birth = :birth;

-- list_all :? :*
SELECT *
FROM basic;