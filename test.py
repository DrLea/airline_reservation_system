import json
import sys
import qrcode
import webbrowser



with open('full_response.json') as f:
    dataframe = json.load(f)

def find(id):
    for ticket in dataframe['data']:
        if ticket['id'] == id:
            return ticket
    return {}

id = sys.argv[1]
ticket =   find(id)
qr = qrcode.make(id)
qr.save('qr.png')

html_doc = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket</title>
</head>
<body style="background-image: url(bgr.jpg); background-repeat: no-repeat; background-size:cover ;">
    <div style="width: 60%;">
        <div style="padding-top: 2rem; padding-left: 10%;">
<hr>
            <h1>{ticket['cityFrom']} --> {ticket['cityTo']}</h1>
            <h4>{ticket['local_departure'].split('.')[0]} --> {ticket['local_arrival'].split('.')[0]}</h4>
            From: <b>{ticket['flyFrom']}</b>
            To: <b>{ticket['flyTo']}</b>
<hr><hr>
            Name: <b>{sys.argv[2]}</b><br>
            Email: <b>{sys.argv[3]}</b><br>
<hr><hr><hr>
            Baglimit: <br>
            Hand: <i>{ticket['baglimit']['hand_weight']}Kg</i><br>
            Hold: <i>{ticket['baglimit']['hold_weight']}Kg</i><br>
<hr><hr><hr><hr>
            Airline: <i>{ticket['route'][0]['airline']}</i><br>
            Flight #: <i>{ticket['route'][0]['flight_no']}</i><br>
            <img src="qr.png" alt="id" style="width: 8rem; position:absolute; right: 1rem; bottom: 1rem;">

        </div>
    </div>
</body>
</html>
"""

with open('ticket.html', 'w') as f:
    f.write(html_doc)



webbrowser.open('ticket.html')