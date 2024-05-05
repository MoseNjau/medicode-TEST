//select DOM elements:
var sendButton = document.getElementById('send')
var messageContent = document.getElementById('message_content')
var attachButton = document.getElementById('attach')

sendButton.onclick = (e)=>{
  e.preventDefault()
  let message = messageContent.value 
  console.log(message)
}

console.log('loaded')
