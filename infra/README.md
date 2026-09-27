# Infrastructure

The environment this application runs in, described as code.

Nothing here is created by hand. If you find yourself running `docker run` to
fix something, stop — change the configuration and re-apply instead. A server
someone fixed by hand is a server nobody can rebuild.

## What it creates

- A Docker network, so the application can reach the database by name
- A PostgreSQL container with a persistent volume and a health check
- One or more application containers, published on sequential host ports

## Before you start

You need the container runtime working (Week 1 checklist) and your application
image available — either published by your Week 5 pipeline, or built locally
with the same tag.

Set the database password from your shell. It has no default, on purpose:

```
export TF_VAR_db_password="$(openssl rand -base64 24)"
```

## Running it

```
cd infra
terraform init

terraform plan  -var-file=envs/staging.tfvars -var app_image=<your image>
terraform apply -var-file=envs/staging.tfvars -var app_image=<your image>
```

The application is then at http://localhost:8081.

To tear it down:

```
terraform destroy -var-file=envs/staging.tfvars -var app_image=<your image>
```

## Two environments, one configuration

```
terraform apply -var-file=envs/production.tfvars -var app_image=<your image>
```

Production runs two instances with more memory. Note what did **not** change:
`main.tf` is identical for both. If you ever have to edit `main.tf` to deploy
somewhere else, the configuration is not parameterised properly.

## Seeing drift

This is the exercise that matters. Apply the configuration, then break it by
hand:

```
docker rm -f northgate-staging-app-1
terraform plan -var-file=envs/staging.tfvars -var app_image=<your image>
```

Terraform compares what it recorded in state against what is actually running,
finds the container missing, and proposes to recreate it. `terraform apply`
puts it back.

That gap between what was recorded and what is real is **drift**. In an
organisation like the one in your case study, drift is what makes a test
environment stop resembling production, one manual fix at a time, until
"it passed testing" stops meaning anything.

## Why the state file is gitignored

`terraform.tfstate` contains every value Terraform manages — including the
database password, in plain text. Committing it is the same class of mistake
as committing a credential in Week 6, and it is easy to make because state
looks like a build artefact rather than a secret.

The lock file, `.terraform.lock.hcl`, **is** committed. It pins provider
checksums so everyone gets the same provider version.

## Structure

```
infra/
  versions.tf              provider and version pinning
  variables.tf             every input, with validation
  main.tf                  network, database, and the module call
  outputs.tf               what you get back after an apply
  envs/staging.tfvars      per-environment values
  envs/production.tfvars
  modules/app_service/     reusable "run N copies of this image"
```

The module exists to show reuse. It is small on purpose — this is the shape
that grows into an internal platform when an organisation has fifty services
instead of one.
