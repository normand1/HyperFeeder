const {postEpisode} = require('./index');

const arg = process.argv[2]; // Get command line argument
console.log(arg);
postEpisode(arg);