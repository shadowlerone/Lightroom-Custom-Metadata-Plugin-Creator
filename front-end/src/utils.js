function sanitize(string) {
	return string.replace(/\W+/g, ' ').trim().replace(/\s/g,'_')
}

function to_id(string) {
	return sanitize(string.trim()).toLowerCase();
}

export {sanitize, to_id}