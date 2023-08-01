--
-- PostgreSQL database dump
--

-- Dumped from database version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE ROLE omelko WITH LOGIN PASSWORD 'ftQazWsxc321';
ALTER ROLE omelko SUPERUSER;

--
-- Name: CryptoStellar; Type: DATABASE; Schema: -; Owner: omelko
--

CREATE DATABASE "CryptoStellar" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'uk_UA.UTF-8';

ALTER DATABASE "CryptoStellar" OWNER TO omelko;
GRANT ALL PRIVILEGES ON DATABASE CryptoStellar TO omelko;

\connect "CryptoStellar"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: Payment; Type: TABLE; Schema: public; Owner: omelko
--

CREATE TABLE public."Payment" (
    payment_id bigint NOT NULL,
    tx_id character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    user_id bigint NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public."Payment" OWNER TO omelko;

--
-- Name: Payment_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: omelko
--

CREATE SEQUENCE public."Payment_payment_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Payment_payment_id_seq" OWNER TO omelko;

--
-- Name: Payment_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: omelko
--

ALTER SEQUENCE public."Payment_payment_id_seq" OWNED BY public."Payment".payment_id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: omelko
--

CREATE TABLE public."User" (
    user_id bigint NOT NULL,
    fullname character varying(255) NOT NULL,
    username character varying(255) NOT NULL,
    mail character varying(255) NOT NULL,
    phone character varying(255) NOT NULL,
    status character varying(25),
    subscription_status boolean NOT NULL,
    subscription_start_date timestamp without time zone,
    subscription_end_date timestamp without time zone,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    is_admin boolean DEFAULT false NOT NULL
);


ALTER TABLE public."User" OWNER TO omelko;

--
-- Name: User_user_id_seq; Type: SEQUENCE; Schema: public; Owner: omelko
--

CREATE SEQUENCE public."User_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_user_id_seq" OWNER TO omelko;

--
-- Name: User_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: omelko
--

ALTER SEQUENCE public."User_user_id_seq" OWNED BY public."User".user_id;


--
-- Name: Payment payment_id; Type: DEFAULT; Schema: public; Owner: omelko
--

ALTER TABLE ONLY public."Payment" ALTER COLUMN payment_id SET DEFAULT nextval('public."Payment_payment_id_seq"'::regclass);


--
-- Name: User user_id; Type: DEFAULT; Schema: public; Owner: omelko
--

ALTER TABLE ONLY public."User" ALTER COLUMN user_id SET DEFAULT nextval('public."User_user_id_seq"'::regclass);


--
-- Data for Name: Payment; Type: TABLE DATA; Schema: public; Owner: omelko
--

INSERT INTO public."Payment" (payment_id, tx_id, username, user_id, created_at, updated_at) VALUES (19, '50c4313d14b50b9526af1a000bf0477ff1a8e12afa808d452ac552dc86106e84', 'sappy_and_happy', 449192755, '2023-05-24 19:56:20.048484+03', '2023-05-24 16:56:20.047844+03');


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: omelko
--

INSERT INTO public."User" (user_id, fullname, username, mail, phone, status, subscription_status, subscription_start_date, subscription_end_date, created_at, updated_at, is_admin) VALUES (425645934, 'Ostap Omelchuk', 'OstapOmelchuk', 'ostap.omelchuk@gmail.com', '+380673436001', 'active', true, '2023-05-20 01:16:35.872953', '2023-06-21 01:16:35.872953', '2023-05-18 03:01:47.387485+03', '2023-05-19 22:16:35.874907+03', true);
INSERT INTO public."User" (user_id, fullname, username, mail, phone, status, subscription_status, subscription_start_date, subscription_end_date, created_at, updated_at, is_admin) VALUES (449192755, 'Ostap kel', 'sappy_and_happy', 'Kek@gmail.com', '380985164898', 'active', false, NULL, NULL, '2023-05-24 19:55:32.019658+03', '2023-05-24 17:40:20.853834+03', false);


--
-- Name: Payment_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omelko
--

SELECT pg_catalog.setval('public."Payment_payment_id_seq"', 19, true);


--
-- Name: User_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omelko
--

SELECT pg_catalog.setval('public."User_user_id_seq"', 1, false);


--
-- Name: Payment Payment_pkey; Type: CONSTRAINT; Schema: public; Owner: omelko
--

ALTER TABLE ONLY public."Payment"
    ADD CONSTRAINT "Payment_pkey" PRIMARY KEY (payment_id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: omelko
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);


--
-- Name: Payment uq_tx_id; Type: CONSTRAINT; Schema: public; Owner: omelko
--

ALTER TABLE ONLY public."Payment"
    ADD CONSTRAINT uq_tx_id UNIQUE (tx_id);


--
-- Name: Payment Payment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: omelko
--

ALTER TABLE ONLY public."Payment"
    ADD CONSTRAINT "Payment_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);


--
-- PostgreSQL database dump complete
--

