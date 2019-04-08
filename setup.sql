CREATE DATABASE rematch;
CREATE ROLE rematch;
ALTER ROLE rematch PASSWORD 'matchbox';
ALTER ROLE rematch LOGIN;
\o hba.txt
SHOW HBA_FILE;
\q
