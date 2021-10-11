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
helm3 create application-starter-1 --starter helm-starter-istio
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
