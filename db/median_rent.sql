drop table area_unit;

create table area_unit (
sau int primary key
,name text
,extra text
,extra2 text
,extra3 text);

grant all privileges on area_unit to steven

CREATE TABLE median_rent
(SAU int
,Property_Type text
,Bedrooms text
,"1993-03-01" text
,"1993-06-01" text
,"1993-09-01" text
,"1993-12-01" text
,"1994-03-01" text
,"1994-06-01" text
,"1994-09-01" text
,"1994-12-01" text
,"1995-03-01" text
,"1995-06-01" text
,"1995-09-01" text
,"1995-12-01" text
,"1996-03-01" text
,"1996-06-01" text
,"1996-09-01" text
,"1996-12-01" text
,"1997-03-01" text
,"1997-06-01" text
,"1997-09-01" text
,"1997-12-01" text
,"1998-03-01" text
,"1998-06-01" text
,"1998-09-01" text
,"1998-12-01" text
,"1999-03-01" text
,"1999-06-01" text
,"1999-09-01" text
,"1999-12-01" text
,"2000-03-01" text
,"2000-06-01" text
,"2000-09-01" text
,"2000-12-01" text
,"2001-03-01" text
,"2001-06-01" text
,"2001-09-01" text
,"2001-12-01" text
,"2002-03-01" text
,"2002-06-01" text
,"2002-09-01" text
,"2002-12-01" text
,"2003-03-01" text
,"2003-06-01" text
,"2003-09-01" text
,"2003-12-01" text
,"2004-03-01" text
,"2004-06-01" text
,"2004-09-01" text
,"2004-12-01" text
,"2005-03-01" text
,"2005-06-01" text
,"2005-09-01" text
,"2005-12-01" text
,"2006-03-01" text
,"2006-06-01" text
,"2006-09-01" text
,"2006-12-01" text
,"2007-03-01" text
,"2007-06-01" text
,"2007-09-01" text
,"2007-12-01" text
,"2008-03-01" text
,"2008-06-01" text
,"2008-09-01" text
,"2008-12-01" text
,"2009-03-01" text
,"2009-06-01" text
,"2009-09-01" text
,"2009-12-01" text
,"2010-03-01" text
,"2010-06-01" text
,"2010-09-01" text
,"2010-12-01" text
,"2011-03-01" text
,"2011-06-01" text
,"2011-09-01" text
,"2011-12-01" text
,"2012-03-01" text
,"2012-06-01" text
,"2012-09-01" text
,"2012-12-01" text
,"2013-03-01" text
,"2013-06-01" text
,"2013-09-01" text
,"2013-12-01" text
,"2014-03-01" text
,"2014-06-01" text
,"2014-09-01" text
,"2014-12-01" text
,"2015-03-01" text
,"2015-06-01" text
,"2015-09-01" text
,"2015-12-01" text
,"2016-03-01" text
,"2016-06-01" text
,"2016-09-01" text
,"2016-12-01" text
,"2017-03-01" text
,"2017-06-01" text
);


select trademe.*
, coalesce(CASE median_rent."2017-06-01" WHEN 'NA' THEN NULL ELSE median_rent."2017-06-01" END
	,CASE median_rent."2017-03-01" WHEN 'NA' THEN NULL ELSE median_rent."2017-06-01" END
	,CASE median_rent."2016-12-01" WHEN 'NA' THEN NULL ELSE median_rent."2017-06-01" END) as median
from trademe
left join area_unit on trademe.suburb = area_unit.name
left join median_rent on median_rent.sau = area_unit.sau and trademe.bedrooms = median_rent.bedrooms
where property_type = 'Property Type Total';
