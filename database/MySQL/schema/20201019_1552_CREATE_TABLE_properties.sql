CREATE TABLE properties
(
	idProperty INT AUTO_INCREMENT,
    idAccount INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    rate DOUBLE NOT NULL,
    pax INT NOT NULL,
    rooms INT NOT NULL,
	beds INT NOT NULL,
    kitchen INT NOT NULL,
	bathrooms INT NOT NULL,
	garage INT NOT NULL,
    pool INT NOT NULL,
	pets BOOLEAN DEFAULT(FALSE),
	wifi BOOLEAN DEFAULT(FALSE),
    CONSTRAINT pk_properties_idProperty PRIMARY KEY(idProperty),
    CONSTRAINT fk_properties_idAccount FOREIGN KEY(idAccount) REFERENCES accounts(idAccount) ON UPDATE CASCADE ON DELETE CASCADE
);
