# Deployment

A production-ready example Docker stack with Crewlink and Impostor included.

1. Change variables in `stack.yml`
2. Change config in `impostor-config.json`
3. Deploy `stack.yml` using Docker Compose or as a Docker stack.

## Notes

When using Azure virtual network firewall, don't forget to add a role
assignment in Azure portal to the network security group for the app/service principal.
