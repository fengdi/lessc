# coding=utf-8
# LESS compiler for Sublime Text 2 in windows
# http://www.cnblogs.com/tangoboy/
# Licensed under the WTFPL

import os, sys, re, subprocess, functools, sublime, sublime_plugin

package_name = 'lessc'

#print sys.getdefaultencoding()
#vars()

def lessc(fileroot):
  	config = sublime.load_settings('lessc.sublime-settings'); #配置
	is_compress = config.get('compress') #获取是否压缩的配置
	mode = config.get('mode') #模式

	if(mode=="off"):
		return;
	else:
		tag = load_tag(fileroot+".less")
		if((mode=="white" and tag=="lessc") or (mode=="black" and tag!="!lessc")):

			execmd = '@cscript //nologo "'+sublime.packages_path()+'\\'+package_name+'\\lessc.wsf"'+' "'+fileroot+'.less"'+' "'+fileroot+'.css"'
			
			if is_compress:
				execmd += ' -compress'

			execmd = execmd.encode("gbk") #先将编码转换到gbk

			res = subprocess.Popen(execmd,stdin = subprocess.PIPE,stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
			res.wait()

			error = res.stderr.read()
			print error.decode("gbk")  #解码gbk
			
			remsg = '';
			if error=='':
				remsg = ' ** compild:'+fileroot+'.css ** '
				print remsg
			else:
				errorinfo = error.split("\r\n")
				remsg = errorinfo[2]+"    "+errorinfo[6]+""

			sublime.set_timeout(functools.partial(status,remsg),1200);
			sublime.set_timeout(functools.partial(reloadCss,fileroot),400);


#状态栏消息
def status(msg):
	sublime.status_message(msg)

#重新读取css文件
def reloadCss(fileroot):
	for win in sublime.windows():
		for view in win.views():
			if(view.file_name()==fileroot+".css"):
				view.run_command("reopen",{"encoding": "utf-8" })

def load_tag(f):
	
	file = open(f)
	pattern = re.compile(r'.*#st:(!?lessc).*')

	while 1:
		line = file.readline()
		if not line:
			break
		pass
		m = pattern.match(line)
		if(m):
			return m.group(1)


class EventListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		filepath = view.file_name()
		(fileroot, fileext) = os.path.splitext(filepath)
		if(fileext=='.less'):
			lessc(fileroot)


