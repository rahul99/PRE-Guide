// Load modules
const express = require('express')
const path = require('path')
const bodyParser = require('body-parser')

// Init App
const app = express()

// Load View Engine
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'pug')

// Body Parser Middleware
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

// Home Route
app.get('/', function(req, res) {
	res.render('index')
})

// Recommend Route
app.post('/recommend', function(req, res) {
	console.log(req.body)

	res.render('index', {
		username: req.body.username,
		tweets: 'Hello World!'
	})
})

// Start server on port 3000
app.listen(3000, function() {
	console.log('Server started on port 3000...')
})
