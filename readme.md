# Extended Interface Scaling

## A UI mod for World of Tanks PC

This mod allows you to scale the UI in World of Tanks PC from 0.7x to 2.0x in 0.1x increments. This is useful for high resolution displays where the UI may be too small to read comfortably.

![extended interface scaling demo](./extended-interface-scaling.gif)

# Installation

This mod is installed by downloading the latest release from the Wargaming Mod portal https://wgmods.net/

Place the .wotmod file inside the mods folder in your World of Tanks installation directory for the latest version of the game.

# Development

## Requirements

- Python 2.7

## Building

> [!NOTE]  
> Python 2.7.18 is required to run the packer.py script.
> If you had Python2.7 installed on your c drive you can point to that version like this
> `C:/Python27/python.exe packer.py`

To build the mod, run the following command in the root directory of the project:

This will run with the default arguments.

```
python packer.py
```

To run the packer.py script with all arguments, use the following command:

```
python packer.py --username ANIALLATOR --name "Extended Interface Scaling" --version 1.0.0 --description "A UI mod for World of Tanks PC" --folder ./res
```

### Paramaters

- `--username` - The username of the mod author
- `--name` - The name of the mod
- `--version` - The version of the mod
- `--description` - A description of the mod
- `--folder` - The folder containing the mod files

C:/Python27/python.exe packer.py --username test

# Credits

StranikS-Scan for the decompiled game files
https://github.com/StranikS-Scan/WorldOfTanks-Decompiled

LockBlock-dev for the packing script
https://github.com/LockBlock-dev/wot-mods/tree/master/auto-packer
