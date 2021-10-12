# Helm3 Udemy Course

- [https://www.udemy.com/course/helm-3-from-scratch-to-advance-level](https://www.udemy.com/course/helm-3-from-scratch-to-advance-level)
- [Source Code](https://github.com/himanshusharma-git/helm)
- [https://helm.sh/blog/migrate-from-helm-v2-to-helm-v3/](https://helm.sh/blog/migrate-from-helm-v2-to-helm-v3/)
- [https://banzaicloud.com/blog/helm3-the-good-the-bad-and-the-ugly/](https://banzaicloud.com/blog/helm3-the-good-the-bad-and-the-ugly/)
- [Helm 3 Hooks](https://helm.sh/docs/topics/charts_hooks/)
- [Helmsmann Declarative Releases tool](https://github.com/Praqma/helmsman)
- [https://github.com/cdwv/awesome-helm](https://github.com/cdwv/awesome-helm)
- [Helm Unittest](https://github.com/quintush/helm-unittest)
- [Helm Flow Control](https://helm.sh/docs/chart_template_guide/control_structures/)

## Helm3 Basics

- Show `env` to distinguish from Helm 2 folders (`~/.helm` no longer used)
- Older repos from Helm2 __still work__ with Helm3 - but no longer maintained (`DEPRECATED` flag)
  - `stable` - `helm repo add stable https://charts.helm.sh/stable`
  - `incubator` - `helm repo add incubator https://charts.helm.sh/incubator`

```Shell
# $USER is dreampaths
helm env
HELM_BIN="helm"
HELM_CACHE_HOME="/home/dreampaths/.cache/helm"
HELM_CONFIG_HOME="/home/dreampaths/.config/helm"
HELM_DATA_HOME="/home/dreampaths/.local/share/helm"
HELM_DEBUG="false"
HELM_KUBEAPISERVER=""
HELM_KUBEASGROUPS=""
HELM_KUBEASUSER=""
HELM_KUBECAFILE=""
HELM_KUBECONTEXT=""
HELM_KUBETOKEN=""
HELM_MAX_HISTORY="10"
HELM_NAMESPACE="default"
HELM_PLUGINS="/home/dreampaths/.local/share/helm/plugins"
HELM_REGISTRY_CONFIG="/home/dreampaths/.config/helm/registry.json"
HELM_REPOSITORY_CACHE="/home/dreampaths/.cache/helm/repository"
HELM_REPOSITORY_CONFIG="/home/dreampaths/.config/helm/repositories.yaml"
```

- Create a chart boilerplate

```Shell
# From scratch
helm3 create application-1

# Create with custom helm starter

# Example
# First clone the starter in $HELM_DATA_HOME/starters e.g. "/home/dreampaths/.local/share/helm/starters"
helm3 create application-starter-1 --starter helm-starter-istio

# You can also install and use the starter plugin
helm plugin install https://github.com/salesforce/helm-starter.git
helm starter fetch https://github.com/salesforce/helm-starter-istio.git

# See multiple starter charts
ll ~/.local/share/helm/starters/helm-starter-istio/

# Example choose mesh-service chart as starter - will also include Istio CRDs
helm create istio-app-1 --starter helm-starter-istio/mesh-service
```

> __Helm starters__ are used by the `helm create` command to customize the default chart. For example, an `Istio` starter can create `VirtualService` and `DestinationRule` objects, in addition to the standard `Service` and `Deployment` objects.

## Template categories

- `.Chart` gets values from `Chart.yaml`
- `.Values` gets values from `values.yaml`
- `{{ include "application-1.fullname" . }}` - Syntax: `{{ include $str $ctx }}` (chainable) include the named template with the given context. Micro templates are usually defined in `_helpers.tpl`
- `{{ .Release }}` - __Built-in__ release values. Attributes include:
  - `.Release.Name`: Name of the release
  - `.Release.Time`: Time release was executed
  - `.Release.Namespace`: Namespace into which release will be placed (if not overridden)
  - `.Release.Service`: The service that produced this release. Usually Tiller.
  - `.Release.IsUpgrade`: True if this is an upgrade
  - `.Release.IsInstall`: True if this is an install
  - `.Release.Revision`: The revision number

Folder/Files structure

- `templates` folder contains templates & helper files
  - `_` in template name is a convention to indicate that this file includes no K8s objects. Example: `_helpers.tpl`
- `charts` folder contains chart dependencies templates
- `NOTES.txt` Chart & application info returned to user

More detailed info: [https://helm.sh/docs/chart_template_guide/builtin_objects/](https://helm.sh/docs/chart_template_guide/builtin_objects/)

## Linting - Templating for error troubleshooting charts

```Shell
# Linting pass or fail
helm lint application-1/ --strict

==> Linting application-1/
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed

# Template render output to stdout
helm template NAME application-1/
# Example
helm template app-1 application-1/ --debug
# Generate name
helm template --generate-name application-1/
# Render templates to output folder application-1/charts/, using release name (app-1) as sub directory
helm template app-1 application-1/ --output-dir application-1/charts/ --release-name
```

## Named Template files .tpl - Access re-usable templates

- [https://helm.sh/docs/chart_template_guide/named_templates/](https://helm.sh/docs/chart_template_guide/named_templates/)
- Example: pass `application-1.labels` block to other templates.

```YAML
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "application-1.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "application-1.labels" -}}
helm.sh/chart: {{ include "application-1.chart" . }}
{{ include "application-1.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

- Re-use in multiple templates: `deployment.yaml`

```YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "application-1.fullname" . }}
  # Syntax {{- include <defined name> <context> }}
  labels:
    {{- include "application-1.labels" . | nindent 4 }}
```

## Packaging, Repositories & Chart Museum

- [Chart Museum](https://chartmuseum.com/)
- [https://github.com/helm/chartmuseum](https://github.com/helm/chartmuseum)
- [ChartMuseum helm chart](https://github.com/chartmuseum/charts/tree/main/src/chartmuseum)

### Install Chart Museum

```Shell
helm repo add chartmuseum https://chartmuseum.github.io/charts
helm repo update

helm search repo chartmuseum
NAME                    CHART VERSION APP VERSION DESCRIPTION
chartmuseum/chartmuseum 3.2.0         0.13.1      Host your own Helm Chart Repository

kubectl create namespace chartmuseum
# Install with default values, no persistence
helm install chartmuseum chartmuseum/chartmuseum --namespace chartmuseum --version 3.2.0

# Helm3 uninstall by default purges history, except when flag --keep-history is used.
helm uninstall --debug -n chartmuseum chartmuseum
# Debug to show resources deleted
uninstall.go:95: [debug] uninstall: Deleting chartmuseum
client.go:299: [debug] Starting delete for "chartmuseum" Service
client.go:299: [debug] Starting delete for "chartmuseum" Deployment
client.go:299: [debug] Starting delete for "chartmuseum" Secret
uninstall.go:144: [debug] purge requested for chartmuseum
release "chartmuseum" uninstalled
```

### Using Chart Museum to package and push helm charts

```Shell
# Port-forward pod & add local repository
kubectl -n chartmuseum port-forward chartmuseum-595fcbdfbf-9bn6k 8080:8080 &
helm repo add localrepo http://localhost:8080/
helm repo list

NAME        URL
chartmuseum https://chartmuseum.github.io/charts
localrepo   http://localhost:8080/

# Package application-1 chart & push
helm package application-1/
Successfully packaged chart and saved it to: /home/dreampaths/Documents/training-code/helm3/application-1-0.1.0.tgz

# Both methods need environment variable DISABLE_API=false in values.yaml of chartmuseum server.
curl --data-binary "@application-1-0.1.0.tgz" http://localhost:8080/api/charts

# Alternative, use cm-push plugin to publish chart without package command
helm plugin install https://github.com/chartmuseum/helm-push.git
helm plugin list

helm cm-push application-1/ localrepo

# Install from localrepo (generate release name)
helm install localrepo/application-1 --generate-name
```

### Pull Repo locally for inspection

```Shell
helm repo add localstack-charts https://localstack.github.io/helm-charts
helm repo update

helm search repo localstack-charts
NAME                          CHART VERSION APP VERSION DESCRIPTION
localstack-charts/localstack  0.3.4         latest      A fully functional local AWS cloud stack

# Pulls latest chart version to file localstack-0.3.4.tgz
helm pull localstack-charts/localstack
tar -xvzf localstack-0.3.4.tgz
localstack/Chart.yaml
localstack/Chart.lock
localstack/values.yaml
localstack/templates/NOTES.txt
localstack/templates/_helpers.tpl
localstack/templates/deployment.yaml
localstack/templates/ingress.yaml
localstack/templates/pvc.yaml
localstack/templates/service.yaml
localstack/templates/serviceaccount.yaml
localstack/templates/tests/test-connection.yaml
localstack/.helmignore
localstack/README.md
localstack/artifacthub-repo.yml
localstack/charts/common/Chart.yaml
localstack/charts/common/values.yaml
localstack/charts/common/templates/_affinities.tpl
localstack/charts/common/templates/_capabilities.tpl
localstack/charts/common/templates/_errors.tpl
localstack/charts/common/templates/_images.tpl
localstack/charts/common/templates/_ingress.tpl
localstack/charts/common/templates/_labels.tpl
localstack/charts/common/templates/_names.tpl
localstack/charts/common/templates/_secrets.tpl
localstack/charts/common/templates/_storage.tpl
localstack/charts/common/templates/_tplvalues.tpl
localstack/charts/common/templates/_utils.tpl
localstack/charts/common/templates/_warnings.tpl
localstack/charts/common/templates/validations/_cassandra.tpl
localstack/charts/common/templates/validations/_mariadb.tpl
localstack/charts/common/templates/validations/_mongodb.tpl
localstack/charts/common/templates/validations/_postgresql.tpl
localstack/charts/common/templates/validations/_redis.tpl
localstack/charts/common/templates/validations/_validations.tpl
localstack/charts/common/.helmignore
localstack/charts/common/README.md
```
