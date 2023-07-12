from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QCheckBox, QDoubleSpinBox, QFormLayout, QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout, QGroupBox, QLabel,  QWidget
from ..backend.lib import QSpinBox, QDoubleSpinBox

class AppearancePage(QWidget):
    def __init__(self, parent=None):
        super(AppearancePage, self).__init__(parent)

        self.mainLayout = QVBoxLayout(self)
        
        cornersGroup = self.create_corners_group()
        opacityGroup = self.create_opacity_group()
        blur_group = self.create_blur_group()
        shadowGroup = self.create_shadow_group()

        self.mainLayout.addWidget(cornersGroup)
        self.mainLayout.addWidget(opacityGroup)
        self.mainLayout.addWidget(blur_group)
        self.mainLayout.addWidget(shadowGroup)

        self.mainLayout.addStretch(1)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)



    def create_corners_group(self):
        group = QGroupBox("Corners")
        layout = QVBoxLayout()

        layout.addItem(QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # Rounding option
        rounding_label = QLabel("Rounded corners’ radius (in layout px)")
        rounding_spinbox = QSpinBox()
        rounding_spinbox.setValue(0)
        layout.addWidget(rounding_label)
        layout.addWidget(rounding_spinbox)

        # Multisample edges option
        multisample_edges_checkbox = QCheckBox("Enable antialiasing (no-jaggies) for rounded corners")
        multisample_edges_checkbox.setChecked(True)
        layout.addWidget(multisample_edges_checkbox)

        group.setLayout(layout)

        return group


    def create_opacity_group(self):
        group = QGroupBox("Opacity")
        layout = QVBoxLayout()

        layout.addItem(QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # Active opacity option
        active_opacity_label = QLabel("Opacity of active windows")
        active_opacity_spinbox = QDoubleSpinBox()
        active_opacity_spinbox.setRange(0.0, 1.0)
        active_opacity_spinbox.setSingleStep(0.1)
        active_opacity_spinbox.setValue(1.0)
        layout.addWidget(active_opacity_label)
        layout.addWidget(active_opacity_spinbox)

        # Inactive opacity option
        inactive_opacity_label = QLabel("Opacity of inactive windows")
        inactive_opacity_spinbox = QDoubleSpinBox()
        inactive_opacity_spinbox.setRange(0.0, 1.0)
        inactive_opacity_spinbox.setSingleStep(0.1)
        inactive_opacity_spinbox.setValue(1.0)
        layout.addWidget(inactive_opacity_label)
        layout.addWidget(inactive_opacity_spinbox)

        # Fullscreen opacity option
        fullscreen_opacity_label = QLabel("Opacity of fullscreen windows")
        fullscreen_opacity_spinbox = QDoubleSpinBox()
        fullscreen_opacity_spinbox.setRange(0.0, 1.0)
        fullscreen_opacity_spinbox.setSingleStep(0.1)
        fullscreen_opacity_spinbox.setValue(1.0)
        layout.addWidget(fullscreen_opacity_label)
        layout.addWidget(fullscreen_opacity_spinbox)

        group.setLayout(layout)

        return group

    def create_shadow_group(self):
        group = QGroupBox("Shadow")
        layout = QVBoxLayout()

        layout.addItem(QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # Drop shadow option
        drop_shadow_checkbox = QCheckBox("Enable drop shadows on windows")
        drop_shadow_checkbox.setChecked(True)
        layout.addWidget(drop_shadow_checkbox)

        # Shadow range option
        shadow_range_label = QLabel("Shadow range ('size') in layout px")
        shadow_range_spinbox = QSpinBox()
        shadow_range_spinbox.setValue(4)
        layout.addWidget(shadow_range_label)
        layout.addWidget(shadow_range_spinbox)

        # Shadow render power option
        shadow_render_power_label = QLabel("In what power to render the falloff (more power, the faster the falloff)")
        shadow_render_power_spinbox = QSpinBox()
        shadow_render_power_spinbox.setValue(3)
        layout.addWidget(shadow_render_power_label)
        layout.addWidget(shadow_render_power_spinbox)

        # Shadow ignore window option
        shadow_ignore_window_checkbox = QCheckBox("If true, the shadow will not be rendered behind the window itself, only around it")
        shadow_ignore_window_checkbox.setChecked(True)
        layout.addWidget(shadow_ignore_window_checkbox)

        # Shadow color option
        # Here I'm using a QLineEdit for simplicity, but you might want to use a color picker widget
        shadow_color_label = QLabel("Shadow's color. Alpha dictates shadow's opacity")
        shadow_color_lineedit = QLineEdit()
        shadow_color_lineedit.setText("0xee1a1a1a")
        layout.addWidget(shadow_color_label)
        layout.addWidget(shadow_color_lineedit)

        # Inactive shadow color option
        # Here I'm using a QLineEdit for simplicity, but you might want to use a color picker widget
        shadow_inactive_color_label = QLabel("Inactive shadow color. (If not set, will fall back to col.shadow)")
        shadow_inactive_color_lineedit = QLineEdit()
        shadow_inactive_color_lineedit.setText("unset")
        layout.addWidget(shadow_inactive_color_label)
        layout.addWidget(shadow_inactive_color_lineedit)

        # Shadow offset option
        # Here I'm using a QLineEdit for simplicity, but you might want to use a vector input widget
        shadow_offset_label = QLabel("Shadow's rendering offset")
        shadow_offset_lineedit = QLineEdit()
        shadow_offset_lineedit.setText("[0, 0]")
        layout.addWidget(shadow_offset_label)
        layout.addWidget(shadow_offset_lineedit)

        # Shadow scale option
        shadow_scale_label = QLabel("Shadow's scale (0.0 - 1.0)")
        shadow_scale_spinbox = QDoubleSpinBox()
        shadow_scale_spinbox.setRange(0.0, 1.0)
        shadow_scale_spinbox.setValue(1.0)
        layout.addWidget(shadow_scale_label)
        layout.addWidget(shadow_scale_spinbox)

        group.setLayout(layout)

        return group




    def create_blur_group(self):
        group = QGroupBox("Blur")
        layout = QVBoxLayout()

        layout.addItem(QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        # Blur option
        blur_checkbox = QCheckBox("Enable kawase window background blur")
        blur_checkbox.setChecked(True)
        layout.addWidget(blur_checkbox)

        # Blur size option
        blur_size_label = QLabel("Blur size (distance)")
        blur_size_spinbox = QSpinBox()
        blur_size_spinbox.setValue(8)
        layout.addWidget(blur_size_label)
        layout.addWidget(blur_size_spinbox)

        # Blur passes option
        blur_passes_label = QLabel("The amount of passes to perform")
        blur_passes_spinbox = QSpinBox()
        blur_passes_spinbox.setValue(1)
        layout.addWidget(blur_passes_label)
        layout.addWidget(blur_passes_spinbox)

        # Blur ignore opacity option
        blur_ignore_opacity_checkbox = QCheckBox("Make the blur layer ignore the opacity of the window")
        blur_ignore_opacity_checkbox.setChecked(False)
        layout.addWidget(blur_ignore_opacity_checkbox)

        # Blur new optimizations option
        blur_new_optimizations_checkbox = QCheckBox("Whether to enable further optimizations to the blur. Recommended to leave on, as it will massively improve performance")
        blur_new_optimizations_checkbox.setChecked(True)
        layout.addWidget(blur_new_optimizations_checkbox)

        # Blur xray option
        blur_xray_checkbox = QCheckBox("If enabled, floating windows will ignore tiled windows in their blur. Only available if blur_new_optimizations is true. Will reduce overhead on floating blur significantly")
        blur_xray_checkbox.setChecked(False)
        layout.addWidget(blur_xray_checkbox)

        group.setLayout(layout)

        return group


if __name__ == "__main__":
    app = QApplication([])
    window = AppearancePage()
    window.show()
    app.exec()