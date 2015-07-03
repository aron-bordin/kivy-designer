from git.exc import InvalidGitRepositoryError
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty, \
    Clock
from kivy.uix.popup import Popup
from pygments.lexers.diff import DiffLexer
from designer.designer_content import DesignerTabbedPanelItem
from designer.helper_functions import ignore_proj_watcher, show_alert, \
    show_message, get_designer
from designer.input_dialog import InputDialog
from designer.uix.designer_action_items import DesignerActionSubMenu, \
        DesignerSubActionButton
from git import Repo
from designer.uix.py_code_input import PyScrollView


class DesignerGit(DesignerActionSubMenu):

    is_repo =  BooleanProperty(False)
    '''Indicates if it's representing a valid git repository
    :data:`is_repo` is a :class:`~kivy.properties.BooleanProperty`, defaults
       to False.
    '''

    path = StringProperty('')
    '''Project path
        :data:`path` is a :class:`~kivy.properties.StringProperty`,
        defaults to ''.
    '''

    repo = ObjectProperty(None)
    '''Instance of Git repository.
        :data:`repo` is a :class:`~kivy.properties.ObjectProperty`, defaults
       to None.
    '''

    diff_code_input = ObjectProperty(None)
    '''Instance of PyCodeInput with Git diff
    :data:`diff_code_input` is a :class:`~kivy.properties.ObjectProperty`,
        defaults to None.
    '''

    def __init__(self, **kwargs):
        super(DesignerGit, self).__init__(**kwargs)
        self._update_menu()

    def load_repo(self, path):
        '''Load a git/non-git repo from path
        '''
        self.path = path
        try:
            self.repo = Repo(path)
            self.is_repo = True
        except InvalidGitRepositoryError:
            self.is_repo = False
        self._update_menu()

    def _update_menu(self, *args):
        '''Update the Git ActionSubMenu content.
        If a valid repo is open, git tools will be available.
        Is not a git repo, git init is available.
        '''
        self.remove_children()
        if self.is_repo:
            btn_commit = DesignerSubActionButton(text='Commit')
            btn_commit.bind(on_press=self.do_commit)

            btn_add = DesignerSubActionButton(text='Add...')
            btn_add.bind(on_press=self.do_add)

            btn_branches = DesignerSubActionButton(text='Branches...')
            btn_branches.bind(on_press=self.do_branches)

            btn_diff = DesignerSubActionButton(text='Diff')
            btn_diff.bind(on_press=self.do_diff)

            self.add_widget(btn_commit)
            self.add_widget(btn_add)
            self.add_widget(btn_branches)
            self.add_widget(btn_diff)
        else:
            btn_init = DesignerSubActionButton(text='Init repo')
            btn_init.bind(on_press=self.do_init)
            self.add_widget(btn_init)
        self._add_widget()

    @ignore_proj_watcher
    def do_init(self, *args):
        '''Git init
        '''
        self.repo = Repo.init(self.path, mkdir=False)
        self.repo.index.commit('Init commit')
        self.is_repo = True
        self._update_menu()
        show_message('Git repo initialized', 5)

    def do_commit(self, *args):
        '''Git commit
        '''
        input = InputDialog('Commit message: ')
        self._popup = Popup(title='Git Commit', content=input,
                            size_hint=(None, None), size=('300pt', '150pt'),
                            auto_dismiss=False)
        input.bind(on_confirm=self._perform_do_commit,
                   on_cancel=self._popup.dismiss)
        self._popup.open()

    @ignore_proj_watcher
    def _perform_do_commit(self, input, *args):
        '''Perform the git commit with data from InputDialog
        '''
        message = input.get_user_input()
        if self.repo.is_dirty():
            self.repo.index.commit(message)
            show_message('Commit: ' + message, 5)
        else:
            show_alert('Git Commit', 'There is nothing to commit')
        self._popup.dismiss()

    @ignore_proj_watcher
    def do_add(self, *args):
        '''Git select files from a list to add
        '''
        files = self.repo.untracked_files

    def do_branches(self, *args):
        '''Shows a list of git branches and allow to change the current one
        '''
        pass

    def do_diff(self, *args):
        '''Open a CodeInput with git diff
        '''
        diff = self.repo.git.diff()

        designer = get_designer()
        designer_content = designer.designer_content
        tabs = designer_content.tab_pannel

        # check if diff is visible on tabbed panel.
        # if so, update the text content
        for i, code_input in enumerate(tabs.list_py_code_inputs):
            if code_input == self.diff_code_input:
                tabs.switch_to(tabs.tab_list[len(tabs.tab_list) - i - 2])
                code_input.text = diff
                return

        # if not displayed, create or add it to the screen
        if self.diff_code_input is None:
            panel_item = DesignerTabbedPanelItem(text='Git diff')
            scroll = PyScrollView()
            _py_code_input = scroll.code_input
            _py_code_input.rel_file_path = 'designer.DesigerGit.diff_code_input'
            _py_code_input.text = diff
            _py_code_input.readonly = True
            _py_code_input.lexer = DiffLexer()
            tabs.list_py_code_inputs.append(_py_code_input)
            panel_item.content = scroll
            self.diff_code_input = panel_item
        else:
            self.diff_code_input.content.code_input.text = diff
        tabs.add_widget(self.diff_code_input)
        tabs.switch_to(tabs.tab_list[0])