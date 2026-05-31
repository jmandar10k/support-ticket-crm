async function loadTickets(){

const search=
document.getElementById(
"search"
).value

const status=
document.getElementById(
"status"
).value

let url=
"http://127.0.0.1:8000/tickets?"

if(search){

url+=`search=${search}&`

}

if(status){

url+=`status=${status}`

}

const response=
await fetch(url)

const tickets=
await response.json()

const table=
document.getElementById(
"ticketTable"
)

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

table.innerHTML +=`

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

<span class="status">

${ticket.status}

</span>

</td>

</tr>

`

})

}

loadTickets()