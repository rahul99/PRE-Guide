// Load modules
const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const pythonShell = require('python-shell')

// Init App
const app = express()

// Load View Engine
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')

// Body Parser Middleware
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

// Set Public Folder
app.use(express.static(path.join(__dirname, 'public')))

// Home Route
app.get('/', function(req, res) {
	res.render('index')
})

// Recommend Route
app.post('/recommend', function(req, res) {

	console.log(req.body)

	// Prepare options to invoke twitter-scraper python script
	var options = {
		mode: 'text',
		pythonPath: 'C:/Users/alant/Anaconda3/python.exe',
		scriptPath: '../twitter-scraper/',
		args:
		[
			req.body.username,	// username
			20					// number of tweets
		]
	}

	// Retrieve tweets using twitter-scraper
	pythonShell.run('main.py', options, function(err, tweets) {
		if(err) {
			throw err
		} else {
			// Log tweets on console
			console.log(tweets)

			// Prepare options to invoke classifier python script
			options = {
				mode: 'text',
				pythonPath: 'C:/Users/alant/Anaconda3/python.exe',
				scriptPath: '../classifier',
				args:
				[
					tweets
				]
			}

			// Get recommendation using classifier
			pythonShell.run('main.py', options, function(err, recommendations) {
				if(err) {
					throw err
				} else {
					let jsonRec = JSON.parse(recommendations)
					console.log(jsonRec)

					// Render result on page
					res.render('index', {
						username: req.body.username
						// tweets: jsonRec.tweets[0]
					})
				}
			})
		}
	})
})

// Start server on port 3000
app.listen(3000, function() {
	console.log('Server started on port 3000...')
})
