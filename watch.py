from willie.module import interval
import os

last_file_list = []

@interval(5)
def scan_files(bot):
   global last_file_list

   if not bot.config.has_section("files"):
      return

   path = bot.config.files.path
   prefix = bot.config.files.prefix
  
   new_file_list = os.listdir(path)

   if not last_file_list:
      last_file_list = new_file_list
      return

   new_files = [f for f in new_file_list if f not in last_file_list and not f.startswith("_")]
   if new_files:
      output = "New Images: %s%s" % (prefix, (" %s" % prefix).join(new_files))
      last_file_list = new_file_list
      bot.msg("#boardgamers", output)
   
