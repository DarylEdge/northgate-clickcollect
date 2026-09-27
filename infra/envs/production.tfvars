# Production. Two instances and more memory.
#
# Nothing in main.tf changes between environments. If you had to edit main.tf
# to produce this, the configuration is not parameterised properly.

environment        = "production"
app_host_port      = 8091
app_instance_count = 2
app_memory_mb      = 512
db_memory_mb       = 512
