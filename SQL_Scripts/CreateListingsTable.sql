-- Table: public.Listings

-- DROP TABLE IF EXISTS public."Listings";

CREATE TABLE IF NOT EXISTS public."Listings"
(
    "Bathrooms" character varying(255) COLLATE pg_catalog."default",
    "Bedrooms" character varying(255) COLLATE pg_catalog."default",
    "Size" real,
    "House Category" character varying(255) COLLATE pg_catalog."default",
    "Price" real,
    "street name" text COLLATE pg_catalog."default",
    city character varying(255) COLLATE pg_catalog."default",
    state character varying(255) COLLATE pg_catalog."default",
    "Latitude" real,
    "Longitude" real,
    "InsertedDate" date,
    "ID" bigint NOT NULL,
    CONSTRAINT "Listings_pkey" PRIMARY KEY ("ID")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Listings"
    OWNER to postgres;