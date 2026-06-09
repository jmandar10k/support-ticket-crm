
document.getElementById(

"welcomeUser"

).innerText=

`Welcome, ${localStorage.getItem("name")}`


function handleUnauthorized(

response

){

if(

response.status===401

){

localStorage.clear()

window.location.href=

"/login-page"

return true

}

return false

}


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


const response =

await fetch(

url,

{

headers:{

Authorization:

`Bearer ${localStorage.getItem("token")}`

}

}

)


if(

handleUnauthorized(

response

)

){

return

}


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


async function syncEmails(){

const btn =

document.getElementById(
"syncBtn"
)


btn.disabled=true

btn.innerText=

"Syncing..."


try{

const response=

await fetch(

"/sync-emails",

{

method:"POST",

headers:{

Authorization:

`Bearer ${localStorage.getItem("token")}`

}

}

)


if(

handleUnauthorized(

response

)

){

return

}


if(

!response.ok

){

throw new Error(

"Backend Error"

)

}


const data=

await response.json()


alert(

`Email Sync Complete

Imported:

${data.tickets_created}

Skipped Existing:

${data.skipped}

Processed:

${data.processed}`

)


loadTickets()

}

catch(error){

console.log(
error
)

alert(

"Email Sync Failed"

)

}

finally{

btn.disabled=false

btn.innerText=

"Sync Emails"

}

}


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

"application/json",

Authorization:

`Bearer ${localStorage.getItem("token")}`

},

body:JSON.stringify({

question

})

}

)


if(

handleUnauthorized(

response

)

){

return

}


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


function logout(){

localStorage.clear()

window.location.href=

"/login-page"

}
