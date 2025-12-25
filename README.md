# Level and Crop
Estimates and recommends image tilt and cropped dimensions

# Installation
You can either download this repository as a zip folder or clone it with Git. If you downloaded the zip folder, you will need to unzip it.

![Repo options](./assets/screenshots/repoOptions.png)

To add the extension in Blender, first navigate to Edit/Preferences.

![Edit menu dropdown](./assets/screenshots/editDropdown.png)

From the Preferences left sidebar, select "Add-ons." Then, open the dropdown menu in the top left corner and select "Install from Disk..."

![Add-ons Menu](./assets/screenshots/preferencesMenu.png)

From the file dialog prompt, navigate to and select `levelAndCrop/level_and_crop.py`. You will then see that the add-on is automatically selected.

![Level and Crop selected](./assets/screenshots/selectedAddon.png)

# Usage
The "Level and Crop" panel is in the compositor.

![Level and Crop menu](./assets/screenshots/compositorTab.png)

From there, you will see the following fields:
* Image - the image to work on
* Rotation - how much the image should be rotated by in degrees
* Estimate Tilt - have the add-on estimate the image tilt
* Apply Rotation - Calculate the new render dimension after rotation the image

## Loading an Image
To load an image, first make a new node tree in the compositor.

![New node tree button](./assets/screenshots/newTree.png)