<h1 align="center">MHGU-MHXX-HP-Overlay-For-Switch-Emulator</h1>

<div align="center">

  [![StaticBadge](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
  [![App](https://img.shields.io/badge/App-1.1.3-green)](https://github.com/Alexander-Lancellott/MHGU-MHXX-HP-Overlay-For-Switch-Emulator)

</div>

## Description

A simple open-source HP overlay that I've developed for MHGU and MHXX Switch Version in Python. This project is a port of another one I previously created called [MH-HP-Overlay-For-3DS-Emulator](https://github.com/Alexander-Lancellott/MH-HP-Overlay-For-3DS-Emulator), but this time it's designed to work with Switch emulators, such as [Ryujinx](https://ryujinx.org/download) and Y\*\*\*, Suda\*\*\* or S\*\*\*, on their PC (Windows) versions.

This overlay uses an AOB (Array of Bytes) scan to locate the memory addresses where each monster's HP values are stored. In my previous project, I was able to use pointers, which is much more efficient and less prone to errors. However, for this project, I had to resort to using AOB scanning because Ryujinx and Y*** do not provide tools to access the game's emulated memory in an orderly and easy manner, as Citra does with a Python script developed by the Citra team that allows external access to the emulated memory with minimal complications. As mentioned earlier, AOB scanning is inefficient because it scans every byte of the entire emulator's memory to find a match for the given pattern. To mitigate this, I reduced the load of this scan by first identifying the memory region where the monsters' HP values are stored and limiting the scan size to that specific chunk of memory instead of scanning the entire emulator memory. Additionally, to minimize the impact on CPU and RAM performance, I created a Python module written in C, which not only reduced the performance impact but also increased execution speed.

I am not sure if the specific memory region used to limit the scan might change in future versions of the emulators. Therefore, in the [compatibility list](#compatibility), besides listing the versions of the games I have tested, I will also include a list of the latest version of each emulator that I have confirmed to work with the overlay.

Although I've conducted numerous tests, the overlay may still contain some bugs that I haven't detected. If you encounter any issues, I would appreciate it if you could report them by opening an issue and providing any evidence that allows for replication.

You can support me by donating! I’d really appreciate it. But either way, thank you for using this mod!

<a href='https://ko-fi.com/B0B115WKYH' target='_blank'>
  <img height='45' style='border:0px;height:45px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' />
</a>

## Compatibility

I think I've managed to make the overlay compatible with the base version and the latest update of MHGU and MHXX. Below is a list of the versions where I tested and confirmed that the overlay works correctly:

- MHGU (USA/EUR) - 0100770008DD8000 - v1.0(default) & v1.4
- MHXX (JPN) - 0100C3800049C000 - v1.0(default) & v1.5.1

Below, I also include a list of the version of each emulator in which I have confirmed the overlay works correctly.

- Ryujinx 1.1.1380 & LDN 3.1.3
- Suda*** 1.0.7
- Y*** EA 4176
- S*** 0.0.3

## High DPI Scaling (optional, only if you notice it)

If your monitor has a resolution higher than 1080p, it's likely you're using a DPI scale above 100%. In this case, the initial position of the overlay may not be the same as when using 100% scaling. To mitigate this, you have three options:

- Set your screen scaling to 100%. You can follow this [guide](https://support.microsoft.com/en-us/windows/view-display-settings-in-windows-37f0e05e-98a9-474c-317a-e85422daa8bb).

- If setting your monitor’s scaling to 100% is not ideal for you, then disable automatic DPI scaling for Ryujinx. To do this, right-click on `Ryujinx.exe`, select Properties, then go to the Compatibility tab. You'll see a checkbox that says, **"Override high DPI scaling behavior."** A drop-down menu will let you choose one of three options. Select `System` or `System Enhanced`. You can find a helpful guide [here](https://www.majorgeeks.com/content/page/how_to_change_dpi_scaling_settings_in_windows.html).

- If neither of the previous options suits you, use the [Fix X & Fix Y](#fix-x--fix-y) options to adjust the overlay more precisely and correct the slight misalignment.

## How to use

To use the overlay, simply open the `MHGU-MHXX-HP-Overlay.exe` file.

> [!IMPORTANT]  
> If the overlay is not working properly, try running it with administrator privileges to ensure it functions correctly. If you're unsure how to do this, you can check this [guide](https://www.majorgeeks.com/content/page/how_to_run_an_app_as_administrator_in_windows_10.html).

If one of the games from the [compatibility list](#compatibility) isn't running in the emulator, you will see a red message in the overlay console saying **No game running** and a countdown starting from 20 minutes. When the countdown reaches zero, the overlay will automatically close to save resources.

![No game running](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/no_game_running_3.webp)

Otherwise, if one of the games from the [compatibility list](#compatibility) is running in the emulator, you will see a green message in the overlay console indicating which of the compatible games is currently running.

![Game running](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/game_running_3.webp)

If everything works correctly, upon starting a hunting mission, you should see `labels` arranged one below the other, displaying the monster's name along with its HP in the top right corner of the game window.

<div align="center">

  ![Labels](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.png)

</div>

If you don't like the color of the overlay or its position in the top right corner of the window, go directly to the [Customize Overlay](#customize-overlay) section to edit it to your liking. However, I recommend that you continue reading this section first.

### Borderless screen system & Native full-screen mode

The full-screen mode in the latest versions of the Ryujinx and Y*** emulators allows the overlay to be visible. However, in Ryujinx LDN 3.1.3, you'll notice that the overlay is not visible in this mode. To address this, I developed a borderless screen system that closely resembles the native full-screen mode of the emulator. This system can be toggled on or off using a keyboard shortcut, which is set to `Ctrl + Alt + F` by default. To exit this mode, simply press the same shortcut again.

It’s important not to confuse this shortcut with the emulator's native shortcut for switching to full-screen mode, which is usually `F11` by default. If you want to change the default keyboard shortcut for the overlay, you can do so by referring to the [Hotkey](#hotkey) subsection.

![Transition](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/transition_2.gif)

Please note that, by default, if you use the overlay’s borderless screen system, the toolbar and the bottom bar of the emulator will still be visible. This differs from the native full-screen mode of the emulator. To achieve a full-screen experience identical to the native one in Ryujinx LDN 3.1.3, you need to go to the Actions menu in the toolbar, click on **Hide UI** to hide both bars, and then modify the `config.ini` file to set the `emu_hide_ui` option from `false` to `true`. Remember to close and restart the overlay, and you can then use `Ctrl + Alt + F` to achieve a native full-screen appearance.

For the latest versions of Ryujinx and Y\*\*\*, you shouldn't have any issues using either the emulator's native full-screen mode or the overlay's borderless screen system. However, if you want to use the borderless screen system in Y\*\*\* and hide the bars, go to the View menu in the toolbar and disable the **Single Window mode** option, which will display another window without the bars.

<table>
  <tr align="center">
    <td>
      <strong>Native full-screen mode</strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="Full-screen"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/native_fullscreen_2.webp"
        style="min-width: 397.5px;" />
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong style="white-space: nowrap;">
        Borderless screen system
      </strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="Borderless"
        src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/borderless_2.webp"
        style="min-width: 397.5px;" />
    </td>
  </tr>
</table>

## Customize Overlay

Inside the root folder, there is a file called `config.ini`, which stores the values for options that can be edited using a text editor like [Notepad++](https://notepad-plus-plus.org/downloads/) to customize the overlay.

**It's important to close and reopen the overlay each time you edit this file for the changes to take effect.**

Below, you will find sub-sections dedicated to documenting each of the available options in the `config.ini`.

### Hotkey & Reset hotkey

The `config.ini` file includes the `hotkey` option, which defines the keyboard shortcut used to toggle the borderless screen system on/off. By default, this shortcut is `Ctrl + Alt + F`. You can replace it with another shortcut if the default one is inconvenient for you.

It's important to note that special keys such as `Ctrl`, `Shift`, or `Alt` are represented by specific symbols. It's recommended to refer to the following [documentation](https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols) to ensure you're using the correct symbols when editing the shortcut. The symbols `*`, `~`, `$` aren't allowed.

In addition, the `config.ini` file also includes a separate option called `reset_hotkey`. This defines a keyboard shortcut used to forcefully reset the overlay in case it becomes frozen or unresponsive due to unexpected behavior. This is especially useful for quickly recovering without having to close and reopen the application manually.

By default, the reset_hotkey is set to `Ctrl + R`. You can change it to any other valid combination that suits your needs.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>hotkey</td>
    <td>^!f</td>
    <td>string</td>
    <td>
      Must be valid hotkey, check this: https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols
    </td>
  </tr>
  <tr align="center">
    <td>reset_hotkey</td>
    <td>^r</td>
    <td>string</td>
    <td>
      Must be valid hotkey, check this: https://www.autohotkey.com/docs/v1/Hotkeys.htm#Symbols
    </td>
  </tr>
</table>

### Debugger

If the `debugger` option in the `config.ini` file is set to `true`, a .log file will be generated where all application logs will be stored. This option is intended solely for testing and troubleshooting, so its default value is `false`.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      debugger
    </td>
    <td>
      false
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Font

Within the `config.ini` file, you can customize the type, weight, and size of the font used in the overlay by editing the following options:

- `font_family`: Allows you to change the font type. You should use fonts that are compatible with the web (**Web Safe Fonts**). You can find a list of these fonts [here](https://www.cssfontstack.com/).
<br>&nbsp;
- `font_weight`: Allows you to adjust the font weight. Common values include `normal` for regular weight and `bold` for bold weight.
<br>&nbsp;
- `font_size`: Allows you to specify the font size in pixels.

Make sure to use **Web Safe Fonts** and to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>font_family</td>
    <td>Consolas, monaco, monospace</td>
    <td>string</td>
    <td>
      This is a <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/font-family">CSS property</a> and must be a <a href="https://www.cssfontstack.com/">Web Safe Font</a>
    </td>
  </tr>
  <tr align="center">
    <td>font_weight</td>
    <td>bold</td>
    <td>string</td>
    <td>
      This is a <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/font-weight">CSS property</a>
    </td>
  </tr>
  <tr align="center">
    <td>font_size</td>
    <td>18</td>
    <td>integer</td>
    <td>
      This is a <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/font-size">CSS property</a>, its value is in pixels and must be greater than or equal to 1
    </td>
  </tr>
</table>

### Max Workers

The `max_workers` option in the `config.ini` file allows you to adjust the maximum number of threads that will parallelize the load and execution of the AOB scan for faster and more efficient CPU performance. The default value is `2`, which should be sufficient in most cases. If your CPU doesn't have very powerful cores, you might consider increasing this value, but even then, performance improvements cannot be guaranteed. The minimum value is `1`, and the maximum is `16`. 

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>max_workers</td>
    <td>2</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 16</td>
  </tr>
</table>

### HP update time

The `hp_update_time` option in the `config.ini` file allows you to adjust the HP value update interval in seconds. The default value is `0.8`, which is equivalent to 800 milliseconds, and the minimum value is `0.1`.

You can modify this value to increase or decrease the time interval for updating the HP value. Higher values will increase the update interval and may improve performance since this overlay uses an AOB scan. If you notice high CPU usage when using it, consider increasing this value. On the other hand, if you have a powerful CPU, you might consider lowering the value to reduce the HP update interval if the default seems too slow.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>hp_update_time</td>
    <td>0.6</td>
    <td>float</td>
    <td>Must be greater than or equal to 0.1</td>
  </tr>
</table>

### Show Initial HP

The `show_initial_hp` option in the `config.ini` file allows you to show or hide each monster's maximum HP. Its default value is set to `true`.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      show_initial_hp
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Show HP Percentage

The `show_hp_percentage` option in the `config.ini` file allows you to show or hide HP as a percentage for each monster. Its default value is set to `true`.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      show_hp_percentage
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Show Small Monsters

The `show_small_monsters` option in the `config.ini` file determines whether the overlay will display all monsters, including small ones. By default, this option is set to `true`.

To display only large monsters, change the value of `show_small_monsters` to `false`.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      show_small_monsters
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Show Size Multiplier & Crown

The `show_size_multiplier` and `show_crown` options in the `config.ini` file allow you to show or hide the size multiplier and crown of each monster.

<div align="center">

![Size Multiplier & Crown](https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/size_multiplier_and_crown.png)

</div>

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      show_size_multiplier
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
  <tr align="center">
    <td>
      show_crown
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Show Abnormal Status

The `show_abnormal_status` option in the `config.ini` file allows you to enable or disable the display of abnormal status for large monsters. To see this information, the monsters must be targeted with the lock-on camera.

<table>
  <tr align="center">
    <td>
      <strong>Monster 1</strong>
    </td>
    <td>
      <strong>Monster 2</strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="abnormal_status"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/jywc9byttd1o7tfmbztw.webp"
      style="max-width: 250px;"/>
    </td>
    <td>
      <img alt="abnormal_status"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_crop,c_thumb,g_face,q_auto:best/MH-HP-Overlay/cm5js4xsjmgd94y3lchr.webp" 
      style="max-width: 250px;"/>
    </td>
  </tr>
</table>

These abnormal statuses are self-explanatory, except for the `Rage` state, which is not an abnormal status but a `timer` that indicates how long the monster will remain enraged. This can be useful, for example, to anticipate when Teostra will unleash its Supernova, as it does so upon exiting its enraged state.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      show_abnormal_status
    </td>
    <td>
      true
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Always show abnormal status

The `always_show_abnormal_status` option in the `config.ini` file allows abnormal statuses to always be displayed without the need to target a monster with the lock-on camera.

<table>
  <tr align="center">
    <td>
      <strong>always_show_abnormal_status = true</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      <img alt="abnormal_status"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/Screenshot_2025-03-16_224548.webp" 
      style="max-width: 290px;"/>
    </td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      always_show_abnormal_status
    </td>
    <td>
      false
    </td>
    <td>
      boolean
    </td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Language

The `language` option in the `config.ini` file allows you to specify the overlay's language. Currently, only two languages are available: `en_US` (default) and `zh_CN`.

I'm not responsible for providing translations, so if the available languages don't suit your needs, you can create your own `.yaml` translation file inside the `locales` folder. Use the `zh_CN.yaml` file as a reference or template.

> [!NOTE]
> In the `language` option of the `config.ini` file, make sure to enter only the filename **without** the `.yaml` extension.

> [!TIP]
> The user [1231joe1231](https://github.com/1231joe1231) contributed both to the `zh_CN.yaml` translation and to the implementation of the internationalization feature.
> If you encounter any issues with that translation, feel free to contact them for help.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      language
    </td>
    <td>
      en_US
    </td>
    <td>
      string
    </td>
    <td>
      You must use one of the available languages from the locales folder by writing only the filename without the .yaml extension, or create your own translation file (.yaml). Except for 'en_US', which does not require a file as it is the default language.
    </td>
  </tr>
</table>

### Position (X & Y)

The `x` and `y` options within the `config.ini` file allow you to adjust the position of the overlay using Cartesian coordinates. These values are relative and percentage-based to the size of the target window, with a minimum range of `0` and maximum of `100` for each coordinate.

- `x`: Controls the horizontal position of the overlay.
<br>&nbsp;
- `y`: Controls the vertical position of the overlay.

Adjust these values to move the overlay to the desired position on the screen.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>x</td>
    <td>100</td>
    <td>integer</td>
    <td>Must be greater than or equal to 0 and less than or equal to 100</td>
  </tr>
  <tr align="center">
    <td>y</td>
    <td>0</td>
    <td>integer</td>
    <td>Must be greater than or equal to 0 and less than or equal to 100</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>x = 100</strong>
      <br>
      <strong>y = 0</strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="x-100"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/x-100.webp"
      style="min-width: 397.5px;" />
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong>x = 0<strong>
      <br>
      <strong>y = 0<strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="x-0"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/x-0.webp"
      style="min-width: 397.5px;" />
    </td>
  </tr>
</table>
<table>
  <tr align="center">
    <td>
      <strong>x = 0<strong>
      <br>
      <strong>y = 100<strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="y-100"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/y-100.webp"
      style="min-width: 397.5px;" />
    </td>
  </tr>
</table>

### Fix X & Fix Y

The `fix_x` and `fix_y` options in the `config.ini` file allow you to adjust the position of the overlay in situations where modifying the `x` and `y` coordinates may not be sufficient. For example, if you want the overlay to extend outside the window to view it on a secondary monitor without obstructing the game's UI, or if changing the opacity or color isn't a solution for you, or when adjusting the `x` and `y` coordinates doesn't adequately address the overlay's placement.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>fix_x</td>
    <td>0</td>
    <td>integer</td>
    <td>It must be any integer, whether positive or negative, its value is in pixels</td>
  </tr>
  <tr align="center">
    <td>fix_y</td>
    <td>0</td>
    <td>integer</td>
    <td>It must be any integer, whether positive or negative, its value is in pixels</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>fix_x = 0</strong>
    </td>
    <td>
      <strong>fix_x = 500</strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="fix-y-0"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/fix_x_0.webp" />
    </td>
    <td>
      <img alt="fix-y-10"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/fix_x_500.webp" />
    </td>
  </tr>
</table>

### Align

Within the `config.ini` file, the `align` option controls the alignment of labels in the overlay. When set to `true`, all labels will adjust their width to match the width of the largest label.

This ensures a consistent and orderly presentation of labels in the overlay interface.

Remember to close and reopen the overlay after making changes to the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>align</td>
    <td>true</td>
    <td>boolean</td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

<table>
  <tr align="center">
    <td>
      <strong>align = true</strong>
    </td>
    <td>
      <strong>align = false</strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="labels"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.webp" />
    </td>
    <td>
      <img alt="align"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/align.webp" />
    </td>
  </tr>
</table>

### Orientation

The `orientation` option within the `config.ini` file allows you to define the position of content within the `labels`. You can configure this option with one of the following values:

- `center`: Centers the content within the `labels`.
<br>&nbsp;
- `left`: Aligns the content to the left within the `labels`.
<br>&nbsp;
- `right`: Aligns the content to the right within the `labels`.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>orientation</td>
    <td>center</td>
    <td>string</td>
    <td>Must be center, left or right</td>
  </tr>
</table>

<table>
  <tr align="center">
    <td colspan="2">
      <strong>align = true</strong>
    </td>
    <td>
      <strong>align = false</strong>
    </td>
  </tr>
  <tr align="center">
    <td>
      <strong>orientation = center</strong>
    </td>
    <td>
      <strong>orientation = left</strong>
    </td>
    <td>
      <strong>orientation = right<strong>
    </td>
  </tr>
  <tr>
    <td>
      <img alt="labels"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/labels.webp" />
    </td>
    <td>
      <img alt="left"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/left.webp" />
    </td>
    <td>
      <img alt="right"
      src="https://res.cloudinary.com/dms5y8rug/image/upload/c_thumb,g_face,q_auto:best/MH-HP-Overlay/right.webp" />
    </td>
  </tr>
</table>

### Emulator Hide UI

The `emu_hide_ui` option in the `config.ini` file, when set to `true`, allows you to remove the top and bottom margins of the overlay. This is useful if these margins are bothersome when the toolbar and bottom bar of the emulator are no longer visible and you want a native fullscreen experience. Its default value is set to `false`.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>emu_hide_ui</td>
    <td>false</td>
    <td>boolean</td>
    <td>
      This is case-insensitive and recognizes boolean values from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
    </td>
  </tr>
</table>

### Color

Within the `config.ini` file, you can customize the color of text and background in the overlay `labels`, as well as their opacity. The available options are as follows:

- `text_color`: Specifies the color of the text within the `labels`. You can use any of the color names from **CSS SVG Colors**. You can view a list of these colors [here](https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg).
<br>&nbsp;
- `background_color`: Defines the background color of the `labels` in the overlay. Similar to text_color, you can use any valid color name from **CSS SVG Colors**.
<br>&nbsp;
- `text_opacity`: Controls the opacity of the text within the `labels`.
<br>&nbsp;
- `background_opacity`: Controls the opacity of the background of the `labels`.
<br>&nbsp;
- `abnormal_status_text_color`: It's the same as `text_color` but for `abnormal status labels`.
<br>&nbsp;
- `abnormal_status_background_color`: It's the same as `background_color` but for `abnormal status labels`.
<br>&nbsp;
- `abnormal_status_text_opacity`: It's the same as `text_opacity` but for `abnormal status labels`.
<br>&nbsp;
- `abnormal_status_background_opacity`: It's the same as `background_opacity` but for `abnormal status labels`.

Adjust these values according to your preferences to customize the visual appearance of the overlay.

Remember to close and reopen the overlay after making changes in the `config.ini` file for these adjustments to take effect.

<table>
  <tr align="center">
    <td>
      <strong>Option</strong>
    </td>
    <td>
      <strong style="white-space: nowrap; ">
        Default value
      </strong>
    </td>
    <td>
      <strong>Type</strong>
    </td>
    <td>
      <strong>Observation</strong>
    </td>
  </tr>
  <tr align="center">
    <td>text_color</td>
    <td>aquamarine</td>
    <td>string</td>
    <td>
      Must be a <a href="https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg">CSS SVG Color</a>
    </td>
  </tr>
  <tr align="center">
    <td>background_color</td>
    <td>darkslategray</td>
    <td>string</td>
    <td>
      Must be a <a href="https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg">CSS SVG Color</a>
    </td>
  </tr>
  <tr align="center">
    <td>text_opacity</td>
    <td>100</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 100</td>
  </tr>
  <tr align="center">
    <td>background_opacity</td>
    <td>60</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 100</td>
  </tr>
  <tr align="center">
    <td>abnormal_status_text_color</td>
    <td>yellow</td>
    <td>string</td>
    <td>
      Must be a <a href="https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg">CSS SVG Color</a>
    </td>
  </tr>
  <tr align="center">
    <td>abnormal_status_background_color</td>
    <td>green</td>
    <td>string</td>
    <td>
      Must be a <a href="https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg">CSS SVG Color</a>
    </td>
  </tr>
  <tr align="center">
    <td>abnormal_status_text_opacity</td>
    <td>100</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 100</td>
  </tr>
  <tr align="center">
    <td>abnormal_status_background_opacity</td>
    <td>50</td>
    <td>integer</td>
    <td>Must be greater than or equal to 1 and less than or equal to 100</td>
  </tr>
</table>

## Building - (For Developers)

```
$ git clone
```

```
$ python -m venv .venv
$ .venv\Scripts\activate
$ pip install .
$ build
```
You will find the `build` in the `build/dist` folder

## Python modules used

- ahk[binary] - v1.8.0
- ahk-wmutil - v0.1.0
- colorama - v0.4.6
- PySide6 - v6.7.2
- Pymem - v1.13.1
- cx_Freeze - v8.0.0
- cursor - v1.3.5
- pywin32 - v306
- numpy - v2.2.4
- art - v6.2
- PyYAML - v6.0.2
