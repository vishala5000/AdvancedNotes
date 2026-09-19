#define MyAppName "Advanced Notes"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Vishal"
#define MyAppExeName "AdvancedNotes.exe"

[Setup]
AppId={{8E1F4B8D-7F6A-4B35-A2E4-ADVANCEDNOTES}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Advanced Notes
DefaultGroupName=Advanced Notes

OutputDir=installer
OutputBaseFilename=AdvancedNotes-Setup

Compression=lzma
SolidCompression=yes

ArchitecturesAllowed=x86 x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes
PrivilegesRequired=lowest

UninstallDisplayName=Advanced Notes
Uninstallable=yes

WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; \
    Description: "Create a desktop shortcut"; \
    GroupDescription: "Additional icons:"; \
    Flags: unchecked

[Files]
Source: "dist\AdvancedNotes\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Advanced Notes"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{autodesktop}\Advanced Notes"; \
    Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Launch Advanced Notes"; \
    Flags: nowait postinstall skipifsilent
