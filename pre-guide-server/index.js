// Load modules
const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')
const pythonShell = require('python-shell')
const exec = require('node-ssh-exec')

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
			10					// number of tweets
		]
	}

	// Retrieve tweets using twitter-scraper
	pythonShell.run('main.py', options, function(err, tweets) {
		if(err) {
			throw err
		} else {
			// // Log tweets on console
			let jsonTweets = JSON.parse(tweets)
			console.log(jsonTweets)
			// console.log(JSON.stringify(tweets))

			// SSH
			var config = {
			        host: 'next-gpu4.d2.comp.nus.edu.sg',
			        username: 'rahul',
			        password: '123@nus'
			    },
			    // command = 'python3 ./pre_guide/tweet_topic_model.py ' + JSON.stringify(tweets)		    
			    command = 'python3 ./pre_guide/tweet.py ' + JSON.stringify(tweets)

			// Render result on page
			// res.render('index', {
			// 	username: 'NUSComputing',
			// 	tweets: jsonTweets.tweets
			// })
			 
			exec(config, command, function (error, response) {
			    if (error) {
			        throw error
			    }

			    // Trim response
			    response = response.replace(/NaN/g, '0')

			    // Parse result
			    let jsonResult = JSON.parse(response)
			    // console.log(jsonResult)
			    console.log(jsonResult['books'])

			    // Extra logs
			    // console.log(typeof(jsonResult['tags']))
			    // console.log(JSON.stringify(jsonResult['tags']))
			    // console.log(typeof(JSON.stringify(jsonResult['tags'])))
			    
			    // Get keys
			    var keys = []
			    jsonResult['books'].forEach(function(item) {
			    	keys.push(Object.keys(item['original_title'])[0]);
			    });
			    console.log(keys)

			    // Render result on page
				res.render('index', {
					username: req.body.username,
					tweets: jsonTweets.tweets,
					keys: keys,
					tags: JSON.stringify(jsonResult['tags']).replace(/\[/g, '').replace(/\]/g, '').replace(/"/g, '').replace(/,/g, ', '),
					books: jsonResult['books']
				})
			})
		}
	})
})

// Start server on port 3000
app.listen(3000, function() {
	console.log('Server started on port 3000...')
})
