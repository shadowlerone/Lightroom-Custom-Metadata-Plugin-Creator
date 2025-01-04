function sanitize(string) {
	return string.replace(/[^A-z0-9]+/g, '_')
}

function to_id(string) {
	return sanitize(string.trim()).toLowerCase();
}

export {sanitize, to_id}