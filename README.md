# Whitelink

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/mhvis/whitelink)](https://hub.docker.com/r/mhvis/whitelink)

A tool for restricting server access using an IP based whitelist.

People that want access to the server visit the web page of this tool where they enter the retrieved access code, after which their IP address is added to the firewall granting access to the service.

The purpose is for providing private Impostor and CrewLink server instances, with the following advantages:

* Low ping and high availability, works even when the public Among Us or CrewLink servers are down. (Ping depends on geographical location of the server.)
* No risk of leaking lobby codes, as streamer you can even set the lobby to public.
* No risk of leaking the CrewLink+Impostor server address.

## How does it work?

One-time set up:

1. The host shares the private code with the other players.
2. The others open this app in their browser and fill in the code to whitelist their IP.
   
After set up the whitelisted people can access CrewLink and Impostor.


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

## Credits

Great projects:

* [CrewLink](https://github.com/ottomated/CrewLink-server) by Ottomated
* [Impostor](https://github.com/Impostor/Impostor) by AeonLucid
