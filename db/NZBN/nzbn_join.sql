select tenancy.id, nzbn, tenancy.caseperorgrespondent
from tenancy
inner join nzbn_directors_new bd ON trim(bd.last_name || ', ' || bd.first_name || ' ' || bd.middle_name) = tenancy.caseperorgrespondent
fetch first 10 rows only;