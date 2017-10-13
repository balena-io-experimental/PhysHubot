Flowdock = require('flowdock').Session
_ = require('lodash')
request = require('request')

flowdock = new Flowdock(process.env.FLOWDOCK_TOKEN)
flowdock.on('error', (error) ->
	console.log(error)
)
try
	flows = JSON.parse(process.env.FLOWDOCK_LISTEN_TO_FLOWS)
	users = JSON.parse(process.env.FLOWDOCK_LISTEN_TO_USERS)
	stream = flowdock.stream(flows)
	console.log(' * Connected to Flowdock.')
	console.log(flows)
	console.log(users)
	stream.on('message', (message) ->
		if message.event == 'message' and _.includes(users, message.user)
			request.post('http://localhost', {
				form: {
					text: message.content.replace(/\s+/gi, ' '),
				},
			})
	)
catch error
	console.log(error)
	console.log(' *** Probably a misconfiguration.')
	console.log(' *** Please set FLOWDOCK_LISTEN_TO_FLOWS and FLOWDOCK_LISTEN_TO_USERS.')
	flowdock.flows((err, flows) ->
		users = {}
		_.forEach(flows, (flow) ->
			console.log("#{flow.name} #{flow.id}")
			_.forEach(flow.users, (user) ->
				users[user.id] = user.nick
			)
		)
		_.forEach(users, (userNick, userId) ->
			console.log("#{userNick} #{userId}")
		)
	)
