print("hello")
"""
PS C:\Users\Madina Zheleu> git config --global user.name "YERGAZY"
PS C:\Users\Madina Zheleu> git config --global user.email "ergazyjeleu@gmail.com"
PS C:\Users\Madina Zheleu> git config --global init.defaultBranch main
PS C:\Users\Madina Zheleu> git config --global core.autocrlf true
PS C:\Users\Madina Zheleu> git config --global core.safecrlf warn
PS C:\Users\Madina Zheleu> mkdir workk


    Каталог: C:\Users\Madina Zheleu


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         9/17/2025  11:15 AM                workk


PS C:\Users\Madina Zheleu> cd workk
PS C:\Users\Madina Zheleu\workk> echo "" > hello.html
PS C:\Users\Madina Zheleu\workk> git init
Initialized empty Git repository in C:/Users/Madina Zheleu/workk/.git/
PS C:\Users\Madina Zheleu\workk> git add hello.html
PS C:\Users\Madina Zheleu\workk> git commit -m "Initial Commit"
[main (root-commit) 4b3943f] Initial Commit
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 hello.html
PS C:\Users\Madina Zheleu\workk> git status
On branch main
nothing to commit, working tree clean
PS C:\Users\Madina Zheleu\workk> Set-Content hello.html '<h1>Hello, World!</h1>'
PS C:\Users\Madina Zheleu\workk> type hello.html
<h1>Hello, World!</h1>
PS C:\Users\Madina Zheleu\workk> git add hello.html
PS C:\Users\Madina Zheleu\workk> git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html

PS C:\Users\Madina Zheleu\workk> git add a.html
fatal: pathspec 'a.html' did not match any files
PS C:\Users\Madina Zheleu\workk> git add b.html
fatal: pathspec 'b.html' did not match any files
PS C:\Users\Madina Zheleu\workk> git commit -m "Changes for a and b"
[main 969e135] Changes for a and b
 1 file changed, 0 insertions(+), 0 deletions(-)
PS C:\Users\Madina Zheleu\workk> git add c.html
fatal: pathspec 'c.html' did not match any files
PS C:\Users\Madina Zheleu\workk> git commit -m "Unrelated change to c"
On branch main
nothing to commit, working tree clean
PS C:\Users\Madina Zheleu\workk> git commit
On branch main
nothing to commit, working tree clean
PS C:\Users\Madina Zheleu\workk> git status
On branch main
nothing to commit, working tree clean
PS C:\Users\Madina Zheleu\workk> Set-Content hello.html "<html>`n  <body>`n    <h1>Hello, World!</h1>`n  </body>`n</html>"
PS C:\Users\Madina Zheleu\workk> git add hello.html
warning: in the working copy of 'hello.html', LF will be replaced by CRLF the next time Git touches it
PS C:\Users\Madina Zheleu\workk> git commit -m "Добавлены теги <html> и <body>"
[main 24f1955] Добавлены теги <html> и <body>
 1 file changed, 5 insertions(+), 1 deletion(-)
PS C:\Users\Madina Zheleu\workk> Set-Content hello.html "<html>`n  <head>`n  </head>`n  <body>`n    <h1>Hello, World!</h1>`n  </body>`n</html>"
PS C:\Users\Madina Zheleu\workk> git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\Users\Madina Zheleu\workk> git commit -m "Added standard HTML page tags"
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\Users\Madina Zheleu\workk> git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\Users\Madina Zheleu\workk> git add .
warning: in the working copy of 'hello.html', LF will be replaced by CRLF the next time Git touches it
PS C:\Users\Madina Zheleu\workk> git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html

PS C:\Users\Madina Zheleu\workk> git commit -m "Added HTML header"
[main 1c5564b] Added HTML header
 1 file changed, 2 insertions(+)
PS C:\Users\Madina Zheleu\workk> git log
commit 1c5564be58d0cc6f2cc18632e390b070cbaa9b25 (HEAD -> main)
Author: YERGAZY <ergazyjeleu@gmail.com>
Date:   Wed Sep 17 11:36:04 2025 +0500

    Added HTML header

commit 24f1955a5e90bfcd88d8c73dbd6eda32e33bb1bf
Author: YERGAZY <ergazyjeleu@gmail.com>
Date:   Wed Sep 17 11:32:01 2025 +0500

    Добавлены теги <html> и <body>

commit 969e135162ce4c1a1afa623c8998eb773dc0fe4b
Author: YERGAZY <ergazyjeleu@gmail.com>
Date:   Wed Sep 17 11:29:26 2025 +0500

    Changes for a and b

commit 4b3943f005674b0737a196bcbd599eb439cc97e4
Author: YERGAZY <ergazyjeleu@gmail.com>
Date:   Wed Sep 17 11:19:31 2025 +0500

    Initial Commit
PS C:\Users\Madina Zheleu\workk> git log --pretty=oneline
1c5564be58d0cc6f2cc18632e390b070cbaa9b25 (HEAD -> main) Added HTML header
24f1955a5e90bfcd88d8c73dbd6eda32e33bb1bf Добавлены теги <html> и <body>
969e135162ce4c1a1afa623c8998eb773dc0fe4b Changes for a and b
4b3943f005674b0737a196bcbd599eb439cc97e4 Initial Commit
PS C:\Users\Madina Zheleu\workk> git log --oneline --max-count=2
1c5564b (HEAD -> main) Added HTML header
24f1955 Добавлены теги <html> и <body>
PS C:\Users\Madina Zheleu\workk> git log --oneline --since="5 minutes ago"
1c5564b (HEAD -> main) Added HTML header
PS C:\Users\Madina Zheleu\workk> git log --oneline --until="5 minutes ago"
24f1955 Добавлены теги <html> и <body>
969e135 Changes for a and b
4b3943f Initial Commit
PS C:\Users\Madina Zheleu\workk> git log --oneline --author="Your Name"
PS C:\Users\Madina Zheleu\workk> git log --oneline --all
1c5564b (HEAD -> main) Added HTML header
24f1955 Добавлены теги <html> и <body>
969e135 Changes for a and b
4b3943f Initial Commit
PS C:\Users\Madina Zheleu\workk> git log --all --pretty=format:"%h %cd %s (%an)" --since="7 days ago"
1c5564b Wed Sep 17 11:36:04 2025 +0500 Added HTML header (YERGAZY)
24f1955 Wed Sep 17 11:32:01 2025 +0500 Добавлены теги <html> и <body> (YERGAZY)
969e135 Wed Sep 17 11:29:26 2025 +0500 Changes for a and b (YERGAZY)
4b3943f Wed Sep 17 11:19:31 2025 +0500 Initial Commit (YERGAZY)
PS C:\Users\Madina Zheleu\workk> git log --pretty=format:"%h %ad | %s%d [%an]" --date=short
1c5564b 2025-09-17 | Added HTML header (HEAD -> main) [YERGAZY]
24f1955 2025-09-17 | Добавлены теги <html> и <body> [YERGAZY]
969e135 2025-09-17 | Changes for a and b [YERGAZY]
4b3943f 2025-09-17 | Initial Commit [YERGAZY]
PS C:\Users\Madina Zheleu\workk> git config --global format.pretty '%h %ad | %s%d [%an]'
PS C:\Users\Madina Zheleu\workk> git config --global log.date short
PS C:\Users\Madina Zheleu\workk> git log
1c5564b 2025-09-17 | Added HTML header (HEAD -> main) [YERGAZY]
24f1955 2025-09-17 | Добавлены теги <html> и <body> [YERGAZY]
969e135 2025-09-17 | Changes for a and b [YERGAZY]
4b3943f 2025-09-17 | Initial Commit [YERGAZY]
PS C:\Users\Madina Zheleu\workk> git log --oneline
1c5564b (HEAD, main) Added HTML header
24f1955 Добавлены теги <html> и <body>
969e135 Changes for a and b
4b3943f Initial Commit
PS C:\Users\Madina Zheleu\workk> git checkout 1c5564b
Note: switching to '1c5564b'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 1c5564b Added HTML header
PS C:\Users\Madina Zheleu\workk> git log --oneline
1c5564b (HEAD, main) Added HTML header
24f1955 Добавлены теги <html> и <body>
969e135 Changes for a and b
4b3943f Initial Commit
PS C:\Users\Madina Zheleu\workk> git checkout 1c5564b
HEAD is now at 1c5564b Added HTML header
PS C:\Users\Madina Zheleu\workk> cat hello.html
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
PS C:\Users\Madina Zheleu\workk> git switch main
Switched to branch 'main'
PS C:\Users\Madina Zheleu\workk> cat hello.html
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
PS C:\Users\Madina Zheleu\workk> git tag v1
PS C:\Users\Madina Zheleu\workk> git log
1c5564b 2025-09-17 | Added HTML header (HEAD -> main, tag: v1) [YERGAZY]
24f1955 2025-09-17 | Добавлены теги <html> и <body> [YERGAZY]
969e135 2025-09-17 | Changes for a and b [YERGAZY]
4b3943f 2025-09-17 | Initial Commit [YERGAZY]
PS C:\Users\Madina Zheleu\workk> git checkout v1^
Note: switching to 'v1^'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:

  git switch -c <new-branch-name>

Or undo this operation with:

  git switch -

Turn off this advice by setting config variable advice.detachedHead to false

HEAD is now at 24f1955 Добавлены теги <html> и <body>
PS C:\Users\Madina Zheleu\workk> cat hello.html
<html>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
PS C:\Users\Madina Zheleu\workk> git tag v1-beta
PS C:\Users\Madina Zheleu\workk> git log
24f1955 2025-09-17 | Добавлены теги <html> и <body> (HEAD, tag: v1-beta) [YERGAZY]
969e135 2025-09-17 | Changes for a and b [YERGAZY]
4b3943f 2025-09-17 | Initial Commit [YERGAZY]
PS C:\Users\Madina Zheleu\workk> git checkout v1
Previous HEAD position was 24f1955 Добавлены теги <html> и <body>
HEAD is now at 1c5564b Added HTML header
PS C:\Users\Madina Zheleu\workk> git checkout v1-beta
Previous HEAD position was 1c5564b Added HTML header
HEAD is now at 24f1955 Добавлены теги <html> и <body>
PS C:\Users\Madina Zheleu\workk> git tag
v1
v1-beta
PS C:\Users\Madina Zheleu\workk> git log main --all
1c5564b 2025-09-17 | Added HTML header (tag: v1, main) [YERGAZY]
24f1955 2025-09-17 | Добавлены теги <html> и <body> (HEAD, tag: v1-beta) [YERGAZY]
969e135 2025-09-17 | Changes for a and b [YERGAZY]
4b3943f 2025-09-17 | Initial Commit [YERGAZY]
PS C:\Users\Madina Zheleu\workk> git switch main
Previous HEAD position was 24f1955 Добавлены теги <html> и <body>
Switched to branch 'main'
PS C:\Users\Madina Zheleu\workk> Set-Content hello.html "<html>`n  <head>`n  </head>`n  <body>`n    <h1>Hello, World!</h1>`n    <!-- This is a bad comment. We want to revert it. -->`n  </body>`n</html>"
PS C:\Users\Madina Zheleu\workk> git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   hello.html

no changes added to commit (use "git add" and/or "git commit -a")
PS C:\Users\Madina Zheleu\workk> git restore hello.html
PS C:\Users\Madina Zheleu\workk> git status
On branch main
nothing to commit, working tree clean
PS C:\Users\Madina Zheleu\workk> cat hello.html
<html>
  <head>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
PS C:\Users\Madina Zheleu\workk> Set-Content hello.html "<html>`n  <head>`n    <!-- This is an unwanted but staged comment -->`n  </head>`n  <body>`n    <h1>Hello, World!</h1>`n  </body>`n</html>"
PS C:\Users\Madina Zheleu\workk> git add hello.html
warning: in the working copy of 'hello.html', LF will be replaced by CRLF the next time Git touches it
PS C:\Users\Madina Zheleu\workk> git status
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   hello.html

PS C:\Users\Madina Zheleu\workk> git restore --staged hello.html
PS C:\Users\Madina Zheleu\workk> git restore hello.html
PS C:\Users\Madina Zheleu\workk> git status
On branch main
nothing to commit, working tree clean
PS C:\Users\Madina Zheleu\workk>
"""
