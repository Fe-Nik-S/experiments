
const express = require('express');


const HOSTNAME = '127.0.0.1';
const PORT = 3000;


const app = express()
app.get('/', (req, res) => {
    res.send("Working...");
})

const server = app.listen(process.env.PORT || PORT, HOSTNAME, () => {
    console.log(`Server ready...Running at http://${HOSTNAME}:${PORT}`);
})
process.on('SIGTERM', () => {
    server.close(() => {
        console.log('Process terminated...');
    })
})
