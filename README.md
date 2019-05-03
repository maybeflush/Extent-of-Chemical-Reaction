# Extent-of-Chemical-Reaction
Building a python standalone.app

	1. With a given reaction ("my_file.json"), the goal is to build graph (evolution of matter) and show the final amount of matters values
	2. In the meantime, it builds a data file ("chem.json") with name,formula of species
	3. my_file.json structure:  
	       >{"1":{
	       >   "Formule":"CH4",
	       >   "Type":"R",
	       >   "Coeff":1,
	       >   "n":1e-5},
	       >     "2":{
	       >    etc...}
	       >}
		   => "1","2"...  the id of the specie
		   => then you enter the formula as describe in chempy 
		   => "R" or "P" stands for Reactif & Produit 
		   => then the stoechiometric ratio as integer
		   => finally the inital amount of substance and so on
	   
	4. Datas.json, Datas1.json are two examples
	5. Setup.py to build a standalone app on macos
	6. chem.json is the "db"
