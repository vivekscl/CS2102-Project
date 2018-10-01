CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
	username varchar(128) UNIQUE NOT NULL,
	name varchar(128) NOT NULL,
	password_hash varchar(128) NOT NULL,
	phoneNo char(8) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS listing (
	listing_id SERIAL PRIMARY KEY,
	owner_id integer,
	description varchar(512),
	isAvailable varchar(5) NOT NULL,
    	FOREIGN KEY (owner_id) REFERENCES users(id),
	CHECK (isAvailable='TRUE' OR isAvailable='FALSE')
);

CREATE TABLE IF NOT EXISTS bid (
	bidder_id integer,
	listing_id integer,
	price numeric NOT NULL,
	FOREIGN KEY (bidder_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (listing_id) REFERENCES listing(listing_id) ON DELETE CASCADE,
	PRIMARY KEY (bidder_id, listing_id),
	CHECK (price >= 0)
);

CREATE TABLE IF NOT EXISTS loan (
	loan_id SERIAL PRIMARY KEY,
	bidder_id integer,
	listing_id integer,
	return_date date NOT NULL,
	borrow_date date NOT NULL,
	return_loc varchar(512) NOT NULL,
	pickup_loc varchar(512) NOT NULL,
FOREIGN KEY (bidder_id, listing_id) REFERENCES bid(bidder_id, listing_id),
	CHECK (return_date >= borrow_date)
);



CREATE TABLE IF NOT EXISTS tag (
	tag_id SERIAL PRIMARY KEY,
	name varchar(16) NOT NULL 
);

CREATE TABLE IF NOT EXISTS listing_tag (
	tag_id integer,
	listing_id integer,
	FOREIGN KEY (tag_id) REFERENCES tag(tag_id) ON DELETE CASCADE,
FOREIGN KEY (listing_id) REFERENCES listing(listing_id) ON DELETE CASCADE,
	PRIMARY KEY(tag_id, listing_id)
);
