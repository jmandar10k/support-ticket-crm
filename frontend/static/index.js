
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