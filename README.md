# Nippl

Nippl (Non Interactive Public Player) is a VLC-based media player, specialized in video playing.

It's intended for unattended computers playing advertising and informative media.

## Installing

1. Set up a standard Ubuntu install in the target computer.
2. Install the following packages: `fluxbox` and `VLC Media Player`
3. Drop the nippl package at `$HOME/nippl`.
  - You should have the file `$HOME/nippl/source/nippl.py`.
4. Use the included sample and set up your own settings
  - `$HOME/nippl/source/config.ini`, created from `config.sample.ini`
5. Create a custom X session ($HOME/.xsession):
  - `fluxbox &`
  - `cd nippl/source`
  - `python nippl.py`
6. Set up auto-login to start playing
  1. System -> Administration -> Login Screen
  2. Click the **Unlock** button
  3. Log in as your user with `.xsession`
  4. Select **User Defined Session** as default session
  5. Close
7. Restart computer, unattended startup is ready to use.
