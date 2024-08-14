const express = require('express');
const router = express.Router();
require('dotenv').config();

router.post('/', async (req, res) => {
    try {
        const query = req.body.query;
        const response = req.body.response;
        const region = req.headers.region;
        if(!query || !region || !response) {
            return res.status(400).send('Query, Region or Response one of them is missing');
        }
        const connection = req.connections[region];
        if(!connection) {
            return res.status(400).send('Invalid region');
        }
        const Data = connection.model('Data', require('../models/data').schema);
        const newData = new Data({query: query, response: response});
        await newData.save();
        return res.status(200).json({ data: newData });
    } catch (error) {
        console.log(error);
        return res.status(400).send(error);
    }
});

module.exports = router;