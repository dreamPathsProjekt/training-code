# Helm3 Udemy Course

- [https://www.udemy.com/course/helm-3-from-scratch-to-advance-level](https://www.udemy.com/course/helm-3-from-scratch-to-advance-level)
- [Source Code](https://github.com/himanshusharma-git/helm)

## Helm3 Basics

- Create a chart boilerplate

```Shell
# From scratch
helm3 create application-1

# Create with custom helm starter

# Example
# First clone the starter in ~/.helm/starters or wherever $HELM_HOME is located.
helm3 create application-starter-1 --starter helm-starter-istio

# You can also install and use the starter plugin
helm plugin install https://github.com/salesforce/helm-starter.git
helm starter fetch https://github.com/salesforce/helm-starter-istio.git
helm3 create application-starter-1 --starter helm-starter-istio
```

> __Helm starters__ are used by the `helm create` command to customize the default chart. For example, an `Istio` starter can create `VirtualService` and `DestinationRule` objects, in addition to the standard `Service` and `Deployment` objects.

