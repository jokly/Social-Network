CREATE OR REPLACE FUNCTION get_comments(curr_post_id int)
RETURNS refcursor AS
$$
DECLARE
    _result CONSTANT refcursor := '_result';
BEGIN
	OPEN _result FOR 
    WITH RECURSIVE r AS (
        SELECT post.id, post.parent_post, post.text, 0 as level
        FROM post
        WHERE post.id = curr_post_id
        
        UNION
        
        SELECT post.id, post.parent_post, post.text, r.level + 1 as level
        FROM post
            JOIN r
            ON post.parent_post = r.id
    ) SELECT * FROM r;
    RETURN _result;
END
$$ LANGUAGE plpgsql;
