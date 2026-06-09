
const params = new URLSearchParams(
window.location.search
)

const ticketId =
params.get("id")


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


async function loadTicket(){

const response=

await fetch(

`/tickets/${ticketId}`,

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


const data=

await response.json()


document.getElementById(
"status"
).value=

data.status


document.getElementById(
"details"
).innerHTML=

`

<div class="card">

<h2>

${data.ticket_id}

</h2>

<p>

<b>Status:</b>

${data.status}

</p>

</div>


<div class="card">

<h3>

Customer Information

</h3>

<p>

<b>Name:</b>

${data.customer_name}

</p>

<p>

<b>Email:</b>

${data.customer_email}

</p>

</div>


<div class="card">

<h3>

Issue Information

</h3>

<p>

<b>Subject:</b>

${data.subject}

</p>

<p>

<b>Description:</b>

${data.description}

</p>

</div>


<div class="card">

<h3>

Status Timeline

</h3>

<div class="timeline">

${

(data.history || []).length

?

data.history.map(

h=>`

<div class="timeline-item">

<div>

${h.old_status}

→

${h.new_status}

</div>

<small>

${new Date(

h.changed_at

).toLocaleString()}

</small>

</div>

`

).join("")

:

"<p>No Status Changes Yet</p>"

}

</div>

</div>


<div class="card">

<h3>

Notes History

</h3>

<ul>

${

(data.notes || []).length

?

data.notes.map(

n=>`

<li>

${n.note_text}

</li>

`

).join("")

:

"<p>No Notes Added</p>"

}

</ul>

</div>

`

}


async function updateTicket(){

const status=

document.getElementById(
"status"
).value


const notes=

document.getElementById(
"notes"
).value


const response=

await fetch(

`/tickets/${ticketId}`,

{

method:"PUT",

headers:{

"Content-Type":

"application/json",

Authorization:

`Bearer ${localStorage.getItem("token")}`

},

body:JSON.stringify({

status,

notes

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


if(response.ok){

document.getElementById(
"message"
).className=

"success"


document.getElementById(
"message"
).innerText=

"Updated Successfully"


document.getElementById(
"notes"
).value=""


await loadTicket()

}

else{

document.getElementById(
"message"
).innerText=

"Update Failed"

}

}


loadTicket()
