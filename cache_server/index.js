const {connectDB, connections} = require('./database');
const express = require('express');
const cors = require('cors');
const getQuery = require('./routes/getQuery');
const postQuery = require('./routes/postQuery');
require('dotenv').config();

connectDB();

const app = express();
const server = require('http').createServer(app);

app.use(express.json());
app.use(cors());
app.use('/getQuery', (req, res, next) => {
    req.connections = connections;
    next();
}, getQuery); 
app.use('/postQuery', (req, res, next) => {
    req.connections = connections;
    next();
},postQuery);

const PORT = process.env.SERVER_PORT;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});