CREATE ROLE govhack_user;
GRANT govhack_user TO CURRENT_USER;
CREATE DATABASE govhack WITH OWNER govhack_user ENCODING 'utf8';
