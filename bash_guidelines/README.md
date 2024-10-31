# Safe Bash Guidelines

- [Safe Bash Guidelines](#safe-bash-guidelines)
  - [Further Resources](#further-resources)
  - [Advanced Bash](#advanced-bash)
    - [Strict scripts](#strict-scripts)
    - [Prefer long flags](#prefer-long-flags)
    - [Do not hide errors unless you are sure](#do-not-hide-errors-unless-you-are-sure)
    - [Error Logging](#error-logging)
    - [Disambiguation: `exit` vs `return`](#disambiguation-exit-vs-return)
    - [Avoid colors](#avoid-colors)
    - [Prefer simple code](#prefer-simple-code)
    - [Splitting long lines](#splitting-long-lines)
    - [Variable and Function names](#variable-and-function-names)
    - [Variable Scope](#variable-scope)
    - [Handling Positional arguments](#handling-positional-arguments)
    - [Handling Optional arguments and flags](#handling-optional-arguments-and-flags)
    - [Use `BASH_SOURCE` to maintain script calls relative paths, regardless of execution path](#use-bash_source-to-maintain-script-calls-relative-paths-regardless-of-execution-path)
    - [Disambiguation: Sourcing vs Execution](#disambiguation-sourcing-vs-execution)
    - [Disambiguation: Eager vs Lazy Evaluation](#disambiguation-eager-vs-lazy-evaluation)
    - [Disambiguation: Different methods of redirects](#disambiguation-different-methods-of-redirects)
    - [Runnable functions trick](#runnable-functions-trick)

Our guidelines for bash are aligned with [Google's style guide for shell scripts](https://google.github.io/styleguide/shellguide.html) with a few differences:

- Initialize scripts with `!#/usr/bin/env bash`
- We use four spaces for indentation instead of two.
- We are not as strict to the maximum line length.
- We do not require the `_main_` function
- We advise to avoid arrays if possible

Repeating some of the guidelines we see often ignored:

- Use `[[` instead of `[`
- Be aware of stderr and stdout and use them properly
- Only the `$()` notation is allowed, backticks must be avoided
- For readability purposes, each function can include 2 lines spacing at before it's start and after it's end points.
- Use shellcheck to verify your script. You might even want to run it as part of the CICD.
- Use `shellcheck -x` when your script includes `source` commands (imports), to allow importing external files. Example:

## Further Resources

- [Google's style guide for shell scripts](https://google.github.io/styleguide/shellguide.html)
- [Bash Coding Style](https://opensourcelibs.com/lib/bash-coding-style)

```Shell
# By default shellcheck source-path is SCRIPTDIR.
# Use the following comment, as annotation, for shellcheck to find the sourced script.
# Always use relative or absolute paths on shellcheck directives, cannot infer variables (such as ${BASH_SOURCE})

# shellcheck source=tf_version_check.sh
source "${BASH_SOURCE%/*}/tf_version_check.sh"
```

## Advanced Bash

When it comes to writing scripts for production, a few more rules apply.

### Strict scripts

Most of the time it is advised to set your script to be strict on errors by setting:

```Shell
TRUE_REG='^([tT][rR][uU][eE]|[yY]|[yY][eE][sS]|1)$'
FALSE_REG='^([fF][aA][lL][sS][eE]|[nN]|[nN][oO]|0)$'

STRICT_SCRIPT=${STRICT_SCRIPT:-true}
if [[ $STRICT_SCRIPT =~ $TRUE_REG ]]; then
    set -o errexit
    set -o nounset
    set -o pipefail
fi
```

`errexit` will make the script exit on any error. `nounset` will make the script
exit if it finds an unbound variable. `pipefail` will fail a pipe if any of its
commands fail.

### Prefer long flags

For flags that are not common it is better to prefer the long option in order
to make the code readable.

As an example, the previous section with short opts would be like this:

```Shell
set +e
set -u
```

Instead of

```Shell
set -o errexit
set -o nounset
```

### Do not hide errors unless you are sure

Many people use `rm -f` or `mkdir -p` automatically. This practice can hide
bugs. For example `rm -f file` will not complain if `file` isn't there. Thus you
have to think if this is ok. Maybe the absence of the file hides an earlier
error in your code. Same goes for `command || true`. Think, then use.

### Error Logging

- Avoid, if possible, to handle error of __another function__. Each function should handle error and/or error message by their own implementation, inside its own definition.
- All errors could be sent to `STDERR` as a good practice. Never send any error/warning message to a `STDOUT` device. Prefer to not use __echo directly__ to print your message; use a wrapper instead (`warn`, `err`, `die`,...). For example,

```Shell
function _err() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] ERROR: $*" >&2
}

function _warn() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] WARN: $*" >&2
}

function _die() {
    _err "$*"
    exit 1
}
```

### Disambiguation: `exit` vs `return`

- For better error handling, it is advised to exit an executable script early with `exit [code]`, e.g. `exit 1`
- Using `exit` in a function, will exit the whole script execution.
- If you only want to check the execution code of a function, for example in a case when the error can be recovered from the caller, you can use `return [code]` instead. Example:

```Shell
# Exit the script immediately, on condition.
function foo() {
    # ...
    exit 1
}

# Return the exit code 1 to the caller, decide if exit (default with set -e), or catch and continue
function bar() {
    # ...
    return 1
}

# Exit execution on error
if foo; then
    echo "Success"
else
    echo "Failed"
    # Always exits the script
fi

# Handle bar return code
if bar; then
    echo "Success"
else
    echo "Failed"
fi
```

### Avoid colors

They are fun at start but soon become complex and make reading code harder.

### Prefer simple code

Bash scripts should be accessible to all enginners in an organization. Whilst SREs/DevOps/IT are capable of using advanced features sometimes it is more prudent to go the simple, albeit a bit longer way, to make our script more readable and maintainable.

An example would be to prefer the easier to understand form:

```Shell
echo "$VAR" | grep [keyword]
```

Instead of the more advanced:

```Shell
grep [keyword] <<<$VAR
```

### Splitting long lines

Prefer to split a long line with the operator at the beginning. Helps with showing the intent of each line, clearly.

```Shell
# Refactor this
curl -s "$_url" | jq -r '.versions[].version' | sort -r --version-sort | head -n 1 && echo "Finished"

# Prefer this
curl -s "$_url" \
    | jq -r '.versions[].version' \
    | sort -r --version-sort \
    | head -n 1 \
    && echo "Finished"

# To this
curl -s "$_url" | \
    jq -r '.versions[].version' | \
    sort -r --version-sort | \
    head -n 1 && \
    echo "Finished"
```

### Variable and Function names

By convention the following naming rules are advised to be applied, to improve codebase consistency & readability:

- All __environment variables__, __exported variables__ and/or __user input variables__ are preferred be named with __`UPPER_CASE`.__ Also all variable and function names are preferred be __`snake_case`__ not `camelCase`, `PascalCase` or `kebab-case`.
- It is preferrable to handle cases of unset environment variables values with default values, except for the case we want to explicitly fail early. Example:

```Shell
# If no value is provided, will try to open test.txt by default
read -r _input_text < "${INPUT_FILE:-test.txt}"

# Explicitly fail, when variable is important to program execution.
if [[ -z "${INPUT_FILE}" ]]; then
    err "No INPUT_FILE variable was set."
    exit 1
fi
```

- Prefer using __leading underscore__ names for script __internal__ variables (used only within the script) and functions used only in other functions. Even though when __executing__ or __sourcing__ a script, all variables and functions get exported to the global shell namespace (either the existing or a new sub-shell), these conventions are better for readability/maintenance reasons and covey intent.
- It's optional, but nice for clarity to use two underscores `__` to indicate some __very internal__ methods aka the ones should be used by other __internal functions__.

```Shell
# Used internally only in script
_json_output="false"

# Function internally used only in executable functions
function _is_json_output() {
    if [[ "$_json_output" == "true" ]]; then
    # ...
    fi

# Indicates function to be sourced and used as command or on another bash script
function output_result() {
    output=$(_is_json_output | jq -r '.')
    echo "$output"
}
```

- We prefer to __quote__ and use __braces__ such as `echo "${foo}"` when referring to variables.
  - Quoting avoids globbing & word-splitting in strings that contain special characters such as `*` and spaces.
  - Braces with `${}` help when expanding variables within strings, such as `echo "${foo}bar"`. In this example if no braces are used `echo "$foobar"`, bash will try to expand variable `foobar` instead of expanding variable `foo` and concatenate with the string `"bar"`.
  - The above rule can be avoided on __leading underscore__ names, if they are not __needed to be expanded in strings__, for readability purposes. E.g. `echo "$_foo"` is more readable to `echo "${_foo}`
  - The rule can also be avoided on __common shell variables__, such as:

```Shell
"$@"
"$*"
"$1"
"$2"
# ...
"$!"
"$?"
```

- Prefer using the keyword `function` prefix to declare bash functions, to simply using the function name, followed by parentheses, for conciseness reasons. Example:

```Shell
# Prefer this
function foo_func() {

}

# To this
foo_func() {

}
```

### Variable Scope

Bash variables by default are __global__ which means the need be extra disciplined with variable and function names, to avoid overriding __environment variables__, __built-in commands__ and __internal shell variables.__

- Additionally the use of `local` keyword is encouraged, to enforce __local scope__ on functions, as much as possible.

```Shell
# Global _foo
_foo="foo"

# Local foo, shadows global _foo correctly.
function _var_mutate() {
    local _foo
    _foo="bar"
    echo "$_foo"
}

echo "$_foo"
# foo
_var_mutate
# bar
echo "$_foo"
# foo - global has not been mutated
```

### Handling Positional arguments

It is strongly advised to store __positional arguments__ in variables with a meaningful name, at the start of functions, or scripts and use this variable for the remainder of the script/function. Example:

```Shell
USER_INPUT_FILE="$1"
# ...

# Positional arguments, relative to function: here $1 refers to the function's argument list, not the script's.
function git_diff() {
    _file_to_diff="$1"
    # ...
}

# Use the full name, instead of the confusing $1
git_diff "${USER_INPUT_FILE}"
```

### Handling Optional arguments and flags

### Use `BASH_SOURCE` to maintain script calls relative paths, regardless of execution path

It is advised to include relative path handling in scripts, to avoid i.e. file not found errors, when execution of a script is performed outside of the script's folder. To achieve this we use the `${BASH_SOURCE}` environment variable that returns the script name from where it was called.

```Shell
#!/usr/bin/env bash

# This will not fail if run from outside of the script's folder
source "${BASH_SOURCE%/*}/imported_script.sh"

# This will fail if run outside of the script's folder
source imported_script.sh
# ~/Documents/outside/test.sh: line 6: imported_script.sh: No such file or directory
```

- `${BASH_SOURCE%/*}` strips the own script name and returns the containing folder.
- `BASH_SOURCE` is an array (containing script's sub-shell call stack) where the first element is the calling script name, whereas `$0` is the 0-th argument variable (the script name)
- It is generally a good idea, to default to `"$0"` whenever `BASH_SOURCE` can't be found, e.g. to be compatible with POSIX `/bin/sh`. Example: `_script_path="${BASH_SOURCE:-$0}`

### Disambiguation: Sourcing vs Execution

Sourcing vs execution - `source` vs `.` vs `exec` vs `./file.sh`

### Disambiguation: Eager vs Lazy Evaluation

Statement vs expression - `{}` vs `()` vs `$()`

### Disambiguation: Different methods of redirects

File output: `>` vs `>>`

File input vs 'here' doc vs 'here' string vs process substitution `<` vs `<<` vs `<<<` vs `<()` and `< <()`

### Runnable functions trick

- Example: `functions.sh`

```Shell
#!/usr/bin/env bash

# set -o xtrace
set -o errexit  # exit when a command fails
set -o nounset  # exit when try to use undefined variable
set -o pipefail # return exit code of the last piped command

function first_command() {}

function second_command() {}

# At the end of your script file
$1 "${@:2}"
```

- Invoke

```Shell
./functions.sh first_command
```
