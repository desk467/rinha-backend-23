#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    CREATE TABLE IF NOT EXISTS t_pessoa (
        id uuid PRIMARY KEY,
        nome varchar(120) NOT NULL,
        apelido varchar(50) NOT NULL,
        nascimento date NOT NULL,
        stack text NOT NULL
    );

    ALTER TABLE t_pessoa ADD COLUMN ts tsvector
    GENERATED ALWAYS AS (
        to_tsvector('english', nome || ' ' || apelido || ' ' || stack )) STORED;

    CREATE INDEX ts_idx ON t_pessoa USING GIN (ts);

    CREATE TABLE row_count (
        table_name text PRIMARY KEY,
        total_rows bigint
    );

    CREATE OR REPLACE FUNCTION do_count() RETURNS TRIGGER AS \$trigger\$
    DECLARE
    BEGIN
        IF TG_OP = 'INSERT' THEN
            EXECUTE 'UPDATE row_count set total_rows = total_rows + 1 where table_name = ''' || TG_TABLE_NAME || ''' ';
            RETURN NEW;
        ELSIF TG_OP = 'DELETE' THEN
            EXECUTE 'UPDATE row_count set total_rows = total_rows - 1 where table_name = ''' || TG_TABLE_NAME || ''' ';
            RETURN OLD;
        END IF;
    END;
    \$trigger\$ LANGUAGE plpgsql;

    CREATE TRIGGER count_rows_t_pessoa BEFORE INSERT OR DELETE ON t_pessoa
    FOR EACH ROW EXECUTE PROCEDURE do_count();

    INSERT INTO row_count (table_name, total_rows) VALUES ('t_pessoa', 0);

    CREATE FUNCTION notify_pessoa_insertion() RETURNS trigger AS \$trigger\$
    DECLARE
        rec RECORD;
        payload TEXT;
    BEGIN
        rec := NEW;
        payload := row_to_json(rec);
        PERFORM pg_notify('t_pessoa__insertion', payload);
        RETURN NEW;
    END;
    \$trigger\$ LANGUAGE plpgsql;

    CREATE TRIGGER notify_inserts_on_pessoa
    BEFORE INSERT ON t_pessoa
    FOR EACH ROW
    EXECUTE PROCEDURE notify_pessoa_insertion();
EOSQL
