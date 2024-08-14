const { Schema, model } = require('mongoose');
require('dotenv').config();

const dataSchema = new Schema({
    query: String,
    response: String,
    appKey: String,
    timestamp: Date,
});

dataSchema.pre('save', function(next) {
    this.timestamp = new Date();
    next();
});

dataSchema.methods.isExpired = function() {
    const currentTime = new Date();
    const timeDifference = currentTime - this.timestamp;
    const cacheTimeout = process.env.CACHE_TIMEOUT_MS; // 2 minutes in milliseconds
    return timeDifference > cacheTimeout;
};

module.exports = model('Data', dataSchema);