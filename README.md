# Whitelink

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/mhvis/whitelink)](https://hub.docker.com/r/mhvis/whitelink)

A tool for restricting server access using an IP based whitelist.

People that want access to the server visit the web page of this tool where they enter the retrieved access code, after which their IP address is added to the firewall granting access to the service.

The original purpose is for providing private Impostor and Crewlink server instances, with the following benefits for streamers:

* Low ping and high availability, works even when the public Among Us or Crewlink servers are down.
* No risk of leaking lobby codes, you can even set the lobby to public.
* No risk of leaking the Crewlink+Impostor server address.

## How does it work?

One-time set up:

1. The host shares the private code with the other players.
2. The others open this app in their browser and fill in the code to whitelist their IP.
   
After set up the whitelisted people can access Crewlink and Impostor.

## Are you a streamer?

I will gladly set up a beefy CrewLink+Impostor server for you in a nearby cloud region for free!
DM me on Twitter or Discord or send a mail to _todo_!

## Demo

_TODO_



## Development

### Local installation

1. Create virtual environment
2. `pip install -r requirements.txt`
3. Set configuration environment variables, see `whitelink/settings.py`
4. `python manage.py runserver`

### Using Docker Compose

```shell
$ docker-compose build
$ docker-compose up
```


## Deployment

See `deploy/stack.yml` for a Docker stack which includes CrewLink, Impostor and HTTPS support.
