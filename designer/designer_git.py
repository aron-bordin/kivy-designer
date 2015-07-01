from git.exc import InvalidGitRepositoryError
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty, \
    Clock
from designer.helper_functions import ignore_proj_watcher
from designer.uix.designer_action_items import DesignerActionSubMenu, \
        DesignerSubActionButton
from git import Repo

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
        # self._update_menu()

    def _update_menu(self, *args):
        '''Update the Git ActionSubMenu content.
        If a valid repo is open, git tools will be available.
        Is not a git repo, git init is available.
        '''
        self.remove_children()
        if self.is_repo:
            #  TODO check available git tools
            pass
        else:
            btn_init = DesignerSubActionButton(text="Init repo")
            btn_init.bind(on_press=self.do_init)
            self.add_widget(btn_init)

    @ignore_proj_watcher
    def do_init(self, *args):
        '''Git init
        '''
        self.repo = Repo.init(self.path, mkdir=False)
