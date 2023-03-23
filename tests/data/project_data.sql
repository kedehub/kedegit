select hexsha,author_name,added_lines,added_chars,deleted_lines,deleted_chars,commit_time,commit_time_utc_offset,c.repository_id, r.project_name, 'allianz' as team, 'eLando' as company
from commits c 
	join projectrepository r
		on c.repository_id = r.repository_id
			