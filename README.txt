Stack Search 
=========================

StackOverflow Search Clustering - NLP Final Project

Project Team Members: Sonali Sharma, Shubham Goel, Priya Iyer


 There are a number of search engines available today. When users type in a query to search for something over internet, they are often overwhelmed with the a large amount of results. It often becomes difficult browse through this list and fetch the most relevant item. Since the aim of our project was to improve user search using NLP techniques, we decided to implement an algorithm that would improve use search using NLP techniques and provide a mechanism to categorise search results into relevant categories, thereby making it easy for the end user to navigate to the category on interest and look for results within that category. We decided to implement Findex algorithm in this project. Findex is a text categorization algorithm that provides an overview of search results as categories where categories are made up of most frequent words and phrases in the resulting document set.  The algorithm is based on the assumption that the most frequently used word/phrases in a set of documents capture major topics very well. We used the stackoverflow data to implement the algorithm.
 
 
 Folder Structure:
 nlp_sentence_clustering
 	README.txt
	/stackOverflow
		/Frontend
			mywebsite.py [contains the server side script]
			
			processing.py [contains the logic to fetch search results]
			
			/templates
				index.html [landing page html content]
				layout.html [landing page parent html]
			
			/static
				[static css, img and js files for html rendering]
			
			models.py [defining the database models]
			
			insert_tables.py [code that creates the database tables from the models defined in models.py]
			
			tutorial.db [sqlite3 database holding the stackOVerflow data]
			
		insert_clean_so_data.py [inserts clean data to the database]
		ir_dcs_gla_ac_uk_stop_words.txt  [stop words list]
		

Requirements:
Python
sqlite3
Flask
nltk python package

Instructions to run and use the code:
1. Clone the repository from https://github.com/sonalisharma/nlp_sentence_clustering
2. Goto folder stackOverFlow/Frontend/
3. Open link http://people.ischool.berkeley.edu/~sonali.sharma/nlp/stackOverFlow/Frontend/ and download database tutorial.db
4. On the terminal, go to : /nlp_sentence_clustering/stackOverflow/Frontend/ and run ‘python mywebsite.py’
5. Go to http://localhost:5000 and enter your query to view the results.
6. On the console, you will be able to see the POS tags of your categories
