-- :name insert_simple :! :n
-- :in :username : VARCHAR(40)
-- :in :birth : DATE
INSERT INTO typing
(username, birth)
VALUES
  (:username, :birth);

-- :name get_user :? :1
-- :doc retrieve a user by name
-- :doc this needs a multiline explanation
-- :in :username : VARCHAR(40)
-- :out :birth : DATE
SELECT *
FROM typing
WHERE username = username
LIMIT 1;

-- :name list_birthdays :? :*
-- :in :birth : DATE
SELECT *
FROM typing
WHERE birth = :birth;

-- :name list_all :? :*
SELECT *
FROM basic;