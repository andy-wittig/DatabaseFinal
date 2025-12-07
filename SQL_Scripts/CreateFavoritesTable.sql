-- Table: public.Favorites

-- DROP TABLE IF EXISTS public."Favorites";

CREATE TABLE IF NOT EXISTS public."Favorites"
(
    favorite_id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id integer,
    listing_id bigint,
    CONSTRAINT "Favorites_listing_id_fkey" FOREIGN KEY (listing_id)
        REFERENCES public."Listings" ("ID") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT "Favorites_user_id_fkey" FOREIGN KEY (user_id)
        REFERENCES public."Users" (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Favorites"
    OWNER to postgres;