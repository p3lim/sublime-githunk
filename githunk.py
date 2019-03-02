import os
import sublime
from sublime_plugin import WindowCommand

settings = None

MODE_TITLE = 'STAGING: '
MESSAGE_DIRTY = 'Please save your changes before attempting hunk staging.'
MESSAGE_HELP = '''\

	Key Bindings:

[n] next hunk
[p] prev hunk
[h] stage hunk
[d] discard hunk
[?] toggle help

[escape] exit mode

'''

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
		# TODO: re-adjust height to show the text fully

	@staticmethod
	def hide():
		'''
		Hide any previously displayed panels.
		'''
		window = sublime.active_window()
		window.destroy_output_panel('githunk')
		# window.run_command('hide_panel', {'panel': 'output.githunk'})

	@staticmethod
	def is_shown():
		'''
		Returns the current shown state of the panel.
		'''
		window = sublime.active_window()
		return not not window.find_output_panel('githunk')

class GitHunkToggleModeCommand(WindowCommand):
	'''
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self):
		'''
		'''
		view = self.window.active_view()

		if view.is_dirty():
			panel.show(MESSAGE_DIRTY)
			return
		panel.hide()

		if view.settings().get('git_hunk.stage_mode', False) is False:
			file_path = view.file_name()

			# cache the file path
			view.settings().set('git_hunk.file_path', file_path)

			# enable mode
			view.settings().set('git_hunk.stage_mode', True)
			view.set_name(MODE_TITLE + os.path.basename(file_path))
			view.set_read_only(True)

			# TODO: reset cursor top top

			# go to first modification
			self.window.run_command('git_hunk_next')

			if settings.get('show_help', True) is True:
				self.window.run_command('git_hunk_toggle_help', {'force': True})
		else:
			# disable mode by closing the view and re-opening the file
			view.settings().set('git_hunk.stage_mode', False)
			self.window.run_command('close_file')
			self.window.open_file(view.settings().get('git_hunk.file_path'))


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
		# TODO: clear selection
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
		# TODO: clear selection
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
		# TODO: stage
		view.run_command('git_hunk_next')


class GitHunkRevertCommand(WindowCommand):
	'''
	Reverts the hunk and goes to the next available one.
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self, force=True):
		view = self.window.active_view()
		view.run_command('revert_modification') # doesn't work
		view.run_command('git_hunk_next')


class GitHunkToggleHelpCommand(WindowCommand):
	'''
	Toggles help panel.

	:arg bool force: Force the panel to show or hide
	'''
	def run(self, **kwargs):
		sublime.set_timeout_async(lambda: self.run_async(**kwargs), 0)

	def run_async(self, force=None):
		if force is True or not panel.is_shown():
			panel.show(MESSAGE_HELP)
			# pass
		elif force is False or panel.is_shown():
			panel.hide()
			# pass
