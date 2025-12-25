bl_info = {
    "name": "Level and Crop",
    "author": "Daniel Hong",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "location": "Compositor > Sidebar",
    "description": "Correct image tilt and crop in the compositor",
    "category": "Compositing",
}

import bpy, math, cv2
import numpy as np


# ------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------

def computeImageCrop(image_width, image_height, rotation_degrees):
    angle_rad = math.radians(rotation_degrees)
    cos_d = abs(math.cos(angle_rad))
    sin_d = abs(math.sin(angle_rad))
    cos_2d = math.cos(2 * angle_rad)

    # Prevent division by zero at extreme angles
    if abs(cos_2d) < 1e-6:
        return None, None

    cropped_width = (image_width * cos_d - image_height * sin_d) / cos_2d
    cropped_height = (image_height * cos_d - image_width * sin_d) / cos_2d

    return math.floor(cropped_width), math.floor(cropped_height)

def estimateTilt(image):
    """
    Estimate image tilt (in degrees) from a bpy.types.Image.

    Returns a float tilt in degrees, positive = clockwise rotation.
    """
    if image is None:
        print("No image selected")
        return 0

    w, h = image.size
    if w == 0 or h == 0:
        print("Invalid image dimensions")
        return 0

    # Blender stores pixels as flattened floats in RGBA order
    buffer = np.array(image.pixels[:])  # flattened float32 0-1
    buffer = (buffer * 255).astype(np.uint8)
    buffer = buffer.reshape((h, w, 4))  # RGBA image

    # Convert RGBA → BGR for OpenCV
    img = cv2.cvtColor(buffer, cv2.COLOR_RGBA2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crop to central vertical band (ignore top/bottom)
    gray = gray[int(0.25*h):int(0.75*h), :]

    # Improve contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Edge detection
    edges = cv2.Canny(gray, 40, 120)

    # Line Segment Detector
    lsd = cv2.createLineSegmentDetector(0)
    lines = lsd.detect(edges)[0]

    tilt_estimates = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            dx = x2 - x1
            dy = y2 - y1
            length = math.hypot(dx, dy)

            if length < 60:
                continue

            angle = math.degrees(math.atan2(dy, dx))

            # Vertical lines (near ±90°)
            if abs(abs(angle) - 90) < 15:
                tilt = angle - 90 if angle > 0 else angle + 90
                tilt_estimates.append((tilt, length))

            # Horizontal lines (near 0°)
            elif abs(angle) < 10:
                tilt = angle
                tilt_estimates.append((tilt, length))

    if tilt_estimates:
        tilts = np.array([t for t, _ in tilt_estimates])
        weights = np.array([w for _, w in tilt_estimates])

        sorted_idx = np.argsort(tilts)
        tilts = tilts[sorted_idx]
        weights = weights[sorted_idx]

        cumulative = np.cumsum(weights)
        cutoff = cumulative[-1] / 2
        tilt_angle = tilts[np.searchsorted(cumulative, cutoff)]
        rounded_angle = round(tilt_angle, 2)

        return rounded_angle

    # Fallback if no reliable lines found
    print("No reliable lines detected")
    return 0


# ------------------------------------------------------------------------
# Properties
# ------------------------------------------------------------------------

class LevelAndCropProperties(bpy.types.PropertyGroup):
    image: bpy.props.PointerProperty(
        name="Image",
        type=bpy.types.Image,
        description="Image to level and crop"
    )
    
    rotation_degrees: bpy.props.FloatProperty(
        name="Rotation",
        description="Manual rotation override in degrees",
        default=0.0
    )


# ------------------------------------------------------------------------
# Operators
# ------------------------------------------------------------------------

class LEVELANDCROP_OT_estimate_tilt(bpy.types.Operator):
    bl_idname = "levelandcrop.estimate_tilt"
    bl_label = "Estimate Tilt"
    bl_description = "Estimate image tilt automatically"

    def execute(self, context):
        props = context.scene.level_and_crop
        image = props.image

        if image is None:
            self.report({'WARNING'}, "No image selected")
            return {'CANCELLED'}

        tilt = estimateTilt(image)
        props.rotation_degrees = tilt

        self.report({'INFO'}, f"Tilt estimated: {tilt:.2f}°")
        print("[Level and Crop] Tilt estimated:", tilt)

        return {'FINISHED'}

class LEVELANDCROP_OT_overwrite_estimated_tilt(bpy.types.Operator):
    bl_idname = "levelandcrop.overwrite_estimated_tilt"
    bl_label = "Apply Rotation"
    bl_description = "Overwrite the estimated tilt with the manual rotation value"

    def execute(self, context):
        props = context.scene.level_and_crop
        image = props.image
        rotation = props.rotation_degrees

        if image is None:
            self.report({'WARNING'}, "No image selected")
            return {'CANCELLED'}

        width, height = image.size
        if width == 0 or height == 0:
            self.report({'WARNING'}, "Image has invalid dimensions")
            return {'CANCELLED'}

        crop_w, crop_h = computeImageCrop(width, height, rotation)
        if crop_w is None:
            self.report({'WARNING'}, "Rotation too close to 45°, cannot compute crop")
            return {'CANCELLED'}

        scene = context.scene
        scene.render.resolution_x = crop_w
        scene.render.resolution_y = crop_h

        message = (
            f"Render size set to {crop_w}×{crop_h}px "
            f"(from {width}×{height}px @ {rotation:.2f}°)"
        )

        self.report({'INFO'}, message)
        print("[Level and Crop]", message)

        return {'FINISHED'}


# ------------------------------------------------------------------------
# Panel
# ------------------------------------------------------------------------

class LEVELANDCROP_PT_main_panel(bpy.types.Panel):
    bl_label = "Level and Crop"
    bl_idname = "LEVELANDCROP_PT_main_panel"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Level and Crop"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space and space.tree_type == 'CompositorNodeTree'

    def draw(self, context):
        layout = self.layout
        props = context.scene.level_and_crop

        layout.prop(props, "image")
        
        layout.separator()
        
        layout.prop(props, "rotation_degrees")
        
        row = layout.row(align=True)
        row.operator("levelandcrop.estimate_tilt", icon='TRACKING')
        row.operator("levelandcrop.overwrite_estimated_tilt", icon='FILE_REFRESH')


# ------------------------------------------------------------------------
# Register
# ------------------------------------------------------------------------

classes = (
    LevelAndCropProperties,
    LEVELANDCROP_OT_estimate_tilt,
    LEVELANDCROP_OT_overwrite_estimated_tilt,
    LEVELANDCROP_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.level_and_crop = bpy.props.PointerProperty(
        type=LevelAndCropProperties
    )


def unregister():
    del bpy.types.Scene.level_and_crop

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
