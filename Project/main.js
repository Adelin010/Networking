/**
 * ('10.220.8.248', 9999) information for connection
 */

import * as net from 'net'
// dependency for std::io as in python
import PromptSync  from 'prompt-sync'

const input = PromptSync()

const option = {
    port: 9999,
    host: '10.220.8.248'
}

const client = net.createConnection(option, () => {
    console.log("client connected...")
})

client.on('data', (data) => {
    // Display what you have to display 
    console.log(data.toString())
   
    // get the message
    let message = input()
    console.log(message)
    client.write(message)

    if(message === "/quit")
        client.end()

})