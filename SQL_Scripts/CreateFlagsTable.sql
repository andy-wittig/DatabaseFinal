CREATE TABLE IF NOT EXISTS public."Flags"
(
    flag_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    flag_text text,
    user_id bigint,
    listing_id bigint,

    CONSTRAINT "Flags_user_listing_unique" UNIQUE (user_id, listing_id),

    CONSTRAINT "Flags_user_id_fkey" FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id)
        ON DELETE CASCADE,

    CONSTRAINT "Flags_listing_id_fkey" FOREIGN KEY (listing_id)
        REFERENCES public."Listings" ("ID")
        ON DELETE CASCADE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Flags"
    OWNER to postgres;