// client.js
const net = require('net');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const client = new net.Socket();

client.connect(9999, '10.220.8.248', () => {
    console.log('Connected to server');
    
    rl.on('line', (input) => {
        client.write(input);
    });
});

client.on('data', (data) => {
    console.log(`Received: ${data}`);
});

client.on('close', () => {
    console.log('Connection closed');
});