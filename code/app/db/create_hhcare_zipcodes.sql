-- CREATE EXTENSION aws_s3 CASCADE;

DROP TABLE IF EXISTS hhcare_zipcodes;

CREATE TABLE hhcare_zipcodes (
	state CHAR(2) NOT NULL,
	cms_certification_number INT NOT NULL,
	zip_code INT NOT NULL,
	PRIMARY KEY (cms_certification_number, zip_code)
);

SELECT aws_s3.table_import_from_s3(
	'hhcare_zipcodes', 'state,cms_certification_number,zip_code',
	'(FORMAT csv, HEADER true)',
	aws_commons.create_s3_uri('haoma-bucket','HH_Zip_Oct2020.csv','us-west-2')
);