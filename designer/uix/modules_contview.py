from kivy.properties import ObjectProperty, Clock, partial
from kivy.uix.actionbar import ContextualActionView
from kivy.modules import screen
import webbrowser
from designer.uix.designer_action_items import DesignerActionProfileCheck


class ModulesContView(ContextualActionView):

    mod_screen = ObjectProperty(None)

    __events__ = ('on_module', )

    def on_module(self, *args, **kwargs):
        '''Dispatch the selected module
        '''
        self.parent.on_previous(self)

    def on_screen(self, *args):
        '''Screen module selected, shows ModScreenContView menu
        '''
        if self.mod_screen is None:
            self.mod_screen = ModScreenContView()
            self.mod_screen.bind(on_run=self.on_screen_module)
        self.parent.add_widget(self.mod_screen)

    def on_screen_module(self, *args, **kwargs):
        '''when running from screen module
        '''
        self.mod_screen.parent.on_previous(self.mod_screen)
        self.dispatch('on_module', *args, **kwargs)

    def on_webdebugger(self, *args):
        '''when running from webdebugger'''
        self.dispatch('on_module', mod='webdebugger', data=[])
        Clock.schedule_once(partial(webbrowser.open,
                                    'http://localhost:5000/'), 5)


class ModScreenContView(ContextualActionView):

    __events__ = ('on_run', )

    def __init__(self, **kwargs):
        super(ModScreenContView, self).__init__(**kwargs)

        # populate emulation devices
        devices = self.ids.module_screen_device
        group = 'screen_device'

        first = True
        for device in sorted(screen.devices):
            btn = DesignerActionProfileCheck(group=group,
                                             allow_no_selection=False,
                                             config_key=device)
            btn.text = screen.devices[device][0]
            btn.checkbox_active = first
            first = False
            devices.add_widget(btn)

    def on_run_press(self, *args):
        '''Run button pressed. Analyze settings and dispatch ModulesContView
                on run
        '''
        device = None
        orientation = None
        scale = None

        for d in self.ids.module_screen_device.list_action_item:
            if d.checkbox.active:
                device = d.config_key
                break

        for o in self.ids.module_screen_orientation.list_action_item:
            if o.checkbox.active:
                orientation = o.config_key
                break

        for s in self.ids.module_screen_scale.list_action_item:
            if s.checkbox.active:
                scale = s.config_key
                break

        parameter = '%s,%s,scale=%s' % (device, orientation, scale)

        self.dispatch('on_run', mod='screen', data=parameter)

    def on_run(self, *args, **kwargs):
        '''Event handler for on_run
        '''
        pass
