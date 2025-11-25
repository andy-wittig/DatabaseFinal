-- Table: public.Users

-- DROP TABLE IF EXISTS public."Users";

CREATE TABLE IF NOT EXISTS public."Users"
(
    user_id integer NOT NULL,
    username character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT "Users_pkey" PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Users"
    OWNER to postgres;