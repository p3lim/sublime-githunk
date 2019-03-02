import os
import sublime
from sublime_plugin import WindowCommand, TextCommand

settings = None

MODE_TITLE = 'STAGING: '
MESSAGE_DIRTY = 'Please save your changes before attempting hunk staging.'

class plugin_loaded():
	'''
	Called when the plugin is loaded, used to load the settings for the package.
	'''
	global settings
	settings = sublime.load_settings('GitHunk.sublime-settings')


class panel():
	@staticmethod
	def show(msg):
		'''
		Shows the given message in an output panel.

		:param str msg: Message to display
		'''
		window = sublime.active_window()
		panel = window.create_output_panel('githunk')
		panel.set_scratch(True)
		panel.run_command('select_all')
		panel.run_command('right_delete')
		panel.run_command('insert', {'characters': msg})
		window.run_command('show_panel', {'panel': 'output.githunk'})

	@staticmethod
	def hide():
		'''
		Hide any previously displayed panels.
		'''
		window = sublime.active_window()
		window.destroy_output_panel('githunk')

	@staticmethod
	def is_shown():
		'''
		Returns the current shown state of the panel.
		'''
		window = sublime.active_window()
		return not not window.find_output_panel('githunk')

class GitHunkToggleModeCommand(WindowCommand):
	'''
	Toggles the staging mode.
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self):
		view = self.window.active_view()

		if view.is_dirty():
			panel.show(MESSAGE_DIRTY)
			return
		panel.hide()

		if view.settings().get('git_hunk.stage_mode', False) is False:
			# file_path = view.file_name()
			# view.set_name(MODE_TITLE + os.path.basename(file_path))

			# enable mode
			view.settings().set('git_hunk.stage_mode', True)
			view.set_read_only(True)

			# reset cursor
			view.sel().clear()
			view.sel().add(sublime.Region(0, 0))

			# go to first modification
			self.window.run_command('git_hunk_next')
		else:
			# disable mode by closing the view and re-opening the file
			view.settings().set('git_hunk.stage_mode', False)
			view.set_read_only(False)


class GitHunkNextCommand(WindowCommand):
	'''
	Goes to the next available hunk and toggles the inline diff.
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self, force=True):
		view = self.window.active_view()
		view.run_command('next_modification')
		view.run_command('toggle_inline_diff', {'prefer_hide': True})
		# TODO: clear selection?
		# TODO: if the hunk is unselected, the diff colors go out the window :/
		#       maybe color the selection green? use diff.deleted.char and diff.inserted.char colors? idk


class GitHunkPrevCommand(WindowCommand):
	'''
	Goes to the previous available hunk and toggles the inline diff.
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self, force=True):
		view = self.window.active_view()
		view.run_command('prev_modification')
		view.run_command('toggle_inline_diff', {'prefer_hide': True})
		# TODO: clear selection?
		# TODO: if the hunk is unselected, the diff colors go out the window :/
		#       maybe color the selection green? use diff.deleted.char and diff.inserted.char colors? idk


class GitHunkStageCommand(WindowCommand):
	'''
	Stages the hunk and goes to the next available one.
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self, force=True):
		view = self.window.active_view()
		view.set_read_only(False)
		# TODO: stage
		view.set_read_only(True)
		self.window.run_command('save')
		self.window.run_command('git_hunk_next')


class GitHunkRevertCommand(WindowCommand):
	'''
	Reverts the hunk and goes to the next available one.
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self, force=True):
		view = self.window.active_view()
		view.set_read_only(False)
		self.window.run_command('revert_modification') # doesn't work
		view.set_read_only(True)
		self.window.run_command('save')
		self.window.run_command('git_hunk_next')


class GitHunkShowHelpCommand(TextCommand):
	'''
	Toggles help panel.
	'''
	def run(self, edit):
		html = sublime.load_resource('Packages/GitHunk/help.html')
		self.view.show_popup(html, 0, -1, 400, 400)
