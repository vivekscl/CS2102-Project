CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
	username VARCHAR(128) UNIQUE NOT NULL,
	name VARCHAR(128) NOT NULL,
  password_hash VARCHAR(128) NOT NULL,
	phone_no CHAR(8)
);

CREATE TABLE IF NOT EXISTS listing (
	listing_id SERIAL PRIMARY KEY,
	owner_id INTEGER,
	name VARCHAR(128) NOT NULL,
	description VARCHAR(512),
	is_available VARCHAR(5) NOT NULL,
    	FOREIGN KEY (owner_id) REFERENCES users(user_id),
	CHECK (is_available='TRUE' OR is_available='FALSE')
);

CREATE TABLE IF NOT EXISTS bid (
	bidder_id INTEGER,
	listing_id INTEGER,
	bid_date TIMESTAMP,
	price NUMERIC NOT NULL,
	FOREIGN KEY (bidder_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY (listing_id) REFERENCES listing(listing_id) ON DELETE CASCADE,
	PRIMARY KEY (bidder_id, listing_id, bid_date),
	CHECK (price >= 0)
);

CREATE TABLE IF NOT EXISTS loan (
	bidder_id INTEGER,
	listing_id INTEGER,
	bid_date TIMESTAMP,
	borrow_date TIMESTAMP,
	return_date TIMESTAMP NOT NULL,
	return_loc VARCHAR(512) NOT NULL,
	pickup_loc VARCHAR(512) NOT NULL,
  FOREIGN KEY (bidder_id, listing_id, bid_date) REFERENCES bid(bidder_id, listing_id, bid_date),
  PRIMARY KEY (bidder_id, listing_id, bid_date, borrow_date),
	CHECK (return_date >= borrow_date)
);
CREATE TABLE IF NOT EXISTS tag (
	tag_id SERIAL PRIMARY KEY,
	name VARCHAR(16) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS listing_tag (
	tag_id INTEGER,
	listing_id INTEGER,
	FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE,
  FOREIGN KEY (listing_id) REFERENCES listing(listing_id) ON DELETE CASCADE,
	PRIMARY KEY(tag_id, listing_id)
);
