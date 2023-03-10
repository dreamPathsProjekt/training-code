# Powershell Masterclass

- [Masterclass Playlist](https://www.youtube.com/playlist?list=PLlVtbbG169nFq_hR7FcMYg32xsSAObuq8)
- [PowershellMC Repo](https://github.com/johnthebrit/PowerShellMC)
- [All cmdlets Referenced](https://github.com/johnthebrit/PowerShellMC/blob/master/Sample.ps1)

- [Powershell Masterclass](#powershell-masterclass)
  - [Fundamentals](#fundamentals)
    - [Install PS Core (7.1) on Windows](#install-ps-core-71-on-windows)
    - [Set own PS Tab Complete Function](#set-own-ps-tab-complete-function)
    - [Show alias cmdlets](#show-alias-cmdlets)
    - [Filesystem navigation](#filesystem-navigation)
    - [Powershell Modules - Help](#powershell-modules---help)
  - [Pipeline - Pass Objects - OO Tricks](#pipeline---pass-objects---oo-tricks)
    - [Semicolon - Multiple cmds on one line](#semicolon---multiple-cmds-on-one-line)
    - [External APIs (normal commands) use with PS - Text manipulation](#external-apis-normal-commands-use-with-ps---text-manipulation)
    - [PS Variables](#ps-variables)
    - [Pipelines](#pipelines)
    - [Metrics, Filtering & Querying](#metrics-filtering--querying)
    - [Comparing sets of data](#comparing-sets-of-data)
    - [Advanced Output](#advanced-output)
    - [Using Objects - WhatIf](#using-objects---whatif)
  - [Mount Azure as PSDrive](#mount-azure-as-psdrive)
  - [AzureAD Module - Currently stable only on 5.1](#azuread-module---currently-stable-only-on-51)
  - [Powershell Remote](#powershell-remote)
    - [Invoke command](#invoke-command)

## Fundamentals

- All cmdlets in PS get input and produce output as objects. The output is not textual (as in Unix shell, or cmd) and also pipes are sequences of operations (messages in Smalltalk lingo) between live objects.
- Text output is there at the end of a pipeline.
- PS is built on top of .NET framework (object oriented) and can touch any object .NET exposes.
- PS Core is built on top of .NET Core (cross-platform in other OSes)
- Common syntax `verb-noun` pair for cmdlets (another messaging ref)

```Powershell
# Sorting based on object (folders, files) properties
dir | Sort-Object -Descending -Property LastAccessTime

# Get the type of each passed object ($_ is passed object)
dir | foreach {"$($_.GetType().FullName) - $_.name"}
System.IO.DirectoryInfo - api_automation.name
System.IO.DirectoryInfo - azuredisk-csi-driver.name
System.IO.DirectoryInfo - bitnami-docker-kafka.name
System.IO.DirectoryInfo - charts-local.name
System.IO.DirectoryInfo - Custom Office Templates.name

dir | foreach {"$($_.Attributes) - $_"}
Directory - vim_bash_profiles
Directory - windows-venvs
Directory - WindowsPowerShell
Directory - Zoom
Archive - ncc.code-workspace
Archive - nccbuild.rdp
Archive - negotiation-3.txt
Archive - qaautomation.rdp
Archive - shared.code-workspace
Archive - win10-desktop-build.rdp
Archive - windowsbastion.rdp
```

- One can create new objects

```Powershell
New-Object -TypeName System.AppContext
AccessViolationException               AppDomainSetup                         Array
Action<>                               AppDomainUnloadedException             ArraySegment<>
ActivationContext                      ApplicationException                   ArrayTypeMismatchException
Activator                              ApplicationId                          AssemblyLoadEventArgs
AggregateException                     ApplicationIdentity                    AssemblyLoadEventHandler
AppContext                             ArgIterator                            AsyncCallback
AppDomain                              ArgumentException                      Attribute
AppDomainInitializer                   ArgumentNullException                  AttributeTargets
AppDomainManager                       ArgumentOutOfRangeException            AttributeUsageAttribute
AppDomainManagerInitializationOptions  ArithmeticException                    ContextForm
```

- Aliases for known historic cmds e.g. `dir` calls `Get-ChildItem` in proper PS syntax.
- Can manage non-Windows such as Linux as `WSMan` and `CIM` (management protocols)
- PS Core can utilize SSH in addition to `WSMan`
- Remote management -> enabled by default
- PS 5 -> Introduced `PS DSC` (Desired State Configuration) & `OneGet` package manager (including `choco`) - All part of `WMF 5.0` - Windows Management Framework.

```Powershell
# Find PS version
$PSVersionTable

Name                           Value
----                           -----
PSVersion                      5.1.18362.1171
PSEdition                      Desktop
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0...}
BuildVersion                   10.0.18362.1171
CLRVersion                     4.0.30319.42000
WSManStackVersion              3.0
PSRemotingProtocolVersion      2.3
SerializationVersion           1.1.0.1

# Only relevant attribute
$PSVersionTable.PSVersion

Major  Minor  Patch  PreReleaseLabel BuildLabel
-----  -----  -----  --------------- ----------
7      1      2

# Alternative way
Get-Host


Name             : ConsoleHost
Version          : 5.1.18362.1171
InstanceId       : dc699c5b-b42a-412a-8584-6ea52ed260f0
UI               : System.Management.Automation.Internal.Host.InternalHostUserInterface
CurrentCulture   : en-US
CurrentUICulture : en-US
PrivateData      : Microsoft.PowerShell.ConsoleHost+ConsoleColorProxy
DebuggerEnabled  : True
IsRunspacePushed : False
Runspace         : System.Management.Automation.Runspaces.LocalRunspace
```

### Install PS Core (7.1) on Windows

- All PS Core releases: [https://github.com/PowerShell/PowerShell/releases/tag/v7.1.2](https://github.com/PowerShell/PowerShell/releases/tag/v7.1.2)

MSI Installer options

- [msiexec options](https://docs.microsoft.com/en-us/windows/win32/msi/command-line-options)

- `ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL` - This property controls the option for adding the Open PowerShell item to the context menu in Windows Explorer.
- `ADD_FILE_CONTEXT_MENU_RUNPOWERSHELL` - This property controls the option for adding the Run with PowerShell item to the context menu in Windows Explorer.
- `ENABLE_PSREMOTING` - This property controls the option for enabling PowerShell remoting during installation.
- `REGISTER_MANIFEST` - This property controls the option for registering the Windows Event Logging manifest.

```Powershell
$url = "https://github.com/PowerShell/PowerShell/releases/download/v7.1.2/PowerShell-7.1.2-win-x64.msi"
$output = "C:\Users\Ioann\Downloads\PowerShell-7.1.2-win-x64.msi"
# Download
Invoke-WebRequest -Uri $url -OutFile $output

# Installer MSI
msiexec.exe /package PowerShell-7.1.2-win-x64.msi /quiet ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1
```

### Set own PS Tab Complete Function

```Powershell
# Bash style completion
Set-PSReadLineKeyHandler -Key Tab -Function Complete

# Menu style completion
Set-PSReadLineKeyHandler -Key Tab -Function MenuComplete
```

> To make it permanent, put this command into `C:\Users\[User]\Documents\WindowsPowerShell\profile.ps1`

```Powershell
# Find current ps profile
$profile
C:\Users\Ioann\Documents\PowerShell\Microsoft.VSCode_profile.ps1

# Change Profile for PS Core
C:\Users\[User]\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
# Change Profile for PS VSCode
C:\Users\[User]\Documents\PowerShell\Microsoft.VSCode_profile.ps1
```

### Show alias cmdlets

> On scripts (.ps1) don't use aliases!

```Powershell
Get-Alias

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           ? -> Where-Object
Alias           % -> ForEach-Object
Alias           ac -> Add-Content
Alias           cat -> Get-Content
Alias           cd -> Set-Location
Alias           chdir -> Set-Location
Alias           clc -> Clear-Content
Alias           clear -> Clear-Host
Alias           clhy -> Clear-History
Alias           cli -> Clear-Item
Alias           clp -> Clear-ItemProperty
Alias           cls -> Clear-Host
Alias           clv -> Clear-Variable
Alias           cnsn -> Connect-PSSession
Alias           compare -> Compare-Object
Alias           copy -> Copy-Item
Alias           cp -> Copy-Item
Alias           cpi -> Copy-Item
Alias           cpp -> Copy-ItemProperty
Alias           cvpa -> Convert-Path
Alias           dbp -> Disable-PSBreakpoint
Alias           del -> Remove-Item
Alias           diff -> Compare-Object
Alias           dir -> Get-ChildItem
Alias           dnsn -> Disconnect-PSSession
Alias           ebp -> Enable-PSBreakpoint
Alias           echo -> Write-Output
Alias           epal -> Export-Alias
Alias           epcsv -> Export-Csv
Alias           erase -> Remove-Item
Alias           etsn -> Enter-PSSession
Alias           exsn -> Exit-PSSession
Alias           fc -> Format-Custom
Alias           fhx -> Format-Hex                                  7.0.0.0    Microsoft.PowerShell.Utility
Alias           fl -> Format-List
Alias           foreach -> ForEach-Object
Alias           ft -> Format-Table
Alias           fw -> Format-Wide
Alias           gal -> Get-Alias
Alias           gbp -> Get-PSBreakpoint
Alias           gc -> Get-Content
Alias           gcb -> Get-Clipboard                               7.0.0.0    Microsoft.PowerShell.Management
Alias           gci -> Get-ChildItem
Alias           gcm -> Get-Command
Alias           gcs -> Get-PSCallStack
Alias           gdr -> Get-PSDrive
Alias           gerr -> Get-Error
Alias           ghy -> Get-History
Alias           gi -> Get-Item
Alias           gin -> Get-ComputerInfo                            7.0.0.0    Microsoft.PowerShell.Management
Alias           gjb -> Get-Job
Alias           gl -> Get-Location
Alias           gm -> Get-Member
Alias           gmo -> Get-Module
Alias           gp -> Get-ItemProperty
Alias           gps -> Get-Process
Alias           gpv -> Get-ItemPropertyValue
Alias           group -> Group-Object
Alias           gsn -> Get-PSSession
Alias           gsv -> Get-Service
Alias           gtz -> Get-TimeZone                                7.0.0.0    Microsoft.PowerShell.Management
Alias           gu -> Get-Unique
Alias           gv -> Get-Variable
Alias           h -> Get-History
Alias           history -> Get-History
Alias           icm -> Invoke-Command
Alias           iex -> Invoke-Expression
Alias           ihy -> Invoke-History
Alias           ii -> Invoke-Item
Alias           ipal -> Import-Alias
Alias           ipcsv -> Import-Csv
Alias           ipmo -> Import-Module
Alias           irm -> Invoke-RestMethod
Alias           iwr -> Invoke-WebRequest
Alias           kill -> Stop-Process
Alias           ls -> Get-ChildItem
Alias           man -> help
Alias           md -> mkdir
Alias           measure -> Measure-Object
Alias           mi -> Move-Item
Alias           mount -> New-PSDrive
Alias           move -> Move-Item
Alias           mp -> Move-ItemProperty
Alias           mv -> Move-Item
Alias           nal -> New-Alias
Alias           ndr -> New-PSDrive
Alias           ni -> New-Item
Alias           nmo -> New-Module
Alias           nsn -> New-PSSession
Alias           nv -> New-Variable
Alias           ogv -> Out-GridView
Alias           oh -> Out-Host
Alias           popd -> Pop-Location
Alias           ps -> Get-Process
Alias           psedit -> Open-EditorFile                          0.2.0      PowerShellEditorServices.Commands
Alias           pushd -> Push-Location
Alias           pwd -> Get-Location
Alias           r -> Invoke-History
Alias           rbp -> Remove-PSBreakpoint
Alias           rcjb -> Receive-Job
Alias           rcsn -> Receive-PSSession
Alias           rd -> Remove-Item
Alias           rdr -> Remove-PSDrive
Alias           ren -> Rename-Item
Alias           ri -> Remove-Item
Alias           rjb -> Remove-Job
Alias           rm -> Remove-Item
Alias           rmdir -> Remove-Item
Alias           rmo -> Remove-Module
Alias           rni -> Rename-Item
Alias           rnp -> Rename-ItemProperty
Alias           rp -> Remove-ItemProperty
Alias           rsn -> Remove-PSSession
Alias           rv -> Remove-Variable
Alias           rvpa -> Resolve-Path
Alias           sajb -> Start-Job
Alias           sal -> Set-Alias
Alias           saps -> Start-Process
Alias           sasv -> Start-Service
Alias           sbp -> Set-PSBreakpoint
Alias           scb -> Set-Clipboard                               7.0.0.0    Microsoft.PowerShell.Management
Alias           select -> Select-Object
Alias           set -> Set-Variable
Alias           shcm -> Show-Command
Alias           si -> Set-Item
Alias           sl -> Set-Location
Alias           sleep -> Start-Sleep
Alias           sls -> Select-String
Alias           sort -> Sort-Object
Alias           sp -> Set-ItemProperty
Alias           spjb -> Stop-Job
Alias           spps -> Stop-Process
Alias           spsv -> Stop-Service
Alias           start -> Start-Process
Alias           stz -> Set-TimeZone                                7.0.0.0    Microsoft.PowerShell.Management
Alias           sv -> Set-Variable
Alias           tee -> Tee-Object
Alias           type -> Get-Content
Alias           where -> Where-Object
Alias           wjb -> Wait-Job
Alias           write -> Write-Output
```

### Filesystem navigation

Regular navigation commands e.g. `dir->Get-ChildItem` work not only on filesystems but also on:

- Registry
- Certificate Store
- Active Directory
- RDS
- IIS
- Azure

```Powershell
# List exposed interfaces as drives
Get-PSDrive

Name           Used (GB)     Free (GB) Provider      Root                                                                                                                                                                   CurrentLocation
----           ---------     --------- --------      ----                                                                                                                                                                   ---------------
Alias                                  Alias
C                 289.33        174.66 FileSystem    C:\                                                                                                                                                                        Users\Ioann
Cert                                   Certificate   \
Env                                    Environment
Function                               Function
HKCU                                   Registry      HKEY_CURRENT_USER
HKLM                                   Registry      HKEY_LOCAL_MACHINE
Temp              289.33        174.66 FileSystem    C:\Users\Ioann\AppData\Local\Temp\
Variable                               Variable
WSMan                                  WSMan

cd Env:
PS Env:\> dir

Name                           Value
----                           -----
ALLUSERSPROFILE                C:\ProgramData
APPDATA                        C:\Users\Ioann\AppData\Roaming
ChocolateyInstall              C:\ProgramData\chocolatey
ChocolateyLastPathUpdate       132515687672484583
ChocolateyToolsLocation        C:\tools
CommonProgramFiles             C:\Program Files\Common Files
CommonProgramFiles(x86)        C:\Program Files (x86)\Common Files
CommonProgramW6432             C:\Program Files\Common Files
COMPUTERNAME                   DESKTOP-CQA3U9S
ComSpec                        C:\WINDOWS\system32\cmd.exe
DriverData                     C:\Windows\System32\Drivers\DriverData
HOMEDRIVE                      C:
HOMEPATH                       \Users\Ioann
LOCALAPPDATA                   C:\Users\Ioann\AppData\Local
LOGONSERVER                    \\DESKTOP-CQA3U9S
NUMBER_OF_PROCESSORS           8
OneDrive                       C:\Users\Ioann\OneDrive
OS                             Windows_NT
Path                           C:\Program Files\PowerShell\7;C:\Python39\Scripts\;C:\Python39\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\ProgramData\chocolatey\bin;C:\Progra…
PATHEXT                        .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW;.CPL
POWERSHELL_DISTRIBUTION_CHANN… MSI:Windows 10 Pro
PROCESSOR_ARCHITECTURE         AMD64
PROCESSOR_IDENTIFIER           Intel64 Family 6 Model 142 Stepping 10, GenuineIntel
PROCESSOR_LEVEL                6
PROCESSOR_REVISION             8e0a
ProgramData                    C:\ProgramData
ProgramFiles                   C:\Program Files
ProgramFiles(x86)              C:\Program Files (x86)
ProgramW6432                   C:\Program Files
PSModulePath                   C:\Users\Ioann\Documents\PowerShell\Modules;C:\Program Files\PowerShell\Modules;c:\program files\powershell\7\Modules;C:\Program Files\WindowsPowerShell\Modules;C:\WINDOWS\system32\WindowsPowerShell\v1.0…
PUBLIC                         C:\Users\Public
SystemDrive                    C:
SystemRoot                     C:\WINDOWS
TEMP                           C:\Users\Ioann\AppData\Local\Temp
TMP                            C:\Users\Ioann\AppData\Local\Temp
USERDOMAIN                     DESKTOP-CQA3U9S
USERDOMAIN_ROAMINGPROFILE      DESKTOP-CQA3U9S
USERNAME                       Ioann
USERPROFILE                    C:\Users\Ioann
VBOX_MSI_INSTALL_PATH          C:\Program Files\Oracle\VirtualBox\
windir                         C:\WINDOWS
WSLENV                         WT_SESSION::WT_PROFILE_ID
WT_PROFILE_ID                  {574e775e-4f2a-5b96-ac1e-a2962a402336}
WT_SESSION                     630f2c7e-e045-41ba-bba3-76042f9fc039

# Alternative way to find aliases
cd Alias:
PS Alias:\> dir

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           ? -> Where-Object
Alias           % -> ForEach-Object
Alias           ac -> Add-Content
Alias           cat -> Get-Content
Alias           cd -> Set-Location
Alias           chdir -> Set-Location
Alias           clc -> Clear-Content
Alias           clear -> Clear-Host
Alias           clhy -> Clear-History
Alias           cli -> Clear-Item
Alias           clp -> Clear-ItemProperty
Alias           cls -> Clear-Host
Alias           clv -> Clear-Variable
Alias           cnsn -> Connect-PSSession
Alias           compare -> Compare-Object
Alias           copy -> Copy-Item
Alias           cp -> Copy-Item
Alias           cpi -> Copy-Item
Alias           cpp -> Copy-ItemProperty
Alias           cvpa -> Convert-Path
Alias           dbp -> Disable-PSBreakpoint
Alias           del -> Remove-Item
Alias           diff -> Compare-Object
Alias           dir -> Get-ChildItem
Alias           dnsn -> Disconnect-PSSession
Alias           ebp -> Enable-PSBreakpoint
Alias           echo -> Write-Output
Alias           epal -> Export-Alias
Alias           epcsv -> Export-Csv
Alias           erase -> Remove-Item
Alias           etsn -> Enter-PSSession
Alias           exsn -> Exit-PSSession
Alias           fc -> Format-Custom
Alias           fhx -> Format-Hex                                  7.0.0.0    Microsoft.PowerShell.Utility
Alias           fl -> Format-List
Alias           foreach -> ForEach-Object
Alias           ft -> Format-Table
Alias           fw -> Format-Wide
Alias           gal -> Get-Alias
Alias           gbp -> Get-PSBreakpoint
Alias           gc -> Get-Content
Alias           gcb -> Get-Clipboard                               7.0.0.0    Microsoft.PowerShell.Management
Alias           gci -> Get-ChildItem
Alias           gcm -> Get-Command
Alias           gcs -> Get-PSCallStack
Alias           gdr -> Get-PSDrive
Alias           gerr -> Get-Error
Alias           ghy -> Get-History
Alias           gi -> Get-Item
Alias           gin -> Get-ComputerInfo                            7.0.0.0    Microsoft.PowerShell.Management
Alias           gjb -> Get-Job
Alias           gl -> Get-Location
Alias           gm -> Get-Member
Alias           gmo -> Get-Module
Alias           gp -> Get-ItemProperty
Alias           gps -> Get-Process
Alias           gpv -> Get-ItemPropertyValue
Alias           group -> Group-Object
Alias           gsn -> Get-PSSession
Alias           gsv -> Get-Service
Alias           gtz -> Get-TimeZone                                7.0.0.0    Microsoft.PowerShell.Management
Alias           gu -> Get-Unique
Alias           gv -> Get-Variable
Alias           h -> Get-History
Alias           history -> Get-History
Alias           icm -> Invoke-Command
Alias           iex -> Invoke-Expression
Alias           ihy -> Invoke-History
Alias           ii -> Invoke-Item
Alias           ipal -> Import-Alias
Alias           ipcsv -> Import-Csv
Alias           ipmo -> Import-Module
Alias           irm -> Invoke-RestMethod
Alias           iwr -> Invoke-WebRequest
Alias           kill -> Stop-Process
Alias           ls -> Get-ChildItem
Alias           man -> help
Alias           md -> mkdir
Alias           measure -> Measure-Object
Alias           mi -> Move-Item
Alias           mount -> New-PSDrive
Alias           move -> Move-Item
Alias           mp -> Move-ItemProperty
Alias           mv -> Move-Item
Alias           nal -> New-Alias
Alias           ndr -> New-PSDrive
Alias           ni -> New-Item
Alias           nmo -> New-Module
Alias           nsn -> New-PSSession
Alias           nv -> New-Variable
Alias           ogv -> Out-GridView
Alias           oh -> Out-Host
Alias           popd -> Pop-Location
Alias           ps -> Get-Process
Alias           pushd -> Push-Location
Alias           pwd -> Get-Location
Alias           r -> Invoke-History
Alias           rbp -> Remove-PSBreakpoint
Alias           rcjb -> Receive-Job
Alias           rcsn -> Receive-PSSession
Alias           rd -> Remove-Item
Alias           rdr -> Remove-PSDrive
Alias           ren -> Rename-Item
Alias           ri -> Remove-Item
Alias           rjb -> Remove-Job
Alias           rm -> Remove-Item
Alias           rmdir -> Remove-Item
Alias           rmo -> Remove-Module
Alias           rni -> Rename-Item
Alias           rnp -> Rename-ItemProperty
Alias           rp -> Remove-ItemProperty
Alias           rsn -> Remove-PSSession
Alias           rv -> Remove-Variable
Alias           rvpa -> Resolve-Path
Alias           sajb -> Start-Job
Alias           sal -> Set-Alias
Alias           saps -> Start-Process
Alias           sasv -> Start-Service
Alias           sbp -> Set-PSBreakpoint
Alias           scb -> Set-Clipboard                               7.0.0.0    Microsoft.PowerShell.Management
Alias           select -> Select-Object
Alias           set -> Set-Variable
Alias           shcm -> Show-Command
Alias           si -> Set-Item
Alias           sl -> Set-Location
Alias           sleep -> Start-Sleep
Alias           sls -> Select-String
Alias           sort -> Sort-Object
Alias           sp -> Set-ItemProperty
Alias           spjb -> Stop-Job
Alias           spps -> Stop-Process
Alias           spsv -> Stop-Service
Alias           start -> Start-Process
Alias           stz -> Set-TimeZone                                7.0.0.0    Microsoft.PowerShell.Management
Alias           sv -> Set-Variable
Alias           tee -> Tee-Object
Alias           type -> Get-Content
Alias           where -> Where-Object
Alias           wjb -> Wait-Job
Alias           write -> Write-Output
```

### Powershell Modules - Help

- Modules are groups (contain) __cmdlets__
- Modules are loaded (before version 3 -> manually loaded)

```Powershell
# List current loaded modules
Get-Module

ModuleType Version    PreRelease Name                                ExportedCommands
---------- -------    ---------- ----                                ----------------
Manifest   7.0.0.0               Microsoft.PowerShell.Management     {Add-Content, Clear-Content, Clear-Item, Clear-ItemProperty…}
Manifest   7.0.0.0               Microsoft.PowerShell.Security       {ConvertFrom-SecureString, ConvertTo-SecureString, Get-Acl, Get-AuthenticodeSignature…}
Manifest   7.0.0.0               Microsoft.PowerShell.Utility        {Add-Member, Add-Type, Clear-Variable, Compare-Object…}
Manifest   7.0.0.0               Microsoft.WSMan.Management          {Connect-WSMan, Disable-WSManCredSSP, Disconnect-WSMan, Enable-WSManCredSSP…}
Script     1.0                   pki                                 {Add-CertificateEnrollmentPolicyServer, Export-Certificate, Export-PfxCertificate, Get-Certificate…}
Script     2.1.0                 PSReadLine                          {Get-PSReadLineKeyHandler, Get-PSReadLineOption, Remove-PSReadLineKeyHandler, Set-PSReadLineKeyHandler…}
Manifest   2.0.0.0               Storage                             {Add-InitiatorIdToMaskingSet, Add-PartitionAccessPath, Add-PhysicalDisk, Add-StorageFaultDomain…}

# Get Available - Installed, but not necessarily loaded
Get-Module -ListAvailable

# Get commands in a module
Get-Command -Module <module_name>

# Example
Get-Command -Module PSDesiredStateConfiguration

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Function        Configuration                                      2.0.5      PSDesiredStateConfiguration
Function        Get-DscResource                                    2.0.5      PSDesiredStateConfiguration
Function        New-DscChecksum                                    2.0.5      PSDesiredStateConfiguration

# Import module into PS Instance
Import-Module PSDesiredStateConfiguration

# Find unique nouns in module commands
Get-Command -Module Microsoft.PowerShell.Utility | Select-Object -Unique Noun | Sort-Object Noun

# Check version of module
(Get-Module Microsoft.PowerShell.Utility).Version
# () is Object output form

# Equivalent
$executedModule = Get-Module Microsoft.PowerShell.Utility
$executedModule.Version

Major  Minor  Build  Revision
-----  -----  -----  --------
7      0      0      0

# Integration with repositories and GitHub
Install-Module Az
Update-Module Az

# Enables initial installation & upgrade (only on Administration PS session)
Install-Module Az
Untrusted repository                                                                                                    You are installing the modules from an untrusted repository. If you trust this repository, change its                   InstallationPolicy value by running the Set-PSRepository cmdlet. Are you sure you want to install the modules from
'PSGallery'?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): Y

# Now Az family modules appear on installed list
Get-Module Az.* -ListAvailable | Select-Object -Unique Name, Version
Name                     Version
----                     -------
Az.Accounts              2.2.6
Az.Advisor               1.1.1
Az.Aks                   2.0.2
Az.AnalysisServices      1.1.4
Az.ApiManagement         2.2.0
Az.AppConfiguration      1.0.0
Az.ApplicationInsights   1.1.0
Az.Automation            1.5.0
Az.Batch                 3.1.0
Az.Billing               2.0.0
Az.Cdn                   1.6.0
Az.CognitiveServices     1.8.0
Az.Compute               4.10.0
Az.ContainerInstance     1.0.3
Az.ContainerRegistry     2.2.1
Az.CosmosDB              1.1.0
Az.DataBoxEdge           1.1.0
Az.Databricks            1.1.0
Az.DataFactory           1.11.4
Az.DataLakeAnalytics     1.0.2
Az.DataLakeStore         1.3.0
Az.DataShare             1.0.0
Az.DeploymentManager     1.1.0
Az.DesktopVirtualization 2.1.1
Az.DevTestLabs           1.0.2
Az.Dns                   1.1.2
Az.EventGrid             1.3.0
Az.EventHub              1.7.1
Az.FrontDoor             1.7.0
Az.Functions             2.0.0
Az.HDInsight             4.2.0
Az.HealthcareApis        1.2.0
Az.IotHub                2.7.2
Az.KeyVault              3.4.0
Az.Kusto                 1.0.1
Az.LogicApp              1.5.0
Az.MachineLearning       1.1.3
Az.Maintenance           1.1.0
Az.ManagedServices       2.0.0
Az.MarketplaceOrdering   1.0.2
Az.Media                 1.1.1
Az.Migrate               1.0.0
Az.Monitor               2.4.0
Az.Network               4.6.0
Az.NotificationHubs      1.1.1
Az.OperationalInsights   2.3.0
Az.PolicyInsights        1.4.1
Az.PowerBIEmbedded       1.1.2
Az.PrivateDns            1.0.3
Az.RecoveryServices      3.4.1
Az.RedisCache            1.4.0
Az.Relay                 1.0.3
Az.Resources             3.3.0
Az.ServiceBus            1.4.1
Az.ServiceFabric         2.2.2
Az.SignalR               1.2.0
Az.Sql                   2.16.0
Az.SqlVirtualMachine     1.1.0
Az.Storage               3.4.0
Az.StorageSync           1.4.0
Az.StreamAnalytics       1.0.1
Az.Support               1.0.0
Az.TrafficManager        1.0.4
Az.Websites              2.4.0

Get-Command -Module Az.Billing

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Get-AzBillingAccount                               2.0.0      Az.Billing
Cmdlet          Get-AzBillingInvoice                               2.0.0      Az.Billing
Cmdlet          Get-AzBillingPeriod                                2.0.0      Az.Billing
Cmdlet          Get-AzBillingProfile                               2.0.0      Az.Billing
Cmdlet          Get-AzConsumptionBudget                            2.0.0      Az.Billing
Cmdlet          Get-AzConsumptionMarketplace                       2.0.0      Az.Billing
Cmdlet          Get-AzConsumptionPriceSheet                        2.0.0      Az.Billing
Cmdlet          Get-AzConsumptionReservationDetail                 2.0.0      Az.Billing
Cmdlet          Get-AzConsumptionReservationSummary                2.0.0      Az.Billing
Cmdlet          Get-AzConsumptionUsageDetail                       2.0.0      Az.Billing
Cmdlet          Get-AzEnrollmentAccount                            2.0.0      Az.Billing
Cmdlet          Get-AzInvoiceSection                               2.0.0      Az.Billing
Cmdlet          Get-UsageAggregates                                2.0.0      Az.Billing
Cmdlet          New-AzConsumptionBudget                            2.0.0      Az.Billing
Cmdlet          Remove-AzConsumptionBudget                         2.0.0      Az.Billing
Cmdlet          Set-AzConsumptionBudget                            2.0.0      Az.Billing

# Sign-In Using browser flow
Connect-AzAccount

# Select Subscription Context
Get-AzContext <Tab>
Pay-As-You-Go - SMG (36941506-a17d-4852-a9ce-c14edafb2bb4) - 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 - ioannis.dritsas@e-share.us
PAYG - Development (65d32e9a-e358-41bc-8c88-ba0e1fa1c0e4) - 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 - ioannis.dritsas@e-share.us
PAYG - Development Testing (53faa829-4516-4dbc-8e6a-e4637c5ee7f8) - 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 - ioannis.dritsas@e-share.us
PAYG - Migration (d28ea675-da7a-4263-b4ee-faf33c7269e2) - 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 - ioannis.dritsas@e-share.us

# Change current context
Get-AzContext 'PAYG - Development (65d32e9a-e358-41bc-8c88-ba0e1fa1c0e4) - 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 - ioannis.dritsas@e-share.us' | Set-AzContext
```

- Without `Install-Module` cmdlet: Install Azure PS Modules [https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-5.6.0](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps?view=azps-5.6.0)

```Powershell
# Get help for cmdlet
Get-Help <cmdlet>

# Options
-Full
-Detailed
-Examples
-Online # Display in browser
-ShowWindow # Show in separate help window

# Example
Get-Help Get-AzBillingAccount

NAME
    Get-AzBillingAccount

SYNOPSIS
    Get billing accounts.


SYNTAX
    Get-AzBillingAccount [-DefaultProfile <Microsoft.Azure.Commands.Common.Authentication.Abstractions.Core.IAzureContextContainer>] [-IncludeAddress] [-ExpandBillingProfile] [-ExpandInvoiceSection] -Name
    <System.Collections.Generic.List`1[System.String]> [-ListEntitiesToCreateSubscription] [<CommonParameters>]


DESCRIPTION
    The Get-AzBillingAccount cmdlet gets billing accounts, user has access to.


RELATED LINKS
    Online Version: https://docs.microsoft.com/en-us/powershell/module/az.billing/get-azbillingaccount

REMARKS
    To see the examples, type: "Get-Help Get-AzBillingAccount -Examples"
    For more information, type: "Get-Help Get-AzBillingAccount -Detailed"
    For technical information, type: "Get-Help Get-AzBillingAccount -Full"
    For online help, type: "Get-Help Get-AzBillingAccount -Online"

# Missing help content (elevated)
Update-Help

# Get list of all verbs for a noun
Get-Command -Noun Process

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Debug-Process                                      7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Get-Process                                        7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Start-Process                                      7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Stop-Process                                       7.0.0.0    Microsoft.PowerShell.Management
Cmdlet          Wait-Process                                       7.0.0.0    Microsoft.PowerShell.Management

# Get Command Help URI (online)
(Get-Command Debug-Process).HelpUri
```

## Pipeline - Pass Objects - OO Tricks

- PS does not convert output to text, rather maintains the objects

```Powershell
Get-Process a* | Get-Member

   # Shows class type
   TypeName: System.Diagnostics.Process

# Shows properties & methods
Name                       MemberType     Definition
----                       ----------     ----------
Handles                    AliasProperty  Handles = Handlecount
Name                       AliasProperty  Name = ProcessName
NPM                        AliasProperty  NPM = NonpagedSystemMemorySize64
PM                         AliasProperty  PM = PagedMemorySize64
SI                         AliasProperty  SI = SessionId
VM                         AliasProperty  VM = VirtualMemorySize64
WS                         AliasProperty  WS = WorkingSet64
Parent                     CodeProperty   System.Object Parent{get=GetParentProcess;}
Disposed                   Event          System.EventHandler Disposed(System.Object, System.EventArgs)
ErrorDataReceived          Event          System.Diagnostics.DataReceivedEventHandler ErrorDataReceived(System.Object, System.Diagnostics.DataReceivedEventArgs)
Exited                     Event          System.EventHandler Exited(System.Object, System.EventArgs)
OutputDataReceived         Event          System.Diagnostics.DataReceivedEventHandler OutputDataReceived(System.Object, System.Diagnostics.DataReceivedEventArgs)
BeginErrorReadLine         Method         void BeginErrorReadLine()
BeginOutputReadLine        Method         void BeginOutputReadLine()
CancelErrorRead            Method         void CancelErrorRead()
CancelOutputRead           Method         void CancelOutputRead()
Close                      Method         void Close()
CloseMainWindow            Method         bool CloseMainWindow()
Dispose                    Method         void Dispose(), void IDisposable.Dispose()
Equals                     Method         bool Equals(System.Object obj)
GetHashCode                Method         int GetHashCode()
GetLifetimeService         Method         System.Object GetLifetimeService()
GetType                    Method         type GetType()
InitializeLifetimeService  Method         System.Object InitializeLifetimeService()
Kill                       Method         void Kill(), void Kill(bool entireProcessTree)
Refresh                    Method         void Refresh()
Start                      Method         bool Start()
ToString                   Method         string ToString()
WaitForExit                Method         void WaitForExit(), bool WaitForExit(int milliseconds)
WaitForExitAsync           Method         System.Threading.Tasks.Task WaitForExitAsync(System.Threading.CancellationToken cancellationToken)
WaitForInputIdle           Method         bool WaitForInputIdle(), bool WaitForInputIdle(int milliseconds)
__NounName                 NoteProperty   string __NounName=Process
BasePriority               Property       int BasePriority {get;}
Container                  Property       System.ComponentModel.IContainer Container {get;}
EnableRaisingEvents        Property       bool EnableRaisingEvents {get;set;}
ExitCode                   Property       int ExitCode {get;}
ExitTime                   Property       datetime ExitTime {get;}
Handle                     Property       System.IntPtr Handle {get;}
HandleCount                Property       int HandleCount {get;}
HasExited                  Property       bool HasExited {get;}
Id                         Property       int Id {get;}
MachineName                Property       string MachineName {get;}
MainModule                 Property       System.Diagnostics.ProcessModule MainModule {get;}
MainWindowHandle           Property       System.IntPtr MainWindowHandle {get;}
MainWindowTitle            Property       string MainWindowTitle {get;}
MaxWorkingSet              Property       System.IntPtr MaxWorkingSet {get;set;}
MinWorkingSet              Property       System.IntPtr MinWorkingSet {get;set;}
Modules                    Property       System.Diagnostics.ProcessModuleCollection Modules {get;}
NonpagedSystemMemorySize   Property       int NonpagedSystemMemorySize {get;}
NonpagedSystemMemorySize64 Property       long NonpagedSystemMemorySize64 {get;}
PagedMemorySize            Property       int PagedMemorySize {get;}
PagedMemorySize64          Property       long PagedMemorySize64 {get;}
PagedSystemMemorySize      Property       int PagedSystemMemorySize {get;}
PagedSystemMemorySize64    Property       long PagedSystemMemorySize64 {get;}
PeakPagedMemorySize        Property       int PeakPagedMemorySize {get;}
PeakPagedMemorySize64      Property       long PeakPagedMemorySize64 {get;}
PeakVirtualMemorySize      Property       int PeakVirtualMemorySize {get;}
PeakVirtualMemorySize64    Property       long PeakVirtualMemorySize64 {get;}
PeakWorkingSet             Property       int PeakWorkingSet {get;}
PeakWorkingSet64           Property       long PeakWorkingSet64 {get;}
PriorityBoostEnabled       Property       bool PriorityBoostEnabled {get;set;}
PriorityClass              Property       System.Diagnostics.ProcessPriorityClass PriorityClass {get;set;}
PrivateMemorySize          Property       int PrivateMemorySize {get;}
PrivateMemorySize64        Property       long PrivateMemorySize64 {get;}
PrivilegedProcessorTime    Property       timespan PrivilegedProcessorTime {get;}
ProcessName                Property       string ProcessName {get;}
ProcessorAffinity          Property       System.IntPtr ProcessorAffinity {get;set;}
Responding                 Property       bool Responding {get;}
SafeHandle                 Property       Microsoft.Win32.SafeHandles.SafeProcessHandle SafeHandle {get;}
SessionId                  Property       int SessionId {get;}
Site                       Property       System.ComponentModel.ISite Site {get;set;}
StandardError              Property       System.IO.StreamReader StandardError {get;}
StandardInput              Property       System.IO.StreamWriter StandardInput {get;}
StandardOutput             Property       System.IO.StreamReader StandardOutput {get;}
StartInfo                  Property       System.Diagnostics.ProcessStartInfo StartInfo {get;set;}
StartTime                  Property       datetime StartTime {get;}
SynchronizingObject        Property       System.ComponentModel.ISynchronizeInvoke SynchronizingObject {get;set;}
Threads                    Property       System.Diagnostics.ProcessThreadCollection Threads {get;}
TotalProcessorTime         Property       timespan TotalProcessorTime {get;}
UserProcessorTime          Property       timespan UserProcessorTime {get;}
VirtualMemorySize          Property       int VirtualMemorySize {get;}
VirtualMemorySize64        Property       long VirtualMemorySize64 {get;}
WorkingSet                 Property       int WorkingSet {get;}
WorkingSet64               Property       long WorkingSet64 {get;}
PSConfiguration            PropertySet    PSConfiguration {Name, Id, PriorityClass, FileVersion}
PSResources                PropertySet    PSResources {Name, Id, Handlecount, WorkingSet, NonPagedMemorySize, PagedMemorySize, PrivateMemorySize, VirtualMemorySize, Threads.Count, TotalProcessorTime}
CommandLine                ScriptProperty System.Object CommandLine {get=…
Company                    ScriptProperty System.Object Company {get=$this.Mainmodule.FileVersionInfo.CompanyName;}
CPU                        ScriptProperty System.Object CPU {get=$this.TotalProcessorTime.TotalSeconds;}
Description                ScriptProperty System.Object Description {get=$this.Mainmodule.FileVersionInfo.FileDescription;}
FileVersion                ScriptProperty System.Object FileVersion {get=$this.Mainmodule.FileVersionInfo.FileVersion;}
Path                       ScriptProperty System.Object Path {get=$this.Mainmodule.FileName;}
Product                    ScriptProperty System.Object Product {get=$this.Mainmodule.FileVersionInfo.ProductName;}
ProductVersion             ScriptProperty System.Object ProductVersion {get=$this.Mainmodule.FileVersionInfo.ProductVersion;}

# Access results in array of objects (e.g. first)
(Get-Process a*)[0].GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     False    Process                                  System.ComponentModel.Component

# Or use foreach accessor
Get-Process a* | ForEach-Object {$_.GetType()}

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     False    Process                                  System.ComponentModel.Component
True     False    Process                                  System.ComponentModel.Component
True     False    Process                                  System.ComponentModel.Component
True     False    Process                                  System.ComponentModel.Component

Get-Alias foreach

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           foreach -> ForEach-Object

# Filter objects by name equality or contains
# Example all processes of VsCode
Get-Process | Where-Object {$_.Name -eq "Code"}

 NPM(K)    PM(M)      WS(M)     CPU(s)      Id  SI ProcessName
 ------    -----      -----     ------      --  -- -----------
     13    16.94      21.20       0.38    1236   1 Code
     19    38.48      23.43       2.41    6708   1 Code
     13    17.42      23.61       1.78    7624   1 Code
     20    15.35      18.87       2.22    8312   1 Code
     58    75.00      84.82     152.08    8592   1 Code
     13    16.37      14.88       0.42   10496   1 Code
     20    43.25      15.86       3.27   12160   1 Code
     42   290.48     277.32     451.89   12868   1 Code
     13    21.10      20.74       0.55   14688   1 Code
     54   299.65     249.19     336.47   15712   1 Code
     15    18.36      21.78       0.83   18308   1 Code
     40   263.39     213.87     261.38   19784   1 Code
     14    19.16      29.87       0.59   19788   1 Code
     13    41.48      26.64       2.03   22900   1 Code
     13    18.43      21.80       1.34   23364   1 Code
     12     9.27       6.86       0.05   23376   1 Code
     43   958.82     285.74     223.50   26112   1 Code
     25    46.02      50.21      66.75   33964   1 Code
     26   271.70     103.13      74.61   36432   1 Code

Get-Process | Where-Object {$_.Name -contains "Code"}

# Equivalent - Reduce number of objects down the pipeline
Get-Process -Name Code | Sort-Object -Property Id

# OO Messaging style pipeline (stop is the msg to send on live objects)
Get-Process -Name Code | Sort-Object -Property Id | Stop-Process
```

### Semicolon - Multiple cmds on one line

> CAUTION!: Pipes after semicolon operate on multiple objects returned

```Powershell
get-alias echo

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           echo -> Write-Output

Write-Output "Hello World!"; Write-Output "Something Else"

# Caution: Processes are mixed in output with services
Get-Process a* | Select-Object -Unique Name; Get-Service a* | Select-Object -Unique Name

Name
----
AdminService
aesm_service
ApplicationFrameHost
audiodg
AarSvc_da46a
AESMService
AJRouter
ALG
AppIDSvc
Appinfo
AppMgmt
AppReadiness
AppVClient
AppXSvc
AssignedAccessManagerSvc
AtherosSvc
AudioEndpointBuilder
Audiosrv
autotimesvc
AxInstSV

# Correctly separate output
Get-Process a* | Select-Object -Unique Name

Name
----
AdminService
aesm_service
ApplicationFrameHost
audiodg

Get-Service a* | Select-Object -Unique Name

Name
----
AarSvc_da46a
AESMService
AJRouter
ALG
AppIDSvc
Appinfo
AppMgmt
AppReadiness
AppVClient
AppXSvc
AssignedAccessManagerSvc
AtherosSvc
AudioEndpointBuilder
Audiosrv
autotimesvc
AxInstSV
```

### External APIs (normal commands) use with PS - Text manipulation

```Powershell
# This doesn't work
ipconfig | Select-Object -Property Id

Id
--

# Object represantation of text output
ipconfig | foreach {$_.GetType()}

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object
True     True     String                                   System.Object

# Using text manipulation - PS grep
ipconfig | Select-String -Pattern 255

   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
```

### PS Variables

```Powershell
# Variable expansion
$var1 = "world"
Write-Output "Hello $var1"
# Primitive types are objects too
$var1.GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     String                                   System.Object

$var2 = 5
$var2.GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Int32                                    System.ValueType

# Ref to objects
$procs = Get-Process
$procs[0] | Get-Member

# Little bit of reflection
$procs[0].GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     False    Process                                  System.ComponentModel.Component

$procs.GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Object[]                                 System.Array

# Format as list of objects (true representation)
$procs | Format-List

Id      : 36664
Handles : 111
CPU     : 0.015625
SI      : 1
Name    : wslhost

Id      : 36832
Handles : 111
CPU     : 0.015625
SI      : 1
Name    : wslhost

Id      : 1380
Handles : 330
CPU     :
SI      : 0
Name    : WUDFHost

Id      : 1568
Handles : 255
CPU     :
SI      : 0
Name    : WUDFHost

Id      : 28492
Handles : 993
CPU     : 1.234375
SI      : 1
Name    : YourPhone

# Custom output query
$procs | Select-Object -Property Name, Path, Id
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   31984
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   32176
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   34016
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   35792
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   36192
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   36664
wslhost                                                        C:\WINDOWS\system32\lxss\wslhost.exe                                                                                   36832
WUDFHost                                                                                                                                                                               1380
WUDFHost                                                                                                                                                                               1568
YourPhone                                                      C:\Program Files\WindowsApps\Microsoft.YourPhone_1.21021.115.0_x64__8wekyb3d8bbwe\YourPhone.exe                        28492

# Cool conversion stuff
$procs | ConvertTo-Xml
$procs | ConvertTo-Html
$procs | ConvertTo-Json
$procs | ConvertTo-Csv

# Example
$procs[0] | ConvertTo-Json
{
  "SafeHandle": null,
  "Handle": null,
  "BasePriority": 8,
  "ExitCode": null,
  "HasExited": null,
  "StartTime": null,
  "ExitTime": null,
  "Id": 4324,
  "MachineName": ".",
  "MaxWorkingSet": null,
  "MinWorkingSet": null,
  "Modules": null,
  "NonpagedSystemMemorySize64": 9104,
  "NonpagedSystemMemorySize": 9104,
  "PagedMemorySize64": 2920448,
  "PagedMemorySize": 2920448,
  "PagedSystemMemorySize64": 120448,
  "PagedSystemMemorySize": 120448,
  "PeakPagedMemorySize64": 3182592,
  "PeakPagedMemorySize": 3182592,
  "PeakWorkingSet64": 8204288,
  "PeakWorkingSet": 8204288,
  "PeakVirtualMemorySize64": 2203418595328,
  "PeakVirtualMemorySize": 100372480,
  "PriorityBoostEnabled": null,
  "PriorityClass": null,
  "PrivateMemorySize64": 2920448,
  "PrivateMemorySize": 2920448,
  "ProcessName": "AdminService",
  "ProcessorAffinity": null,
  "SessionId": 0,
  "StartInfo": null,
  "Threads": [
    {
      "BasePriority": 8,
      "CurrentPriority": 9,
      "Id": 4328,
      "PriorityBoostEnabled": null,
      "PriorityLevel": null,
      "StartAddress": {
        "value": 140715088598784
      },
      "ThreadState": 5,
      "WaitReason": 6,
      "PrivilegedProcessorTime": null,
      "StartTime": null,
      "TotalProcessorTime": null,
      "UserProcessorTime": null,
      "Site": null,
      "Container": null
    },
    {
      "BasePriority": 8,
      "CurrentPriority": 10,
      "Id": 4744,
      "PriorityBoostEnabled": null,
      "PriorityLevel": null,
      "StartAddress": {
        "value": 140715088598784
      },
      "ThreadState": 5,
      "WaitReason": 6,
      "PrivilegedProcessorTime": null,
      "StartTime": null,
      "TotalProcessorTime": null,
      "UserProcessorTime": null,
      "Site": null,
      "Container": null
    },
    {
      "BasePriority": 8,
      "CurrentPriority": 8,
      "Id": 5216,
      "PriorityBoostEnabled": null,
      "PriorityLevel": null,
      "StartAddress": {
        "value": 140715088598784
      },
      "ThreadState": 5,
      "WaitReason": 4,
      "PrivilegedProcessorTime": null,
      "StartTime": null,
      "TotalProcessorTime": null,
      "UserProcessorTime": null,
      "Site": null,
      "Container": null
    }
  ],
  "HandleCount": 159,
  "VirtualMemorySize64": 2203414401024,
  "VirtualMemorySize": 96178176,
  "EnableRaisingEvents": false,
  "StandardInput": null,
  "StandardOutput": null,
  "StandardError": null,
  "WorkingSet64": 2789376,
  "WorkingSet": 2789376,
  "SynchronizingObject": null,
  "MainModule": null,
  "PrivilegedProcessorTime": null,
  "TotalProcessorTime": null,
  "UserProcessorTime": null,
  "MainWindowHandle": {
    "value": 0
  },
  "MainWindowTitle": "",
  "Responding": true,
  "Site": null,
  "Container": null,
  "Name": "AdminService",
  "SI": 0,
  "Handles": 159,
  "VM": 2203414401024,
  "WS": 2789376,
  "PM": 2920448,
  "NPM": 9104,
  "Path": null,
  "CommandLine": null,
  "Parent": null,
  "Company": null,
  "CPU": null,
  "FileVersion": null,
  "ProductVersion": null,
  "Description": null,
  "Product": null,
  "__NounName": "Process"
}

# Filtering queries
$procs | Where-Object {$_.Handles -gt 1000}
# Equivalent query (with alias)
$procs | where Handles -GT 1000

 NPM(K)    PM(M)      WS(M)     CPU(s)      Id  SI ProcessName
 ------    -----      -----     ------      --  -- -----------
     74   155.99     203.09     626.17   25248   1 chrome
     59 1,249.72     457.46     949.41   30100   1 chrome
     58    75.25      81.71     174.91    8592   1 Code
     55     4.97       3.10       0.00    1040   1 csrss
     42    77.49      24.22       0.00   12168   0 DellSupportAssistRemedationService
     71   323.25      93.20       0.00    1696   1 dwm
    228   265.98     136.54   2,234.81    7800   1 explorer
     43    21.62      13.45      58.52    8100   1 igfxEM
     47   295.41     146.45     309.88   10716   1 jetbrains-toolbox
     58    11.40      13.30       0.00    1116   0 lsass
     59    88.59      16.10      11.80   20264   1 Microsoft.Photos
     59    39.89      88.28       8.75   27292   1 msedge
     98 1,699.09     334.05       0.00   27304   0 MsMpEng
    107   101.28     102.08      14.58   16648   1 pwsh
    152   275.65     182.41      50.84   31648   1 pwsh
     84   156.35      67.06       0.00    8516   0 SearchIndexer
    160   238.35      71.98      92.23   16736   1 SearchUI
     70    86.49      64.42       2.42   29620   1 SearchUI
     65    82.79      30.23       0.00   11160   0 ServiceShell
     39    41.46      39.00      49.06   12108   1 ShellExperienceHost
     94   589.58      31.89       0.00   12144   0 SupportAssistAgent
     30    37.94      43.79       0.00    1340   0 svchost
     21    16.95      16.77       0.00    1500   0 svchost
     24     5.49       5.84       0.00    2968   0 svchost
     11     3.08       5.59       0.00    3168   0 svchost
     17    23.96      23.73       0.00    4452   0 svchost
    103   238.10      37.58       0.00    9124   0 svchost
     16     3.21       6.68       0.00   11928   0 svchost
      0     0.21       2.61       0.00       4   0 System
     56   151.64      72.53     395.14   17088   1 Teams
     34   343.20     250.38     476.20   20272   1 Teams
     84   238.41     132.13     311.61   34104   1 Teams
     32   390.82      15.25       0.00   16848   0 usocoreworker
     69    73.76      21.81     860.73   10152   1 Viscosity
     32    40.79      21.59       0.00    4968   0 ViscosityService

# Complex queries
$procs | where Handles -GT 1000 | Sort-Object -Property Handles | Format-Table Name, Handles -AutoSize

Name                               Handles
----                               -------
svchost                               1013
SupportAssistAgent                    1057
svchost                               1068
ViscosityService                      1069
usocoreworker                         1094
SearchUI                              1104
SearchIndexer                         1117
DellSupportAssistRemedationService    1141
Microsoft.Photos                      1169
pwsh                                  1191
Teams                                 1262
Teams                                 1351
pwsh                                  1370
svchost                               1427
msedge                                1556
csrss                                 1613
jetbrains-toolbox                     1751
SearchUI                              1779
svchost                               1859
lsass                                 1882
Viscosity                             1986
svchost                               2112
ServiceShell                          2129
chrome                                2316
dwm                                   2424
svchost                               2453
igfxEM                                2563
ShellExperienceHost                   2564
Teams                                 2727
svchost                               2812
Code                                  2922
chrome                                3948
explorer                              5117
MsMpEng                               9035
System                               43519
```

### Pipelines

- Pipelines are full compatible (objects) when the object noun is the same
- Typically, at the end of the pipeline data is sent to standard output (screen)
- Default pipeline output: `Out-Default`. Various `Out` cmdlets to transform output of pipeline.
- Sometimes on different nouns, we must use property name __"custom hashmap"__ (as shown below)
- Example map property name `"Id"` to `"procid"`

```Powershell
# Custom output query with custom hash table
# Hash Table syntax
@{name=<key>;expression={<calculated value>}}
# Example
$procs | Select-Object -Property Name, @{name='procid';expression={$_.Id}}
# Useful to also send non-matching Property Names to other cmdlets (adapter pattern)

# Pipeline outputs
# Default Out-Default -> directs to Out-Host
# Other targets
Out-Printer
Out-GridView # Sents to GUI window.
Out-Null # suppress, similar to > /dev/null in bash

# Example
Get-Process | Out-GridView -PassThru | Stop-Process

# Send output to normal commands. Example copy paste
Get-Process | clip

# Send to files (or similar objects from get-psdrive)
Get-Process > file.txt

# Filesystem (get-psdrove: drive, registry, env etc.) operations
Get-Alias del

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           del -> Remove-Item

# > out to file operator
Get-Process | Out-File procs.txt
# Alias cat
Get-Content procs.txt
# Returns an array of strings - similar to readlines()
(Get-Content .\procs.txt).GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Object[]                                 System.Array                                                                                                                                                                                                                                                             PS C:\Users\Ioann> (Get-Content .\procs.txt)[0].GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     String                                   System.Object

# Export Data
Get-Process | Export-Csv procs.csv
Get-Process | Export-Clixml procs.xml

# Cool: When Importing data get serialized back as objects! (kind of)
Import-Csv procs.csv | where {$_.Name -eq "notepad"} | Stop-process
Import-Clixml procs.xml | where {$_.Name -eq "notepad"} | Stop-process

# Example
Get-Process | Export-Csv procs.csv
Import-Csv .\procs.csv | Get-Member
# Or
$procs = Import-Csv .\procs.csv
$procs | Get-Member
# List of properties retained but this time as of PSCustomObject type (loses initial type)

   TypeName: System.Management.Automation.PSCustomObject

Name                       MemberType   Definition
----                       ----------   ----------
Equals                     Method       bool Equals(System.Object obj)
GetHashCode                Method       int GetHashCode()
GetType                    Method       type GetType()
# ...

# Even though import creates objects of PSCustomObject, cmdlets piping works
$procs | where Name -eq "notepad" | Stop-Process
# But Stop-Process takes as input object type <Process[]>
get-help Stop-Process
SYNTAX
    Stop-Process [-Id] <int[]> [-PassThru] [-Force] [-WhatIf] [-Confirm] [<CommonParameters>]

    Stop-Process -Name <string[]> [-PassThru] [-Force] [-WhatIf] [-Confirm] [<CommonParameters>]

    Stop-Process [-InputObject] <Process[]> [-PassThru] [-Force] [-WhatIf] [-Confirm] [<CommonParameters>]

# But it takes also Id or Name as inputs. So it does not work as pass by value, but pass by Property name (Id)

# Let's Try with XML (hint: maintains semantic content - attributes, metadata)
Get-Process | Export-Clixml procs.xml

# Import from xml
$procs = Import-Clixml .\procs.xml
$procs | Get-Member
# This time object type is retained as Deserialized(.System.Diagnostics)
# Deserialized means - NO methods retained - not linked to live processes anymore (Smalltalk ref!)
# On PS-Remoting, usually output is in Deserialized form.
                                                                                                                                                                     TypeName: Deserialized.System.Diagnostics.Process                                                                                                                                                                                                                                                                                Name                       MemberType   Definition
----                       ----------   ----------
GetType                    Method       type GetType()
ToString                   Method       string ToString(), string ToString(string format, System.IFormatProvider formatProvider), string IFormattable.ToString(s…
CommandLine                NoteProperty object CommandLine=null
Company                    NoteProperty object Company=null
CPU                        NoteProperty object CPU=null

```

### Metrics, Filtering & Querying

```Powershell
# Count
Get-Process | Measure-Object

Count             : 479
Average           :
Sum               :
Maximum           :
Minimum           :
StandardDeviation :
Property          :

# Metrics
Get-Process | Measure-Object WorkingSet -Sum -Maximum -Minimum -Average

Count             : 479
Average           : 18063265.9373695
Sum               : 8652304384
Maximum           : 985796608
Minimum           : 8192
StandardDeviation :
Property          : WorkingSet

# Sorting
Get-Process | Sort-Object WorkingSet
# Filter top 5 memory usage (WS)
Get-Process | Sort-Object WorkingSet -Descending -Top 5
# Equivalent
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5

 NPM(K)    PM(M)      WS(M)     CPU(s)      Id  SI ProcessName
 ------    -----      -----     ------      --  -- -----------
      0     3.87     947.04       0.00    2744   0 Memory Compression
     48   584.76     431.21     217.83   30524   1 chrome
     32   498.25     358.98      45.91   36636   1 Code
     98 1,709.70     352.98       0.00   27304   0 MsMpEng
     87   212.82     243.84      52.62   35036   1 pwsh

# Incompatible cmdlet with PS Core. Needs compatibility module. Exists in Windows Powershell.
Get-Eventlog
# Equivalent for PS Core
Get-WinEvent
# Needs Admin
# Get-WinEvent: To access the 'Security' log start PowerShell with elevated user rights.  Error: Attempted to perform an unauthorized operation.
# Get-WinEvent: Log count (441) is exceeded Windows Event Log API limit (256). Adjust filter to return less log names.

# Get newest security log
Get-WinEvent -LogName security -MaxEvents 5

   ProviderName: Microsoft-Windows-Security-Auditing

TimeCreated                     Id LevelDisplayName Message
-----------                     -- ---------------- -------
3/9/2021 12:43:32 AM          5061 Information      Cryptographic operation.…
3/9/2021 12:43:31 AM          5061 Information      Cryptographic operation.…
3/9/2021 12:43:30 AM          5061 Information      Cryptographic operation.…
3/9/2021 12:41:11 AM          4672 Information      Special privileges assigned to new logon.…
3/9/2021 12:41:11 AM          4624 Information      An account was successfully logged on.…

# Get oldest system log
Get-WinEvent -LogName system -MaxEvents 5 -Oldest

   ProviderName: Microsoft-Windows-Kernel-Power

TimeCreated                     Id LevelDisplayName Message
-----------                     -- ---------------- -------
3/3/2020 1:30:25 PM            506 Information      The system is entering connected standby …
3/3/2020 1:33:43 PM            507 Information      The system is exiting connected standby …

   ProviderName: Microsoft-Windows-Kernel-General

TimeCreated                     Id LevelDisplayName Message
-----------                     -- ---------------- -------
3/3/2020 1:33:44 PM             16 Information      The access history in hive \??\C:\ProgramData\Packages\Microsoft.MicrosoftOfficeHub_8wekyb3d8bbwe\S-1-5-21-18…
3/3/2020 1:33:44 PM             16 Information      The access history in hive \??\C:\ProgramData\Packages\Microsoft.MicrosoftOfficeHub_8wekyb3d8bbwe\S-1-5-21-18…

   ProviderName: Microsoft-Windows-DistributedCOM

TimeCreated                     Id LevelDisplayName Message
-----------                     -- ---------------- -------
3/3/2020 1:53:38 PM          10016 Warning          The machine-default permission settings do not grant Local Activation permission for the COM Server applicati…

# Invoke on Remote machines with filtering - avoids getting all events back
Invoke-Command -ComputerName WinBuild02, WinTest01 -ScriptBlock {Get-WinEvent -LogName system -MaxEvents 5}

# Cool fact: PS Remote can work on remote machines with disabled NICs
Get-NetAdapter | Where-Object {$_.Name -like "Ethernet*"}

Name                      InterfaceDescription                    ifIndex Status       MacAddress             LinkSpeed
----                      --------------------                    ------- ------       ----------             ---------
Ethernet 4                VirtualBox Host-Only Ethernet Adapter        24 Up           0A-00-27-00-00-18         1 Gbps
Ethernet                  Realtek USB GbE Family Controller            15 Disconnected 00-E0-4C-68-05-19          0 bps

# Example fix using filtered objects pipeline
Get-NetAdapter | Where-Object {$_.Name -like "Ethernet*"} | Enable-NetAdapter
```

### Comparing sets of data

```Powershell
# Compare two sets of data - show diff
# Can select term of comparison with -Property
Compare-Object

# Example
$procs = Get-Process
$procs2 = Get-Process
Compare-Object -ReferenceObject $procs -DifferenceObject $procs2 -Property Name

Name               SideIndicator
----               -------------
SearchFilterHost   <=
SearchProtocolHost <=
# Reference has the above fields, as indicated by fat arrow.
```

### Advanced Output

```Powershell
# Convert-To Family
# Options
ConvertTo-Html
ConvertTo-Csv
ConvertTo-Json
ConvertTo-SecureString
ConvertTo-Xml

# Use-case specific
ConvertTo-ProcessMitigationPolicy
ConvertTo-TpmOwnerAuth
ConvertTo-AzVMManagedDisk # Is conversion from blob-based to managed-disk based VM
```

### Using Objects - WhatIf

```Powershell
# Use -WhatIf to dry-run a command

# Example: hazard command dry-run
Get-Process | Stop-Process -WhatIf
What if: Performing the operation "Stop-Process" on target "AdminService (4324)".
What if: Performing the operation "Stop-Process" on target "aesm_service (10780)".
What if: Performing the operation "Stop-Process" on target "ApplicationFrameHost (8320)".
What if: Performing the operation "Stop-Process" on target "audiodg (15264)".
What if: Performing the operation "Stop-Process" on target "Calculator (12932)".
What if: Performing the operation "Stop-Process" on target "chrome (3972)".
What if: Performing the operation "Stop-Process" on target "chrome (6228)".
What if: Performing the operation "Stop-Process" on target "chrome (6456)".
# ...

# Use -PassThru to continue piping object (maybe deleting) after a command. Example (mostly stop/delete commands)
Get-ADUser ioannis | Disable-ADAccount -PassThru | Get-Membet | Out-GridView

# -Confirm will always ask before action.
Get-Process -Name notepad | Stop-Process -Confirm

# Lookup cmdlet impact level (documented get-help) if higher or equal to $ConfirmPreference
$ConfirmPreference
High

Get-Process -Name notepad | Stop-Process
# Does not ask for confirm, since impact level is not High

$ConfirmPreference = "Medium"
Get-Process -Name notepad | Stop-Process
# Now asks for confirm

# Override impact level with -Confirm:$false
Get-Process -Name notepad | Stop-Process -Confirm:$false

# Fun fact true, false are object values (primitive of System.ValueType Name: Boolean)
$true
True
$false
False
$true.GetType()

IsPublic IsSerial Name                                     BaseType
-------- -------- ----                                     --------
True     True     Boolean                                  System.ValueType

# Enter PSSession on remote
Enter-PSSession -ComputerName WinBuild02

# Date and timedelta
Get-Date

Tuesday, March 9, 2021 1:18:09 AM                                                                                                                                                                                                                                                                    (Get-Date).AddDays(-7) # 1 week before

Tuesday, March 2, 2021 1:18:15 AM

# Get help on operators
Get-Help *operators*

# $_ refers to each object passed thru the pipeline
# Equivalent $PSItem
Get-Service | where {$PSItem.Status -eq "Stopped"}
# PS Version >= 3, just skip $_, $PSItem
Get-Service | where Status -eq "Stopped"
# Equivalent
Get-Service | ? Status -eq "Stopped"

Get-Alias ? # Alias symbols here look like object macros

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           ? -> Where-Object
Alias           % -> ForEach-Object
Alias           h -> Get-History
Alias           r -> Invoke-History
```

## Mount Azure as PSDrive

```Powershell
Get-PSProvider

Name                 Capabilities                                                                                                Drives
----                 ------------                                                                                                ------
Registry             ShouldProcess                                                                                               {HKLM, HKCU}
Alias                ShouldProcess                                                                                               {Alias}
Environment          ShouldProcess                                                                                               {Env}
FileSystem           Filter, ShouldProcess, Credentials                                                                          {C, Temp}
Function             ShouldProcess                                                                                               {Function}
Variable             ShouldProcess                                                                                               {Variable}
SHiPS                Filter, ShouldProcess                                                                                       {}
Certificate          ShouldProcess                                                                                               {Cert}
WSMan                Credentials                                                                                                 {WSMan}
```

- [https://savilltech.com/2018/03/29/using-the-azure-ps-drive/](https://savilltech.com/2018/03/29/using-the-azure-ps-drive/)
- [https://github.com/PowerShell/AzurePSDrive](https://github.com/PowerShell/AzurePSDrive)
- [Azure Storage PS Reference](https://github.com/uglide/azure-content/blob/master/articles/storage/storage-powershell-guide-full.md)
- [All about PSProviders](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_providers?view=powershell-7.1)

```Powershell
# Sign-In to Azzount Using browser flow
Connect-AzAccount

# Install SHiPS & import module
Install-Module AzurePSDrive
Import-Module AzurePSDrive

# Create PSDrive & mount current Azure Account
New-PSDrive -Name Azure -PSProvider SHiPS -root 'AzurePSDrive#Azure'

Get-PSDrive

Name           Used (GB)     Free (GB) Provider      Root                                                                                                                                                                   CurrentLocation
----           ---------     --------- --------      ----                                                                                                                                                                   ---------------
Alias                                  Alias
Azure                                  SHiPS         AzurePSDrive#Azure                                                                                             PAYG - Development\ResourceGroups\ppe\Microsoft.Compute\virtualMachines
C                 289.24        174.75 FileSystem    C:\                                                                                                                                                                        Users\Ioann
Cert                                   Certificate   \
Env                                    Environment
Function                               Function
HKCU                                   Registry      HKEY_CURRENT_USER
HKLM                                   Registry      HKEY_LOCAL_MACHINE
Temp              289.24        174.75 FileSystem    C:\Users\Ioann\AppData\Local\Temp\
Variable                               Variable
WSMan                                  WSMan

# Navigate to Azure: drive - List and select ops as normal filesystem
cd Azure:
PS Azure:\> dir
                                                                                                                                                                                                                                                Directory: Azure:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Mode SubscriptionName           SubscriptionId                       TenantId                             State                                                                                                                             ---- ----------------           --------------                       --------                             -----
+    Pay-As-You-Go - SMG        36941506-a17d-4852-a9ce-c14edafb2bb4 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 Enabled
+    PAYG - Development         65d32e9a-e358-41bc-8c88-ba0e1fa1c0e4 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 Enabled
+    PAYG - Development Testing 53faa829-4516-4dbc-8e6a-e4637c5ee7f8 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 Enabled
+    PAYG - Migration           d28ea675-da7a-4263-b4ee-faf33c7269e2 8ba9573d-c2ec-4486-a1a3-3b55546c9c64 Enabled

PS Azure:\> cd '.\PAYG - Development\'
PS Azure:\PAYG - Development> dir

    Directory: Azure:\PAYG - Development

Mode Name
---- ----
+    AllResources
+    ResourceGroups
+    StorageAccounts
+    VirtualMachines
+    WebApps

PS Azure:\PAYG - Development> cd .\ResourceGroups\ppe
PS Azure:\PAYG - Development\ResourceGroups\ppe> dir

# Utilize Resources using other Az cmdlets

# Navigate to Microsoft.ContainerRegistry\registries
PS Azure:\PAYG - Development\ResourceGroups\ppe\Microsoft.ContainerRegistry\registries> Get-ChildItem | select @{name='RegistryName';Expression={$_.Name}} | Get-AzContainerRegistryRepository
ppe/libreoffice
ppe/ncc-secure-messages
ppe/ncc-webapp
ppe/ncc-webapp-frontend
tools/azuredisksnapshotter
tools/central-backup
tools/kafka-exact-mirror
tools/mysqlmigration
tools/rook-mons-backup
tools/updater
```

## AzureAD Module - Currently stable only on 5.1

- PS Core Issue [https://github.com/PowerShell/PowerShell/issues/10473](https://github.com/PowerShell/PowerShell/issues/10473)

```Powershell
# Needs admin
Install-Module AzureAD

Import-Module AzureAD
Connect-AzureAD
# PS Core
# Connect-AzureAD: One or more errors occurred. (Could not load type 'System.Security.Cryptography.SHA256Cng' from assembly 'System.Core, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'.): Could not load type 'System.Security.Cryptography.SHA256Cng' from assembly 'System.Core, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089'.

# Remove from current session
Remove-Module AzureAD

Uninstall-Module AzureAD -WhatIf
# Needs admin
Uninstall-Module AzureAD
```

## Powershell Remote

- No RPC implementation (insecure)
- Uses WinRM - WSMAN protocol for remote management over HTTP/S - WinRM is Windows implementation
- WinRM does not use `80/443` ports to avoid conflicts.
- WinRM v >= `1.1` uses default: `5985` HTTP - `5986` HTTPS
- WinRM is __installed by default__ on Windows 2008 R2 and above. __Enabled by default__ on Windows 2012.
- WinRM must be enabled on client OS & other OS using __administrator__ PS.
- View WinRM status with `Get-PSSessionConfiguration` cmdlet.

```Powershell
# On Remote Machine
# Admin PS - Needs ethernet connection marked as private not public
Enable-PSRemoting
WinRM is already set up to receive requests on this computer.
WinRM has been updated for remote management.
WinRM firewall exception enabled.
Configured LocalAccountTokenFilterPolicy to grant administrative rights remotely to local users.

# Verify & show endpoints
PS C:\Windows\system32> Get-PSSessionConfiguration


Name          : microsoft.powershell
PSVersion     : 5.1
StartupScript :
RunAsUser     :
Permission    : NT AUTHORITY\INTERACTIVE AccessAllowed, BUILTIN\Administrators AccessAllowed, BUILTIN\Remote
                Management Users AccessAllowed

Name          : microsoft.powershell.workflow
PSVersion     : 5.1
StartupScript :
RunAsUser     :
Permission    : BUILTIN\Administrators AccessAllowed, BUILTIN\Remote Management Users AccessAllowed

Name          : microsoft.powershell32
PSVersion     : 5.1
StartupScript :
RunAsUser     :
Permission    : NT AUTHORITY\INTERACTIVE AccessAllowed, BUILTIN\Administrators AccessAllowed, BUILTIN\Remote
                Management Users AccessAllowed

# Get Computer Name
$env:COMPUTERNAME
DESKTOP-SVI4OFT

# Default listens on HTTP
winrm enumerate winrm/config/listener
Listener
    Address = *
    Transport = HTTP
    Port = 5985
    Hostname
    Enabled = true
    URLPrefix = wsman
    CertificateThumbprint
    ListeningOn = 10.0.100.160, 127.0.0.1, ::1, fe80::2dba:73ec:a310:f8b6%14
```

Configure HTTPS WinRM:

- [https://docs.microsoft.com/en-us/troubleshoot/windows-client/system-management-components/configure-winrm-for-https](https://docs.microsoft.com/en-us/troubleshoot/windows-client/system-management-components/configure-winrm-for-https)
- [Self signed](https://cloudblogs.microsoft.com/industry-blog/en-gb/technetuk/2016/02/11/configuring-winrm-over-https-to-enable-powershell-remoting/)

### Invoke command

- Can be one-to-many
- Invoke commands to existing session - __useful to persists state between each command__
- Data requested from remote is __deserialized to XML__, sent back & __serialized back to objects__ locally.

```Powershell
# Get computername from remote machine
Invoke-Command -ComputerName DESKTOP-SVI4OFT -ScriptBlock {$env:COMPUTERNAME}
OpenError: [DESKTOP-SVI4OFT] Connecting to remote server DESKTOP-SVI4OFT failed with the following error message : The WinRM client cannot process the request. If the authentication scheme is different from Kerberos, or if the client computer is not joined to a domain, then HTTPS transport must be used or the destination machine must be added to the TrustedHosts configuration setting. Use winrm.cmd to configure TrustedHosts. Note that computers in the TrustedHosts list might not be authenticated. You can get more information about that by running the following command: winrm help config. For more information, see the about_Remote_Troubleshooting Help topic.

# Setup TrustedHosts (Client)
Get-Item WSMan:\localhost\Client\TrustedHosts
Set-Item WSMan:\localhost\Client\TrustedHosts -Value 'machineA,machineB' # Syntax
# Administrator PS
Set-Item WSMan:\localhost\Client\TrustedHosts -Value 'DESKTOP-SVI4OFT'

# Basic auth with HTTP & re-run previous command to test
$cred = Get-Credential

PowerShell credential request
Enter your credentials.
User: admin
Password for user admin: **********

$cred

UserName                     Password
--------                     --------
admin    System.Security.SecureString

Invoke-Command -ComputerName DESKTOP-SVI4OFT -ScriptBlock {$env:COMPUTERNAME} -credential $cred
DESKTOP-SVI4OFT

# Test stateless sessions
Invoke-Command -ComputerName DESKTOP-SVI4OFT -ScriptBlock {$testVar=10} -credential $cred
Invoke-Command -ComputerName DESKTOP-SVI4OFT -ScriptBlock {$testVar} -credential $cred # output of $testVar is blank
```

## Hints & Tips

Importing a module on top of an existing module that is imported (update), use `-Force`:

```Powershell
Import-Module -Path ./MyModule/MyModule.psd1 -Force
```
