Create table data
(SELECT grid.id, grid.status, info.json_data 
	FROM jets_form.application_grid grid join jets_form.application_info info 
	WHERE grid.id = info.id
	)