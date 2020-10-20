CREATE TABLE properties_photos
(
	idPropertyPhoto INT AUTO_INCREMENT,
    idProperty INT NOT NULL,
    photo BLOB NOT NULL,
	CONSTRAINT pk_properties_photos_idPropertyPhoto PRIMARY KEY(idPropertyPhoto),
	CONSTRAINT fk_properties_photos_idProperty FOREIGN KEY(idProperty) REFERENCES properties(idProperty) ON UPDATE CASCADE ON DELETE CASCADE
);