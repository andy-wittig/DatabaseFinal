-- Table: public.Flags

-- DROP TABLE IF EXISTS public."Flags";

CREATE TABLE IF NOT EXISTS public."Flags"
(
    flag_id integer NOT NULL DEFAULT nextval('"Notes_note_id_seq"'::regclass),
    flag_text text COLLATE pg_catalog."default",
    user_id bigint,
    listing_id bigint,
    CONSTRAINT "Notes_pkey" PRIMARY KEY (flag_id),
    CONSTRAINT "Notes_user_id_listing_id_key" UNIQUE (user_id, listing_id),
    CONSTRAINT "Flags_user_id_fkey" FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Notes_listing_id_fkey" FOREIGN KEY (listing_id)
        REFERENCES public."Listings" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Flags"
    OWNER to postgres;