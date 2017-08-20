# Fusion maps

Fun project to test Django & google fusion tables.
This is a single page application that shows a maps and a list of addresses.
Clicking on the addresses will add a new marker on the map and will
save the new location both on django and on a google fusion table.

## Setup

To start using this, you first need to:
1. edit the `settings.py` file to setup your google maps api key.
2. create a service account for the google api dashboard:
<https://console.developers.google.com/apis/credentials/serviceaccountkey> and place the downloaded json file in the root folder of this
project, in a file named `client_secrets.json`
3. create a new fusion table <https://fusiontables.google.com> and share it with the newly created service account.
4. prepare the env and run it:
```
virtualenv .ve
source .ve/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

Then open up your browser and go to <http://localhost:8000/fusionmaps>
