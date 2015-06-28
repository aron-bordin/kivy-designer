import datetime
import os

from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from designer.helper_functions import ignore_proj_watcher


class DesignerTools(EventDispatcher):

    designer = ObjectProperty()
    '''Instance of Designer
       :data:`designer` is a :class:`~kivy.properties.ObjectProperty`
    '''

    @ignore_proj_watcher
    def export_png(self):
        playground = self.designer.ui_creator.playground
        proj_dir = self.designer.project_loader.proj_dir
        status = self.designer.statusbar

        wdg = playground.selected_widget
        if wdg is None:
            wdg = playground.root

        name = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S.png")
        if wdg.id:
            name = wdg.id + '_' + name
        wdg.export_to_png(os.path.join(proj_dir, name))
        status.show_message('Image saved at ' + name, 5)
