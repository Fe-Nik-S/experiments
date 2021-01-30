
const EXPRESS_MODULE = require('express');

const HOSTNAME = '127.0.0.1';
const PORT = 9000;

const app = EXPRESS_MODULE()
const HELLO_MESSAGE = "Hello, world!";


app.get('/', (req, resp) => {
    resp.send(HELLO_MESSAGE);
})

app.listen(PORT, () => {
   console.log(`Server listening on http://${HOSTNAME}:${PORT}`);
});
