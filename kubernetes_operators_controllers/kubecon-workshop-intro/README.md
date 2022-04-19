# Kubecon Workshop: Zero to Operator in 90 Minutes

## Initialize

```Shell
# Fork git@github.com:DirectXMan12/kubebuilder-workshops.git
git clone git@github.com:dreamPathsProjekt/kubebuilder-workshops.git
cd kubebuilder-workshops/
git checkout start
```

## Scaffolding

```Shell
# Go modules
go mod init github.com/dreamPathsProjekt/training-code/kubebuilder-workshops
go get sigs.k8s.io/controller-tools/cmd/controller-gen sigs.k8s.io/controller-runtime
go mod download

# Kubebuilder init
kubebuilder init --domain kubecon.workshop.intro
# Create an API
kubebuilder create api --group webapp --kind GuestBook --version v1
# Output
Create Resource [y/n]
y
Create Controller [y/n]
y
Writing kustomize manifests for you to edit...
Writing scaffold for you to edit...
api/v1/guestbook_types.go
controllers/guestbook_controller.go
Update dependencies:
$ go mod tidy
Running make:
$ make generate
go: creating new go.mod: module tmp
```
