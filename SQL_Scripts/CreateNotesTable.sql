CREATE TABLE IF NOT EXISTS public."Notes"
(
    note_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    listing_id bigint,
    user_id bigint,
    note_text text,

    CONSTRAINT "Notes_listing_user_unique" UNIQUE (listing_id, user_id),

    CONSTRAINT "Notes_user_id_fkey" FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id)
        ON DELETE CASCADE,

    CONSTRAINT "Notes_listing_id_fkey" FOREIGN KEY (listing_id)
        REFERENCES public."Listings" ("ID")
        ON DELETE CASCADE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Notes"
    OWNER to postgres;