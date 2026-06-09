
import re

def clean_email_body(text):

    if not text:

        return ""


    text=text.replace(

        "\r",

        ""

    )


    stop_patterns=[

        r"Regards[, ]*",

        r"Best regards[, ]*",

        r"Thanks[, ]*",

        r"Thank you[, ]*",

        r"Sent from my.*",

        r"On .* wrote:",

        r"From:.*",

        r"-----Original Message-----",

        r"Forwarded message",

        r"Get Outlook for.*",

        r"Sent from Gmail.*"

    ]


    lines=text.split("\n")


    cleaned=[]


    for line in lines:


        should_stop=False


        for pattern in stop_patterns:


            if re.search(

                pattern,

                line,

                re.IGNORECASE

            ):

                should_stop=True

                break


        if should_stop:

            break


        cleaned.append(

            line

        )


    result="\n".join(

        cleaned

    )


    result=re.sub(

        r"\n\s*\n+",

        "\n\n",

        result

    )


    return result.strip()
