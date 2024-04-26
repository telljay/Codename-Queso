const express = require('express');
const app = express();
const port = 3000;

app.use(express.urlencoded({extended : true}));

app.get('/', (req,res) => {
    res.sendFile('C:\\Users\\danie\\Desktop\\Coding Projects\\HTML\\Tutorial Level\\index.html');
});

app.post('/submit', (req,res)=>{
    const userInput = req.body.textInput;
    console.log('User Input: ', userInput);

    //Something cheesey soon

    res.send('Input received and processed.') //check to see if client got heard
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
})