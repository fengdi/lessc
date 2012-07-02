# LESS compiler for Sublime Text 2 in windows
# http://www.cnblogs.com/tangoboy/
# Licensed under the WTFPL

import os, sys, subprocess, functools, sublime, sublime_plugin

package_name = 'lessc'


def lessc(fileroot):

	is_compress = sublime.load_settings('lessc.sublime-settings').get('compress')

	#execmd = '"'+sublime.packages_path()+'\\'+package_name+'\\lessc.cmd"'+' "'+fileroot+'.less"'+' "'+fileroot+'.css"'
	execmd = '@cscript //nologo "'+sublime.packages_path()+'\\'+package_name+'\\lessc.wsf"'+' "'+fileroot+'.less"'+' "'+fileroot+'.css"'
	
	if is_compress:
		execmd += ' -compress'

	res = subprocess.Popen(execmd,stdout=subprocess.PIPE,shell=True)
	#res.wait()
	remsg = res.stdout.read()

	if remsg=='':
		remsg = ' ** compild:'+fileroot+'.css ** '

	print remsg

	sublime.set_timeout(functools.partial(status,remsg),1200);
	sublime.set_timeout(functools.partial(reloadCss,fileroot),400);


def status(msg):
	sublime.status_message(msg)

def reloadCss(fileroot):
	for win in sublime.windows():
		for view in win.views():
			if(view.file_name()==fileroot+".css"):
				view.run_command("reopen",{"encoding": "utf-8" })

class EventListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		filepath = view.file_name()
		(fileroot, fileext) = os.path.splitext(filepath)
		if(fileext=='.less'):
			lessc(fileroot)


