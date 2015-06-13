from kivy.adapters.listadapter import ListAdapter
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, \
    ListProperty
from kivy.uix.behaviors import CompoundSelectionBehavior
from kivy.uix.bubble import Bubble
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListView, ListItemButton
from kivy.garden.recycleview import RecycleView
from kivy.uix.relativelayout import RelativeLayout
from time import time


Builder.load_string('''
#:import LinearRecycleLayoutManager kivy.garden.recycleview.LinearRecycleLayoutManager

<CompletionRecycleView>:
	view_layout: layout
    ScrollView:
        id: sv
        on_scroll_y: root.refresh_from_scroll("y")
        on_scroll_x: root.refresh_from_scroll("x")
        on_size: root.request_layout(full=True)
        CompletionRecycleViewLayout:
            id: layout
            size_hint: None, None

<CompletionBubble>
    recycle_view: rv
    size_hint: None, None
    orientation: 'vertical'
    width: 200
    height: 210
    arrow_pos: 'top_mid'
    CompletionRecycleView:
		id: rv
		layout_manager: LinearRecycleLayoutManager(orientation='vertical', default_size='35dp')
		data: root.data
		viewclass: "SuggestionItem"
		canvas.before:
			Color:
				rgba: 0, 0, 0, 0.8
			Rectangle:
				size: self.size

<SuggestionItem>:
	halign: 'left'
	valign: 'middle'
	text_size: self.size
	padding_x: 15
	shorten: True
	shorten_from: 'right'
	canvas.before:
        Color:
			rgba: 1, 1, 1, 0.1 if self.is_selected else 0
		Rectangle:
			pos: self.pos
			size: self.size
	canvas.after:
		Color:
			rgba: 47 / 255., 167 / 255., 212 / 255., 1
		Rectangle:
			pos: self.x, self.y - 1
			size: self.width, 1
''')


class SuggestionItem(Label):
    complete = StringProperty('')
    '''Completion text
    '''

    is_selected = BooleanProperty(False)
    '''Is current item is selected
    '''

    recycle_layout = ObjectProperty(None)
    '''(internal) Reference to CompletionRecycleViewLayout
    '''

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.recycle_layout.select_with_touch(self, touch)
            return True
        return False


class CompletionRecycleView(RecycleView):

    view_layout = ObjectProperty(None)
    '''(internal) Reference to CompletionRecycleViewLayout
    '''


class CompletionRecycleViewLayout(CompoundSelectionBehavior, FloatLayout):

    def __init__(self, **kwargs):
        super(CompletionRecycleViewLayout, self).__init__(**kwargs)

    def select_node(self, node):
        node.is_selected = True
        node_src, idx_src = self._reslove_last_node()
        selectable = self.get_selectable_nodes()
        diff = idx_src - selectable.index(node)
        if diff == -1 and idx_src > 2:  # up
            print(','.join([item.text for item in selectable]))
            self.parent.scroll_to(selectable[-1], 70, False)
        elif diff == 1 and idx_src < 3:  # down
            self.parent.scroll_to(selectable[0], 15, False)
        return super(CompletionRecycleViewLayout, self).select_node(node)

    def deselect_node(self, node):
        node.is_selected = False
        super(CompletionRecycleViewLayout, self).deselect_node(node)

    def select_with_key_down(self, keyboard, scancode, codepoint, modifiers,
                             **kwargs):
        '''Processes a key press. This is called when a key press is to be used
        for selection.
        :Returns:
            bool, True if the keypress was used, False otherwise.
        '''
        if not self.keyboard_select:
            return False
        node_src, idx_src = self._reslove_last_node()

        if scancode[1] in self._offset_counts:  # navigation keys
            node, idx = self.goto_node(scancode[1], node_src, idx_src)
            self.clear_selection()
            self.select_node(node)
            return True
        return False


class CompletionBubble(Bubble):

    recycle_view = ObjectProperty(None)
    '''(internal) Reference a RecycleView with a list of SuggestionItems
       :data:`recycle_view` is a :class:`~kivy.properties.ObjectProperty`
    '''

    recycle_layout = ObjectProperty(None)
    '''(internal) Reference a RecycleViewLayout with a list of SuggestionItems
       :data:`recycle_layout` is a :class:`~kivy.properties.ObjectProperty`
    '''

    keyboard = ObjectProperty(None)
    '''(internal) Keyboard instance to bind events
        :data:`keyboard` is a :class:`~kivy.properties.ObjectProperty`
    '''

    data = ListProperty([])
    ''' List of dicts with data to RecycleView
    :data:`data` is a :class:`~kivy.properties.ListProperty`
    '''

    __events__ = ('on_complete', 'on_cancel', )

    def __init__(self, **kwargs):
        super(CompletionBubble, self).__init__(**kwargs)
        self.recycle_layout = self.recycle_view.view_layout
        self.keyboard =  Window.request_keyboard(None, self)

    def on_window_touch_down(self, win, touch):
        '''Disable the completion if the user clicks anywhere
        '''
        if not self.collide_point(*touch.pos):
            self.dispatch('on_cancel')

    def show_completions(self, completions):
        '''Update the Completion ListView with completions
        '''
        self._restore_recycle()
        if completions == []:
            fake_completion = type('obj', (object,),
                                   {'name': 'No suggestions', 'complete': ''})
            completions.append(fake_completion)
        self.data = self._create_data(completions)
        Window.bind(on_touch_down=self.on_window_touch_down)
        self.keyboard.bind(on_key_down=self.on_key_down)
        self.keyboard.bind(on_key_up=self.recycle_layout.select_with_key_up)

    def _create_data(self, completions):
        for item in completions:
            yield {
                'text': item.name,
                'complete': item.complete,
                'recycle_layout': self.recycle_layout,
            }

    def on_key_down(self, keyboard, scancode, codepoint, modifiers, **kwargs):
        '''Keyboard listener to grab key codes and interact with the
        Completion box
        '''
        # start checking if there is a selected item
        if len(self.recycle_layout.selected_nodes) == 1:
            selected_item = self.recycle_layout.selected_nodes[0]
            if scancode[1] in ['enter', 'tab', 'space']:
                self.dispatch('on_complete', selected_item.complete)
                return True
            else:
                result = self.recycle_layout.select_with_key_down(
                    keyboard, scancode, codepoint, modifiers, **kwargs
                )
                if result:
                    return True
                else: # another key cancel the completion
                    self.dispatch('on_cancel')
                    return False
        elif scancode[1] in ['escape', 'backspace', 'delete']:
            self.dispatch('on_cancel')
            return False
        else:
            # first, remove repeated items from the list
            selectable_nodes = self.recycle_layout.get_selectable_nodes()
            selectable_names = []
            for item in selectable_nodes[:]:
                n = item.text
                if n in selectable_names:
                    selectable_nodes.remove(item)
                else:
                    selectable_names.append(n)

            # then select the first item of the list
            self.recycle_layout.select_node(selectable_nodes[-1])
            if scancode[1] in ['up', 'down']:
                # if using the arrow key, we do nothing because a item was
                # already selected in the above step
                return True
            else: # if not using the arrow key, call CompoundSelectionBehavior
                return self.on_key_down(keyboard, scancode, codepoint,
                                                            modifiers, **kwargs)

    def reposition(self, pos):
        '''Update the Bubble position. Try to display it in the best place of
        the screen
        '''

        # FIXME check why +20
        # TODO update bubble size, position depending the content and screen
        self.x = pos[0] + self.width / 2 + 20
        self.y = pos[1] - self.height

    def _restore_recycle(self):
        '''Clear some recycle view data
        '''
        self.recycle_layout.clear_selection()
        self.recycle_layout.clear_widgets()
        self.data = []

    def _unbind_listeners(self):
        self.keyboard.unbind(on_key_down=self.on_key_down)
        self.keyboard.unbind(on_key_up=self.recycle_layout.select_with_key_up)
        Window.unbind(on_touch_down=self.on_window_touch_down)

    def on_complete(self, *args):
        '''Dispatch a completion selection
        '''
        self._unbind_listeners()


    def on_cancel(self, *args):
        '''Disable key listener on cancel
        '''
        self._unbind_listeners()

if __name__ == '__main__':
    from kivy.app import App
    import jedi

    Builder.load_string('''
<Test>:
    background_normal: ''
    background_color: 1, 0, 1, 1
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.8
        Rectangle:
            pos: self.pos
            size: self.size
    Button:
        text: 'Toggle Completion Menu'
        size_hint: None, None
        width: 250
        height: 50
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press: root.show_bubble()
''')

    class Test(FloatLayout):
        def __init__(self, **kwargs):
            super(Test, self).__init__(**kwargs)
            self.bubble = CompletionBubble(pos=(100, 100))

        def show_bubble(self):
            source = '''
import datetime
datetime.da'''
            script = jedi.Script(source, 3, len('datetime.da'))
            completions = script.completions()
            self.bubble.show_completions(completions)
            self.add_widget(self.bubble)
            self.bubble.bind(on_cancel=self.on_cancel)
            self.bubble.bind(on_complete=self.on_cancel)

        def on_cancel(self, *args):
            if self.bubble.parent is not None:
                self.bubble.show_completions([])
                self.bubble.parent.remove_widget(self.bubble)
                self.is_bubble_visible = False

    class MyApp(App):
        def build(self):
            return Test()

    MyApp().run()
