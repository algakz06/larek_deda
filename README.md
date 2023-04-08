# larek_deda

docker exec -it yiialkalmi_postgres_1 psql -U project -W project

cd var/lib/postgresql/data
psql -U testuser prod
docker exec -it yiialkalmi_postgres_1 psql -U project -W project

COPY contract_improper_executions FROM 'var/lib/postgresql/data/improper.csv' DELIMITER ';' CSV HEADER;
