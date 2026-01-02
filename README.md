# Level and Crop
Blender add-on estimates and recommends image tilt and cropped dimensions. Example titled image:

![United 737 Star Alliance SFO arrival - tilted](./assets/examples/United737_StarAlliance_SFO_Arrival_Tilted.JPG)

After tilt correction:

![United 737 Star Alliance SFO arrival - fixed](./assets/examples/United737_StarAlliance_SFO_Arrival_Fixed.JPG)

The add-on optimizes how much image is kept, so your image's original aspect ratio may be lost.

# Installation
Before installing, ensure you have the Python libraries and version listed in the `requirements.txt` file. You can either download this repository as a zip folder or clone it with Git. If you downloaded the zip folder, you will need to unzip it.

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

Replace the Render node with an Image node.

![New Image node](./assets/screenshots/newImageNode_edited.png)

With the new Image node, you can use its Open button to load one of your images. Your selected image will also appear in the backdrop as a preview.

![Sun Country preload](./assets/screenshots/sunCountryPreload.png)

## Remaining Workspace Setup
Keyboard shortcuts for adjusting preview image zoom:
* `V` to zoom out
* `Alt` + `V` to zoom in

So that your original image color quality is preserved, navigate on the right side widget to Render/Color Management/View and change the view to Standard.

![Color Management options](./assets/screenshots/colorManagement.png)

In the Output tab, you can configure resolution, default output folder, image extension, and compression.

![Output settings](./assets/screenshots/outputConfig.png)

## Picking an Image
From the Level and Crop panel, the Image dropdown lists images that you have loaded. From there, you select what image you want to work on.

![Image dropdown](./assets/screenshots/imageDropdown.png)

## Adjusting Rotation

To rotate your image, add a Transform node and input a rotation value in there. Positive values rotate the image __counterclockwise__.

![Transform node](./assets/screenshots/transformNode.png)

To get your new render dimensions after adjustment, input that same rotation value into the Level and Crop widget's Rotation field.

![Rotation input](./assets/screenshots/rotationInput.png)

The add-on will inform you at the bottom of your window that the new image dimension has been computed.

![Render adjustment log](./assets/screenshots/renderAdjustmentLog.png)

You can also see those values updated in the Render tab.

![New dimensions](./assets/screenshots/newDimensions.png)

## Estimating Tilt

You can use the add-on's "Estimate Tilt" button to estimate how much your image should be rotated by to be considered level. When doing so, the add-on will inform you how much your image is tilted by.

![Tilt estimate message](./assets/screenshots/estimateTilt.png)

That value will also be copied to the Level and Crop widget.

![Copied tilt estimate](./assets/screenshots/estimateCopied.png)

Note that the cropped image dimension is not used until you hit "Apply Rotation." If the rotation does not level your image, you can overwrite that value in the Level and Crop widget.