const express = require('express');
const router = express.Router();
require('dotenv').config();

router.post('/', async (req, res) => {
    try {
        const query = req.body.query;
        const region = req.headers.region;
        if(!query || !region) {
            return res.status(400).send('Query and Region are required');
        }
        const connection = req.connections[region];
        if(!connection) {
            return res.status(400).send('Invalid region');
        }
        const Data = connection.model('Data', require('../models/data').schema);
        const data = await Data.findOne({ query: query });
        if(!data) {
            return res.status(404).send('Data does not exist');
        }
        if(data.isExpired()) {
            await data.deleteOne();
            return res.status(404).send('Data is expired');
        }
        await data.save();
        return res.status(200).json({ response: data.response });
    } catch (error) {
        console.log(error);
        return res.status(400).send(error);
    }
});

module.exports = router;