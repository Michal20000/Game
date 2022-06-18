INSERT INTO matches
(
	id,
	host_id,
	guest_id,
	host_image,
	guest_image,
	host_rating,
	guest_rating,
	host_change,
	guest_change,
	match_date

)
VALUES
(
	?,
	?,
	?,
	?,
	?,
	?,
	?,
	?,
	?,
	?

);
