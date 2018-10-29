SET timezone = 'Asia/Singapore';


CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(128) UNIQUE NOT NULL,
  email VARCHAR(128) UNIQUE NOT NULL,
	name VARCHAR(128) NOT NULL,
  password_hash VARCHAR(128) NOT NULL,
	phone_no CHAR(8)
);

CREATE TABLE listing (
  listing_name VARCHAR(128) NOT NULL,
	owner_id INTEGER,
	description VARCHAR(512),
	listed_date TIMESTAMP NOT NULL,
	is_available VARCHAR(5) NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES users(id),
	PRIMARY KEY (listing_name, owner_id),
	CHECK (is_available='true' OR is_available='false')
);

CREATE TABLE bid (
	bidder_id INTEGER,
	listing_name VARCHAR(128),
	owner_id INTEGER,
	bid_date TIMESTAMP,
	price NUMERIC NOT NULL,
	FOREIGN KEY (bidder_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (listing_name, owner_id) REFERENCES listing(listing_name, owner_id) ON DELETE CASCADE,
	PRIMARY KEY (bidder_id, listing_name, owner_id, bid_date),
	CHECK (price >= 0)
);

CREATE TABLE loan (
	bidder_id INTEGER,
	listing_name VARCHAR(128),
	owner_id INTEGER,
	bid_date TIMESTAMP,
	borrow_date TIMESTAMP,
	return_date TIMESTAMP NOT NULL,
	return_loc VARCHAR(512) NOT NULL,
	pickup_loc VARCHAR(512) NOT NULL,
  FOREIGN KEY (bidder_id, listing_name, owner_id, bid_date) REFERENCES bid(bidder_id, listing_name, owner_id, bid_date),
  PRIMARY KEY (bidder_id, listing_name, owner_id, bid_date, borrow_date),
	CHECK (return_date >= borrow_date)
);

CREATE TABLE tag (
	tag_id SERIAL PRIMARY KEY,
	name VARCHAR(16) UNIQUE NOT NULL
);

CREATE TABLE listing_tag (
	tag_id INTEGER,
	listing_name VARCHAR(128),
	owner_id INTEGER,
	FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE,
  FOREIGN KEY (listing_name, owner_id) REFERENCES listing(listing_name, owner_id) ON DELETE CASCADE,
	PRIMARY KEY(tag_id, listing_name, owner_id)
);

CREATE OR REPLACE FUNCTION generate_loan() RETURNS TRIGGER AS $$
   BEGIN
      DELETE FROM bid WHERE listing_name = NEW.listing_name AND owner_id = NEW.owner_id AND bidder_id <> NEW.bidder_id;
		  UPDATE listing SET is_available = false WHERE listing_name = NEW.listing_name AND owner_id = NEW.owner_id;
      RETURN NEW;
   END; $$
LANGUAGE plpgsql;

CREATE TRIGGER on_loan_insert
  AFTER INSERT
  ON loan
  FOR EACH ROW
  EXECUTE PROCEDURE generate_loan();

CREATE OR REPLACE FUNCTION return_loan() RETURNS TRIGGER AS $$
   BEGIN
      DELETE FROM bid WHERE listing_name = OLD.listing_name AND owner_id = OLD.owner_id AND bidder_id = OLD.bidder_id;
	  UPDATE listing SET is_available = true WHERE listing_name = OLD.listing_name AND owner_id = OLD.owner_id;
      RETURN NEW;
   END; $$
LANGUAGE plpgsql;

CREATE TRIGGER on_loan_remove
  AFTER DELETE
  ON loan
  FOR EACH ROW
  EXECUTE PROCEDURE return_loan();

CREATE OR REPLACE FUNCTION stop_insertion() RETURNS TRIGGER AS $$
    BEGIN
        RAISE NOTICE 'You cannot bid for your own item!';
        RETURN NULL;
    END; $$
LANGUAGE plpgsql

CREATE TRIGGER on_bid_insert
    BEFORE INSERT
    ON bid 
    FOR EACH ROW
    WHEN (NEW.bidder_id = NEW.owner_id)
    EXECUTE PRODEDURE stop_insertion()
