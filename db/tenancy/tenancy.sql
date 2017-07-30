create table tenancy
(	 id varchar(100) primary key
	,applicationId  text
	,applicationNumber  text 
	,casePerOrg  text
    ,casePerOrgApplicant text
    ,casePerOrgFirstName text
    ,casePerOrgLastName text 
    ,casePerOrgOrganisationName text
    ,casePerOrgRespondent text
    ,decisionDateIndex text
    ,jurisdictionName text
	,jurisdictionCode text
    ,orderDetailCsv text
    ,orderDetailJson text
    ,orderDetailXml text
    ,publishedDate text
	,tenancyAddress text
    ,tenancyCityTown text
    ,tenancyStreetName text
    ,tenancyStreetNumber text
    ,tenancyStreetType text
	,tenancySuburb  text 
	,tenancyUnitIdentifier_s text
);

create table trademe_tenancy
(listing_id int
,tenancy_id varchar(100)
,primary key (listing_id, tenancy_id)
);



DROP FUNCTION IF EXISTS geomatch_tenancy_score(TRADEME, tenancy);
CREATE FUNCTION geomatch_tenancy_score(listing TRADEME, tenancy TENANCY)
RETURNS INT
LANGUAGE plpgsql AS $$
DECLARE
    score INT := 0; 
BEGIN
    -- +40 pts for exact match of unit
    -- +20 pts if neither address has a unit
    IF (listing.unit IS NULL AND tenancyUnitIdentifier_s IS NULL) THEN 
    	score := score + 20;
    ELSIF (listing.unit = tenancyUnitIdentifier_s) THEN 
    	score := score + 40;
    END IF;

    -- +40 pts for exact match of house numbers
    IF (listing.house = tenancy.tenancyStreetNumber) THEN
        score := score + 40;
    END IF;

    -- +10 pts for suburb match
    IF (listing.suburb = tenancy.tenancySuburb) THEN 
    	score := score + 10; 
    END IF;

    RETURN score;
END;
$$;

INSERT INTO trademe_tenancy (listing_id, tenancy_id)
WITH matches AS (
    -- Join to addresses using street name, then score each candidate
    SELECT listing_id, id, geomatch_tenancy_score(tm, t) AS score,
           row_number() OVER (PARTITION BY listing_id ORDER BY geomatch_tenancy_score(tm, t) DESC) AS ranking
    FROM trademe tm 
    JOIN tenancy t
    ON (canonical_street(tm.street) = t.tenancystreetname AND
        house_digits(tm.house) = house_digits(t.tenancystreetnumber))
)
-- Use a window query to select the best-ranked address point for each listing
SELECT listing_id, id
FROM matches
WHERE ranking = 1
;
