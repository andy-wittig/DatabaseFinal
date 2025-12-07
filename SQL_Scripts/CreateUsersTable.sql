-- Table: public.Users

-- DROP TABLE IF EXISTS public."Users";

CREATE TABLE IF NOT EXISTS public."Users"
(
    username character varying(255) COLLATE pg_catalog."default",
    user_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Users"
    OWNER to postgres;