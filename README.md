# AxelRuiz Mod List – Fallout 4 VR

**[Discord](https://discord.gg/EHJa5sK3zJ)** · **[Nexus](https://www.nexusmods.com/fallout4/mods/110989)**

A **Fallout 4 VR** mod list installed with Wabbajack. It comes with two Mod Organizer 2 profiles:

- **AxelRuiz - ES**: everything translated into Spanish (mods, MCM and menus).
- **AxelRuiz - EN**: the same list in English.

Current version: **0.7.0** (beta). Bugs are possible: let us know on [Discord](https://discord.gg/EHJa5sK3zJ) and attach your crash log.

### Requirements

1. **Fallout 4 VR** on Steam, a clean install that has been launched once.
2. **Fallout 4 (flat) with all DLC.** Fallout 4 VR does not include the DLC; you must copy them (see below).
3. About **300 GB** free for the install and downloads, on an SSD.
4. A **Nexus Mods** account. Premium downloads automatically; without Premium you'll click "Download" for each mod.
5. A SteamVR-compatible headset. If you use **Virtual Desktop**, enable the optional "OpenComposite (VD)" mod (block 99).

### Copy the DLC (required)

Copy these files from `Fallout 4\Data` to `Fallout 4 VR\Data`:

- `DLCRobot`, `DLCworkshop01`, `DLCCoast`, `DLCworkshop02`, `DLCworkshop03`, `DLCNukaWorld`
- For each one: the `.esm`, all of its `.ba2` files and the `.cdx`.

**Voice language:** DLC voices are in whatever language your flat Fallout 4 is installed in. For English voices, set Fallout 4 and Fallout 4 VR to English in Steam (Properties → Language) before copying.

### Installation

1. Install [Wabbajack](https://www.wabbajack.org/) in a short path such as `C:\Wabbajack`. Not in Program Files or on the Desktop.
2. Add an antivirus (Windows Defender) exclusion for the Wabbajack and install folders.
3. Open Wabbajack, find **AxelRuiz** in the gallery (tick the **Non-featured** box to see it) or load `AxelRuiz.wabbajack`, and choose:
   - Install folder: for example `C:\AxelRuiz`, outside the game folder.
   - Downloads folder: for example `C:\AxelRuiz\downloads`.
4. Click install and wait. The first install takes several hours.
5. Open `ModOrganizer.exe` in the install folder, pick the profile (ES or EN) at the top left and launch **F4SE VR**.

### When starting a new game

- Wait until the messages in the top left disappear, then save and reload.
- Copy the contents of the **Config for Documents** mod (under the "100 Instructions" separator) into `Documents\My Games\Fallout4VR`. It adds the list's `ROCK.toml` (in `Mods_Config\ROCK`, with `FrikUserWeaponOffsets = true`) and tuned grips for several modded weapons (`FRIK_Config\Weapons_Offsets`). Without it, those weapons are held wrong.
- The first time you load into the game, ROCK opens its setup wizard: pick your controllers and the main settings.
- **Sim Settlements 2** (recommended): before leaving the bathroom, use the holotape on top of the toilet and enable the cities. Stay inside until it says they have loaded (about 2 minutes).
- In Settings → Mod Config adjust FRIK, Virtual Holsters, FallUI and the HUD.

### Optionals (block 99)

They come disabled. Enable them in MO2 by ticking their box.

- **OpenComposite (VD)**: Virtual Desktop only. Leave it off if you use regular SteamVR.
- **OCU FO4 (OpenComposite Unleashed)**: experimental alternative to OpenComposite (VD), not fully tested. Don't enable both.
- **Quest Controller Fix**: fixes Meta Quest controllers under SteamVR.
- **Vive Wand Controller Fix**: fixes Vive Wand controllers.
- **Desktop Window VR**: shows the game in a desktop window.
- **No Companion Window**: hides the desktop mirror window (SteamVR only, not with OpenComposite).
- **Dynamic Terrain Deformation** and **Dynamic Bottle Liquids**: visual effects (terrain footprints, liquid in bottles). They add latency, especially with Virtual Desktop.
- **MantellaMod**: AI companions. Requires installing Mantella separately.

### Common problems

- **Game crashes on load:** check that you copied all DLC and are launching F4SE VR from MO2.
- **DLC NPCs have no voice in the EN profile:** your DLC are in another language. Copy them from an English Fallout 4.
- **Voices do not match the profile:** the Steam game language must match the profile (Spanish for ES, English for EN).
- **Wabbajack fails extracting a file:** check your antivirus (it may quarantine it) and try again.

### Open permissions

You may fork, modify and re-upload this modlist under the Wabbajack license. Please rename your fork and do not present it as AxelRuiz. I do not provide support for modified versions.

### Credits

Thanks to every mod author. Mods packed inside the list are included with their authors' permission.
