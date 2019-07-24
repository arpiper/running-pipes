# Set environment variables
export FLASK_ENV=development
export FLASK_APP=rungoals

df:
	flask run

dv:
	cd frontendrun && npm run serve	
