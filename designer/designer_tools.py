import datetime
import os
import designer

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
        '''Export playground widget to png file.
        If there is a selected widget, export it.
        If not, export the root widget
        '''
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

    def check_pep8(self):
        '''Check the PEP8 from current project
        '''
        proj_dir = self.designer.project_loader.proj_dir
        kd_dir = os.path.dirname(designer.__file__)
        kd_dir = os.path.split(kd_dir)[0]
        pep8_dir = os.path.join(kd_dir, 'tools', 'pep8checker',
                                'pep8kivy.py')

        python_path =\
            self.designer.designer_settings.config_parser.getdefault(
                'global',
                'python_shell_path',
                ''
            )

        if python_path == '':
            self.profiler.dispatch('on_error', 'Python Shell Path not '
                                   'specified.'
                                   '\n\nUpdate it on \'File\' -> \'Settings\'')
            return

        cmd = '%s %s %s' % (python_path, pep8_dir, proj_dir)
        self.designer.ui_creator.tab_pannel.switch_to(
            self.designer.ui_creator.tab_pannel.tab_list[2])
        self.designer.ui_creator.kivy_console.run_command(cmd)
