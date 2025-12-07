-- Table: public.Notes

-- DROP TABLE IF EXISTS public."Notes";

CREATE TABLE IF NOT EXISTS public."Notes"
(
    listing_id bigint,
    note_text text COLLATE pg_catalog."default",
    note_id integer NOT NULL DEFAULT nextval('"Realtors_realtor_id_seq"'::regclass),
    user_id bigint,
    CONSTRAINT "Realtors_pkey" PRIMARY KEY (note_id),
    CONSTRAINT "Notes_listing_id_user_id_key" UNIQUE (listing_id, user_id),
    CONSTRAINT "Notes_user_id_fkey1" FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Realtors_listing_id_fkey" FOREIGN KEY (listing_id)
        REFERENCES public."Listings" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Notes"
    OWNER to postgres;