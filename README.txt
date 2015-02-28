galaxy simulator to do:

server/meta:
	set up software: "easy to install"
	implement logins/users
	set up workflow: 
		server accepts simulation inputs from users, writes to DB
		processors run the simulation jobs
		server publishes the results and notifies users
simulation code:
	extend simulation code to 3D
	add "restart" function
visualization/postprocessing:
	extend visualizer for non-GIF filetype (so the whole file doesn't have to fit in memory)
	modify visualizer for 3D-to-2D projection (see http://en.wikipedia.org/wiki/3D_projection )
