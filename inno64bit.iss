; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{8AA739D1-D334-4A55-A23B-92AEA85E5951}
AppName=AMR Extractor
AppVersion=1.0
;AppVerName=AMR Extractor 1.0
AppPublisher=Thiran Softwares
DefaultDirName={autopf}\AMR Extractor
DisableProgramGroupPage=yes
LicenseFile=D:\Karthikeyan personal\python\my-work\license.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\Users\Karthikeyan\Desktop
OutputBaseFilename=Amr_setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\Karthikeyan personal\python\my-work\build\exe.win32-3.6\AMR.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Karthikeyan personal\python\my-work\build\exe.win32-3.6\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\AMR Extractor"; Filename: "{app}\AMR.exe"
Name: "{autodesktop}\AMR Extractor"; Filename: "{app}\AMR.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AMR.exe"; Description: "{cm:LaunchProgram,AMR Extractor}"; Flags: nowait postinstall skipifsilent

