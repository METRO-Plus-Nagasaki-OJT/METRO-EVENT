import os
import winreg

def set_env_variable(name, value, system=False):
    key = winreg.HKEY_LOCAL_MACHINE if system else winreg.HKEY_CURRENT_USER
    key_path = r'SYSTEM\\CurrentControlSet\\Control\Session Manager\\Environment' if system else r'Environment'
    try:
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, name, 0, winreg.REG_EXPAND_SZ, value)
        print(f"Environment variable '{name}' set to '{value}'")
    except PermissionError:
        print("Permission denied. You may need to run this script as an administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

