--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3 (Homebrew)
-- Dumped by pg_dump version 17.3 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: reading_list; Type: TABLE; Schema: public; Owner: petedavis
--

CREATE TABLE public.reading_list (
    reader character varying(100),
    month character varying(10),
    year integer,
    title character varying(100),
    author_last character varying(100),
    author_first character varying(100),
    genre character varying(50),
    subgenre character varying(50),
    pub_year integer,
    country character varying(50),
    rating numeric(10,2),
    pages integer,
    format character varying(10),
    keys text,
    pov character varying(10),
    movie boolean,
    id integer NOT NULL
);


ALTER TABLE public.reading_list OWNER TO petedavis;

--
-- Name: reading_list_id_seq; Type: SEQUENCE; Schema: public; Owner: petedavis
--

ALTER TABLE public.reading_list ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.reading_list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: reading_list; Type: TABLE DATA; Schema: public; Owner: petedavis
--

COPY public.reading_list (reader, month, year, title, author_last, author_first, genre, subgenre, pub_year, country, rating, pages, format, keys, pov, movie, id) FROM stdin;
Pete	January	2025	The War of the Worlds	Wells	H.G.	fiction	science fiction	1898	United Kingdom	2.50	145	book	alien, dystopian, war, space	first	t	1
Pete	January	2025	The Remains of the Day	Ishiguro	Kazou	fiction	historical fiction	1989	United Kingdom	4.00	245	book	literary, introspective, historical, emotion, regret, love, class	first	t	2
Pete	December	2024	Klara and the Sun	Ishiguro	Kazou	fiction	science fiction	2021	United Kingdom	4.50	303	book	dystopian, AI, existentialism, technology, consciousness	first	t	3
Pete	February	2025	Never Let Me Go	Ishiguro	Kazou	fiction	science fiction	2005	United Kingdom	4.50	288	book	dystopian, emotion, love, trauma, clone acceptance	first	t	4
Bradley	January	2025	The Hobbit	Tolkien	J.R.R	fiction	fantasy	1937	United Kingdom	4.50	374	book	high fantasy, children, war, bravery, classic	third	t	5
Pete	January	2025	Kafka on the Shore	Murakami	Haruki	Fiction	magical realism	2002	Japan	4.50	467	book	metaphysical, sex, mind and body, consciousness, symbolism	first	f	6
Pete	February	2025	The Women	Hannah	Kristen	Fiction	historical fiction	2024	United States	3.00	480	book	war, vietnam, femanism, patriotism, protest, love, history	first	f	7
Pete	February	2024	Orbital	Harvey	Samantha	fiction	science-fiction	1850	United Kingdom	2.50	205	Paperback	space, philosophy, fragility, climate, science, emotion	Third	f	8
Pete	March	2025	In the Distance	Diaz	Hernan	fiction	historical fiction	2017	United States	3.00	256	Paperback	western, adventure, travel	Third	f	9
\.


--
-- Name: reading_list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: petedavis
--

SELECT pg_catalog.setval('public.reading_list_id_seq', 9, true);


--
-- Name: reading_list reading_list_pkey; Type: CONSTRAINT; Schema: public; Owner: petedavis
--

ALTER TABLE ONLY public.reading_list
    ADD CONSTRAINT reading_list_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

