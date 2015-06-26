from kivy.uix.codeinput import CodeInput
from kivy.properties import BooleanProperty


class DesignerCodeInput(CodeInput):
    '''A subclass of CodeInput to be used for KivyDesigner.
       It has copy, cut and paste functions, which otherwise are accessible
       only using Keyboard.
       It emits on_show_edit event whenever clicked, this is catched
       to show EditContView;
    '''

    __events__ = ('on_show_edit',)

    clicked = BooleanProperty(False)
    '''If clicked is True, then it confirms that this widget has been clicked.
       The one checking this property, should set it to False.
       :data:`clicked` is a :class:`~kivy.properties.BooleanProperty`
    '''

    def on_show_edit(self, *args):
        pass

    def on_touch_down(self, touch):
        '''Override of CodeInput's on_touch_down event.
           Used to emit on_show_edit
        '''

        if self.collide_point(*touch.pos):
            self.clicked = True
            self.dispatch('on_show_edit')

        return super(DesignerCodeInput, self).on_touch_down(touch)

    def _do_focus(self, *args):
        '''Force the focus on this widget
        '''
        self.focus = True

    def do_select_all(self, *args):
        '''Function to select all text
        '''
        self.select_all()
