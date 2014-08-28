all:compiled.js
	
compiled.js:bootstrap.js  bootstrap.min.js  bootstrap-modal.js  jquery.cookie.js  jquery.js  md5.js mustache.js
	java -jar compiler.jar --js jquery.js   --js bootstrap.js --js bootstrap.min.js --js bootstrap-modal.js --js jquery.cookie.js --js md5.js --js mustache.js  --js_output_file compiled.js
	#--compilation_level ADVANCED_OPTIMIZATIONS 
