
async function loadTickets(){

const search =

document.getElementById(
"search"
).value


const status =

document.getElementById(
"status"
).value


const params =

new URLSearchParams()


if(search){

params.append(

"search",

search

)

}


if(status){

params.append(

"status",

status

)

}


const url =

`/tickets?${params.toString()}`


console.log(url)


const response =

await fetch(url)


const tickets =

await response.json()


const table =

document.getElementById(
"ticketTable"
)


table.innerHTML=""


if(tickets.length===0){

table.innerHTML=

`

<tr>

<td colspan="4">

No Tickets Found

</td>

</tr>

`

return

}


tickets.forEach(ticket=>{

table.innerHTML +=

`

<tr>

<td>

<a href="/ticket?id=${ticket.ticket_id}">

${ticket.ticket_id}

</a>

</td>

<td>

${ticket.customer_name}

</td>

<td>

${ticket.subject}

</td>

<td>

${ticket.status}

</td>

</tr>

`

})

}


loadTickets()



async function askBot(){

const input=

document.getElementById(
"chatInput"
)

const question=

input.value.trim()


if(!question){

return

}


const messages=

document.getElementById(
"chatMessages"
)


messages.innerHTML +=

`

<div class="user-msg">

🙂 ${question}

</div>

`


input.value=""


messages.innerHTML +=

`

<div class="bot-msg">

🤖 Thinking...

</div>

`


messages.scrollTop=

messages.scrollHeight


const response=

await fetch(

"/chat",

{

method:"POST",

headers:{

"Content-Type":

"application/json"

},

body:JSON.stringify({

question

})

}

)


const data=

await response.json()


const bots=

document.querySelectorAll(
".bot-msg"
)


bots[
bots.length-1
].innerHTML=

`🤖 ${data.answer}`


messages.scrollTop=

messages.scrollHeight

}