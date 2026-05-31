const form = document.getElementById(
    "ticketForm"
)

form.addEventListener(
    "submit",

    async function(event){

        event.preventDefault()

        const data={

            customer_name:
            document.getElementById(
                "customer_name"
            ).value,

            customer_email:
            document.getElementById(
                "customer_email"
            ).value,

            subject:
            document.getElementById(
                "subject"
            ).value,

            description:
            document.getElementById(
                "description"
            ).value
        }

        const response=
        await fetch(

            "/tickets",

            {

                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify(
                    data
                )

            }

        )

        const result=
        await response.json()

                    document.getElementById(
            "result"
        ).className =

        "success"


        document.getElementById(
            "result"
        ).innerText =

        "Created Successfully: "

        + result.ticket_id



        setTimeout(

        ()=>{

        window.location.href="/"

        },

        1500

        )

    }

)