const express = require('express');
const multer = require('multer');
const app = express()
const eventEmitter = require('events');
const messageQueueEvent = new eventEmitter();

const ws = require('ws');

const wsServer = new ws.Server({
    noServer: true
});
const clients = new Set();

let messageQueue = [];

let firstIdAssigned = false;
let secondIdAssigned = false;


app.get("/assign-id", (req, res) => {
    if (!firstIdAssigned) {
        res.end("1");
        firstIdAssigned = true;
    } else if (!secondIdAssigned) {
        res.end("2");
        secondIdAssigned = true;
    }
});

app.get('/', (req, res) => res.sendFile('views/index.html', {
    root: __dirname
}));

app.get("/polling/messages", (req, res) => {
    if (messageQueue.length == 0)
        res.end();
    else {
        let tempMessages = []
        for (let message of messageQueue) {
            if (message.id != req.query.id) {
                tempMessages.push(message.content);

                const index = messageQueue.indexOf(message);
                if (index > -1) { // only splice array when item is found
                    messageQueue.splice(index, 1); // 2nd parameter means remove one item only
                }
            }
        }
        res.json({
            "messages": tempMessages
        });
    }
});
app.post("/polling/messages", multer().none(), (req, res) => {
    let messageSent = false;
    for (let client of clients) {
        if (client.client_id != req.body.id) {
            console.log("Sending via web socket")
            client.send(JSON.stringify({
                "id": req.body.id,
                "content": req.body.message
            }))
            messageSent = true;
            break;
        }
    }
    if (!messageSent) {
        messageQueue.push({
            "id": req.body.id,
            "content": req.body.message
        });
        console.log(messageQueue);
        res.end();
        messageQueueEvent.emit("message_receive");
    }

});


app.get("/long-polling/messages", multer().none(), (req, res) => {
    let tempMessages = []
    for (let message of messageQueue) {
        if (message.id != req.query.id) {
            tempMessages.push(message.content);

            const index = messageQueue.indexOf(message);
            if (index > -1) { // only splice array when item is found
                messageQueue.splice(index, 1); // 2nd parameter means remove one item only
            }
        }
    }
    if (tempMessages.length > 0) {
        res.json({
            "messages": tempMessages
        });
    }

    const responseHandler = () => {
        let tempMessages = []
        for (let message of messageQueue) {
            if (message.id != req.query.id) {
                tempMessages.push(message.content);

                const index = messageQueue.indexOf(message);
                if (index > -1) { // only splice array when item is found
                    messageQueue.splice(index, 1); // 2nd parameter means remove one item only
                }
            }
        }

        res.json({
            "messages": tempMessages
        });
        messageQueueEvent.removeListener("message_receive", responseHandler);
    }
    messageQueueEvent.on("message_receive", responseHandler);
});
app.post("/long-polling/messages", multer().none(), (req, res) => {
    let messageSent = false;
    for (let client of clients) {
        if (client.client_id != req.body.id) {
            console.log("Sending via web socket")
            client.send(JSON.stringify({
                "id": req.body.id,
                "content": req.body.message
            }))
            messageSent = true;
            break;
        }
    }
    if (!messageSent) {
        messageQueue.push({
            "id": req.body.id,
            "content": req.body.message
        });
        messageQueueEvent.emit("message_receive");
    }
    res.end();
});


wsServer.on('connection', (socket, req) => {
    clients.add(socket)
    const urlParams = new URLSearchParams(req.url);
    const id = urlParams.get('/?id');
    socket.client_id = id;

    for (let message of messageQueue) {
        if (message.id != id) {
            console.log(JSON.stringify(message))
            socket.send(JSON.stringify(message));
/*
            const index = messageQueue.indexOf(message);
            if (index > -1) { // only splice array when item is found
                messageQueue.splice(index, 1); // 2nd parameter means remove one item only
            }*/
        }
    }

    socket.on('message', message => {
        message = JSON.parse(message.toString())
        console.log("On message" + JSON.stringify(message))
        let messageSent = false;
        for (let client of clients) {
            if (client && client != socket) {
                client.send(JSON.stringify(message));
                messageSent = true;
            }
        }
        if (!messageSent) {
            messageQueue.push({
                "content": message.content,
                "id": id
            })
            messageQueueEvent.emit("message_receive");
        }
    });
    socket.on('close', function () {
        clients.delete(socket)
    })
})


// Start the Express server
const server = app.listen(3000, () => console.log('Server running on port 3000!'))
server.on('upgrade', (request, socket, head) => {
    wsServer.handleUpgrade(request, socket, head, socket => {
        wsServer.emit('connection', socket, request);
    })
})