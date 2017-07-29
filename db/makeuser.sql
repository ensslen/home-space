\echo 'Create user script'
\echo
\prompt 'Username: ' username

BEGIN;


CREATE USER :username WITH LOGIN;
GRANT govhack_user TO :username;
GRANT CONNECT ON DATABASE govhack TO :username;
\password :username


COMMIT;
