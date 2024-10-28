# Dynatrace GitHubAction Exporter
<p float="left">
  <img src="images/opentelemetry-logo.png" alt="OpenTelemetry Logo" width="45" height="" style="background-color:white;">
  <img src="images/Dynatrace_Logo.png" alt="Dynatrace Logo" width="45" height="" style="background-color:white;">
</p>
A GitHub Action to export Workflow runs as OTel Traces, Metric and Logs to Dynatrace


## Monitoring Github Actions with Dynatrace
This action will allow you to monitor your Github Actions with Dynatrace.
This Action works as an exporter, that will create OpenTelemetry Traces and Spans for the steps within your GitHub Workflows.

These details and metrics can then be used to analyse the performance of your CI/CD workflows.


## How to

Configuring the Dynatrace OTel GitHub Action.

Before setting up the integration, you will need a [Dynatrace API Token](https://docs.dynatrace.com/docs/dynatrace-api/basics/dynatrace-api-authentication).
This will require the following permissions:
- openTelemetryTrace.ingest
- logs.ingest
- metrics.ingest (This has not been implemented yet so the permission is optional)

Also, refer to the Dynatrace Open Telemetry information page:
[Using OpenTelemetry with Dynatrace](https://docs.dynatrace.com/docs/get-started/opentelemetry)


1. Configure your Dynatrace API Token as a secret in your repository, and call it `DYNATRACE_OTEL_API_TOKEN`
2. Configure your Dynatrace Tenant ID (eg. abc12345) as a secret in your repository, and call it `DYNATRACE_TENANT_ID` (Not needed if using `OTEL_EXPORTER_OTEL_ENDPOINT` - See [Optional Configuration](##Optional-Configuration))
3. The exporter uses automatic token authentication by default, for this you need to ensure that `GITHUB_TOKEN` has at least read access to the action scope (see example [Here](Dynatrace_GitHubAction-Exporter.yaml.example?plain=1#L8)).

Create your workflow yaml, under .github/workflows, this can be named anything you like.
Refer to the [Example Workflow YML](Dynatrace_GitHubAction-Exporter.yaml.example).

By having the trigger as:
```
on:
  workflow_run:
    workflows: ['*']
    types: [completed]
```
This means it will run whenever any of your other workflows complete - which means you don't need to edit any existing workflows, just put the new yaml file alongside the others in your repository.

## Optional Configuration
**OTEL_EXPORTER_OTEL_ENDPOINT** - This can be used to override the Dynatrace SaaS specific endpoint

**HEADERS_OVERRIDE** - This can be used to override the default Headers (Authorization: Api-Token dtc.01......). Enter these in a commas separated, key=value format.
For example:
```
Authorization=Bearer 123456,AnotherHeader=Value
```

**GITHUB_DEBUG** - see [Troubleshooting](#Troubleshooting)

## Example

Traces are viewable in the Distributed Tracing app within Dynatrace. The service name will be your repository name:
![DsitrubutedTraces](images/DistributedTraces.png)

Each trace can be opened to show the steps in context:
![SingleTrace](images/SingleTrace.png)

Logs will be available through the Traces view, or the Logs application:
![Logs](images/Logs.png)

## Troubleshooting 

- Configure `GITHUB_DEBUG` as true in your workflow file

## Contributing

Please create an issue/PR as needed [Dynatrace GitHubAction Exporter](../../) ).

## License

Dynatrace GitHubAction Exporter is based on [gha-new-relic-exporter](https://github.com/newrelic-experimental/gha-new-relic-exporter/) and has been modified to use Protobuf over HTTP rather than GRPC, and to use the required Authorization header for Dynatrace. This wouldn't be possible (from me at least) without their hard work!

Dynatrace GitHubAction Exporter is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.

>Dynatrace GitHubAction Exporter also use source code from third-party libraries. You can find full details on which libraries are used and the terms under which they are licensed in the [third-party notices document](THIRDPARTYLICENSES).