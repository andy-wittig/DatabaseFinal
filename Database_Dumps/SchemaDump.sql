--
-- PostgreSQL database dump
--

\restrict p47g1S3m8EJfXPGybFcZcPnCUsyRJlKEby7abp3k8XdcQc03hG4zxFau6BEljsz

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0

-- Started on 2025-12-07 10:48:57

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO pg_database_owner;

--
-- TOC entry 4946 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 16708)
-- Name: Favorites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Favorites" (
    favorite_id integer NOT NULL,
    user_id integer,
    listing_id bigint
);


ALTER TABLE public."Favorites" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16707)
-- Name: Favorites_favorite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Favorites" ALTER COLUMN favorite_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Favorites_favorite_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 227 (class 1259 OID 16746)
-- Name: Flags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Flags" (
    flag_id integer NOT NULL,
    flag_text text,
    user_id bigint,
    listing_id bigint
);


ALTER TABLE public."Flags" OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16745)
-- Name: Flags_flag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Flags" ALTER COLUMN flag_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Flags_flag_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16686)
-- Name: Listings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Listings" (
    "Bathrooms" character varying(255),
    "Bedrooms" character varying(255),
    "Size" real,
    "House Category" character varying(255),
    "Price" real,
    "street name" text,
    city character varying(255),
    state character varying(255),
    "Latitude" real,
    "Longitude" real,
    "InsertedDate" date,
    "ID" bigint NOT NULL
);


ALTER TABLE public."Listings" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16725)
-- Name: Notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Notes" (
    note_id integer NOT NULL,
    listing_id bigint,
    user_id bigint,
    note_text text
);


ALTER TABLE public."Notes" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16724)
-- Name: Notes_note_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Notes" ALTER COLUMN note_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Notes_note_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 16701)
-- Name: Users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Users" (
    username character varying(255),
    user_id integer NOT NULL
);


ALTER TABLE public."Users" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16700)
-- Name: Users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."Users" ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."Users_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4779 (class 2606 OID 16713)
-- Name: Favorites Favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Favorites"
    ADD CONSTRAINT "Favorites_pkey" PRIMARY KEY (favorite_id);


--
-- TOC entry 4785 (class 2606 OID 16753)
-- Name: Flags Flags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Flags"
    ADD CONSTRAINT "Flags_pkey" PRIMARY KEY (flag_id);


--
-- TOC entry 4787 (class 2606 OID 16755)
-- Name: Flags Flags_user_listing_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Flags"
    ADD CONSTRAINT "Flags_user_listing_unique" UNIQUE (user_id, listing_id);


--
-- TOC entry 4775 (class 2606 OID 16693)
-- Name: Listings Listings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Listings"
    ADD CONSTRAINT "Listings_pkey" PRIMARY KEY ("ID");


--
-- TOC entry 4781 (class 2606 OID 16734)
-- Name: Notes Notes_listing_user_unique; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Notes"
    ADD CONSTRAINT "Notes_listing_user_unique" UNIQUE (listing_id, user_id);


--
-- TOC entry 4783 (class 2606 OID 16732)
-- Name: Notes Notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Notes"
    ADD CONSTRAINT "Notes_pkey" PRIMARY KEY (note_id);


--
-- TOC entry 4777 (class 2606 OID 16706)
-- Name: Users Users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Users"
    ADD CONSTRAINT "Users_pkey" PRIMARY KEY (user_id);


--
-- TOC entry 4788 (class 2606 OID 16714)
-- Name: Favorites Favorites_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Favorites"
    ADD CONSTRAINT "Favorites_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public."Listings"("ID") ON DELETE CASCADE;


--
-- TOC entry 4789 (class 2606 OID 16719)
-- Name: Favorites Favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Favorites"
    ADD CONSTRAINT "Favorites_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users"(user_id);


--
-- TOC entry 4792 (class 2606 OID 16761)
-- Name: Flags Flags_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Flags"
    ADD CONSTRAINT "Flags_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public."Listings"("ID") ON DELETE CASCADE;


--
-- TOC entry 4793 (class 2606 OID 16756)
-- Name: Flags Flags_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Flags"
    ADD CONSTRAINT "Flags_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users"(user_id) ON DELETE CASCADE;


--
-- TOC entry 4790 (class 2606 OID 16740)
-- Name: Notes Notes_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Notes"
    ADD CONSTRAINT "Notes_listing_id_fkey" FOREIGN KEY (listing_id) REFERENCES public."Listings"("ID") ON DELETE CASCADE;


--
-- TOC entry 4791 (class 2606 OID 16735)
-- Name: Notes Notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Notes"
    ADD CONSTRAINT "Notes_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."Users"(user_id) ON DELETE CASCADE;


-- Completed on 2025-12-07 10:48:58

--
-- PostgreSQL database dump complete
--

\unrestrict p47g1S3m8EJfXPGybFcZcPnCUsyRJlKEby7abp3k8XdcQc03hG4zxFau6BEljsz

