import time, datetime, os, sys, re, argparse
from os.path import expanduser
from git import *

parser = argparse.ArgumentParser(description='Rename all markdown files to post with Jekyll.')
parser.add_argument('targetpath', help='Target dir', default='./', nargs='?')
parser.add_argument('-f','--force', help='Regenerate all.', default=None, required=False, nargs='*')
parser.add_argument('-r','--revert', help='Revert all.', default=None, required=False, nargs='*')
parser.add_argument('-c','--committed', help='Date from commit.', default=[], required=False, nargs='*')
args = parser.parse_args()

__path__ = expanduser(parser.parse_args().targetpath)
__repo__ = Repo(__path__)
__force__ = args.force is not None
__revert__ = args.revert is not None
__committed__ = args.committed is not None

def commit_by_file(file):
    commits = [c for c in __repo__.iter_commits(paths=[file], max_count=1)]
    return commits[0] if commits else None

for dir, subdirs, files in list(os.walk(__path__, topdown=True)):
    for filename in files:
        if os.path.splitext(filename)[1][1:]=='md':
            file = os.path.join(dir, filename)

            matcher = re.search("(^[0-9]{4}\-[0-9]{2}\-[0-9]{2}\-)", filename)
            if __force__ or matcher if __revert__ else not matcher:
                #get last commit date
                mdate = time.strftime("%Y-%m-%d",time.gmtime(os.path.getmtime(file)))
                commit = commit_by_file(file) if __committed__ and not __revert__ else None
                if commit:
                    mdate = time.strftime("%Y-%m-%d",time.gmtime(commit.committed_date))

                #set target file
                source_filename = filename.replace(matcher.group(0),"") if matcher else filename
                dest_filename = mdate+"-"+source_filename if not __revert__ else source_filename

                os.rename(file, os.path.join(dir, dest_filename))
                print filename ,' > ', dest_filename
